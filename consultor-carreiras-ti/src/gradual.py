"""Avaliação gradual ponderada, independente do modo clássico Experta.

Os índices apresentados são pontuações internas de aderência, não probabilidades.
"""
import json
from pathlib import Path

CONFIG_PATH = Path(__file__).resolve().parent.parent / "regras_carreiras.json"


def load_rules(path=None):
    with open(path or CONFIG_PATH, encoding="utf-8") as file:
        config = json.load(file)
    if not config.get("perguntas"):
        raise ValueError("Base de conhecimento sem perguntas")
    from .knowledge import CAREERS
    for question in config["perguntas"]:
        if set(question["pesos"]) != set(CAREERS):
            raise ValueError("Pesos incompletos em " + question["id"])
        if any(not isinstance(v, (int, float)) or not 0 <= v <= 5 for v in question["pesos"].values()):
            raise ValueError("Pesos inválidos em " + question["id"])
    if "competencias" in config:
        if set(config["competencias"]) != set(CAREERS):
            raise ValueError("Competências incompletas para as carreiras")
        for career, items in config["competencias"].items():
            if not items or len({item["id"] for item in items}) != len(items):
                raise ValueError("Competências duplicadas ou ausentes: " + career)
            if any(type(item["nivel_junior"]) is not int or not 1 <= item["nivel_junior"] <= 5 for item in items):
                raise ValueError("Níveis júnior inválidos: " + career)
    return config


def recommend_gradual(answers, config=None):
    """Pontuação centrada em 3: indiferente não soma pontos.

    A afinidade acima de 3 contribui positivamente, abaixo contribui
    negativamente. O denominador é a soma dos pesos da trilha vezes 2;
    o índice varia entre 0 e 100 e 50 representa respostas neutras.
    """
    from .knowledge import CAREERS
    config = config or load_rules()
    expected = {item["id"] for item in config["perguntas"]}
    if set(answers) != expected:
        raise ValueError("Responda exatamente às afinidades solicitadas")
    for key, value in answers.items():
        if type(value) is not int or not 1 <= value <= 5:
            raise ValueError(f"Resposta inválida (esperado 1–5): {key}")
    scores, contributions = {}, {}
    for career in CAREERS:
        maximum = sum(item["pesos"][career] * 2 for item in config["perguntas"])
        total = sum((answers[item["id"]] - 3) * item["pesos"][career] for item in config["perguntas"])
        scores[career] = round(50 + 50 * total / maximum, 1) if maximum else 50.0
        contributions[career] = sorted(
            ({"question":item["texto"], "answer":answers[item["id"]],
              "impact":(answers[item["id"]] - 3) * item["pesos"][career]}
             for item in config["perguntas"]),
            key=lambda item: (-item["impact"], item["question"]),
        )
    penalties = {}
    penalty_cfg = config.get("penalidades", {})
    for career in CAREERS:
        conflicts = [q["id"] for q in config["perguntas"] if
                     answers[q["id"]] <= penalty_cfg.get("limiar_resposta", 0) and
                     q["pesos"][career] >= penalty_cfg.get("peso_minimo", 6)]
        discount = min(20.0, round(100 * penalty_cfg.get("fator", 0) * len(conflicts) / max(1, len(config["perguntas"])), 1))
        scores[career] = round(max(0.0, min(100.0, scores[career] - discount)), 1)
        penalties[career] = {"conflitos":conflicts,"desconto":discount}
    ranking = sorted(CAREERS, key=lambda c: (-scores[c], list(CAREERS).index(c)))
    return {"career":ranking[0], "ranking":ranking, "scores":scores,
            "top3":ranking[:3], "contributions":contributions, "penalties":penalties}
