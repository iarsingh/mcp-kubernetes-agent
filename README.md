# MCP Kubernetes Agent

Level: 10 — MCP and tool-using agents

Skills: Python, a tool schema, Kubernetes manifest checks

`mcp/tools.json` lists get_pods, read_logs, and render_manifest. The agent refuses `latest`, a replica count outside 1 to 5, and any goal that applies or deletes. `applied` stays false.

```bash
pip install -r requirements.txt
pytest -q
```
