import os
import json
import sqlite3
import pandas as pd
from pathlib import Path


# ─────────────────────────────────────────────
#  CONFIG
# ─────────────────────────────────────────────
BASE_DIR   = Path(__file__).resolve().parent          # …/PhonePe_transaction_insights/scripts
ROOT_DIR   = BASE_DIR.parent                          # …/PhonePe_transaction_insights
DATA_DIR   = ROOT_DIR / "phonepe_pulse_data" / "pulse" / "data"
DB_PATH    = ROOT_DIR / "phonepe.db"


# ─────────────────────────────────────────────
#  HELPERS
# ─────────────────────────────────────────────
def open_json(path: Path) -> dict:
    with open(path, "r") as f:
        return json.load(f)

def get_conn() -> sqlite3.Connection:
    return sqlite3.connect(DB_PATH)


# ─────────────────────────────────────────────
#  1. AGGREGATED TABLES
# ─────────────────────────────────────────────
def extract_aggregated_transaction() -> pd.DataFrame:
    base = DATA_DIR / "aggregated" / "transaction" / "country" / "india" / "state"
    if not base.exists():
        print(f"  ⚠  Path not found: {base}")
        return pd.DataFrame()

    rows = []
    for state in os.listdir(base):
        for year in os.listdir(base / state):
            for file in os.listdir(base / state / year):
                if not file.endswith(".json"):
                    continue
                quarter = int(file.replace(".json", ""))
                data = open_json(base / state / year / file)
                for txn in data.get("data", {}).get("transactionData", []):
                    pi = txn["paymentInstruments"][0]
                    rows.append({
                        "State": state, "Year": int(year), "Quarter": quarter,
                        "Transaction_Type": txn["name"],
                        "Transaction_Count": pi["count"],
                        "Transaction_Amount": pi["amount"],
                    })
    return pd.DataFrame(rows)


def extract_aggregated_user() -> pd.DataFrame:
    base = DATA_DIR / "aggregated" / "user" / "country" / "india" / "state"
    if not base.exists():
        print(f"  ⚠  Path not found: {base}")
        return pd.DataFrame()

    rows = []
    for state in os.listdir(base):
        for year in os.listdir(base / state):
            for file in os.listdir(base / state / year):
                if not file.endswith(".json"):
                    continue
                quarter = int(file.replace(".json", ""))
                data = open_json(base / state / year / file)
                summary = data.get("data", {}).get("aggregated", {})
                rows.append({
                    "State": state, "Year": int(year), "Quarter": quarter,
                    "Registered_Users": summary.get("registeredUsers", 0),
                    "App_Opens": summary.get("appOpens", 0),
                })
                # per-brand breakdown
                for brand in data.get("data", {}).get("usersByDevice", []) or []:
                    rows.append({
                        "State": state, "Year": int(year), "Quarter": quarter,
                        "Brand": brand["brand"],
                        "Count": brand["count"],
                        "Percentage": brand["percentage"],
                    })
    return pd.DataFrame(rows)


def extract_aggregated_insurance() -> pd.DataFrame:
    base = DATA_DIR / "aggregated" / "insurance" / "country" / "india" / "state"
    if not base.exists():
        print(f"  ⚠  Path not found: {base}")
        return pd.DataFrame()

    rows = []
    for state in os.listdir(base):
        for year in os.listdir(base / state):
            for file in os.listdir(base / state / year):
                if not file.endswith(".json"):
                    continue
                quarter = int(file.replace(".json", ""))
                data = open_json(base / state / year / file)
                for txn in data.get("data", {}).get("transactionData", []):
                    pi = txn["paymentInstruments"][0]
                    rows.append({
                        "State": state, "Year": int(year), "Quarter": quarter,
                        "Insurance_Type": txn["name"],
                        "Insurance_Count": pi["count"],
                        "Insurance_Amount": pi["amount"],
                    })
    return pd.DataFrame(rows)


# ─────────────────────────────────────────────
#  2. MAP TABLES
# ─────────────────────────────────────────────
def extract_map_transaction() -> pd.DataFrame:
    base = DATA_DIR / "map" / "transaction" / "hover" / "country" / "india" / "state"
    if not base.exists():
        print(f"  ⚠  Path not found: {base}")
        return pd.DataFrame()

    rows = []
    for state in os.listdir(base):
        for year in os.listdir(base / state):
            for file in os.listdir(base / state / year):
                if not file.endswith(".json"):
                    continue
                quarter = int(file.replace(".json", ""))
                data = open_json(base / state / year / file)
                for district in data.get("data", {}).get("hoverDataList", []):
                    metric = district.get("metric", [{}])[0]
                    rows.append({
                        "State": state, "Year": int(year), "Quarter": quarter,
                        "District": district["name"],
                        "Transaction_Count": metric.get("count", 0),
                        "Transaction_Amount": metric.get("amount", 0),
                    })
    return pd.DataFrame(rows)


def extract_map_user() -> pd.DataFrame:
    base = DATA_DIR / "map" / "user" / "hover" / "country" / "india" / "state"
    if not base.exists():
        print(f"  ⚠  Path not found: {base}")
        return pd.DataFrame()

    rows = []
    for state in os.listdir(base):
        for year in os.listdir(base / state):
            for file in os.listdir(base / state / year):
                if not file.endswith(".json"):
                    continue
                quarter = int(file.replace(".json", ""))
                data = open_json(base / state / year / file)
                for district in data.get("data", {}).get("hoverData", {}).items():
                    name, info = district
                    rows.append({
                        "State": state, "Year": int(year), "Quarter": quarter,
                        "District": name,
                        "Registered_Users": info.get("registeredUsers", 0),
                        "App_Opens": info.get("appOpens", 0),
                    })
    return pd.DataFrame(rows)


def extract_map_insurance() -> pd.DataFrame:
    base = DATA_DIR / "map" / "insurance" / "hover" / "country" / "india" / "state"
    if not base.exists():
        print(f"  ⚠  Path not found: {base}")
        return pd.DataFrame()

    rows = []
    for state in os.listdir(base):
        for year in os.listdir(base / state):
            for file in os.listdir(base / state / year):
                if not file.endswith(".json"):
                    continue
                quarter = int(file.replace(".json", ""))
                data = open_json(base / state / year / file)
                for district in data.get("data", {}).get("hoverDataList", []):
                    metric = district.get("metric", [{}])[0]
                    rows.append({
                        "State": state, "Year": int(year), "Quarter": quarter,
                        "District": district["name"],
                        "Insurance_Count": metric.get("count", 0),
                        "Insurance_Amount": metric.get("amount", 0),
                    })
    return pd.DataFrame(rows)


# ─────────────────────────────────────────────
#  3. TOP TABLES
# ─────────────────────────────────────────────
def extract_top_transaction() -> pd.DataFrame:
    base = DATA_DIR / "top" / "transaction" / "country" / "india" / "state"
    if not base.exists():
        print(f"  ⚠  Path not found: {base}")
        return pd.DataFrame()

    rows = []
    for state in os.listdir(base):
        for year in os.listdir(base / state):
            for file in os.listdir(base / state / year):
                if not file.endswith(".json"):
                    continue
                quarter = int(file.replace(".json", ""))
                data = open_json(base / state / year / file)
                for entry in data.get("data", {}).get("pincodes", []):
                    rows.append({
                        "State": state, "Year": int(year), "Quarter": quarter,
                        "Pincode": entry["entityName"],
                        "Transaction_Count": entry["metric"]["count"],
                        "Transaction_Amount": entry["metric"]["amount"],
                    })
    return pd.DataFrame(rows)


def extract_top_user() -> pd.DataFrame:
    base = DATA_DIR / "top" / "user" / "country" / "india" / "state"
    if not base.exists():
        print(f"  ⚠  Path not found: {base}")
        return pd.DataFrame()

    rows = []
    for state in os.listdir(base):
        for year in os.listdir(base / state):
            for file in os.listdir(base / state / year):
                if not file.endswith(".json"):
                    continue
                quarter = int(file.replace(".json", ""))
                data = open_json(base / state / year / file)
                for entry in data.get("data", {}).get("pincodes", []):
                    rows.append({
                        "State": state, "Year": int(year), "Quarter": quarter,
                        "Pincode": entry["name"],
                        "Registered_Users": entry["registeredUsers"],
                    })
    return pd.DataFrame(rows)


def extract_top_insurance() -> pd.DataFrame:
    base = DATA_DIR / "top" / "insurance" / "country" / "india" / "state"
    if not base.exists():
        print(f"  ⚠  Path not found: {base}")
        return pd.DataFrame()

    rows = []
    for state in os.listdir(base):
        for year in os.listdir(base / state):
            for file in os.listdir(base / state / year):
                if not file.endswith(".json"):
                    continue
                quarter = int(file.replace(".json", ""))
                data = open_json(base / state / year / file)
                for entry in data.get("data", {}).get("pincodes", []):
                    rows.append({
                        "State": state, "Year": int(year), "Quarter": quarter,
                        "Pincode": entry["entityName"],
                        "Insurance_Count": entry["metric"]["count"],
                        "Insurance_Amount": entry["metric"]["amount"],
                    })
    return pd.DataFrame(rows)


# ─────────────────────────────────────────────
#  4. LOAD ALL INTO SQLite
# ─────────────────────────────────────────────
TABLES = {
    # table_name                : extractor function
    "aggregated_transaction"    : extract_aggregated_transaction,
    "aggregated_user"           : extract_aggregated_user,
    "aggregated_insurance"      : extract_aggregated_insurance,
    "map_transaction"           : extract_map_transaction,
    "map_user"                  : extract_map_user,
    "map_insurance"             : extract_map_insurance,
    "top_transaction"           : extract_top_transaction,
    "top_user"                  : extract_top_user,
    "top_insurance"             : extract_top_insurance,
}

def setup_database():
    print(f"\n📂  Data source : {DATA_DIR}")
    print(f"🗄   Database    : {DB_PATH}\n")

    if not DATA_DIR.exists():
        print("❌  DATA_DIR does not exist. Did the repo clone correctly?")
        print(f"    Expected: {DATA_DIR}")
        return

    conn = get_conn()

    for table_name, extractor in TABLES.items():
        print(f"⏳  Extracting  → {table_name} …", end=" ", flush=True)
        df = extractor()
        if df.empty:
            print("⚠   No data extracted — skipped.")
            continue
        df.to_sql(table_name, conn, if_exists="replace", index=False)
        print(f"✅  {len(df):,} rows saved.")

    conn.close()
    print(f"\n🎉  All done! Database ready at: {DB_PATH}")


if __name__ == "__main__":
    setup_database()