terraform {
  backend "s3" {
    bucket = "bt-webgenie-collector-sudhdd"
    key    = "staging/main.tfstate"
    region = "us-east-1"
  }
}
