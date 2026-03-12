from typing import Dict, Any
from app.agents.agents_registry import multi_step_agent

def multi_step_node(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    Generate execution plan for form interaction.
    """
    result = multi_step_agent.run(
        user_intent=state["user_query"],
        candidate_forms=state["dom_elements"]
    )
    state["multi_step_plan"] = result
    return state
