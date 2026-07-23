# ----------------------------------------
# Get Latest Amazon Linux 2023 AMI
# ----------------------------------------

data "aws_ami" "amazon_linux" {

  most_recent = true

  owners = ["137112412989"]

  filter {
    name = "name"

    values = ["al2023-ami-2023*-x86_64"]
  }

  filter {
    name = "virtualization-type"

    values = ["hvm"]
  }
}

# ----------------------------------------
# EC2 Instance
# ----------------------------------------

resource "aws_instance" "retailpulse_ec2" {

  ami                    = data.aws_ami.amazon_linux.id

  instance_type          = var.instance_type

  subnet_id              = aws_subnet.public_subnet.id

  vpc_security_group_ids = [aws_security_group.retailpulse_sg.id]

  iam_instance_profile   = aws_iam_instance_profile.retailpulse_profile.name

  key_name               = var.key_name

  associate_public_ip_address = false

  user_data = file("${path.module}/userdata.sh")

  tags = {
    Name = "RetailPulse-EC2"
  }
}

# ----------------------------------------
# Elastic IP
# ----------------------------------------

resource "aws_eip" "retailpulse_eip" {

  domain = "vpc"

  instance = aws_instance.retailpulse_ec2.id

  tags = {
    Name = "RetailPulse-EIP"
  }

  depends_on = [
    aws_internet_gateway.igw
  ]
}