from graph_state import TriageState
from llm.clients import get_llm_client
from llm.prompts import EXTRACTOR_PROMPT
from pydantic import BaseModel

class SchemaForExtraction(BaseModel):
    intent: str

def extractor_agent(state: TriageState) -> dict:
    
    client = get_llm_client().with_structured_output(SchemaForExtraction)

    text = state["raw_text"]

    response = client.invoke(EXTRACTOR_PROMPT.format(raw_text=text))

    return {"extracted_data": response.model_dump()}    #didnt use response.dict() because thats in pydantic v1 not v2