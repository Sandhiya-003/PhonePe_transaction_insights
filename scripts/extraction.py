import os
import json
import pandas as pd

def extract_aggregated_transaction(data_folder):
    """
    Extract aggregated transaction data from PhonePe Pulse JSON files.
    data_folder should point to the 'data' directory inside the cloned repo.
    """
    transaction_path = os.path.join(
        data_folder, "aggregated", "transaction", "country", "india", "state"
    )

    if not os.path.exists(transaction_path):
        print(f"❌ Could not find the transaction folder inside {data_folder}")
        print(f"   Looked at: {transaction_path}")
        return pd.DataFrame()

    records = []

    for state in os.listdir(transaction_path):
        state_path = os.path.join(transaction_path, state)
        if not os.path.isdir(state_path):
            continue
        for year in os.listdir(state_path):
            year_path = os.path.join(state_path, year)
            if not os.path.isdir(year_path):
                continue
            for file in os.listdir(year_path):
                if not file.endswith(".json"):
                    continue
                quarter = int(file.replace(".json", ""))
                file_path = os.path.join(year_path, file)
                with open(file_path, "r") as f:
                    data = json.load(f)

                transactions = data.get("data", {}).get("transactionData", [])
                for txn in transactions:
                    records.append({
                        "State": state,
                        "Year": int(year),
                        "Quarter": quarter,
                        "Transaction_Type": txn["name"],
                        "Transaction_Count": txn["paymentInstruments"][0]["count"],
                        "Transaction_Amount": txn["paymentInstruments"][0]["amount"],
                    })

    return pd.DataFrame(records)