DIRECT_PROMPT = """
You are a senior bioinformatics / BioML research engineer.

Project context:
{context}

New item:
{item}

Task:
1) Relevance: HIGH / MEDIUM / IGNORE
2) Why (2-3 bullets)
3) If relevant: how to leverage within 1 month (2-4 bullets, concrete)
4) If ignore: why ignore (1-2 bullets)

Be specific. No hype. Prefer actionable guidance.
""".strip()

CREATIVE_PROMPT = """
You are a speculative research collaborator.

Project context:
{context}

New item:
{item}

Task:
- 2 non-obvious ways this could inspire new approaches
- 1 risky idea worth exploring
Keep it grounded in the project context.
""".strip()
