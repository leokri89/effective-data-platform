
resource "aws_instance" "ec2-xgboost" {
    ami = "ami-0c94855ba95c71c99"
    instance_type = "t2.micro"

    key_name = aws_key_pair.ec2-key.key_name

    subnet_id = aws_subnet.public_subnet_1.id
    private_ip = "10.0.0.10"

    tags = {
        Name = "ec2-tocheck"
    }
}

resource "aws_eip" "eip_ec2" {
    vpc = true

    instance = aws_instance.ec2-xgboost.id
    associate_with_private_ip = "10.0.0.10"

    depends_on = [aws_internet_gateway.gw]
}

resource "aws_key_pair" "ec2-key" {
    key_name = "deployer-key"
    public_key = "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABgQDiuvtNSLME+rpzbCXErROpv9s4OzUEglcm7NLH4ibW2s3GK5qEe+Im1LeY+HmqBY8MZlH2u5BD5n2A77TNfE5421lpsw9LqshsiGiEH3+f/izJ1dsPZ18kr4W5+J90eNGD1B+8nLFQgUxDMyWHN2lMUAJ2YLo/6IgKPwYGY/z9Bn9ApSMazchuA6piHe+NiVJBtOq7l6aoEjyboxkw6VGpdOseR3B6K5VPXbF0eVFua1r0wSBHcG7X6pn9UJtq63ovj6y0GVaJgLy3YQrHppC7vctCoTWMEORQ7+oDf8f84AoEcr3TT+YdAJ6OYhYrKLk1/hJbuIsa4YqAHLpFpOdvrpkQUfPXyQwjmSguLOs3M2gXEiDUe1Mh7lUR4jC2fWe8Pv1IvllOodivuM+l268r88XN7hxK/+Hd3am+mxfX2H2ZZB6WEqEhzeWH9n/ELkOKqlNvr5GFYUIEPz1A9aaCE1rML0JxzEoGmiROaKbNe5r6goUTB7GiUkwNNw8r6Ks= leonardok@NBK-Q0LQDL3"
}

resource "aws_instance" "ec2-private-sb" {
    ami = "ami-0c94855ba95c71c99"
    instance_type = "t2.micro"

    key_name = aws_key_pair.ec2-key.key_name

    subnet_id = aws_subnet.private_subnet_1.id

    tags = {
        Name = "ec2-private-sb"
    }
}