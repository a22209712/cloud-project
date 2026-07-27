resource "aws_secretsmanager_secret" "db_password" {
  name = "${local.name_prefix}-db-password"
}

resource "aws_secretsmanager_secret_version" "db_password" {
  secret_id = aws_secretsmanager_secret.db_password.id

  secret_string = jsonencode({
    username = "postgres"
    password = "CloudProject123!"
  })
}

