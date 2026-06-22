# Day 1-3 TODO (single-AZ first):
#   - aws_db_subnet_group across private_subnet_ids
#   - aws_security_group allowing 5432 ingress only from eks_node_sg_id
#   - aws_db_instance: postgres, var.db_instance_class, var.multi_az (default false)
#   - random_password for master password, store in AWS Secrets Manager
#     (read by the K8s External Secrets setup, or just passed via Terraform output
#      -> manually synced into a K8s Secret for simplicity on Day 7-10)
#
# Day 11-12 TODO:
#   - flip var.multi_az = true via tfvars, terraform apply, observe failover behavior
#     (this is the HA test - documented as a war story)

variable "project_name" {
  type = string
}

variable "db_instance_class" {
  type = string
}

variable "multi_az" {
  type = bool
}

variable "db_name" {
  type = string
}

variable "db_username" {
  type      = string
  sensitive = true
}

variable "vpc_id" {
  type = string
}

variable "private_subnet_ids" {
  type = list(string)
}

variable "eks_node_sg_id" {
  type = string
}

# --- resources go here ---

output "endpoint" {
  value     = null # TODO
  sensitive = true
}

output "db_name" {
  value = null # TODO
}
