-- Execute conectado ao banco coffee_shop_dw:
-- psql -U postgres -d coffee_shop_dw -f sql/01_schema_dw.sql

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

CREATE INDEX idx_fato_vendas_tempo ON coffee_dw.fato_vendas (tempo_key);
CREATE INDEX idx_fato_vendas_loja ON coffee_dw.fato_vendas (loja_key);
CREATE INDEX idx_fato_vendas_produto ON coffee_dw.fato_vendas (produto_key);
CREATE INDEX idx_fato_vendas_transacao ON coffee_dw.fato_vendas (transacao_id);

COMMENT ON TABLE coffee_dw.fato_vendas IS
  'Tabela fato em star schema. transacao_id e uma dimensao degenerada mantida diretamente na fato.';
