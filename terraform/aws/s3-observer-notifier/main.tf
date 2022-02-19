module "s3_bucket" {
    source = "terraform-aws-modules/s3-bucket/aws"

    bucket = "lk-observer-bucket"
    acl    = "private"

    versioning = {
       enabled = false
    }
    force_destroy = true
}


resource "aws_lambda_permission" "allow_bucket" {
    statement_id  = "AllowExecutionFromS3Bucket"
    action = "lambda:InvokeFunction"
    function_name = module.lambda_notifier.lambda_function_name
    principal = "s3.amazonaws.com"
    source_arn = module.s3_bucket.s3_bucket_arn
}


resource "aws_s3_bucket_notification" "bucket_notification" {
    bucket = module.s3_bucket.s3_bucket_id

    lambda_function {
        lambda_function_arn = module.lambda_notifier.lambda_function_arn
        events = ["s3:ObjectCreated:*","s3:ObjectRemoved:*","s3:ObjectRestore:*","s3:Replication:*"]
        filter_prefix = ""
        filter_suffix = ""
    }

    depends_on = [aws_lambda_permission.allow_bucket]
}


module "lambda_notifier" {
    depends_on = [
        "module.observer_sns"
    ]
    source = "terraform-aws-modules/lambda/aws"

    function_name = "lambda_notifier"
    description = "My lambda function to publish to SNS"
    handler = "lambda_function.lambda_handler"
    runtime = "python3.9"

    source_path = "./observer-code"

    environment_variables = {
        topicArn = module.observer_sns.sns_topic_arn
    }

    policy = aws_iam_policy.lambda_sns_publish.arn
    attach_policy = true

    tags = {
        Propose = "attributer"
    }
}


resource "aws_iam_policy" "lambda_sns_publish" {
    name        = "lambda_sns_publish"
    path        = "/"
    description = "Policy to lambda publish to SNS"

    policy = jsonencode({
        "Version": "2012-10-17",
        "Statement": [
            {
                "Sid": "VisualEditor0",
                "Effect": "Allow",
                "Action": [
                    "sns:Publish"
                ],
                "Resource": [
                    module.observer_sns.sns_topic_arn
                ]
            }
        ]
    })
}


module "observer_sns" {
    source  = "terraform-aws-modules/sns/aws"
    version = "~> 3.0"

    name  = "observer_sns"
    tags = {
        Propose = "subscriber"
    }
}


module "subscriber_sqs" {
    source  = "terraform-aws-modules/sqs/aws"
    version = "~> 3.3.0"

    name = "subscriber_sqs"

    tags = {
        Propose = "subscriber"
    }
}


resource "aws_sqs_queue_policy" "accept_receive_sns" {
    queue_url = module.subscriber_sqs.sqs_queue_id

    policy = jsonencode({
    "Version": "2008-10-17",
    "Id": "__default_policy_ID",
    "Statement": [{
            "Sid": format("%s:%s","topic-subscription-arn",module.observer_sns.sns_topic_arn),
            "Effect": "Allow",
            "Principal": {
            "AWS": "*"
            },
            "Action": "SQS:SendMessage",
            "Resource": module.subscriber_sqs.sqs_queue_arn,
            "Condition": {
            "ArnLike": {
                    "aws:SourceArn": module.observer_sns.sns_topic_arn
                }
            }
        }]
    })
}


resource "aws_sns_topic_subscription" "user_updates_sqs_target" {
    topic_arn = module.observer_sns.sns_topic_arn
    protocol  = "sqs"
    endpoint  = module.subscriber_sqs.sqs_queue_arn
}