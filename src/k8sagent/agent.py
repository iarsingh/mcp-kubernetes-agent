import json
from pathlib import Path

TOOLS = json.loads((Path(__file__).resolve().parents[2] / "mcp" / "tools.json").read_text())

def run(goal, image, replicas):
    names = [tool["name"] for tool in TOOLS]
    if image.endswith(":latest") or ":" not in image:
        return {"refused": True, "reason": "Pin an image tag. latest is refused.", "applied": False, "tools": names}
    if not 1 <= replicas <= 5:
        return {"refused": True, "reason": "Replicas must be from 1 to 5.", "applied": False, "tools": names}
    if any(word in goal.lower() for word in ("apply", "delete", "prod")):
        return {"refused": True, "reason": "This agent does not apply to a cluster.", "applied": False, "tools": names}
    manifest = {"kind": "Deployment", "image": image, "replicas": replicas, "resources": {"cpu": "100m", "memory": "128Mi"}}
    return {"refused": False, "tools": names, "manifest": manifest, "applied": False}
