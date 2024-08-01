#!/usr/bin/env bash

set -eux

function cleanup() {
    rm -rf test.terraform_state.yml
    ansible-playbook terraform.yml -e "tf_operation=destroy" "$@"
    exit 1
}

trap 'cleanup "${@}"'  ERR

# Create resources
ansible-playbook terraform.yml "$@"

export ANSIBLE_INVENTORY_ENABLED="cloud.terraform.terraform_state"

export ANSIBLE_INVENTORY=test.terraform_state.yml

# Test inventory with cloud nested block
ansible-playbook test.yml -e "inventory_template_file=inventory_cloud_nested_block" "$@"

# Test inventory with Remote backend
ansible-playbook test.yml -e "inventory_template_file=inventory_with_remote_backend" "$@"

# Test inventory with Remote backend and backend config files
ansible-playbook test.yml -e "inventory_template_file=inventory_with_remote_backend_with_config_files" "$@"


# Delete resources
ansible-playbook terraform.yml -e "tf_operation=destroy" "$@"
