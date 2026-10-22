"""Interface web do Consultor Inteligente de Carreiras em TI."""
import streamlit as st
from src.engine import recommend
from src.knowledge import QUESTIONS, CAREERS

st.set_page_config(page_title='Consultor de Carreiras em TI', page_icon='🧭', layout='wide')
st.markdown('''<style>
.block-container {max-width: 1050px; padding-top: 2rem;}
.hero {background: linear-gradient(120deg,#132b50,#2255a4);padding:2rem;border-radius:18px;color:white;margin-bottom:1.6rem}
.hero h1 {color:white;font-size:2rem;margin-bottom:.5rem}
.hero p {color:#e2eaff;margin:0}
[data-testid="stMetricValue"] {font-size:2rem}
</style>''', unsafe_allow_html=True)
st.markdown('''<div class="hero"><h1>🧭 Consultor Inteligente de Carreiras em TI</h1>
<p>Descubra qual das 10 trilhas de tecnologia mais combina com seu perfil.
Sistema especialista baseado em regras, com justificativas transparentes.</p></div>''', unsafe_allow_html=True)
st.caption('UNIPAC Barbacena · Inteligência Artificial · Sistema Especialista com Experta')

with st.form('entrevista'):
    st.subheader('Sua entrevista de carreira')
    st.write('Responda às seis perguntas. Não existem respostas certas ou erradas.')
    answers = {}
    for index, (field, question, options) in enumerate(QUESTIONS, 1):
        answers[field] = st.selectbox(f'{index}. {question}', options, index=None,
                                      placeholder='Selecione uma resposta...', key=field)
    submitted = st.form_submit_button('🔎 Analisar meu perfil', type='primary', use_container_width=True)

if submitted:
    if any(value is None for value in answers.values()):
        st.warning('Responda a todas as perguntas para receber sua recomendação.')
    else:
        st.session_state.result = recommend(answers)
        st.session_state.answers = answers

if 'result' in st.session_state:
    result = st.session_state.result
    name, description, next_steps = CAREERS[result['career']]
    st.divider()
    st.subheader('🎯 Sua trilha recomendada')
    st.success(f'**{name}**')
    st.write(description)
    a, b = st.columns(2)
    a.metric('Pontos de compatibilidade', result['scores'][result['career']])
    b.metric('Regras disparadas', result['total_rules_fired'])
    st.markdown('#### Por que essa trilha foi recomendada?')
    for evidence in result['reasons']:
        st.markdown(f'- **{evidence.rule} (+{evidence.points})** — {evidence.reason}')
    st.info(f'**Próximos assuntos para estudar:** {next_steps}')
    st.markdown('#### Comparação entre as 10 trilhas')
    for career in result['ranking']:
        label = CAREERS[career][0]
        score = result['scores'][career]
        st.write(f'**{label}** — {score} pontos')
        st.progress(score / max(result['scores'].values(), default=1) if max(result['scores'].values()) else 0)
    with st.expander('Ver todas as regras que contribuíram para a análise'):
        for evidence in sorted(result['evidence'], key=lambda e: (e.career, e.rule)):
            st.write(f'**{CAREERS[evidence.career][0]}** | {evidence.rule}: +{evidence.points} — {evidence.reason}')
    st.caption('O resultado é uma orientação exploratória baseada nas suas respostas, não um diagnóstico definitivo de carreira.')
