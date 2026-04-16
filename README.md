# 🛒 Retail Sales Forecasting & Inventory Optimization System

**An end-to-end retail analytics system** that forecasts weekly product sales using Machine Learning and provides automated inventory optimization — Safety Stock, Reorder Points, EOQ calculations, and stockout risk alerts — all without needing real company data.

***

## 🔍 Overview

This project simulates a real-world **retail analytics pipeline** similar to systems used by companies like **D-Mart, Reliance Retail, Amazon, Flipkart, and Walmart** to:

- 📈 **Forecast** weekly product sales using ML models (Random Forest, Gradient Boosting, Linear Regression)
- 📦 **Optimize inventory** using Safety Stock, Reorder Point, and EOQ formulas
- 🔔 **Detect stockout risk** and generate automated reorder alerts
- 📊 **Visualize business insights** through an interactive Streamlit dashboard

The entire project is built on **synthetically generated retail data** — no real company access required. This makes it a perfect portfolio project for students targeting Data Analyst, Business Analyst, Supply Chain Analyst, and Data Science roles.

***

## 🎯 Problem Statement

Retail businesses lose **millions of rupees every year** due to:

| Problem | Impact |
|---|---|
| **Overstock** | Money locked in unsold inventory, high storage costs |
| **Stockout** | Lost sales, unhappy customers, damaged brand reputation |
| **Manual forecasting** | Inaccurate guesswork, no data-driven decisions |
| **Reactive replenishment** | Ordering after stock runs out instead of before |

**This system solves all of the above** by using historical sales data combined with Machine Learning to:
- Accurately predict future demand at product-store level
- Automatically calculate optimal stock levels
- Alert managers when products need to be reordered

***

## 🏭 Industry Relevance

| Company | Real-World Use Case |
|---|---|
| **D-Mart** | Weekly demand planning for 5,000+ SKUs across stores |
| **Amazon** | Real-time inventory management in fulfillment centers |
| **Flipkart** | Seller stock recommendations and warehouse optimization |
| **Walmart** | Supply chain demand forecasting across regions |
| **Reliance Retail** | Category-level sales trend analysis and reorder automation |
| **Big Basket** | Perishable goods demand forecasting to reduce waste |

***

## 💼 Business Value

- **Reduce excess inventory** → Lower holding costs
- **Prevent stockouts** → No lost sales
- **Automate reorder decisions** → Save analyst time
- **Identify top-performing products and categories** → Better purchasing strategy
- **Understand seasonal trends** → Plan promotions around demand peaks

***

## 🛠️ Tech Stack

| Tool | Purpose |
|---|---|
| **Python 3.9+** | Core programming language |
| **Pandas** | Data manipulation and analysis |
| **NumPy** | Numerical computation |
| **Matplotlib** | Static chart generation |
| **Seaborn** | Statistical visualizations |
| **Scikit-learn** | Machine learning models |
| **Joblib** | Model saving and loading |
| **Streamlit** | Interactive web dashboard |
| **Plotly** | Interactive charts in dashboard |
| **CSV/Excel** | Data storage format |

***

## 🏗️ Architecture

```
┌──────────────────────────────────────────────────┐
│              INPUT LAYER                         │
│   Synthetic CSV (65,700 rows × 11 columns)       │
│   3 Stores | 4 Categories | 20 Products          │
│   3 Years Daily Data (2021–2023)                 │
└──────────────────────┬───────────────────────────┘
                       │
                       ▼
┌──────────────────────────────────────────────────┐
│    MODULE 1: DATA GENERATION                     │
│    src/generate_dataset.py                       │
│    Simulates seasonality, trends, weekend        │
│    boosts, holiday spikes, restocking events     │
└──────────────────────┬───────────────────────────┘
                       │
                       ▼
┌──────────────────────────────────────────────────┐
│    MODULE 2: PREPROCESSING                       │
│    src/preprocessing.py                          │
│    Null checks, deduplication, date features,    │
│    column clipping, type corrections             │
└──────────────────────┬───────────────────────────┘
                       │
                       ▼
┌──────────────────────────────────────────────────┐
│    MODULE 3: EDA                                 │
│    src/eda.py                                    │
│    Monthly trends, category analysis,            │
│    heatmaps, top products, holiday analysis      │
└──────────────────────┬───────────────────────────┘
                       │
                       ▼
┌──────────────────────────────────────────────────┐
│    MODULE 4: FEATURE ENGINEERING                 │
│    src/feature_engineering.py                    │
│    Lag features (1–4 weeks), rolling means       │
│    (2, 4, 8 weeks), label encoding               │
└──────────────────────┬───────────────────────────┘
                       │
                       ▼
┌──────────────────────────────────────────────────┐
│    MODULE 5: FORECASTING MODEL                   │
│    src/forecasting.py                            │
│    Linear Regression + Random Forest +           │
│    Gradient Boosting, time-based split           │
│    Metrics: MAE, RMSE, R²                        │
│    Best model saved as .pkl                      │
└──────────────────────┬───────────────────────────┘
                       │
                       ▼
┌──────────────────────────────────────────────────┐
│    MODULE 6: INVENTORY OPTIMIZATION              │
│    src/inventory_optimization.py                 │
│    Safety Stock = Z × σ × √Lead Time            │
│    Reorder Point = D̄ × L + Safety Stock         │
│    EOQ = √(2DS / H)                              │
│    Stockout risk alerts per product-store        │
└──────────────────────┬───────────────────────────┘
                       │
                       ▼
┌──────────────────────────────────────────────────┐
│    MODULE 7: BUSINESS INSIGHTS                   │
│    src/business_insights.py                      │
│    Year-over-year comparison chart,              │
│    summary KPIs, business_summary.csv            │
└──────────────────────┬───────────────────────────┘
                       │
                       ▼
┌──────────────────────────────────────────────────┐
│    MODULE 8: INTERACTIVE DASHBOARD               │
│    app/streamlit_app.py                          │
│    Streamlit + Plotly interactive charts,        │
│    store/category filters, reorder alerts        │
└──────────────────────┬───────────────────────────┘
                       │
                       ▼
┌──────────────────────────────────────────────────┐
│              OUTPUT LAYER                        │
│  📊 11 PNG Charts │ 📋 3 CSV Reports             │
│  🤖 Trained Model │ 🌐 Streamlit Dashboard       │
└──────────────────────────────────────────────────┘
```





## ⚙️ Installation

### Requirements
- Python 3.9 or higher
- pip package manager

### Step 1 — Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/Retail-Sales-Forecasting-Inventory-Optimization.git
cd Retail-Sales-Forecasting-Inventory-Optimization
```

### Step 2 — Create and activate virtual environment

**Windows (PowerShell):**
```powershell
python -m venv venv
venv\Scripts\activate
```

**Mac / Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### Step 3 — Install dependencies

```bash
pip install -r requirements.txt
```

### Step 4 — Verify installation

```bash
python -c "import pandas, numpy, sklearn, matplotlib, seaborn, streamlit, plotly; print('All libraries installed!')"
```

***

## 📊 Dataset Details

This project uses a **synthetically generated retail dataset** — no real company data required.

| Feature | Description | Example |
|---|---|---|
| `date` | Daily transaction date | 2021-01-01 |
| `store` | Store identifier | Store_A, Store_B, Store_C |
| `category` | Product category | Electronics, Groceries, Clothing, Sports |
| `product` | Individual product name | Laptop, Rice, T-Shirt |
| `units_sold` | Daily units sold | 42 |
| `unit_price` | Price per unit (₹) | 1903.97 |
| `revenue` | Total daily revenue | ₹78,637 |
| `discount_pct` | Discount applied (%) | 0, 5, 10, 15, 20 |
| `stock_level` | Available stock | 143 |
| `reorder_point` | Stock level that triggers reorder | 37 |
| `lead_time_days` | Days to receive new stock | 7 |

**Simulated patterns include:**
- 📈 Year-over-year growth trend (+5% per year)
- 🎆 Holiday season demand spikes (Oct–Jan: +40%)
- 📅 Weekend sales boost (+20%)
- 📦 Automatic restocking when stock < reorder point
- 🎲 Random demand noise (normal distribution)

***

## ▶️ How to Run

### Option 1: Run Full Pipeline (Recommended)

```bash
python main.py
```

This runs all 7 phases automatically:

```
[Phase 1] Generating Synthetic Dataset...
[Phase 2] Preprocessing & Cleaning...
[Phase 3] Exploratory Data Analysis...
[Phase 4] Feature Engineering...
[Phase 5] Forecasting Model Training...
[Phase 6] Inventory Optimization...
[Phase 7] Business Insights Summary...
```

### Option 2: Run Step by Step

```bash
python src/generate_dataset.py
python src/preprocessing.py
python src/eda.py
python src/feature_engineering.py
python src/forecasting.py
python src/inventory_optimization.py
python src/business_insights.py
```

### Option 3: Launch Interactive Dashboard

```bash
streamlit run app/streamlit_app.py
```

Open your browser at **http://localhost:8501**

***

## 🔄 Simulation Workflow

Since no real retail company data is used, here is how simulation works:

| Step | Action |
|---|---|
| **1** | Generate 3 years × 3 stores × 20 products = 65,700+ row dataset |
| **2** | Apply holiday seasonality (Oct–Jan: +40%), weekend boost (+20%), annual trend (+5%) |
| **3** | Add random noise to simulate real-world demand variation |
| **4** | Simulate stock depletion and automatic restocking events |
| **5** | Aggregate to weekly level, create lag and rolling features |
| **6** | Train ML models with time-based train/test split |
| **7** | Apply inventory formulas per product-store combination |
| **8** | Generate reorder alerts for at-risk products |
| **9** | Visualize all results in Streamlit dashboard |

***

## 📈 Results

| Metric | Value |
|---|---|
| Dataset Size | 65,700+ rows |
| Stores Covered | 3 |
| Products Covered | 20 |
| Categories | 4 |
| Time Period | 2021–2023 (3 years) |
| Best Forecast Model | Gradient Boosting Regressor |
| Model R² Score | 0.97 |
| Model MAE | ~22–23 units/week |
| Charts Generated | 11 PNG files |
| Reports Generated | 3 CSV files |
| Products Monitored | 60 (20 × 3 stores) |

***



## 🚀 Future Improvements

- [ ] Integrate **Facebook Prophet** for long-range time series forecasting
- [ ] Add **XGBoost** model for comparison
- [ ] Multi-region / multi-store forecasting with region as a feature
- [ ] **Price elasticity analysis** — measure how demand changes with price
- [ ] **Promotional impact modeling** — add is_promotion feature
- [ ] **Weather-based demand forecasting** via Open-Meteo API
- [ ] Real-time data pipeline with live database connection
- [ ] Automated email reorder alerts using smtplib
- [ ] Anomaly detection for unusual sales patterns (Isolation Forest)
- [ ] Integration with ERP / supply chain management systems
- [ ] Docker containerization for easy deployment
- [ ] LSTM / Deep Learning model for long-term patterns

***

## 🎓 Learning Outcomes

After completing this project, you will understand:

✅ End-to-end data science pipeline from raw data to deployed dashboard  
✅ Synthetic data generation with realistic business patterns  
✅ Data preprocessing and feature extraction from time-series data  
✅ Time-series feature engineering (lag features, rolling statistics)  
✅ Supervised ML regression modeling for demand forecasting  
✅ Time-based train/test split to avoid data leakage  
✅ Model evaluation using MAE, RMSE, and R² metrics  
✅ Inventory optimization formulas: Safety Stock, Reorder Point, EOQ  
✅ Business KPI calculation and reporting  
✅ Interactive dashboard development with Streamlit and Plotly  
✅ Professional project documentation and GitHub publishing  

***

## 🛠️ Troubleshooting

| Error | Fix |
|---|---|
| `ModuleNotFoundError: No module named 'src'` | Run `python main.py` from the project root folder |
| `OSError: Cannot save file into a non-existent directory` | Run `mkdir outputs outputs\charts outputs\reports data models` |
| `streamlit: Error: File does not exist` | Make sure `app/streamlit_app.py` exists |
| `FileNotFoundError: retail_sales_clean.csv` | Run phases in order — data files depend on previous steps |
| `streamlit: command not found` | Run `pip install streamlit` inside your virtual environment |

***
 👤 Author

Tanishq Jakate

🔗 LinkedIn Profile-(www.linkedin.com/in/tanishq-jakate-93617a402)  
💻 GitHub Profile-(tanishqcodes10)  



 ⭐ Show Your Support

If you found this project helpful, please give it a **⭐ star on GitHub**.  
It helps other students discover this project too!


