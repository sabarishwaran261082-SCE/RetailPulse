#!/bin/bash

# Update system
dnf update -y

# Install Docker
dnf install -y docker

# Start Docker
systemctl enable docker
systemctl start docker

# Install AWS CLI (if not already installed)
dnf install -y awscli

# Login to Amazon ECR
aws ecr get-login-password --region ap-south-1 | \
docker login --username AWS --password-stdin \
208519603970.dkr.ecr.ap-south-1.amazonaws.com

# Pull Docker image
docker pull 208519603970.dkr.ecr.ap-south-1.amazonaws.com/retailpulse:1.0

# Remove old container if it exists
docker rm -f retailpulse || true

# Run Streamlit container
docker run -d \
  --name retailpulse \
  --restart unless-stopped \
  -p 8501:8501 \
  208519603970.dkr.ecr.ap-south-1.amazonaws.com/retailpulse:1.0