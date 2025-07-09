#!/bin/sh

set -eux

ansible-playbook playbooks/run.yml -i inventory.yaml "$@"
