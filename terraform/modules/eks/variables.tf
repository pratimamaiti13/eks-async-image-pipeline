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