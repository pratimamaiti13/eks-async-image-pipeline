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

resource "aws_db_subnet_group" "postgres" {
  name       = "${var.project_name}-db-subnet-group"
  subnet_ids = var.private_subnet_ids

  tags = {
    Name = "${var.project_name}-db-subnet-group"
  }
}

resource "aws_security_group" "rds" {
  name        = "${var.project_name}-rds-sg"
  description = "Allow Postgres access from EKS nodes"
  vpc_id      = var.vpc_id

  ingress {
    description     = "Postgres from EKS"
    from_port       = 5432
    to_port         = 5432
    protocol        = "tcp"
    security_groups = [var.eks_node_sg_id]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "${var.project_name}-rds-sg"
  }
}

resource "random_password" "db" {
  length  = 20
  special = false
}

# resource "aws_secretsmanager_secret" "rds" {
#   name = "${var.project_name}-rds-credentials"
# }

# resource "aws_secretsmanager_secret_version" "rds" {
#   secret_id = aws_secretsmanager_secret.rds.id

#   secret_string = jsonencode({
#     username = var.db_username
#     password = random_password.db.result
#   })
# }

resource "aws_db_instance" "postgres" {
  identifier = "${var.project_name}-postgres"

  engine         = "postgres"
  engine_version = "18.3"

  instance_class = var.db_instance_class

  allocated_storage = 20
  storage_type      = "gp3"

  db_name  = var.db_name
  username = var.db_username
  password = random_password.db.result

  db_subnet_group_name = aws_db_subnet_group.postgres.name

  vpc_security_group_ids = [
    aws_security_group.rds.id
  ]

  multi_az = var.db_multi_az

  publicly_accessible = false

  skip_final_snapshot = true

  tags = {
    Name = "${var.project_name}-postgres"
  }
}
