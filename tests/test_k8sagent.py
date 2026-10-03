from fastapi.testclient import TestClient
from k8sagent.main import app

def test_renders_and_refuses_latest():
    client = TestClient(app)
    good = client.post("/agent/run", json={"goal": "inspect the billing pods", "image": "billing:1.4.2", "replicas": 2}).json()
    assert good["applied"] is False
    assert good["tools"] == ["get_pods", "read_logs", "render_manifest"]
    assert good["manifest"]["image"] == "billing:1.4.2"
    bad = client.post("/agent/run", json={"goal": "apply this", "image": "billing:latest", "replicas": 2}).json()
    assert bad["refused"] is True
    assert bad["applied"] is False
