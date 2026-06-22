"""
load_test.py - Day 11-12.

Purpose: generate a real, bounded amount of concurrent load (thousands, not millions -
see project notes on why "millions of users" isn't a meaningful target for a personal
project) against the API, so HPA (API pods on CPU) and KEDA (worker pods on SQS queue
depth) can be observed actually reacting in real time.

Usage (planned):
    python scripts/load_test.py --api-url http://<alb-dns-name> --concurrency 200 --total 3000

While this runs, watch scaling live in separate terminals:
    kubectl get hpa -w
    kubectl get pods -n imgproc -w
    kubectl get scaledobject -n imgproc -w   (KEDA)

This is also where the honest metrics for the resume/README come from - actual numbers
observed during this run (requests/sec sustained, time for worker pods to scale 2->6,
p99 latency under load), not invented figures.
"""

import argparse
import asyncio
import time


async def send_one_request(api_url: str, image_bytes: bytes) -> float:
    # TODO Day 11-12: httpx.AsyncClient POST to {api_url}/jobs, return latency in seconds
    raise NotImplementedError


async def run_load(api_url: str, concurrency: int, total: int):
    # TODO Day 11-12:
    #   - load one sample image into memory once, reuse for all requests
    #   - use an asyncio.Semaphore(concurrency) to bound concurrent in-flight requests
    #   - fire `total` requests total, collect latencies
    #   - print: total time, requests/sec, p50/p95/p99 latency
    raise NotImplementedError


def main():
    parser = argparse.ArgumentParser(description="Load test the API to trigger autoscaling")
    parser.add_argument("--api-url", required=True)
    parser.add_argument("--concurrency", type=int, default=200)
    parser.add_argument("--total", type=int, default=3000)
    args = parser.parse_args()

    start = time.monotonic()
    asyncio.run(run_load(args.api_url, args.concurrency, args.total))
    elapsed = time.monotonic() - start
    print(f"\nTotal wall time: {elapsed:.1f}s")


if __name__ == "__main__":
    main()
