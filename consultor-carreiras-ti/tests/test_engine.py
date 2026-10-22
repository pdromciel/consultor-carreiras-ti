import unittest
from src.engine import recommend, InferenceEngine
from src.knowledge import QUESTIONS, CAREERS

# Personas: cobrem 10 perfis consistentes, incluindo 4 exigidos na atividade.
TOOLS = ['Java/SQL', 'Figma/Jira', 'Python', 'SQL/ETL', 'Linux/Redes',
         'Docker/CI-CD', 'AWS/Azure/GCP', 'Flutter/React Native',
         'Ferramentas de testes', 'Figma/Jira']

class TestCareerRecommendations(unittest.TestCase):
    def make_persona(self, index):
        return {'math': 'Alta' if index == 2 else 'Média',
                'activity': QUESTIONS[1][2][index],
                'tool': TOOLS[index],
                'value': QUESTIONS[3][2][index],
                'interest': QUESTIONS[4][2][index],
                'workstyle': QUESTIONS[5][2][index]}

    def test_all_ten_personas(self):
        for i, career in enumerate(CAREERS):
            with self.subTest(career=career):
                result = recommend(self.make_persona(i))
                self.assertEqual(result['career'], career)
                self.assertTrue(result['reasons'])
                self.assertEqual(len(result['scores']), 10)

    def test_data_science_vs_data_engineering(self):
        self.assertEqual(recommend(self.make_persona(2))['career'], 'data_science')
        self.assertEqual(recommend(self.make_persona(3))['career'], 'data_engineering')

    def test_deterministic(self):
        answers = self.make_persona(4)
        self.assertEqual(recommend(answers)['scores'], recommend(answers)['scores'])

    def test_invalid_answer(self):
        with self.assertRaises(ValueError):
            recommend({'math': 'não existe'})

    def test_at_least_25_rules(self):
        rules = InferenceEngine().get_rules()
        self.assertGreaterEqual(len(rules), 25)

if __name__ == '__main__':
    unittest.main()
