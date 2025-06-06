CREATE TABLE IF NOT EXISTS funcionarios (
    id SERIAL PRIMARY KEY,
    nome TEXT NOT NULL,
    cpf VARCHAR(11) UNIQUE NOT NULL,
    data_nascimento DATE NOT NULL,
    sexo CHAR(1) CHECK (sexo IN ('M', 'F')),
    cargo TEXT,
    data_admissao DATE NOT NULL,
    regime_aposentadoria TEXT CHECK (regime_aposentadoria IN ('RPPS', 'RGPS')) DEFAULT 'RPPS',
    vinculo TEXT,
    id_prefeitura INT
);
CREATE TABLE IF NOT EXISTS contribuicoes (
    id SERIAL PRIMARY KEY,
    id_funcionario INT REFERENCES funcionarios(id),
    competencia DATE NOT NULL,
    salario_contribuicao NUMERIC(10,2),
    aliquota NUMERIC(4,2),
    contribuicao NUMERIC(10,2) GENERATED ALWAYS AS (salario_contribuicao * aliquota / 100) STORED
);
CREATE TABLE IF NOT EXISTS aposentadorias (
    id SERIAL PRIMARY KEY,
    id_funcionario INT REFERENCES funcionarios(id),
    tipo TEXT CHECK (tipo IN ('Voluntária', 'Invalidez', 'Compulsória')),
    data_requerimento DATE,
    data_concessao DATE,
    tempo_contribuicao_anos NUMERIC(5,2),
    media_salarial NUMERIC(10,2),
    provento_mensal NUMERIC(10,2)
);
CREATE TABLE IF NOT EXISTS prefeituras (
    id SERIAL PRIMARY KEY,
    nome TEXT NOT NULL,
    cnpj VARCHAR(14) UNIQUE NOT NULL,
    municipio TEXT,
    estado CHAR(2),
    email_contato TEXT,
    telefone_contato TEXT
);
CREATE TABLE IF NOT EXISTS gestores (
    id SERIAL PRIMARY KEY,
    nome TEXT,
    cargo TEXT,
    email TEXT,
    telefone TEXT,
    id_prefeitura INT REFERENCES prefeituras(id)
);
CREATE TABLE IF NOT EXISTS contatos_tecnicos (
    id SERIAL PRIMARY KEY,
    nome TEXT,
    funcao TEXT,
    email TEXT,
    telefone TEXT,
    id_prefeitura INT REFERENCES prefeituras(id)
);
