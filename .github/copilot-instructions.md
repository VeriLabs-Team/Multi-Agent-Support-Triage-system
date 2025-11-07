# Copilot Instructions for the Multi-Agent Triage System

This document provides guidance for AI coding agents to effectively contribute to this project.

## 1. The "Big Picture": Supervisor/Worker Architecture

This project implements a multi-agent AI system for triaging customer support tickets using a **Supervisor/Worker** model built with **LangGraph**.

- **Orchestrator (Supervisor):** The central agent that manages the workflow. It inspects the current state of a ticket and decides which "worker" agent to dispatch next. This logic is in `app/orchestrator/router.py`.
- **Worker Agents:** These are specialized, single-purpose agents that perform specific tasks like classifying intent, extracting data, or fetching information from a database. They are located in the `app/nodes/` directory.
- **Stateful Workflow:** The entire process is a stateful loop. Workers update a central `TriageState` object, and the Orchestrator reads this state to make its next decision. This cycle continues until the ticket is fully processed.

## 2. Core Concept: The `TriageState` Object

The `TriageState` is the single source of truth for a ticket's journey through the system. It's a `TypedDict` defined in `graph_state.py`. All agents read from and write to this object. Understanding its structure is critical.

```python
# graph_state.py
from typing import TypedDict, Optional, Dict, Any

class TriageState(TypedDict):
    # Input
    raw_text: str
    # Analysis
    intent: Optional[str]
    extracted_data: Optional[Dict[str, Any]]
    # Enrichment
    enrichment: Optional[Dict[str, Any]]
    # Output
    draft_reply: Optional[str]
    final_output: Optional[Dict[str, Any]]
```

- **Always check the `TriageState`** to understand what information is available before implementing a new step.
- **Update the state immutably** by returning a dictionary with the fields you want to change. LangGraph handles the update.

## 3. Key Files and Directories

- **`workflow.py`**: This is where the LangGraph graph is defined and all the nodes (agents) are wired together.
- **`main.py`**: The FastAPI application that serves the final graph as an API endpoint.
- **`graph_state.py`**: Defines the central `TriageState` TypedDict.
- **`app/orchestrator/router.py`**: Contains the core routing logic for the supervisor agent.
- **`app/nodes/`**: Home to all worker agents (e.g., `triage_node.py`, `billing_node.py`).
- **`app/services/`**: Contains business logic that is independent of the graph, like functions to read from CSV files (e.g., `billing_service.py`).
- **`app/llm/`**: Manages AI model clients (`clients.py`) and prompts (`prompts.py`).

## 4. Developer Workflow & Conventions

### Building and Running
1.  **Install dependencies:** `pip install -r requirements.txt`
2.  **Run the application:** `uvicorn main:app --reload`

### Agent Implementation Pattern
- **Nodes (`app/nodes/`)** are the graph workers. They should:
    1.  Take `state: TriageState` as input.
    2.  Perform **one specific job**.
    3.  Return a dictionary to update the `TriageState`.
    4.  For database/service lookups, they call functions from `app/services/`.

    *Example: `billing_node.py`*
    ```python
    from graph_state import TriageState
    from app.services.billing_service import get_billing_details

    def billing_agent(state: TriageState) -> dict:
        order_id = state["extracted_data"]["order_id"]
        data = get_billing_details(order_id)
        if data is None:
            return {"enrichment": {"error": "Billing record not found."}}
        return {"enrichment": data}
    ```

### Service Implementation Pattern
- **Services (`app/services/`)** contain reusable business logic. They should **not** be aware of the `TriageState` or the graph. They are pure functions that take simple inputs and return data.

    *Example: `billing_service.py`*
    ```python
    import pandas as pd

    def get_billing_details(order_id: str) -> dict | None:
        df = pd.read_csv("data/billing.csv")
        record = df[df['order_id'] == order_id]
        if record.empty:
            return None
        return record.to_dict('records')[0]
    ```

## 5. External Dependencies and Integration Points

- **LangGraph:** The core orchestration framework. Key concepts are `StatefulGraph`, `add_node`, `add_edge`, and `add_conditional_edges`.
- **LLMs (via Ollama/Groq):** The AI models are accessed through a centralized `get_llm_client()` function in `app/llm/clients.py`. Prompts are stored in `app/llm/prompts.py`.
- **Data Stores:** Mock databases are simple CSV files in the `data/` directory, accessed via `pandas` in the `app/services/` modules.
- **FastAPI:** Used to expose the final, compiled graph as a web endpoint in `main.py`.
