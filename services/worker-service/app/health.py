"""
Tiny FastAPI app exposing only /healthz and /ready for the worker service.

The worker's real job (poll_loop in worker.py) isn't HTTP-driven, but K8s liveness/
readiness probes need something to hit over HTTP. Run this alongside poll_loop
(separate thread or separate container in the same pod - decide on approach Day 4-6;
a sidecar-free single-process-with-thread is simplest for now).
"""

from fastapi import FastAPI

health_app = FastAPI(title="worker-service-health")


@health_app.get("/healthz")
def healthz():
    return {"status": "ok"}


@health_app.get("/ready")
def ready():
    # TODO Day 7-10: check Postgres + SQS connectivity, same pattern as api-service
    return {"status": "ready"}
