import uuid
from sqlalchemy import text
from app.db.database import SessionLocal

MAX_RETRIES = 3


class JobStatus:
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"


class job_service:

    @staticmethod
    def create_job(object_key: str):
        db = SessionLocal()
        try:
            job_id = str(uuid.uuid4())

            db.execute(
                text("""
                    INSERT INTO jobs (
                        job_id,
                        status,
                        original_s3_key,
                        retry_count,
                        created_at,
                        updated_at
                    )
                    VALUES (
                        :job_id,
                        CAST(:status AS job_status),
                        :key,
                        0,
                        NOW(),
                        NOW()
                    )
                """),
                {
                    "job_id": job_id,
                    "status": JobStatus.PENDING,
                    "key": object_key
                }
            )

            db.commit()
            return job_id

        finally:
            db.close()

    @staticmethod
    def mark_processing(job_id: str):
        db = SessionLocal()
        try:
            db.execute(
                text("""
                    UPDATE jobs
                    SET status = CAST(:processing AS job_status),
                        processing_started_at = NOW(),
                        updated_at = NOW()
                    WHERE job_id = :job_id
                    AND status = CAST(:pending AS job_status)
                """),
                {
                    "job_id": job_id,
                    "processing": JobStatus.PROCESSING,
                    "pending": JobStatus.PENDING
                }
            )
            db.commit()
        finally:
            db.close()

    @staticmethod
    def mark_completed(job_id: str, processed_key: str):
        db = SessionLocal()
        try:
            db.execute(
                text("""
                    UPDATE jobs
                    SET status = CAST(:completed AS job_status),
                        results = jsonb_build_object('processed_s3_key', :key),
                        completed_at = NOW(),
                        updated_at = NOW()
                    WHERE job_id = :job_id
                """),
                {
                    "job_id": job_id,
                    "key": processed_key,
                    "completed": JobStatus.COMPLETED
                }
            )
            db.commit()
        finally:
            db.close()

    @staticmethod
    def mark_failed(job_id: str, error: str):
        db = SessionLocal()
        try:
            db.execute(
                text("""
                    UPDATE jobs
                    SET retry_count = retry_count + 1,
                        error_message = :error,
                        status = CASE
                            WHEN retry_count + 1 >= :max_retry
                                THEN CAST(:failed AS job_status)
                            ELSE CAST(:pending AS job_status)
                        END,
                        updated_at = NOW()
                    WHERE job_id = :job_id
                """),
                {
                    "job_id": job_id,
                    "error": error,
                    "max_retry": MAX_RETRIES,
                    "failed": JobStatus.FAILED,
                    "pending": JobStatus.PENDING
                }
            )
            db.commit()
        finally:
            db.close()