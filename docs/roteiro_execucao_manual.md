# Roteiro Completo De Execução Manual

Este roteiro é para o grupo fazer o projeto **na mão**, entendendo cada etapa e conseguindo explicar tudo na apresentação.

Projeto: **Coffee Shop Sales - Data Warehouse + Machine Learning**

Entrega: **24/06/2026**

Grupo: **2 pessoas**

## 1. Entender O Que O Professor Pediu

Antes de mexer no código, confirmem os requisitos obrigatórios:

- Usar um dataset público.
- Ter no mínimo `10.000` registros.
- Ter variáveis numéricas e categóricas.
- Criar um Data Warehouse no PostgreSQL.
- Usar modelagem dimensional com star schema.
- Criar pelo menos:
  - 1 tabela fato.
  - 3 a 5 dimensões.
  - 2 views analíticas.
- Fazer análise exploratória em Python.
- Criar gráficos de:
  - distribuição.
  - comparação entre categorias.
  - evolução temporal, se aplicável.
- Implementar Machine Learning:
  - KNN.
  - Árvore de Decisão.
  - Random Forest.
  - Logistic Regression.
  - Regressão Linear.
- Avaliar modelos.
- Comparar resultados.
- Apresentar 3 a 5 insights de negócio.
- Fazer slides e apresentar em 10 a 15 minutos.

## 2. Baixar E Conferir O Dataset

Dataset escolhido:

- Coffee Shop Sales.
- Fonte: Maven Analytics / Kaggle.
- Arquivo principal: `Coffee Shop Sales.xlsx`.

O que conferir manualmente:

- O arquivo abre corretamente no Excel.
- Existem `149.116` registros.
- Existem `11` colunas originais.
- O período dos dados vai de `01/01/2023` a `30/06/2023`.
- Existem 3 lojas:
  - Astoria.
  - Hell's Kitchen.
  - Lower Manhattan.
- Existem variáveis numéricas:
  - `transaction_id`
  - `transaction_qty`
  - `store_id`
  - `product_id`
  - `unit_price`
- Existem variáveis categóricas:
  - `store_location`
  - `product_category`
  - `product_type`
  - `product_detail`
- Existem variáveis temporais:
  - `transaction_date`
  - `transaction_time`

Conclusão que vocês devem saber explicar:

> O dataset atende ao requisito mínimo porque possui mais de 10.000 registros, contém variáveis numéricas, categóricas e temporais, e permite análises por loja, produto e tempo.

## 3. Definir A Pergunta De Negócio

Pergunta central do projeto:

> Quais fatores explicam maior receita e maior demanda por loja, produto, mês, dia da semana e horário?

Essa pergunta guia todas as próximas etapas:

- O Data Warehouse organiza os dados.
- As views respondem perguntas analíticas.
- A EDA mostra padrões.
- O Machine Learning prevê demanda.
- Os insights viram decisões de negócio.

## 4. Planejar A Modelagem Dimensional

Usem star schema.

### Tabela Fato

Criar a tabela:

`fato_vendas`

Grão da fato:

> Uma linha por item vendido em uma transação.

Campos principais:

- `venda_key`
- `transacao_id`
- `tempo_key`
- `loja_key`
- `produto_key`
- `quantidade`
- `preco_unitario`
- `receita`

Medidas:

- quantidade vendida.
- preço unitário.
- receita.

Fórmula:

```text
receita = transaction_qty * unit_price
```

Dimensão degenerada:

- `transacao_id`

Explicação:

> O `transacao_id` é uma dimensão degenerada porque identifica a transação, mas não precisa de uma tabela dimensão separada.

### Dimensão Tempo

Criar:

`dim_tempo`

Campos sugeridos:

- `tempo_key`
- data
- hora
- ano
- mês
- nome do mês
- trimestre
- dia do mês
- dia da semana
- fim de semana
- período do dia

Essa dimensão permite analisar vendas por:

- mês.
- dia da semana.
- hora.
- manhã, tarde ou noite.

### Dimensão Loja

Criar:

`dim_loja`

Campos sugeridos:

- `loja_key`
- localização.
- cidade.
- país.
- rede.
- tipo de loja.

Exemplo:

- Hell's Kitchen.
- Astoria.
- Lower Manhattan.

### Dimensão Produto

Criar:

`dim_produto`

Campos sugeridos:

- `produto_key`
- categoria.
- tipo do produto.
- detalhe do produto.
- preço médio.
- preço mínimo.
- preço máximo.
- faixa de preço.

Essa dimensão permite comparar:

- Coffee.
- Tea.
- Bakery.
- Drinking Chocolate.
- outras categorias.

## 5. Preparar Os Dados Para O DW

Vocês podem fazer isso no Python, Excel ou manualmente com apoio de fórmulas, mas precisam entender a lógica.

Para fazer especificamente no Excel, use o arquivo:

```text
docs/guia_excel_preparacao_dados.md
```

Ele mostra as letras das colunas, as fórmulas de `receita`, `hora`, `tempo_key`, os atributos de tempo e como montar `dim_tempo`, `dim_loja`, `dim_produto` e `fato_vendas`.

Etapas:

1. Abrir o dataset original.
2. Criar a coluna `receita`.
3. Extrair data e hora.
4. Criar uma chave de tempo combinando data e hora.
5. Separar dados únicos para a dimensão tempo.
6. Separar dados únicos para a dimensão loja.
7. Separar dados únicos para a dimensão produto.
8. Criar a fato com as chaves e medidas.
9. Conferir se a fato tem `149.116` linhas.
10. Conferir se nenhuma dimensão ficou vazia.

Checklist:

- `dim_tempo` criada.
- `dim_loja` criada.
- `dim_produto` criada.
- `fato_vendas` criada.
- Receita calculada corretamente.
- A fato tem a mesma quantidade de linhas do dataset original.

## 6. Criar O Banco No PostgreSQL

Nome sugerido do banco:

`coffee_shop_dw`

Passos manuais:

1. Abrir o PostgreSQL ou pgAdmin.
2. Criar o banco `coffee_shop_dw`.
3. Criar um schema chamado `coffee_dw`.
4. Criar as dimensões.
5. Criar a tabela fato.
6. Criar chaves primárias.
7. Criar chaves estrangeiras da fato para as dimensões.
8. Criar índices nas chaves da fato.
9. Inserir/carregar os dados.
10. Rodar consultas de conferência.

Ordem correta:

1. Criar banco.
2. Criar schema.
3. Criar dimensões.
4. Criar fato.
5. Carregar dimensões.
6. Carregar fato.
7. Criar views.
8. Rodar validações.

## 7. Criar Views Analíticas

O professor pediu 2 views. Façam pelo menos estas duas.

### View 1: Receita Mensal Por Loja E Categoria

Objetivo:

> Ver quanto cada loja e categoria venderam por mês.

Campos:

- ano.
- mês.
- nome do mês.
- loja.
- categoria.
- quantidade vendida.
- receita total.
- preço médio.
- número de transações.

Perguntas que essa view responde:

- Qual loja vende mais?
- Qual categoria gera mais receita?
- Em qual mês a receita foi maior?
- Existe diferença entre lojas?

### View 2: Demanda Por Hora E Produto

Objetivo:

> Entender quando a demanda acontece e quais produtos/categorias vendem em cada horário.

Campos:

- dia da semana.
- hora.
- período do dia.
- loja.
- categoria.
- tipo de produto.
- quantidade vendida.
- receita total.
- número de transações.

Perguntas que essa view responde:

- Qual horário tem maior movimento?
- Existe pico de vendas pela manhã?
- Cada loja tem comportamento diferente?
- Quais produtos precisam de mais estoque em horários específicos?

### View Extra Recomendada

Criar uma terceira view:

`vw_ranking_produtos`

Objetivo:

> Listar os produtos com maior receita e maior quantidade vendida.

Isso ajuda muito nos insights e slides.

## 8. Validar O SQL

Rodar consultas para conferir:

- Quantidade de linhas da fato.
- Quantidade de linhas das dimensões.
- Se a receita foi calculada corretamente.
- Se as views retornam dados.
- Se não existem chaves sem correspondência.

Validações importantes:

```text
fato_vendas deve ter 149.116 linhas
receita deve ser igual a quantidade * preco_unitario
dim_loja deve ter 3 lojas
dim_produto deve ter 80 produtos
as views devem retornar resultados
```

## 9. Fazer A Análise Exploratória Em Python

Abrir o notebook e organizar a análise nesta ordem:

1. Importar bibliotecas.
2. Carregar o dataset.
3. Mostrar primeiras linhas.
4. Ver dimensões do dataset.
5. Ver tipos das colunas.
6. Ver dados nulos.
7. Criar coluna de receita.
8. Criar colunas de mês, dia da semana e hora.
9. Calcular métricas gerais.
10. Criar gráficos.

Métricas que precisam aparecer:

- total de registros.
- total de receita.
- total de itens vendidos.
- número de lojas.
- número de produtos.
- número de categorias.
- loja com maior receita.
- categoria com maior receita.
- produto com maior receita.
- horário de pico.

## 10. Criar Os Gráficos Obrigatórios

### Distribuição

Fazer pelo menos um:

- distribuição da quantidade por transação.
- distribuição do preço unitário.
- distribuição da receita por transação.
- distribuição por horário.

Melhor opção:

> Distribuição da quantidade por transação.

Por quê:

> Mostra que a maioria das vendas tem poucos itens, o que é comum em cafeterias.

### Comparação Entre Categorias

Fazer pelo menos um:

- receita por categoria.
- quantidade vendida por categoria.
- receita por loja.
- receita por tipo de produto.

Melhores opções:

- receita por loja.
- receita por categoria.

### Evolução Temporal

Fazer:

- receita mensal de janeiro a junho.

Explicação:

> Esse gráfico mostra se a receita cresce, cai ou varia ao longo do tempo.

### Gráfico Extra Recomendado

Fazer:

- demanda por hora e loja.

Por quê:

> Esse gráfico gera um insight visual forte sobre o pico de movimento.

## 11. Preparar A Base De Machine Learning

Não use cada transação individual como alvo principal. Para ficar mais coerente, agregue os dados.

Agrupar por:

- data.
- hora.
- loja.
- categoria.
- tipo de produto.

Criar colunas:

- `quantidade_vendida`
- `receita`
- `preco_medio`
- `transacoes`
- `mes`
- `dia_mes`
- `dia_semana`
- `fim_de_semana`

## 12. Definir Os Problemas De ML

### Classificação

Objetivo:

> Prever se uma combinação de loja, produto, dia e horário terá alta demanda.

Criar a variável:

`alta_demanda`

Regra:

> Alta demanda = quantidade vendida acima ou igual ao quartil 75.

Modelos obrigatórios:

- KNN.
- Árvore de Decisão.
- Random Forest.
- Logistic Regression.

Métricas obrigatórias:

- acurácia.
- precision.
- recall.
- F1-score.
- matriz de confusão.

### Regressão

Objetivo:

> Prever a quantidade vendida.

Modelo obrigatório:

- Regressão Linear.

Métricas recomendadas:

- MAE.
- RMSE.
- R².

## 13. Treinar Os Modelos

Passos:

1. Separar variáveis preditoras.
2. Separar variável alvo.
3. Fazer one-hot encoding nas variáveis categóricas.
4. Padronizar variáveis numéricas quando necessário.
5. Separar treino e teste.
6. Treinar KNN.
7. Treinar Árvore de Decisão.
8. Treinar Random Forest.
9. Treinar Logistic Regression.
10. Treinar Regressão Linear.
11. Gerar métricas.
12. Comparar resultados.

Variáveis preditoras sugeridas:

- hora.
- preço médio.
- mês.
- dia do mês.
- dia da semana.
- fim de semana.
- loja.
- categoria.
- tipo de produto.

## 14. Comparar Os Modelos

Resultado encontrado no projeto:

| Modelo | Accuracy | Precision | Recall | F1 |
|---|---:|---:|---:|---:|
| KNN | 0.7245 | 0.5722 | 0.4987 | 0.5329 |
| Árvore de Decisão | 0.8233 | 0.7284 | 0.7007 | 0.7143 |
| Random Forest | 0.8098 | 0.7652 | 0.5722 | 0.6548 |
| Logistic Regression | 0.7303 | 0.6057 | 0.4135 | 0.4915 |

Conclusão:

> A Árvore de Decisão teve melhor F1-score, então foi o melhor modelo de classificação neste recorte.

Explicação:

> A demanda da cafeteria depende de combinações de horário, loja e produto. A Árvore de Decisão consegue capturar regras não lineares melhor que a regressão logística.

Resultado da Regressão Linear:

- MAE: `1.6091`
- RMSE: `2.2356`
- R²: `0.2464`

Conclusão:

> A Regressão Linear teve desempenho limitado porque a demanda não é totalmente linear e faltam variáveis importantes como clima, feriados, promoções e dados de clientes.

## 15. Tirar Insights De Negócio

Escolham 3 a 5 insights. Sugestão:

### Insight 1

Hell's Kitchen lidera em receita.

Decisão:

> Priorizar estoque, equipe e disponibilidade dos produtos mais vendidos nessa loja.

### Insight 2

O pico de demanda ocorre às 10h.

Decisão:

> Reforçar equipe e pré-preparo no período da manhã.

### Insight 3

Coffee é a categoria com maior receita.

Decisão:

> Tratar Coffee como categoria âncora do mix.

### Insight 4

Barista Espresso lidera em receita.

Decisão:

> Usar esse produto em combos premium ou destaques comerciais.

### Insight 5

Brewed Chai tea lidera em quantidade vendida.

Decisão:

> Usar produtos de alto giro para atrair clientes e vender itens complementares.

## 16. Montar Os Slides

Ordem recomendada dos slides:

1. Capa.
2. Objetivo e pergunta de negócio.
3. Dataset e validação dos requisitos.
4. Modelagem dimensional.
5. Implementação SQL e views.
6. Análise exploratória.
7. Principais gráficos.
8. Machine Learning.
9. Comparação dos modelos.
10. Insights e recomendações.
11. Conclusão.

Se precisarem ficar em 10 slides, juntem objetivo com capa ou EDA com gráficos.

## 17. Divisão Da Apresentação Para 2 Pessoas

### Pessoa 1

Falar sobre:

- objetivo do projeto.
- dataset.
- requisitos atendidos.
- modelagem dimensional.
- PostgreSQL.
- tabela fato, dimensões e views.

Tempo sugerido:

5 a 7 minutos.

### Pessoa 2

Falar sobre:

- análise exploratória.
- gráficos.
- Machine Learning.
- comparação dos modelos.
- insights.
- recomendações finais.

Tempo sugerido:

5 a 7 minutos.

### Ambos

Participar:

- da abertura.
- da conclusão.
- das perguntas do professor.

## 18. Fala Sugerida Para Abertura

> Nosso projeto constrói uma solução completa de dados para vendas de uma cafeteria. A partir de um dataset público com mais de 149 mil registros, criamos um Data Warehouse em PostgreSQL, fizemos análises exploratórias em Python, aplicamos modelos de Machine Learning e extraímos insights para apoiar decisões de estoque, equipe e mix de produtos.

## 19. Fala Sugerida Para Modelagem

> A modelagem escolhida foi star schema. Criamos uma tabela fato chamada fato_vendas, no grão de uma venda por item de transação, e três dimensões principais: tempo, loja e produto. Também usamos o transaction_id como dimensão degenerada, porque ele identifica a transação, mas não exige uma tabela dimensão própria.

## 20. Fala Sugerida Para Machine Learning

> Para o Machine Learning, transformamos o problema em previsão de demanda. Criamos uma base agregada por data, hora, loja e produto. Para classificação, criamos a variável alta_demanda usando o quartil 75 da quantidade vendida. Testamos KNN, Árvore de Decisão, Random Forest e Regressão Logística. Também usamos Regressão Linear para prever quantidade vendida.

## 21. Fala Sugerida Para Comparação Dos Modelos

> O melhor modelo de classificação foi a Árvore de Decisão, com maior F1-score. Isso faz sentido porque a demanda depende de regras combinadas, como loja, horário e tipo de produto. A Regressão Linear teve desempenho mais limitado, mostrando que a demanda provavelmente depende de relações não lineares e de variáveis que não estão no dataset, como clima, feriados e promoções.

## 22. Fala Sugerida Para Insights

> Os principais insights foram: Hell's Kitchen lidera a receita, o pico de demanda acontece às 10h, Coffee é a principal categoria por receita, Barista Espresso lidera em receita e Brewed Chai tea lidera em volume. Com isso, recomendamos reforço de estoque e equipe pela manhã, foco nos produtos líderes e promoções em horários de menor movimento.

## 23. Checklist Final Antes De Entregar

Confirmem:

- O dataset está na pasta do projeto.
- O notebook abre e roda.
- Os scripts SQL estão organizados.
- O banco foi criado no PostgreSQL.
- As tabelas foram carregadas.
- As views funcionam.
- Os gráficos aparecem no notebook.
- Todos os modelos obrigatórios foram treinados.
- As métricas obrigatórias aparecem.
- A matriz de confusão aparece.
- Existe comparação dos modelos.
- Existem 3 a 5 insights.
- Os slides estão prontos.
- Os dois integrantes sabem explicar sua parte.
- A apresentação cabe em 10 a 15 minutos.

## 24. Ordem De Trabalho Recomendada

Dia 1:

- Baixar dataset.
- Entender colunas.
- Validar requisitos.
- Definir pergunta de negócio.

Dia 2:

- Fazer modelagem dimensional.
- Desenhar star schema.
- Criar tabelas no PostgreSQL.

Dia 3:

- Preparar dados.
- Carregar dimensões e fato.
- Criar views.
- Validar SQL.

Dia 4:

- Fazer EDA no notebook.
- Criar gráficos.
- Separar principais métricas.

Dia 5:

- Preparar base de ML.
- Treinar modelos.
- Avaliar métricas.
- Comparar modelos.

Dia 6:

- Escrever insights.
- Montar slides.
- Criar fala de cada pessoa.

Dia 7:

- Ensaiar.
- Ajustar tempo.
- Revisar notebook, SQL e slides.

## 25. O Que Não Pode Faltar Na Apresentação

- Mostrar que o dataset atende aos requisitos.
- Mostrar o star schema.
- Explicar a dimensão degenerada.
- Mostrar pelo menos duas views.
- Mostrar gráficos de EDA.
- Mostrar todos os modelos obrigatórios.
- Mostrar as métricas de classificação.
- Mostrar a regressão linear.
- Responder qual modelo foi melhor e por quê.
- Apresentar insights e decisões de negócio.

## 26. Conclusão Final Do Projeto

Conclusão recomendada:

> O projeto mostrou como transformar dados transacionais em uma solução analítica completa. O Data Warehouse organizou as vendas por tempo, loja e produto; a análise exploratória revelou padrões de receita e demanda; e o Machine Learning permitiu comparar modelos para previsão de alta demanda. Os resultados podem apoiar decisões práticas de estoque, equipe, promoções e mix de produtos.
