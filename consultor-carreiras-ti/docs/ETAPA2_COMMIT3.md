# Etapa 2 — Commit 3: interface Wizard e validação final

## Alterações
- Interface Streamlit em quatro telas: perfil, afinidades, objetivos/competências e resultados.
- Top 3 com métricas, gráfico das dez trilhas, justificativas e penalidades exibidas.
- Lacunas de competências com barras de progresso, roadmap e projetos de portfólio.
- Modo original com Experta preservado, disponível por alternância na interface.
- Casos de teste adicionais: perfil ambíguo, empates, pontuações extremas, gaps completos e sem gaps.

## Execução
```bash
pip install -r requirements.txt
streamlit run app.py
python -m unittest discover -s tests -v
```

## Observação metodológica
Compatibilidades são **índices heurísticos de afinidade**, não probabilidades estatísticas. Os patamares de nível júnior são metas pedagógicas de referência, não certificação de empregabilidade.
