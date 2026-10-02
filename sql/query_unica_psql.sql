-- QUERY UNICA PARA RODAR NO PSQL
-- Projeto: Coffee Shop Sales - Data Warehouse + Machine Learning
--
-- Como rodar no PowerShell, a partir da pasta raiz do projeto:
--
-- cd "C:\Users\henri\Documents\New project 2"
-- psql -U postgres -d postgres -f "sql\query_unica_psql.sql"
--
-- Observacao:
-- Este arquivo usa comandos do psql, como \connect e \copy.
-- Portanto, rode no terminal com psql. Nao rode no Query Tool do pgAdmin.

DROP DATABASE IF EXISTS coffee_shop_dw;

CREATE DATABASE coffee_shop_dw
  WITH
  ENCODING = 'UTF8'
  TEMPLATE = template0;

\connect coffee_shop_dw

DROP SCHEMA IF EXISTS coffee_dw CASCADE;
CREATE SCHEMA coffee_dw;

CREATE TABLE coffee_dw.dim_tempo (
  tempo_key INTEGER PRIMARY KEY,
  data DATE NOT NULL,
  hora SMALLINT NOT NULL CHECK (hora BETWEEN 0 AND 23),
  ano SMALLINT NOT NULL,
  mes SMALLINT NOT NULL CHECK (mes BETWEEN 1 AND 12),
  nome_mes VARCHAR(20) NOT NULL,
  trimestre SMALLINT NOT NULL CHECK (trimestre BETWEEN 1 AND 4),
  dia_mes SMALLINT NOT NULL CHECK (dia_mes BETWEEN 1 AND 31),
  dia_semana_num SMALLINT NOT NULL CHECK (dia_semana_num BETWEEN 1 AND 7),
  nome_dia_semana VARCHAR(20) NOT NULL,
  fim_de_semana BOOLEAN NOT NULL,
  periodo_dia VARCHAR(20) NOT NULL
);

CREATE TABLE coffee_dw.dim_loja (
  loja_key INTEGER PRIMARY KEY,
  localizacao VARCHAR(80) NOT NULL,
  cidade VARCHAR(80) NOT NULL,
  pais VARCHAR(80) NOT NULL,
  rede VARCHAR(80) NOT NULL,
  tipo_loja VARCHAR(40) NOT NULL
);

CREATE TABLE coffee_dw.dim_produto (
  produto_key INTEGER PRIMARY KEY,
  categoria VARCHAR(80) NOT NULL,
  tipo_produto VARCHAR(120) NOT NULL,
  detalhe_produto VARCHAR(160) NOT NULL,
  preco_medio NUMERIC(10, 2) NOT NULL,
  preco_minimo NUMERIC(10, 2) NOT NULL,
  preco_maximo NUMERIC(10, 2) NOT NULL,
  faixa_preco VARCHAR(20) NOT NULL
);

CREATE TABLE coffee_dw.fato_vendas (
  venda_key INTEGER PRIMARY KEY,
  transacao_id INTEGER NOT NULL,
  tempo_key INTEGER NOT NULL REFERENCES coffee_dw.dim_tempo (tempo_key),
  loja_key INTEGER NOT NULL REFERENCES coffee_dw.dim_loja (loja_key),
  produto_key INTEGER NOT NULL REFERENCES coffee_dw.dim_produto (produto_key),
  quantidade SMALLINT NOT NULL CHECK (quantidade > 0),
  preco_unitario NUMERIC(10, 2) NOT NULL CHECK (preco_unitario >= 0),
  receita NUMERIC(12, 2) NOT NULL CHECK (receita >= 0)
);

CREATE INDEX idx_fato_vendas_tempo
  ON coffee_dw.fato_vendas (tempo_key);

CREATE INDEX idx_fato_vendas_loja
  ON coffee_dw.fato_vendas (loja_key);

CREATE INDEX idx_fato_vendas_produto
  ON coffee_dw.fato_vendas (produto_key);

CREATE INDEX idx_fato_vendas_transacao
  ON coffee_dw.fato_vendas (transacao_id);

COMMENT ON TABLE coffee_dw.fato_vendas IS
  'Tabela fato em star schema. transacao_id e uma dimensao degenerada mantida diretamente na fato.';

\copy coffee_dw.dim_tempo FROM 'data/processed/dim_tempo.csv' WITH (FORMAT csv, HEADER true, ENCODING 'UTF8');
\copy coffee_dw.dim_loja FROM 'data/processed/dim_loja.csv' WITH (FORMAT csv, HEADER true, ENCODING 'UTF8');
\copy coffee_dw.dim_produto FROM 'data/processed/dim_produto.csv' WITH (FORMAT csv, HEADER true, ENCODING 'UTF8');
\copy coffee_dw.fato_vendas FROM 'data/processed/fato_vendas.csv' WITH (FORMAT csv, HEADER true, ENCODING 'UTF8');

CREATE OR REPLACE VIEW coffee_dw.vw_receita_mensal_loja_categoria AS
SELECT
  t.ano,
  t.mes,
  t.nome_mes,
  l.localizacao AS loja,
  p.categoria,
  SUM(f.quantidade) AS quantidade_vendida,
  ROUND(SUM(f.receita), 2) AS receita_total,
  ROUND(AVG(f.preco_unitario), 2) AS preco_medio,
  COUNT(*) AS transacoes
FROM coffee_dw.fato_vendas f
JOIN coffee_dw.dim_tempo t
  ON t.tempo_key = f.tempo_key
JOIN coffee_dw.dim_loja l
  ON l.loja_key = f.loja_key
JOIN coffee_dw.dim_produto p
  ON p.produto_key = f.produto_key
GROUP BY
  t.ano,
  t.mes,
  t.nome_mes,
  l.localizacao,
  p.categoria;

CREATE OR REPLACE VIEW coffee_dw.vw_demanda_horaria_produto AS
SELECT
  t.nome_dia_semana,
  t.dia_semana_num,
  t.hora,
  t.periodo_dia,
  l.localizacao AS loja,
  p.categoria,
  p.tipo_produto,
  SUM(f.quantidade) AS quantidade_vendida,
  ROUND(SUM(f.receita), 2) AS receita_total,
  COUNT(*) AS transacoes
FROM coffee_dw.fato_vendas f
JOIN coffee_dw.dim_tempo t
  ON t.tempo_key = f.tempo_key
JOIN coffee_dw.dim_loja l
  ON l.loja_key = f.loja_key
JOIN coffee_dw.dim_produto p
  ON p.produto_key = f.produto_key
GROUP BY
  t.nome_dia_semana,
  t.dia_semana_num,
  t.hora,
  t.periodo_dia,
  l.localizacao,
  p.categoria,
  p.tipo_produto;

CREATE OR REPLACE VIEW coffee_dw.vw_ranking_produtos AS
SELECT
  p.categoria,
  p.tipo_produto,
  p.detalhe_produto,
  SUM(f.quantidade) AS quantidade_vendida,
  ROUND(SUM(f.receita), 2) AS receita_total,
  ROUND(SUM(f.receita) / NULLIF(SUM(f.quantidade), 0), 2) AS receita_media_por_item,
  COUNT(*) AS transacoes
FROM coffee_dw.fato_vendas f
JOIN coffee_dw.dim_produto p
  ON p.produto_key = f.produto_key
GROUP BY
  p.categoria,
  p.tipo_produto,
  p.detalhe_produto;

SELECT 'fato_vendas_rows' AS check_name, COUNT(*) AS value
FROM coffee_dw.fato_vendas;

SELECT 'receita_formula_erros' AS check_name, COUNT(*) AS value
FROM coffee_dw.fato_vendas
WHERE receita <> ROUND(quantidade * preco_unitario, 2);

SELECT 'dim_tempo_rows' AS check_name, COUNT(*) AS value
FROM coffee_dw.dim_tempo;

SELECT 'dim_loja_rows' AS check_name, COUNT(*) AS value
FROM coffee_dw.dim_loja;

SELECT 'dim_produto_rows' AS check_name, COUNT(*) AS value
FROM coffee_dw.dim_produto;

SELECT *
FROM coffee_dw.vw_receita_mensal_loja_categoria
ORDER BY receita_total DESC
LIMIT 10;

SELECT *
FROM coffee_dw.vw_demanda_horaria_produto
ORDER BY quantidade_vendida DESC
LIMIT 10;
