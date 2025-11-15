from typing import TypedDict, Optional, Dict, Any

class TriageState(TypedDict):
    """
    Represents the complete memory of our task.
    """
    # Input
    raw_text: str # The initial support email
    # Analysis
    intent: Optional[str] # The category (e.g., "Billing", "Order_Status")
    extracted_data: Optional[Dict[str, Any]] # JSON blob (e.g., {"order_id": "12345"})
    # Enrichment
    enrichment: Optional[Dict[str, Any]] # Data from our mock DBs (e.g., {"status": "Shipped"})
    # Output
    final_customer_reply: Optional[str] # The suggested reply for the human
    final_output: Optional[Dict[str, Any]] # The final, clean JSON for the API
