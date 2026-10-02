# Guia Excel: Preparacao Dos Dados

Este guia explica exatamente como criar, no Excel, as colunas derivadas usadas no projeto.

Use este arquivo quando forem preparar os CSVs manualmente.

## 1. Antes De Comecar

Abra o arquivo:

```text
data/raw/Coffee Shop Sales.xlsx
```

A aba original do arquivo se chama:

```text
Transactions
```

Se no seu Excel a aba aparecer com outro nome, use o nome que aparece ai nas formulas.

A planilha original vem com estas colunas:

| Letra | Coluna original |
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

Nao altere os nomes dessas colunas originais.

Crie as novas colunas a partir da coluna `L`.

## 2. Colunas Derivadas Na Planilha Original

Na linha 1, crie estes cabecalhos:

| Letra | Novo cabecalho | Para que serve |
|---|---|---|
| L | `receita` | medida da tabela fato |
| M | `hora` | atributo da dimensao tempo |
| N | `tempo_key` | chave da dimensao tempo |
| O | `ano` | atributo da dimensao tempo |
| P | `mes` | atributo da dimensao tempo |
| Q | `nome_mes` | atributo da dimensao tempo |
| R | `trimestre` | atributo da dimensao tempo |
| S | `dia_mes` | atributo da dimensao tempo |
| T | `dia_semana_num` | atributo da dimensao tempo |
| U | `nome_dia_semana` | atributo da dimensao tempo |
| V | `fim_de_semana` | atributo da dimensao tempo |
| W | `periodo_dia` | atributo da dimensao tempo |

## 3. Formula Da Receita

Na celula `L2`, digite:

```excel
=D2*H2
```

Depois arraste ate a ultima linha.

Explicacao:

```text
receita = transaction_qty * unit_price
```

Exemplo:

```text
2 itens * 3,00 = 6,00
```

Conferencia:

- A coluna `receita` deve ter valores numericos.
- Nao deve ficar vazia.
- Nao deve ter texto.

## 4. Formula Da Hora

Na celula `M2`, digite:

```excel
=HORA(C2)
```

Se seu Excel estiver em ingles, use:

```excel
=HOUR(C2)
```

Depois arraste ate a ultima linha.

Resultado esperado:

```text
07:06:11 -> 7
10:30:15 -> 10
20:18:00 -> 20
```

Conferencia:

- A coluna `hora` deve ir de `6` a `20` neste dataset.
- Se aparecer erro, a coluna `transaction_time` pode estar como texto. Nesse caso, tente:

```excel
=HORA(VALOR(C2))
```

Em ingles:

```excel
=HOUR(TIMEVALUE(C2))
```

## 5. Formula Da Chave De Tempo

A chave de tempo junta data e hora.

Formato:

```text
YYYYMMDDHH
```

Exemplo:

```text
2023-01-01 07h -> 2023010107
```

Na celula `N2`, digite:

```excel
=VALOR(TEXTO(B2;"aaaammdd")&TEXTO(M2;"00"))
```

Se seu Excel estiver em ingles, use:

```excel
=VALUE(TEXT(B2,"yyyymmdd")&TEXT(M2,"00"))
```

Depois arraste ate a ultima linha.

Observacao importante:

- Em alguns Excels em portugues, o formato de ano usa `aaaa`.
- Em alguns Excels em ingles, usa `yyyy`.
- Se `aaaammdd` nao funcionar, teste `yyyymmdd`.

Conferencia:

- A chave deve ter 10 digitos.
- Exemplo correto: `2023010107`.
- Nao pode ficar como `2023117`.

## 6. Formulas Dos Atributos De Tempo

Use estas formulas na linha 2 e arraste ate o fim.

### Ano

Celula `O2`:

```excel
=ANO(B2)
```

Ingles:

```excel
=YEAR(B2)
```

### Mes

Celula `P2`:

```excel
=MÊS(B2)
```

Ingles:

```excel
=MONTH(B2)
```

### Nome Do Mes

Celula `Q2`:

```excel
=TEXTO(B2;"mmmm")
```

Ingles:

```excel
=TEXT(B2,"mmmm")
```

### Trimestre

Celula `R2`:

```excel
=ARREDONDAR.PARA.CIMA(MÊS(B2)/3;0)
```

Ingles:

```excel
=ROUNDUP(MONTH(B2)/3,0)
```

### Dia Do Mes

Celula `S2`:

```excel
=DIA(B2)
```

Ingles:

```excel
=DAY(B2)
```

### Numero Do Dia Da Semana

Celula `T2`:

```excel
=DIA.DA.SEMANA(B2;2)
```

Ingles:

```excel
=WEEKDAY(B2,2)
```

Explicacao:

```text
1 = segunda-feira
2 = terca-feira
3 = quarta-feira
4 = quinta-feira
5 = sexta-feira
6 = sabado
7 = domingo
```

### Nome Do Dia Da Semana

Celula `U2`:

```excel
=TEXTO(B2;"dddd")
```

Ingles:

```excel
=TEXT(B2,"dddd")
```

### Fim De Semana

Celula `V2`:

```excel
=SE(T2>=6;"true";"false")
```

Ingles:

```excel
=IF(T2>=6,"true","false")
```

Importante:

- Use texto `true` e `false`, nao `VERDADEIRO` e `FALSO`.
- Isso evita problema na carga do PostgreSQL, porque a coluna `fim_de_semana` e booleana.

### Periodo Do Dia

Celula `W2`:

```excel
=SE(M2<=10;"Manha";SE(M2<=14;"Almoco";SE(M2<=18;"Tarde";"Noite")))
```

Ingles:

```excel
=IF(M2<=10,"Manha",IF(M2<=14,"Almoco",IF(M2<=18,"Tarde","Noite")))
```

Regra usada:

| Hora | Periodo |
|---:|---|
| 0 a 10 | `Manha` |
| 11 a 14 | `Almoco` |
| 15 a 18 | `Tarde` |
| 19 a 23 | `Noite` |

## 7. Como Criar A `dim_tempo` No Excel

Crie uma nova aba chamada:

```text
dim_tempo
```

Copie da aba original estas colunas, nesta ordem:

| Coluna na `dim_tempo` | Vem da coluna original |
|---|---|
| `tempo_key` | N |
| `data` | B |
| `hora` | M |
| `ano` | O |
| `mes` | P |
| `nome_mes` | Q |
| `trimestre` | R |
| `dia_mes` | S |
| `dia_semana_num` | T |
| `nome_dia_semana` | U |
| `fim_de_semana` | V |
| `periodo_dia` | W |

Depois:

1. Selecione toda a tabela da aba `dim_tempo`.
2. Va em **Dados > Remover Duplicatas**.
3. Marque apenas `tempo_key` como criterio.
4. Confirme.
5. Ordene por `data` e depois por `hora`.

Resultado esperado:

```text
dim_tempo = 2512 linhas
```

Exportar como:

```text
data/processed/dim_tempo.csv
```

## 8. Como Criar A `dim_loja` No Excel

Crie uma nova aba chamada:

```text
dim_loja
```

Copie estas colunas:

| Coluna na `dim_loja` | Vem da coluna original |
|---|---|
| `loja_key` | E `store_id` |
| `localizacao` | F `store_location` |

Depois:

1. Remova duplicatas usando `loja_key`.
2. Crie a coluna `cidade` com o valor:

```text
New York
```

3. Crie a coluna `pais` com o valor:

```text
Estados Unidos
```

4. Crie a coluna `rede` com o valor:

```text
Maven Roasters
```

5. Crie a coluna `tipo_loja` com o valor:

```text
Cafeteria
```

Resultado esperado:

```text
dim_loja = 3 linhas
```

Exportar como:

```text
data/processed/dim_loja.csv
```

## 9. Como Criar A `dim_produto` No Excel

Crie uma nova aba chamada:

```text
dim_produto
```

Copie estas colunas:

| Coluna na `dim_produto` | Vem da coluna original |
|---|---|
| `produto_key` | G `product_id` |
| `categoria` | I `product_category` |
| `tipo_produto` | J `product_type` |
| `detalhe_produto` | K `product_detail` |

Depois:

1. Remova duplicatas usando `produto_key`.
2. Crie `preco_medio`.
3. Crie `preco_minimo`.
4. Crie `preco_maximo`.
5. Crie `faixa_preco`.

Supondo que `produto_key` esteja em `A2` na aba `dim_produto`, use:

### Preco Medio

```excel
=ARRED(MÉDIASE(Transactions!$G:$G;A2;Transactions!$H:$H);2)
```

Ingles:

```excel
=ROUND(AVERAGEIF(Transactions!$G:$G,A2,Transactions!$H:$H),2)
```

### Preco Minimo

```excel
=ARRED(MÍNIMOSES(Transactions!$H:$H;Transactions!$G:$G;A2);2)
```

Ingles:

```excel
=ROUND(MINIFS(Transactions!$H:$H,Transactions!$G:$G,A2),2)
```

### Preco Maximo

```excel
=ARRED(MÁXIMOSES(Transactions!$H:$H;Transactions!$G:$G;A2);2)
```

Ingles:

```excel
=ROUND(MAXIFS(Transactions!$H:$H,Transactions!$G:$G,A2),2)
```

### Faixa De Preco

Supondo que `preco_medio` esteja em `E2`:

```excel
=SE(E2<3;"Baixo";SE(E2<5;"Medio";"Alto"))
```

Ingles:

```excel
=IF(E2<3,"Baixo",IF(E2<5,"Medio","Alto"))
```

Resultado esperado:

```text
dim_produto = 80 linhas
```

Exportar como:

```text
data/processed/dim_produto.csv
```

## 10. Como Criar A `fato_vendas` No Excel

Crie uma nova aba chamada:

```text
fato_vendas
```

Crie estas colunas, exatamente nesta ordem:

| Coluna na fato | Vem de onde |
|---|---|
| `venda_key` | numero sequencial |
| `transacao_id` | A `transaction_id` |
| `tempo_key` | N `tempo_key` |
| `loja_key` | E `store_id` |
| `produto_key` | G `product_id` |
| `quantidade` | D `transaction_qty` |
| `preco_unitario` | H `unit_price` |
| `receita` | L `receita` |

### Criar `venda_key`

Na celula `A2` da aba `fato_vendas`, use:

```excel
=LIN()-1
```

Ingles:

```excel
=ROW()-1
```

Depois arraste ate a ultima linha.

Resultado:

```text
1
2
3
...
149116
```

Resultado esperado:

```text
fato_vendas = 149116 linhas
```

Exportar como:

```text
data/processed/fato_vendas.csv
```

## 11. Exportacao Correta Dos CSVs

Cada aba deve ser salva como CSV UTF-8.

Arquivos esperados:

```text
data/processed/dim_tempo.csv
data/processed/dim_loja.csv
data/processed/dim_produto.csv
data/processed/fato_vendas.csv
```

Atencao:

- Mantenha os nomes das colunas exatamente iguais aos nomes usados no SQL.
- Mantenha a ordem das colunas exatamente como descrita.
- Nao deixe linhas em branco no final.
- Nao use separador `;` se o PostgreSQL estiver esperando CSV com virgula.
- Se o Excel salvar com `;`, ajuste o comando de carga ou exporte novamente como CSV com virgula.

## 12. Conferencias Finais No Excel

Antes de ir para o PostgreSQL, confira:

```text
dim_tempo: 2512 linhas
dim_loja: 3 linhas
dim_produto: 80 linhas
fato_vendas: 149116 linhas
```

Confira tambem:

```text
receita = quantidade * preco_unitario
tempo_key tem 10 digitos
fim_de_semana esta como true/false
venda_key vai de 1 ate 149116
```

## 13. O Que Falar Para O Professor

> As colunas receita, hora e tempo_key foram criadas como variaveis derivadas. A receita e uma medida da fato, calculada pela quantidade vezes o preco unitario. A hora e os demais atributos temporais alimentam a dimensao tempo. A chave tempo_key conecta a fato com a dimensao tempo no star schema.
