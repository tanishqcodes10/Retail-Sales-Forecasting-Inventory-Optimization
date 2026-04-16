# src/feature_engineering.py
import pandas as pd
import numpy as np
import os

def engineer_features(filepath="data/retail_sales_clean.csv"):
    df = pd.read_csv(filepath, parse_dates=["date"])

    df_weekly = (
        df.groupby(["store", "category", "product",
                    pd.Grouper(key="date", freq="W")])
          .agg(units_sold=("units_sold","sum"),
               revenue=("revenue","sum"),
               avg_stock=("stock_level","mean"),
               avg_price=("unit_price","mean"))
          .reset_index()
    )
    df_weekly.sort_values(["store","product","date"], inplace=True)

    for lag in [1, 2, 3, 4]:
        df_weekly[f"lag_{lag}w"] = (
            df_weekly.groupby(["store","product"])["units_sold"].shift(lag)
        )

    for window in [2, 4, 8]:
        df_weekly[f"roll_mean_{window}w"] = (
            df_weekly.groupby(["store","product"])["units_sold"]
                     .transform(lambda x: x.shift(1).rolling(window, min_periods=1).mean())
        )

    df_weekly["month"]             = df_weekly["date"].dt.month
    df_weekly["quarter"]           = df_weekly["date"].dt.quarter
    df_weekly["week_of_year"]      = df_weekly["date"].dt.isocalendar().week.astype(int)
    df_weekly["year"]              = df_weekly["date"].dt.year
    df_weekly["is_holiday_season"] = df_weekly["month"].isin([10,11,12,1]).astype(int)

    for col in ["store","category","product"]:
        df_weekly[f"{col}_code"] = df_weekly[col].astype("category").cat.codes

    df_weekly.dropna(inplace=True)
    df_weekly.to_csv("data/retail_features.csv", index=False)
    print(f"Feature-engineered dataset: {df_weekly.shape}")
    return df_weekly

if __name__ == "__main__":
    engineer_features()