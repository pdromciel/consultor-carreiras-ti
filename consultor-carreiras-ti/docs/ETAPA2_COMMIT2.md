# Etapa 2 — Commit 2

## Implementado
- Mapeamento de competências e metas pedagógicas de nível júnior para as dez trilhas no JSON externo.
- Penalidades pequenas e limitadas quando respostas baixas conflitam com características de peso alto.
- Identificação dos gaps entre nível declarado e referência para júnior.
- Roadmap priorizado conforme a maior lacuna, com propostas de portfólio e sugestões de formação.
- Testes de perfis neutros, conflitantes, lacunas zeradas e completas e empates.

## Limites
Os pesos e níveis são heurísticas acadêmicas, e não estatísticas ou certificações de empregabilidade. O compromisso deste commit é o motor e os resultados; o fluxo Wizard visual será feito no commit 3.

## Validar
`python -m unittest discover -s tests -v` e `streamlit run app.py`.
