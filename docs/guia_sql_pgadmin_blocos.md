# Guia SQL por blocos no pgAdmin

Este guia e para fazer o projeto manualmente no pgAdmin, copiando e colando os
comandos em partes no Query Tool.

A arquitetura usada e:

- Banco de dados: `cafe_projeto`
- Schema repositorio: `cafe_repositorio`
- Schema dimensional/DW: `cafe_dw`
- Tabela bruta do Excel: `cafe_repositorio.vendas_excel_bruto`
- View de tratamento: `cafe_repositorio.vw_vendas_tratadas`
- Tabela fato: `cafe_dw.fato_vendas`
- Dimensoes: `cafe_dw.dim_tempo`, `cafe_dw.dim_loja`, `cafe_dw.dim_produto`

Importante: os nomes estao sem acento de proposito. PostgreSQL aceita acentos
com aspas, mas isso deixa todas as queries mais dificeis. Na apresentacao, voce
pode chamar de "cafe repositorio" e "cafe DW".

## Antes de comecar

O PostgreSQL nao le arquivo `.xlsx` diretamente com SQL puro. Para puxar os
dados por SQL, salve o Excel como CSV UTF-8.

Arquivo esperado:

```text
C:/Users/henri/Documents/New project 2/data/raw/coffee_shop_sales_raw.csv
```

Se o arquivo estiver em outro caminho, troque o caminho no bloco de `COPY`.

O arquivo CSV precisa ter estas colunas no cabecalho:

```text
transaction_id,transaction_date,transaction_time,transaction_qty,store_id,store_location,product_id,unit_price,product_category,product_type,product_detail
```

## Como executar

1. Abra o pgAdmin.
2. Conecte no servidor local.
3. Abra o Query Tool.
4. Copie um bloco por vez.
5. Clique em executar.
6. Confira o resultado.
7. Va para o proximo bloco.

Nao precisa executar tudo de uma vez.

## Bloco 1A - apagar o banco antigo, se existir

Onde rodar: Query Tool conectado no banco `postgres`.

Use este bloco se voce quer recomecar do zero.

```sql
DROP DATABASE IF EXISTS cafe_projeto WITH (FORCE);
```

Resultado esperado: mensagem de sucesso. Se o banco nao existir, tudo bem.

## Bloco 1B - criar o banco vazio

Onde rodar: Query Tool conectado no banco `postgres`.

```sql
CREATE DATABASE cafe_projeto
WITH
  ENCODING = 'UTF8'
  TEMPLATE = template0;
```

Resultado esperado: banco `cafe_projeto` criado.

Depois disso, no pgAdmin:

1. Clique com o botao direito em `Databases`.
2. Clique em `Refresh`.
3. Abra o banco `cafe_projeto`.
4. Abra um novo Query Tool em cima do banco `cafe_projeto`.

Todos os proximos blocos devem ser rodados dentro do banco `cafe_projeto`.

## Bloco 2 - criar os schemas

Onde rodar: Query Tool conectado no banco `cafe_projeto`.

```sql
CREATE SCHEMA cafe_repositorio;

CREATE SCHEMA cafe_dw;

COMMENT ON SCHEMA cafe_repositorio IS
  'Schema repositorio: guarda os dados crus vindos do Excel, tudo como texto.';

COMMENT ON SCHEMA cafe_dw IS
  'Schema DW: guarda a modelagem dimensional em star schema.';
```

Conferencia:

```sql
SELECT schema_name
FROM information_schema.schemata
WHERE schema_name IN ('cafe_repositorio', 'cafe_dw')
ORDER BY schema_name;
```

Resultado esperado:

```text
cafe_dw
cafe_repositorio
```

## Bloco 3 - criar a tabela bruta do repositorio

Esta tabela representa o Excel cru. Todas as colunas ficam como `TEXT`.

```sql
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
```

Conferencia:

```sql
SELECT
  table_schema,
  table_name
FROM information_schema.tables
WHERE table_schema = 'cafe_repositorio'
ORDER BY table_name;
```

Resultado esperado: aparecer a tabela `vendas_excel_bruto`.

## Bloco 4 - carregar o CSV local para a tabela bruta

Aqui o PostgreSQL puxa o arquivo local e coloca tudo na tabela bruta.

```sql
COPY cafe_repositorio.vendas_excel_bruto
FROM 'C:/Users/henri/Documents/New project 2/data/raw/coffee_shop_sales_raw.csv'
WITH (FORMAT csv, HEADER true, ENCODING 'UTF8');
```

Se der erro de permissao ou caminho, use um caminho mais simples:

1. Crie a pasta `C:/temp`.
2. Copie o CSV para `C:/temp/coffee_shop_sales_raw.csv`.
3. Rode este comando:

```sql
COPY cafe_repositorio.vendas_excel_bruto
FROM 'C:/temp/coffee_shop_sales_raw.csv'
WITH (FORMAT csv, HEADER true, ENCODING 'UTF8');
```

## Bloco 5 - conferir se os dados brutos entraram

```sql
SELECT
  'linhas_no_repositorio' AS verificacao,
  COUNT(*) AS valor
FROM cafe_repositorio.vendas_excel_bruto;
```

Resultado esperado:

```text
149116
```

Agora veja as primeiras linhas:

```sql
SELECT *
FROM cafe_repositorio.vendas_excel_bruto
LIMIT 10;
```

Resultado esperado: dados aparecendo ainda como texto.

## Bloco 6 - criar a view tratada

Esta e a parte que resolve a duvida sobre Excel.

Nao precisa criar `receita`, `hora` ou `tempo_key` com formulas no Excel. Aqui o
SQL cria tudo:

- `hora`: vem de `EXTRACT(HOUR FROM transaction_time::TIME)`
- `receita`: vem de `transaction_qty * unit_price`
- `tempo_key`: junta data + hora para ligar a fato com a dimensao tempo

```sql
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
  ROUND(
    transaction_qty::NUMERIC * REPLACE(unit_price, ',', '.')::NUMERIC(10, 2),
    2
  ) AS receita,
  (
    TO_CHAR(transaction_date::DATE, 'YYYYMMDD') ||
    LPAD(EXTRACT(HOUR FROM transaction_time::TIME)::TEXT, 2, '0')
  )::INTEGER AS tempo_key
FROM cafe_repositorio.vendas_excel_bruto;
```

Conferencia:

```sql
SELECT *
FROM cafe_repositorio.vw_vendas_tratadas
LIMIT 10;
```

Resultado esperado: agora aparecem colunas com tipos certos e colunas criadas
pelo SQL, como `hora`, `receita` e `tempo_key`.

## Bloco 7 - validar a view tratada

Conferir quantidade de linhas:

```sql
SELECT
  'linhas_tratadas' AS verificacao,
  COUNT(*) AS valor
FROM cafe_repositorio.vw_vendas_tratadas;
```

Resultado esperado:

```text
149116
```

Conferir se a formula da receita esta correta:

```sql
SELECT
  'erros_formula_receita' AS verificacao,
  COUNT(*) AS valor
FROM cafe_repositorio.vw_vendas_tratadas
WHERE receita <> ROUND(transaction_qty * unit_price, 2);
```

Resultado esperado:

```text
0
```

Conferir periodo dos dados:

```sql
SELECT
  MIN(transaction_date) AS primeira_data,
  MAX(transaction_date) AS ultima_data
FROM cafe_repositorio.vw_vendas_tratadas;
```

Resultado esperado:

```text
2023-01-01 ate 2023-06-30
```

## Bloco 8 - criar as tabelas do star schema

Aqui nasce o Data Warehouse.

Estrutura:

- `fato_vendas` fica no centro.
- `dim_tempo`, `dim_loja` e `dim_produto` ficam ao redor.
- `transacao_id` fica dentro da fato como dimensao degenerada.
- As dimensoes sao desnormalizadas, porque ja carregam atributos prontos para
  analise.

```sql
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

COMMENT ON TABLE cafe_dw.fato_vendas IS
  'Tabela fato do star schema. transacao_id e dimensao degenerada mantida diretamente na fato.';
```

Conferencia:

```sql
SELECT
  table_schema,
  table_name
FROM information_schema.tables
WHERE table_schema = 'cafe_dw'
ORDER BY table_name;
```

Resultado esperado:

```text
dim_loja
dim_produto
dim_tempo
fato_vendas
```

## Bloco 9 - carregar a dimensao tempo

```sql
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
```

Conferencia:

```sql
SELECT COUNT(*) AS linhas_dim_tempo
FROM cafe_dw.dim_tempo;
```

Resultado esperado:

```text
2512
```

## Bloco 10 - carregar a dimensao loja

```sql
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
```

Conferencia:

```sql
SELECT *
FROM cafe_dw.dim_loja
ORDER BY loja_key;
```

Resultado esperado: 3 lojas.

## Bloco 11 - carregar a dimensao produto

```sql
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
```

Conferencia:

```sql
SELECT COUNT(*) AS linhas_dim_produto
FROM cafe_dw.dim_produto;
```

Resultado esperado:

```text
80
```

## Bloco 12 - carregar a tabela fato

```sql
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
```

Conferencia:

```sql
SELECT COUNT(*) AS linhas_fato_vendas
FROM cafe_dw.fato_vendas;
```

Resultado esperado:

```text
149116
```

## Bloco 13 - criar indices

Os indices ajudam nas consultas com joins e filtros.

```sql
CREATE INDEX idx_fato_vendas_tempo
  ON cafe_dw.fato_vendas (tempo_key);

CREATE INDEX idx_fato_vendas_loja
  ON cafe_dw.fato_vendas (loja_key);

CREATE INDEX idx_fato_vendas_produto
  ON cafe_dw.fato_vendas (produto_key);

CREATE INDEX idx_fato_vendas_transacao
  ON cafe_dw.fato_vendas (transacao_id);
```

Conferencia:

```sql
SELECT indexname
FROM pg_indexes
WHERE schemaname = 'cafe_dw'
ORDER BY indexname;
```

Resultado esperado: aparecerem as chaves primarias e os indices criados.

## Bloco 14 - criar as views analiticas

Estas views sao as bases para analise, graficos e apresentacao.

View 1: receita e quantidade por mes, loja e categoria.

```sql
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
```

View 2: receita e quantidade por dia da semana, hora, loja e produto.

```sql
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
```

View 3: ranking de produtos.

```sql
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
```

Conferencia:

```sql
SELECT table_name
FROM information_schema.views
WHERE table_schema = 'cafe_dw'
ORDER BY table_name;
```

Resultado esperado:

```text
vw_demanda_horaria_produto
vw_ranking_produtos
vw_receita_mensal_loja_categoria
```

## Bloco 15 - validacoes finais obrigatorias

Validacao 1: o dataset tem mais de 10.000 linhas.

```sql
SELECT
  'dataset_maior_que_10000' AS validacao,
  CASE WHEN COUNT(*) >= 10000 THEN 'OK' ELSE 'ERRO' END AS resultado,
  COUNT(*) AS linhas
FROM cafe_repositorio.vendas_excel_bruto;
```

Validacao 2: a fato tem a mesma quantidade de registros da base bruta.

```sql
SELECT
  'fato_mesma_qtd_repositorio' AS validacao,
  CASE
    WHEN
      (SELECT COUNT(*) FROM cafe_dw.fato_vendas) =
      (SELECT COUNT(*) FROM cafe_repositorio.vendas_excel_bruto)
    THEN 'OK'
    ELSE 'ERRO'
  END AS resultado,
  (SELECT COUNT(*) FROM cafe_repositorio.vendas_excel_bruto) AS linhas_repositorio,
  (SELECT COUNT(*) FROM cafe_dw.fato_vendas) AS linhas_fato;
```

Validacao 3: receita igual a quantidade vezes preco unitario.

```sql
SELECT
  'formula_receita' AS validacao,
  CASE WHEN COUNT(*) = 0 THEN 'OK' ELSE 'ERRO' END AS resultado,
  COUNT(*) AS linhas_com_erro
FROM cafe_dw.fato_vendas
WHERE receita <> ROUND(quantidade * preco_unitario, 2);
```

Validacao 4: dimensoes preenchidas.

```sql
SELECT 'dim_tempo' AS tabela, COUNT(*) AS linhas FROM cafe_dw.dim_tempo
UNION ALL
SELECT 'dim_loja' AS tabela, COUNT(*) AS linhas FROM cafe_dw.dim_loja
UNION ALL
SELECT 'dim_produto' AS tabela, COUNT(*) AS linhas FROM cafe_dw.dim_produto
UNION ALL
SELECT 'fato_vendas' AS tabela, COUNT(*) AS linhas FROM cafe_dw.fato_vendas;
```

Resultado esperado:

```text
dim_tempo    2512
dim_loja     3
dim_produto  80
fato_vendas  149116
```

Validacao 5: totais principais.

```sql
SELECT
  ROUND(SUM(receita), 2) AS receita_total,
  SUM(quantidade) AS quantidade_total
FROM cafe_dw.fato_vendas;
```

Resultado esperado:

```text
receita_total: 698812.33
quantidade_total: 214470
```

## Bloco 16 - consultas para visualizacoes

Estas consultas geram as tabelas que viram graficos no notebook, Excel, Power BI
ou nos slides.

Grafico de evolucao temporal: receita por mes.

```sql
SELECT
  ano,
  mes,
  nome_mes,
  ROUND(SUM(receita_total), 2) AS receita_total
FROM cafe_dw.vw_receita_mensal_loja_categoria
GROUP BY ano, mes, nome_mes
ORDER BY ano, mes;
```

Grafico de comparacao: receita por loja.

```sql
SELECT
  l.localizacao AS loja,
  ROUND(SUM(f.receita), 2) AS receita_total,
  SUM(f.quantidade) AS quantidade_vendida
FROM cafe_dw.fato_vendas f
JOIN cafe_dw.dim_loja l
  ON l.loja_key = f.loja_key
GROUP BY l.localizacao
ORDER BY receita_total DESC;
```

Grafico de comparacao: receita por categoria.

```sql
SELECT
  p.categoria,
  ROUND(SUM(f.receita), 2) AS receita_total,
  SUM(f.quantidade) AS quantidade_vendida
FROM cafe_dw.fato_vendas f
JOIN cafe_dw.dim_produto p
  ON p.produto_key = f.produto_key
GROUP BY p.categoria
ORDER BY receita_total DESC;
```

Grafico de distribuicao: quantidade de vendas por hora.

```sql
SELECT
  t.hora,
  COUNT(*) AS transacoes,
  SUM(f.quantidade) AS quantidade_vendida,
  ROUND(SUM(f.receita), 2) AS receita_total
FROM cafe_dw.fato_vendas f
JOIN cafe_dw.dim_tempo t
  ON t.tempo_key = f.tempo_key
GROUP BY t.hora
ORDER BY t.hora;
```

Ranking de produtos mais lucrativos.

```sql
SELECT *
FROM cafe_dw.vw_ranking_produtos
ORDER BY receita_total DESC
LIMIT 10;
```

Ranking de produtos mais vendidos.

```sql
SELECT *
FROM cafe_dw.vw_ranking_produtos
ORDER BY quantidade_vendida DESC
LIMIT 10;
```

Melhores combinacoes de loja, dia e hora.

```sql
SELECT
  loja,
  nome_dia_semana,
  hora,
  SUM(quantidade_vendida) AS quantidade_vendida,
  ROUND(SUM(receita_total), 2) AS receita_total
FROM cafe_dw.vw_demanda_horaria_produto
GROUP BY loja, nome_dia_semana, dia_semana_num, hora
ORDER BY receita_total DESC
LIMIT 15;
```

## Bloco 17 - consulta para mostrar o star schema

Use esta consulta para mostrar, no resultado do pgAdmin, que a fato se conecta
as dimensoes.

```sql
SELECT
  f.venda_key,
  f.transacao_id,
  t.data,
  t.hora,
  t.nome_dia_semana,
  l.localizacao AS loja,
  p.categoria,
  p.tipo_produto,
  f.quantidade,
  f.preco_unitario,
  f.receita
FROM cafe_dw.fato_vendas f
JOIN cafe_dw.dim_tempo t
  ON t.tempo_key = f.tempo_key
JOIN cafe_dw.dim_loja l
  ON l.loja_key = f.loja_key
JOIN cafe_dw.dim_produto p
  ON p.produto_key = f.produto_key
ORDER BY f.venda_key
LIMIT 20;
```

## Como explicar para o professor

Use esta fala:

```text
Criamos dois schemas. O schema cafe_repositorio funciona como uma camada bruta,
recebendo os dados do Excel em formato texto, sem tratamento. Depois criamos uma
view de tratamento que converte tipos, calcula hora, receita e chave de tempo.
Com essa view, carregamos o schema cafe_dw, que segue star schema: uma tabela
fato de vendas no centro e tres dimensoes desnormalizadas ao redor: tempo, loja
e produto. Tambem usamos uma dimensao degenerada, que e o transacao_id mantido
diretamente na fato.
```

## O que cada parte atende da tarefa

- Dataset publico: Coffee Shop Sales, Kaggle/Maven Analytics.
- Star schema: `cafe_dw.fato_vendas` ligada a `dim_tempo`, `dim_loja` e `dim_produto`.
- Dimensoes desnormalizadas: cada dimensao tem varios atributos prontos para analise.
- Dimensao degenerada: `transacao_id` dentro da fato.
- Views analiticas: tres views no schema `cafe_dw`.
- EDA/visualizacoes: consultas do Bloco 16 alimentam graficos.
- Validacoes: Bloco 15 prova linha, receita, dimensoes e totais.

