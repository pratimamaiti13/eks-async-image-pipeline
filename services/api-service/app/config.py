from dataclasses import dataclass
import os


@dataclass
class Settings:
    database_url: str = os.getenv("DATABASE_URL")

    aws_access_key_id: str = os.getenv("AWS_ACCESS_KEY_ID")
    aws_secret_access_key: str = os.getenv("AWS_SECRET_ACCESS_KEY")
    aws_region: str = os.getenv("AWS_REGION")

    s3_bucket_name: str = os.getenv("S3_BUCKET_NAME")
    sqs_queue_name: str = os.getenv("SQS_QUEUE_NAME")


settings = Settings()