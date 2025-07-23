import streamlit as st
import pandas as pd
import plotly.express as px

@st.cache_data
def load_data():
    """Charge les données nettoyées finales."""
    path = "../data/processed/dataset_clean_no_outliers.parquet"
    df = pd.read_parquet(path)
    if 'loan_status' in df.columns:
        df['is_default'] = (df['loan_status'] == 'Charged Off')
    return df

def render_dashboard_page():
    st.title("📊 Dashboard des Prêts")
    st.markdown("Vue d'ensemble du portefeuille de prêts existants.")

    df = load_data()
    
    # --- Indicateurs Clés (KPIs) ---
    st.subheader("Indicateurs Clés")
    
    total_loans = len(df)
    total_loan_amount = df['loan_amnt'].sum()
    avg_interest_rate = df['int_rate'].mean()
    default_rate = df['is_default'].mean()

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Nombre de Prêts", f"{total_loans:,}".replace(',', ' '))
    col2.metric("Montant Total Prêté", f"{int(total_loan_amount/1_000_000)} M€")
    col3.metric("Taux d'Intérêt Moyen", f"{avg_interest_rate :.2f} %")
    col4.metric("Taux de Défaut Global", f"{default_rate * 100:.2f} %", delta_color="inverse")

    st.divider()

    col5, col6 = st.columns(2)

    with col5:
        st.subheader("Top 5 des Motifs de Prêt")
        purpose_counts = df['purpose'].value_counts().nlargest(5)
        fig_purpose = px.pie(purpose_counts, values=purpose_counts.values, names=purpose_counts.index, hole=0.3)
        fig_purpose.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig_purpose, use_container_width=True)

    with col6:
        st.subheader("Répartition par Catégorie Socio-Pro.")
        csp_counts = df['csp_category'].value_counts()
        st.bar_chart(csp_counts)
    
    st.divider()

    #Distribution des Montants de Prêts
    st.subheader("Distribution des Montants de Prêts")
    fig_hist = px.histogram(
        df,
        x="loan_amnt",
        nbins=50,
        title="Fréquence des Montants de Prêts",
        labels={'loan_amnt': 'Montant du Prêt (€)'}
    )
    st.plotly_chart(fig_hist, use_container_width=True)

    st.divider()

    #Taux de Défaut par Grade et Durée
    st.subheader("Taux de Défaut par Grade et Durée du Prêt")
    df['term'] = df['term'].astype('str') # Pour un meilleur affichage
    default_by_grade_term = df.groupby(['grade', 'term'])['is_default'].mean().unstack() * 100
    fig_bar_grouped = px.bar(
        default_by_grade_term,
        barmode='group',
        title="Taux de Défaut (%) par Grade et Durée",
        labels={'value': 'Taux de Défaut (%)', 'grade': 'Grade', 'term': 'Durée (mois)'}
    )
    st.plotly_chart(fig_bar_grouped, use_container_width=True)