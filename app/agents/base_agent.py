# app/agents/base_agent.py
from app.config.log_config import logger
from typing import Any, Dict, List
import json

class BaseAgent:
    """
    Base class for all LLM-based agents.
    Centralizes LLM call, JSON parsing, logging, and validation.
    """

    def __init__(self, llm_client):
        self.llm = llm_client

    def call_llm(
        self,
        prompt: str,
        agent_name: str = "BaseAgent",
        required_keys: List[str] = None
    ) -> Dict[str, Any]:
        """
        Calls the LLM, parses JSON if necessary, validates required keys,
        and logs everything consistently.
        """
        logger.info(f"---- {agent_name} START ----")
        logger.debug(f"[{agent_name}] Prompt:\n{prompt}")

        # Call LLM
        result = self.llm.call(prompt)
        logger.debug(f"[{agent_name}] Raw LLM response:\n{result}")

        # Ensure dict
        if not isinstance(result, dict):
            try:
                result = json.loads(result)
            except json.JSONDecodeError:
                logger.error(f"[{agent_name}] LLM returned invalid JSON")
                raise ValueError(f"[{agent_name}] LLM returned invalid JSON")

        # Validate required keys
        if required_keys:
            missing_keys = [k for k in required_keys if k not in result]
            if missing_keys:
                logger.error(f"[{agent_name}] Missing keys: {missing_keys}")
                raise ValueError(f"[{agent_name}] Missing keys in LLM output: {missing_keys}")

        # Normalize inputs
        if "inputs" not in result:
            result["inputs"] = {}

        logger.info(f"---- {agent_name} END ----")
        return result