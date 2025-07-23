import streamlit as st
import pandas as pd
import joblib
import os

@st.cache_resource
def load_simple_proxy_model():
    """
    Charge le modèle proxy SIMPLIFIÉ et sa structure de colonnes.
    """
    base_path = os.path.join("..", "models")
    try:
        assets = {
            "proxy_model": joblib.load(os.path.join(base_path, "chatbot_proxy_model_SIMPLE.pkl")),
            "model_columns": joblib.load(os.path.join(base_path, "chatbot_proxy_model_SIMPLE_columns.pkl")),
        }
        return assets
    except FileNotFoundError as e:
        st.error(f"Erreur : {e}. Entraînez le modèle proxy SIMPLIFIÉ.")
        return None

# Grille tarifaire basée sur l'analyse des données historiques
RATE_GRID = {
    'A': {36: 6.99 / 100, 60: 7.55 / 100}, 'B': {36: 10.49 / 100, 60: 10.99 / 100},
    'C': {36: 13.66 / 100, 60: 14.27 / 100}, 'D': {36: 16.99 / 100, 60: 17.86 / 100},
    'E': {36: 19.99 / 100, 60: 20.99 / 100}, 'F': {36: 23.99 / 100, 60: 24.99 / 100},
    'G': {36: 26.06 / 100, 60: 26.77 / 100},
}

def calculate_monthly_payment(principal, annual_rate_decimal, years=3):
    """Calcule la mensualité d'un prêt."""
    monthly_rate = annual_rate_decimal / 12
    n_payments = int(years * 12)
    if monthly_rate <= 0: return principal / n_payments
    payment = principal * (monthly_rate * (1 + monthly_rate)**n_payments) / ((1 + monthly_rate)**n_payments - 1)
    return payment

def get_loan_proposal(form_data, assets):
    # 1. Prédiction du score de risque
    user_data = pd.DataFrame([form_data])
    user_data_prepared = pd.get_dummies(user_data, drop_first=True, dtype=float)
    user_data_prepared = user_data_prepared.reindex(columns=assets['model_columns'], fill_value=0.0)
    risk_score = assets['proxy_model'].predict(user_data_prepared)[0]
    risk_score = max(0, min(1, risk_score))

    # 2. Logique Métier pour Grade, Décision et Taux
    if risk_score < 0.14:   grade, decision = "A", "✅ Approbation"
    elif risk_score < 0.24: grade, decision = "B", "✅ Approbation"
    elif risk_score < 0.33: grade, decision = "C", "✅ Approbation"
    elif risk_score < 0.41: grade, decision = "D", "⚠️ Analyse Requise"
    elif risk_score < 0.50: grade, decision = "E", "⚠️ Analyse Requise"
    else: grade, decision = "F+", "❌ Refus Prudent"
    
    rate = 0
    if "Refus" not in decision:
        rate = RATE_GRID.get(grade, {}).get(form_data['term'], 0)

    # 3. Calculs financiers
    monthly_payment, total_repaid, credit_cost, final_dti = 0, 0, 0, form_data['dti']
    if rate > 0:
        # On utilise la fonction calculate_monthly_payment
        monthly_payment = calculate_monthly_payment(form_data['loan_amnt'], rate, years=form_data['term'] / 12)
        total_repaid = monthly_payment * form_data['term']
        credit_cost = total_repaid - form_data['loan_amnt']
        
        monthly_income = form_data['annual_inc'] / 12
        current_monthly_debts = (form_data['dti'] / 100) * monthly_income
        final_dti = ((current_monthly_debts + monthly_payment) / monthly_income) * 100

    return {
        "risk_score": risk_score, 
        "grade": grade, 
        "rate": rate,
        "decision": decision, 
        "monthly_payment": monthly_payment,
        "total_repaid": total_repaid,
        "credit_cost": credit_cost,
        "final_dti": final_dti
    }