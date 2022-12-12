#!/bin/sh

set -eux

terraform init
terraform apply -auto-approve

ansible-playbook test_outputs.yml
