# src/eda.py
# Exploratory Data Analysis for Retail Sales Forecasting Project

import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.ticker as mticker

sns.set_theme(style="whitegrid")
os.makedirs("outputs/charts", exist_ok=True)


def run_eda(filepath="data/retail_sales_clean.csv"):
    df = pd.read_csv(filepath, parse_dates=["date"])

    print("\n========== EDA STARTED ==========")
    print("\nDataset Shape:", df.shape)
    print("\nColumns:")
    print(df.columns.tolist())

    print("\nSummary Statistics:")
    print(df.describe(include="all"))

    # -------------------------------
    # 1. Monthly Revenue Trend
    # -------------------------------
    monthly_sales = (
        df.groupby(df["date"].dt.to_period("M"))["revenue"]
        .sum()
        .reset_index()
    )
    monthly_sales["date"] = monthly_sales["date"].astype(str)

    plt.figure(figsize=(14, 6))
    plt.plot(monthly_sales["date"], monthly_sales["revenue"], marker="o", linewidth=2, color="#01696f")
    plt.xticks(range(0, len(monthly_sales), 3), monthly_sales["date"][::3], rotation=45)
    plt.title("Monthly Revenue Trend", fontsize=14, fontweight="bold")
    plt.xlabel("Month")
    plt.ylabel("Revenue")
    plt.gca().yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"₹{x/1e6:.1f}M"))
    plt.tight_layout()
    plt.savefig("outputs/charts/01_monthly_revenue_trend.png", dpi=300, bbox_inches="tight")
    plt.close()

    # -------------------------------
    # 2. Category-wise Revenue
    # -------------------------------
    category_sales = df.groupby("category")["revenue"].sum().sort_values(ascending=False)

    plt.figure(figsize=(10, 6))
    sns.barplot(x=category_sales.index, y=category_sales.values, palette="viridis")
    plt.title("Category-wise Revenue", fontsize=14, fontweight="bold")
    plt.xlabel("Category")
    plt.ylabel("Revenue")
    plt.gca().yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"₹{x/1e6:.1f}M"))
    plt.tight_layout()
    plt.savefig("outputs/charts/02_category_revenue.png", dpi=300, bbox_inches="tight")
    plt.close()

    # -------------------------------
    # 3. Store-wise Revenue
    # -------------------------------
    store_sales = df.groupby("store")["revenue"].sum().sort_values(ascending=False)

    plt.figure(figsize=(8, 5))
    sns.barplot(x=store_sales.values, y=store_sales.index, palette="magma")
    plt.title("Store-wise Revenue", fontsize=14, fontweight="bold")
    plt.xlabel("Revenue")
    plt.ylabel("Store")
    plt.gca().xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"₹{x/1e6:.1f}M"))
    plt.tight_layout()
    plt.savefig("outputs/charts/03_store_revenue.png", dpi=300, bbox_inches="tight")
    plt.close()

    # -------------------------------
    # 4. Sales Heatmap (Month vs Day of Week)
    # -------------------------------
    heatmap_data = df.pivot_table(
        values="units_sold",
        index="day_of_week",
        columns="month",
        aggfunc="mean"
    )

    day_names = {
        0: "Mon", 1: "Tue", 2: "Wed", 3: "Thu",
        4: "Fri", 5: "Sat", 6: "Sun"
    }
    heatmap_data.index = [day_names.get(i, i) for i in heatmap_data.index]

    plt.figure(figsize=(12, 6))
    sns.heatmap(heatmap_data, cmap="YlOrBr", annot=True, fmt=".0f")
    plt.title("Average Units Sold Heatmap (Day of Week vs Month)", fontsize=14, fontweight="bold")
    plt.xlabel("Month")
    plt.ylabel("Day of Week")
    plt.tight_layout()
    plt.savefig("outputs/charts/04_sales_heatmap.png", dpi=300, bbox_inches="tight")
    plt.close()

    # -------------------------------
    # 5. Holiday vs Non-Holiday Revenue
    # -------------------------------
    holiday_sales = df.groupby("is_holiday_season")["revenue"].mean().reset_index()
    holiday_sales["season"] = holiday_sales["is_holiday_season"].map({0: "Non-Holiday", 1: "Holiday Season"})

    plt.figure(figsize=(8, 5))
    sns.barplot(data=holiday_sales, x="season", y="revenue", palette="Set2")
    plt.title("Average Revenue: Holiday vs Non-Holiday", fontsize=14, fontweight="bold")
    plt.xlabel("Season Type")
    plt.ylabel("Average Revenue")
    plt.gca().yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"₹{x:,.0f}"))
    plt.tight_layout()
    plt.savefig("outputs/charts/05_holiday_vs_nonholiday.png", dpi=300, bbox_inches="tight")
    plt.close()

    # -------------------------------
    # 6. Top 10 Products by Revenue
    # -------------------------------
    top_products = df.groupby("product")["revenue"].sum().sort_values(ascending=False).head(10)

    plt.figure(figsize=(10, 6))
    sns.barplot(x=top_products.values, y=top_products.index, palette="crest")
    plt.title("Top 10 Products by Revenue", fontsize=14, fontweight="bold")
    plt.xlabel("Revenue")
    plt.ylabel("Product")
    plt.gca().xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"₹{x/1e6:.1f}M"))
    plt.tight_layout()
    plt.savefig("outputs/charts/06_top10_products.png", dpi=300, bbox_inches="tight")
    plt.close()

    print("\nEDA complete. Charts saved in outputs/charts/")
    print("Generated charts:")
    print("1. 01_monthly_revenue_trend.png")
    print("2. 02_category_revenue.png")
    print("3. 03_store_revenue.png")
    print("4. 04_sales_heatmap.png")
    print("5. 05_holiday_vs_nonholiday.png")
    print("6. 06_top10_products.png")
    print("\n========== EDA COMPLETED ==========")


if __name__ == "__main__":
    run_eda()