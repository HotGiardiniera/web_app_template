terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 3.0"
    }
  }
  backend "s3" {
    bucket = "example-infra"
    key    = "terraform/vpc/remote-state.tf"
    region = "us-east-2"
  }

  required_version = "= 0.15.5"

}

provider "aws" {
  region = var.aws_region
}