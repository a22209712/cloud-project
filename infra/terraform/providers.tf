terraform {
  required_version = ">= 1.9"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = "eu-west-1"

  default_tags {
    tags = {
      Project     = "cloud-project"
      Environment = "dev"
      ManagedBy   = "terraform"
    }
  }
}

provider "aws" {
  alias  = "standby"
  region = "eu-central-1"

  default_tags {
    tags = {
      Project     = "cloud-project"
      Environment = "standby"
      ManagedBy   = "terraform"
    }
  }
}