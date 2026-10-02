from __future__ import annotations

import json
from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
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


ROOT = Path(__file__).resolve().parents[1]
RAW_PATH = ROOT / "data" / "raw" / "Coffee Shop Sales.xlsx"
PROCESSED_DIR = ROOT / "data" / "processed"
FIGURES_DIR = ROOT / "reports" / "figures"
METRICS_PATH = ROOT / "reports" / "metrics.json"

sns.set_theme(style="whitegrid", palette="Set2")


def savefig(name: str) -> str:
    FIGURES_DIR.mkdir(parents=True, exist_ok=True)
    path = FIGURES_DIR / name
    plt.tight_layout()
    plt.savefig(path, dpi=180, bbox_inches="tight")
    plt.close()
    return str(path.relative_to(ROOT)).replace("\\", "/")


def encoder() -> OneHotEncoder:
    try:
        return OneHotEncoder(handle_unknown="ignore", sparse_output=False)
    except TypeError:
        return OneHotEncoder(handle_unknown="ignore", sparse=False)


def currency(value: float) -> str:
    return f"${value:,.2f}"


def load_data() -> tuple[pd.DataFrame, pd.DataFrame]:
    raw = pd.read_excel(RAW_PATH)
    raw["transaction_date"] = pd.to_datetime(raw["transaction_date"])
    raw["hour"] = raw["transaction_time"].apply(lambda value: int(value.hour))
    raw["revenue"] = raw["transaction_qty"] * raw["unit_price"]
    raw["month"] = raw["transaction_date"].dt.month
    raw["month_name"] = raw["transaction_date"].dt.strftime("%b")
    raw["weekday"] = raw["transaction_date"].dt.day_name()
    ml = pd.read_csv(PROCESSED_DIR / "ml_vendas_agregado.csv", parse_dates=["transaction_date"])
    return raw, ml


def build_charts(raw: pd.DataFrame, metrics: dict) -> None:
    monthly = (
        raw.groupby(["month", "month_name"], as_index=False)["revenue"]
        .sum()
        .sort_values("month")
    )
    plt.figure(figsize=(9, 4.8))
    sns.lineplot(data=monthly, x="month_name", y="revenue", marker="o", linewidth=2.5)
    plt.title("Receita mensal cresceu de janeiro a junho")
    plt.xlabel("Mes")
    plt.ylabel("Receita")
    metrics["figures"]["revenue_by_month"] = savefig("revenue_by_month.png")

    store = raw.groupby("store_location", as_index=False)["revenue"].sum().sort_values("revenue")
    plt.figure(figsize=(8, 4.8))
    sns.barplot(data=store, x="revenue", y="store_location")
    plt.title("Hell's Kitchen lidera em receita")
    plt.xlabel("Receita")
    plt.ylabel("Loja")
    metrics["figures"]["revenue_by_store"] = savefig("revenue_by_store.png")

    category = (
        raw.groupby("product_category", as_index=False)
        .agg(revenue=("revenue", "sum"), quantity=("transaction_qty", "sum"))
        .sort_values("revenue", ascending=False)
    )
    plt.figure(figsize=(9, 5))
    sns.barplot(data=category, x="revenue", y="product_category")
    plt.title("Coffee e Tea concentram maior receita")
    plt.xlabel("Receita")
    plt.ylabel("Categoria")
    metrics["figures"]["revenue_by_category"] = savefig("revenue_by_category.png")

    hourly = (
        raw.groupby(["hour", "store_location"], as_index=False)["transaction_qty"]
        .sum()
        .rename(columns={"transaction_qty": "quantity"})
    )
    plt.figure(figsize=(10, 5))
    sns.lineplot(data=hourly, x="hour", y="quantity", hue="store_location", marker="o")
    plt.title("Pico de demanda acontece no periodo da manha")
    plt.xlabel("Hora")
    plt.ylabel("Itens vendidos")
    metrics["figures"]["hourly_demand_by_store"] = savefig("hourly_demand_by_store.png")

    qty_dist = raw["transaction_qty"].value_counts().sort_index().reset_index()
    qty_dist.columns = ["quantity", "transactions"]
    plt.figure(figsize=(7, 4.5))
    sns.barplot(data=qty_dist, x="quantity", y="transactions")
    plt.title("A maioria das transacoes tem 1 ou 2 itens")
    plt.xlabel("Quantidade por transacao")
    plt.ylabel("Transacoes")
    metrics["figures"]["quantity_distribution"] = savefig("quantity_distribution.png")


def run_models(ml: pd.DataFrame, metrics: dict) -> None:
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
    numeric_features = [
        "transaction_hour",
        "preco_medio",
        "mes",
        "dia_mes",
        "dia_semana",
        "fim_de_semana",
    ]
    categorical_features = ["store_location", "product_category", "product_type"]

    preprocessor = ColumnTransformer(
        transformers=[
            ("num", StandardScaler(), numeric_features),
            ("cat", encoder(), categorical_features),
        ]
    )

    X = model_data[features]
    y_class = model_data["alta_demanda"]
    X_train, X_test, y_train, y_test = train_test_split(
        X, y_class, test_size=0.2, random_state=42, stratify=y_class
    )

    classifiers = {
        "KNN": KNeighborsClassifier(n_neighbors=7),
        "Arvore de Decisao": DecisionTreeClassifier(max_depth=12, random_state=42),
        "Random Forest": RandomForestClassifier(
            n_estimators=120, max_depth=14, random_state=42, n_jobs=-1
        ),
        "Logistic Regression": LogisticRegression(max_iter=1000),
    }
    classification_rows = []
    fitted_models = {}
    for name, estimator in classifiers.items():
        pipe = Pipeline(steps=[("preprocess", preprocessor), ("model", estimator)])
        pipe.fit(X_train, y_train)
        pred = pipe.predict(X_test)
        row = {
            "modelo": name,
            "accuracy": round(float(accuracy_score(y_test, pred)), 4),
            "precision": round(float(precision_score(y_test, pred, zero_division=0)), 4),
            "recall": round(float(recall_score(y_test, pred, zero_division=0)), 4),
            "f1": round(float(f1_score(y_test, pred, zero_division=0)), 4),
        }
        classification_rows.append(row)
        fitted_models[name] = (pipe, pred)

    best = max(classification_rows, key=lambda row: row["f1"])
    metrics["classification"] = classification_rows
    metrics["best_classification_model"] = best

    comparison = pd.DataFrame(classification_rows).sort_values("f1")
    plt.figure(figsize=(8, 4.8))
    sns.barplot(data=comparison, x="f1", y="modelo")
    plt.title("Comparacao dos modelos de classificacao por F1-score")
    plt.xlabel("F1-score")
    plt.ylabel("Modelo")
    metrics["figures"]["model_comparison"] = savefig("model_comparison.png")

    best_pipe, best_pred = fitted_models[best["modelo"]]
    ConfusionMatrixDisplay.from_predictions(
        y_test,
        best_pred,
        display_labels=["Demanda normal", "Alta demanda"],
        cmap="Blues",
        values_format="d",
    )
    plt.title(f"Matriz de confusao - {best['modelo']}")
    metrics["figures"]["confusion_matrix"] = savefig("confusion_matrix.png")

    if hasattr(best_pipe.named_steps["model"], "feature_importances_"):
        feature_names = best_pipe.named_steps["preprocess"].get_feature_names_out()
        importances = best_pipe.named_steps["model"].feature_importances_
        top_features = (
            pd.DataFrame({"feature": feature_names, "importance": importances})
            .sort_values("importance", ascending=False)
            .head(12)
        )
        plt.figure(figsize=(8, 5.2))
        sns.barplot(data=top_features, x="importance", y="feature")
        plt.title(f"Variaveis mais importantes no {best['modelo']}")
        plt.xlabel("Importancia")
        plt.ylabel("Variavel")
        metrics["figures"]["feature_importance"] = savefig("feature_importance.png")
        metrics["top_features"] = top_features.to_dict(orient="records")

    y_reg = model_data["quantidade_vendida"]
    X_train_r, X_test_r, y_train_r, y_test_r = train_test_split(
        X, y_reg, test_size=0.2, random_state=42
    )
    reg_pipe = Pipeline(
        steps=[("preprocess", preprocessor), ("model", LinearRegression())]
    )
    reg_pipe.fit(X_train_r, y_train_r)
    reg_pred = reg_pipe.predict(X_test_r)
    rmse = mean_squared_error(y_test_r, reg_pred) ** 0.5
    metrics["regression"] = {
        "modelo": "Regressao Linear",
        "target": "quantidade_vendida",
        "mae": round(float(mean_absolute_error(y_test_r, reg_pred)), 4),
        "rmse": round(float(rmse), 4),
        "r2": round(float(r2_score(y_test_r, reg_pred)), 4),
    }

    pred_df = pd.DataFrame({"real": y_test_r, "previsto": reg_pred}).sample(
        n=min(1200, len(y_test_r)), random_state=42
    )
    plt.figure(figsize=(6, 5.5))
    sns.scatterplot(data=pred_df, x="real", y="previsto", alpha=0.35)
    plt.title("Regressao Linear: demanda real vs prevista")
    plt.xlabel("Quantidade real")
    plt.ylabel("Quantidade prevista")
    metrics["figures"]["regression_scatter"] = savefig("regression_scatter.png")


def build_business_metrics(raw: pd.DataFrame) -> dict:
    store_revenue = raw.groupby("store_location")["revenue"].sum().sort_values(ascending=False)
    category_revenue = raw.groupby("product_category")["revenue"].sum().sort_values(ascending=False)
    product_revenue = raw.groupby("product_type")["revenue"].sum().sort_values(ascending=False)
    product_qty = raw.groupby("product_type")["transaction_qty"].sum().sort_values(ascending=False)
    month_revenue = raw.groupby("month_name")["revenue"].sum()
    weekday_qty = raw.groupby("weekday")["transaction_qty"].sum().sort_values(ascending=False)
    hour_qty = raw.groupby("hour")["transaction_qty"].sum().sort_values(ascending=False)

    return {
        "rows": int(len(raw)),
        "columns": 11,
        "date_min": str(raw["transaction_date"].min().date()),
        "date_max": str(raw["transaction_date"].max().date()),
        "total_revenue": round(float(raw["revenue"].sum()), 2),
        "total_quantity": int(raw["transaction_qty"].sum()),
        "stores": int(raw["store_location"].nunique()),
        "products": int(raw["product_id"].nunique()),
        "categories": int(raw["product_category"].nunique()),
        "top_store": {
            "name": store_revenue.index[0],
            "revenue": round(float(store_revenue.iloc[0]), 2),
        },
        "top_category": {
            "name": category_revenue.index[0],
            "revenue": round(float(category_revenue.iloc[0]), 2),
        },
        "top_product_by_revenue": {
            "name": product_revenue.index[0],
            "revenue": round(float(product_revenue.iloc[0]), 2),
        },
        "top_product_by_quantity": {
            "name": product_qty.index[0],
            "quantity": int(product_qty.iloc[0]),
        },
        "top_weekday": {
            "name": weekday_qty.index[0],
            "quantity": int(weekday_qty.iloc[0]),
        },
        "peak_hour": {"hour": int(hour_qty.index[0]), "quantity": int(hour_qty.iloc[0])},
        "monthly_revenue": {
            str(index): round(float(value), 2) for index, value in month_revenue.items()
        },
    }


def main() -> None:
    raw, ml = load_data()
    metrics = {"figures": {}, "business": build_business_metrics(raw)}
    build_charts(raw, metrics)
    run_models(ml, metrics)
    METRICS_PATH.parent.mkdir(parents=True, exist_ok=True)
    METRICS_PATH.write_text(json.dumps(metrics, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(metrics, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
