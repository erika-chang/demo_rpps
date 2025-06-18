from sqlalchemy import Column, Integer, String, Date, Numeric, ForeignKey
from .database import Base

class Prefeitura(Base):
    __tablename__ = 'prefeituras'
    id = Column(Integer, primary_key=True)
    nome = Column(String, nullable=False)
    cnpj = Column(String(14), unique=True, nullable=False)
    municipio = Column(String)
    estado = Column(String(2))
    email_contato = Column(String)
    telefone_contato = Column(String)

class Funcionario(Base):
    __tablename__ = 'funcionarios'
    id = Column(Integer, primary_key=True)
    nome = Column(String, nullable=False)
    cpf = Column(String(11), unique=True, nullable=False)
    data_nascimento = Column(Date, nullable=False)
    sexo = Column(String(1))
    cargo = Column(String)
    data_admissao = Column(Date, nullable=False)
    regime_aposentadoria = Column(String)
    vinculo = Column(String)
    id_prefeitura = Column(Integer, ForeignKey('prefeituras.id'))

class Contribuicao(Base):
    __tablename__ = 'contribuicoes'
    id = Column(Integer, primary_key=True)
    id_funcionario = Column(Integer, ForeignKey('funcionarios.id'))
    competencia = Column(Date, nullable=False)
    salario_contribuicao = Column(Numeric(10, 2))
    aliquota = Column(Numeric(4, 2))
    contribuicao = Column(Numeric(10, 2))

class Aposentadoria(Base):
    __tablename__ = 'aposentadorias'
    id = Column(Integer, primary_key=True)
    id_funcionario = Column(Integer, ForeignKey('funcionarios.id'))
    tipo = Column(String)
    data_requerimento = Column(Date)
    data_concessao = Column(Date)
    tempo_contribuicao_anos = Column(Numeric(5, 2))
    media_salarial = Column(Numeric(10, 2))
    provento_mensal = Column(Numeric(10, 2))
