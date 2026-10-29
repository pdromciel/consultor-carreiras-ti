"""Interface web do Consultor Inteligente de Carreiras em TI."""
import streamlit as st
from src.engine import recommend
from src.gradual import load_rules, recommend_gradual
from src.desenvolvimento import avaliar_gaps
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

mode = st.radio('Modo de avaliação', ['Avaliação gradual (Etapa 2)', 'Questionário clássico'], horizontal=True)

if mode == 'Questionário clássico':
    st.caption('Modo original preservado para comparação com a primeira etapa.')

if mode == 'Questionário clássico':
    with st.form('entrevista'):
        st.subheader('Sua entrevista de carreira')
        st.write('Responda às seis perguntas. Não existem respostas certas ou erradas.')
        answers = {}
        for index, (field, question, options) in enumerate(QUESTIONS, 1):
            answers[field] = st.selectbox(f'{index}. {question}', options, index=None,
                                          placeholder='Selecione uma resposta...', key=field)
        submitted = st.form_submit_button('🔎 Analisar meu perfil', type='primary', use_container_width=True)
if mode == 'Questionário clássico' and submitted:
    if any(value is None for value in answers.values()):
        st.warning('Responda a todas as perguntas para receber sua recomendação.')
    else:
        st.session_state.result = recommend(answers)
        st.session_state.answers = answers
        st.session_state.result_mode = 'classic'


if mode == 'Avaliação gradual (Etapa 2)':
    config = load_rules()
    st.subheader('Afinidades técnicas (escala de 1 a 5)')
    st.caption('1 = nenhuma afinidade · 3 = neutro · 5 = muita afinidade. Considere seus interesses, não seu conhecimento atual.')
    with st.form('afinidades_graduais'):
        gradual_answers = {}
        for item in config['perguntas']:
            gradual_answers[item['id']] = st.slider(item['texto'], 1, 5, 3, key='gradual_' + item['id'])
        gradual_submitted = st.form_submit_button('🔎 Calcular compatibilidade', type='primary', use_container_width=True)
    if gradual_submitted:
        st.session_state.result = recommend_gradual(gradual_answers, config)
        st.session_state.result_mode = 'gradual'
    if st.session_state.get('result_mode') == 'gradual' and 'result' in st.session_state:
        result = st.session_state.result
        st.divider()
        st.subheader('Top 3 — índice de compatibilidade')
        for i, key in enumerate(result['top3'], 1):
            st.write(f"**{i}º {CAREERS[key][0]} — {result['scores'][key]:.1f}%**")
        st.bar_chart({CAREERS[k][0]: result['scores'][k] for k in result['ranking']}, horizontal=True)
        with st.expander('Justificativa da primeira carreira'):
            for impact in result['contributions'][result['career']]:
                if impact['impact'] != 0:
                    st.write(f"{impact['question']}: resposta {impact['answer']} · contribuição {impact['impact']:+g}")
        st.caption('Os percentuais são índices internos de afinidade, não probabilidades de contratação.')
        pena = result['penalties'][result['career']]
        with st.expander('Análise de conflitos e penalidades'):
            st.write(f"Desconto na trilha recomendada: {pena['desconto']:.1f} ponto(s) percentual(is)")
            if pena['conflitos']:
                labels = {q['id']: q['texto'] for q in config['perguntas']}
                for item in pena['conflitos']:
                    st.write(f"• Baixa afinidade: {labels[item]}")
            else:
                st.write('Não foram identificados conflitos fortes nessa trilha.')
        st.divider()
        st.subheader('Competências atuais e preparação para nível júnior')
        st.caption('Informe quanto conhece de cada competência: 0 = desconheço, 3 = pratico com apoio, 5 = avançado. Metas pedagógicas estimadas.')
        trilha = st.selectbox('Trilha para analisar', result['top3'],
                              format_func=lambda key: CAREERS[key][0], key='trilha_gaps')
        with st.form('form_gaps'):
            conhecimentos = {}
            for item in config['competencias'][trilha]:
                conhecimentos[item['id']] = st.slider(item['nome'], 0, 5, 0,
                                                       key='gap_' + trilha + '_' + item['id'])
            enviar_gaps = st.form_submit_button('Gerar meu plano de estudos', type='primary')
        if enviar_gaps:
            st.session_state.plano = avaliar_gaps(trilha, conhecimentos, config)
        if 'plano' in st.session_state and st.session_state.plano['carreira'] == trilha:
            plano = st.session_state.plano
            st.metric('Metas iniciais atingidas', f"{plano['percentual_metas_atingidas']:.1f}%")
            if plano['lacunas']:
                st.warning(f"{plano['total_lacunas']} competência(s) com lacunas identificadas")
            else:
                st.success('Você atingiu todas as metas pedagógicas informadas para esta trilha.')
            st.markdown('#### Roadmap priorizado')
            for etapa in plano['roadmap']:
                st.markdown(f"**{etapa['ordem']}. {etapa['orientacao']}**\n\nProjeto para portfólio: {etapa['projeto']}")
            st.markdown('#### Cursos e certificações para pesquisar')
            for sugestao in plano['certificacoes']:
                st.write('• ' + sugestao)
            st.caption('As sugestões são referências de estudo; confira preços, disponibilidade e pré-requisitos nos sites oficiais.')

if mode == 'Questionário clássico' and st.session_state.get('result_mode') == 'classic' and 'result' in st.session_state:
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
