from typing import TypedDict, Optional, Dict, Any, List


class WebAutomationState(TypedDict, total=False):
    api_type: str
    
    # Input
    user_query: str
    dom_elements: List[Dict[str, Any]]

    # Agent outputs
    interpreted_action: Optional[Dict[str, Any]]
    selected_element: Optional[Dict[str, Any]]
    multi_step_plan: Optional[Dict[str, Any]]

    # Control fields
    next_step: Optional[str]
    iteration: int
    error: Optional[str]
