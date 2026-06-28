import boto3

from app.config import settings


class SQSService:
    def __init__(self):
        self.client = boto3.client(
            "sqs",
            region_name=settings.aws_region,
            aws_access_key_id=settings.aws_access_key_id,
            aws_secret_access_key=settings.aws_secret_access_key,
        )

        response = self.client.get_queue_url(
            QueueName=settings.sqs_queue_name
        )

        self.queue_url = response["QueueUrl"]

    def receive_message(self):
        response = self.client.receive_message(
            QueueUrl=self.queue_url,
            MaxNumberOfMessages=1,
            WaitTimeSeconds=10,
        )

        return response.get("Messages", [])
    
    def delete_message(self, receipt_handle: str):
        self.client.delete_message(
            QueueUrl=self.queue_url,
            ReceiptHandle=receipt_handle,
    )


sqs_service = SQSService()