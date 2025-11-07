from graph_state import TriageState
from app.services.billing_service import get_billing_details

def billing_agent(state: TriageState) -> dict:
    """
    Billing specialist node. Retrieves billing details from the CSV database.
    """
    # Extract order_id from the state
    order_id = state["extracted_data"]["order_id"]
    
    # Call the service to get billing data
    data = get_billing_details(order_id)
    
    # Handle errors
    if data is None:
        return {"enrichment": {"error": "Billing record not found for this order ID."}}
    
    # Return the enrichment data
    return {"enrichment": data}
