#!/usr/bin/env bash

set -eux

function cleanup() {
    rm -rf test.terraform_state.yml aws_credentials.sh
    ansible-playbook teardown.yml "$@"
    exit 1
}

trap 'cleanup "${@}"'  ERR

# Create ec2 instances
ansible-playbook setup.yml "$@"

export ANSIBLE_INVENTORY_ENABLED="cloud.terraform.terraform_state"

export ANSIBLE_INVENTORY=test.terraform_state.yml

set +x
source aws_credentials.sh
set -x

ansible-playbook test.yml "$@"

# Delete ec2 instances
ansible-playbook teardown.yml "$@"
