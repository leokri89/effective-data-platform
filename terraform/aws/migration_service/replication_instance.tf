resource "aws_dms_replication_instance" "ec2_replication_instance" {
  allocated_storage            = 50
  apply_immediately            = true
  auto_minor_version_upgrade   = true
  availability_zone            = "us-east-1b"
  preferred_maintenance_window = "sun:10:30-sun:14:30"
  replication_instance_class   = "dms.c4.2xlarge"
  replication_instance_id      = "ec2-replication-instance"
  replication_subnet_group_id  = aws_dms_replication_subnet_group.ec2_replication_subnet.id

  tags = {
    Name = "test"
  }

  vpc_security_group_ids = [
    "sg-12345678",
  ]

  depends_on = [
    aws_iam_role_policy_attachment.dms-access-for-endpoint-AmazonDMSRedshiftS3Role,
    aws_iam_role_policy_attachment.dms-cloudwatch-logs-role-AmazonDMSCloudWatchLogsRole,
    aws_iam_role_policy_attachment.dms-vpc-role-AmazonDMSVPCManagementRole
  ]
}

resource "aws_dms_replication_subnet_group" "ec2_replication_subnet" {
  replication_subnet_group_description = "replication subnet group"
  replication_subnet_group_id          = "ec2-replication-subnet"

  subnet_ids = [
    "subnet-12345678",
  ]

  tags = {
    Name = "test"
  }
}