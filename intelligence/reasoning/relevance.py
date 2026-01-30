from __future__ import annotations

import json
import hashlib
import re
from pathlib import Path
from typing import Callable, Optional, Dict, Any

REPO_ROOT = Path(__file__).resolve().parents[2]
CACHE_DIR = REPO_ROOT / "outputs" / "cache"
CACHE_DIR.mkdir(parents=True, exist_ok=True)

LLMCallable = Callable[[str], str]

DIRECT_PROMPT = """
You are a senior BioML research engineer.

Project context:
{context}

New item (paper/repo/model/doc):
{item}

Return STRICT JSON only with keys:
- relevance: one of ["HIGH","MEDIUM","IGNORE"]
- rationale: array of 2-4 bullet strings
- direct_actions_30d: array of 2-6 bullet strings (tie to modules: writers/build_features/phase_analysis/scorer/eval)
- risks_or_mismatches: array of 1-4 bullet strings
No prose outside JSON. No code fences.
""".strip()

CREATIVE_PROMPT = """
You are a speculative research collaborator.

Project context:
{context}

New item:
{item}

Return STRICT JSON only with keys:
- creative_ideas: array of 2-4 bullet strings
- risky_bet: single bullet string
No prose outside JSON. No code fences.
""".strip()


def _h(s: str) -> str:
    return hashlib.sha256(s.encode("utf-8", errors="replace")).hexdigest()[:16]


def _extract_json(text: str) -> Optional[Dict[str, Any]]:
    t = text.strip()
    t = re.sub(r"^```(json)?\s*|\s*```$", "", t, flags=re.IGNORECASE | re.MULTILINE).strip()
    m = re.search(r"\{.*\}", t, flags=re.DOTALL)
    if not m:
        return None
    try:
        return json.loads(m.group(0))
    except json.JSONDecodeError:
        return None


def _cache_path(kind: str, context: str, item: dict) -> Path:
    key = f"{kind}_{_h(context)}_{_h(json.dumps(item, sort_keys=True))}.json"
    return CACHE_DIR / key


def _read_cache(p: Path) -> Optional[dict]:
    if not p.exists():
        return None
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except Exception:
        return None


def _write_cache(p: Path, obj: dict) -> None:
    p.write_text(json.dumps(obj, indent=2, sort_keys=False), encoding="utf-8")


def _fmt(title: str, bullets: list[str]) -> str:
    lines = [f"**{title}**"]
    for b in bullets:
        lines.append(f"- {b}")
    return "\n".join(lines)


def assess(llm: Optional[LLMCallable], context: str, item: dict) -> str:
    category = item.get("category", "unknown")
    title = item.get("title") or item.get("name") or item.get("repo") or item.get("model") or "item"
    url = item.get("url")
    notes = item.get("notes", "")

    if llm is None:
        # deterministic fallback to keep pipeline runnable
        t = (title + " " + notes).lower()
        relevance = "HIGH" if any(k in t for k in ["esm", "evcouplings", "ndcg", "scorer", "build_features"]) else \
                    "MEDIUM" if any(k in t for k in ["pandas", "pytorch", "alphafold"]) else "IGNORE"
        lines = [f"### {category}: {title}"]
        if url: lines.append(f"- URL: {url}")
        if notes: lines.append(f"- Notes: {notes}")
        lines.append(f"- Relevance: {relevance} (no-LLM fallback)")
        lines.append(_fmt("Why", ["Wire an LLM to generate project-specific rationale/actions."]))
        lines.append(_fmt("Direct actions (30d)", ["Add tags/notes to items.yaml to improve specificity."]))
        lines.append(_fmt("Creative mode", ["Enable LLM to propose creative ideas."]))
        return "\n\n".join(lines)

    item_text = json.dumps(item, ensure_ascii=False, indent=2, sort_keys=True)

    direct_cache = _cache_path("direct", context, item)
    creative_cache = _cache_path("creative", context, item)

    direct = _read_cache(direct_cache)
    if direct is None:
        resp = llm(DIRECT_PROMPT.format(context=context, item=item_text))
        direct = _extract_json(resp) or {}
        _write_cache(direct_cache, direct)

    creative = _read_cache(creative_cache)
    if creative is None:
        resp = llm(CREATIVE_PROMPT.format(context=context, item=item_text))
        creative = _extract_json(resp) or {}
        _write_cache(creative_cache, creative)

    relevance = direct.get("relevance", "MEDIUM")
    rationale = direct.get("rationale", []) if isinstance(direct.get("rationale"), list) else []
    actions = direct.get("direct_actions_30d", []) if isinstance(direct.get("direct_actions_30d"), list) else []
    risks = direct.get("risks_or_mismatches", []) if isinstance(direct.get("risks_or_mismatches"), list) else []
    ideas = creative.get("creative_ideas", []) if isinstance(creative.get("creative_ideas"), list) else []
    risky = creative.get("risky_bet", "") if isinstance(creative.get("risky_bet"), str) else ""

    lines = [f"### {category}: {title}"]
    if url: lines.append(f"- URL: {url}")
    if notes: lines.append(f"- Notes: {notes}")
    lines.append(f"- Relevance: {relevance}")

    if rationale:
        lines.append(_fmt("Why", rationale))
    if actions:
        lines.append(_fmt("Direct actions (30d)", actions))
    if risks:
        lines.append(_fmt("Risks / mismatches", risks))
    if ideas or risky:
        cm = ideas[:]
        if risky:
            cm.append(f"Risky bet: {risky}")
        lines.append(_fmt("Creative mode", cm))

    return "\n\n".join(lines)
