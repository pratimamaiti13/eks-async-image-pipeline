output "eks_cluster_name" {
  description = "EKS cluster name - used for `aws eks update-kubeconfig`"
  value       = module.eks.cluster_name
}

output "eks_cluster_endpoint" {
  value = module.eks.cluster_endpoint
}

# output "ecr_repository_urls" {
#   description = "Map of service name to ECR repo URL, used when pushing images"
#   value       = module.ecr.repository_urls
# }

output "rds_endpoint" {
  value = module.rds.rds_endpoint
}

# output "rds_secret_arn" {
#   value = module.rds.rds_secret_arn
# }

output "rds_password" {
  value     = module.rds.rds_password
  sensitive = true
}

# output "sqs_queue_url" {
#   description = "SQS queue URL - injected into both services' config"
#   value       = module.sqs.queue_url
# }

# output "sqs_dlq_url" {
#   value = module.sqs.dlq_url
# }
