# main.py — Run the entire pipeline with one command
import os
import sys

sys.path.insert(0, ".")

os.makedirs("data", exist_ok=True)
os.makedirs("models", exist_ok=True)
os.makedirs("outputs/charts", exist_ok=True)
os.makedirs("outputs/reports", exist_ok=True)
print("=" * 60)
print("  RETAIL SALES FORECASTING & INVENTORY OPTIMIZATION")
print("=" * 60)

print("\n[Phase 1] Generating Synthetic Dataset...")
from src.generate_dataset import generate_sales_data
generate_sales_data()

print("\n[Phase 2] Preprocessing & Cleaning...")
from src.preprocessing import load_and_clean
load_and_clean()

print("\n[Phase 3] Exploratory Data Analysis...")
from src.eda import run_eda
run_eda()

print("\n[Phase 4] Feature Engineering...")
from src.feature_engineering import engineer_features
engineer_features()

print("\n[Phase 5] Forecasting Model Training...")
from src.forecasting import train_and_evaluate
train_and_evaluate()

print("\n[Phase 6] Inventory Optimization...")
from src.inventory_optimization import calculate_inventory_metrics
calculate_inventory_metrics()

print("\n[Phase 7] Business Insights Summary...")
from src.business_insights import generate_summary_report
generate_summary_report()

print("\n" + "=" * 60)
print("  ALL PHASES COMPLETE. Outputs saved to outputs/")
print("=" * 60)