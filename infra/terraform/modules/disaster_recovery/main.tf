locals {
  name_prefix = "${var.project_name}-dr"
}

resource "aws_iam_role" "dr_lambda_role" {
  name = "${local.name_prefix}-lambda-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"

    Statement = [
      {
        Effect = "Allow"

        Principal = {
          Service = "lambda.amazonaws.com"
        }

        Action = "sts:AssumeRole"
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "lambda_basic" {
  role = aws_iam_role.dr_lambda_role.name

  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}


resource "aws_iam_policy" "dr_controller_policy" {
  name = "${local.name_prefix}-controller"

  policy = jsonencode({
    Version = "2012-10-17"

    Statement = [
      {
        Effect = "Allow"

        Action = [
          "ec2:DescribeInstances",
          "ec2:StartInstances",
          "ec2:StopInstances"
        ]

        Resource = "*"
      }
    ]
  })
}


resource "aws_iam_role_policy_attachment" "controller" {
  role       = aws_iam_role.dr_lambda_role.name
  policy_arn = aws_iam_policy.dr_controller_policy.arn
}

resource "aws_cloudwatch_event_rule" "dr_check" {
  name                = "${local.name_prefix}-check"
  schedule_expression = "rate(5 minutes)"
}

resource "aws_cloudwatch_event_target" "lambda" {
  rule = aws_cloudwatch_event_rule.dr_check.name
  arn  = aws_lambda_function.dr_controller.arn
}

resource "aws_lambda_permission" "eventbridge" {
  statement_id  = "AllowExecutionFromEventBridge"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.dr_controller.function_name
  principal     = "events.amazonaws.com"
  source_arn    = aws_cloudwatch_event_rule.dr_check.arn
}