resource "aws_s3_bucket" "fakerairflow" {
  bucket = var.bucket_name

tags = {
    owner       = var.owner
    service     = var.service_name
    
}
}