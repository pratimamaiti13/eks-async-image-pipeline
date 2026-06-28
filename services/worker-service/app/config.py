import os


class Settings:
    aws_region = os.getenv("AWS_DEFAULT_REGION")
    aws_access_key_id = os.getenv("AWS_ACCESS_KEY_ID")
    aws_secret_access_key = os.getenv("AWS_SECRET_ACCESS_KEY")

    sqs_queue_name = os.getenv("SQS_QUEUE_NAME")
    s3_bucket_name = os.getenv("S3_BUCKET_NAME")

    database_url = os.getenv("DATABASE_URL")


settings = Settings()