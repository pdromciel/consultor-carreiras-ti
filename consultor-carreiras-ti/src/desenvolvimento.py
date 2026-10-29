"""Gaps de competências e roteiros de estudo baseados em requisitos externos JSON.

Escala de conhecimento: 0=desconheço, 1=estudo inicial, 2=básico,
3=pratico com apoio, 4=autônomo, 5=avançado. O limiar de júnior é
uma meta pedagógica, não uma exigência universal do mercado.
"""
from .gradual import load_rules
from .knowledge import CAREERS


def avaliar_gaps(carreira, conhecimentos, config=None):
    config = config or load_rules()
    if carreira not in CAREERS:
        raise ValueError("Trilha desconhecida")
    competencias = config["competencias"][carreira]
    expected = {item["id"] for item in competencias}
    if set(conhecimentos) != expected:
        raise ValueError("Informe o conhecimento de todas as competências da trilha")
    gaps = []
    for item in competencias:
        atual = conhecimentos[item["id"]]
        if type(atual) is not int or not 0 <= atual <= 5:
            raise ValueError("Conhecimento deve ser número inteiro entre 0 e 5")
        faltam = max(0, item["nivel_junior"] - atual)
        gaps.append({**item, "atual": atual, "gap": faltam, "atingido": faltam == 0})
    # Prioriza maior lacuna, preservando ordem de pré-requisitos do JSON em empates.
    prioridades = sorted((item for item in gaps if item["gap"]), key=lambda x: -x["gap"])
    sugestoes = []
    for i, item in enumerate(prioridades, 1):
        sugestoes.append({"ordem": i, "competencia": item["nome"],
                          "orientacao": f"Estudar {item['nome']} até o nível {item['nivel_junior']}/5",
                          "projeto": item["projeto"]})
    if not sugestoes:
        sugestoes.append({"ordem":1,"competencia":"Consolidar portfólio",
                          "orientacao":"Aprofundar as competências e buscar avaliação prática",
                          "projeto": competencias[0]["projeto"]})
    return {"carreira":carreira,"competencias":gaps,"lacunas":prioridades,
            "total_lacunas":len(prioridades),"percentual_metas_atingidas":round(100*(len(gaps)-len(prioridades))/len(gaps),1),
            "roadmap":sugestoes,"certificacoes":config["certificacoes_sugeridas"][carreira]}
