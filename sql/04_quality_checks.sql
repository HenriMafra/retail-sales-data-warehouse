-- Consultas de validacao para demonstrar criterio de aceite.

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
