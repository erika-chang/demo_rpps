from faker import Faker
from sqlalchemy import create_engine, MetaData, Table, insert, text
from sqlalchemy.orm import sessionmaker
import random
from datetime import date, timedelta

fake = Faker('pt_BR')

# Conexão com o banco
engine = create_engine('postgresql://rpps_user:rpps_pass@localhost:5432/rpps_db')
Session = sessionmaker(bind=engine)
session = Session()

metadata = MetaData()
metadata.reflect(bind=engine)

# Tabelas
prefeituras = metadata.tables['prefeituras']
funcionarios = metadata.tables['funcionarios']
contribuicoes = metadata.tables['contribuicoes']
aposentadorias = metadata.tables['aposentadorias']
gestores = metadata.tables['gestores']
contatos_tecnicos = metadata.tables['contatos_tecnicos']

# 🔄 Resetar tabelas e IDs
session.execute(text("""TRUNCATE TABLE
                funcionarios,
                contribuicoes,
                aposentadorias,
                prefeituras,
                gestores,
                contatos_tecnicos
                RESTART IDENTITY CASCADE;"""))
session.commit()

# Gerar prefeituras únicas
cnpjs_gerados = set()
prefeitura_ids = []
for _ in range(50):
    cnpj = fake.unique.cnpj().replace('.', '').replace('/', '').replace('-', '')
    prefeitura = {
        'nome': f"Prefeitura de {fake.city()}",
        'cnpj': cnpj,
        'municipio': fake.city(),
        'estado': fake.estado_sigla(),
        'email_contato': fake.email(),
        'telefone_contato': fake.phone_number()
    }
    result = session.execute(insert(prefeituras).returning(prefeituras.c.id), prefeitura)
    prefeitura_id = result.scalar()
    prefeitura_ids.append(prefeitura_id)

    # Inserir gestor
    gestor = {
        'nome': fake.name(),
        'cargo': 'Gestor Municipal',
        'email': fake.email(),
        'telefone': fake.phone_number(),
        'id_prefeitura': prefeitura_id
    }
    session.execute(insert(gestores), gestor)

    # Inserir contato técnico
    contato = {
        'nome': fake.name(),
        'funcao': 'Responsável Técnico',
        'email': fake.email(),
        'telefone': fake.phone_number(),
        'id_prefeitura': prefeitura_id
    }
    session.execute(insert(contatos_tecnicos), contato)

# Gerar funcionários e contribuições
cpfs_gerados = set()
for _ in range(5000):
    cpf = fake.unique.cpf().replace('.', '').replace('-', '')
    data_nasc = fake.date_of_birth(minimum_age=40, maximum_age=65)
    data_admissao = fake.date_between(start_date='-30y', end_date='-5y')
    prefeitura_id = random.choice(prefeitura_ids)

    funcionario = {
        'nome': fake.name(),
        'cpf': cpf,
        'data_nascimento': data_nasc,
        'sexo': random.choice(['M', 'F']),
        'cargo': random.choice(['Professor', 'Técnico', 'Agente de Saúde', 'Assistente']),
        'data_admissao': data_admissao,
        'regime_aposentadoria': random.choice(['RPPS', 'RGPS']),
        'vinculo': random.choice(['Efetivo', 'Comissionado', 'Temporário']),
        'id_prefeitura': prefeitura_id
    }
    result = session.execute(insert(funcionarios).returning(funcionarios.c.id), funcionario)
    funcionario_id = result.scalar()

    # Inserir contribuições (últimos 12 meses)
    for i in range(12):
        competencia = date.today().replace(day=1) - timedelta(days=30 * i)
        salario = round(random.uniform(3000, 8000), 2)
        aliquota = round(random.uniform(11, 14), 2)
        session.execute(insert(contribuicoes), {
            'id_funcionario': funcionario_id,
            'competencia': competencia,
            'salario_contribuicao': salario,
            'aliquota': aliquota
        })

    # Inserir aposentadoria (20% dos casos)
    if random.random() < 0.2:
        tempo = round(random.uniform(30, 40), 2)
        media = round(random.uniform(4000, 6000), 2)
        provento = round(media * 0.85, 2)
        session.execute(insert(aposentadorias), {
            'id_funcionario': funcionario_id,
            'tipo': random.choice(['Voluntária', 'Invalidez', 'Compulsória']),
            'data_requerimento': date.today() - timedelta(days=random.randint(30, 365)),
            'data_concessao': date.today() - timedelta(days=random.randint(1, 29)),
            'tempo_contribuicao_anos': tempo,
            'media_salarial': media,
            'provento_mensal': provento
        })

session.commit()
session.close()
print("Base populada com sucesso.")
