
from typing import Any, Dict
import json
from app.config.log_config import logger
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage
from app.config.llm_config import get_settings



class OpenAIChatClient:
    """
    Industrial OpenAI chat wrapper.

    - Centralized model config
    - JSON enforcement
    - Retry handling
    - Clean dict output
    """

    def __init__(self) -> None:
        self.settings = get_settings()
        self.model_name = self.settings.OPENAI_MODEL_NAME
        self.temperature = self.settings.OPENAI_TEMPERATURE
        

        self.client = ChatOpenAI(
            model_name=self.model_name,
            temperature=self.temperature,
            api_key=self.settings.OPENAI_API_KEY,
        )

    def call(self, prompt: str) -> Dict[str, Any]:
        """
        Execute LLM call and enforce JSON output.
        """

        last_error = None

        
        try:
            response = self.client.invoke(
                [HumanMessage(content=prompt)]
            )

            content = response.content

            # Enforce JSON parsing
            parsed = self._parse_json(content)
            return parsed

        except Exception as e:
            logger.warning
            last_error = e

        raise RuntimeError(f"LLM failed after retries: {last_error}")

    def _parse_json(self, content: str) -> Dict[str, Any]:
        """
        Safely parse JSON from model output.
        Handles markdown fences and stray 'json' prefixes.
        """

        content = content.strip()

        # Remove ```json or ``` wrappers
        if content.startswith("```"):
            parts = content.split("```")
            if len(parts) >= 2:
                content = parts[1].strip()

        # Remove leading 'json'
        if content.startswith("json"):
            content = content[4:].strip()

        try:
            return json.loads(content)

        except json.JSONDecodeError:
            logger.error("Invalid JSON from LLM:\n%s", content)
            raise ValueError("LLM did not return valid JSON")
