import sqlite3
import pandas as pd
from pathlib import Path

# ─────────────────────────────────────────────
#  CONFIG
# ─────────────────────────────────────────────
ROOT_DIR = Path(__file__).resolve().parent.parent
DB_PATH  = ROOT_DIR / "phonepe.db"

def run_query(query: str, label: str = "") -> pd.DataFrame:
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query(query, conn)
    conn.close()
    if label:
        print(f"\n{'='*60}")
        print(f"  {label}")
        print(f"{'='*60}")
        print(df.to_string(index=False))
    return df


# ══════════════════════════════════════════════════════════════
#  1. TRANSACTION QUERIES
# ══════════════════════════════════════════════════════════════

# Q1 — Top 10 states by total transaction amount
Q1_top_states_by_amount = """
    SELECT
        State,
        ROUND(SUM(Transaction_Amount) / 1e9, 2)  AS Total_Amount_Billion,
        SUM(Transaction_Count)                    AS Total_Transactions
    FROM aggregated_transaction
    GROUP BY State
    ORDER BY Total_Amount_Billion DESC
    LIMIT 10;
"""

# Q2 — Most popular transaction type overall
Q2_popular_transaction_type = """
    SELECT
        Transaction_Type,
        SUM(Transaction_Count)                    AS Total_Count,
        ROUND(SUM(Transaction_Amount) / 1e9, 2)  AS Total_Amount_Billion,
        ROUND(SUM(Transaction_Count) * 100.0 /
              (SELECT SUM(Transaction_Count) FROM aggregated_transaction), 2) AS Percentage
    FROM aggregated_transaction
    GROUP BY Transaction_Type
    ORDER BY Total_Count DESC;
"""

# Q3 — Year-wise transaction trend
Q3_yearly_trend = """
    SELECT
        Year,
        SUM(Transaction_Count)                    AS Total_Transactions,
        ROUND(SUM(Transaction_Amount) / 1e9, 2)  AS Total_Amount_Billion,
        ROUND(AVG(Transaction_Amount), 2)         AS Avg_Transaction_Value
    FROM aggregated_transaction
    GROUP BY Year
    ORDER BY Year;
"""

# Q4 — Quarter-wise performance (all years combined)
Q4_quarterly_performance = """
    SELECT
        Quarter,
        SUM(Transaction_Count)                    AS Total_Transactions,
        ROUND(SUM(Transaction_Amount) / 1e9, 2)  AS Total_Amount_Billion
    FROM aggregated_transaction
    GROUP BY Quarter
    ORDER BY Quarter;
"""

# Q5 — Top 10 districts by transaction amount (map table)
Q5_top_districts = """
    SELECT
        State,
        District,
        SUM(Transaction_Count)                    AS Total_Transactions,
        ROUND(SUM(Transaction_Amount) / 1e9, 2)  AS Total_Amount_Billion
    FROM map_transaction
    GROUP BY State, District
    ORDER BY Total_Amount_Billion DESC
    LIMIT 10;
"""

# Q6 — Top 10 pincodes by transaction amount
Q6_top_pincodes_transaction = """
    SELECT
        State,
        Pincode,
        SUM(Transaction_Count)                    AS Total_Transactions,
        ROUND(SUM(Transaction_Amount) / 1e9, 2)  AS Total_Amount_Billion
    FROM top_transaction
    GROUP BY State, Pincode
    ORDER BY Total_Amount_Billion DESC
    LIMIT 10;
"""

# Q7 — Average transaction value per state
Q7_avg_transaction_value = """
    SELECT
        State,
        ROUND(SUM(Transaction_Amount) / NULLIF(SUM(Transaction_Count), 0), 2) AS Avg_Transaction_Value,
        SUM(Transaction_Count) AS Total_Transactions
    FROM aggregated_transaction
    GROUP BY State
    ORDER BY Avg_Transaction_Value DESC
    LIMIT 10;
"""

# Q8 — Transaction type breakdown per year
Q8_type_by_year = """
    SELECT
        Year,
        Transaction_Type,
        SUM(Transaction_Count)                    AS Total_Count,
        ROUND(SUM(Transaction_Amount) / 1e9, 2)  AS Total_Amount_Billion
    FROM aggregated_transaction
    GROUP BY Year, Transaction_Type
    ORDER BY Year, Total_Count DESC;
"""


# ══════════════════════════════════════════════════════════════
#  2. USER QUERIES
# ══════════════════════════════════════════════════════════════

# Q9 — Top 10 states by registered users
Q9_top_states_users = """
    SELECT
        State,
        SUM(Registered_Users) AS Total_Registered_Users,
        SUM(App_Opens)        AS Total_App_Opens
    FROM aggregated_user
    GROUP BY State
    ORDER BY Total_Registered_Users DESC
    LIMIT 10;
"""

# Q10 — Year-wise user growth
Q10_user_growth = """
    SELECT
        Year,
        SUM(Registered_Users) AS Total_Registered_Users,
        SUM(App_Opens)        AS Total_App_Opens,
        ROUND(SUM(App_Opens) * 1.0 / NULLIF(SUM(Registered_Users), 0), 2) AS App_Opens_Per_User
    FROM aggregated_user
    GROUP BY Year
    ORDER BY Year;
"""

# Q11 — Top 10 pincodes by registered users
Q11_top_pincodes_users = """
    SELECT
        State,
        Pincode,
        SUM(Registered_Users) AS Total_Registered_Users
    FROM top_user
    GROUP BY State, Pincode
    ORDER BY Total_Registered_Users DESC
    LIMIT 10;
"""

# Q12 — Top 10 districts by registered users (map table)
Q12_top_districts_users = """
    SELECT
        State,
        District,
        SUM(Registered_Users) AS Total_Registered_Users,
        SUM(App_Opens)        AS Total_App_Opens
    FROM map_user
    GROUP BY State, District
    ORDER BY Total_Registered_Users DESC
    LIMIT 10;
"""

# Q13 — Quarter-wise user engagement
Q13_quarterly_users = """
    SELECT
        Quarter,
        SUM(Registered_Users) AS Total_Registered_Users,
        SUM(App_Opens)        AS Total_App_Opens
    FROM aggregated_user
    GROUP BY Quarter
    ORDER BY Quarter;
"""


# ══════════════════════════════════════════════════════════════
#  3. INSURANCE QUERIES
# ══════════════════════════════════════════════════════════════

# Q14 — Top 10 states by insurance amount
Q14_top_states_insurance = """
    SELECT
        State,
        ROUND(SUM(Insurance_Amount) / 1e9, 2)  AS Total_Insurance_Billion,
        SUM(Insurance_Count)                    AS Total_Policies
    FROM aggregated_insurance
    GROUP BY State
    ORDER BY Total_Insurance_Billion DESC
    LIMIT 10;
"""

# Q15 — Insurance growth year over year
Q15_insurance_growth = """
    SELECT
        Year,
        SUM(Insurance_Count)                    AS Total_Policies,
        ROUND(SUM(Insurance_Amount) / 1e9, 2)  AS Total_Amount_Billion
    FROM aggregated_insurance
    GROUP BY Year
    ORDER BY Year;
"""

# Q16 — Top 10 districts by insurance amount
Q16_top_districts_insurance = """
    SELECT
        State,
        District,
        SUM(Insurance_Count)                    AS Total_Policies,
        ROUND(SUM(Insurance_Amount) / 1e9, 2)  AS Total_Amount_Billion
    FROM map_insurance
    GROUP BY State, District
    ORDER BY Total_Amount_Billion DESC
    LIMIT 10;
"""

# Q17 — Insurance penetration rate (insurance vs total transactions per state)
Q17_insurance_penetration = """
    SELECT
        i.State,
        SUM(i.Insurance_Count)      AS Insurance_Policies,
        SUM(t.Transaction_Count)    AS Total_Transactions,
        ROUND(SUM(i.Insurance_Count) * 100.0 /
              NULLIF(SUM(t.Transaction_Count), 0), 4) AS Penetration_Rate_Pct
    FROM aggregated_insurance i
    JOIN aggregated_transaction t
        ON i.State = t.State AND i.Year = t.Year AND i.Quarter = t.Quarter
    GROUP BY i.State
    ORDER BY Penetration_Rate_Pct DESC
    LIMIT 10;
"""


# ══════════════════════════════════════════════════════════════
#  4. BUSINESS CASE QUERIES
# ══════════════════════════════════════════════════════════════

# Q18 — Customer segmentation: high vs low value states
Q18_customer_segmentation = """
    SELECT
        State,
        ROUND(SUM(Transaction_Amount) / NULLIF(SUM(Transaction_Count), 0), 2) AS Avg_Txn_Value,
        SUM(Transaction_Count) AS Total_Transactions,
        CASE
            WHEN SUM(Transaction_Amount) / NULLIF(SUM(Transaction_Count), 0) > 5000 THEN 'High Value'
            WHEN SUM(Transaction_Amount) / NULLIF(SUM(Transaction_Count), 0) > 1000 THEN 'Mid Value'
            ELSE 'Low Value'
        END AS Segment
    FROM aggregated_transaction
    GROUP BY State
    ORDER BY Avg_Txn_Value DESC;
"""

# Q19 — Fraud detection proxy: states with abnormally high avg transaction
Q19_fraud_proxy = """
    SELECT
        State,
        Year,
        Quarter,
        Transaction_Type,
        ROUND(Transaction_Amount / NULLIF(Transaction_Count, 0), 2) AS Avg_Txn_Value
    FROM aggregated_transaction
    WHERE (Transaction_Amount / NULLIF(Transaction_Count, 0)) >
          (SELECT AVG(Transaction_Amount / NULLIF(Transaction_Count, 0)) * 3
           FROM aggregated_transaction)
    ORDER BY Avg_Txn_Value DESC
    LIMIT 20;
"""

# Q20 — Competitive benchmarking: bottom 10 states (opportunity markets)
Q20_bottom_states = """
    SELECT
        State,
        SUM(Transaction_Count)                    AS Total_Transactions,
        ROUND(SUM(Transaction_Amount) / 1e6, 2)  AS Total_Amount_Million,
        SUM(u.Registered_Users)                   AS Registered_Users
    FROM aggregated_transaction t
    LEFT JOIN aggregated_user u USING (State, Year, Quarter)
    GROUP BY State
    ORDER BY Total_Transactions ASC
    LIMIT 10;
"""

# Q21 — Payment performance: growth rate of each transaction type
Q21_payment_growth = """
    SELECT
        Transaction_Type,
        SUM(CASE WHEN Year = (SELECT MIN(Year) FROM aggregated_transaction) THEN Transaction_Count ELSE 0 END) AS Count_First_Year,
        SUM(CASE WHEN Year = (SELECT MAX(Year) FROM aggregated_transaction) THEN Transaction_Count ELSE 0 END) AS Count_Last_Year,
        ROUND(
            (SUM(CASE WHEN Year = (SELECT MAX(Year) FROM aggregated_transaction) THEN Transaction_Count ELSE 0 END) -
             SUM(CASE WHEN Year = (SELECT MIN(Year) FROM aggregated_transaction) THEN Transaction_Count ELSE 0 END))
            * 100.0 /
            NULLIF(SUM(CASE WHEN Year = (SELECT MIN(Year) FROM aggregated_transaction) THEN Transaction_Count ELSE 0 END), 0)
        , 2) AS Growth_Rate_Pct
    FROM aggregated_transaction
    GROUP BY Transaction_Type
    ORDER BY Growth_Rate_Pct DESC;
"""


# ══════════════════════════════════════════════════════════════
#  5. RUNNER — prints all query results to console
# ══════════════════════════════════════════════════════════════
ALL_QUERIES = {
    # Transactions
    "Q1  Top 10 States by Amount"           : Q1_top_states_by_amount,
    "Q2  Popular Transaction Types"         : Q2_popular_transaction_type,
    "Q3  Yearly Transaction Trend"          : Q3_yearly_trend,
    "Q4  Quarterly Performance"             : Q4_quarterly_performance,
    "Q5  Top 10 Districts by Amount"        : Q5_top_districts,
    "Q6  Top 10 Pincodes by Amount"         : Q6_top_pincodes_transaction,
    "Q7  Avg Transaction Value per State"   : Q7_avg_transaction_value,
    "Q8  Transaction Type by Year"          : Q8_type_by_year,
    # Users
    "Q9  Top 10 States by Users"            : Q9_top_states_users,
    "Q10 User Growth Year-over-Year"        : Q10_user_growth,
    "Q11 Top 10 Pincodes by Users"          : Q11_top_pincodes_users,
    "Q12 Top 10 Districts by Users"         : Q12_top_districts_users,
    "Q13 Quarterly User Engagement"         : Q13_quarterly_users,
    # Insurance
    "Q14 Top 10 States by Insurance"        : Q14_top_states_insurance,
    "Q15 Insurance Growth Year-over-Year"   : Q15_insurance_growth,
    "Q16 Top 10 Districts by Insurance"     : Q16_top_districts_insurance,
    "Q17 Insurance Penetration by State"    : Q17_insurance_penetration,
    # Business Cases
    "Q18 Customer Segmentation"             : Q18_customer_segmentation,
    "Q19 Fraud Detection Proxy"             : Q19_fraud_proxy,
    "Q20 Bottom States (Opportunity)"       : Q20_bottom_states,
    "Q21 Payment Type Growth Rate"          : Q21_payment_growth,
}

def run_all():
    print(f"\n🗄  Connected to: {DB_PATH}")
    for label, query in ALL_QUERIES.items():
        try:
            run_query(query, label)
        except Exception as e:
            print(f"\n⚠  {label} failed: {e}")
    print("\n✅  All queries done.")

# individual getters for Streamlit dashboard use
def get_top_states_by_amount():        return run_query(Q1_top_states_by_amount)
def get_popular_transaction_types():   return run_query(Q2_popular_transaction_type)
def get_yearly_trend():                return run_query(Q3_yearly_trend)
def get_quarterly_performance():       return run_query(Q4_quarterly_performance)
def get_top_districts():               return run_query(Q5_top_districts)
def get_top_pincodes_transaction():    return run_query(Q6_top_pincodes_transaction)
def get_avg_transaction_value():       return run_query(Q7_avg_transaction_value)
def get_type_by_year():                return run_query(Q8_type_by_year)
def get_top_states_users():            return run_query(Q9_top_states_users)
def get_user_growth():                 return run_query(Q10_user_growth)
def get_top_pincodes_users():          return run_query(Q11_top_pincodes_users)
def get_top_districts_users():         return run_query(Q12_top_districts_users)
def get_quarterly_users():             return run_query(Q13_quarterly_users)
def get_top_states_insurance():        return run_query(Q14_top_states_insurance)
def get_insurance_growth():            return run_query(Q15_insurance_growth)
def get_top_districts_insurance():     return run_query(Q16_top_districts_insurance)
def get_insurance_penetration():       return run_query(Q17_insurance_penetration)
def get_customer_segmentation():       return run_query(Q18_customer_segmentation)
def get_fraud_proxy():                 return run_query(Q19_fraud_proxy)
def get_bottom_states():               return run_query(Q20_bottom_states)
def get_payment_growth():              return run_query(Q21_payment_growth)


if __name__ == "__main__":
    run_all()
