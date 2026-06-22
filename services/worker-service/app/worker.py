"""
Worker service - Day 4-6.

This is a background poller, not a typical request/response API - it doesn't serve
HTTP traffic for its core job (though it exposes /healthz and /ready for K8s probes,
same as api-service, run on a small embedded FastAPI app just for those two endpoints).

Responsibilities:
  1. Long-poll SQS for messages.
  2. For each message: fetch the original image, generate thumbnails (2-3 sizes) with
     Pillow - this is the genuinely CPU-bound, variable-latency work that justifies
     the whole async/queue design. Larger images take longer; that's real, not faked.
  3. Write result (thumbnail locations) to Postgres, update job status to "done".
  4. Delete the SQS message only after the DB write succeeds (so a crash mid-processing
     means the message becomes visible again after visibility_timeout and gets retried -
     this is exactly the at-least-once delivery behavior worth calling out as a real
     distributed systems property, not a bug).
  5. /healthz, /ready - same pattern as api-service.

Idempotency note (Day 13-14 relevant): since SQS gives at-least-once delivery, the same
job_id could be processed twice. We are NOT adding Redis-based dedup (decided to skip
Redis for this project) - instead, the DB write should be an idempotent UPSERT keyed on
job_id, so a duplicate delivery just overwrites the same result rather than corrupting
state. Worth a line in the README under "design decisions."
"""

import time


def poll_loop():
    # TODO Day 4-6:
    #   while True:
    #     messages = sqs_client.receive_message(...)
    #     for msg in messages:
    #         process_one(msg)
    pass


def process_one(message):
    # TODO Day 4-6:
    #   1. parse job_id + image location from message body
    #   2. fetch image
    #   3. generate thumbnails with Pillow (e.g. 128x128, 512x512)
    #   4. UPSERT result into Postgres (idempotent on job_id)
    #   5. delete message from SQS
    pass


if __name__ == "__main__":
    # TODO Day 4-6: also start a tiny FastAPI app in a separate thread/process for
    # /healthz and /ready, since K8s probes need an HTTP endpoint to hit even though
    # this service's main job (polling) isn't HTTP-driven.
    poll_loop()
