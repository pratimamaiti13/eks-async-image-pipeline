# Day 4-6 TODO: confirm base image version, pin it.

FROM python:3.12-slim AS builder

WORKDIR /build
COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

FROM python:3.12-slim

RUN useradd --create-home --shell /bin/bash appuser

WORKDIR /app
COPY --from=builder /root/.local /home/appuser/.local
COPY app/ ./app/

ENV PATH=/home/appuser/.local/bin:$PATH \
    PYTHONUNBUFFERED=1

USER appuser

EXPOSE 8001

# TODO Day 4-6: entrypoint needs to run both poll_loop() and the health_app -
# decide between a small supervisor script vs threading in worker.py itself.
CMD ["python", "-m", "app.worker"]
