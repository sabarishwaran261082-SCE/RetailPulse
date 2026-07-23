# -----------------------------------------
# IAM Role for EC2
# -----------------------------------------

resource "aws_iam_role" "retailpulse_role" {

  name = "RetailPulse-EC2-Role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"

    Statement = [
      {
        Effect = "Allow"

        Principal = {
          Service = "ec2.amazonaws.com"
        }

        Action = "sts:AssumeRole"
      }
    ]
  })

  tags = {
    Name = "RetailPulse-EC2-Role"
  }
}

# -----------------------------------------
# Attach Amazon ECR ReadOnly Policy
# -----------------------------------------

resource "aws_iam_role_policy_attachment" "ecr_readonly" {

  role       = aws_iam_role.retailpulse_role.name

  policy_arn = "arn:aws:iam::aws:policy/AmazonEC2ContainerRegistryReadOnly"
}

# -----------------------------------------
# Attach SSM Managed Instance Policy
# (Optional but Recommended)
# -----------------------------------------

resource "aws_iam_role_policy_attachment" "ssm_policy" {

  role       = aws_iam_role.retailpulse_role.name

  policy_arn = "arn:aws:iam::aws:policy/AmazonSSMManagedInstanceCore"
}

# -----------------------------------------
# Instance Profile
# -----------------------------------------

resource "aws_iam_instance_profile" "retailpulse_profile" {

  name = "RetailPulse-Instance-Profile"

  role = aws_iam_role.retailpulse_role.name
}