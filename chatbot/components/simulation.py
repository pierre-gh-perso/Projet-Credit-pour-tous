# chatbot/components/simulation.py

import streamlit as st
import pandas as pd
import joblib
import os

# --- Configuration et Chargement du Modèle Proxy ---

@st.cache_resource
def load_proxy_model():
    """
    Charge le modèle proxy et sa structure de colonnes.
    """
    base_path = os.path.join("..", "models")
    try:
        assets = {
            "proxy_model": joblib.load(os.path.join(base_path, "chatbot_proxy_model.pkl")),
            "model_columns": joblib.load(os.path.join(base_path, "chatbot_proxy_model_columns.pkl")),
        }
        return assets
    except FileNotFoundError as e:
        st.error(f"Erreur de chargement : {e}. Assurez-vous d'avoir entraîné et sauvegardé le modèle proxy (notebook 13).")
        return None

# --- Interface Utilisateur et Logique de Prédiction ---

def render_simulation_page():
    st.title("🧮 Simulation de Risque Crédit")
    st.markdown("Remplissez les informations ci-dessous pour obtenir une évaluation du risque.")

    assets = load_proxy_model()
    if not assets:
        return

    # --- Formulaire de simulation ---
    with st.form(key="simulation_form"):
        st.subheader("Informations sur le Prêt et le Client")
        
        col1, col2 = st.columns(2)
        with col1:
            loan_amnt = st.number_input("Montant du prêt (€)", 500, 40000, 15000, 500)
            annual_inc = st.number_input("Revenu annuel (€)", 10000, 1000000, 60000, 1000)
            purpose = st.selectbox("Motif du prêt", ['debt_consolidation', 'credit_card', 'home_improvement', 'other'])

        with col2:
            dti = st.number_input("Ratio d'endettement (DTI)", 0.0, 100.0, 20.0, 0.1)
            emp_length = st.slider("Ancienneté pro. (années)", 0, 10, 5)
            home_ownership = st.selectbox("Type de propriété", ['MORTGAGE', 'RENT', 'OWN'])

        with st.expander("Détails sur l'endettement et l'historique de crédit"):
            col3, col4 = st.columns(2)
            with col3:
                revol_bal = st.number_input("Solde total crédits renouvelables (€)", 0, 200000, 10000, 100)
                revol_util = st.slider("Utilisation crédit renouvelable (%)", 0, 150, 50)
                total_acc = st.slider("Nombre total de comptes de crédit", 1, 100, 20)
                open_acc = st.slider("Nombre de comptes de crédit ouverts", 1, 50, 10)

            with col4:
                mort_acc = st.slider("Nombre de crédits immobiliers", 0, 20, 1)
                pub_rec = st.slider("Incidents de paiement publics", 0, 20, 0)
                pub_rec_bankruptcies = st.slider("Faillites enregistrées", 0, 10, 0)

        submit_button = st.form_submit_button(label="📈 Lancer l'évaluation du risque")
    
    # --- Logique de Prédiction et d'Affichage ---
    if submit_button:
        with st.spinner("Analyse du profil en cours..."):
            
            # 1. Collecte des données du formulaire
            user_data = pd.DataFrame([{
                'loan_amnt': float(loan_amnt), 'annual_inc': float(annual_inc), 'dti': float(dti),
                'revol_bal': float(revol_bal), 'revol_util': float(revol_util), 'emp_length': float(emp_length),
                'home_ownership': home_ownership, 'purpose': purpose, 'total_acc': float(total_acc),
                'open_acc': float(open_acc), 'mort_acc': float(mort_acc), 'pub_rec': float(pub_rec),
                'pub_rec_bankruptcies': float(pub_rec_bankruptcies),
                # Ajout des champs fixes pour la cohérence avec l'entraînement
                'term': 36.0, 'verification_status': 'Verified'
            }])

            # 2. Préparation des données pour le modèle proxy
            user_data_prepared = pd.get_dummies(user_data, drop_first=True, dtype=float)
            user_data_prepared = user_data_prepared.reindex(columns=assets['model_columns'], fill_value=0.0)
            
            # 3. Prédiction avec le modèle proxy
            risk_score = assets['proxy_model'].predict(user_data_prepared)[0]
            # On s'assure que le score reste dans les bornes [0, 1]
            risk_score = max(0, min(1, risk_score))

        # 4. Affichage du résultat
        st.subheader("Résultats de l'Évaluation de Risque")
        col_res1, col_res2 = st.columns(2)
        
        with col_res1:
            st.metric(label="Score de Risque de Défaut Estimé", value=f"{risk_score:.2%}")

        with col_res2:
            if risk_score < 0.25:
                st.success("✅ **Profil Standard - Risque Faible**")
            elif risk_score < 0.50:
                st.warning("⚠️ **Profil Atypique - Risque Modéré**")
            else:
                st.error("❌ **Profil Anormal - Risque Élevé**")

    if st.button("⬅️ Nouvelle simulation"):
        st.rerun()