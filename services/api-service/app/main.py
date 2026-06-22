"""
API service - Day 4-6.

Responsibilities (kept deliberately narrow):
  1. POST /jobs - accept an image upload, write a job row to Postgres (status=pending),
     push a message onto SQS with the job id, return {"job_id": ...} immediately.
  2. GET /jobs/{job_id} - read job status/result from Postgres. This is the endpoint
     that gets polled by seed_and_test.py and load_test.py - no blocking on inference here,
     that's the whole point of the queue.
  3. GET /healthz - liveness: process is up.
  4. GET /ready - readiness: can reach Postgres AND SQS. Wired into K8s probes Day 7-10.

Deliberately NOT doing here: image processing itself. That's worker-service's job.
This service should never block on anything slow.
"""

from fastapi import FastAPI, UploadFile, HTTPException

app = FastAPI(title="api-service")


@app.get("/healthz")
def healthz():
    # TODO Day 4-6: trivial liveness check, just confirms the process is responsive
    return {"status": "ok"}


@app.get("/ready")
def ready():
    # TODO Day 7-10: check DB connection + SQS reachability, return 503 if either fails
    # This matters for K8s readiness probes - a pod that can't reach its dependencies
    # shouldn't receive traffic from the Service.
    return {"status": "ready"}


@app.post("/jobs")
async def create_job(file: UploadFile):
    # TODO Day 4-6:
    #   1. validate file is an image, reject oversized/invalid uploads
    #   2. store original (S3, or pass-through to worker - decide during Day 4-6)
    #   3. INSERT job row into Postgres with status="pending"
    #   4. send_message to SQS with job_id + image location
    #   5. return {"job_id": job_id} WITHOUT waiting for processing
    raise HTTPException(status_code=501, detail="not implemented yet")


@app.get("/jobs/{job_id}")
async def get_job(job_id: str):
    # TODO Day 4-6: SELECT job by id from Postgres, return status + result location if done
    raise HTTPException(status_code=501, detail="not implemented yet")
