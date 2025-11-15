from graph_state import TriageState
import logging 

logger = logging.getLogger(__name__)

def final_formatter(state: TriageState) -> str:
    """
    This is the final node in the graph. It takes the complete state
    and formats a clean JSON output for the API.
    """
    logger.info("Formatting final output")

    # Get all the key data from the state
    intent = state.get("intent")
    order_id = state.get("extracted_data", {}).get("order_id")
    customer_email = state.get("extracted_data", {}).get("customer_email")
    final_reply = state.get("final_reply")

    # Handle the gneral inquiry case
    if intent == "general_inquiry":
        logger.info("Handling general inquiry")
        output = {
            "status": "Resolved",
            "intent": intent,
            "order_id": None,
            "customer_email": customer_email,
            "response_sent": final_reply
        }
    else:
        logger.info("Handling order-related inquiry")
        output = {
            "status": "Processed",
            "intent": intent,
            "order_id": order_id,
            "customer_email": customer_email,
            "enrichment_data": state.get("enrichment_data"), # attach enrichment data if any
            "response_sent": final_reply
        }

    return {"final_output": output }
