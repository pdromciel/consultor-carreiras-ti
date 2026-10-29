"""Cenários adversos da inferência e integração com o roadmap."""
import unittest
from src.gradual import load_rules, recommend_gradual
from src.desenvolvimento import avaliar_gaps

class TestEdgeCases(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.config=load_rules()
        cls.neutral={q['id']:3 for q in cls.config['perguntas']}

    def test_ambiguous_profile_has_stable_ranking(self):
        perfil=self.neutral.copy()
        for q in self.config['perguntas']:
            if q['id'] in ('logic','design','data','programming'):
                perfil[q['id']]=5
        a=recommend_gradual(perfil,self.config)
        self.assertEqual(a['ranking'], recommend_gradual(perfil,self.config)['ranking'])
        self.assertEqual(len(set(a['top3'])),3)

    def test_scores_always_in_range(self):
        for value in range(1,6):
            r=recommend_gradual({k:value for k in self.neutral},self.config)
            self.assertTrue(all(0 <= s <= 100 for s in r['scores'].values()))

    def test_equal_answers_are_deterministic(self):
        a=recommend_gradual(self.neutral,self.config)
        self.assertEqual(a['ranking'],recommend_gradual(self.neutral,self.config)['ranking'])

    def test_all_skills_at_target_has_no_gaps(self):
        career=recommend_gradual(self.neutral,self.config)['career']
        skills={x['id']:x['nivel_junior'] for x in self.config['competencias'][career]}
        p=avaliar_gaps(career,skills,self.config)
        self.assertEqual(p['total_lacunas'],0)
        self.assertEqual(p['percentual_metas_atingidas'],100)
        self.assertTrue(p['roadmap'])

    def test_no_skill_has_all_gaps(self):
        career=recommend_gradual(self.neutral,self.config)['career']
        skills={x['id']:0 for x in self.config['competencias'][career]}
        p=avaliar_gaps(career,skills,self.config)
        self.assertEqual(p['total_lacunas'],len(skills))
        self.assertEqual(p['percentual_metas_atingidas'],0)

    def test_invalid_skill_rejected(self):
        career=recommend_gradual(self.neutral,self.config)['career']
        skills={x['id']:0 for x in self.config['competencias'][career]}
        skills[next(iter(skills))]=-1
        with self.assertRaises(ValueError):
            avaliar_gaps(career,skills,self.config)

if __name__=='__main__':
    unittest.main()
