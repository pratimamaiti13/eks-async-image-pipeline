"""
seed_and_test.py - Day 4-6.

Purpose: integration test + demo script. Uploads a handful of sample images through
the API, polls /jobs/{job_id} until each finishes, and prints a summary - this is both
how you'll prove the system works end-to-end and how you'd demo it to anyone reviewing
the project.

Usage (planned):
    python scripts/seed_and_test.py --api-url http://<alb-dns-name> --images ./sample_images/

This deliberately does NOT use Locust/load-testing patterns - that's load_test.py's job.
This script is about correctness (did the job complete, is the result sane), not load.
"""

import argparse
import time
from pathlib import Path


def upload_image(api_url: str, image_path: Path) -> str:
    # TODO Day 4-6: POST to {api_url}/jobs with the image, return job_id
    raise NotImplementedError


def poll_until_done(api_url: str, job_id: str, timeout_s: int = 30) -> dict:
    # TODO Day 4-6: GET {api_url}/jobs/{job_id} every ~1s until status != "pending"
    # or timeout - return the final job record
    raise NotImplementedError


def main():
    parser = argparse.ArgumentParser(description="Seed sample jobs and verify end-to-end")
    parser.add_argument("--api-url", required=True)
    parser.add_argument("--images", default="./sample_images/")
    args = parser.parse_args()

    image_dir = Path(args.images)
    images = sorted(image_dir.glob("*.jpg")) + sorted(image_dir.glob("*.png"))

    if not images:
        print(f"No sample images found in {image_dir}")
        return

    results = []
    for img in images:
        job_id = upload_image(args.api_url, img)
        print(f"Uploaded {img.name} -> job {job_id}")
        result = poll_until_done(args.api_url, job_id)
        results.append((img.name, result))

    print("\nSummary:")
    for name, result in results:
        print(f"  {name}: {result}")


if __name__ == "__main__":
    main()
