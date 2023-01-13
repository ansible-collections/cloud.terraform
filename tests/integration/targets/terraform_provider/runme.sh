#!/bin/sh

set -eux

# TODO: remove env var and uncomment when ansibe provider is available 
export TESTING_STATE_FILE="True"

# (
#     mkdir -p subdir2/
#     cp test.yml subdir2/
#     cp ansible_provider.tf subdir2/
#     cd subdir2/
#     terraform init
#     terraform apply -auto-approve -state mycustomstate.tfstate
# )
# ansible-playbook -i localhost, -i inventory2.yml test.yml

# (
#     mkdir -p subdir3/
#     cp test.yml subdir3/
#     cp ansible_provider.tf subdir3/
#     cd subdir3/
#     terraform init
#     terraform apply -auto-approve
# )
# ansible-playbook -i localhost, -i inventory3.yml test.yml

# (
#     mkdir -p subdir4/
#     cp test.yml subdir4/
#     cp ansible_provider.tf subdir4/
#     cd subdir4/
#     terraform init
#     terraform apply -auto-approve -state mystate.tfstate
#     cd ..
#     terraform init
# )
# ansible-playbook -i localhost, -i inventory4.yml test.yml

# (
#     terraform init
#     terraform apply -auto-approve
# )
ansible-playbook -i localhost, -i inventory1.yml test.yml
