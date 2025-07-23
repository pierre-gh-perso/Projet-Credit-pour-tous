import streamlit as st
import base64
from pathlib import Path

def add_logo(logo_path, height=50):
    logo_bytes = Path(logo_path).read_bytes()
    logo_b64 = base64.b64encode(logo_bytes).decode("utf-8")
    
    st.markdown(
        f'<img src="data:image/png;base64,{logo_b64}" style="height:{height}px;margin-top:10px;">',
        unsafe_allow_html=True
    )

def render_header():
    with open("styles/style.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

    col1, col2 = st.columns([1, 0.2])

    with col1:
        add_logo("assets/logo.png")

    with col2:
        if st.button("🏠 Accueil", use_container_width=True):
            st.session_state.step = 0
            st.session_state.answers = {}
            st.session_state.run_simulation = False
            st.session_state.page = "home"
            st.rerun()

    st.divider()