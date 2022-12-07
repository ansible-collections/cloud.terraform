#!/bin/sh

set -eux

(
    mkdir -p subdir/
    cp outputs.tf subdir/
    cd subdir/
    terraform init
    terraform apply -var source_input=hello_project -auto-approve
    terraform apply -var source_input=hello_custom -auto-approve -state mycustomstate.tfstate
)

ansible-playbook test_outputs.yml
