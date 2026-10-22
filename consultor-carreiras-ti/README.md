# 🧭 Consultor Inteligente de Carreiras em TI

Sistema especialista em **Python + Experta + Streamlit**, desenvolvido para a
atividade da disciplina **Inteligência Artificial — UNIPAC Barbacena**.

## Funcionalidades

- Entrevista dinâmica com seis perguntas (matemática, atividade, ferramenta,
  entrega de valor, interesse técnico e estilo de trabalho).
- Motor especialista com **37 regras** (`@Rule`) e **encadeamento para frente**.
- Recomendação de **uma entre dez carreiras de TI**, acompanhada dos motivos.
- Pontuação comparativa de todas as dez trilhas e indicação de estudos iniciais.
- Matriz de decisão documentada e testes automatizados com **dez personas**.

## Instalação

Recomendado: **Python 3.10** (a Experta é uma dependência antiga; este projeto
inclui um pequeno ajuste de compatibilidade com `collections`).

```bash
git clone https://github.com/SEU-USUARIO/consultor-carreiras-ti.git
cd consultor-carreiras-ti
python -m venv .venv
```

**Windows (PowerShell):**

```powershell
.venv\Scripts\Activate.ps1
```

**Linux/macOS:**

```bash
source .venv/bin/activate
```

```bash
pip install -r requirements.txt
streamlit run app.py
```

Abra o endereço indicado no terminal (normalmente `http://localhost:8501`).

## Testes

```bash
python -m unittest discover -s tests -v
```

O arquivo `tests/test_engine.py` inclui perfis das dez carreiras, incluindo
cientista de dados, engenheiro de dados, profissional de segurança,
frontend e gestor de produto, além de validação das regras e entradas.

## Estrutura

```text
consultor-carreiras-ti/
├── app.py                    # Interface Streamlit
├── src/
│   ├── __init__.py
│   ├── engine.py             # Fatos, motor de inferência e regras
│   └── knowledge.py          # Base de conhecimento e questionário
├── tests/
│   └── test_engine.py        # Personas e validações
├── docs/
│   └── MATRIZ_DE_DECISAO.md  # Mapeamento dos pesos e regras
├── .streamlit/config.toml    # Tema
├── .gitignore
├── requirements.txt
└── README.md
```

## Como funciona

1. O usuário responde às perguntas.
2. As respostas são validadas e convertidas em um fato `Profile` (Experta).
3. O motor realiza encadeamento para frente e executa as regras aplicáveis.
4. Cada regra adiciona evidências com pesos à trilha correspondente.
5. As pontuações são somadas; a maior pontuação indica a carreira.
6. O resultado apresenta os motivos e a comparação entre todas as trilhas.

Leia a [matriz de decisão](docs/MATRIZ_DE_DECISAO.md) para os detalhes.

## Publicação no GitHub

Crie um repositório vazio no GitHub e, na pasta do projeto, execute:

```bash
git init
git add .
git commit -m "feat: implementar sistema especialista de carreiras em TI"
git branch -M main
git remote add origin https://github.com/SEU-USUARIO/consultor-carreiras-ti.git
git push -u origin main
```

Substitua `SEU-USUARIO` pelo seu usuário real do GitHub.

## Tecnologias

Python 3.10+, Experta 1.9.4, Streamlit.

## Contexto acadêmico

Disciplina: Inteligência Artificial · Professor: Felipe Roncalli de Paula Carneiro.
Instituição: Centro Universitário Presidente Antônio Carlos (UNIPAC Barbacena).
