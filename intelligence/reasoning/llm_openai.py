import os
from openai import OpenAI

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

def llm(prompt: str) -> str:
    r = client.responses.create(
        model="gpt-5",
        input=prompt,
    )
    return r.output_text
