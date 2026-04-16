# src/inventory_optimization.py
import pandas as pd
import numpy as np
import os

os.makedirs("outputs/reports", exist_ok=True)

def calculate_inventory_metrics(filepath="data/retail_sales_clean.csv"):
    df = pd.read_csv(filepath, parse_dates=["date"])

    stats = (
        df.groupby(["store","category","product"])
          .agg(
              avg_daily_demand = ("units_sold","mean"),
              std_daily_demand = ("units_sold","std"),
              avg_lead_time    = ("lead_time_days","mean"),
              avg_stock        = ("stock_level","mean"),
              total_revenue    = ("revenue","sum"),
          )
          .reset_index().round(2)
    )

    Z = 1.65  # 95% service level
    stats["safety_stock"] = (
        Z * stats["std_daily_demand"] * np.sqrt(stats["avg_lead_time"])
    ).round(0).astype(int)

    stats["reorder_point"] = (
        stats["avg_daily_demand"] * stats["avg_lead_time"] + stats["safety_stock"]
    ).round(0).astype(int)

    annual_demand = stats["avg_daily_demand"] * 365
    stats["eoq"] = (np.sqrt(2 * annual_demand * 500 / 50)).round(0).astype(int)

    stats["stockout_risk"] = stats["avg_stock"] < stats["reorder_point"]
    stats["alert"]         = stats["stockout_risk"].map({True: "🔴 REORDER NOW", False: "🟢 OK"})
    stats["days_of_stock"] = (
        stats["avg_stock"] / stats["avg_daily_demand"].replace(0, np.nan)
    ).round(1)

    stats.to_csv("outputs/reports/inventory_optimization_report.csv", index=False)
    print(f"Products needing reorder: {stats['stockout_risk'].sum()} / {len(stats)}")
    return stats

if __name__ == "__main__":
    calculate_inventory_metrics()