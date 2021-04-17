
resource "aws_efs_file_system" "shared" {}

resource "aws_efs_mount_target" "mount_efs_subnet1" {
    file_system_id  = aws_efs_file_system.shared.id
    subnet_id = aws_subnet.private_subnet_1.id
    security_groups = [aws_security_group.allow_mount.id]
}

resource "aws_efs_mount_target" "mount_efs_subnet2" {
    file_system_id  = aws_efs_file_system.shared.id
    subnet_id = aws_subnet.private_subnet_2.id
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