terraform {
  backend "s3" {
    bucket         = "cloud-project-968477812241-tfstate"
    key            = "env/dev/terraform.tfstate"
    region         = "eu-west-1"
    dynamodb_table = "cloud-project-tf-locks"
    encrypt        = true
  }
}