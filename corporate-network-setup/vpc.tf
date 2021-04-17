
## VPC Setup
resource "aws_vpc" "main" {
    cidr_block = "10.0.0.0/16"
    instance_tenancy = "default"
    enable_dns_support   = true
    enable_dns_hostnames = true
    tags = {
        Name = "main-vpc"
    }
}

## MAIN ROUTE TABLE
resource "aws_route_table" "main" {
    vpc_id = aws_vpc.main.id
    tags = {
        Name = "main-rtable"
    }
}

resource "aws_main_route_table_association" "main_table" {
    vpc_id = aws_vpc.main.id
    route_table_id = aws_route_table.main.id
}


## Internet Gateway
resource "aws_internet_gateway" "gw" {
    vpc_id = aws_vpc.main.id
}

resource "aws_route" "main_igateway" {
    route_table_id = aws_route_table.main.id
    destination_cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.gw.id
}

resource "aws_eip" "nat_eip" {
    vpc = true
    depends_on = [aws_internet_gateway.gw]
}


## Public SUBNET
resource "aws_subnet" "public_subnet_1" {
    vpc_id = aws_vpc.main.id
    cidr_block = "10.0.0.0/24"
    availability_zone = "us-east-1b"
    map_public_ip_on_launch = false
    tags = {
        Name = "public_subnet_1"
    }
}

resource "aws_nat_gateway" "nat-gateway" {
    allocation_id = aws_eip.nat_eip.id
    subnet_id = aws_subnet.public_subnet_1.id
    depends_on = [aws_internet_gateway.gw]
    tags = {
        Name = "nat-gateway"
    }
}

resource "aws_subnet" "public_subnet_2" {
    vpc_id = aws_vpc.main.id
    cidr_block = "10.0.1.0/24"
    availability_zone = "us-east-1a"
    map_public_ip_on_launch = false
    tags = {
        Name = "public_subnet_2"
    }
}

resource "aws_route_table_association" "public_1" {
    subnet_id = aws_subnet.public_subnet_1.id
    route_table_id = aws_route_table.main.id
}

resource "aws_route_table_association" "public_2" {
    subnet_id = aws_subnet.public_subnet_2.id
    route_table_id = aws_route_table.main.id
}

## Private SUBNET
resource "aws_subnet" "private_subnet_1" {
    vpc_id = aws_vpc.main.id
    cidr_block = "10.0.2.0/24"
    availability_zone = "us-east-1b"
    map_public_ip_on_launch = false
    tags = {
        Name = "private_subnet_1"
    }
}

resource "aws_subnet" "private_subnet_2" {
    vpc_id = aws_vpc.main.id
    cidr_block = "10.0.3.0/24"
    availability_zone = "us-east-1a"
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
    subnet_id = aws_subnet.private_subnet_1.id
    route_table_id = aws_route_table.private_rtable.id
}

resource "aws_route_table_association" "private_2" {
    subnet_id = aws_subnet.private_subnet_2.id
    route_table_id = aws_route_table.private_rtable.id
}

resource "aws_route" "private_nat_gateway" {
    route_table_id = aws_route_table.private_rtable.id
    destination_cidr_block = "0.0.0.0/0"
    nat_gateway_id = aws_nat_gateway.nat-gateway.id
}

#Default Security Group
resource "aws_security_group" "default" {
    name = "vpc-default-sg"
    description = "Default security group to allow inbound/outbound from the VPC"
    vpc_id = aws_vpc.main.id
    depends_on  = [aws_vpc.main]
        ingress {
            from_port = "0"
            to_port = "0"
            protocol  = "-1"
            self = true
        }
        ingress {
            from_port = "22"
            to_port = "22"
            protocol  = "tcp"
            self = true
        }

        egress {
            from_port = "0"
            to_port = "0"
            protocol = "-1"
            self = "true"
        }

}