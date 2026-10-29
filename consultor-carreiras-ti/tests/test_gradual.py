import unittest
from src.gradual import load_rules, recommend_gradual
from src.knowledge import CAREERS

class TestGradual(unittest.TestCase):
    def setUp(self):
        self.config = load_rules()
        self.neutral = {q['id']: 3 for q in self.config['perguntas']}

    def test_ten_careers_and_ten_affinities(self):
        self.assertEqual(len(CAREERS), 10)
        self.assertEqual(len(self.config['perguntas']), 10)

    def test_neutral_is_fifty_for_all(self):
        self.assertTrue(all(value == 50 for value in recommend_gradual(self.neutral)['scores'].values()))

    def test_high_and_low_affinity(self):
        highs = {key: 5 for key in self.neutral}
        lows = {key: 1 for key in self.neutral}
        self.assertTrue(all(value == 100 for value in recommend_gradual(highs)['scores'].values()))
        self.assertTrue(all(value == 0 for value in recommend_gradual(lows)['scores'].values()))

    def test_determinism_and_top3(self):
        a = recommend_gradual(self.neutral)
        self.assertEqual(a, recommend_gradual(self.neutral))
        self.assertEqual(len(a['top3']), 3)

    def test_invalid_input(self):
        with self.assertRaises(ValueError):
            recommend_gradual({'logic': 7})
        with self.assertRaises(ValueError):
            recommend_gradual({**self.neutral, 'logic': 0})

if __name__ == '__main__':
    unittest.main()
