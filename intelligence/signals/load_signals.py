from pathlib import Path
import yaml

REPO_ROOT = Path(__file__).resolve().parents[2]

def load_items():
    path = REPO_ROOT / "intelligence" / "signals" / "items.yaml"
    with open(path) as f:
        raw = yaml.safe_load(f)

    items = []
    for category, entries in raw.items():
        for entry in entries:
            items.append({"category": category, **entry})
    return items

if __name__ == "__main__":
    for item in load_items():
        print(item)
