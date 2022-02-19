/*
Proposito: Código de criação de API Gateway com Lambda de integração.
Recursos:
    - 
    - 
    - 
    - 
*/

resource "aws_iam_role" "iam_for_api_gateway_lambda" {
  name = "userGeneratorPlusGoldDiamond-role"
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
  tags = {}

}

resource "aws_lambda_function" "api_gateway_lambda" {
  function_name    = "userGeneratorPlusGoldDiamond"
  handler          = "lambda_function.lambda_handler"
  filename         = "./src/deployment-package.zip"
  source_code_hash = filebase64sha256("./src/deployment-package.zip")

  role = aws_iam_role.iam_for_api_gateway_lambda.arn

  runtime                        = "python3.9"
  reserved_concurrent_executions = 10
  memory_size                    = 128
  timeout                        = 10

  tags = {}
}

resource "aws_lambda_permission" "apigw_lambda" {
  statement_id  = "AllowExecutionFromAPIGateway"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.api_gateway_lambda.function_name
  principal     = "apigateway.amazonaws.com"

  source_arn = "arn:aws:execute-api:${var.myregion}:${var.accountId}:${aws_api_gateway_rest_api.user-generator-endpoint.id}/*/${aws_api_gateway_method.user-generator-post.http_method}${aws_api_gateway_resource.user-generator-criar-usuario.path}"
}

resource "aws_api_gateway_rest_api" "user-generator-endpoint" {
  name = "user-generator-endpoint"
  tags = {}

  endpoint_configuration {
    types = [
      "REGIONAL",
    ]
  }
}

resource "aws_api_gateway_stage" "user-generator-stage" {
  deployment_id = aws_api_gateway_deployment.user-generator-deployment.id
  rest_api_id   = aws_api_gateway_rest_api.user-generator-endpoint.id
  stage_name    = "deployed"
}

resource "aws_api_gateway_usage_plan" "user-generator-usage-plan" {
  name = "basic"
  tags = {}

  api_stages {
    api_id = aws_api_gateway_rest_api.user-generator-endpoint.id
    stage  = aws_api_gateway_stage.user-generator-stage.stage_name
  }

  quota_settings {
    limit  = 1000
    offset = 0
    period = "MONTH"
  }

  throttle_settings {
    burst_limit = 20
    rate_limit  = 10
  }
}

resource "aws_api_gateway_api_key" "user-generator-api-key" {
  enabled = true
  name    = "user-generator-api-key"
  tags    = {}
}

resource "aws_api_gateway_usage_plan_key" "user-generator-usage-api-key" {
  key_id        = aws_api_gateway_api_key.user-generator-api-key.id
  key_type      = "API_KEY"
  usage_plan_id = aws_api_gateway_usage_plan.user-generator-usage-plan.id
}

resource "aws_api_gateway_resource" "user-generator-criar-usuario" {
  parent_id   = aws_api_gateway_rest_api.user-generator-endpoint.root_resource_id
  path_part   = "criar-usuario"
  rest_api_id = aws_api_gateway_rest_api.user-generator-endpoint.id
}

resource "aws_api_gateway_method" "user-generator-post" {
  api_key_required = true
  http_method      = "POST"
  authorization    = "NONE"
  resource_id      = aws_api_gateway_resource.user-generator-criar-usuario.id
  rest_api_id      = aws_api_gateway_rest_api.user-generator-endpoint.id
}

resource "aws_api_gateway_integration" "user-generator-post-integration" {
  rest_api_id             = aws_api_gateway_rest_api.user-generator-endpoint.id
  resource_id             = aws_api_gateway_resource.user-generator-criar-usuario.id
  http_method             = aws_api_gateway_method.user-generator-post.http_method
  integration_http_method = "POST"
  type                    = "AWS"
  uri                     = aws_lambda_function.api_gateway_lambda.invoke_arn
}

resource "aws_api_gateway_method_response" "user-generator-method_response_200" {
  rest_api_id = aws_api_gateway_rest_api.user-generator-endpoint.id
  resource_id = aws_api_gateway_resource.user-generator-criar-usuario.id
  http_method = aws_api_gateway_method.user-generator-post.http_method
  status_code = "200"
  response_models = {
    "application/json" = "Empty"
  }
}

resource "aws_api_gateway_integration_response" "user-generator-integration_response" {
  depends_on  = [aws_api_gateway_integration.user-generator-post-integration]
  rest_api_id = aws_api_gateway_rest_api.user-generator-endpoint.id
  resource_id = aws_api_gateway_resource.user-generator-criar-usuario.id
  http_method = aws_api_gateway_method.user-generator-post.http_method
  status_code = aws_api_gateway_method_response.user-generator-method_response_200.status_code
}

resource "aws_api_gateway_deployment" "user-generator-deployment" {
  rest_api_id = aws_api_gateway_rest_api.user-generator-endpoint.id

  triggers = {
    redeployment = sha1(jsonencode([
      aws_api_gateway_resource.user-generator-criar-usuario.id,
      aws_api_gateway_method.user-generator-post.id,
      aws_api_gateway_integration.user-generator-post-integration.id
    ]))
  }

  lifecycle {
    create_before_destroy = true
  }
}