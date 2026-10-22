"""Motor de inferência por encadeamento para frente usando Experta.

São 34 regras @Rule: 10 de atividade, 10 de entrega, 10 de interesse
 e 4 regras cruzadas. As demais evidências são produzidas por regras
 genéricas de ferramenta, estilo de trabalho e matemática (3 regras).
Total: 37 regras declaradas.
"""
# Compatibilidade com bibliotecas legadas transitivas da Experta em Python 3.10+.
import collections
import collections.abc
for _attr in ('Mapping', 'MutableMapping', 'Sequence', 'Iterable', 'Set'):
    if not hasattr(collections, _attr):
        setattr(collections, _attr, getattr(collections.abc, _attr))

from experta import Fact, KnowledgeEngine, Rule, MATCH, AS, TEST
from .knowledge import (CAREERS, Evidence, ACTIVITY_TO_CAREER,
                        VALUE_TO_CAREER, INTEREST_TO_CAREER,
                        WORKSTYLE_TO_CAREER, TOOL_TO_CAREERS, QUESTIONS)

class Profile(Fact):
    """Respostas do questionário como fatos para inferência."""

class CareerEngine(KnowledgeEngine):
    def __init__(self):
        super().__init__()
        self.evidence = []

    def add(self, rule, career, points, reason):
        item = Evidence(rule, career, points, reason)
        if item not in self.evidence:
            self.evidence.append(item)

    @Rule(Profile(tool=MATCH.tool))
    def tool_affinity(self, tool):
        for career in TOOL_TO_CAREERS[tool]:
            self.add('R31 · Ferramenta', career, 2, f'Familiaridade com {tool}.')

    @Rule(Profile(workstyle=MATCH.workstyle))
    def style_affinity(self, workstyle):
        self.add('R32 · Estilo', WORKSTYLE_TO_CAREER[workstyle], 3,
                 f'Seu estilo de trabalho combina com: {workstyle.lower()}.')

    @Rule(Profile(math=MATCH.math))
    def mathematics(self, math):
        if math == 'Alta':
            self.add('R33 · Matemática', 'data_science', 3, 'Alta afinidade com matemática e estatística.')
            self.add('R33 · Matemática', 'data_engineering', 1, 'Base matemática útil no trabalho com dados.')
        elif math == 'Média':
            self.add('R33 · Matemática', 'data_science', 1, 'Afinidade intermediária com matemática.')

    @Rule(Profile(activity='Criar modelos preditivos', value='Previsões e descobertas em dados'))
    def cross_science(self):
        self.add('R34 · Cruzamento', 'data_science', 5, 'Combinação de modelagem preditiva com entrega de insights.')

    @Rule(Profile(activity='Criar pipelines de dados', value='Dados confiáveis e disponíveis'))
    def cross_engineering(self):
        self.add('R35 · Cruzamento', 'data_engineering', 5, 'Construção de pipelines para disponibilizar dados confiáveis.')

    @Rule(Profile(activity='Investigar vulnerabilidades', interest='Hacking ético e redes'))
    def cross_security(self):
        self.add('R36 · Cruzamento', 'security', 4, 'Interesse em segurança somado à investigação de vulnerabilidades.')

    @Rule(Profile(activity='Automatizar entregas e servidores', value='Implantações rápidas e confiáveis'))
    def cross_devops(self):
        self.add('R37 · Cruzamento', 'devops', 4, 'Automação combinada à confiabilidade das entregas.')

# Regras especializadas por opção: criadas como métodos distintos e decoradas com @Rule.
# Cada uma é registrada pelo metaclass do Experta como produção independente.
def _build_rule(field, selected, career, number, weight, description):
    def firing(self):
        self.add(f'R{number:02d} · {description}', career, weight,
                 f'Você escolheu "{selected}" em {description.lower()}.')
    firing.__name__ = f'rule_{number:02d}'
    return Rule(Profile(**{field: selected}))(firing)

for _start, _field, _mapping, _weight, _description in (
    (1, 'activity', ACTIVITY_TO_CAREER, 6, 'Atividade principal'),
    (11, 'value', VALUE_TO_CAREER, 5, 'Entrega de valor'),
    (21, 'interest', INTEREST_TO_CAREER, 4, 'Interesse técnico'),
):
    for _offset, (_selected, _career) in enumerate(_mapping.items()):
        setattr(CareerEngine, f'rule_{_start + _offset:02d}',
                _build_rule(_field, _selected, _career, _start + _offset, _weight, _description))

# Experta registra as regras no metaclass durante a definição da classe;
# como as regras dinâmicas foram acrescentadas depois, usamos uma subclasse
# criada *após* injetá-las para efetivar o registro na versão instalada.
class InferenceEngine(CareerEngine):
    pass


def validate_answers(answers):
    for field, _, options in QUESTIONS:
        if answers.get(field) not in options:
            raise ValueError(f'Resposta inválida ou ausente: {field}')


def recommend(answers):
    validate_answers(answers)
    engine = InferenceEngine()
    engine.reset()
    engine.declare(Profile(**answers))
    engine.run()
    score = {key: 0 for key in CAREERS}
    for item in engine.evidence:
        score[item.career] += item.points
    # Empates são resolvidos pela ordem fixa da base (sem aleatoriedade).
    ranking = sorted(score, key=lambda career: (-score[career], list(CAREERS).index(career)))
    winner = ranking[0]
    reasons = sorted((e for e in engine.evidence if e.career == winner),
                     key=lambda e: (-e.points, e.rule))
    return {'career': winner, 'ranking': ranking, 'scores': score,
            'reasons': reasons, 'evidence': engine.evidence,
            'total_rules_fired': len({e.rule for e in engine.evidence})}
