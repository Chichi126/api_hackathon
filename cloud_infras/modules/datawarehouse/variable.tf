variable "node_type" {
    default = "dc2.large"
}

variable "cluster_type" {
    default = "single-node"
}

variable "skip_final_snapshot" {
    default = "true"
}

variable "publicly_accessible" {
    default = "true"
}

variable "database_name" {}

variable "iam_roles" {}

variable "master_password" {}

variable "master_username" {}

variable "cluster_identifier" {}