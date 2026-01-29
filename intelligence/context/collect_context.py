from pathlib import Path
import yaml

REPO_ROOT = Path(__file__).resolve().parents[2]

def _read_text(path: Path, max_chars: int = 6000) -> str:
    txt = path.read_text(encoding="utf-8", errors="replace")
    txt = txt.strip()
    return txt[:max_chars] + ("\n...[truncated]" if len(txt) > max_chars else "")

def load_projects():
    path = REPO_ROOT / "intelligence" / "config" / "projects.yaml"
    with open(path) as f:
        return yaml.safe_load(f)["projects"]

def build_context():
    projects = load_projects()
    lines = ["Active projects:"]
    for p in projects:
        lines.append(
            f"- {p['name']}: {p['domain']} using {', '.join(p['stack'])}. "
            f"Goals: {', '.join(p['goals'])}. "
            f"Constraints: {', '.join(p['constraints'])}."
        )
        for rel in p.get("context_files", []) or []:
            doc_path = REPO_ROOT / rel
            if doc_path.exists():
                lines.append(f"\n[Context doc: {rel}]\n{_read_text(doc_path)}\n")
            else:
                lines.append(f"\n[Context doc missing: {rel}]\n")
    return "\n".join(lines)

if __name__ == "__main__":
    print(build_context())
