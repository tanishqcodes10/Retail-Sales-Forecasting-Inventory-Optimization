# src/preprocessing.py
import pandas as pd
import numpy as np
import os

def load_and_clean(filepath="data/retail_sales_raw.csv"):
    df = pd.read_csv(filepath, parse_dates=["date"])

    print("=== MISSING VALUES ===")
    print(df.isnull().sum())

    before = len(df)
    df.drop_duplicates(inplace=True)
    print(f"Dropped {before - len(df)} duplicate rows")

    num_cols = df.select_dtypes(include=np.number).columns
    for col in num_cols:
        if df[col].isnull().any():
            df[col].fillna(df[col].median(), inplace=True)

    df["units_sold"]  = df["units_sold"].clip(lower=0)
    df["revenue"]     = df["revenue"].clip(lower=0)
    df["stock_level"] = df["stock_level"].clip(lower=0)

    df["year"]              = df["date"].dt.year
    df["month"]             = df["date"].dt.month
    df["day"]               = df["date"].dt.day
    df["day_of_week"]       = df["date"].dt.dayofweek
    df["week_of_year"]      = df["date"].dt.isocalendar().week.astype(int)
    df["quarter"]           = df["date"].dt.quarter
    df["is_weekend"]        = (df["day_of_week"] >= 5).astype(int)
    df["is_holiday_season"] = df["month"].isin([10, 11, 12, 1]).astype(int)

    os.makedirs("data", exist_ok=True)
    df.to_csv("data/retail_sales_clean.csv", index=False)
    print(f"Cleaned dataset saved: {df.shape}")
    return df

if __name__ == "__main__":
    load_and_clean()