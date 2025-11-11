from langgraph.graph import StateGraph, END
from app.orchestrator.router import orchestrator
from app.nodes import (
    billing_node,
    response_node,
    extractor_node,
    triage_node,
    order_node
)
from utils.formatter import final_formatter
from graph_state import TriageState


# Define the workflow using the TriageState
workflow = StateGraph(TriageState)

# Add nodes to the workflow
workflow.add_node("orchestrator", orchestrator)
workflow.add_node("triage", triage_node)
workflow.add_node("extractor", extractor_node)
workflow.add_node("order", order_node)
workflow.add_node("billing", billing_node)
workflow.add_node("response_agent", response_node)
workflow.add_node("final_formatter", final_formatter)

# entry point of the workflow
workflow.set_entrypoint("orchestrator")

# adding conditional edges based on the orchestrator's routing
print("Adding conditional edges based on orchestrator routing")
workflow.add_conditional_edge(
    "orchestrator",
    orchestrator,
    {
        "call_triage": "triage",
        "call_extractor": "extractor",
        "call_order": "order",
        "call_billing": "billing",
        "call_response_agent": "response_agent",
        "finalize": "final_formatter"
    })

# Define the edges between nodes to establish the flow
workflow.add_edge("triage", "orchestrator")
workflow.add_edge("extractor", "orchestrator")
workflow.add_edge("order", "orchestrator")
workflow.add_edge("billing", "orchestrator")
workflow.add_edge("response_agent", "orchestrator")

# End the workflow
workflow.add_edge("final_formatter", END)  

# Compile the workflow
app_graph = workflow.compile()

# Visualize the graph
from IPython.display import Image

try:
    img_data = app_graph.get_graph(xdot=True).draw_png()
    with open("graph.png", "wb") as f:
        f.write(img_data)
    print("Graph visualization saved to graph.png")
except Exception as e:
    print(f"Could not save graph visualization: {e}")