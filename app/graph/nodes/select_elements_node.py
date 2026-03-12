from typing import Dict, Any
from app.agents.agents_registry import select_elements_agent

def select_elements_node(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    Resolve actual DOM element for action.
    """
    result = select_elements_agent.run(
        interpreted_action=state["interpreted_action"],
        dom_elements=state["dom_elements"]
    )
    state["selected_element"] = result.get("selected_element")
    return state
