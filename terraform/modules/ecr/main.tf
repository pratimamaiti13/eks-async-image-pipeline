# Day 1 TODO:
#   - aws_ecr_repository for each name in var.repo_names (api-service, worker-service)
#   - lifecycle_policy: keep last ~5 images, expire untagged after a few days
#     (small but real cost/hygiene detail worth mentioning in the README)


resource "aws_ecr_repository" "this" {
  for_each = toset(var.repo_names)

  name                 = "${var.project_name}-${each.value}"
  image_tag_mutability = "MUTABLE"

  encryption_configuration {
    encryption_type = "AES256"
  }
}

resource "aws_ecr_lifecycle_policy" "this" {
  for_each = aws_ecr_repository.this

  repository = each.value.name

  policy = jsonencode({
    rules = [
      {
        rulePriority = 1
        description  = "Keep last 5 images"

        selection = {
          tagStatus   = "any"
          countType   = "imageCountMoreThan"
          countNumber = 5
        }

        action = {
          type = "expire"
        }
      }
    ]
  })
}
