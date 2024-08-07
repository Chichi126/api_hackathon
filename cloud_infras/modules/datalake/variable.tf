variable "bucket_name" {
  description = "The name of the S3 bucket"
  type        = string
}

variable "owner" {
  description = "The owner of the S3 bucket"
  type        = string
}

variable "service_name" {
  description = "The name of the service using the S3 bucket"
  type        = string
}
