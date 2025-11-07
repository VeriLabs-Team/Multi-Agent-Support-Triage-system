from graph_state import TriageState
from app.services.order_service import get_order_status

def order_agent(state: TriageState) -> dict:
    """
    Order status specialist node. Retrieves order details from the CSV database.
    """
    # Extract order_id from the state
    order_id = state["extracted_data"]["order_id"]
    
    # Call the service to get order data
    data = get_order_status(order_id)
    
    # Handle errors
    if data is None:
        return {"enrichment": {"error": "Order record not found for this order ID."}}
    
    # Return the enrichment data
    return {"enrichment": data}
