import json

import boto3

from app.config import settings


class SQSService:
    def __init__(self):
        self.client = boto3.client(
            "sqs",
            region_name=settings.aws_region,
        )

        response = self.client.get_queue_url(
            QueueName=settings.sqs_queue_name
        )

        self.queue_url = response["QueueUrl"]

    def send_message(self, job_id: str, object_key: str):
        message = {
            "job_id": job_id,
            "object_key": object_key,
        }

        self.client.send_message(
            QueueUrl=self.queue_url,
            MessageBody=json.dumps(message),
        )


sqs_service = SQSService()