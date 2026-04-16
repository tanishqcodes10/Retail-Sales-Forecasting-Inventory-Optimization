# src/forecasting.py
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import joblib, os

os.makedirs("models", exist_ok=True)
os.makedirs("outputs/charts", exist_ok=True)

FEATURE_COLS = [
    "lag_1w","lag_2w","lag_3w","lag_4w",
    "roll_mean_2w","roll_mean_4w","roll_mean_8w",
    "month","quarter","week_of_year","year",
    "is_holiday_season","avg_price",
    "store_code","category_code","product_code",
]
TARGET = "units_sold"

def train_and_evaluate(filepath="data/retail_features.csv"):
    df = pd.read_csv(filepath, parse_dates=["date"])
    df.sort_values("date", inplace=True)

    split_idx = int(len(df) * 0.80)
    X_train = df.iloc[:split_idx][FEATURE_COLS]
    y_train = df.iloc[:split_idx][TARGET]
    X_test  = df.iloc[split_idx:][FEATURE_COLS]
    y_test  = df.iloc[split_idx:][TARGET]

    models = {
        "Linear Regression":  LinearRegression(),
        "Random Forest":      RandomForestRegressor(n_estimators=150, max_depth=12,
                                                    random_state=42, n_jobs=-1),
        "Gradient Boosting":  GradientBoostingRegressor(n_estimators=100, max_depth=5,
                                                        learning_rate=0.1, random_state=42),
    }

    results = {}
    for name, model in models.items():
        model.fit(X_train, y_train)
        preds = model.predict(X_test).clip(min=0)
        results[name] = {
            "MAE":   mean_absolute_error(y_test, preds),
            "RMSE":  np.sqrt(mean_squared_error(y_test, preds)),
            "R2":    r2_score(y_test, preds),
            "model": model, "preds": preds
        }
        print(f"{name:22s} | MAE={results[name]['MAE']:.2f}  R²={results[name]['R2']:.4f}")

    best_name  = max(results, key=lambda k: results[k]["R2"])
    best_model = results[best_name]["model"]
    joblib.dump(best_model, "models/best_forecasting_model.pkl")
    print(f"\nBest model: {best_name} saved.")

    metrics_df = pd.DataFrame({k:{m:v for m,v in v.items() if m not in ("model","preds")}
                                for k,v in results.items()}).T.round(4)
    metrics_df.to_csv("outputs/reports/model_metrics.csv")
    return best_model, df.iloc[split_idx:].copy().assign(predicted=results[best_name]["preds"])

if __name__ == "__main__":
    train_and_evaluate()