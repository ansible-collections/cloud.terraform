#!/bin/sh

(
    set -eux
    mkdir -p terraform_init
    cd terraform_init
    terraform init
)

export TF_DATA_DIR="$PWD/terraform_init/.terraform"
env | grep TF_

# this uses TF_DATA_DIR
terraform apply -auto-approve

ansible-playbook test_outputs.yml
