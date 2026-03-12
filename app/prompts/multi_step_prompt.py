import textwrap

def build_multi_step_prompt(user_intent: str, candidate_forms):

    return textwrap.dedent(f"""
    You are a Web Automation Planner.

    You are given:
    - A user intent
    - A list of candidate forms extracted from the webpage

    Rules:
    - Use ONLY the provided selectors
    - NEVER invent selectors
    - Ask for required fields only
    - Always generate steps for ALL required form fields even if the user command provides only some values. Missing values must be collected using an ask step.
    - Value_from must reference the field name NOT the literal value
    - Input_name and value_from MUST use the semantic field name from the user intent (e.g., username, password, goal) and MUST NOT use the DOM selector or element id (e.g., txtName, txtPassword).
    - Steps must be executable as-is
    - Output JSON ONLY
    - No explanations

    Output format (EXACT):

    {{
      "plan_type": "form_fill",
      "form_selector": "",
      "steps": [
        {{
          "action": "ask",
          "field": "",
          "message": "",
          "selector": "",
          "input_name":""
        }},
        {{
          "action": "type",
          "selector": "",
          "value_from": ""
        }},
        {{
          "action": "click",
          "selector": ""
        }}
      ]
    }}

    User intent:
    {user_intent}

    Candidate forms:
    {candidate_forms}
    """)