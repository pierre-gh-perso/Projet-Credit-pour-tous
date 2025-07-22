import streamlit as st

# La liste QUESTIONS reste identique
QUESTIONS = [
    {"key": "loan_amnt", "label": "Quel est le montant du prêt que vous souhaitez ?", "widget": st.number_input, "params": {"min_value": 500, "max_value": 40000, "value": 15000, "step": 500}},
    {"key": "annual_inc", "label": "Quel est votre revenu annuel (€) ?", "widget": st.number_input, "params": {"min_value": 10000, "max_value": 1000000, "value": 60000, "step": 1000}},
    {"key": "term", "label": "Sur quelle durée souhaitez-vous emprunter ?", "widget": st.selectbox, "params": {"options": [36, 60]}},
    {"key": "dti", "label": "Quel est votre taux d'endettement actuel (en %) ?", "widget": st.number_input, "params": {"min_value": 0.0, "max_value": 100.0, "value": 20.0, "step": 0.1}},
    {"key": "emp_length", "label": "Depuis combien d'années travaillez-vous ?", "widget": st.slider, "params": {"min_value": 0, "max_value": 10, "value": 5, "help": "Mettez 10 si vous avez 10 ans ou plus."}},
    {"key": "home_ownership", "label": "Quel est votre statut de logement ?", "widget": st.selectbox, "params": {"options": ['MORTGAGE', 'RENT', 'OWN'], "format_func": lambda x: {"MORTGAGE": "Propriétaire (avec crédit)", "RENT": "Locataire", "OWN": "Propriétaire (sans crédit)"}[x]}},
    {"key": "purpose", "label": "Quel est le motif principal de ce prêt ?", "widget": st.selectbox, "params": {"options": ['debt_consolidation', 'credit_card', 'home_improvement', 'other'], "format_func": lambda x: {"debt_consolidation": "Consolidation de dettes", "credit_card": "Carte de crédit", "home_improvement": "Rénovations", "other": "Autre"}[x]}}
]

def render_questionnaire():
    """Affiche le questionnaire pas à pas."""
    step = st.session_state.step
    
    progress_value = (step / len(QUESTIONS))
    st.progress(progress_value, text=f"Étape {step + 1}/{len(QUESTIONS)}")

    if step < len(QUESTIONS):
        q = QUESTIONS[step]
        
        with st.form(key=f"form_step_{step}"):
            st.subheader(q['label'])
            answer = q['widget'](label="Réponse", **q['params'], label_visibility="collapsed")
            
            # === MODIFICATION 2 : Alignement des boutons à droite ===
            empty_col, prev_col, next_col = st.columns([0.5, 0.25, 0.25])
            with prev_col:
                if step > 0:
                    if st.form_submit_button("⬅️ Précédent", use_container_width=True):
                        # Pas besoin de sauvegarder la réponse si on recule
                        st.session_state.step -= 1
                        st.rerun()
            with next_col:
                if st.form_submit_button("Suivant ➡️", type="primary", use_container_width=True):
                    st.session_state.answers[q['key']] = answer
                    st.session_state.step += 1
                    st.rerun()
    else:
        st.success("🎉 Questionnaire terminé !")
        st.write("Cliquez ci-dessous pour obtenir votre proposition.")
        if st.button("🚀 Lancer la simulation", type="primary", use_container_width=True):
            st.session_state.run_simulation = True
            st.rerun()

def display_results(results, form_data):
    """Affiche les résultats de la simulation."""
    st.subheader(f"Proposition Finale sur {form_data['term']} mois")
    
    if "Refus" in results['decision']:
        st.error(f"{results['decision']} (Score de risque : {results['risk_score']:.2%}, Grade équivalent : {results['grade']})")
        return
        
    if results['final_dti'] > 40:
        st.error(f"❌ **Refus (Règle Métier)** : Le taux d'endettement final ({results['final_dti']:.1f}%) dépasserait le seuil de 40%.")
        return

    if "Approbation" in results['decision']: 
        st.success(results['decision'])
    else: 
        st.warning(results['decision'])
    
    # === MODIFICATION 1 : Formatage des nombres avec séparateur de milliers ===
    # On utilise la syntaxe f-string : ,.2f pour séparateur + 2 décimales
    
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Score de Risque", f"{results['risk_score']:.2%}")
    col2.metric("Grade Équivalent", f"Grade {results['grade']}")
    col3.metric("Taux Annuel Proposé", f"{results['rate']*100:.2f} %")
    col4.metric("Mensualité Estimée", f"{results['monthly_payment']:,.2f} €")
    
    st.divider()
    
    col5, col6 = st.columns(2)
    col5.metric("Montant Total Remboursé", f"{results['total_repaid']:,.2f} €")
    col6.metric("Coût Total du Crédit", f"{results['credit_cost']:,.2f} €", delta_color="inverse")
    
    st.info(f"Le taux d'endettement après ce crédit passerait de **{form_data['dti']:.1f}%** à **{results['final_dti']:.1f}%**.")