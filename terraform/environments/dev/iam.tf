############################################
# API IAM POLICY DOCUMENT
############################################

data "aws_iam_policy_document" "api" {

  statement {

    sid = "S3Access"

    actions = [
      "s3:GetObject",
      "s3:PutObject"
    ]

    resources = [
      "${module.s3.bucket_arn}/*"
    ]
  }

  statement {

    sid = "SQSSend"

    actions = [
      "sqs:GetQueueUrl",
      "sqs:SendMessage"
    ]

    resources = [
      module.sqs.queue_arn
    ]
  }
}

############################################
# WORKER IAM POLICY DOCUMENT
############################################

data "aws_iam_policy_document" "worker" {

  statement {

    sid = "S3Access"

    actions = [
      "s3:GetObject",
      "s3:PutObject"
    ]

    resources = [
      "${module.s3.bucket_arn}/*"
    ]
  }

  statement {

    sid = "SQSReceive"

    actions = [
      "sqs:GetQueueUrl",
      "sqs:ReceiveMessage",
      "sqs:DeleteMessage",
      "sqs:GetQueueAttributes"
    ]

    resources = [
      module.sqs.queue_arn
    ]
  }
}


############################################
# API IAM POLICY
############################################

resource "aws_iam_policy" "api" {

  name = "${var.project_name}-api-policy"

  policy = data.aws_iam_policy_document.api.json
}

############################################
# WORKER IAM POLICY
############################################

resource "aws_iam_policy" "worker" {

  name = "${var.project_name}-worker-policy"

  policy = data.aws_iam_policy_document.worker.json
}


############################################
# AWS LOAD BALANCER CONTROLLER IAM POLICY
############################################

resource "aws_iam_policy" "alb_controller" {

  name = "AWSLoadBalancerControllerIAMPolicy"

  policy = file("${path.module}/iam_policy.json")
}

############################################
# API IRSA
############################################

module "api_irsa" {

  source = "../../modules/irsa"

  role_name = "${var.project_name}-api-irsa-role"

  namespace = "imgproc"

  service_account_name = "api-service"

  oidc_provider_arn = module.eks.oidc_provider_arn

  oidc_issuer_without_https = replace(
    module.eks.oidc_issuer_url,
    "https://",
    ""
  )

  policy_arn = aws_iam_policy.api.arn
}

############################################
# WORKER IRSA
############################################

module "worker_irsa" {

  source = "../../modules/irsa"

  role_name = "${var.project_name}-worker-irsa-role"

  namespace = "imgproc"

  service_account_name = "worker-service"

  oidc_provider_arn = module.eks.oidc_provider_arn

  oidc_issuer_without_https = replace(
    module.eks.oidc_issuer_url,
    "https://",
    ""
  )

  policy_arn = aws_iam_policy.worker.arn
}


############################################
# AWS LOAD BALANCER CONTROLLER IRSA
############################################

module "aws_load_balancer_controller_irsa" {

  source = "../../modules/irsa"

  role_name = "${var.project_name}-alb-controller-role"

  namespace = "kube-system"

  service_account_name = "aws-load-balancer-controller"

  oidc_provider_arn = module.eks.oidc_provider_arn

  oidc_issuer_without_https = replace(
    module.eks.oidc_issuer_url,
    "https://",
    ""
  )

  policy_arn = aws_iam_policy.alb_controller.arn
}