from rapidfuzz import fuzz
from app.constants.select_elements_constant import WEIGHTS, THRESHOLD

def get_css_selector(el: dict) -> str:
    el_id = el.get("id") or el.get("el", {}).get("id")
    if el_id:
        return f"#{el_id}"

    classes = (
        el.get("class")
        or el.get("el", {}).get("classes")
        or el.get("attributes", {}).get("class")
        or ""
    )

    if isinstance(classes, list):
        classes = " ".join(classes)

    if classes:
        tag = el.get("tag", "div")
        class_selector = ".".join(classes.split())
        return f"{tag}.{class_selector}"

    href = (
        el.get("attributes", {}).get("href")
        or el.get("el", {}).get("attributes", {}).get("href")
    )

    if href and el.get("tag") == "a":
        return f'a[href="{href}"]'

    return el.get("tag", "div")


def filter_valid_elements(elements: list) -> list:
    valid_elements = []

    for el in elements:
        el_id = el.get("id") or el.get("el", {}).get("id")

        classes = (
            el.get("class")
            or el.get("el", {}).get("classes")
            or el.get("attributes", {}).get("class")
            or ""
        )

        if isinstance(classes, list):
            classes = " ".join(classes)

        href = (
            el.get("attributes", {}).get("href")
            or el.get("el", {}).get("attributes", {}).get("href")
            or ""
        )

        if el_id or classes or href:
            valid_elements.append(el)

    return valid_elements


def extract_click_elements(elements_json):
    processed = []

    for el in elements_json:
        attrs = el.get("attributes", {}) or {}

        raw_text = (el.get("text") or "").strip()
        title = attrs.get("title") or ""
        aria = el.get("ariaLabel") or ""

        if not raw_text or raw_text in {"<", ">", "«", "»", "←", "→"}:
            text = title or aria or raw_text
        else:
            text = raw_text

        processed.append({
            "tag": el.get("tag", ""),
            "text": text,
            "id": el.get("id", ""),
            "class": el.get("class", ""),
            "name": el.get("name", ""),
            "role": el.get("role", ""),
            "ariaLabel": aria,
            "title": title,
            "el": el
        })

    return processed


def extract_search_elements(elements_json):
    processed = []

    for el in elements_json:
        attrs = el.get("attributes", {})
        disabled = el.get("disabled") or el.get("attributes", {}).get("disabled")

        if disabled is not None:
            if isinstance(disabled, bool) and disabled:
                continue
            if isinstance(disabled, str) and disabled.lower() in ("true", "disabled", "1"):
                continue
            if isinstance(disabled, int) and disabled != 0:
                continue

        style = attrs.get("style", "")
        if "display:none" in style.replace(" ", "").lower():
            continue

        text = (
            el.get("value")
            or el.get("placeholder")
            or el.get("text")
            or el.get("title")
            or el.get("ariaLabel")
            or ""
        )

        processed.append({
            "tag": el.get("tag", ""),
            "text": text,
            "id": el.get("id", ""),
            "class": el.get("class", ""),
            "name": el.get("name", ""),
            "role": el.get("role", ""),
            "ariaLabel": el.get("ariaLabel", ""),
            "el": el
        })

    return processed


def extract_checkboxes(elements_json):
    checkboxes = []

    for el in elements_json:
        tag = el.get("tag", "").lower()
        attrs = el.get("attributes", {}) or {}

        if tag != "input" or attrs.get("type") != "checkbox":
            continue

        checkbox_id = attrs.get("id") or el.get("id")
        name = attrs.get("name") or el.get("name")
        value = attrs.get("value") or ""
        aria_label = el.get("ariaLabel") or attrs.get("aria-label") or ""
        raw_text = (el.get("text") or "").strip()
        title = el.get("title") or attrs.get("title") or ""

        label_text = ""
        if checkbox_id:
            label_el = next(
                (lbl for lbl in elements_json 
                 if lbl.get("tag") == "label" and lbl.get("attributes", {}).get("for") == checkbox_id), 
                None
            )
            if label_el:
                label_text = (label_el.get("text") or "").strip()

        parent_text = el.get("parent_text") or ""
        text = label_text or parent_text or aria_label or name or value or title

        if checkbox_id:
            selector = f"#{checkbox_id}"
        elif name:
            selector = f"input[type='checkbox'][name='{name}']"
        else:
            selector = "input[type='checkbox']"

        checkboxes.append({
            "tag": "input",
            "type": "checkbox",
            "text": text,
            "id": checkbox_id,
            "name": name,
            "selector": selector,
            "el": el,
            "index" : len(checkboxes)
        })

    return checkboxes


def flatten_element(el):
    parts = []

    for key in ["text", "ariaLabel", "name", "id", "class"]:
        val = el.get(key)
        if val:
            parts.append(str(val))

    attrs = el.get("attributes", {})
    if isinstance(attrs, dict):
        parts.extend(str(v) for v in attrs.values() if v)

    return " ".join(parts)


def fuzzy_search(elements, target_text, limit=20):
    target_text = target_text.lower()
    scored = []

    for el in elements:
        element_text = flatten_element(el).lower()

        if target_text in element_text:
            score = 100
        else:
            score = fuzz.partial_ratio(target_text, element_text)

        if score >= THRESHOLD:
            scored.append((score, el))

    scored.sort(key=lambda x: x[0], reverse=True)
    return [el for _, el in scored[:limit]]
