
resource "aws_iam_role" "iam_for_lambda" {
    name = "iam_for_lambda_wefs"

    assume_role_policy = <<EOF
{
    "Version": "2012-10-17",
    "Statement": [
{
    "Action": "sts:AssumeRole",
    "Principal": {
    "Service": "lambda.amazonaws.com"
},
    "Effect": "Allow",
    "Sid": ""
}]}
EOF
}

resource "aws_lambda_function" "lambda_wefs" {
    filename = "lambda_function.zip"
    function_name = "xgboost_predict"
    role = aws_iam_role.iam_for_lambda.arn
    handler = "lambda_function.lambda_handler"

    source_code_hash = filebase64sha256("lambda_function.zip")

    runtime = "python3.7"

    file_system_config {
        arn = aws_efs_access_point.efs_accesspoint.arn
        local_mount_path = "/mnt/efs"
    }

    vpc_config {
        subnet_ids         = [aws_subnet.public.id]
        security_group_ids = [aws_security_group.allow_mount.id]
    }

    depends_on = [aws_efs_mount_target.mount_efs_public]
}

resource "aws_iam_policy" "lambda_efs" {
  name        = "lambda_efs"
  path        = "/"
  description = "IAM policy for EFS from a lambda"

  policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": [
        "ec2:CreateNetworkInterface",
        "ec2:DeleteNetworkInterface",
        "ec2:DescribeNetworkInterfaces"
      ],
      "Resource": "*",
      "Effect": "Allow"
    }
  ]
}
EOF
}

resource "aws_iam_role_policy_attachment" "lambda_logs" {
  role       = aws_iam_role.iam_for_lambda.name
  policy_arn = aws_iam_policy.lambda_efs.arn
}
