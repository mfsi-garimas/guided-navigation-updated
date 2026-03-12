from typing import Dict, Any
from app.agents.agents_registry import interpret_agent

def interpret_node(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    Extract structured intent from user query.
    """
    result = interpret_agent.run(
        user_command=state["user_query"],
        elements=state["dom_elements"]
    )
    state["interpreted_action"] = result
    return state