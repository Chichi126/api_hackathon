resource "aws_iam_role" "test_redshift" {
  name = "redshift_glue_s3role"

  # Terraform's "jsonencode" function converts a
  # Terraform expression result to valid JSON syntax.
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Sid    = ""
        Principal = {
          Service = "redshift.amazonaws.com"
        }
      },
    ]
  })

  tags = {
    owner = "chi-de"
  }
}

resource "aws_iam_policy" "redshifpolicy" {
  name        = "redshift_glue_S3_policy"
  path        = "/"
  description = "My test policy"

  # Terraform's "jsonencode" function converts a
  # Terraform expression result to valid JSON syntax.
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = [
          "S3:list",
          "s3: get*"
        ]
        Effect   = "Allow"
        Resource = ["arn:aws:s3:::chi-apidataset",
                    "arn:aws:s3:::chi-apidataset/api_countries_dataset.parquet/"]
      },
      {
        Action = [
          "glue:*",
        ]
        Effect   = "Allow"
        Resource = "*"
      },
    ]
  })
}


resource "aws_iam_role_policy_attachment" "redshift-attach" {
  role       = aws_iam_role.test_redshift.name
  policy_arn = aws_iam_policy.redshifpolicy.arn
}


resource "random_password" "randomp_retest" {
  length           = 20
  special          = false
  }

resource "aws_ssm_parameter" "api_redshift_pwd_params" {
  name  = "api_redshift_pwd"
  type  = "String"
  value = random_password.randomp_retest.result
}


module "datawarehouse_cluster" {
  source                  = "./dataware_house"
  cluster_identifier      = "chi-de" 
  database_name           = "api_countries"
  iam_roles               = [aws_iam_role.test_redshift.arn]
  master_password         = aws_ssm_parameter.api_redshift_pwd_params.value
  master_username         = "chichi"
}