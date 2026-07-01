############################################
# Stage 1 - Builder
############################################
FROM python:3.12-slim AS builder

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

COPY . .

############################################
# Stage 2 - Runtime
############################################
FROM python:3.12-slim

WORKDIR /app

RUN apt-get update && \
    apt-get install -y procps && \
    rm -rf /var/lib/apt/lists/*

COPY --from=builder /install /usr/local
COPY --from=builder /app /app

CMD ["python", "-u", "-m", "app.worker"]