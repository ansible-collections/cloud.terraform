#!/usr/bin/env bash

set -eux

function cleanup() {
    rm -f google.terraform_state.yml gcp_credentials.sh
    ansible-playbook teardown.yml "$@"
    exit 1
}

trap 'cleanup "${@}"'  ERR

# Create infrastructure
ansible-playbook setup.yml -e "inventory_file_path=google.terraform_state.yml" "$@"

# export ANSIBLE_INVENTORY_ENABLED="cloud.terraform.terraform_state"
set +x 
source gcp_credentials.sh
set -x

ansible-playbook test.yml -i google.terraform_state.yml "$@"

# Delete infrastructure
rm -f google.terraform_state.yml gcp_credentials.sh
ansible-playbook teardown.yml "$@"
