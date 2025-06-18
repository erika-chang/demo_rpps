import pandas as pd
from sqlalchemy import create_engine, text
import re

# Conexão com o banco
engine = create_engine('postgresql://rpps_user:rpps_pass@localhost:5432/rpps_db')
conn = engine.connect()

# Funções de limpeza
def limpar_cpf(cpf):
    return re.sub(r'\D', '', cpf)

def limpar_cnpj(cnpj):
    return re.sub(r'\D', '', cnpj)

def limpar_telefone(tel):
    numeros = re.sub(r'\D', '', tel)
    return numeros[-10:]

def padronizar_email(email):
    return email.strip().lower()

def padronizar_nome(nome):
    return nome.strip().title()

# 1. EXTRACT (carrega as tabelas em DataFrames)
df_func = pd.read_sql(text("SELECT * FROM funcionarios"), conn)
df_pref = pd.read_sql(text("SELECT * FROM prefeituras"), conn)
df_apos = pd.read_sql(text("SELECT * FROM aposentadorias"), conn)
df_contrib = pd.read_sql(text("SELECT * FROM contribuicoes"), conn)
df_gestores = pd.read_sql(text("SELECT * FROM gestores"), conn)
df_contatos = pd.read_sql(text("SELECT * FROM contatos_tecnicos"), conn)

# 2. TRANSFORM (limpeza)
df_func['cpf'] = df_func['cpf'].apply(limpar_cpf)
df_func['nome'] = df_func['nome'].apply(padronizar_nome)

df_pref['cnpj'] = df_pref['cnpj'].apply(limpar_cnpj)
df_pref['email_contato'] = df_pref['email_contato'].apply(padronizar_email)
df_pref['telefone_contato'] = df_pref['telefone_contato'].apply(limpar_telefone)
df_pref['nome'] = df_pref['nome'].apply(padronizar_nome)

df_gestores['nome'] = df_gestores['nome'].apply(padronizar_nome)
df_gestores['email'] = df_gestores['email'].apply(padronizar_email)
df_gestores['telefone'] = df_gestores['telefone'].apply(limpar_telefone)

df_contatos['nome'] = df_contatos['nome'].apply(padronizar_nome)
df_contatos['email'] = df_contatos['email'].apply(padronizar_email)
df_contatos['telefone'] = df_contatos['telefone'].apply(limpar_telefone)

# Verificação de datas inconsistentes
df_func = df_func[df_func['data_admissao'] >= df_func['data_nascimento']]
df_apos = df_apos[df_apos['data_concessao'] >= df_apos['data_requerimento']]


# Remoção de duplicatas (com base em CPF e CNPJ)
df_func.drop_duplicates(subset='cpf', inplace=True)
df_pref.drop_duplicates(subset='cnpj', inplace=True)
df_gestores.drop_duplicates(subset='id_prefeitura', inplace=True)

# 3. LOAD (opcional: salvar dados limpos em tabelas auxiliares)
df_func.to_sql('funcionarios_clean', con=engine, index=False, if_exists='replace')
df_pref.to_sql('prefeituras_clean', con=engine, index=False, if_exists='replace')
df_apos.to_sql('aposentadorias_clean', con=engine, index=False, if_exists='replace')
df_contrib.to_sql('contribuicoes_clean', con=engine, index=False, if_exists='replace')
df_gestores.to_sql('gestores_clean', con=engine, index=False, if_exists='replace')
df_contatos.to_sql('contatos_tecnicos_clean', con=engine, index=False, if_exists='replace')

print("ETL finalizado com sucesso.")

conn.close()
