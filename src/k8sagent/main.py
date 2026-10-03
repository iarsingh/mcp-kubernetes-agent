from fastapi import FastAPI
from k8sagent.agent import run

app = FastAPI()

@app.post("/agent/run")
def post_run(body: dict):
    return run(body["goal"], body["image"], body["replicas"])
