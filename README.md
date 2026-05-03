#  PhonePe Transaction Insights

> End-to-end data analysis and machine learning project on India's PhonePe digital payment ecosystem — from raw JSON extraction to an interactive Streamlit dashboard.

---

## 🗂️ Project Overview

This project analyzes the **PhonePe Pulse** open dataset covering 2018–2022 across all Indian states, districts, and pincodes. It extracts transaction, user, and insurance data from GitHub, stores it in a structured SQLite database, performs deep exploratory analysis, runs statistical hypothesis tests, and trains ML models to predict quarterly transaction volumes — all presented through an interactive Streamlit dashboard.

---

## 🚀 Tech Stack

![Python](https://img.shields.io/badge/Python-3.12-blue?logo=python)
![Streamlit](https://img.shields.io/badge/Streamlit-Dashboard-red?logo=streamlit)
![SQLite](https://img.shields.io/badge/SQLite-Database-lightgrey?logo=sqlite)
![Plotly](https://img.shields.io/badge/Plotly-Visualizations-3D4DB7?logo=plotly)
![XGBoost](https://img.shields.io/badge/XGBoost-ML_Model-orange)
![Pandas](https://img.shields.io/badge/Pandas-Data_Analysis-150458?logo=pandas)

---

## 📁 Repository Structure

```
PhonePe_transaction_insights/
│
├── notebooks/
│   └── Phonepe_transaction_insights.ipynb   # Full EDA + ML notebook
│
├── phonepe_pulse_data/
│   └── pulse/                               # Auto-cloned from PhonePe/pulse
│       └── data/
│           ├── aggregated/
│           │   ├── transaction/
│           │   ├── user/
│           │   └── insurance/
│           ├── map/
│           │   ├── transaction/
│           │   ├── user/
│           │   └── insurance/
│           └── top/
│               ├── transaction/
│               ├── user/
│               └── insurance/
│
├── scripts/
│   ├── database_setup.py     # Extracts JSON files → loads into SQLite DB
│   └── extraction.py         # JSON parsing and extraction helpers
│
├── sql_queries/
│   └── sql_queries.py        # 21 SQL queries covering all business cases
│
├── streamlit_dashboard/
│   └── dashboard.py          # Interactive Streamlit dashboard (7 pages)
│
├── phonepe.db                # SQLite database (auto-generated, gitignored)
└── README.md
```

---

## 🗄️ Database Schema

9 tables across 3 categories:

| Category | Tables |
|---|---|
| **Aggregated** | `aggregated_transaction`, `aggregated_user`, `aggregated_insurance` |
| **Map** | `map_transaction`, `map_user`, `map_insurance` |
| **Top** | `top_transaction`, `top_user`, `top_insurance` |

---

## 📊 Dashboard Pages

| Page | What's Inside |
|---|---|
| 🏠 Overview | KPI cards, yearly trend, transaction type donut, state bar chart |
| 📊 Transactions | Quarterly trends, type breakdown, state comparison |
| 🗺️ Map View | State/district rankings, India treemap |
| 👤 Users | Growth charts, engagement metrics, top districts |
| 🏆 Top Performers | Medal leaderboard for states, districts, pincodes |
| 🛡️ Insurance | Growth trends, penetration rate by state |
| 🔍 Business Insights | Segmentation, fraud proxy, growth rate, opportunity markets |

---

## 🤖 ML Models

| Model | R² | RMSE |
|---|---|---|
| Linear Regression | 0.74 | 2.8 Cr |
| Random Forest (tuned) | 0.89 | 1.5 Cr |
| **XGBoost (tuned) ✅** | **0.91** | **1.2 Cr** |

**Target**: Predict quarterly transaction amount per state  
**Best Model**: XGBoost Regressor with GridSearchCV hyperparameter tuning

---

## 🔬 Key Insights

- **Maharashtra, Karnataka & Telangana** account for ~40% of all transaction value
- **Q4 (Oct–Dec)** consistently peaks every year — driven by Diwali festive spending
- User registrations grew **10x from 2018 to 2022**, accelerated by COVID-19
- **Merchant payments** are growing in share — improving PhonePe's monetization
- **Gujarat & Rajasthan** lead insurance penetration; Karnataka is an untapped market

---

## ⚙️ Setup & Run

### 1. Clone this repo
```bash
git clone https://github.com/YourUsername/PhonePe_transaction_insights.git
cd PhonePe_transaction_insights
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Clone PhonePe Pulse data & build the database
```bash
git clone https://github.com/PhonePe/pulse.git phonepe_pulse_data/pulse
python scripts/database_setup.py
```

### 4. Launch the dashboard
```bash
streamlit run streamlit_dashboard/dashboard.py
```

### 5. Run SQL queries
```bash
python sql_queries/sql_queries.py
```

---

## 📦 Requirements

```
streamlit
plotly
pandas
numpy
matplotlib
seaborn
scipy
scikit-learn
xgboost
joblib
```

---

## 📄 Data Source

[PhonePe Pulse — Official GitHub Repository](https://github.com/PhonePe/pulse)

> PhonePe Pulse data is publicly available under the **Attribution Non-Commercial (CC BY-NC 4.0)** license.
