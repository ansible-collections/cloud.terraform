terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "=4.38.0"
    }
  }
}

provider "aws" {
}

variable "cloud_terraform_integration_id" {
  type = string
}

output "aws_sqs_queue_tags" {
  description = "AWS SQS queue tags"
  value       = resource.aws_sqs_queue.this.tags
}

output "aws_sqs_role_tags" {
  description = "AWS IAM role tags"
  value       = resource.aws_iam_role.this.tags
}

resource "aws_sqs_queue" "this" {
  name = "${var.cloud_terraform_integration_id}-queue"
  tags = {
    Name                        = var.cloud_terraform_integration_id
    cloud_terraform_integration = "true"
  }
}

data "aws_iam_policy_document" "this" {
  statement {
    effect = "Allow"

    principals {
      type = "AWS"
      identifiers = [
        aws_iam_role.this.arn
      ]
    }

    actions = [
      "sqs:SendMessage"
    ]

    resources = [
      aws_sqs_queue.this.arn
    ]
  }
}

resource "aws_sqs_queue_policy" "this" {
  queue_url = aws_sqs_queue.this.id
  policy    = data.aws_iam_policy_document.this.json
}

resource "aws_iam_role" "this" {
  name = "${var.cloud_terraform_integration_id}-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Action = "sts:AssumeRole"
      Effect = "Allow"
      Sid    = ""
      Principal = {
        Service = "lambda.amazonaws.com"
      }
    }]
  })
  tags = {
    Name                        = var.cloud_terraform_integration_id
    cloud_terraform_integration = "true"
  }
}

resource "aws_iam_role_policy_attachment" "this" {
  role       = aws_iam_role.this.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}
