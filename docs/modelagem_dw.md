# Modelagem Dimensional

## Objetivo

Construir um Data Warehouse em PostgreSQL para analisar vendas da Maven Roasters por tempo, loja e produto.

## Star Schema

### Fato: `fato_vendas`

Grão: uma linha por item vendido em uma transação.

Medidas:

- `quantidade`
- `preco_unitario`
- `receita`

Chaves:

- `tempo_key`
- `loja_key`
- `produto_key`

Dimensão degenerada:

- `transacao_id`

### Dimensão: `dim_tempo`

Representa data e hora da venda.

Principais atributos:

- data
- hora
- ano
- mês
- trimestre
- dia do mês
- dia da semana
- fim de semana
- período do dia

### Dimensão: `dim_loja`

Representa a loja onde a venda ocorreu.

Principais atributos:

- localização
- cidade
- país
- rede
- tipo de loja

### Dimensão: `dim_produto`

Representa o produto vendido.

Principais atributos:

- categoria
- tipo do produto
- detalhe do produto
- preço médio
- preço mínimo
- preço máximo
- faixa de preço

## Views Analíticas

`vw_receita_mensal_loja_categoria`

Mostra receita, quantidade, preço médio e transações por mês, loja e categoria.

`vw_demanda_horaria_produto`

Mostra quantidade, receita e transações por dia da semana, hora, loja, categoria e tipo de produto.

`vw_ranking_produtos`

Mostra ranking de produtos por quantidade vendida, receita e receita média por item.
