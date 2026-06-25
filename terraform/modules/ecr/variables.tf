variable "repo_names" {
  description = "List of ECR repositories"
  type        = list(string)
}
variable "project_name" {
  description = "Project name to prefix resources with"
  type        = string
}