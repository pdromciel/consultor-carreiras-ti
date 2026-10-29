# Etapa 2 — Commit 1: base JSON e respostas graduais

Esta versão amplia o projeto original **sem apagar nenhum arquivo**.

## O que mudou
- `regras_carreiras.json`: define perguntas, pesos por carreira e pesos do motor antigo.
- `src/gradual.py`: carrega o JSON, valida todos os pesos e calcula a aderência ponderada.
- `src/engine.py`: mantém Experta, mas lê os pesos originais do JSON.
- `app.py`: seletor entre avaliação gradual e o questionário clássico.
- `tests/test_gradual.py`: verifica entradas inválidas, neutralidade, extremos e determinismo.

## Regra da avaliação gradual
Cada resposta está entre 1 e 5, com **3 como ponto neutro**. A contribuição de uma pergunta a uma carreira é `(resposta - 3) * peso`. O índice é `50 + 50 * soma(contribuições) / (2 * soma(pesos))`, limitado naturalmente ao intervalo de 0 a 100.

Não é uma probabilidade calibrada de sucesso profissional. Os pesos são heurísticas didáticas, sujeitos a validação. Perfis em que todas as respostas são iguais podem empatar.

## Próximos commits
2. Incorporar competências atuais, gaps, penalidades e roadmap.
3. Wizard em etapas, gráficos adicionais e testes dos casos limites.
