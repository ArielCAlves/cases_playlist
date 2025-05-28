-- Remove o schema anterior, se existir
DROP SCHEMA IF EXISTS case10 CASCADE;

-- Cria novo schema
CREATE SCHEMA case10 AUTHORIZATION "case10";

-- Tabela 1: Organizações analisadas no relatório
CREATE TABLE case10.organizacoes (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    setor VARCHAR(50) NOT NULL,
    pais VARCHAR(50) NOT NULL
);

-- Tabela 2: Ferramentas tecnológicas aplicadas pelas organizações
CREATE TABLE case10.ferramentas (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    categoria VARCHAR(50) NOT NULL
);

-- Tabela 3: Aplicações práticas de IA com base nas ferramentas e nas organizações
CREATE TABLE case10.aplicacoes (
    id SERIAL PRIMARY KEY,
    id_org INTEGER NOT NULL REFERENCES case10.organizacoes(id),
    id_ferramenta INTEGER NOT NULL REFERENCES case10.ferramentas(id),
    descricao_uso VARCHAR(200) NOT NULL,
    beneficio_percentual DECIMAL(5, 2) NOT NULL,
    ano INTEGER NOT NULL
);
