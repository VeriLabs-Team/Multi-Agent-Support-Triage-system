from graph_state import TriageState
from ..llm.clients import get_llm_client
from ..llm.prompts import RESPONSE_PROMPT

def response_agent(state: TriageState) -> dict:

    client=get_llm_client() 

    chain=RESPONSE_PROMPT | client

    prompt_values=state.copy()

    if "enrichment" not in prompt_values or prompt_values["enrichment"] is None:
        prompt_values["enrichment"] = "No additional context or enrichment was found."

    response =chain.invoke(prompt_values)    
     
    return {"final_customer_reply": response.content}



