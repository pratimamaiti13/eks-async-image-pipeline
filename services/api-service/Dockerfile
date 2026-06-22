# Day 4-6 TODO: confirm base image version, pin it. Using slim to keep image size down
# since this gets pulled by every pod on every scale-up/rollout.

FROM python:3.12-slim AS builder

WORKDIR /build
COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

FROM python:3.12-slim

# Non-root user - flagged in the original plan as a deliberate hardening step,
# worth keeping even on a personal project so the habit is real, not just stated.
RUN useradd --create-home --shell /bin/bash appuser

WORKDIR /app
COPY --from=builder /root/.local /home/appuser/.local
COPY app/ ./app/

ENV PATH=/home/appuser/.local/bin:$PATH \
    PYTHONUNBUFFERED=1

USER appuser

EXPOSE 8000

# TODO Day 4-6: add HEALTHCHECK instruction once /healthz is implemented
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
