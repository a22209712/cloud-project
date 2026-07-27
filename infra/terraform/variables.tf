variable "project_name" {
  default = "cloud-project"
}

variable "environment" {
  default = "dev"
}

variable "region" {
  default = "eu-west-1"
}

variable "vpc_cidr" {
  default = "10.10.0.0/16"
}

variable "public_subnet_cidr" {
  default = "10.10.1.0/24"
}

variable "private_subnet1_cidr" {
  default = "10.10.2.0/24"
}

variable "private_subnet2_cidr" {
  default = "10.10.3.0/24"
}