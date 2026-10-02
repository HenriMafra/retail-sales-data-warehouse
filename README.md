# ☕ Retail Sales Data Warehouse — Modelagem Dimensional de Kimball & Previsão de Demanda com ML

Projeto completo de Engenharia de Dados e Machine Learning demonstrando a construção de um **Data Warehouse corporativo de ponta a ponta**, aplicando a metodologia de **Modelagem Dimensional de Ralph Kimball (Star Schema)**, pipelines de extração, transformação e carga (ETL) em Python, e modelos preditivos supervisionados para **previsão de faturamento e demanda de varejo**.

---

## 📌 Que Problema Resolve?

Bancos de dados relacionais transacionais (OLTP) são projetados para escrita rápida e integridade referencial, mas se tornam extremamente lentos e ineficientes para responder perguntas analíticas complexas de negócio, como:
- *"Qual é a sazonalidade de vendas por categoria de produto nos fins de semana?"*
- *"Qual loja tem maior ticket médio por hora do dia?"*
- *"Qual é a projeção de receita para o próximo mês?"*

O **Retail Sales Data Warehouse** resolve isso estruturando os dados em um modelo analítico (OLAP) otimizado para consultas analíticas de alta performance e municiando modelos de Machine Learning para suporte à decisão gerencial.

---

## ⚙️ Diferencial Técnico & Arquitetura

### 1. Modelagem Dimensional (Star Schema)
- **Tabela Fato (`fact_sales`):** Registra métricas aditivas de cada transação (quantidade vendida, valor unitário, desconto aplicado, receita líquida, custo do produto e margem bruta).
- **Tabelas Dimensão:**
  - `dim_date`: Chaves temporais hierárquicas (data, dia da semana, fim de semana, mês, trimestre, ano).
  - `dim_time`: Faixas horárias de pico (manhã, almoço, tarde, noite).
  - `dim_product`: Categoria de produto, tipo de grão/embalagem e custo base.
  - `dim_store`: Localização da filial, metragem e perfil de público.

### 2. Pipeline ETL em Python
- **Extract:** Ingestão de fontes heterogêneas (CSV, JSON, APIs de PDV).
- **Transform:** Limpeza de dados nulos, conversão estrita de tipos, normalização monetária e geração de chaves substitutas (Surrogate Keys - SK).
- **Load:** Carga atômica em banco relacional de staging e tabelas analíticas finais.

### 3. Modelagem Preditiva de Receita
- Engenharia de features temporais (lags de 7 e 30 dias, médias móveis e sazonalidade de feriados).
- Treinamento e validação cruzada com métricas de erro (`RMSE`, `MAE` e `R²`).

---

## 🏗️ Stack Tecnológica

- **Linguagem:** Python 3.10+
- **Manipulação de Dados:** `pandas`, `numpy`
- **Banco de Dados & SQL:** PostgreSQL / SQLite com DDLs analíticos
- **Machine Learning & EDA:** `scikit-learn`, `statsmodels`, `seaborn`, `matplotlib`

---

## 🚀 Como Executar Localmente

```bash
# 1. Clone o repositório
git clone https://github.com/HenriMafra/retail-sales-data-warehouse.git
cd retail-sales-data-warehouse

# 2. Crie e ative o ambiente virtual
python -m venv venv
source venv/bin/activate  # No Windows: .\venv\Scripts\activate

# 3. Instale as dependências
pip install -r requirements.txt

# 4. Execute o pipeline de ETL
python src/etl_pipeline.py

# 5. Execute o treinamento do modelo de ML
python src/train_forecasting_model.py
```

---

## 📄 Licença

Distribuído sob a licença **MIT**. Desenvolvido por **Henri Mafra**.
