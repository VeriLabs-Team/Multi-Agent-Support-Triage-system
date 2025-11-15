from graph_state import TriageState
from ..llm.clients import get_llm_client
from ..llm.prompts import EXTRACTOR_PROMPT
from pydantic import BaseModel
from typing import Optional

class SchemaForExtraction(BaseModel):
    order_id: Optional[str] = None
    customer_email: Optional[str] = None
    item_name: Optional[str] = None

def extractor_agent(state: TriageState) -> dict:
    client = get_llm_client()
    
    text = state["raw_text"]
    
    # Chain with structured output
    chain = EXTRACTOR_PROMPT | client.with_structured_output(SchemaForExtraction)
    
    response = chain.invoke({"raw_text": text})
    
    return {"extracted_data": response.model_dump()}
