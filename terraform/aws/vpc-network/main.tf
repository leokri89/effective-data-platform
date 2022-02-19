/*
VPC Setup
*/

resource "aws_vpc" "main" {
  cidr_block           = "10.0.0.0/16"
  instance_tenancy     = "default"
  enable_dns_support   = true
  enable_dns_hostnames = true
  tags = {
    Name = "main-vpc"
  }
}

/*
MAIN ROUTE TABLE
*/
resource "aws_route_table" "main" {
  vpc_id = aws_vpc.main.id
  tags = {
    Name = "main-rtable"
  }
}

resource "aws_main_route_table_association" "main_table" {
  vpc_id         = aws_vpc.main.id
  route_table_id = aws_route_table.main.id
}

/*
Internet Gateway
*/
resource "aws_internet_gateway" "gw" {
  vpc_id = aws_vpc.main.id
}

resource "aws_route" "main_igateway" {
  route_table_id         = aws_route_table.main.id
  destination_cidr_block = "0.0.0.0/0"
  gateway_id             = aws_internet_gateway.gw.id
}

resource "aws_eip" "nat_eip" {
  vpc        = true
  depends_on = [aws_internet_gateway.gw]
}

/*
Public SUBNET
*/
resource "aws_subnet" "public_subnet_1" {
  vpc_id                  = aws_vpc.main.id
  cidr_block              = "10.0.0.0/24"
  availability_zone       = "us-east-1b"
  map_public_ip_on_launch = false
  tags = {
    Name = "public_subnet_1"
  }
}

resource "aws_nat_gateway" "nat-gateway" {
  allocation_id = aws_eip.nat_eip.id
  subnet_id     = aws_subnet.public_subnet_1.id
  depends_on    = [aws_internet_gateway.gw]
  tags = {
    Name = "nat-gateway"
  }
}

resource "aws_subnet" "public_subnet_2" {
  vpc_id                  = aws_vpc.main.id
  cidr_block              = "10.0.1.0/24"
  availability_zone       = "us-east-1a"
  map_public_ip_on_launch = false
  tags = {
    Name = "public_subnet_2"
  }
}

resource "aws_route_table_association" "public_1" {
  subnet_id      = aws_subnet.public_subnet_1.id
  route_table_id = aws_route_table.main.id
}

resource "aws_route_table_association" "public_2" {
  subnet_id      = aws_subnet.public_subnet_2.id
  route_table_id = aws_route_table.main.id
}

/*
Private SUBNET
*/
resource "aws_subnet" "private_subnet_1" {
  vpc_id                  = aws_vpc.main.id
  cidr_block              = "10.0.2.0/24"
  availability_zone       = "us-east-1b"
  map_public_ip_on_launch = false
  tags = {
    Name = "private_subnet_1"
  }
}

resource "aws_subnet" "private_subnet_2" {
  vpc_id                  = aws_vpc.main.id
  cidr_block              = "10.0.3.0/24"
  availability_zone       = "us-east-1a"
  map_public_ip_on_launch = false
  tags = {
    Name = "private_subnet_2"
  }
}

resource "aws_route_table" "private_rtable" {
  vpc_id = aws_vpc.main.id
  tags = {
    Name = "private-rtable"
  }
}

resource "aws_route_table_association" "private_1" {
  subnet_id      = aws_subnet.private_subnet_1.id
  route_table_id = aws_route_table.private_rtable.id
}

resource "aws_route_table_association" "private_2" {
  subnet_id      = aws_subnet.private_subnet_2.id
  route_table_id = aws_route_table.private_rtable.id
}

resource "aws_route" "private_nat_gateway" {
  route_table_id         = aws_route_table.private_rtable.id
  destination_cidr_block = "0.0.0.0/0"
  nat_gateway_id         = aws_nat_gateway.nat-gateway.id
}

/*
Default Security Group
*/
resource "aws_security_group" "default" {
  name        = "vpc-default-sg"
  description = "Default security group to allow inbound/outbound from the VPC"
  vpc_id      = aws_vpc.main.id
  depends_on  = [aws_vpc.main]
  ingress {
    from_port = "0"
    to_port   = "0"
    protocol  = "-1"
    self      = true
  }
  ingress {
    from_port = "22"
    to_port   = "22"
    protocol  = "tcp"
    self      = true
  }

  egress {
    from_port = "0"
    to_port   = "0"
    protocol  = "-1"
    self      = "true"
  }

}

/*
EC2 dentro da rede VPC
*/
resource "aws_instance" "ec2-xgboost" {
  ami           = "ami-0c94855ba95c71c99"
  instance_type = "t2.micro"

  key_name = aws_key_pair.ec2-key.key_name

  subnet_id  = aws_subnet.public_subnet_1.id
  private_ip = "10.0.0.10"

  tags = {
    Name = "ec2-tocheck"
  }
}

resource "aws_eip" "eip_ec2" {
  vpc = true

  instance                  = aws_instance.ec2-xgboost.id
  associate_with_private_ip = "10.0.0.10"

  depends_on = [aws_internet_gateway.gw]
}

resource "aws_key_pair" "ec2-key" {
  key_name   = "deployer-key"
  public_key = "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABgQDiuvtNSLME+rpzbCXErROpv9s4OzUEglcm7NLH4ibW2s3GK5qEe+Im1LeY+HmqBY8MZlH2u5BD5n2A77TNfE5421lpsw9LqshsiGiEH3+f/izJ1dsPZ18kr4W5+J90eNGD1B+8nLFQgUxDMyWHN2lMUAJ2YLo/6IgKPwYGY/z9Bn9ApSMazchuA6piHe+NiVJBtOq7l6aoEjyboxkw6VGpdOseR3B6K5VPXbF0eVFua1r0wSBHcG7X6pn9UJtq63ovj6y0GVaJgLy3YQrHppC7vctCoTWMEORQ7+oDf8f84AoEcr3TT+YdAJ6OYhYrKLk1/hJbuIsa4YqAHLpFpOdvrpkQUfPXyQwjmSguLOs3M2gXEiDUe1Mh7lUR4jC2fWe8Pv1IvllOodivuM+l268r88XN7hxK/+Hd3am+mxfX2H2ZZB6WEqEhzeWH9n/ELkOKqlNvr5GFYUIEPz1A9aaCE1rML0JxzEoGmiROaKbNe5r6goUTB7GiUkwNNw8r6Ks= leonardok@NBK-Q0LQDL3"
}

resource "aws_instance" "ec2-private-sb" {
  ami           = "ami-0c94855ba95c71c99"
  instance_type = "t2.micro"

  key_name = aws_key_pair.ec2-key.key_name

  subnet_id = aws_subnet.private_subnet_1.id

  tags = {
    Name = "ec2-private-sb"
  }
}

/*
Recursos para o EFS dentro da VPC
*/

resource "aws_efs_file_system" "shared" {}

resource "aws_efs_mount_target" "mount_efs_subnet1" {
  file_system_id  = aws_efs_file_system.shared.id
  subnet_id       = aws_subnet.private_subnet_1.id
  security_groups = [aws_security_group.allow_mount.id]
}

resource "aws_efs_mount_target" "mount_efs_subnet2" {
  file_system_id  = aws_efs_file_system.shared.id
  subnet_id       = aws_subnet.private_subnet_2.id
  security_groups = [aws_security_group.allow_mount.id]
}

resource "aws_efs_access_point" "efs_accesspoint" {
  file_system_id = aws_efs_file_system.shared.id

  posix_user {
    gid = 1001
    uid = 1001
  }

  root_directory {
    path = "/"
    creation_info {
      owner_gid   = 1001
      owner_uid   = 1001
      permissions = "0777"
    }
  }
}

resource "aws_security_group" "allow_mount" {
  name   = "allow_mount"
  vpc_id = aws_vpc.main.id

  ingress {
    from_port   = 2049
    to_port     = 2049
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
}