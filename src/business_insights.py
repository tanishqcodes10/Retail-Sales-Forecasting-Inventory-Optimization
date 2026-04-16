# src/business_insights.py
# Generates business summary report and yearly comparison chart

import os
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker

os.makedirs("outputs/reports", exist_ok=True)
os.makedirs("outputs/charts", exist_ok=True)


def generate_summary_report():
    df = pd.read_csv("data/retail_sales_clean.csv", parse_dates=["date"])

    metrics_path = "outputs/reports/model_metrics.csv"
    inventory_path = "outputs/reports/inventory_optimization_report.csv"

    if os.path.exists(metrics_path):
        metrics = pd.read_csv(metrics_path, index_col=0)
        best_model = metrics["R2"].idxmax()
        best_r2 = metrics["R2"].max()
    else:
        best_model = "Not Available"
        best_r2 = None

    if os.path.exists(inventory_path):
        inv = pd.read_csv(inventory_path)
        reorder_ct = (inv["alert"].astype(str).str.contains("REORDER")).sum()
    else:
        reorder_ct = 0

    total_revenue = df["revenue"].sum()
    total_units = df["units_sold"].sum()
    avg_daily_revenue = df.groupby("date")["revenue"].sum().mean()
    best_category = df.groupby("category")["revenue"].sum().idxmax()
    best_store = df.groupby("store")["revenue"].sum().idxmax()

    summary = {
        "Total Revenue (₹)": f"₹{total_revenue:,.0f}",
        "Total Units Sold": f"{total_units:,}",
        "Average Daily Revenue (₹)": f"₹{avg_daily_revenue:,.0f}",
        "Best Performing Category": best_category,
        "Best Performing Store": best_store,
        "Products Needing Reorder": int(reorder_ct),
        "Best Forecast Model": best_model,
        "Best Model R2": f"{best_r2:.4f}" if best_r2 is not None else "N/A"
    }

    summary_df = pd.DataFrame(list(summary.items()), columns=["Metric", "Value"])
    summary_df.to_csv("outputs/reports/business_summary.csv", index=False)

    print("\n========== BUSINESS SUMMARY ==========")
    print(summary_df.to_string(index=False))

    # Year-over-year monthly revenue chart
    monthly = (
        df.groupby([df["date"].dt.year, df["date"].dt.month])["revenue"]
        .sum()
        .unstack(0)
    )

    plt.figure(figsize=(12, 6))
    for year in monthly.columns:
        plt.plot(monthly.index, monthly[year], marker="o", linewidth=2, label=str(year))

    plt.title("Year-over-Year Monthly Revenue Comparison", fontsize=14, fontweight="bold")
    plt.xlabel("Month")
    plt.ylabel("Revenue")
    plt.xticks(
        range(1, 13),
        ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
         "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    )
    plt.gca().yaxis.set_major_formatter(
        mticker.FuncFormatter(lambda x, _: f"₹{x/1e6:.1f}M")
    )
    plt.legend(title="Year")
    plt.tight_layout()
    plt.savefig("outputs/charts/11_yoy_comparison.png", dpi=300, bbox_inches="tight")
    plt.close()

    print("\nSaved:")
    print("- outputs/reports/business_summary.csv")
    print("- outputs/charts/11_yoy_comparison.png")
    print("========== SUMMARY COMPLETE ==========")

    return summary_df


if __name__ == "__main__":
    generate_summary_report()