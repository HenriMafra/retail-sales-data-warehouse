# Roteiro Da Apresentação

Tempo sugerido: 10 a 15 minutos.

## 1. Abertura

Apresentar o objetivo: construir uma solução completa de dados, indo de um dataset público até Data Warehouse, análise exploratória, Machine Learning e insights de negócio.

## 2. Dataset

Explicar que o dataset possui:

- `149.116` registros
- `11` colunas
- período de janeiro a junho de 2023
- três lojas em Nova York
- 80 produtos e 9 categorias

Ponto de atenção: a Maven Roasters é fictícia, mas o dataset é público e foi publicado para prática analítica.

## 3. Data Warehouse

Mostrar o star schema:

- fato de vendas
- dimensão tempo
- dimensão loja
- dimensão produto
- dimensão degenerada `transacao_id`

Explicar as duas views obrigatórias e a view extra de ranking de produtos.

## 4. Análise Exploratória

Mostrar:

- evolução mensal da receita
- comparação de receita por loja
- comparação de receita por categoria
- demanda por hora e loja
- distribuição da quantidade por transação

## 5. Machine Learning

Explicar a formulação:

- classificação de alta demanda
- regressão da quantidade vendida

Comparar KNN, Árvore de Decisão, Random Forest e Logistic Regression.

Resultado principal: a Árvore de Decisão teve melhor F1-score no recorte testado.

## 6. Insights

Apresentar 3 a 5 insights:

- Hell's Kitchen lidera receita.
- O pico de demanda ocorre às 10h.
- Coffee é a categoria mais relevante em receita.
- Barista Espresso lidera em receita.
- Brewed Chai tea lidera em quantidade vendida.

## 7. Recomendações

Sugerir:

- reforço de estoque e equipe no período da manhã
- priorização dos produtos líderes
- promoções para horários fracos
- combos com produtos de menor giro
- análise futura com dados de cliente, clima, feriados e campanhas
