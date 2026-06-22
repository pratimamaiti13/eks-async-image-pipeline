# Day 1 TODO:
#   - aws_ecr_repository for each name in var.repo_names (api-service, worker-service)
#   - lifecycle_policy: keep last ~5 images, expire untagged after a few days
#     (small but real cost/hygiene detail worth mentioning in the README)

variable "project_name" {
  type = string
}

variable "repo_names" {
  type = list(string)
}

# --- resources go here ---

output "repository_urls" {
  description = "Map of repo name to full ECR URL"
  value       = {} # TODO
}
