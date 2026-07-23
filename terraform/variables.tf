variable "aws_region" {
  description = "AWS Region"
  type        = string
  default     = "ap-south-1"
}

variable "availability_zone" {
  description = "Availability Zone"
  type        = string
  default     = "ap-south-1a"
}

variable "vpc_cidr" {
  description = "VPC CIDR Block"
  type        = string
  default     = "10.0.0.0/16"
}

variable "public_subnet_cidr" {
  description = "Public Subnet CIDR"
  type        = string
  default     = "10.0.1.0/24"
}

variable "instance_type" {
  description = "EC2 Instance Type"
  type        = string
  default     = "t3.micro"
}

variable "key_name" {
  description = "Existing EC2 Key Pair Name"
  type        = string
}

variable "repository_url" {
  description = "Amazon ECR Repository URL"
  type        = string
  default     = "208519603970.dkr.ecr.ap-south-1.amazonaws.com/retailpulse"
}

variable "container_port" {
  description = "Streamlit Container Port"
  type        = number
  default     = 8501
}