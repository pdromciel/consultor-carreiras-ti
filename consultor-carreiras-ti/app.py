"""Interface da Etapa 2: entrevista em etapas, resultado explicável e roadmap."""
import streamlit as st
from src.engine import recommend
from src.gradual import load_rules, recommend_gradual
from src.desenvolvimento import avaliar_gaps
from src.knowledge import CAREERS, QUESTIONS

st.set_page_config(page_title="Consultor de Carreiras em TI", page_icon="🧭", layout="wide")
st.markdown("""<style>
.block-container {max-width: 1100px; padding-top: 2rem}
.hero {background:linear-gradient(115deg,#153158,#2c5da3);padding:2rem;border-radius:16px;color:white;margin-bottom:1.5rem}
.hero h1 {color:white;font-size:2rem}.hero p {color:#e4ecfa}
</style>""", unsafe_allow_html=True)
st.markdown('<div class="hero"><h1>🧭 Consultor Inteligente de Carreiras em TI</h1><p>Dez trilhas · regras ponderadas · análise de lacunas · plano de desenvolvimento</p></div>', unsafe_allow_html=True)
st.caption("UNIPAC Barbacena · Inteligência Artificial · Sistema especialista baseado em regras")

config = load_rules()
if 'etapa' not in st.session_state:
    st.session_state.etapa = 0

modo = st.radio('Modo de avaliação', ['Etapa 2 — avaliação avançada', 'Modo clássico — Experta'], horizontal=True)
if modo == 'Modo clássico — Experta':
    st.info('O questionário original foi preservado para comparar os métodos de inferência.')
    with st.form('classic'):
        respostas = {field: st.selectbox(f'{idx}. {question}', options, index=None, placeholder='Selecione...', key='old_'+field)
                     for idx,(field,question,options) in enumerate(QUESTIONS,1)}
        enviar = st.form_submit_button('Analisar com o motor clássico', type='primary')
    if enviar:
        if any(v is None for v in respostas.values()):
            st.warning('Responda todas as perguntas.')
        else:
            st.session_state.classic_result = recommend(respostas)
    if 'classic_result' in st.session_state:
        r = st.session_state.classic_result
        st.success(f"Trilha indicada: {CAREERS[r['career']][0]}")
        st.write(CAREERS[r['career']][1])
        st.metric('Pontos no modo clássico',r['scores'][r['career']])
        for evidence in r['reasons']:
            st.write(f'• {evidence.rule} (+{evidence.points}) — {evidence.reason}')
        st.bar_chart({CAREERS[c][0]:r['scores'][c] for c in r['ranking']}, horizontal=True)
else:
    nomes = ['1. Perfil pessoal', '2. Afinidades técnicas', '3. Objetivos de carreira', '4. Resultado e roadmap']
    st.progress(st.session_state.etapa / 3)
    st.caption('  ·  '.join(('**'+n+'**' if i==st.session_state.etapa else n) for i,n in enumerate(nomes)))
    etapa = st.session_state.etapa
    if etapa == 0:
        st.subheader('Sobre você')
        with st.form('perfil'):
            nome = st.text_input('Como gostaria de ser chamado(a)? (opcional)',value=st.session_state.get('nome',''))
            experiencia = st.selectbox('Sua experiência em TI', ['Iniciante','Estudante','Já desenvolvo projetos','Atuo profissionalmente'],index=['Iniciante','Estudante','Já desenvolvo projetos','Atuo profissionalmente'].index(st.session_state.get('experiencia','Iniciante')))
            avancar = st.form_submit_button('Continuar →', type='primary')
        if avancar:
            st.session_state.nome=nome.strip()
            st.session_state.experiencia=experiencia
            st.session_state.etapa=1
            st.rerun()
    elif etapa == 1:
        st.subheader('Afinidades técnicas')
        st.write('Avalie seu **interesse**, não seu domínio técnico. 1 = muito baixo · 3 = neutro · 5 = muito alto.')
        with st.form('afinidades'):
            answers = {q['id']:st.slider(q['texto'],1,5,st.session_state.get('afinidades',{}).get(q['id'],3),key='aff_'+q['id']) for q in config['perguntas']}
            proximo = st.form_submit_button('Calcular e continuar →',type='primary')
        if st.button('← Voltar ao perfil'):
            st.session_state.etapa=0;st.rerun()
        if proximo:
            st.session_state.afinidades=answers
            st.session_state.resultado=recommend_gradual(answers,config)
            st.session_state.etapa=2
            st.rerun()
    elif etapa == 2:
        r=st.session_state.get('resultado')
        if not r:
            st.session_state.etapa=1;st.rerun()
        st.subheader('Objetivos e conhecimento atual')
        st.caption('Selecione uma das três trilhas mais compatíveis e informe seu nível atual em cada competência (0 a 5).')
        labels={k:CAREERS[k][0] for k in r['top3']}
        trilha=st.selectbox('Trilha de interesse',r['top3'],format_func=lambda k:labels[k],key='chosen_career')
        with st.form('competencias'):
            conhecimentos={item['id']:st.slider(item['nome'],0,5,st.session_state.get('conhecimentos',{}).get(trilha,{}).get(item['id'],0),key=f"skill_{trilha}_{item['id']}") for item in config['competencias'][trilha]}
            gerar=st.form_submit_button('Gerar meu resultado →',type='primary')
        if st.button('← Voltar às afinidades'):
            st.session_state.etapa=1;st.rerun()
        if gerar:
            st.session_state.conhecimentos={**st.session_state.get('conhecimentos',{}),trilha:conhecimentos}
            st.session_state.plano=avaliar_gaps(trilha,conhecimentos,config)
            st.session_state.etapa=3;st.rerun()
    else:
        r=st.session_state.get('resultado');p=st.session_state.get('plano')
        if not r or not p:
            st.session_state.etapa=0;st.rerun()
        st.subheader('Seu resultado personalizado')
        if st.session_state.get('nome'):
            st.write(f"Olá, **{st.session_state.nome}**! Estas são suas recomendações.")
        st.caption(f"Perfil: {st.session_state.get('experiencia','não informado')} · Índices heurísticos, não probabilidades de emprego.")
        a,b,c=st.columns(3)
        for col,i in zip((a,b,c),range(3)):
            k=r['top3'][i]
            col.metric(f'{i+1}º {CAREERS[k][0]}',f"{r['scores'][k]:.1f}%")
        st.markdown('#### Compatibilidade entre as dez trilhas')
        st.bar_chart({CAREERS[k][0]:r['scores'][k] for k in r['ranking']},horizontal=True)
        with st.expander('Como o sistema calculou as recomendações?'):
            st.write('Cada afinidade de 1 a 5 é ponderada por carreira com pesos do JSON. A referência neutra é 50%; conflitos de baixa afinidade podem gerar penalidades.')
            st.write('**Contribuições para a primeira trilha:**')
            for item in r['contributions'][r['career']]:
                if item['impact']:
                    st.write(f"• {item['question']}: resposta {item['answer']}; contribuição {item['impact']:+g}")
            for k in r['top3']:
                pen=r['penalties'][k]
                st.write(f"{CAREERS[k][0]}: desconto {pen['desconto']:.1f} p.p. · {len(pen['conflitos'])} conflito(s)")
        st.divider()
        st.subheader(f"Lacunas para nível júnior — {CAREERS[p['carreira']][0]}")
        x,y=st.columns(2)
        x.metric('Metas atingidas',f"{p['percentual_metas_atingidas']:.1f}%")
        y.metric('Competências a desenvolver',p['total_lacunas'])
        st.caption('Os níveis júnior são metas pedagógicas estimadas para orientação, não exigências oficiais do mercado.')
        for item in p['competencias']:
            st.write(f"**{item['nome']}** — atual {item['atual']}/5 · meta {item['nivel_junior']}/5")
            st.progress(min(item['atual']/item['nivel_junior'],1.0))
        st.markdown('#### Roadmap priorizado e projetos de portfólio')
        for etapa_roadmap in p['roadmap']:
            with st.expander(f"{etapa_roadmap['ordem']}. {etapa_roadmap['orientacao']}",expanded=etapa_roadmap['ordem']==1):
                st.write('**Projeto no GitHub:** '+etapa_roadmap['projeto'])
        st.markdown('#### Certificações e referências de estudo')
        for cert in p['certificacoes']:
            st.write('• '+cert)
        st.caption('Confirme pré-requisitos, preços e disponibilidade das certificações nos sites oficiais.')
        aa,bb=st.columns(2)
        if aa.button('← Alterar objetivos'):
            st.session_state.etapa=2;st.rerun()
        if bb.button('Recomeçar entrevista',type='primary'):
            for key in ['resultado','plano','afinidades','conhecimentos','chosen_career']:
                st.session_state.pop(key,None)
            st.session_state.etapa=0;st.rerun()
