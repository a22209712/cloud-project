output "vpc_id" {
  value = module.primary.vpc_id
}

output "instance_public_ip" {
  value = module.primary.instance_public_ip
}

output "instance_public_dns" {
  value = module.primary.instance_public_dns
}

output "sqs_queue_url" {
  value = module.primary.queue_url
}

output "rds_endpoint" {
  value = module.primary.db_endpoint
}