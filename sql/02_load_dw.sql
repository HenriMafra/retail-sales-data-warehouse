-- Execute a partir da raiz do projeto, conectado ao banco coffee_shop_dw:
-- psql -U postgres -d coffee_shop_dw -f sql/02_load_dw.sql

\copy coffee_dw.dim_tempo FROM 'data/processed/dim_tempo.csv' WITH (FORMAT csv, HEADER true, ENCODING 'UTF8');
\copy coffee_dw.dim_loja FROM 'data/processed/dim_loja.csv' WITH (FORMAT csv, HEADER true, ENCODING 'UTF8');
\copy coffee_dw.dim_produto FROM 'data/processed/dim_produto.csv' WITH (FORMAT csv, HEADER true, ENCODING 'UTF8');
\copy coffee_dw.fato_vendas FROM 'data/processed/fato_vendas.csv' WITH (FORMAT csv, HEADER true, ENCODING 'UTF8');
