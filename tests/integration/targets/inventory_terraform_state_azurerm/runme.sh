#!/usr/bin/env bash

set -eux

function cleanup() {
    rm -f azurerm.terraform_state.yml azure_credentials.sh
    ansible-playbook teardown.yml "$@"
    exit 1
}

trap 'cleanup "${@}"'  ERR

# Create infrastructure
ansible-playbook setup.yml -e "inventory_file_path=azurerm.terraform_state.yml" "$@"

export ANSIBLE_INVENTORY_ENABLED="cloud.terraform.terraform_state"

set +x
source azure_credentials.sh
set -x

ansible-playbook test.yml -i azurerm.terraform_state.yml "$@"

# Delete infrastructure
rm -f azurerm.terraform_state.yml azure_credentials.sh
ansible-playbook teardown.yml "$@"
