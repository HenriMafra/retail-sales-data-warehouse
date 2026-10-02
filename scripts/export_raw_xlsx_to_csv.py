from __future__ import annotations

from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
XLSX_PATH = ROOT / "data" / "raw" / "Coffee Shop Sales.xlsx"
CSV_PATH = ROOT / "data" / "raw" / "coffee_shop_sales_raw.csv"


def main() -> None:
    if not XLSX_PATH.exists():
        raise FileNotFoundError(f"Arquivo bruto nao encontrado: {XLSX_PATH}")

    df = pd.read_excel(XLSX_PATH, sheet_name="Transactions")
    df["transaction_date"] = pd.to_datetime(df["transaction_date"]).dt.strftime("%Y-%m-%d")
    df["transaction_time"] = df["transaction_time"].astype(str)
    df.to_csv(CSV_PATH, index=False, encoding="utf-8")
    print(f"CSV bruto gerado: {CSV_PATH}")
    print(f"Linhas: {len(df)}")
    print(f"Colunas: {len(df.columns)}")


if __name__ == "__main__":
    main()
