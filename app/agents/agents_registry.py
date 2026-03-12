from app.llms.llm_client import LLMClient
from app.agents.interpret_agent import InterpretAgent
from app.agents.multi_step_agent import MultiStepAgent
from app.agents.select_elements_agent import SelectElementsAgent

llm_client = LLMClient()

interpret_agent = InterpretAgent(llm_client)
multi_step_agent = MultiStepAgent(llm_client)
select_elements_agent = SelectElementsAgent(llm_client)