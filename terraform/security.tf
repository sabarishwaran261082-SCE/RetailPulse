# ---------------------------------
# Security Group for RetailPulse
# ---------------------------------

resource "aws_security_group" "retailpulse_sg" {

  name        = "RetailPulse-SG"
  description = "Security Group for RetailPulse EC2"
  vpc_id      = aws_vpc.retailpulse_vpc.id

  # -----------------------------
  # SSH
  # -----------------------------
ingress {
  description = "SSH"

  from_port   = 22
  to_port     = 22
  protocol    = "tcp"

  cidr_blocks = ["0.0.0.0/0"]
}
  # -----------------------------
  # HTTP
  # -----------------------------
  ingress {
    description = "HTTP"

    from_port   = 80
    to_port     = 80
    protocol    = "tcp"

    cidr_blocks = ["0.0.0.0/0"]
  }

  # -----------------------------
  # HTTPS
  # -----------------------------
  ingress {
    description = "HTTPS"

    from_port   = 443
    to_port     = 443
    protocol    = "tcp"

    cidr_blocks = ["0.0.0.0/0"]
  }

  # -----------------------------
  # Streamlit
  # -----------------------------
  ingress {
    description = "Streamlit"

    from_port   = var.container_port
    to_port     = var.container_port
    protocol    = "tcp"

    cidr_blocks = ["0.0.0.0/0"]
  }

  # -----------------------------
  # Outbound
  # -----------------------------
  egress {

    from_port   = 0
    to_port     = 0
    protocol    = "-1"

    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "RetailPulse-SecurityGroup"
  }
}