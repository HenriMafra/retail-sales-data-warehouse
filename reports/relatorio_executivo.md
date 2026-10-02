# Relatório Executivo: Coffee Shop Sales

## Resumo

Este projeto constrói uma solução completa de dados para a Maven Roasters, uma cafeteria fictícia com três lojas em Nova York. A solução inclui Data Warehouse em PostgreSQL, análise exploratória em Python, modelos de Machine Learning e recomendações de negócio.

O dataset possui `149.116` registros, `11` colunas e cobre o período de `2023-01-01` a `2023-06-30`.

## Principais Métricas

- Receita total: `$698,812.33`
- Itens vendidos: `214.470`
- Lojas: `3`
- Produtos: `80`
- Categorias: `9`
- Loja líder em receita: `Hell's Kitchen`
- Categoria líder em receita: `Coffee`
- Produto líder em receita: `Barista Espresso`
- Produto líder em quantidade: `Brewed Chai tea`
- Pico de demanda: `10h`

## Data Warehouse

A modelagem usa star schema, com uma tabela fato e três dimensões:

- `fato_vendas`
- `dim_tempo`
- `dim_loja`
- `dim_produto`

O identificador `transacao_id` foi mantido na fato como dimensão degenerada, atendendo ao requisito de modelagem dimensional.

## Machine Learning

A modelagem de ML foi orientada para demanda:

- Classificação: prever alta demanda.
- Regressão: prever quantidade vendida.

Resultado da classificação:

| Modelo | Accuracy | Precision | Recall | F1 |
|---|---:|---:|---:|---:|
| KNN | 0.7245 | 0.5722 | 0.4987 | 0.5329 |
| Árvore de Decisão | 0.8233 | 0.7284 | 0.7007 | 0.7143 |
| Random Forest | 0.8098 | 0.7652 | 0.5722 | 0.6548 |
| Logistic Regression | 0.7303 | 0.6057 | 0.4135 | 0.4915 |

A Árvore de Decisão teve melhor F1-score. Isso indica que regras de horário, produto, categoria e loja ajudam a separar situações de demanda normal e alta demanda.

Resultado da regressão:

- Modelo: Regressão Linear
- Target: `quantidade_vendida`
- MAE: `1.6091`
- RMSE: `2.2356`
- R²: `0.2464`

O R² baixo mostra que a demanda depende de relações não lineares e de variáveis ausentes, como clima, feriados, promoções e perfil de clientes.

## Insights De Negócio

1. **Hell's Kitchen lidera em receita.** A loja deve receber prioridade em planejamento de estoque, escala de funcionários e disponibilidade dos produtos mais vendidos.
2. **O pico de demanda ocorre às 10h.** O período da manhã deve concentrar reforço operacional e pré-preparo de itens de maior saída.
3. **Coffee é a principal categoria por receita.** A categoria deve ser tratada como âncora comercial do mix.
4. **Barista Espresso lidera em receita.** O produto tem forte contribuição financeira e pode ser destaque em combos premium.
5. **Brewed Chai tea lidera em volume.** Produtos de alto giro podem atrair tráfego e sustentar estratégias de venda cruzada.

## Recomendações

- Ajustar estoque e equipe para o pico da manhã.
- Criar promoções em horários de menor movimento.
- Manter Coffee e Tea como categorias centrais.
- Usar produtos de alto volume para combos.
- Enriquecer análises futuras com clima, feriados, campanhas e dados de cliente.
