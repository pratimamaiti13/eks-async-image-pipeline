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
# API IRSA
############################################

module "api_irsa" {

  source = "../../modules/irsa"

  role_name = "${var.project_name}-api-irsa-role"

  namespace = "default"

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

  namespace = "default"

  service_account_name = "worker-service"

  oidc_provider_arn = module.eks.oidc_provider_arn

  oidc_issuer_without_https = replace(
    module.eks.oidc_issuer_url,
    "https://",
    ""
  )

  policy_arn = aws_iam_policy.worker.arn
}