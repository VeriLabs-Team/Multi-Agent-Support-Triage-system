from graph_state import TriageState
from llm.clients import get_llm_client
from llm.prompts import TRIAGE_PROMPT

def triage_agent(state: TriageState) -> dict:
    client = get_llm_client()

    text = state["raw_text"]

    chain = TRIAGE_PROMPT | client
    
    response =chain.invoke(TRIAGE_PROMPT.format(raw_text=text))

    return {"intent": response.content}
