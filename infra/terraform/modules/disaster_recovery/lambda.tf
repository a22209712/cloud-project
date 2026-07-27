data "archive_file" "dr_lambda_zip" {
  type = "zip"

  source_file = "${path.module}/lambda/index.py"

  output_path = "${path.module}/lambda/dr-controller.zip"
}

resource "aws_lambda_function" "dr_controller" {
  function_name = "${local.name_prefix}-controller"

  role = aws_iam_role.dr_lambda_role.arn

  filename         = data.archive_file.dr_lambda_zip.output_path
  source_code_hash = data.archive_file.dr_lambda_zip.output_base64sha256

  runtime = "python3.12"
  handler = "index.lambda_handler"

  timeout = 30

  environment {
    variables = {
      PRIMARY_INSTANCE_ID = var.primary_instance_id
      STANDBY_INSTANCE_ID = var.standby_instance_id
      PRIMARY_REGION      = var.primary_region
      STANDBY_REGION      = var.standby_region
    }
  }
}