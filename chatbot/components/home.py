import streamlit as st

def render_home():
    st.title("💼 Crédit pour Tous")
    st.markdown("""
        Bienvenue dans l’assistant intelligent de **Crédit pour Tous**.  
        Utilisez les outils ci-dessous pour explorer les crédits existants ou simuler un nouveau scénario.
    """)

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("📊 Statut des prêts")
        st.markdown("Consultez les dossiers et l’état d’avancement des prêts enregistrés.")
        st.button("🔍 Voir les statuts", key="go_status")  # À implémenter plus tard

    with col2:
        st.subheader("🧮 Simulation de crédit")
        st.markdown("Testez l’éligibilité d’un scénario de prêt à partir de vos données.")
        if st.button("🚀 Lancer une simulation"):
            st.session_state.page = "simulation"