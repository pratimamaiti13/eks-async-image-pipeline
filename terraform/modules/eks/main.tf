############################################
# EKS CLUSTER IAM ROLE
############################################

resource "aws_iam_role" "eks_cluster_role" {
  name = "${var.project_name}-eks-cluster-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"

    Statement = [{
      Effect = "Allow"

      Principal = {
        Service = "eks.amazonaws.com"
      }

      Action = "sts:AssumeRole"
    }]
  })
}

resource "aws_iam_role_policy_attachment" "cluster_policy" {
  role       = aws_iam_role.eks_cluster_role.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonEKSClusterPolicy"
}

############################################
# NODE IAM ROLE
############################################

resource "aws_iam_role" "node_role" {
  name = "${var.project_name}-node-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"

    Statement = [{
      Effect = "Allow"

      Principal = {
        Service = "ec2.amazonaws.com"
      }

      Action = "sts:AssumeRole"
    }]
  })
}

resource "aws_iam_role_policy_attachment" "worker_node_policy" {
  role       = aws_iam_role.node_role.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonEKSWorkerNodePolicy"
}

resource "aws_iam_role_policy_attachment" "cni_policy" {
  role       = aws_iam_role.node_role.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonEKS_CNI_Policy"
}

resource "aws_iam_role_policy_attachment" "ecr_policy" {
  role       = aws_iam_role.node_role.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonEC2ContainerRegistryReadOnly"
}

############################################
# EKS CLUSTER
############################################

resource "aws_eks_cluster" "this" {
  name     = "${var.project_name}-cluster"
  role_arn = aws_iam_role.eks_cluster_role.arn

  version = var.cluster_version

  enabled_cluster_log_types = [
    "api",
    "audit",
    "authenticator"
  ]

  vpc_config {
    subnet_ids = var.private_subnet_ids
  }

  depends_on = [
    aws_iam_role_policy_attachment.cluster_policy
  ]
}

############################################
# GENERAL NODE GROUP
############################################

resource "aws_eks_node_group" "general" {

  cluster_name    = aws_eks_cluster.this.name
  node_group_name = "general"

  node_role_arn = aws_iam_role.node_role.arn

  subnet_ids = var.private_subnet_ids

  instance_types = [
    var.general_node_instance_type
  ]

  ami_type = "AL2023_x86_64_STANDARD"

  capacity_type = "ON_DEMAND"

  labels = {
    workload = "general"
  }

  scaling_config {
    desired_size = 2
    min_size     = 2
    max_size     = 4
  }

  depends_on = [
    aws_iam_role_policy_attachment.worker_node_policy,
    aws_iam_role_policy_attachment.cni_policy,
    aws_iam_role_policy_attachment.ecr_policy
  ]
}

############################################
# WORKER NODE GROUP (SPOT)
############################################

resource "aws_eks_node_group" "worker" {

  cluster_name    = aws_eks_cluster.this.name
  node_group_name = "worker"

  node_role_arn = aws_iam_role.node_role.arn

  subnet_ids = var.private_subnet_ids

  instance_types = [
    var.worker_node_instance_type
  ]

  ami_type = "AL2023_x86_64_STANDARD"

  capacity_type = "SPOT"

  labels = {
    workload = "worker"
  }

  taint {
    key    = "workload"
    value  = "worker"
    effect = "NO_SCHEDULE"
  }

  scaling_config {
    desired_size = 1
    min_size     = 1
    max_size     = 10
  }

  depends_on = [
    aws_iam_role_policy_attachment.worker_node_policy,
    aws_iam_role_policy_attachment.cni_policy,
    aws_iam_role_policy_attachment.ecr_policy
  ]
}

############################################
# EKS MANAGED ADDONS
############################################

resource "aws_eks_addon" "vpc_cni" {
  cluster_name = aws_eks_cluster.this.name
  addon_name   = "vpc-cni"

  depends_on = [
    aws_eks_node_group.general,
    aws_eks_node_group.worker
  ]
}

resource "aws_eks_addon" "coredns" {
  cluster_name = aws_eks_cluster.this.name
  addon_name   = "coredns"

  depends_on = [
    aws_eks_node_group.general,
    aws_eks_node_group.worker
  ]
}

resource "aws_eks_addon" "kube_proxy" {
  cluster_name = aws_eks_cluster.this.name
  addon_name   = "kube-proxy"

  depends_on = [
    aws_eks_node_group.general,
    aws_eks_node_group.worker
  ]
}

############################################
# OIDC PROVIDER (IRSA FOUNDATION)
############################################

data "tls_certificate" "eks" {
  url = aws_eks_cluster.this.identity[0].oidc[0].issuer
}

resource "aws_iam_openid_connect_provider" "eks" {

  url = aws_eks_cluster.this.identity[0].oidc[0].issuer

  client_id_list = [
    "sts.amazonaws.com"
  ]

  thumbprint_list = [
    data.tls_certificate.eks.certificates[0].sha1_fingerprint
  ]
}