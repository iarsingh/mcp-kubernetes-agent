# MCP Kubernetes Agent

<!-- project-guide:start -->
## Project guide

[Project architecture](PROJECT_ARCHITECTURE.md) · [Interview questions and answers](INTERVIEW_QA.md)

Use the architecture document for the component diagram, implementation boundaries, and verification entry points. The interview guide includes source-backed answers and project walkthroughs.

### Implementation map

| Component | Responsibility |
| --- | --- |
| [`src/k8sagent/main.py`](src/k8sagent/main.py) | HTTP handlers: `POST /agent/run` |
| [`src/k8sagent/agent.py`](src/k8sagent/agent.py) | Functions: `run` |
| [`requirements.txt`](requirements.txt) | Implementation or supporting configuration |
| [`src/k8sagent/__init__.py`](src/k8sagent/__init__.py) | Implementation or supporting configuration |
| [`tests/test_k8sagent.py`](tests/test_k8sagent.py) | Executable checks and regression examples |
| [`.github/workflows/ci.yml`](.github/workflows/ci.yml) | GitHub Actions job definitions |
| [`README.md`](README.md) | Project explanations or operating notes |

### Local setup and verification

From the repository root (the commands follow the checked-in manifests):

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m pytest -q
```

To serve the FastAPI application locally, install the server separately if it is not already available:

```bash
python -m pip install uvicorn
PYTHONPATH=src python -m uvicorn k8sagent.main:app --reload
```

<!-- project-guide:end -->

Level: 10 — MCP and tool-using agents

Skills: Python, a tool schema, Kubernetes manifest checks

`mcp/tools.json` lists get_pods, read_logs, and render_manifest. The agent refuses `latest`, a replica count outside 1 to 5, and any goal that applies or deletes. `applied` stays false.

```bash
pip install -r requirements.txt
pytest -q
```

## Ops plane

Workspaces, tenant isolation, job approval, and audit live under `/v1`. Production apply is refused. See `docs/ARCHITECTURE.md`.
