variable "aws_region" {
  description = "The AWS region to deploy into"
  type        = string
}

variable "vpc_cidr" {
  description = "CIDR block for the VPC"
  type        = string
}

variable "subnet_cidr" {
  description = "CIDR block for the public subnet"
  type        = string
}

variable "instance_type" {
  description = "The EC2 instance type"
  type        = string
}

variable "public_key_path" {
  description = "Path to your local public SSH key"
  type        = string
}