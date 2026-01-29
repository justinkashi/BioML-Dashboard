from intelligence.reasoning.prompts import DIRECT_PROMPT

def assess(llm, context, item):
    """
    V1 stub: no LLM yet.
    Produces a predictable markdown block so the pipeline is testable.
    """
    title = item.get("title") or item.get("name") or item.get("repo") or "item"
    url = item.get("url")
    notes = item.get("notes", "")
    category = item.get("category", "unknown")

    lines = [f"### {category}: {title}"]
    if url:
        lines.append(f"- URL: {url}")
    lines.append(f"- Notes: {notes}")
    lines.append("- Relevance: STUB (wire LLM later)")
    lines.append("- Why: STUB")
    lines.append("- How to leverage (1 month): STUB")
    return "\n".join(lines)

def debug_prompt(context, item_text):
    return DIRECT_PROMPT.format(context=context, item=item_text)
