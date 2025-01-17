# each of this vars can be overridden by adding ENVIRONMENT variable with name:
# TF_VAR_var_name="value"

name             = "bt-webgenie-collector"
region           = "us-east-1"
env              = "prod"

# VPC and subnet CIDR settings, change them if you need to pair
# multiple CIDRs (i.e. with different component)
vpc_cidr         = "10.2.0.0/16"
subnet_cidrs     = ["10.2.1.0/24", "10.2.2.0/24"]
azs              = ["us-east-1c", "us-east-1d"]

# By default, we have an ubuntu image
base_ami_image        = "*ubuntu-focal-20.04-amd64-minimal-*"
base_ami_image_owner  = "099720109477"

# domain setting
base_domain_name = "bactensor.io"
domain_name      = "webgenie-collector.bactensor.io"

# default ssh key
ec2_ssh_key      = "ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAINL5xrAUJR1gB/BWXJetVluwhi8yObV5az0Ci2/zfThU Alex"

instance_type     = "t3.medium"
rds_instance_type = "db.t3.small"

# defines if we use EC2-only healthcheck or ELB healthcheck
# EC2 healthcheck reacts only on internal EC2 checks (i.e. if machine cannot be reached)
# recommended for staging = EC2, for prod = ELB
autoscaling_health_check_type = "ELB"
