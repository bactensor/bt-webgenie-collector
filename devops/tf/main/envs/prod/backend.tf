terraform {
  backend "s3" {
    bucket = "bt-webgenie-collector-sudhdd"
    key    = "prod/main.tfstate"
    region = "us-east-1"
  }
}
