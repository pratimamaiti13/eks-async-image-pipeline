############################################
# IRSA TRUST POLICY
############################################

data "aws_iam_policy_document" "trust_policy" {

  statement {

    effect = "Allow"

    actions = [
      "sts:AssumeRoleWithWebIdentity"
    ]

    principals {

      type = "Federated"

      identifiers = [
        var.oidc_provider_arn
      ]
    }

    condition {

      test = "StringEquals"

      variable = "${var.oidc_issuer_without_https}:sub"

      values = [
        "system:serviceaccount:${var.namespace}:${var.service_account_name}"
      ]
    }

    condition {

      test = "StringEquals"

      variable = "${var.oidc_issuer_without_https}:aud"

      values = [
        "sts.amazonaws.com"
      ]
    }
  }
}

############################################
# IRSA IAM ROLE
############################################

resource "aws_iam_role" "this" {

  name = var.role_name

  assume_role_policy = data.aws_iam_policy_document.trust_policy.json
}

############################################
# ATTACH IAM POLICY
############################################

resource "aws_iam_role_policy_attachment" "this" {

  role = aws_iam_role.this.name

  policy_arn = var.policy_arn
}