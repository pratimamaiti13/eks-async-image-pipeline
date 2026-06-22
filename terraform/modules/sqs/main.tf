# Day 1 TODO:
#   - aws_sqs_queue "jobs" - main queue, visibility_timeout_seconds tuned to worker
#     processing time (start ~60s, revisit once Day 4-6 worker is timed)
#   - aws_sqs_queue "jobs_dlq" - dead-letter queue
#   - redrive_policy on "jobs" pointing at "jobs_dlq", maxReceiveCount ~3
#     (this matters for Day 13-14: a poison-pill job that always fails should land
#      in the DLQ, not loop forever - worth deliberately testing as a chaos scenario)

variable "project_name" {
  type = string
}

# --- resources go here ---

output "queue_url" {
  value = null # TODO
}

output "queue_arn" {
  value = null # TODO - needed for IRSA policy on worker service
}

output "dlq_url" {
  value = null # TODO
}
