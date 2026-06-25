output "rds_endpoint" {
  value     = aws_db_instance.postgres.endpoint
  sensitive = true
}

output "rds_security_group_id" {
  value = aws_security_group.rds.id
}

output "rds_password" {
  value     = random_password.db.result
  sensitive = true
}