from typing import List, Dict, Any
from app.agents.base_agent import BaseAgent
from app.config.log_config import logger
from app.tools.select_element_tools import (
    extract_click_elements,
    extract_search_elements,
    extract_checkboxes,
    filter_valid_elements,
    fuzzy_search,
    get_css_selector,
)
from app.prompts.select_element_prompt import build_select_elements_prompt, build_search_prompt

class SelectElementsAgent(BaseAgent):

    def run(self, interpreted_action: Dict[str, Any], dom_elements: List[Dict[str, Any]]) -> Dict[str, Any]:
        logger.info(f"[SelectElementsAgent] Interpreted Action: {interpreted_action}")

        action = interpreted_action.get("action")
        key = interpreted_action.get("key")

        if not action or not key:
            logger.error("Invalid interpreted action")
            raise ValueError("Invalid interpreted action")

        results = []
        if action == "click":
            elements = filter_valid_elements(extract_click_elements(dom_elements))
            results = fuzzy_search(elements, key)
        elif action == "search":
            elements = extract_search_elements(dom_elements)
            results = fuzzy_search(elements, "search")
        elif action in ["check", "uncheck"]:
            results = extract_checkboxes(dom_elements)

        if not results:
            logger.warning("No matching elements found")
            return {"selected_element": None}

        llm_elements = []
        for index, item in enumerate(results):
            el = item.get("el", item)
            classes = el.get("classes") or el.get("class") or []
            if isinstance(classes, str):
                classes = classes.split()
            llm_elements.append({
                "index": index,
                "tag": el.get("tag", ""),
                "text": item.get("text", "")[:200],
                "attributes": {
                    "id": el.get("id") or None,
                    "class": " ".join(classes) if classes else None,
                    "href": el.get("attributes", {}).get("href") or None
                },
                "selector": get_css_selector(el)
            })

        if action in ["click", "check", "uncheck"]:
            prompt = build_select_elements_prompt(action, key, llm_elements)
        else:  # search
            prompt = build_search_prompt(key, llm_elements)

        response = self.call_llm(prompt, agent_name="SelectElementsAgent")

        selected_index = response.get("index")
        if selected_index is not None and selected_index < len(results):
            selected = results[selected_index]
            response["selector"] = selected.get("selector") or get_css_selector(selected.get("el", selected))
            response["tag"] = selected.get("tag")
            response["text"] = selected.get("text")

        return {"selected_element": response}