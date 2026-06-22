# Day 1-3 TODO:
#   - aws_eks_cluster (control plane) in private subnets
#   - IRSA setup (OIDC provider) - needed Day 7-10 for pod-level AWS permissions
#   - node group "general": on-demand, var.general_node_instance_type, runs api-service
#   - node group "worker": SPOT, var.worker_node_instance_type, runs worker-service
#     (taint this node group e.g. workload=worker:NoSchedule so only worker pods land here,
#      tolerate it explicitly in the worker Deployment spec)
#   - Cluster Autoscaler IAM role/policy (Day 11-12 installs the addon itself via k8s/)

variable "project_name" {
  type = string
}

variable "cluster_version" {
  type = string
}

variable "vpc_id" {
  type = string
}

variable "private_subnet_ids" {
  type = list(string)
}

variable "general_node_instance_type" {
  type = string
}

variable "worker_node_instance_type" {
  type = string
}

# --- resources go here ---

output "cluster_name" {
  value = null # TODO
}

output "cluster_endpoint" {
  value = null # TODO
}

output "node_security_group_id" {
  value = null # TODO - needed by RDS module for ingress rule
}

output "oidc_provider_arn" {
  value = null # TODO - needed for IRSA role trust policies
}
