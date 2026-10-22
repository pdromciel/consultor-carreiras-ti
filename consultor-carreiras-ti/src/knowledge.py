"""Base de conhecimento explícita do sistema especialista."""
from dataclasses import dataclass

CAREERS = {
    'backend': ('Desenvolvimento Back-end', 'APIs, regras de negócio e bancos de dados.', 'Python/Java, SQL, APIs REST e testes de integração.'),
    'frontend': ('Desenvolvimento Front-end & UI/UX', 'Interfaces acessíveis, experiência do usuário e aplicações web.', 'HTML, CSS, JavaScript, React e Figma.'),
    'data_science': ('Ciência de Dados e Machine Learning', 'Estatística, exploração de dados e modelos preditivos.', 'Python, pandas, estatística e scikit-learn.'),
    'data_engineering': ('Engenharia de Dados', 'ETL/ELT, pipelines e arquitetura de armazenamento de dados.', 'SQL, Python, Airflow e ferramentas de dados.'),
    'security': ('Cibersegurança (Security / Pentesting)', 'Análise de vulnerabilidades, defesa e redes seguras.', 'Redes, Linux, OWASP e fundamentos de segurança.'),
    'devops': ('DevOps & SRE', 'Automação de infraestrutura, CI/CD e confiabilidade.', 'Linux, Docker, GitHub Actions e observabilidade.'),
    'cloud': ('Computação em Nuvem (Cloud Architecture)', 'Arquiteturas escaláveis e serviços de nuvem.', 'AWS/Azure/GCP, redes, IAM e infraestrutura como código.'),
    'mobile': ('Desenvolvimento Mobile', 'Aplicativos para dispositivos móveis.', 'Flutter/Dart ou React Native/TypeScript.'),
    'qa': ('Engenharia de Qualidade e Testes (QA)', 'Qualidade, testes automatizados e prevenção de falhas.', 'Pytest, Playwright, testes de API e CI.'),
    'product': ('Gestão de Produtos (Product Management)', 'Estratégia, necessidades do usuário e priorização.', 'Discovery, métricas de produto, roadmaps e métodos ágeis.'),
}

QUESTIONS = [
    ('math', 'Qual é sua afinidade com matemática e estatística?', ['Baixa', 'Média', 'Alta']),
    ('activity', 'Qual atividade você mais gostaria de realizar diariamente?', [
        'Construir APIs e regras de negócio', 'Criar interfaces e layouts', 'Criar modelos preditivos',
        'Criar pipelines de dados', 'Investigar vulnerabilidades', 'Automatizar entregas e servidores',
        'Projetar soluções em nuvem', 'Criar aplicativos móveis', 'Testar e garantir qualidade',
        'Definir prioridades de produto']),
    ('tool', 'Qual linguagem ou ferramenta é mais familiar?', [
        'Python', 'Java/SQL', 'JavaScript/TypeScript', 'SQL/ETL', 'Linux/Redes',
        'Docker/CI-CD', 'AWS/Azure/GCP', 'Flutter/React Native', 'Ferramentas de testes',
        'Figma/Jira', 'Nenhuma/Iniciante']),
    ('value', 'Que tipo de valor você mais gostaria de entregar?', [
        'Funcionalidades e APIs', 'Experiência visual do usuário', 'Previsões e descobertas em dados',
        'Dados confiáveis e disponíveis', 'Proteção contra ataques', 'Implantações rápidas e confiáveis',
        'Infraestrutura escalável', 'Aplicativos para celular', 'Software com poucos defeitos',
        'Produto alinhado ao negócio']),
    ('interest', 'Qual assunto desperta mais seu interesse?', [
        'Lógica e arquitetura de software', 'Design e usabilidade', 'Estatística e inteligência artificial',
        'Bancos de dados e integração', 'Hacking ético e redes', 'Automação e monitoramento',
        'Serviços e arquitetura cloud', 'Experiência em smartphones', 'Testes e análise de defeitos',
        'Clientes, estratégia e mercado']),
    ('workstyle', 'Qual estilo de trabalho mais combina com você?', [
        'Resolver desafios técnicos por código', 'Prototipar e iterar com usuários',
        'Experimentar hipóteses usando dados', 'Organizar grandes volumes de dados',
        'Investigar riscos e incidentes', 'Melhorar operações e processos',
        'Desenhar arquiteturas e plataformas', 'Construir experiências mobile',
        'Identificar problemas antes do lançamento', 'Alinhar equipes e negociar prioridades']),
]

# Cada opção tem uma afinidade principal. As regras cruzadas abaixo distinguem casos próximos.
ACTIVITY_TO_CAREER = dict(zip(QUESTIONS[1][2], CAREERS))
VALUE_TO_CAREER = dict(zip(QUESTIONS[3][2], CAREERS))
INTEREST_TO_CAREER = dict(zip(QUESTIONS[4][2], CAREERS))
WORKSTYLE_TO_CAREER = dict(zip(QUESTIONS[5][2], CAREERS))
TOOL_TO_CAREERS = {
    'Python': ['backend', 'data_science', 'data_engineering'],
    'Java/SQL': ['backend', 'data_engineering'],
    'JavaScript/TypeScript': ['frontend', 'mobile'],
    'SQL/ETL': ['data_engineering', 'backend'],
    'Linux/Redes': ['security', 'devops', 'cloud'],
    'Docker/CI-CD': ['devops', 'cloud'],
    'AWS/Azure/GCP': ['cloud', 'devops'],
    'Flutter/React Native': ['mobile'],
    'Ferramentas de testes': ['qa'],
    'Figma/Jira': ['frontend', 'product'],
    'Nenhuma/Iniciante': [],
}

@dataclass(frozen=True)
class Evidence:
    rule: str
    career: str
    points: int
    reason: str
