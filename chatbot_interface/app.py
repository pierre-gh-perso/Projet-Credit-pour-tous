import streamlit as st

# 🎨 Configuration de la page
st.set_page_config(
    page_title="Crédit pour Tous - Assistant",
    page_icon="💼",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# 🖼️ En-tête
st.title("💼 Crédit pour Tous")
st.markdown("Bienvenue dans l’assistant de simulation et de suivi de crédits.\n\nSélectionnez une option ci-dessous.")

# 🔘 Choix d'action
option = st.selectbox(
    "Que souhaitez-vous faire ?",
    [
        "🔍 Consulter les statuts de prêts",
        "🧮 Tester une simulation de crédit"
    ]
)

# 🚀 Actions selon le choix
if option == "🔍 Consulter les statuts de prêts":
    st.markdown("👉 Rendez-vous sur la page de consultation des prêts.")
    # Plus tard : rediriger ou afficher loan_status()
elif option == "🧮 Tester une simulation de crédit":
    st.markdown("👉 Lancez une simulation pour évaluer un scénario de crédit.")
    # Plus tard : rediriger ou afficher test_credit()

    # 📁 app.py
import streamlit as st
from components import home, test_credit  # Ajoute d'autres pages si besoin

# 🧭 Menu de navigation
st.sidebar.title("🧭 Navigation")
page = st.sidebar.radio("Aller à :", ["🏠 Accueil", "💳 Simuler un crédit"])

# 📄 Affichage des pages
if page == "🏠 Accueil":
    home.render()
elif page == "💳 Simuler un crédit":
    test_credit.render()
