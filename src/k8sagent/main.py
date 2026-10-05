from k8sagent.ops import router as ops_router
from fastapi import FastAPI
from k8sagent.agent import run

app = FastAPI()
app.include_router(ops_router, prefix="/v1")

@app.post("/agent/run")
def post_run(body: dict):
    return run(body["goal"], body["image"], body["replicas"])
