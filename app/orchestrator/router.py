from graph_state import TriageState
import logging

# Set up logging
logger = logging.getLogger(__name__)

def orchestrator(state: TriageState) -> str:
    """
    This is the main "brain" of the agent. It reads the current state
    and decides which node to call next. This is a "Finite State Machine."

    It returns a string that is the "name" of the edge to follow.
    """
    # Check if we have an intent
    if state.get("intent") is None:
        logger.info("Decision: No intent found, calling triage.")
        return "call_triage"
    
    # Check the intent to decide next steps
    intent = state.get("intent")
    logger.info(f"state has intent: {intent}")
    
    # Is this a general inquiry if yes we don't need to extract data
    if intent.lower() == "general_inquiry":
        logger.info("Intent is general inquiry, skipping extraction.")
        return "call_response_agent"
    
    # For other intents, check for extracted data and enrichment
    if state.get("extracted_data") is None:
        logger.info("Decision: No extracted data, calling extraction.")
        return "call_extraction"
    
    # Check for enrichment next
    if state.get("enrichment") is None:
        logger.info("Decision: No enrichment found, calling enrichment.")

        intent_lower = intent.lower()
        if intent_lower in ["billing"]:
            logger.info("Intent is billing, providing billing information.")
            return "call_billing"
        elif intent_lower in ["order_status"]:
            logger.info("Intent is order status, providing order status information.")
            return "call_order"
        else:
            logger.warning(f"Unknown intent '{intent}' for enrichment.")
            return "call_response_agent"  # Fallback to response agent

    
    # Finally, if we have everything, go to the response agent
    if state.get("final_customer_reply") is None:
        logger.info("All necessary data present, calling response agent.")
        return "call_response_agent"

    # If we reach here, something is missing; default to response agent
    logger.warning("Decision: All steps complete. routing to finalize.")
    return "finalize"    