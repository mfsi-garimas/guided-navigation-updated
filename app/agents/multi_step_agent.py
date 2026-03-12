from typing import List, Dict, Any
from app.agents.base_agent import BaseAgent
from app.prompts.multi_step_prompt import build_multi_step_prompt
from app.config.log_config import logger

class MultiStepAgent(BaseAgent):

    def run(self, user_intent: str, candidate_forms: List[Dict[str, Any]]) -> Dict[str, Any]:
        logger.info(f"[MultiStepAgent] User intent: {user_intent}")

        if not candidate_forms:
            logger.error("No forms received")
            raise ValueError("No forms received.")

        prompt = build_multi_step_prompt(user_intent, candidate_forms)
        result = self.call_llm(prompt, agent_name="MultiStepAgent")
        return result