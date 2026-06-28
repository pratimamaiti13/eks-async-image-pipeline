import json
import os
import time
from pathlib import Path

from app.services.image_processor import ImageProcessor
from app.services.job_service import job_service
from app.services.s3_service import S3Service
from app.services.sqs import SQSService

s3_service = S3Service()


def cleanup_tmp_files(*paths: str):
    """Best-effort removal of local /tmp files. Guarded individually so a
    missing file (e.g. download never succeeded) doesn't raise inside cleanup
    itself - this runs in a `finally` block and should never throw."""
    for path in paths:
        try:
            if path and Path(path).exists():
                os.remove(path)
        except OSError as e:
            # Not worth failing the job over a cleanup error - just log it.
            print(f"Warning: failed to remove {path}: {e}")


def start_worker():
    print("Worker started...")

    while True:
        messages = SQSService().receive_message()

        if messages:
            message = messages[0]
            body = json.loads(message["Body"])
            job_id = body["job_id"]
            object_key = body["object_key"]

            print(f"Processing Job: {job_id}")

            original_path = f"/tmp/original/{Path(object_key).name}"
            processed_path = f"/tmp/processed/{Path(object_key).name}"

            try:
                job_service.mark_processing(job_id)
                print("Database updated.")

                print("Downloading image from S3...")
                s3_service.download_file(object_key, original_path)
                print("Image downloaded.")

                ImageProcessor.resize(original_path, processed_path)
                print(f"Processed image saved to {processed_path}")

                processed_object_key = f"processed/{Path(object_key).name}"

                print("Uploading processed image to S3...")
                s3_service.upload_file(processed_path, processed_object_key)
                print(f"Processed image uploaded to S3: {processed_object_key}")

                job_service.mark_completed(job_id, processed_object_key)
                print("Job marked as completed.")

                SQSService().delete_message(message["ReceiptHandle"])
                print("SQS message deleted.")

            except Exception as e:
                print(f"Job {job_id} failed: {e}")
                job_service.mark_failed(job_id, str(e))
                # Deliberately NOT deleting the SQS message here - let it become
                # visible again after the visibility timeout so SQS's own retry
                # mechanism (and eventually the DLQ) handles redelivery.

            finally:
                # Runs whether the job succeeded or failed, and regardless of
                # which step failed - keeps /tmp from accumulating leftovers
                # across many processed (or repeatedly retried) jobs.
                cleanup_tmp_files(original_path, processed_path)

        time.sleep(2)


if __name__ == "__main__":
    start_worker()