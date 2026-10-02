# Retail Sales Data Warehouse: Kimball Dimensional Modeling and Time-Series Demand Forecasting

**Author:** Henri Mafra  
**License:** MIT License  
**Domain:** Data Warehousing, Dimensional Modeling, Supervised Machine Learning  

---

## 1. Overview

Retail Sales Data Warehouse is an end-to-end data engineering and predictive modeling project demonstrating the construction of an enterprise-grade analytics store. The architecture implements **Ralph Kimball's Dimensional Modeling methodology (Star Schema)**, robust Python ETL pipelines, and supervised machine learning regressors for commercial demand and revenue forecasting.

---

## 2. Dimensional Star Schema Specification

The schema separates additive numerical measures from analytical business dimensions:

### 2.1. Fact Table (`fact_sales`)
- **Granularity:** One record per individual transaction line item.
- **Surrogate Keys:** `date_key`, `time_key`, `product_key`, `store_key`, `customer_key`.
- **Degenerate Dimensions:** `transaction_id`.
- **Additive Measures:** `quantity`, `unit_price`, `discount_amount`, `net_revenue`, `cost_amount`, `gross_margin`.

### 2.2. Dimension Tables
- `dim_date`: Date, DayOfWeek, IsWeekend, Month, Quarter, Year, FiscalQuarter.
- `dim_time`: Hour, Minute, DayPeriod (Morning, Lunch, Afternoon, Evening).
- `dim_product`: SKU, Category, SubCategory, UnitCost, PackagingType.
- `dim_store`: StoreID, StoreName, Region, City, SquareMeters, StoreTier.

---

## 3. Supervised Demand Forecasting Pipeline

The machine learning module extracts lagged features to capture temporal dependencies:

$$y_t = f\left(y_{t-1}, y_{t-7}, y_{t-30}, \text{RollingMean}_{7}(t), \text{DayOfWeek}_t, \text{IsHoliday}_t\right)$$

Evaluation metrics:
- **Root Mean Squared Error (RMSE):** $\sqrt{\frac{1}{N}\sum_{i=1}^N (y_i - \hat{y}_i)^2}$
- **Mean Absolute Error (MAE):** $\frac{1}{N}\sum_{i=1}^N |y_i - \hat{y}_i|$
- **Coefficient of Determination ($R^2$):** $1 - \frac{\sum_i (y_i - \hat{y}_i)^2}{\sum_i (y_i - \bar{y})^2}$

---

## 4. Setup and Execution

```bash
# 1. Clone repository
git clone https://github.com/HenriMafra/retail-sales-data-warehouse.git
cd retail-sales-data-warehouse

# 2. Setup virtual environment
python -m venv venv
source venv/bin/activate  # Windows: .\venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Execute ETL pipeline
python src/etl_pipeline.py

# 5. Execute model training and evaluation
python src/train_forecasting_model.py
```

---

## 5. References

- Kimball, R., & Ross, M. (2013). *The Data Warehouse Toolkit: The Definitive Guide to Dimensional Modeling* (3rd ed.). John Wiley & Sons.
- Hyndman, R. J., & Athanasopoulos, G. (2018). *Forecasting: Principles and Practice* (2nd ed.). OTexts.

---

## 6. License

Licensed under the MIT License. Copyright (c) Henri Mafra.
