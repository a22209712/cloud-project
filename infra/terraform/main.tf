module "primary" {
  source = "./modules/infrastructure"

  providers = {
    aws = aws
  }

  project_name = "cloud-project"
  environment  = "dev"

  aws_region = "eu-west-1"

  availability_zone_1 = "eu-west-1a"
  availability_zone_2 = "eu-west-1b"

  vpc_cidr              = "10.10.0.0/16"
  public_subnet_cidr    = "10.10.1.0/24"
  private_subnet_1_cidr = "10.10.2.0/24"
  private_subnet_2_cidr = "10.10.3.0/24"

  key_name = "cloud-project-key"

  create_database = true
  create_sqs      = true
}

module "standby" {
  source = "./modules/infrastructure"

  providers = {
    aws = aws.standby
  }

  project_name = "cloud-project"
  environment  = "standby"

  aws_region = "eu-central-1"

  availability_zone_1 = "eu-central-1a"
  availability_zone_2 = "eu-central-1b"

  vpc_cidr              = "10.20.0.0/16"
  public_subnet_cidr    = "10.20.1.0/24"
  private_subnet_1_cidr = "10.20.2.0/24"
  private_subnet_2_cidr = "10.20.3.0/24"

  key_name = "cloud-project-key"

  create_database = false
  create_sqs      = false
}


module "disaster_recovery" {
  source = "./modules/disaster_recovery"

  providers = {
    aws = aws
  }

  project_name = "cloud-project"

  primary_instance_id = module.primary.instance_id
  standby_instance_id = module.standby.instance_id

  primary_region = "eu-west-1"
  standby_region = "eu-central-1"
}