import unittest
from src.gradual import load_rules, recommend_gradual
from src.desenvolvimento import avaliar_gaps
from src.knowledge import CAREERS

class TestEtapa2(unittest.TestCase):
    def setUp(self):
        self.config=load_rules()
        self.neutro={p['id']:3 for p in self.config['perguntas']}

    def test_dez_trilhas_com_competencias(self):
        self.assertEqual(set(self.config['competencias']),set(CAREERS))

    def test_penalidade_nao_afeta_neutro(self):
        result=recommend_gradual(self.neutro,self.config)
        self.assertTrue(all(value == 50 for value in result['scores'].values()))

    def test_afinidade_baixa_gera_conflitos(self):
        result=recommend_gradual({k:1 for k in self.neutro},self.config)
        self.assertGreater(result['penalties']['backend']['desconto'],0)
        self.assertTrue(all(0<=v<=100 for v in result['scores'].values()))

    def test_empate_e_deterministico(self):
        self.assertEqual(recommend_gradual(self.neutro,self.config), recommend_gradual(self.neutro,self.config))

    def test_todos_zerados_geram_gaps(self):
        for carreira in CAREERS:
            conhecimentos={x['id']:0 for x in self.config['competencias'][carreira]}
            plano=avaliar_gaps(carreira,conhecimentos,self.config)
            self.assertEqual(plano['total_lacunas'],len(conhecimentos))
            self.assertTrue(plano['roadmap'])

    def test_todas_competencias_atingidas(self):
        conhecimentos={x['id']:x['nivel_junior'] for x in self.config['competencias']['qa']}
        plano=avaliar_gaps('qa',conhecimentos,self.config)
        self.assertEqual(plano['total_lacunas'],0)
        self.assertEqual(plano['percentual_metas_atingidas'],100)

    def test_rejeitar_valores_invalidos(self):
        with self.assertRaises(ValueError):avaliar_gaps('qa',{'testing':8},self.config)
        with self.assertRaises(ValueError):avaliar_gaps('inexistente',{},self.config)

if __name__=='__main__':unittest.main()
