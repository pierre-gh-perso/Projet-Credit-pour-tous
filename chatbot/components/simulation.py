import streamlit as st
from .simulation_logic import load_simple_proxy_model, get_loan_proposal
from .simulation_ui import render_questionnaire, display_results

def render_simulation_page():
    st.title("Simulateur de Prêt")
    st.divider()
    st.markdown("""
        Ce simulateur permet de tester l'éligibilité d'un scénario de prêt en fonction des données du client.
        Répondez aux questions ci-dessous pour obtenir une proposition personnalisée.
    """)
    if 'step' not in st.session_state:
        st.session_state.step = 0
    if 'answers' not in st.session_state:
        st.session_state.answers = {}
    if 'run_simulation' not in st.session_state:
        st.session_state.run_simulation = False

    assets = load_simple_proxy_model()
    if not assets: return

    if st.session_state.run_simulation:
        form_data = st.session_state.answers
        
        form_data['verification_status'] = 'Verified'

        if form_data['dti'] > 50 or form_data['annual_inc'] < 15000 or form_data['loan_amnt'] > form_data['annual_inc']:
            st.error("❌ **Refus Automatique** : Le profil ne respecte pas les critères de base.")
        else:
            with st.spinner("Analyse du profil en cours..."):
                results = get_loan_proposal(form_data, assets)
            display_results(results, form_data)
        
        if st.button("🔄 Lancer une nouvelle simulation"):
            st.session_state.step = 0
            st.session_state.answers = {}
            st.session_state.run_simulation = False
            st.rerun()
            
    else:
        render_questionnaire()