from typing import List, Dict, Any
from app.agents.base_agent import BaseAgent
from app.tools.interpret_tools import prepare_elements_for_prompt
from app.prompts.interpret_prompt import build_interpret_prompt
from app.config.log_config import logger

class InterpretAgent(BaseAgent):

    def run(self, user_command: str, elements: List[Dict[str, Any]]) -> Dict[str, Any]:
        logger.info(f"[InterpretAgent] User Command: {user_command}")
        elements_json = prepare_elements_for_prompt(elements)
        prompt = build_interpret_prompt(user_command, elements_json)

        result = self.call_llm(prompt, agent_name="InterpretAgent", required_keys=["action", "key"])

        if result["action"] == "search" and "search" in result.get("inputs", {}):
            result["key"] = result["inputs"]["search"]

        return result