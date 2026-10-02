-- QUERY DO ZERO PARA RODAR NO PSQL
-- Projeto: Coffee Shop Sales - Data Warehouse + Machine Learning
--
-- O que este arquivo faz:
-- 1. Cria o banco coffee_shop_dw_codigo.
-- 2. Cria uma tabela staging com os dados brutos.
-- 3. Carrega data/raw/coffee_shop_sales_raw.csv.
-- 4. Calcula receita, hora, tempo_key e atributos dimensionais em SQL.
-- 5. Cria dim_tempo, dim_loja, dim_produto e fato_vendas.
-- 6. Cria as views analiticas.
-- 7. Roda validacoes.
--
-- Antes de rodar este SQL, gere o CSV bruto:
--
-- python scripts/export_raw_xlsx_to_csv.py
--
-- Depois rode, a partir da raiz do projeto:
--
-- psql -U postgres -d postgres -f "sql\query_do_zero_psql.sql"
--
-- Se o psql nao estiver no PATH:
--
-- & "C:\Program Files\PostgreSQL\18\bin\psql.exe" -U postgres -d postgres -f "sql\query_do_zero_psql.sql"

DROP DATABASE IF EXISTS coffee_shop_dw_codigo;

CREATE DATABASE coffee_shop_dw_codigo
  WITH
  ENCODING = 'UTF8'
  TEMPLATE = template0;

\connect coffee_shop_dw_codigo

DROP SCHEMA IF EXISTS coffee_dw CASCADE;
CREATE SCHEMA coffee_dw;

CREATE TABLE coffee_dw.stg_coffee_sales (
  transaction_id INTEGER,
  transaction_date DATE,
  transaction_time TIME,
  transaction_qty INTEGER,
  store_id INTEGER,
  store_location VARCHAR(80),
  product_id INTEGER,
  unit_price NUMERIC(10, 2),
  product_category VARCHAR(80),
  product_type VARCHAR(120),
  product_detail VARCHAR(160)
);

\copy coffee_dw.stg_coffee_sales FROM 'data/raw/coffee_shop_sales_raw.csv' WITH (FORMAT csv, HEADER true, ENCODING 'UTF8');

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

INSERT INTO coffee_dw.dim_tempo (
  tempo_key,
  data,
  hora,
  ano,
  mes,
  nome_mes,
  trimestre,
  dia_mes,
  dia_semana_num,
  nome_dia_semana,
  fim_de_semana,
  periodo_dia
)
SELECT DISTINCT
  (TO_CHAR(transaction_date, 'YYYYMMDD') || LPAD(EXTRACT(HOUR FROM transaction_time)::TEXT, 2, '0'))::INTEGER AS tempo_key,
  transaction_date AS data,
  EXTRACT(HOUR FROM transaction_time)::SMALLINT AS hora,
  EXTRACT(YEAR FROM transaction_date)::SMALLINT AS ano,
  EXTRACT(MONTH FROM transaction_date)::SMALLINT AS mes,
  CASE EXTRACT(MONTH FROM transaction_date)::INTEGER
    WHEN 1 THEN 'Janeiro'
    WHEN 2 THEN 'Fevereiro'
    WHEN 3 THEN 'Marco'
    WHEN 4 THEN 'Abril'
    WHEN 5 THEN 'Maio'
    WHEN 6 THEN 'Junho'
    WHEN 7 THEN 'Julho'
    WHEN 8 THEN 'Agosto'
    WHEN 9 THEN 'Setembro'
    WHEN 10 THEN 'Outubro'
    WHEN 11 THEN 'Novembro'
    WHEN 12 THEN 'Dezembro'
  END AS nome_mes,
  EXTRACT(QUARTER FROM transaction_date)::SMALLINT AS trimestre,
  EXTRACT(DAY FROM transaction_date)::SMALLINT AS dia_mes,
  EXTRACT(ISODOW FROM transaction_date)::SMALLINT AS dia_semana_num,
  CASE EXTRACT(ISODOW FROM transaction_date)::INTEGER
    WHEN 1 THEN 'Segunda-feira'
    WHEN 2 THEN 'Terca-feira'
    WHEN 3 THEN 'Quarta-feira'
    WHEN 4 THEN 'Quinta-feira'
    WHEN 5 THEN 'Sexta-feira'
    WHEN 6 THEN 'Sabado'
    WHEN 7 THEN 'Domingo'
  END AS nome_dia_semana,
  EXTRACT(ISODOW FROM transaction_date)::INTEGER IN (6, 7) AS fim_de_semana,
  CASE
    WHEN EXTRACT(HOUR FROM transaction_time)::INTEGER <= 10 THEN 'Manha'
    WHEN EXTRACT(HOUR FROM transaction_time)::INTEGER <= 14 THEN 'Almoco'
    WHEN EXTRACT(HOUR FROM transaction_time)::INTEGER <= 18 THEN 'Tarde'
    ELSE 'Noite'
  END AS periodo_dia
FROM coffee_dw.stg_coffee_sales
ORDER BY data, hora;

INSERT INTO coffee_dw.dim_loja (
  loja_key,
  localizacao,
  cidade,
  pais,
  rede,
  tipo_loja
)
SELECT DISTINCT
  store_id AS loja_key,
  store_location AS localizacao,
  'New York' AS cidade,
  'Estados Unidos' AS pais,
  'Maven Roasters' AS rede,
  'Cafeteria' AS tipo_loja
FROM coffee_dw.stg_coffee_sales
ORDER BY loja_key;

INSERT INTO coffee_dw.dim_produto (
  produto_key,
  categoria,
  tipo_produto,
  detalhe_produto,
  preco_medio,
  preco_minimo,
  preco_maximo,
  faixa_preco
)
SELECT
  product_id AS produto_key,
  MIN(product_category) AS categoria,
  MIN(product_type) AS tipo_produto,
  MIN(product_detail) AS detalhe_produto,
  ROUND(AVG(unit_price), 2) AS preco_medio,
  MIN(unit_price) AS preco_minimo,
  MAX(unit_price) AS preco_maximo,
  CASE
    WHEN ROUND(AVG(unit_price), 2) < 3 THEN 'Baixo'
    WHEN ROUND(AVG(unit_price), 2) < 5 THEN 'Medio'
    ELSE 'Alto'
  END AS faixa_preco
FROM coffee_dw.stg_coffee_sales
GROUP BY product_id
ORDER BY produto_key;

INSERT INTO coffee_dw.fato_vendas (
  venda_key,
  transacao_id,
  tempo_key,
  loja_key,
  produto_key,
  quantidade,
  preco_unitario,
  receita
)
SELECT
  ROW_NUMBER() OVER (ORDER BY transaction_id)::INTEGER AS venda_key,
  transaction_id AS transacao_id,
  (TO_CHAR(transaction_date, 'YYYYMMDD') || LPAD(EXTRACT(HOUR FROM transaction_time)::TEXT, 2, '0'))::INTEGER AS tempo_key,
  store_id AS loja_key,
  product_id AS produto_key,
  transaction_qty::SMALLINT AS quantidade,
  unit_price AS preco_unitario,
  ROUND(transaction_qty * unit_price, 2) AS receita
FROM coffee_dw.stg_coffee_sales
ORDER BY transaction_id;

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

SELECT 'staging_rows' AS check_name, COUNT(*) AS value
FROM coffee_dw.stg_coffee_sales;

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

SELECT 'receita_total' AS check_name, ROUND(SUM(receita), 2) AS value
FROM coffee_dw.fato_vendas;

SELECT 'quantidade_total' AS check_name, SUM(quantidade) AS value
FROM coffee_dw.fato_vendas;

SELECT *
FROM coffee_dw.vw_receita_mensal_loja_categoria
ORDER BY receita_total DESC
LIMIT 10;

SELECT *
FROM coffee_dw.vw_demanda_horaria_produto
ORDER BY quantidade_vendida DESC
LIMIT 10;
