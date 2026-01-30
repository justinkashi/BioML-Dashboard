from datetime import date
from intelligence.context.collect_context import build_context
from intelligence.signals.load_signals import load_items
from intelligence.reasoning.relevance import assess
from intelligence.reasoning.llm_openai import llm

def main(llm=None):
    context = build_context()
    items = load_items()

    out = []
    out.append(f"# Weekly Research Intelligence — {date.today().isoformat()}\n")
    out.append("## Context\n")
    out.append("```")
    out.append(context)
    out.append("```\n")
    out.append("## Items\n")

    for item in items:
        out.append(assess(llm, context, item))
        out.append("")

    report = "\n".join(out)
    with open("outputs/weekly_report.md", "w") as f:
        f.write(report)

    print("Wrote outputs/weekly_report.md")

if __name__ == "__main__":
    main(llm=llm)
