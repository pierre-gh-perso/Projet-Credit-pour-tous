import streamlit as st
import numpy as np
import pandas as pd
import joblib

def render():
    st.subheader("🧮 Simuler une demande de crédit")

# 📦 Chargement du modèle et de l'encodeur
@st.cache_resource
def load_model():
    model = joblib.load("../../models/decision_tree_model.joblib")
    encoder = joblib.load("../../models/label_encoder_grade.pkl")
    return model, encoder

model, encoder = load_model()

st.subheader("🧮 Simuler une demande de crédit")

# 📋 Formulaire utilisateur
with st.form("formulaire_credit"):
    loan_amnt = st.number_input("💰 Montant du prêt souhaité (€)", min_value=500, max_value=40000, step=500)
    term = st.selectbox("📅 Durée du prêt", [36, 60])
    annual_inc = st.number_input("💼 Revenu annuel (€)", min_value=1000, max_value=1000000, step=1000)
    emp_length = st.selectbox("🕒 Ancienneté professionnelle (en années)", list(range(0, 11)))
    home_ownership = st.selectbox("🏠 Statut du logement", ["OWN", "RENT", "MORTGAGE", "OTHER"])
    dti = st.slider("💳 DTI (Debt-to-Income %)", 0.0, 45.0, step=0.1)
    revol_util = st.slider("📈 Utilisation du crédit renouvelable (%)", 0.0, 100.0, step=0.1)
    purpose = st.selectbox("🎯 Objet du crédit", ["credit_card", "car", "home_improvement", "debt_consolidation", "other"])
    application_type = st.selectbox("👥 Type de demande", ["INDIVIDUAL", "JOINT"])

    submitted = st.form_submit_button("📊 Lancer la simulation")

if submitted:
    # 🎯 Préparation des données
    input_data = pd.DataFrame([{
        'loan_amnt': loan_amnt,
        'term': term,
        'annual_inc': annual_inc,
        'emp_length': emp_length,
        'home_ownership': home_ownership,
        'dti': dti,
        'revol_util': revol_util,
        'purpose': purpose,
        'application_type': application_type
    }])

    # 🧪 Encodage des variables catégorielles
    input_data_encoded = pd.get_dummies(input_data)
    
    # Harmonisation des colonnes (au cas où il manque des colonnes du modèle)
    model_features = model.feature_names_in_
    for col in model_features:
        if col not in input_data_encoded.columns:
            input_data_encoded[col] = 0
    input_data_encoded = input_data_encoded[model_features]

    # 🔮 Prédiction
    grade_pred = model.predict(input_data_encoded)[0]
    grade_label = encoder.inverse_transform([grade_pred])[0]

    # 💬 Résultats
    st.success(f"✅ Simulation terminée : Le grade prévisionnel est **{grade_label}**")

    if grade_label in ["A", "B"]:
        st.markdown("🟢 **Prêt accordé** - Conditions favorables")
    elif grade_label in ["C", "D"]:
        st.markdown("🟡 **Prêt accordé** - Conditions à évaluer avec prudence")
    else:
        st.markdown("🔴 **Prêt refusé** - Risque trop élevé")

    # Calcul des mensualités simulées (optionnel)
    taux_simulé = 0.08 + 0.02 * (ord(grade_label) - ord("A"))  # taux entre 8% et 18%
    mensualite = (loan_amnt * taux_simulé / 12) / (1 - (1 + taux_simulé / 12)**(-term))

    st.markdown(f"""
    ---
    📈 **Taux simulé** : {round(taux_simulé * 100, 2)}%  
    💸 **Mensualité estimée** : {round(mensualite, 2)} €  
    📆 **Durée** : {term} mois
    """)