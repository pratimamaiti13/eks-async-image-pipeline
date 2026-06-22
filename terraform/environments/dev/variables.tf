variable "aws_region" {
  description = "AWS region to deploy into"
  type        = string
  default     = "ap-south-1"
}

variable "project_name" {
  description = "Short name used to tag/prefix all resources"
  type        = string
  default     = "imgproc"
}

variable "vpc_cidr" {
  description = "CIDR block for the VPC"
  type        = string
  default     = "10.20.0.0/16"
}

variable "azs" {
  description = "Availability zones to spread subnets/nodes across"
  type        = list(string)
  default     = ["ap-south-1a", "ap-south-1b"]
}

variable "eks_cluster_version" {
  description = "Kubernetes version for the EKS cluster"
  type        = string
  default     = "1.30"
}

variable "general_node_instance_type" {
  description = "Instance type for the general (on-demand) node group running the API service"
  type        = string
  default     = "t3.small"
}

variable "worker_node_instance_type" {
  description = "Instance type for the worker (spot) node group running the image-processing worker"
  type        = string
  default     = "t3.medium"
}

variable "db_instance_class" {
  description = "RDS instance class"
  type        = string
  default     = "db.t3.micro"
}

variable "db_multi_az" {
  description = "Whether RDS runs multi-AZ. Toggle on only when demoing HA/failover to control cost."
  type        = bool
  default     = false
}

variable "db_name" {
  description = "Postgres database name"
  type        = string
  default     = "imgproc"
}

variable "db_username" {
  description = "Postgres master username"
  type        = string
  default     = "imgproc_admin"
  sensitive   = true
}
