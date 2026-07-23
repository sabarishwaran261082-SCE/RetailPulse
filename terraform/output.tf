# ----------------------------------------
# VPC ID
# ----------------------------------------

output "vpc_id" {
  description = "RetailPulse VPC ID"
  value       = aws_vpc.retailpulse_vpc.id
}

# ----------------------------------------
# Public Subnet ID
# ----------------------------------------

output "public_subnet_id" {
  description = "Public Subnet ID"
  value       = aws_subnet.public_subnet.id
}

# ----------------------------------------
# Security Group ID
# ----------------------------------------

output "security_group_id" {
  description = "Security Group ID"
  value       = aws_security_group.retailpulse_sg.id
}

# ----------------------------------------
# EC2 Instance ID
# ----------------------------------------

output "instance_id" {
  description = "EC2 Instance ID"
  value       = aws_instance.retailpulse_ec2.id
}

# ----------------------------------------
# Elastic IP
# ----------------------------------------

output "elastic_ip" {
  description = "Elastic IP Address"
  value       = aws_eip.retailpulse_eip.public_ip
}

# ----------------------------------------
# Public DNS
# ----------------------------------------

output "public_dns" {
  description = "Public DNS Name"
  value       = aws_instance.retailpulse_ec2.public_dns
}

# ----------------------------------------
# Streamlit URL
# ----------------------------------------

output "streamlit_url" {
  description = "RetailPulse Streamlit Application URL"

  value = "http://${aws_eip.retailpulse_eip.public_ip}:8501"
}