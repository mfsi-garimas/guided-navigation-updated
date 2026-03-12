import json
import textwrap

def build_select_elements_prompt(action: str, key: str, elements):

    return textwrap.dedent(f"""
    You are analyzing candidate elements and must return the single most relevant element.

    Goal:
    - Select EXACTLY one candidate
    - Action: "{action}"
    - Target text: "{key}"

    Rules:
    - Return JSON ONLY
    - Do NOT include explanations
    - Use ONLY the provided candidate elements
    - Never invent elements
    - If a field is missing, return null
    - Partial matches of the target text or element title are acceptable

    Return format:
    {{
    "action": "{action}",
    "selector": "",
    "tag": "",
    "text": "",
    "attributes": {{
        "id": "",
        "class": "",
        "href": ""
    }}
    }}

    Candidates:
    {json.dumps(elements, indent=2)}
    """.strip())


def build_search_prompt(key: str, elements):
 
    return textwrap.dedent(f"""
    You are analyzing webpage elements and must return the most relevant elements for a SEARCH action.
    
    Target:
    - Action: "search"
    - Search query text: "{key}"
    
    Rules:
    - Output ONLY one JSON object
    - Do NOT return arrays
    - Do NOT generate JavaScript or explanations
    - Use ONLY the provided candidate elements
    - Never invent elements
    - If a field does not exist, return null or "" as appropriate
    
    Search element selection:
    
    1. searchInput  
    - The input element where the search query is typed.
    
    2. searchButton  
    - The element that triggers the search (button, submit button, icon, or clickable div).
    
    3. resultsContainer  
    Container priority:
    - Prefer the container used for search suggestions or autocomplete.
    - If no suggestion container exists, choose the container where search results are rendered.
    
    Text field rule:
    - "text" must contain the visible text of the element.
    - If the element has no visible text, return "".
    - Do NOT invent descriptive text.
    
    Return format:
    {{
    "action": "search",
    "searchInput": {{
        "tag": "",
        "text": "",
        "selector": "",
        "attributes": {{
            "id": "",
            "class": "",
            "name": "",
            "placeholder": ""
        }},
        "key": "{key}"
    }},
    "searchButton": {{
        "tag": "",
        "text": "",
        "selector": "",
        "attributes": {{
            "id": "",
            "class": ""
        }}
    }},
    "resultsContainer": {{
        "tag": "",
        "text": "",
        "selector": "",
        "attributes": {{
            "id": "",
            "class": ""
        }}
    }}
    }}
    
    Candidate elements (use ONLY these):
    {json.dumps(elements, indent=2)}
    """.strip())