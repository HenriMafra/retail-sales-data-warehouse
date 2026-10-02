# Roteiro Completo Com SQL

Este documento e o passo a passo completo para fazer o projeto **Coffee Shop Sales - Data Warehouse + Machine Learning** manualmente, entendendo cada parte.

Use como roteiro de execucao, roteiro de estudo e guia para apresentacao.

## 0. Objetivo Do Projeto

Construir uma solucao completa de dados:

1. Escolher e validar um dataset publico.
2. Preparar os dados.
3. Criar um Data Warehouse no PostgreSQL.
4. Usar modelagem dimensional em star schema.
5. Criar views analiticas.
6. Fazer analise exploratoria em Python.
7. Treinar modelos de Machine Learning.
8. Comparar os modelos.
9. Gerar insights de negocio.
10. Montar slides e apresentar.

Pergunta central:

> Quais fatores explicam maior receita e maior demanda por loja, produto, mes, dia da semana e horario?

## 1. Materiais Necessarios

Instalem ou tenham acesso a:

- PostgreSQL.
- pgAdmin ou psql.
- Python 3.
- Jupyter Notebook ou VS Code.
- Excel ou LibreOffice para abrir o dataset.
- GitHub, se forem entregar tambem como repositorio.

Bibliotecas Python:

```bash
pip install pandas numpy matplotlib seaborn scikit-learn openpyxl nbformat
```

## 2. Estrutura De Pastas

Organizem o projeto assim:

```text
coffee-shop-sales-dw-ml/
  data/
    raw/
      Coffee Shop Sales.xlsx
    processed/
      dim_tempo.csv
      dim_loja.csv
      dim_produto.csv
      fato_vendas.csv
      ml_vendas_agregado.csv
  docs/
    modelagem_dw.md
    roteiro_apresentacao.md
    roteiro_execucao_manual.md
    roteiro_completo_com_sql.md
  notebooks/
    coffee_shop_dw_ml.ipynb
  reports/
    figures/
    metrics.json
    relatorio_executivo.md
  scripts/
    prepare_data.py
    analyze_and_export_assets.py
  slides/
    coffee_shop_sales_dw_ml.pptx
    roteiro_execucao_manual.pptx
  sql/
    00_create_database.sql
    01_schema_dw.sql
    02_load_dw.sql
    03_views_analiticas.sql
    04_quality_checks.sql
  README.md
  requirements.txt
```

## 3. Dataset

Dataset escolhido:

- Nome: `Coffee Shop Sales`.
- Fonte: Maven Analytics / Kaggle.
- Arquivo: `Coffee Shop Sales.xlsx`.

Conferencias obrigatorias:

```text
Registros: 149.116
Colunas originais: 11
Periodo: 2023-01-01 a 2023-06-30
Lojas: 3
Produtos: 80
Categorias: 9
```

Colunas originais:

```text
transaction_id
transaction_date
transaction_time
transaction_qty
store_id
store_location
product_id
unit_price
product_category
product_type
product_detail
```

O que falar:

> O dataset atende aos requisitos porque tem mais de 10.000 registros, possui variaveis numericas, categoricas e temporais, e permite analisar vendas por loja, produto e tempo.

## 4. Preparacao Dos Dados

Abram o dataset e criem as colunas necessarias.

Se forem fazer no Excel, usem o guia detalhado:

```text
docs/guia_excel_preparacao_dados.md
```

As colunas originais ficam assim no arquivo `Coffee Shop Sales.xlsx`:

| Letra | Coluna |
|---|---|
| A | `transaction_id` |
| B | `transaction_date` |
| C | `transaction_time` |
| D | `transaction_qty` |
| E | `store_id` |
| F | `store_location` |
| G | `product_id` |
| H | `unit_price` |
| I | `product_category` |
| J | `product_type` |
| K | `product_detail` |

Criem as colunas derivadas a partir da coluna `L`:

| Letra | Nova coluna | Formula em portugues |
|---|---|---|
| L | `receita` | `=D2*H2` |
| M | `hora` | `=HORA(C2)` |
| N | `tempo_key` | `=VALOR(TEXTO(B2;"aaaammdd")&TEXTO(M2;"00"))` |
| O | `ano` | `=ANO(B2)` |
| P | `mes` | `=MÊS(B2)` |
| Q | `nome_mes` | `=TEXTO(B2;"mmmm")` |
| R | `trimestre` | `=ARREDONDAR.PARA.CIMA(MÊS(B2)/3;0)` |
| S | `dia_mes` | `=DIA(B2)` |
| T | `dia_semana_num` | `=DIA.DA.SEMANA(B2;2)` |
| U | `nome_dia_semana` | `=TEXTO(B2;"dddd")` |
| V | `fim_de_semana` | `=SE(T2>=6;"true";"false")` |
| W | `periodo_dia` | `=SE(M2<=10;"Manha";SE(M2<=14;"Almoco";SE(M2<=18;"Tarde";"Noite")))` |

Depois de digitar na linha 2, arrastem todas as formulas ate a ultima linha do dataset.

### 4.1 Criar Receita

Formula:

```text
receita = transaction_qty * unit_price
```

Exemplo:

```text
transaction_qty = 2
unit_price = 3.00
receita = 6.00
```

### 4.2 Criar Hora

Extrair a hora de `transaction_time`.

Exemplo:

```text
07:06:11 -> 7
10:30:15 -> 10
```

### 4.3 Criar Chave De Tempo

Criar uma chave combinando data e hora.

Formato sugerido:

```text
YYYYMMDDHH
```

Exemplo:

```text
2023-01-01 as 7h -> 2023010107
```

No projeto, essa chave se chama:

```text
tempo_key
```

### 4.4 Criar Dimensoes E Fato

Arquivos finais esperados:

```text
dim_tempo.csv
dim_loja.csv
dim_produto.csv
fato_vendas.csv
```

Validacoes:

```text
dim_loja deve ter 3 linhas
dim_produto deve ter 80 linhas
fato_vendas deve ter 149.116 linhas
receita deve ser quantidade * preco_unitario
```

## 5. Modelagem Dimensional

Modelo usado:

```text
Star Schema
```

### 5.1 Tabela Fato

Tabela:

```text
fato_vendas
```

Grao:

> Uma linha por item vendido em uma transacao.

Campos:

```text
venda_key
transacao_id
tempo_key
loja_key
produto_key
quantidade
preco_unitario
receita
```

Medidas:

```text
quantidade
preco_unitario
receita
```

Dimensao degenerada:

```text
transacao_id
```

O que falar:

> O transacao_id e uma dimensao degenerada porque identifica a transacao, mas fica diretamente na tabela fato e nao precisa de uma dimensao propria.

### 5.2 Dimensao Tempo

Tabela:

```text
dim_tempo
```

Campos:

```text
tempo_key
data
hora
ano
mes
nome_mes
trimestre
dia_mes
dia_semana_num
nome_dia_semana
fim_de_semana
periodo_dia
```

### 5.3 Dimensao Loja

Tabela:

```text
dim_loja
```

Campos:

```text
loja_key
localizacao
cidade
pais
rede
tipo_loja
```

### 5.4 Dimensao Produto

Tabela:

```text
dim_produto
```

Campos:

```text
produto_key
categoria
tipo_produto
detalhe_produto
preco_medio
preco_minimo
preco_maximo
faixa_preco
```

## 6. Execucao No PostgreSQL

Ordem correta:

1. Criar banco.
2. Criar schema.
3. Criar tabelas.
4. Carregar dimensoes.
5. Carregar fato.
6. Criar views.
7. Rodar validacoes.

Entre na pasta raiz do projeto antes de rodar os comandos.

Exemplo:

```bash
cd "C:\Users\henri\Documents\New project 2"
```

## 7. SQL 00 - Criar Banco

Arquivo:

```text
sql/00_create_database.sql
```

Como executar:

```bash
psql -U postgres -d postgres -f sql/00_create_database.sql
```

Codigo SQL:

```sql
DROP DATABASE IF EXISTS coffee_shop_dw;

CREATE DATABASE coffee_shop_dw
  WITH
  ENCODING = 'UTF8'
  TEMPLATE = template0;
```

O que falar:

> Primeiro criamos um banco separado para o projeto, chamado coffee_shop_dw, para isolar as tabelas do Data Warehouse.

## 8. SQL 01 - Criar Schema, Dimensoes E Fato

Arquivo:

```text
sql/01_schema_dw.sql
```

Como executar:

```bash
psql -U postgres -d coffee_shop_dw -f sql/01_schema_dw.sql
```

Codigo SQL completo:

```sql
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
```

O que falar:

> Criamos um schema chamado coffee_dw. Depois criamos tres dimensoes e uma tabela fato. A fato possui chaves estrangeiras para tempo, loja e produto, garantindo integridade referencial.

## 9. SQL 02 - Carregar Dados

Arquivo:

```text
sql/02_load_dw.sql
```

Importante:

Execute este script a partir da raiz do projeto, porque os caminhos dos CSVs sao relativos.

Como executar:

```bash
psql -U postgres -d coffee_shop_dw -f sql/02_load_dw.sql
```

Codigo:

```sql
\copy coffee_dw.dim_tempo
FROM 'data/processed/dim_tempo.csv'
WITH (FORMAT csv, HEADER true, ENCODING 'UTF8');

\copy coffee_dw.dim_loja
FROM 'data/processed/dim_loja.csv'
WITH (FORMAT csv, HEADER true, ENCODING 'UTF8');

\copy coffee_dw.dim_produto
FROM 'data/processed/dim_produto.csv'
WITH (FORMAT csv, HEADER true, ENCODING 'UTF8');

\copy coffee_dw.fato_vendas
FROM 'data/processed/fato_vendas.csv'
WITH (FORMAT csv, HEADER true, ENCODING 'UTF8');
```

O que falar:

> Carregamos primeiro as dimensoes e depois a fato, porque a fato depende das chaves das dimensoes.

## 10. SQL 03 - Criar Views Analiticas

Arquivo:

```text
sql/03_views_analiticas.sql
```

Como executar:

```bash
psql -U postgres -d coffee_shop_dw -f sql/03_views_analiticas.sql
```

### 10.1 View 1 - Receita Mensal Por Loja E Categoria

Objetivo:

> Analisar receita e quantidade por mes, loja e categoria.

Codigo:

```sql
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
```

Perguntas que essa view responde:

- Qual loja teve mais receita?
- Qual categoria vendeu mais?
- Qual mes teve maior receita?
- Como cada loja performa por categoria?

### 10.2 View 2 - Demanda Horaria Por Produto

Objetivo:

> Entender demanda por dia da semana, hora, loja, categoria e tipo de produto.

Codigo:

```sql
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
```

Perguntas que essa view responde:

- Qual horario tem maior demanda?
- O pico e de manha, tarde ou noite?
- Cada loja tem comportamento diferente?
- Quais produtos precisam de estoque por horario?

### 10.3 View Extra - Ranking De Produtos

Objetivo:

> Identificar produtos lideres em receita e quantidade.

Codigo:

```sql
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
```

O que falar:

> O professor pediu duas views, mas criamos uma terceira para apoiar os insights de produto.

## 11. SQL 04 - Validacoes

Arquivo:

```text
sql/04_quality_checks.sql
```

Como executar:

```bash
psql -U postgres -d coffee_shop_dw -f sql/04_quality_checks.sql
```

Codigo completo:

```sql
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
```

Resultados esperados:

```text
fato_vendas_rows = 149116
receita_formula_erros = 0
dim_loja_rows = 3
dim_produto_rows = 80
dim_tempo_rows = 2512
```

O que falar:

> Essas consultas validam se a carga foi feita corretamente, se a receita foi calculada certo e se as views retornam dados uteis.

## 12. Analise Exploratoria Em Python

Abrir:

```text
notebooks/coffee_shop_dw_ml.ipynb
```

Ordem das celulas:

1. Importar bibliotecas.
2. Carregar `Coffee Shop Sales.xlsx`.
3. Mostrar primeiras linhas.
4. Mostrar quantidade de linhas e colunas.
5. Verificar tipos das colunas.
6. Verificar nulos.
7. Criar coluna `revenue`.
8. Criar colunas `month`, `weekday` e `hour`.
9. Calcular metricas gerais.
10. Criar graficos.

Metricas que precisam aparecer:

```text
Receita total: 698812.33
Itens vendidos: 214470
Lojas: 3
Produtos: 80
Categorias: 9
Loja lider: Hell's Kitchen
Categoria lider: Coffee
Produto lider em receita: Barista Espresso
Pico de demanda: 10h
```

## 13. Graficos Obrigatorios

### 13.1 Distribuicao

Grafico recomendado:

```text
Distribuicao da quantidade por transacao
```

O que mostrar:

> A maioria das transacoes tem poucos itens, comportamento comum em cafeterias.

### 13.2 Comparacao Entre Categorias

Graficos recomendados:

```text
Receita por loja
Receita por categoria
```

O que mostrar:

> Hell's Kitchen lidera em receita e Coffee e a categoria mais importante.

### 13.3 Evolucao Temporal

Grafico recomendado:

```text
Receita mensal de janeiro a junho
```

O que mostrar:

> A receita cresce no segundo trimestre, com junho como melhor mes.

### 13.4 Grafico Extra Forte

Grafico recomendado:

```text
Demanda por hora e loja
```

O que mostrar:

> O pico de demanda acontece pela manha, especialmente perto das 10h.

## 14. Machine Learning

O ML deve ser explicado como previsao de demanda.

Nao falem que o modelo "adivinha produto"; isso fica artificial. O melhor e dizer:

> Usamos as vendas historicas para prever se uma combinacao de loja, produto e horario tera alta demanda.

### 14.1 Criar Base Agregada

Agrupar por:

```text
transaction_date
transaction_hour
store_location
product_category
product_type
```

Criar:

```text
quantidade_vendida
receita
preco_medio
transacoes
ano
mes
dia_mes
dia_semana
fim_de_semana
alta_demanda
```

### 14.2 Problema De Classificacao

Target:

```text
alta_demanda
```

Regra:

```text
alta_demanda = 1 se quantidade_vendida >= quartil 75
alta_demanda = 0 caso contrario
```

Modelos:

```text
KNN
Arvore de Decisao
Random Forest
Logistic Regression
```

Metricas:

```text
Accuracy
Precision
Recall
F1-score
Matriz de confusao
```

### 14.3 Problema De Regressao

Target:

```text
quantidade_vendida
```

Modelo:

```text
Regressao Linear
```

Metricas:

```text
MAE
RMSE
R2
```

## 15. Resultados Dos Modelos

Classificacao:

| Modelo | Accuracy | Precision | Recall | F1 |
|---|---:|---:|---:|---:|
| KNN | 0.7245 | 0.5722 | 0.4987 | 0.5329 |
| Arvore de Decisao | 0.8233 | 0.7284 | 0.7007 | 0.7143 |
| Random Forest | 0.8098 | 0.7652 | 0.5722 | 0.6548 |
| Logistic Regression | 0.7303 | 0.6057 | 0.4135 | 0.4915 |

Melhor modelo:

```text
Arvore de Decisao
```

O que falar:

> A Arvore de Decisao teve o melhor F1-score. Isso faz sentido porque a demanda depende de combinacoes entre horario, loja e produto, e arvores conseguem capturar regras nao lineares.

Regressao Linear:

```text
MAE = 1.6091
RMSE = 2.2356
R2 = 0.2464
```

O que falar:

> A Regressao Linear teve desempenho limitado porque a demanda nao e totalmente linear e o dataset nao tem variaveis como clima, feriados, promocoes e dados de cliente.

## 16. Insights De Negocio

Escolham entre 3 e 5 insights.

### Insight 1

```text
Hell's Kitchen lidera em receita.
```

Decisao:

```text
Priorizar estoque, equipe e disponibilidade dos produtos mais vendidos nessa loja.
```

### Insight 2

```text
O pico de demanda ocorre as 10h.
```

Decisao:

```text
Reforcar equipe e pre-preparo no periodo da manha.
```

### Insight 3

```text
Coffee e a categoria com maior receita.
```

Decisao:

```text
Tratar Coffee como categoria ancora do mix.
```

### Insight 4

```text
Barista Espresso lidera em receita.
```

Decisao:

```text
Usar esse produto em combos premium ou destaques comerciais.
```

### Insight 5

```text
Brewed Chai tea lidera em quantidade vendida.
```

Decisao:

```text
Usar produtos de alto giro para atrair clientes e vender itens complementares.
```

## 17. Slides Da Apresentacao Final

Arquivo:

```text
slides/coffee_shop_sales_dw_ml.pptx
```

Ordem recomendada:

1. Capa.
2. Dataset e requisitos.
3. Star schema.
4. PostgreSQL e scripts.
5. EDA temporal.
6. Lojas e categorias.
7. Demanda horaria.
8. Machine Learning.
9. Comparacao de modelos.
10. Insights e decisoes.

## 18. Divisao Da Fala

Grupo com 2 pessoas.

### Pessoa 1

Falar:

- Objetivo.
- Dataset.
- Requisitos atendidos.
- Modelagem dimensional.
- Star schema.
- PostgreSQL.
- Views e validacoes SQL.

Tempo:

```text
5 a 7 minutos
```

### Pessoa 2

Falar:

- EDA.
- Graficos.
- Machine Learning.
- Metricas.
- Comparacao dos modelos.
- Insights.
- Recomendacoes.

Tempo:

```text
5 a 7 minutos
```

## 19. Falas Prontas

### Abertura

> Nosso projeto constroi uma solucao completa de dados para vendas de uma cafeteria. A partir de um dataset publico com mais de 149 mil registros, criamos um Data Warehouse em PostgreSQL, fizemos analises exploratorias em Python, aplicamos modelos de Machine Learning e extraimos insights para apoiar decisoes de estoque, equipe e mix de produtos.

### Modelagem

> A modelagem escolhida foi star schema. Criamos uma tabela fato chamada fato_vendas, no grao de uma venda por item de transacao, e tres dimensoes principais: tempo, loja e produto. Tambem usamos o transacao_id como dimensao degenerada.

### SQL

> No PostgreSQL, criamos um schema especifico para o projeto, as tabelas dimensionais, a tabela fato com chaves estrangeiras, indices para consulta e views analiticas para responder perguntas de negocio.

### Machine Learning

> Para o Machine Learning, transformamos o problema em previsao de demanda. Criamos uma base agregada por data, hora, loja e produto. Para classificacao, criamos a variavel alta_demanda usando o quartil 75 da quantidade vendida.

### Comparacao

> O melhor modelo de classificacao foi a Arvore de Decisao, com maior F1-score. Ela consegue capturar regras combinadas entre horario, loja e produto. A Regressao Linear teve desempenho mais limitado, indicando que a demanda depende de relacoes nao lineares e de variaveis ausentes.

### Insights

> Os principais insights foram: Hell's Kitchen lidera a receita, o pico de demanda acontece as 10h, Coffee e a principal categoria por receita, Barista Espresso lidera em receita e Brewed Chai tea lidera em volume. Com isso, recomendamos reforco de estoque e equipe pela manha, foco nos produtos lideres e promocoes em horarios de menor movimento.

## 20. Checklist Final

Antes de entregar, confiram:

- Dataset esta na pasta `data/raw`.
- Dados processados estao em `data/processed`.
- Scripts SQL estao em `sql`.
- Banco `coffee_shop_dw` foi criado.
- Schema `coffee_dw` foi criado.
- Dimensoes foram carregadas.
- Fato foi carregada.
- Views foram criadas.
- Validacoes SQL foram executadas.
- Notebook abre e roda.
- Graficos aparecem.
- Todos os modelos obrigatorios foram treinados.
- Matriz de confusao aparece.
- Regressao Linear aparece.
- Comparacao dos modelos aparece.
- Insights aparecem.
- Slides estao prontos.
- Os dois integrantes sabem explicar.
- Apresentacao cabe em 10 a 15 minutos.

## 21. Ordem Final De Execucao

Se voces forem fazer tudo do zero, sigam exatamente esta ordem:

```text
1. Baixar dataset.
2. Abrir no Excel.
3. Conferir linhas e colunas.
4. Conferir variaveis numericas e categoricas.
5. Definir pergunta de negocio.
6. Criar coluna receita.
7. Criar colunas de tempo.
8. Criar dim_tempo.
9. Criar dim_loja.
10. Criar dim_produto.
11. Criar fato_vendas.
12. Validar CSVs.
13. Criar banco PostgreSQL.
14. Criar schema.
15. Criar tabelas.
16. Carregar dimensoes.
17. Carregar fato.
18. Criar views.
19. Rodar quality checks.
20. Abrir notebook.
21. Fazer EDA.
22. Criar graficos.
23. Preparar base agregada de ML.
24. Separar treino e teste.
25. Treinar modelos de classificacao.
26. Treinar regressao linear.
27. Calcular metricas.
28. Comparar modelos.
29. Escrever insights.
30. Montar slides.
31. Dividir fala.
32. Ensaiar.
33. Entregar.
```

## 22. Conclusao Recomendada

> O projeto mostrou como transformar dados transacionais em uma solucao analitica completa. O Data Warehouse organizou as vendas por tempo, loja e produto; a analise exploratoria revelou padroes de receita e demanda; e o Machine Learning permitiu comparar modelos para previsao de alta demanda. Os resultados podem apoiar decisoes praticas de estoque, equipe, promocoes e mix de produtos.
