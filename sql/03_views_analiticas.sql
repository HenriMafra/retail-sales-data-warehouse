-- Execute conectado ao banco coffee_shop_dw:
-- psql -U postgres -d coffee_shop_dw -f sql/03_views_analiticas.sql

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
JOIN coffee_dw.dim_tempo t ON t.tempo_key = f.tempo_key
JOIN coffee_dw.dim_loja l ON l.loja_key = f.loja_key
JOIN coffee_dw.dim_produto p ON p.produto_key = f.produto_key
GROUP BY t.ano, t.mes, t.nome_mes, l.localizacao, p.categoria;

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
JOIN coffee_dw.dim_tempo t ON t.tempo_key = f.tempo_key
JOIN coffee_dw.dim_loja l ON l.loja_key = f.loja_key
JOIN coffee_dw.dim_produto p ON p.produto_key = f.produto_key
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
JOIN coffee_dw.dim_produto p ON p.produto_key = f.produto_key
GROUP BY p.categoria, p.tipo_produto, p.detalhe_produto;
