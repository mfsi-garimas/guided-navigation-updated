from langgraph.graph import StateGraph, END
from app.graph.state import WebAutomationState

from app.graph.nodes.router_node import router_node
from app.graph.nodes.interpret_node import interpret_node
from app.graph.nodes.select_elements_node import select_elements_node
from app.graph.nodes.multi_step_node import multi_step_node


def route_decision(state: WebAutomationState):

    api_type = state.get("api_type")

    if api_type == "interpret":
        return "interpret_node"

    if api_type == "select_elements":
        return "select_elements_node"

    if api_type == "multi_step":
        return "multi_step_node"

    raise ValueError(f"Unknown api_type {api_type}")


def build_main_graph():

    workflow = StateGraph(WebAutomationState)

    workflow.add_node("router", router_node)
    workflow.add_node("interpret_node", interpret_node)
    workflow.add_node("select_elements_node", select_elements_node)
    workflow.add_node("multi_step_node", multi_step_node)

    workflow.set_entry_point("router")

    workflow.add_conditional_edges(
        "router",
        route_decision,
        {
            "interpret_node": "interpret_node",
            "select_elements_node": "select_elements_node",
            "multi_step_node": "multi_step_node",
        }
    )

    workflow.add_edge("interpret_node", END)
    workflow.add_edge("select_elements_node", END)
    workflow.add_edge("multi_step_node", END)

    return workflow.compile()