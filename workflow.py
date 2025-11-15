import logging
import sys
from langgraph.graph import StateGraph, END
from app.orchestrator.router import orchestrator
from app.nodes.triage_node import triage_agent
from app.nodes.extractor_node import extractor_agent
from app.nodes.billing_node import billing_agent
from app.nodes.order_node import order_agent
from app.nodes.response_node import response_agent
from app.utils.formatter import final_formatter
from graph_state import TriageState

# Set up basic logging to see the flow
logging.basicConfig(stream=sys.stdout, level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', force=True)
log = logging.getLogger(__name__)

# Define the workflow using the TriageState
workflow = StateGraph(TriageState)

# A passthrough orchestrator node (for logging purposes)
def orchestrator_passthrough(state: TriageState):
    """A simple node that just passes the state through."""
    log.info("--- ORCHESTRATOR HUB (PASSTHROUGH) ---")
    return {} 

# Add nodes to the workflow
log.info("Adding nodes to the graph...")
workflow.add_node("orchestrator", orchestrator_passthrough)
workflow.add_node("triage", triage_agent)
workflow.add_node("extractor", extractor_agent)
workflow.add_node("order", order_agent)
workflow.add_node("billing", billing_agent)
workflow.add_node("response_agent", response_agent)
workflow.add_node("final_formatter", final_formatter)

# entry point of the workflow
workflow.set_entry_point("orchestrator")

# adding conditional edges based on the orchestrator's routing
log.info("Adding conditional edges based on orchestrator routing")
workflow.add_conditional_edges(
    "orchestrator",
    orchestrator,
    {
        "call_triage": "triage",
        "call_extraction": "extractor",
        "call_order": "order",
        "call_billing": "billing",
        "call_response_agent": "response_agent",
        "finalize": "final_formatter"
    })

# Define the edges between nodes to establish the flow
log.info("Adding loop-back edges...")
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
    # This argument is deprecated in newer langgraph versions.
    img_data = app_graph.get_graph().draw_png()
    with open("graph.png", "wb") as f:
        f.write(img_data)
    log.info("Graph visualization saved to graph.png")
except Exception as e:
    # Updated warning message
    log.warning(f"Could not save graph visualization: {e}. ('xdot' is likely not supported in your langgraph version.)")

# --- 9. Test the graph ---
if __name__ == "__main__":
    print("\n--- Running Workflow ---")

    # --- FIX 4: The test input MUST match TriageState ---
    sample_input = {
        "raw_text": "Hello, I received my last invoice and I believe there is a mistake in the total amount. Can you please check billing for order #1005? Thanks."
    }

    print(f"Initial State: {sample_input}\n")
    print("Streaming graph execution...")
    print("-" * 30)
    
    try:
        config = {"recursion_limit": 15}
        
        for event in app_graph.stream(sample_input, config=config):
            for node_name, output_state in event.items():
                print(f"\nOutput from node '{node_name}':")
                print(f"-> State Update: {output_state}") 
                print("-" * 30)
                
        final_state = app_graph.invoke(sample_input, config=config)
        print("\n--- Workflow Finished ---")
        print("\nFinal API Output (from 'final_output' key):")
        print(final_state.get("final_output"))

    except Exception as e:
        print(f"\nAn error occurred during workflow execution: {e}")
        import traceback
        traceback.print_exc()