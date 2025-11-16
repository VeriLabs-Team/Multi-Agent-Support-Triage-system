# Multi-Agent Support Ticket Triage System

This project implements a sophisticated multi-agent system using Python, LangGraph, and FastAPI to automate the processing of customer support tickets. The system can understand, classify, enrich, and respond to customer inquiries in a structured and intelligent manner.

## ✨ Features

-   **Automated Triage**: Automatically classifies incoming tickets into categories like 'Billing', 'Order_Status', 'Tech_Support', or 'General_Inquiry'.
-   **Information Extraction**: Intelligently extracts key information from the ticket text, such as `order_id` and `customer_email`.
-   **Data Enrichment**: Fetches additional context from internal data sources (e.g., CSV files for billing and order details) to provide agents with all necessary information.
-   **Dynamic Routing**: An orchestrator agent dynamically routes the ticket through the workflow based on its current state and intent.
-   **Empathetic Response Generation**: A dedicated agent crafts a helpful and context-aware response for the customer.
-   **API-Driven**: The entire workflow is exposed via a FastAPI endpoint for easy integration with other services.

## 🏛️ Architecture Overview

The system is built as a stateful graph using LangGraph. Each node in the graph represents a specialized agent or a tool.

1.  **API Input**: A raw support email text is sent to the FastAPI endpoint.
2.  **Orchestrator**: The central "brain" that directs the workflow. It first routes the ticket to the Triage Agent.
3.  **Triage Agent**: Classifies the primary intent of the ticket.
4.  **Orchestrator**: Based on the intent, it decides the next step. If the intent is technical, it may require data extraction.
5.  **Extractor Agent**: If needed, this agent extracts structured data (like an order ID) from the text.
6.  **Orchestrator**: Routes to the appropriate tool-using agent.
7.  **Tool Agents (`billing_agent`, `order_agent`)**: These agents use the extracted data to look up details in internal databases (simulated with CSV files). The result is added to the state as "enrichment".
8.  **Orchestrator**: Once all necessary information is gathered, it routes to the Response Agent.
9.  **Response Agent**: Generates a comprehensive and empathetic email reply for the customer using the original message and all enriched data.
10. **Final Formatter**: Prepares the final JSON output for the API.

This cyclical process allows the system to handle complex queries by looping back to the orchestrator to decide the next logical step, ensuring all necessary tasks are completed before responding.

### Project Structure

```
.
├── app/
│   ├── llm/
│   │   ├── clients.py      # Configures the LLM client (e.g., Groq, OpenRouter)
│   │   └── prompts.py      # Contains all agent prompts
│   ├── nodes/
│   │   ├── billing_node.py # Agent for fetching billing data
│   │   ├── extractor_node.py # Agent for extracting structured data
│   │   ├── order_node.py   # Agent for fetching order status
│   │   ├── response_node.py# Agent for generating the final response
│   │   └── triage_node.py  # Agent for classifying ticket intent
│   ├── orchestrator/
│   │   └── router.py       # The main routing logic for the graph
│   ├── services/
│   │   ├── billing_service.py # Logic to read from billing.csv
│   │   └── order_service.py   # Logic to read from orders.csv
│   └── utils/
│       └── formatter.py    # Final output formatting node
├── data/
│   ├── billing.csv         # Mock billing database
│   └── orders.csv          # Mock orders database
├── .env                    # Stores secret keys (API keys)
├── main.py                 # FastAPI application entry point
├── workflow.py             # Defines the LangGraph structure and flow
├── graph_state.py          # Defines the shared state object for the graph
└── README.md               # This file
```

## 🚀 Getting Started

Follow these steps to set up and run the project locally.

### 1. Prerequisites

-   Python 3.9+
-   Git

### 2. Clone the Repository

```bash
git clone https://github.com/your-username/Multi-agent-Triage-system.git
cd Multi-agent-Triage-system
```

### 3. Create and Activate a Virtual Environment

On Windows:
```bash
# Create the virtual environment
python -m venv .venv

# Activate the virtual environment
.venv\Scripts\activate
```

### 4. Install Dependencies

Install all the required Python packages from the `requirements.txt` file.
```bash
pip install -r requirements.txt
```
*(If you don't have a `requirements.txt` file, you can create one with `pip freeze > requirements.txt` after installing the necessary packages like `fastapi`, `uvicorn`, `langchain`, `langgraph`, `python-dotenv`, `langchain-groq`, etc.)*

### 5. Set Up Environment Variables

The application requires API keys for the Language Model.

1.  Create a file named `.env` in the root of the project.
2.  Add your API key to this file. Use the example below as a template.

***File: `.env`***
```
# Replace with your actual API key from Groq
GROQ_API_KEY="gsk_..."
```

### 6. Run the Application

Use `uvicorn` to run the FastAPI server. The `--reload` flag will automatically restart the server when you make changes to the code.

```bash
uvicorn main:app --reload
```

The API will now be running at **http://127.0.0.1:8000**.

## ⚙️ API Usage

You can interact with the API using any HTTP client, or by visiting the interactive documentation.

### Interactive Docs (Swagger UI)

Once the server is running, navigate to **http://127.0.0.1:8000/docs** in your browser to see the auto-generated Swagger UI documentation. You can test the endpoint directly from this interface.

### Example `curl` Request

Here is an example of how to call the `/v1/process_ticket` endpoint using `curl`.

```bash
curl -X POST "http://127.0.0.1:8000/v1/process_ticket" \
-H "Content-Type: application/json" \
-d '{
  "messages": [
    ["user", "Hello, I received my last invoice and I believe there is a mistake in the total amount. Can you please check billing for order #G4512-B? Thanks."]
  ]
}'
```

---

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---
<p align="center">
  Powered by <strong><a href="(https://github.com/VeriLabs-Team)" target="_blank">VeriLabs</a></strong>
</p>
