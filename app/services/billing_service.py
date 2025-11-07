import pandas as pd
from pathlib import Path

def get_billing_details(order_id: str) -> dict | None:
    """
    Retrieves billing details for a given order ID from the billing CSV file.
    """
    billing_csv_path = Path(__file__).parent.parent.parent / "data" / "billing.csv"
    df = pd.read_csv(billing_csv_path)
    record = df[df['order_id'] == int(order_id)]
    if record.empty:
        return None
    return record.to_dict('records')[0]
