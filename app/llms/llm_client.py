from typing import Dict, Any
from app.llms.openai_chat_client import OpenAIChatClient


class LLMClient:
    """
    Abstraction layer over LLM providers.

    Agents use this.
    They never directly use OpenAIChatClient.
    """

    def __init__(self):
        self.provider = OpenAIChatClient()

    def call(self, prompt: str) -> Dict[str, Any]:
        """
        Execute prompt through configured provider.
        """
        return self.provider.call(prompt)