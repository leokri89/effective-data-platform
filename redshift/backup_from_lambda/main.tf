resource "aws_iam_role" "dynamoLambda-role" {
  name = "dynamoLambda-role"

  assume_role_policy = jsonencode({
    Version : "2012-10-17",
    Statement : [
      {
        Action : "sts:AssumeRole",
        Principal : {
          Service : "lambda.amazonaws.com"
        },
        Effect : "Allow",
        Sid : ""
      }
    ]
  })

  tags = {
    tag-key = "tag-value"
  }
}


resource "aws_iam_role_policy" "dynamoLambda-policy" {
  name = "dynamoLambda-policy"
  role = aws_iam_role.dynamoLambda-role.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = [
            "dynamodb:*"
        ]
        Effect   = "Allow"
        Resource = "*"
      },
    ]
  })
}


resource "aws_lambda_function" "dynamoLambda-function" {
  filename      = "code.zip"
  function_name = "dynamoLambda-function"
  role          = aws_iam_role.dynamoLambda-role.arn
  handler       = "main.handler"

  source_code_hash = filebase64sha256("code.zip")

  runtime = "python3.8"

  environment {
    variables = {
      foo = "bar"
    }
  }
}


resource "aws_cloudwatch_event_rule" "run_backup_rule" {
  name                = "BackupSchedule"
  description         = "Run Weekly Backup"
  #schedule_expression = "cron(1 23 ? * SUN *)"
  schedule_expression = "cron(*/1 * ? * * *)"
}


resource "aws_cloudwatch_event_target" "schedule_lambda" {
    rule = aws_cloudwatch_event_rule.run_backup_rule.name
    target_id = "dynamoLambda-function"
    arn = aws_lambda_function.dynamoLambda-function.arn
}


resource "aws_lambda_permission" "allow_events_bridge_to_run_lambda" {
    statement_id = "AllowExecutionFromCloudWatch"
    action = "lambda:InvokeFunction"
    function_name = aws_lambda_function.dynamoLambda-function.function_name
    principal = "events.amazonaws.com"
}