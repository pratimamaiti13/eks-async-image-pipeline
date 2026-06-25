# Day 1-3 build order:
#   1. module.vpc        - public/private subnets, NAT, multi-AZ
#   2. module.ecr         - container registries for api-service and worker-service
#   3. module.eks         - cluster + 2 node groups (general on-demand, worker spot)
#   4. module.rds         - Postgres, single-AZ to start, multi-AZ toggle for Day 11-12
#   5. module.sqs         - job queue + dead-letter queue
#
# Each module is intentionally separate so any one piece can be applied/destroyed
# independently while iterating, and so the dev->later-env path is just adding
# another environments/<env> folder that calls the same modules with different vars.

module "vpc" {
  source = "../../modules/vpc"

  project_name = var.project_name
  vpc_cidr     = var.vpc_cidr
  azs          = var.azs
}

# module "ecr" {
#   source = "../../modules/ecr"

#   project_name = var.project_name
#   repo_names   = ["api-service", "worker-service"]
# }

module "eks" {
  source = "../../modules/eks"

  project_name                = var.project_name
  cluster_version              = var.eks_cluster_version
  vpc_id                       = module.vpc.vpc_id
  private_subnet_ids           = module.vpc.private_subnet_ids
  general_node_instance_type   = var.general_node_instance_type
  worker_node_instance_type    = var.worker_node_instance_type
}

module "rds" {
  source = "../../modules/rds"

  project_name        = var.project_name
  db_instance_class   = var.db_instance_class
  db_multi_az         = var.db_multi_az
  db_name             = var.db_name
  db_username         = var.db_username
  vpc_id              = module.vpc.vpc_id
  private_subnet_ids  = module.vpc.private_subnet_ids
  eks_node_sg_id       = module.eks.cluster_security_group_id
}

# module "sqs" {
#   source = "../../modules/sqs"

#   project_name = var.project_name
# }
