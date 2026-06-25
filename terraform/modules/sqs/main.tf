# Day 1 TODO:
#   - aws_sqs_queue "jobs" - main queue, visibility_timeout_seconds tuned to worker
#     processing time (start ~60s, revisit once Day 4-6 worker is timed)
#   - aws_sqs_queue "jobs_dlq" - dead-letter queue
#   - redrive_policy on "jobs" pointing at "jobs_dlq", maxReceiveCount ~3
#     (this matters for Day 13-14: a poison-pill job that always fails should land
#      in the DLQ, not loop forever - worth deliberately testing as a chaos scenario)



resource "aws_sqs_queue" "dlq" {
  name = "${var.project_name}-jobs-dlq"

  tags = {
    Name = "${var.project_name}-jobs-dlq"
  }
}

resource "aws_sqs_queue" "main" {
  name = "${var.project_name}-jobs"

  visibility_timeout_seconds = 60

  redrive_policy = jsonencode({
    deadLetterTargetArn = aws_sqs_queue.dlq.arn
    maxReceiveCount     = 3
  })

  tags = {
    Name = "${var.project_name}-jobs"
  }
}