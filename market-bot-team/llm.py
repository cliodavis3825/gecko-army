# llm.py  -- asks Claude for JSON and parses it
import json, re
from clients import claude

def ask_json(system, user, model, max_tokens=2000):
    msg = claude.messages.create(
        model=model, max_tokens=max_tokens, system=system,
        messages=[{"role": "user", "content": user}],
    )
    text = "".join(b.text for b in msg.content if b.type == "text")
    text = re.sub(r"```(json)?", "", text).strip()
    return json.loads(text)
