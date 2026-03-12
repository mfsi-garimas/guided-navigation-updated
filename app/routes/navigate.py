from fastapi import APIRouter, HTTPException
from typing import Dict, Any
from app.graph.main_graph import build_main_graph
from app.config.log_config import logger

router = APIRouter()

graph = build_main_graph()

def run_graph(state: Dict[str, Any]):
    try:
        return graph.invoke(state)
    except Exception as e:
        logger.exception("Graph execution failed")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/health")
async def health():
    return {"status": "ok"}

@router.post("/api/interpret")
async def interpret(payload: Dict[str, Any]):
    state = {
        "api_type": "interpret",
        "user_query": payload["command"],
        "dom_elements": payload["elements"]
    }
    result = run_graph(state)
    return result["interpreted_action"]


@router.post("/api/multi_step")
async def multi_step(payload: Dict[str, Any]):
    state = {
        "api_type": "multi_step",
        "user_query": payload["command"],
        "dom_elements": payload["elements"]
    }
    result = run_graph(state)
    return result["multi_step_plan"]

@router.post("/api/get_required_elements")
async def get_required_elements(payload: Dict[str, Any]):
    state = {
        "api_type": "select_elements",
        "interpreted_action": payload["interpreted_action"],
        "dom_elements": payload["elements"]
    }
    result = run_graph(state)
    return {"selected_element": result.get("selected_element")}
