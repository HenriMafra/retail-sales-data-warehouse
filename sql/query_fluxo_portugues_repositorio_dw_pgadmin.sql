-- FLUXO COMPLETO EM SQL COM SCHEMA REPOSITORIO + SCHEMA DW
--
-- Rode no pgAdmin Query Tool conectado ao banco onde voce quer criar o projeto.
--
-- Ideia do modelo:
-- 1. cafe_repositorio = guarda os dados crus vindos do Excel, tudo como TEXT.
-- 2. cafe_dw = guarda a modelagem dimensional tratada, com dimensoes e fato.
--
-- Observacao sobre nomes:
-- Usei nomes sem acento: cafe_repositorio, cafe_dw.
-- PostgreSQL ate aceita acento se usar aspas, por exemplo "café_repositório",
-- mas isso complica todas as queries. Na apresentacao voces podem chamar de
-- "schema cafe repositorio" e "schema cafe DW".
--
-- Antes de rodar:
-- Gere ou salve o Excel como CSV UTF-8 neste caminho:
-- C:/Users/henri/Documents/New project 2/data/raw/coffee_shop_sales_raw.csv

DROP SCHEMA IF EXISTS cafe_dw CASCADE;
DROP SCHEMA IF EXISTS cafe_repositorio CASCADE;

CREATE SCHEMA cafe_repositorio;
CREATE SCHEMA cafe_dw;

-- =========================================================
-- 1. REPOSITORIO: DADOS BRUTOS DO EXCEL, TUDO COMO TEXT
-- =========================================================

CREATE TABLE cafe_repositorio.vendas_excel_bruto (
  transaction_id TEXT,
  transaction_date TEXT,
  transaction_time TEXT,
  transaction_qty TEXT,
  store_id TEXT,
  store_location TEXT,
  product_id TEXT,
  unit_price TEXT,
  product_category TEXT,
  product_type TEXT,
  product_detail TEXT
);

COPY cafe_repositorio.vendas_excel_bruto
FROM 'C:/Users/henri/Documents/New project 2/data/raw/coffee_shop_sales_raw.csv'
WITH (FORMAT csv, HEADER true, ENCODING 'UTF8');

-- Conferencia inicial do repositorio.
SELECT 'linhas_repositorio' AS verificacao, COUNT(*) AS valor
FROM cafe_repositorio.vendas_excel_bruto;

-- =========================================================
-- 2. VIEW DE TRATAMENTO: CONVERTE TEXT PARA TIPOS CORRETOS
-- =========================================================

CREATE OR REPLACE VIEW cafe_repositorio.vw_vendas_tratadas AS
SELECT
  transaction_id::INTEGER AS transaction_id,
  transaction_date::DATE AS transaction_date,
  transaction_time::TIME AS transaction_time,
  transaction_qty::INTEGER AS transaction_qty,
  store_id::INTEGER AS store_id,
  store_location,
  product_id::INTEGER AS product_id,
  REPLACE(unit_price, ',', '.')::NUMERIC(10, 2) AS unit_price,
  product_category,
  product_type,
  product_detail,
  EXTRACT(HOUR FROM transaction_time::TIME)::SMALLINT AS hora,
  ROUND(transaction_qty::NUMERIC * REPLACE(unit_price, ',', '.')::NUMERIC(10, 2), 2) AS receita,
  (
    TO_CHAR(transaction_date::DATE, 'YYYYMMDD') ||
    LPAD(EXTRACT(HOUR FROM transaction_time::TIME)::TEXT, 2, '0')
  )::INTEGER AS tempo_key
FROM cafe_repositorio.vendas_excel_bruto;

-- Conferencia da view tratada.
SELECT *
FROM cafe_repositorio.vw_vendas_tratadas
LIMIT 10;

-- =========================================================
-- 3. DW: DIMENSOES E FATO
-- =========================================================

CREATE TABLE cafe_dw.dim_tempo (
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

CREATE TABLE cafe_dw.dim_loja (
  loja_key INTEGER PRIMARY KEY,
  localizacao VARCHAR(80) NOT NULL,
  cidade VARCHAR(80) NOT NULL,
  pais VARCHAR(80) NOT NULL,
  rede VARCHAR(80) NOT NULL,
  tipo_loja VARCHAR(40) NOT NULL
);

CREATE TABLE cafe_dw.dim_produto (
  produto_key INTEGER PRIMARY KEY,
  categoria VARCHAR(80) NOT NULL,
  tipo_produto VARCHAR(120) NOT NULL,
  detalhe_produto VARCHAR(160) NOT NULL,
  preco_medio NUMERIC(10, 2) NOT NULL,
  preco_minimo NUMERIC(10, 2) NOT NULL,
  preco_maximo NUMERIC(10, 2) NOT NULL,
  faixa_preco VARCHAR(20) NOT NULL
);

CREATE TABLE cafe_dw.fato_vendas (
  venda_key INTEGER PRIMARY KEY,
  transacao_id INTEGER NOT NULL,
  tempo_key INTEGER NOT NULL REFERENCES cafe_dw.dim_tempo (tempo_key),
  loja_key INTEGER NOT NULL REFERENCES cafe_dw.dim_loja (loja_key),
  produto_key INTEGER NOT NULL REFERENCES cafe_dw.dim_produto (produto_key),
  quantidade SMALLINT NOT NULL CHECK (quantidade > 0),
  preco_unitario NUMERIC(10, 2) NOT NULL CHECK (preco_unitario >= 0),
  receita NUMERIC(12, 2) NOT NULL CHECK (receita >= 0)
);

COMMENT ON SCHEMA cafe_repositorio IS
  'Schema repositorio: dados crus vindos do Excel, mantidos como texto.';

COMMENT ON SCHEMA cafe_dw IS
  'Schema dimensional: star schema com dimensoes e fato.';

COMMENT ON TABLE cafe_dw.fato_vendas IS
  'Tabela fato do star schema. transacao_id e dimensao degenerada mantida diretamente na fato.';

-- =========================================================
-- 4. CARGA DAS DIMENSOES
-- =========================================================

INSERT INTO cafe_dw.dim_tempo (
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
  tempo_key,
  transaction_date AS data,
  hora,
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
    WHEN hora <= 10 THEN 'Manha'
    WHEN hora <= 14 THEN 'Almoco'
    WHEN hora <= 18 THEN 'Tarde'
    ELSE 'Noite'
  END AS periodo_dia
FROM cafe_repositorio.vw_vendas_tratadas
ORDER BY data, hora;

INSERT INTO cafe_dw.dim_loja (
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
FROM cafe_repositorio.vw_vendas_tratadas
ORDER BY loja_key;

INSERT INTO cafe_dw.dim_produto (
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
FROM cafe_repositorio.vw_vendas_tratadas
GROUP BY product_id
ORDER BY produto_key;

-- =========================================================
-- 5. CARGA DA FATO
-- =========================================================

INSERT INTO cafe_dw.fato_vendas (
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
  tempo_key,
  store_id AS loja_key,
  product_id AS produto_key,
  transaction_qty::SMALLINT AS quantidade,
  unit_price AS preco_unitario,
  receita
FROM cafe_repositorio.vw_vendas_tratadas
ORDER BY transaction_id;

CREATE INDEX idx_fato_vendas_tempo
  ON cafe_dw.fato_vendas (tempo_key);

CREATE INDEX idx_fato_vendas_loja
  ON cafe_dw.fato_vendas (loja_key);

CREATE INDEX idx_fato_vendas_produto
  ON cafe_dw.fato_vendas (produto_key);

CREATE INDEX idx_fato_vendas_transacao
  ON cafe_dw.fato_vendas (transacao_id);

-- =========================================================
-- 6. VIEWS ANALITICAS
-- =========================================================

CREATE OR REPLACE VIEW cafe_dw.vw_receita_mensal_loja_categoria AS
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
FROM cafe_dw.fato_vendas f
JOIN cafe_dw.dim_tempo t
  ON t.tempo_key = f.tempo_key
JOIN cafe_dw.dim_loja l
  ON l.loja_key = f.loja_key
JOIN cafe_dw.dim_produto p
  ON p.produto_key = f.produto_key
GROUP BY
  t.ano,
  t.mes,
  t.nome_mes,
  l.localizacao,
  p.categoria;

CREATE OR REPLACE VIEW cafe_dw.vw_demanda_horaria_produto AS
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
FROM cafe_dw.fato_vendas f
JOIN cafe_dw.dim_tempo t
  ON t.tempo_key = f.tempo_key
JOIN cafe_dw.dim_loja l
  ON l.loja_key = f.loja_key
JOIN cafe_dw.dim_produto p
  ON p.produto_key = f.produto_key
GROUP BY
  t.nome_dia_semana,
  t.dia_semana_num,
  t.hora,
  t.periodo_dia,
  l.localizacao,
  p.categoria,
  p.tipo_produto;

CREATE OR REPLACE VIEW cafe_dw.vw_ranking_produtos AS
SELECT
  p.categoria,
  p.tipo_produto,
  p.detalhe_produto,
  SUM(f.quantidade) AS quantidade_vendida,
  ROUND(SUM(f.receita), 2) AS receita_total,
  ROUND(SUM(f.receita) / NULLIF(SUM(f.quantidade), 0), 2) AS receita_media_por_item,
  COUNT(*) AS transacoes
FROM cafe_dw.fato_vendas f
JOIN cafe_dw.dim_produto p
  ON p.produto_key = f.produto_key
GROUP BY
  p.categoria,
  p.tipo_produto,
  p.detalhe_produto;

-- =========================================================
-- 7. VALIDACOES
-- =========================================================

SELECT 'repositorio_linhas_brutas' AS verificacao, COUNT(*) AS valor
FROM cafe_repositorio.vendas_excel_bruto;

SELECT 'fato_vendas_linhas' AS verificacao, COUNT(*) AS valor
FROM cafe_dw.fato_vendas;

SELECT 'erros_formula_receita' AS verificacao, COUNT(*) AS valor
FROM cafe_dw.fato_vendas
WHERE receita <> ROUND(quantidade * preco_unitario, 2);

SELECT 'dim_tempo_linhas' AS verificacao, COUNT(*) AS valor
FROM cafe_dw.dim_tempo;

SELECT 'dim_loja_linhas' AS verificacao, COUNT(*) AS valor
FROM cafe_dw.dim_loja;

SELECT 'dim_produto_linhas' AS verificacao, COUNT(*) AS valor
FROM cafe_dw.dim_produto;

SELECT 'receita_total' AS verificacao, ROUND(SUM(receita), 2) AS valor
FROM cafe_dw.fato_vendas;

SELECT 'quantidade_total' AS verificacao, SUM(quantidade) AS valor
FROM cafe_dw.fato_vendas;

SELECT *
FROM cafe_dw.vw_receita_mensal_loja_categoria
ORDER BY receita_total DESC
LIMIT 10;
