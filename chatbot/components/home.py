import streamlit as st

def render_home():
    st.markdown("""
        Bienvenue dans l’assistant intelligent de **Crédit pour Tous**. 
        Utilisez les outils ci-dessous pour explorer les crédits existants ou simuler un nouveau scénario.
    """)

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("📊 Dashboard des Prêts")
        st.markdown("Consultez les indicateurs clés et les statistiques des prêts enregistrés.")
        if st.button("🔍 Afficher le Dashboard"):
            st.session_state.page = "dashboard"
            st.rerun()

    with col2:
        st.subheader("🧮 Simulation de crédit")
        st.markdown("Testez l’éligibilité d’un scénario de prêt à partir de vos données.")
        if st.button("🚀 Lancer une simulation"):
            st.session_state.page = "simulation"
            st.rerun()