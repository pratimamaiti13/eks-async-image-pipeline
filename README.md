# Async image-processing platform on AWS EKS

A small, infrastructure project built with Terraform, Docker, and Kubernetes.

## What it does

An API service accepts image uploads and immediately returns a job ID. The actual
thumbnail-generation work (CPU-bound, variable latency) happens asynchronously: the API
drops a job onto an SQS queue, and a separate worker service pulls jobs off the queue,
generates thumbnails, and writes results to Postgres. This way a slow or backed-up worker
never blocks the API.

Workers autoscale based on **SQS queue depth** (via KEDA), not CPU — queue depth is the more
direct signal of real backlog for this kind of workload. The API autoscales on CPU (HPA).
Nodes scale via Cluster Autoscaler. Everything runs multi-AZ for fault tolerance.

After deliberately breaking things (killing pods, draining nodes, forcing bad deploys,
RDS failover), a small script sends the relevant logs/events to an LLM for a structured
root-cause writeup — the same category of tool used in real incident response, validated
here against failures triggered on purpose.

## Architecture

See `docs/architecture.md` (diagram + writeup, added on Day 15).

High level:

```
User -> ALB Ingress -> API service (FastAPI, on-demand nodes)
                              |
                        SQS queue
                              |
                     Worker service (FastAPI, spot nodes)
                              |
                        RDS Postgres (multi-AZ)
```

## Repo structure

```
terraform/          # VPC, EKS, RDS, SQS, ECR - infra as code
services/
  api-service/       # FastAPI: accepts uploads, enqueues jobs
  worker-service/     # FastAPI: polls queue, processes images, writes results
k8s/                 # Kubernetes manifests (base + dev overlay)
scripts/             # Python automation: cost guard, load test, chaos runner, incident diagnosis, teardown check
docs/                # Architecture notes, war stories, diagrams
```

## Cost discipline

This is a personal project, not a production system - it is built to be destroyed
nightly. `terraform apply` at the start of a work session, `terraform destroy` at the
end. See `scripts/infra_cost_guard.py`.

## Status

Work in progress - see commit history for day-by-day build log.
