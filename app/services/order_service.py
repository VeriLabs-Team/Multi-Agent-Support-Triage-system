import pandas as pd
from pathlib import Path

def get_order_status(order_id: str) -> dict | None:
    """
    Retrieves order status for a given order ID from the orders CSV file.
    """
    orders_csv_path = Path(__file__).parent.parent.parent / "data" / "orders.csv"
    df = pd.read_csv(orders_csv_path)
    record = df[df['order_id'] == int(order_id)]
    if record.empty:
        return None
    return record.to_dict('records')[0]
