output "vpc_id" {
  value = aws_vpc.main.id
}

output "public_subnet_id" {
  value = aws_subnet.public.id
}

output "web_security_group_id" {
  value = aws_security_group.web.id
}

output "instance_id" {
  value = aws_instance.app.id
}

output "instance_public_ip" {
  value = aws_instance.app.public_ip
}

output "instance_public_dns" {
  value = aws_instance.app.public_dns
}

output "iam_role_name" {
  value = aws_iam_role.ec2_role.name
}

output "iam_instance_profile" {
  value = aws_iam_instance_profile.ec2_profile.name
}

output "db_endpoint" {
  value = var.create_database ? aws_db_instance.postgres[0].endpoint : null
}

output "queue_url" {
  value = var.create_sqs ? aws_sqs_queue.messages[0].url : null
}