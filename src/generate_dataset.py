# src/generate_dataset.py
import pandas as pd
import numpy as np
from datetime import datetime
import os

np.random.seed(42)

STORES      = ["Store_A", "Store_B", "Store_C"]
PRODUCTS    = {
    "Electronics": ["Laptop", "Mobile", "Headphones", "Tablet", "Smartwatch"],
    "Groceries":   ["Rice", "Wheat", "Sugar", "Oil", "Salt"],
    "Clothing":    ["T-Shirt", "Jeans", "Jacket", "Saree", "Shoes"],
    "Sports":      ["Cricket_Bat", "Football", "Yoga_Mat", "Dumbbells", "Cycle"],
}
START_DATE  = datetime(2021, 1, 1)
END_DATE    = datetime(2023, 12, 31)
HOLIDAY_MONTHS = [10, 11, 12, 1]

def generate_sales_data():
    records = []
    date_range = pd.date_range(START_DATE, END_DATE, freq="D")

    for store in STORES:
        for category, products in PRODUCTS.items():
            for product in products:
                base_price     = np.random.uniform(50, 5000)
                base_demand    = np.random.randint(5, 80)
                stock_level    = np.random.randint(100, 500)
                reorder_point  = np.random.randint(30, 80)
                lead_time_days = np.random.randint(3, 10)

                for date in date_range:
                    seasonal_mult = 1.4 if date.month in HOLIDAY_MONTHS else 1.0
                    weekend_mult  = 1.2 if date.dayofweek >= 5 else 1.0
                    trend_mult    = 1 + (date.year - 2021) * 0.05
                    noise         = np.random.normal(1.0, 0.15)

                    units_sold = max(0, int(
                        base_demand * seasonal_mult * weekend_mult * trend_mult * noise
                    ))
                    units_sold = min(units_sold, stock_level)
                    revenue = round(units_sold * base_price * np.random.uniform(0.95, 1.05), 2)
                    discount_pct = np.random.choice([0, 5, 10, 15, 20], p=[0.5, 0.2, 0.15, 0.1, 0.05])

                    stock_level = max(0, stock_level - units_sold)
                    if stock_level < reorder_point:
                        stock_level += np.random.randint(100, 300)

                    records.append({
                        "date": date, "store": store, "category": category,
                        "product": product, "units_sold": units_sold,
                        "unit_price": round(base_price, 2), "revenue": revenue,
                        "discount_pct": discount_pct, "stock_level": stock_level,
                        "reorder_point": reorder_point, "lead_time_days": lead_time_days,
                    })

    df = pd.DataFrame(records)
    df["date"] = pd.to_datetime(df["date"])
    os.makedirs("data", exist_ok=True)
    df.to_csv("data/retail_sales_raw.csv", index=False)
    print(f"Dataset created: {df.shape[0]:,} rows x {df.shape[1]} columns")
    return df

if __name__ == "__main__":
    generate_sales_data()