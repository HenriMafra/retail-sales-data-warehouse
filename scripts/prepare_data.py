from __future__ import annotations

import json
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
RAW_PATH = ROOT / "data" / "raw" / "Coffee Shop Sales.xlsx"
PROCESSED_DIR = ROOT / "data" / "processed"

MONTHS_PT = {
    1: "Janeiro",
    2: "Fevereiro",
    3: "Marco",
    4: "Abril",
    5: "Maio",
    6: "Junho",
    7: "Julho",
    8: "Agosto",
    9: "Setembro",
    10: "Outubro",
    11: "Novembro",
    12: "Dezembro",
}

DAYS_PT = {
    0: "Segunda-feira",
    1: "Terca-feira",
    2: "Quarta-feira",
    3: "Quinta-feira",
    4: "Sexta-feira",
    5: "Sabado",
    6: "Domingo",
}


def price_band(value: float) -> str:
    if value < 3:
        return "Baixo"
    if value < 5:
        return "Medio"
    return "Alto"


def load_raw() -> pd.DataFrame:
    if not RAW_PATH.exists():
        raise FileNotFoundError(
            f"Arquivo nao encontrado: {RAW_PATH}. Baixe o dataset da Maven/Kaggle antes de rodar."
        )

    df = pd.read_excel(RAW_PATH)
    expected_columns = {
        "transaction_id",
        "transaction_date",
        "transaction_time",
        "transaction_qty",
        "store_id",
        "store_location",
        "product_id",
        "unit_price",
        "product_category",
        "product_type",
        "product_detail",
    }
    missing = expected_columns.difference(df.columns)
    if missing:
        raise ValueError(f"Colunas ausentes no dataset: {sorted(missing)}")

    df = df.copy()
    df["transaction_date"] = pd.to_datetime(df["transaction_date"])
    df["transaction_hour"] = df["transaction_time"].apply(lambda value: int(value.hour))
    df["tempo_key"] = (
        df["transaction_date"].dt.strftime("%Y%m%d").astype(int) * 100 + df["transaction_hour"]
    )
    df["receita"] = (df["transaction_qty"] * df["unit_price"]).round(2)
    return df


def build_dimensions(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    dim_tempo = (
        df[["tempo_key", "transaction_date", "transaction_hour"]]
        .drop_duplicates()
        .rename(columns={"transaction_date": "data", "transaction_hour": "hora"})
        .sort_values(["data", "hora"])
        .reset_index(drop=True)
    )
    dim_tempo["ano"] = dim_tempo["data"].dt.year
    dim_tempo["mes"] = dim_tempo["data"].dt.month
    dim_tempo["nome_mes"] = dim_tempo["mes"].map(MONTHS_PT)
    dim_tempo["trimestre"] = dim_tempo["data"].dt.quarter
    dim_tempo["dia_mes"] = dim_tempo["data"].dt.day
    dim_tempo["dia_semana_num"] = dim_tempo["data"].dt.weekday + 1
    dim_tempo["nome_dia_semana"] = dim_tempo["data"].dt.weekday.map(DAYS_PT)
    dim_tempo["fim_de_semana"] = dim_tempo["data"].dt.weekday >= 5
    dim_tempo["periodo_dia"] = pd.cut(
        dim_tempo["hora"],
        bins=[-1, 10, 14, 18, 23],
        labels=["Manha", "Almoco", "Tarde", "Noite"],
    ).astype(str)
    dim_tempo = dim_tempo[
        [
            "tempo_key",
            "data",
            "hora",
            "ano",
            "mes",
            "nome_mes",
            "trimestre",
            "dia_mes",
            "dia_semana_num",
            "nome_dia_semana",
            "fim_de_semana",
            "periodo_dia",
        ]
    ]

    dim_loja = (
        df[["store_id", "store_location"]]
        .drop_duplicates()
        .rename(columns={"store_id": "loja_key", "store_location": "localizacao"})
        .sort_values("loja_key")
        .reset_index(drop=True)
    )
    dim_loja["cidade"] = "New York"
    dim_loja["pais"] = "Estados Unidos"
    dim_loja["rede"] = "Maven Roasters"
    dim_loja["tipo_loja"] = "Cafeteria"

    produto_price = (
        df.groupby("product_id", as_index=False)
        .agg(
            preco_medio=("unit_price", "mean"),
            preco_minimo=("unit_price", "min"),
            preco_maximo=("unit_price", "max"),
        )
        .round(2)
    )
    dim_produto = (
        df[["product_id", "product_category", "product_type", "product_detail"]]
        .drop_duplicates()
        .merge(produto_price, on="product_id", how="left")
        .rename(
            columns={
                "product_id": "produto_key",
                "product_category": "categoria",
                "product_type": "tipo_produto",
                "product_detail": "detalhe_produto",
            }
        )
        .sort_values("produto_key")
        .reset_index(drop=True)
    )
    dim_produto["faixa_preco"] = dim_produto["preco_medio"].apply(price_band)

    return dim_tempo, dim_loja, dim_produto


def build_fact(df: pd.DataFrame) -> pd.DataFrame:
    fato = df[
        [
            "transaction_id",
            "tempo_key",
            "store_id",
            "product_id",
            "transaction_qty",
            "unit_price",
            "receita",
        ]
    ].rename(
        columns={
            "transaction_id": "transacao_id",
            "store_id": "loja_key",
            "product_id": "produto_key",
            "transaction_qty": "quantidade",
            "unit_price": "preco_unitario",
        }
    )
    fato = fato.sort_values("transacao_id").reset_index(drop=True)
    fato.insert(0, "venda_key", range(1, len(fato) + 1))
    return fato


def build_ml_dataset(df: pd.DataFrame) -> pd.DataFrame:
    ml = (
        df.groupby(
            [
                "transaction_date",
                "transaction_hour",
                "store_location",
                "product_category",
                "product_type",
            ],
            as_index=False,
        )
        .agg(
            quantidade_vendida=("transaction_qty", "sum"),
            receita=("receita", "sum"),
            preco_medio=("unit_price", "mean"),
            transacoes=("transaction_id", "count"),
        )
        .round({"receita": 2, "preco_medio": 2})
    )
    ml["ano"] = ml["transaction_date"].dt.year
    ml["mes"] = ml["transaction_date"].dt.month
    ml["dia_mes"] = ml["transaction_date"].dt.day
    ml["dia_semana"] = ml["transaction_date"].dt.weekday
    ml["fim_de_semana"] = (ml["dia_semana"] >= 5).astype(int)
    threshold = ml["quantidade_vendida"].quantile(0.75)
    ml["alta_demanda"] = (ml["quantidade_vendida"] >= threshold).astype(int)
    return ml


def write_outputs() -> dict:
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    df = load_raw()
    dim_tempo, dim_loja, dim_produto = build_dimensions(df)
    fato = build_fact(df)
    ml = build_ml_dataset(df)

    outputs = {
        "dim_tempo": dim_tempo,
        "dim_loja": dim_loja,
        "dim_produto": dim_produto,
        "fato_vendas": fato,
        "ml_vendas_agregado": ml,
    }
    for name, frame in outputs.items():
        frame.to_csv(PROCESSED_DIR / f"{name}.csv", index=False, encoding="utf-8")

    summary = {
        "raw_rows": int(len(df)),
        "raw_columns": 11,
        "date_min": str(df["transaction_date"].min().date()),
        "date_max": str(df["transaction_date"].max().date()),
        "stores": sorted(df["store_location"].unique().tolist()),
        "categories": sorted(df["product_category"].unique().tolist()),
        "dim_tempo_rows": int(len(dim_tempo)),
        "dim_loja_rows": int(len(dim_loja)),
        "dim_produto_rows": int(len(dim_produto)),
        "fato_vendas_rows": int(len(fato)),
        "ml_rows": int(len(ml)),
        "total_revenue": round(float(df["receita"].sum()), 2),
        "total_quantity": int(df["transaction_qty"].sum()),
        "top_store_by_revenue": (
            df.groupby("store_location")["receita"].sum().sort_values(ascending=False).index[0]
        ),
        "top_category_by_revenue": (
            df.groupby("product_category")["receita"].sum().sort_values(ascending=False).index[0]
        ),
        "top_product_type_by_revenue": (
            df.groupby("product_type")["receita"].sum().sort_values(ascending=False).index[0]
        ),
        "peak_hour_by_quantity": int(
            df.groupby("transaction_hour")["transaction_qty"].sum().sort_values(ascending=False).index[0]
        ),
    }
    (PROCESSED_DIR / "summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    return summary


if __name__ == "__main__":
    result = write_outputs()
    print(json.dumps(result, ensure_ascii=False, indent=2))
