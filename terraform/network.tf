# -----------------------------
# Create Custom VPC
# -----------------------------
resource "aws_vpc" "retailpulse_vpc" {
  cidr_block           = var.vpc_cidr
  enable_dns_support   = true
  enable_dns_hostnames = true

  tags = {
    Name = "RetailPulse-VPC"
  }
}

# -----------------------------
# Create Public Subnet
# -----------------------------
resource "aws_subnet" "public_subnet" {
  vpc_id                  = aws_vpc.retailpulse_vpc.id
  cidr_block              = var.public_subnet_cidr
  availability_zone       = var.availability_zone
  map_public_ip_on_launch = true

  tags = {
    Name = "RetailPulse-Public-Subnet"
  }
}

# -----------------------------
# Create Internet Gateway
# -----------------------------
resource "aws_internet_gateway" "igw" {
  vpc_id = aws_vpc.retailpulse_vpc.id

  tags = {
    Name = "RetailPulse-IGW"
  }
}

# -----------------------------
# Create Public Route Table
# -----------------------------
resource "aws_route_table" "public_rt" {
  vpc_id = aws_vpc.retailpulse_vpc.id

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.igw.id
  }

  tags = {
    Name = "RetailPulse-Public-RT"
  }
}

# -----------------------------
# Associate Route Table
# -----------------------------
resource "aws_route_table_association" "public_assoc" {
  subnet_id      = aws_subnet.public_subnet.id
  route_table_id = aws_route_table.public_rt.id
}