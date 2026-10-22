# Matriz de decisão e engenharia do conhecimento

O sistema coleta seis fatos: `math`, `activity`, `tool`, `value`, `interest` e `workstyle`.
Cada regra ativada adiciona evidências pontuadas à trilha correspondente. A maior
pontuação determina a recomendação, e todas as justificativas disparadas são exibidas.

| Dimensão | Regra | Peso | Observação |
|---|---|---:|---|
| Atividade principal | R01–R10 | 6 | Dez opções, uma por carreira |
| Entrega de valor | R11–R20 | 5 | Dez opções, uma por carreira |
| Interesse técnico | R21–R30 | 4 | Dez opções, uma por carreira |
| Ferramenta conhecida | R31 | 2 | Pode reforçar mais de uma carreira |
| Estilo de trabalho | R32 | 3 | Uma associação por estilo |
| Afinidade matemática | R33 | 1–3 | Reforça dados e ML conforme o nível |
| Modelagem + insights | R34 | 5 | Bônus para Ciência de Dados |
| Pipeline + dados disponíveis | R35 | 5 | Bônus para Engenharia de Dados |
| Vulnerabilidades + hacking ético | R36 | 4 | Bônus para Cibersegurança |
| Automação + entrega confiável | R37 | 4 | Bônus para DevOps/SRE |

## Correspondência entre opções e carreiras

| Trilha | Atividade | Entrega de valor | Interesse |
|---|---|---|---|
| Back-end | Construir APIs e regras de negócio | Funcionalidades e APIs | Lógica e arquitetura de software |
| Front-end/UI/UX | Criar interfaces e layouts | Experiência visual do usuário | Design e usabilidade |
| Ciência de Dados/ML | Criar modelos preditivos | Previsões e descobertas em dados | Estatística e inteligência artificial |
| Engenharia de Dados | Criar pipelines de dados | Dados confiáveis e disponíveis | Bancos de dados e integração |
| Cibersegurança | Investigar vulnerabilidades | Proteção contra ataques | Hacking ético e redes |
| DevOps/SRE | Automatizar entregas e servidores | Implantações rápidas e confiáveis | Automação e monitoramento |
| Cloud | Projetar soluções em nuvem | Infraestrutura escalável | Serviços e arquitetura cloud |
| Mobile | Criar aplicativos móveis | Aplicativos para celular | Experiência em smartphones |
| QA | Testar e garantir qualidade | Software com poucos defeitos | Testes e análise de defeitos |
| Produto | Definir prioridades de produto | Produto alinhado ao negócio | Clientes, estratégia e mercado |

## Resolução de ambiguidades

- **Ciência de Dados x Engenharia de Dados:** Modelagem preditiva e descoberta
  de insights reforçam Ciência de Dados, enquanto pipelines e dados disponíveis
  reforçam Engenharia de Dados.
- **Segurança x DevOps x Cloud:** Atividades e entregas especializadas recebem
  pesos mais fortes que afinidades genéricas com Linux ou redes.
- **Front-end x Produto:** Interesse em interfaces e experiência visual diferencia
  Front-end de estratégia, planejamento e priorização de produto.
- Em caso de empate total, aplica-se uma ordem fixa, documentada em `CAREERS`;
  isso garante uma única recomendação reproduzível.

## Limitações

A base de regras é construída para fins didáticos, não calibrada em pesquisas
psicométricas. O resultado é uma orientação inicial, não uma avaliação profissional.
