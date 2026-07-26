import json
import os
from datetime import datetime, timezone
from typing import Optional

DREAMS_DIR = os.path.expanduser("~/.config/opencode/dreams")


def _ensure_dir():
    os.makedirs(DREAMS_DIR, exist_ok=True)


def store_dream(domain: str, content: str, kind: str = "general") -> dict:
    _ensure_dir()
    timestamp = datetime.now(timezone.utc).isoformat()
    entry = {
        "domain": domain,
        "content": content,
        "kind": kind,
        "timestamp": timestamp,
    }
    safe = timestamp.replace(":", "-").replace("+", "_")
    filename = f"{domain}_{safe}.json"
    path = os.path.join(DREAMS_DIR, filename)
    with open(path, "w") as f:
        json.dump(entry, f, indent=2)
    return entry


def list_dreams(domain: Optional[str] = None) -> list:
    _ensure_dir()
    results = []
    for fname in sorted(os.listdir(DREAMS_DIR), reverse=True):
        if not fname.endswith(".json"):
            continue
        if domain and not fname.startswith(domain + "_"):
            continue
        path = os.path.join(DREAMS_DIR, fname)
        try:
            with open(path) as f:
                results.append(json.load(f))
        except (json.JSONDecodeError, OSError):
            continue
    return results
