import streamlit as st
from components.home import render_home
from components.simulation import render_simulation_page

# 🎨 Configuration globale
st.set_page_config(
    page_title="Crédit pour Tous - Assistant",
    page_icon="💼",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# 🧭 Initialisation de l’état
if "page" not in st.session_state:
    st.session_state.page = "home"

# 🧭 Navigation entre les pages
if st.session_state.page == "home":
    render_home()
elif st.session_state.page == "simulation":
    render_simulation_page()