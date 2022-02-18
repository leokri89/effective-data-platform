resource "aws_iam_role" "mock-stream-lambda-role" {
  assume_role_policy = jsonencode(
    {
      Statement = [
        {
          Action = "sts:AssumeRole"
          Effect = "Allow"
          Principal = {
            Service = "lambda.amazonaws.com"
          }
        },
      ]
      Version = "2012-10-17"
    }
  )
  force_detach_policies = false
  managed_policy_arns = [
    "arn:aws:iam::781782762636:policy/service-role/AWSLambdaBasicExecutionRole-6a314627-247d-4a9a-ade9-8ed78f0bb8f8",
  ]
  max_session_duration = 3600
  name                 = "mock-stream-lambda-role-hrzdvq7f"
  path                 = "/service-role/"
  tags                 = {}
  tags_all             = {}

  inline_policy {}
}

resource "aws_iam_role" "mock-firehose-role" {
  assume_role_policy = jsonencode(
    {
      Statement = [
        {
          Action = "sts:AssumeRole"
          Effect = "Allow"
          Principal = {
            Service = "firehose.amazonaws.com"
          }
        },
      ]
      Version = "2012-10-17"
    }
  )
  force_detach_policies = false
  managed_policy_arns = [
    "arn:aws:iam::781782762636:policy/service-role/KinesisFirehoseServicePolicy-mock-delivery-stream-us-east-1",
  ]
  max_session_duration = 3600
  name                 = "KinesisFirehoseServiceRole-mock-delivery-us-east-1-1645154601030"
  path                 = "/service-role/"
  tags                 = {}
  tags_all             = {}

  inline_policy {}
}

resource "aws_kinesis_firehose_delivery_stream" "mock-delivery-stream" {
  destination    = "extended_s3"
  name           = "mock-delivery-stream"
  tags           = {}
  tags_all       = {}
  version_id     = "1"

  extended_s3_configuration {
    bucket_arn         = aws_s3_bucket.mock-bucket-leonardok.arn
    buffer_interval    = 300
    buffer_size        = 5
    compression_format = "UNCOMPRESSED"
    role_arn           = aws_iam_role.mock-firehose-role.arn
    s3_backup_mode     = "Disabled"

    cloudwatch_logging_options {
      enabled         = true
      log_group_name  = "/aws/kinesisfirehose/mock-delivery-stream"
      log_stream_name = "DestinationDelivery"
    }

    processing_configuration {
      enabled = false
    }
  }

  kinesis_source_configuration {
    kinesis_stream_arn = aws_kinesis_stream.mock-stream.arn
    role_arn           = aws_iam_role.mock-firehose-role.arn
  }

}


resource "aws_kinesis_stream" "mock-stream" {
  encryption_type     = "NONE"
  name                = "mock-stream"
  retention_period    = 24
  shard_count         = 0
  shard_level_metrics = []
  tags                = {}
  tags_all            = {}

  stream_mode_details {
    stream_mode = "ON_DEMAND"
  }

  timeouts {}
}


resource "aws_lambda_function" "mock-stream-lambda" {
  architectures = [
    "x86_64",
  ]
  description                    = "An Amazon Kinesis Firehose stream processor that accesses the records in the input and returns them with a processing status."
  function_name                  = "mock-stream-lambda"
  handler                        = "index.handler"
  memory_size                    = 128
  package_type                   = "Zip"
  reserved_concurrent_executions = -1
  role                           = aws_iam_role.mock-stream-lambda-role.arn
  runtime                        = "nodejs12.x"
  tags = {
    "lambda-console:blueprint" = "kinesis-firehose-process-record"
  }
  tags_all = {
    "lambda-console:blueprint" = "kinesis-firehose-process-record"
  }
  timeout = 60

  timeouts {}

  tracing_config {
    mode = "PassThrough"
  }
}


resource "aws_s3_bucket" "mock-bucket-leonardok" {
  bucket   = "mock-bucket-leonardok"
  tags     = {}
  tags_all = {}

  versioning {
    enabled    = false
    mfa_delete = false
  }
}