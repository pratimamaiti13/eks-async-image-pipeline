# Day 1 TODO:
#   - aws_vpc with var.vpc_cidr
#   - public + private subnet per AZ in var.azs
#   - 1 NAT gateway (single NAT to save cost - acceptable tradeoff for a personal project;
#     note in README that a real prod setup would use 1 NAT per AZ for true HA)
#   - internet gateway, route tables for public/private

variable "project_name" {
  type = string
}

variable "vpc_cidr" {
  type = string
}

variable "azs" {
  type = list(string)
}

# --- resources go here ---

output "vpc_id" {
  value = null # TODO: aws_vpc.this.id
}

output "public_subnet_ids" {
  value = [] # TODO
}

output "private_subnet_ids" {
  value = [] # TODO
}
