import streamlit as st
import pandas as pd
import joblib

def render_simulation_page():
    st.title("🧮 Simulation de crédit")
    st.markdown("Remplissez les informations pour simuler un prêt et obtenir un grade prévisionnel.")

    # 🧾 Formulaire utilisateur
    with st.form("form_simulation"):
        montant = st.number_input("💰 Montant du prêt (€)", min_value=1000, max_value=50000, step=500)
        projet = st.selectbox("🎯 Motif du prêt", [
            "credit_card", "car", "home_improvement", "major_purchase", 
            "medical", "moving", "vacation", "other"
        ])
        emp_length = st.selectbox("📅 Ancienneté en années", options=list(range(0, 11)))
        revenu_mensuel = st.number_input("📈 Revenu mensuel (€)", min_value=500, max_value=20000, step=100)
        bouton = st.form_submit_button("🔍 Lancer la simulation")

    # ✅ Le modèle ne se charge et ne tourne que si on clique
    if bouton:
        with st.spinner("Simulation en cours..."):
            model = joblib.load("../models/decision_tree_model.joblib")
            encoder = joblib.load("../models/label_encoder_grade.pkl")

            annual_inc = revenu_mensuel * 12
            features_list = []

            for term in [36, 60]:
                dti = (montant / term) / revenu_mensuel * 100
                row = {
                    "loan_amnt": montant,
                    "term": term,
                    "int_rate": 0.1,
                    "emp_length": emp_length,
                    "annual_inc": annual_inc,
                    "dti": dti,
                    f"purpose_{projet}": 1
                }
                features_list.append(row)

            df_input = pd.DataFrame(features_list)

            # Ajouter les colonnes manquantes attendues par le modèle
            for col in model.feature_names_in_:
                if col not in df_input.columns:
                    df_input[col] = 0
            df_input = df_input[model.feature_names_in_]

            # 🔮 Prédiction
            preds = model.predict(df_input)
            grades = encoder.inverse_transform(preds)

            taux_estimes = {
                "A": 6.0, "B": 9.0, "C": 12.0,
                "D": 15.0, "E": 18.0, "F": 22.0, "G": 25.0
            }

            # 📊 Résultats
            st.success("📊 Résultats de la simulation")
            st.write(f"📆 **Durée 36 mois** : Grade **{grades[0]}**, taux estimé : **{taux_estimes[grades[0]]}%**")
            st.write(f"📆 **Durée 60 mois** : Grade **{grades[1]}**, taux estimé : **{taux_estimes[grades[1]]}%**")
            st.write("🔍 Données envoyées au modèle :", df_input.head())

    if st.button("⬅️ Retour"):
        st.session_state.page = "home"