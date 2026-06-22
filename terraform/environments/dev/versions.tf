terraform {
  required_version = ">= 1.7.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
    kubernetes = {
      source  = "hashicorp/kubernetes"
      version = "~> 2.30"
    }
  }

  # backend "s3" {
  #   bucket = "REPLACE_ME-tfstate-bucket"
  #   key    = "dev/terraform.tfstate"
  #   region = "ap-south-1"
  # }
}

provider "aws" {
  region = var.aws_region

  default_tags {
    tags = {
      Project   = "infra-eks-project"
      ManagedBy = "terraform"
      Env       = "dev"
    }
  }
}
