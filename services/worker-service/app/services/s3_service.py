import boto3
from pathlib import Path

from app.config import settings


class S3Service:
    def __init__(self):
        self.s3 = boto3.client(
            "s3",
            region_name=settings.aws_region,
            aws_access_key_id=settings.aws_access_key_id,
            aws_secret_access_key=settings.aws_secret_access_key,
        )

    def upload_file(self, local_path: str, s3_key: str):
        self.s3.upload_file(
            local_path,
            settings.s3_bucket_name,
            s3_key,
        )

    def download_file(self, s3_key: str, local_path: str):
        Path(local_path).parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        self.s3.download_file(
            settings.s3_bucket_name,
            s3_key,
            local_path,
        )