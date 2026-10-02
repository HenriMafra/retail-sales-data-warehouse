from __future__ import annotations

from pathlib import Path
from textwrap import dedent

import nbformat as nbf


ROOT = Path(__file__).resolve().parents[1]
NOTEBOOK_PATH = ROOT / "notebooks" / "coffee_shop_dw_ml.ipynb"


def md(text: str):
    return nbf.v4.new_markdown_cell(dedent(text).strip())


def code(text: str):
    return nbf.v4.new_code_cell(dedent(text).strip())


def build() -> None:
    nb = nbf.v4.new_notebook()
    nb["metadata"] = {
        "kernelspec": {
            "display_name": "Python 3",
            "language": "python",
            "name": "python3",
        },
        "language_info": {"name": "python", "pygments_lexer": "ipython3"},
    }

    nb["cells"] = [
        md(
            """
            # Projeto Pratico Final: Coffee Shop Sales

            **Disciplina:** Desenvolvimento para Ciencia de Dados II  
            **Tema:** Data Warehouse + Machine Learning aplicado a vendas de cafeteria  
            **Dataset:** Coffee Shop Sales, Maven Analytics / Kaggle  

            Pergunta central: quais fatores explicam maior receita e maior demanda por loja, produto, mes, dia da semana e horario?
            """
        ),
        md(
            """
            ## 1. Preparacao do ambiente

            A primeira celula instala bibliotecas ausentes quando o notebook for executado em outro computador.
            """
        ),
        code(
            """
            import importlib.util
            import subprocess
            import sys

            required = {
                "pandas": "pandas",
                "numpy": "numpy",
                "matplotlib": "matplotlib",
                "seaborn": "seaborn",
                "sklearn": "scikit-learn",
                "openpyxl": "openpyxl",
            }

            missing = [pkg for module, pkg in required.items() if importlib.util.find_spec(module) is None]
            if missing:
                subprocess.check_call([sys.executable, "-m", "pip", "install", *missing])
            """
        ),
        code(
            """
            from pathlib import Path

            import matplotlib.pyplot as plt
            import numpy as np
            import pandas as pd
            import seaborn as sns
            from sklearn.compose import ColumnTransformer
            from sklearn.ensemble import RandomForestClassifier
            from sklearn.linear_model import LinearRegression, LogisticRegression
            from sklearn.metrics import (
                ConfusionMatrixDisplay,
                accuracy_score,
                f1_score,
                mean_absolute_error,
                mean_squared_error,
                precision_score,
                r2_score,
                recall_score,
            )
            from sklearn.model_selection import train_test_split
            from sklearn.neighbors import KNeighborsClassifier
            from sklearn.pipeline import Pipeline
            from sklearn.preprocessing import OneHotEncoder, StandardScaler
            from sklearn.tree import DecisionTreeClassifier

            sns.set_theme(style="whitegrid", palette="Set2")
            PROJECT_ROOT = Path.cwd().parent if Path.cwd().name == "notebooks" else Path.cwd()
            RAW_PATH = PROJECT_ROOT / "data" / "raw" / "Coffee Shop Sales.xlsx"
            PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"
            RAW_PATH
            """
        ),
        md(
            """
            ## 2. Carregamento e validacao do dataset

            O projeto exige no minimo 10.000 registros, variaveis numericas e variaveis categoricas. O dataset atende com folga.
            """
        ),
        code(
            """
            df = pd.read_excel(RAW_PATH)
            print(f"Linhas: {df.shape[0]:,}".replace(",", "."))
            print(f"Colunas: {df.shape[1]}")
            display(df.head())
            display(df.dtypes.to_frame("tipo"))
            display(df.isna().sum().to_frame("nulos"))
            """
        ),
        code(
            """
            assert df.shape[0] >= 10_000, "O dataset nao atende ao minimo de 10.000 registros."
            assert df.select_dtypes(include="number").shape[1] > 0, "Nao ha variaveis numericas."
            assert df.select_dtypes(include="object").shape[1] > 0, "Nao ha variaveis categoricas."
            print("Dataset aprovado nos criterios minimos.")
            """
        ),
        md(
            """
            ## 3. Engenharia de variaveis para analise

            A receita da transacao e calculada por `transaction_qty * unit_price`. Tambem extraimos mes, dia da semana e hora.
            """
        ),
        code(
            """
            df = df.copy()
            df["transaction_date"] = pd.to_datetime(df["transaction_date"])
            df["hour"] = df["transaction_time"].apply(lambda value: value.hour)
            df["revenue"] = df["transaction_qty"] * df["unit_price"]
            df["month"] = df["transaction_date"].dt.month
            df["month_name"] = df["transaction_date"].dt.strftime("%b")
            df["weekday"] = df["transaction_date"].dt.day_name()

            summary = {
                "periodo": f"{df['transaction_date'].min().date()} a {df['transaction_date'].max().date()}",
                "receita_total": round(df["revenue"].sum(), 2),
                "itens_vendidos": int(df["transaction_qty"].sum()),
                "lojas": df["store_location"].nunique(),
                "produtos": df["product_id"].nunique(),
                "categorias": df["product_category"].nunique(),
            }
            summary
            """
        ),
        md(
            """
            ## 4. Data Warehouse: Star Schema

            O DW foi materializado nos CSVs de `data/processed`, prontos para carga no PostgreSQL.

            - `fato_vendas`: grao de uma linha por item/transacao.
            - `dim_tempo`: data, hora, mes, trimestre, dia da semana e periodo do dia.
            - `dim_loja`: loja, cidade, pais e rede.
            - `dim_produto`: categoria, tipo, detalhe e faixa de preco.
            - Dimensao degenerada: `transacao_id` fica diretamente na fato.
            """
        ),
        code(
            """
            tables = {
                "dim_tempo": pd.read_csv(PROCESSED_DIR / "dim_tempo.csv"),
                "dim_loja": pd.read_csv(PROCESSED_DIR / "dim_loja.csv"),
                "dim_produto": pd.read_csv(PROCESSED_DIR / "dim_produto.csv"),
                "fato_vendas": pd.read_csv(PROCESSED_DIR / "fato_vendas.csv"),
            }
            pd.DataFrame(
                [{"tabela": name, "linhas": len(frame), "colunas": len(frame.columns)} for name, frame in tables.items()]
            )
            """
        ),
        code(
            """
            fato = tables["fato_vendas"]
            assert len(fato) == len(df)
            assert (fato["receita"].round(2) == (fato["quantidade"] * fato["preco_unitario"]).round(2)).all()
            print("Fato validada: mesma quantidade de registros e receita correta.")
            """
        ),
        md(
            """
            ## 5. Analise exploratoria de dados

            A EDA cobre distribuicao, comparacao entre categorias e evolucao temporal, como pedido no enunciado.
            """
        ),
        code(
            """
            plt.figure(figsize=(7, 4))
            sns.countplot(data=df, x="transaction_qty")
            plt.title("Distribuicao da quantidade por transacao")
            plt.xlabel("Quantidade")
            plt.ylabel("Transacoes")
            plt.show()
            """
        ),
        code(
            """
            monthly = (
                df.groupby(["month", "month_name"], as_index=False)["revenue"]
                .sum()
                .sort_values("month")
            )
            plt.figure(figsize=(9, 4))
            sns.lineplot(data=monthly, x="month_name", y="revenue", marker="o", linewidth=2.5)
            plt.title("Evolucao temporal da receita")
            plt.xlabel("Mes")
            plt.ylabel("Receita")
            plt.show()
            display(monthly)
            """
        ),
        code(
            """
            store_revenue = df.groupby("store_location", as_index=False)["revenue"].sum().sort_values("revenue")
            plt.figure(figsize=(8, 4))
            sns.barplot(data=store_revenue, x="revenue", y="store_location")
            plt.title("Receita por loja")
            plt.xlabel("Receita")
            plt.ylabel("Loja")
            plt.show()
            display(store_revenue)
            """
        ),
        code(
            """
            category_revenue = (
                df.groupby("product_category", as_index=False)
                .agg(receita=("revenue", "sum"), quantidade=("transaction_qty", "sum"))
                .sort_values("receita", ascending=False)
            )
            plt.figure(figsize=(9, 5))
            sns.barplot(data=category_revenue, x="receita", y="product_category")
            plt.title("Receita por categoria")
            plt.xlabel("Receita")
            plt.ylabel("Categoria")
            plt.show()
            display(category_revenue)
            """
        ),
        code(
            """
            hourly_store = (
                df.groupby(["hour", "store_location"], as_index=False)["transaction_qty"]
                .sum()
                .rename(columns={"transaction_qty": "quantidade"})
            )
            plt.figure(figsize=(10, 5))
            sns.lineplot(data=hourly_store, x="hour", y="quantidade", hue="store_location", marker="o")
            plt.title("Demanda por horario e loja")
            plt.xlabel("Hora")
            plt.ylabel("Itens vendidos")
            plt.show()
            """
        ),
        md(
            """
            ## 6. Base agregada para Machine Learning

            Para transformar transacoes em um problema de demanda, agregamos por data, hora, loja, categoria e tipo de produto.

            - Regressao: prever `quantidade_vendida`.
            - Classificacao: prever `alta_demanda`, definida como quantidade acima do quartil 75.
            """
        ),
        code(
            """
            ml = pd.read_csv(PROCESSED_DIR / "ml_vendas_agregado.csv", parse_dates=["transaction_date"])
            print(ml.shape)
            display(ml.head())
            display(ml["alta_demanda"].value_counts(normalize=True).rename("proporcao"))
            """
        ),
        code(
            """
            def make_encoder():
                try:
                    return OneHotEncoder(handle_unknown="ignore", sparse_output=False)
                except TypeError:
                    return OneHotEncoder(handle_unknown="ignore", sparse=False)

            model_data = ml.sample(n=min(30000, len(ml)), random_state=42)

            features = [
                "transaction_hour",
                "preco_medio",
                "mes",
                "dia_mes",
                "dia_semana",
                "fim_de_semana",
                "store_location",
                "product_category",
                "product_type",
            ]
            numeric_features = ["transaction_hour", "preco_medio", "mes", "dia_mes", "dia_semana", "fim_de_semana"]
            categorical_features = ["store_location", "product_category", "product_type"]

            preprocessor = ColumnTransformer(
                transformers=[
                    ("num", StandardScaler(), numeric_features),
                    ("cat", make_encoder(), categorical_features),
                ]
            )

            X = model_data[features]
            y_class = model_data["alta_demanda"]
            X_train, X_test, y_train, y_test = train_test_split(
                X, y_class, test_size=0.2, random_state=42, stratify=y_class
            )
            """
        ),
        md("## 7. Modelos de classificacao"),
        code(
            """
            classifiers = {
                "KNN": KNeighborsClassifier(n_neighbors=7),
                "Arvore de Decisao": DecisionTreeClassifier(max_depth=12, random_state=42),
                "Random Forest": RandomForestClassifier(n_estimators=120, max_depth=14, random_state=42, n_jobs=-1),
                "Logistic Regression": LogisticRegression(max_iter=1000),
            }

            results = []
            fitted_models = {}
            for name, estimator in classifiers.items():
                pipe = Pipeline(steps=[("preprocess", preprocessor), ("model", estimator)])
                pipe.fit(X_train, y_train)
                pred = pipe.predict(X_test)
                results.append(
                    {
                        "modelo": name,
                        "accuracy": accuracy_score(y_test, pred),
                        "precision": precision_score(y_test, pred, zero_division=0),
                        "recall": recall_score(y_test, pred, zero_division=0),
                        "f1": f1_score(y_test, pred, zero_division=0),
                    }
                )
                fitted_models[name] = (pipe, pred)

            results_df = pd.DataFrame(results).sort_values("f1", ascending=False)
            display(results_df.round(4))
            """
        ),
        code(
            """
            best_model_name = results_df.iloc[0]["modelo"]
            best_pipe, best_pred = fitted_models[best_model_name]
            ConfusionMatrixDisplay.from_predictions(
                y_test,
                best_pred,
                display_labels=["Demanda normal", "Alta demanda"],
                cmap="Blues",
                values_format="d",
            )
            plt.title(f"Matriz de confusao - {best_model_name}")
            plt.show()
            """
        ),
        code(
            """
            if hasattr(best_pipe.named_steps["model"], "feature_importances_"):
                feature_names = best_pipe.named_steps["preprocess"].get_feature_names_out()
                importances = best_pipe.named_steps["model"].feature_importances_
                importance_df = (
                    pd.DataFrame({"feature": feature_names, "importance": importances})
                    .sort_values("importance", ascending=False)
                    .head(12)
                )
                plt.figure(figsize=(8, 5))
                sns.barplot(data=importance_df, x="importance", y="feature")
                plt.title(f"Variaveis mais importantes - {best_model_name}")
                plt.xlabel("Importancia")
                plt.ylabel("Variavel")
                plt.show()
                display(importance_df)
            """
        ),
        md("## 8. Regressao Linear"),
        code(
            """
            y_reg = model_data["quantidade_vendida"]
            X_train_r, X_test_r, y_train_r, y_test_r = train_test_split(
                X, y_reg, test_size=0.2, random_state=42
            )

            reg_pipe = Pipeline(steps=[("preprocess", preprocessor), ("model", LinearRegression())])
            reg_pipe.fit(X_train_r, y_train_r)
            reg_pred = reg_pipe.predict(X_test_r)

            regression_metrics = {
                "MAE": mean_absolute_error(y_test_r, reg_pred),
                "RMSE": mean_squared_error(y_test_r, reg_pred) ** 0.5,
                "R2": r2_score(y_test_r, reg_pred),
            }
            regression_metrics
            """
        ),
        code(
            """
            pred_df = pd.DataFrame({"real": y_test_r, "previsto": reg_pred}).sample(
                n=min(1200, len(y_test_r)), random_state=42
            )
            plt.figure(figsize=(6, 5))
            sns.scatterplot(data=pred_df, x="real", y="previsto", alpha=0.35)
            plt.title("Regressao Linear: demanda real vs prevista")
            plt.xlabel("Quantidade real")
            plt.ylabel("Quantidade prevista")
            plt.show()
            """
        ),
        md(
            """
            ## 9. Comparacao e conclusoes

            - A **Arvore de Decisao** tende a performar melhor neste recorte porque captura regras nao lineares de horario, produto e loja.
            - O **Random Forest** teve boa precisao, mas menor recall, ou seja, errou mais casos de alta demanda.
            - A **Regressao Linear** e limitada para demanda porque as vendas variam por combinacoes categoricas e padroes de horario.
            - Os dados influenciaram o resultado: ha apenas seis meses de historico, tres lojas e nenhuma informacao de cliente, clima, feriado ou campanha.

            ## 10. Insights de negocio

            1. Hell's Kitchen lidera a receita e deve ser prioridade em estoque e equipe.
            2. A demanda se concentra pela manha, especialmente perto das 10h.
            3. Coffee e Tea concentram grande parte da receita; promocoes devem preservar esses produtos como ancoras.
            4. Barista Espresso lidera em receita, enquanto Brewed Chai tea lidera em quantidade vendida.
            5. Produtos de menor giro podem entrar em combos ou campanhas em horarios de menor movimento.
            """
        ),
    ]

    NOTEBOOK_PATH.parent.mkdir(parents=True, exist_ok=True)
    nbf.write(nb, NOTEBOOK_PATH)


if __name__ == "__main__":
    build()
    print(NOTEBOOK_PATH)
