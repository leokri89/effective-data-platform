# aws_api_gateway_api_key.mock-api-key:
resource "aws_api_gateway_api_key" "mock-api-key" {
    arn               = "arn:aws:apigateway:us-east-1::/apikeys/5ho8edw8jd"
    created_date      = "2022-02-18T05:44:01Z"
    enabled           = true
    id                = "5ho8edw8jd"
    last_updated_date = "2022-02-18T05:44:01Z"
    name              = "mock-api-key"
    tags              = {}
    tags_all          = {}
    value             = (sensitive value)
}

# aws_api_gateway_method.mock-post:
resource "aws_api_gateway_method" "mock-post" {
    api_key_required     = true
    authorization        = "NONE"
    authorization_scopes = []
    http_method          = "POST"
    id                   = "agm-9nsd1yfnt6-j401dc-POST"
    request_models       = {}
    request_parameters   = {}
    resource_id          = "j401dc"
    rest_api_id          = "9nsd1yfnt6"
}

# aws_api_gateway_method.mock-put:
resource "aws_api_gateway_method" "mock-put" {
    api_key_required     = true
    authorization        = "NONE"
    authorization_scopes = []
    http_method          = "GET"
    id                   = "agm-9nsd1yfnt6-j401dc-GET"
    request_models       = {}
    request_parameters   = {}
    resource_id          = "j401dc"
    rest_api_id          = "9nsd1yfnt6"
}

# aws_api_gateway_resource.mock-route:
resource "aws_api_gateway_resource" "mock-route" {
    id          = "j401dc"
    parent_id   = "sbwfvn8a9d"
    path        = "/mock-route"
    path_part   = "mock-route"
    rest_api_id = "9nsd1yfnt6"
}

# aws_api_gateway_resource.root:
resource "aws_api_gateway_resource" "root" {
    id          = "sbwfvn8a9d"
    path        = "/"
    rest_api_id = "9nsd1yfnt6"
}

# aws_api_gateway_rest_api.mock-api-gateway:
resource "aws_api_gateway_rest_api" "mock-api-gateway" {
    api_key_source               = "HEADER"
    arn                          = "arn:aws:apigateway:us-east-1::/restapis/9nsd1yfnt6"
    binary_media_types           = []
    created_date                 = "2022-02-18T05:40:40Z"
    disable_execute_api_endpoint = false
    execution_arn                = "arn:aws:execute-api:us-east-1:781782762636:9nsd1yfnt6"
    id                           = "9nsd1yfnt6"
    minimum_compression_size     = -1
    name                         = "mock-api-gateway"
    root_resource_id             = "sbwfvn8a9d"
    tags                         = {}
    tags_all                     = {}

    endpoint_configuration {
        types            = [
            "REGIONAL",
        ]
        vpc_endpoint_ids = []
    }
}

# aws_api_gateway_stage.beta:
resource "aws_api_gateway_stage" "beta" {
    arn                   = "arn:aws:apigateway:us-east-1::/restapis/9nsd1yfnt6/stages/beta"
    cache_cluster_enabled = false
    deployment_id         = "pc99pj"
    execution_arn         = "arn:aws:execute-api:us-east-1:781782762636:9nsd1yfnt6/beta"
    id                    = "ags-9nsd1yfnt6-beta"
    invoke_url            = "https://9nsd1yfnt6.execute-api.us-east-1.amazonaws.com/beta"
    rest_api_id           = "9nsd1yfnt6"
    stage_name            = "beta"
    tags                  = {}
    tags_all              = {}
    variables             = {}
    xray_tracing_enabled  = false
}
