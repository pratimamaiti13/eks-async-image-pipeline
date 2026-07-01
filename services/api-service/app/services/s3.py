import uuid

import boto3

from app.config import settings


class S3Service:
    def __init__(self):
        self.client = boto3.client(
            "s3",
            region_name=settings.aws_region,
        )

    def upload_file(self, file_obj, filename: str) -> str:
        object_key = f"{uuid.uuid4()}-{filename}"

        self.client.upload_fileobj(
            Fileobj=file_obj,
            Bucket=settings.s3_bucket_name,
            Key=object_key,
        )

        return object_key


s3_service = S3Service()