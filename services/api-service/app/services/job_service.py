import uuid

from app.db.database import get_connection


class JobService:

    def create_job(self, original_s3_key):

        job_id = uuid.uuid4()

        conn = get_connection()
        cur = conn.cursor()

        cur.execute(
            """
            INSERT INTO jobs(job_id, status, original_s3_key)
            VALUES (%s, %s, %s)
            """,
            (
                str(job_id),
                "pending",
                original_s3_key,
            ),
        )

        conn.commit()

        cur.close()
        conn.close()

        return str(job_id)


job_service = JobService()