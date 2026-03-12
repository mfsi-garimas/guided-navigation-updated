from typing import List, Dict, Any

def truncate_text(text: str, limit: int = 100) -> str:
    if not text:
        return ""
    return text.strip()[:limit]

def prepare_elements_for_prompt(elements: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Convert DOM elements into JSON-ready dict with truncated text.
    This is used before sending elements to LLM.
    """

    processed = []

    for el in elements:
        attrs = el.get("attributes", {}) or {}

        title = truncate_text(attrs.get("title", ""), 100)
        raw_text = el.get("text") or ""
        text = truncate_text(raw_text, 100)

        # If text is empty or only symbols, fallback to title
        if not text.strip() or all(not c.isalnum() for c in text):
            text = title

        processed.append({
            "tag": el.get("tag", "").lower(),
            "text": text,
            "title": truncate_text(attrs.get("title", ""), 100),
            "id": el.get("id", ""),
            "class": el.get("class", ""),
            "name": el.get("name", ""),
            "ariaLabel": el.get("ariaLabel", ""),
            "type": el.get("type", ""),
        })

    return processed
