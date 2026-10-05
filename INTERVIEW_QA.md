# mcp-kubernetes-agent — interview questions and answers

[README](README.md) · [Project architecture](PROJECT_ARCHITECTURE.md)

Answers below use this repository’s files and implementation. They distinguish existing behavior from suggested extensions; source links let you verify each walkthrough.

## 1. What problem does mcp-kubernetes-agent address, and what can you demonstrate?

`mcp/tools.json` lists get_pods, read_logs, and render_manifest. The agent refuses `latest`, a replica count outside 1 to 5, and any goal that applies or deletes. `applied` stays false.

I would demonstrate the linked implementation or examples and distinguish that evidence from any planned production features. Start with [`README.md`](README.md).

## 2. How is this repository organized?

- [`src/k8sagent/main.py`](src/k8sagent/main.py): Implementation or supporting configuration.
- [`src/k8sagent/agent.py`](src/k8sagent/agent.py): Implementation or supporting configuration.
- [`requirements.txt`](requirements.txt): Implementation or supporting configuration.
- [`src/k8sagent/__init__.py`](src/k8sagent/__init__.py): Implementation or supporting configuration.
- [`tests/test_k8sagent.py`](tests/test_k8sagent.py): Executable checks and regression examples.
- [`.github/workflows/ci.yml`](.github/workflows/ci.yml): GitHub Actions job definitions.
- [`README.md`](README.md): Project explanations or operating notes.

[PROJECT_ARCHITECTURE.md](PROJECT_ARCHITECTURE.md) contains the component diagram and the implementation walkthrough.

## 3. Can you walk through `run` and explain the decision it makes?

The main walkthrough here is `run(goal, image, replicas)` in [`src/k8sagent/agent.py`](src/k8sagent/agent.py#L6).

```python
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
```

The implementation calls `any`, `goal.lower`, `image.endswith`. In an interview, trace those calls in execution order using a fixture input.

## 4. Where would you add input-validation tests?

Start with the handlers `post_run` in [`src/k8sagent/main.py`](src/k8sagent/main.py#L7). Use the request schema or body access in each handler to build valid, missing-field, wrong-type, and boundary inputs. I would inspect existing tests before claiming coverage.

## 5. Which test would you use to demonstrate correctness?

[`tests/test_k8sagent.py`](tests/test_k8sagent.py#L4) contains `test_renders_and_refuses_latest`:

```python
def test_renders_and_refuses_latest():
    client = TestClient(app)
    good = client.post("/agent/run", json={"goal": "inspect the billing pods", "image": "billing:1.4.2", "replicas": 2}).json()
    assert good["applied"] is False
    assert good["tools"] == ["get_pods", "read_logs", "render_manifest"]
    assert good["manifest"]["image"] == "billing:1.4.2"
    bad = client.post("/agent/run", json={"goal": "apply this", "image": "billing:latest", "replicas": 2}).json()
    assert bad["refused"] is True
    assert bad["applied"] is False
```

This is a concrete regression example from the repository. Its assertions establish that case; they do not establish behavior for every input or under production load.

## 6. What HTTP interface does the code expose?

- `POST /agent/run` → `post_run` in [`src/k8sagent/main.py`](src/k8sagent/main.py#L7).

These are literal decorators. Application/router prefixes, authentication, and middleware must be checked in the corresponding setup code.

## 7. How would you investigate data ownership and persistence?

Trace the data/configuration files and the code that reads or writes them in the component table. Identify which files are examples, which records are mutable, and which external store is actually configured. I would document those facts before discussing retention, backup, or tenant isolation.

## 8. How would another engineer reproduce your walkthrough?

Start from the repository root:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m pytest -q
```

These commands follow repository manifests; environment setup and command results still need to be checked on the target machine.

## 9. What does automation verify, and what does it not prove?

Inspect [`.github/workflows/ci.yml`](.github/workflows/ci.yml) for triggers, permissions, and job commands. I would name the checks that those definitions run and show the latest run separately. A workflow definition alone does not establish a successful deployment, security review, or production SLO.

## 10. How would you present this project in a Forward Deployed Engineer interview?

Start with the user and operational problem described in [`README.md`](README.md). Explain one constraint that changes the implementation, show the linked code or example, and walk through a success case and a failure case. Agree on a measurable acceptance criterion before expanding the solution, and leave a handoff with data boundaries and rollback ownership. Any proposed production or business metric should be identified as a target until measured.

## 11. What is the input-to-output contract of `run`?

In [`src/k8sagent/agent.py`](src/k8sagent/agent.py#L6), `run(goal, image, replicas)` receives the inputs. The function computes these intermediate values:

- `names = [tool['name'] for tool in TOOLS]`
- `manifest = {'kind': 'Deployment', 'image': image, 'replicas': replicas, 'resources': {'cpu': '100m', 'memory': '128Mi'}}`

Its result is defined by:

- `{'refused': False, 'tools': names, 'manifest': manifest, 'applied': False}`
- `{'refused': True, 'reason': 'Pin an image tag. latest is refused.', 'applied': False, 'tools': names}`
- `{'refused': True, 'reason': 'Replicas must be from 1 to 5.', 'applied': False, 'tools': names}`

## 12. Which decision rules or boundary conditions should an interviewer challenge?

The implementation in [`src/k8sagent/agent.py`](src/k8sagent/agent.py#L6) branches on:

- `image.endswith(':latest') or ':' not in image`
- `not 1 <= replicas <= 5`
- `any((word in goal.lower() for word in ('apply', 'delete', 'prod')))`

A useful extension is a table-driven test that covers each condition just below, at, and above its boundary where applicable. These expressions are the current rules; changing them changes behavior and should be justified by the project’s acceptance criteria.
