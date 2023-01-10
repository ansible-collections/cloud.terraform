# Terraform Collection for Ansible Automation Platform

The `cloud.terraform` collection supports running Terraform in sync with Ansible.

## Ansible version compatibility

This collection requires Ansible Core 2.13 or later and thus Python 3.8 or later.

## Included content
<!--start collection content-->
### Modules
Name | Description
--- | ---
[cloud.terraform.terraform](https://github.com/ansible-collections/cloud.terraform/blob/main/docs/cloud.terraform.terraform_module.rst)|Manages a Terraform deployment (and plans)
[cloud.terraform.terraform_output](https://github.com/ansible-collections/cloud.terraform/blob/main/docs/cloud.terraform.terraform_output_module.rst)|Returns Terraform module outputs.

### Lookup
Name | Description
--- | ---
[cloud.terraform.tf_output](https://github.com/ansible-collections/cloud.terraform/blob/main/docs/cloud.terraform.tf_output_lookup.rst)|Reads state file outputs.

### Inventory
Name | Description
--- | ---
[cloud.terraform.terraform_provider](https://github.com/ansible-collections/cloud.terraform/blob/main/docs/cloud.terraform.terraform_provider_inventory.rst)|Builds an inventory from Terraform state file.

### Roles
Name | Description
--- | ---
[cloud.terraform.git_plan](https://github.com/ansible-collections/cloud.terraform/blob/main/docs/cloud.terraform.git_plan_role.rst)|Clones a Git repository and applys a plan from it.
[cloud.terraform.inventory_from_outputs](https://github.com/ansible-collections/cloud.terraform/blob/main/docs/cloud.terraform.inventory_from_outputs_role.rst)|Creates an in-memory inventory from Terraform outputs.

<!--end collection content-->

## Installing this collection

You can install the cloud.terraform collection with the Ansible Galaxy CLI:

    ansible-galaxy collection install cloud.terraform

You can also include it in a `requirements.yml` file and install it with `ansible-galaxy collection install -r requirements.yml`, using the format:

```yaml
---
collections:
  - name: cloud.terraform
```

A specific version of the collection can be installed by using the `version` keyword in the `requirements.yml` file:

```yaml
---
collections:
  - name: cloud.terraform
    version: 1.0.0
```

## Using this collection

You can either call modules by their Fully Qualified Collection Name (FQCN), such as `cloud.terraform.terraform`, or you can call modules by their short name if you list the `cloud.terraform` collection in the playbook's `collections` keyword:

```yaml
---
  - name: Basic deploy of a service
    cloud.terraform.terraform:
      project_path: '{{ project_dir }}'
      state: present
```

## Developing and testing

The project uses `mypy` and `black`.
Black works without special configuration, while `mypy` requires a valid package structure.
Assuming this repository is checked out in the proper structure,
e.g. `collections_root/ansible_collections/cloud/terraform/`, run:

```shell
black --check --diff .
black .

export MYPYPATH="$(realpath "$PWD/../../../")"
mypy -p ansible_collections.cloud.terraform.plugins
```

Sanity and unit tests are run as normal:

```shell
ansible-test sanity
ansible-test units
antsibull-docs lint-collection-docs .
```

To run integration tests, install `terraform` and ensure it is in your `PATH`.
If you want to run cloud integration tests, ensure you log in to the clouds:

```shell
# using the "default" profile on AWS
aws configure set aws_access_key_id     my-access-key
aws configure set aws_secret_access_key my-secret-key
aws configure set region                eu-north-1

# Azure login
az login
az account set --subscription <id>

# GCP login
gcloud auth application-default login
gcloud auth application-default set-quota-project <id>

black --check --diff .
MYPYPATH="$(realpath "$PWD/../../../")" mypy -p ansible_collections.cloud.terraform.plugins
ansible-test integration [target] [--exclude aws|azure|gcp]

# Generate docs
ansible-doc --list | grep cloud.terraform | cut -d " " -f 1 | xargs -I {} antsibull-docs plugin --dest-dir docs/ {}
```

## Licensing

GNU General Public License v3.0 or later.

See [LICENSE](https://github.com/ansible-collections/cloud.terraform/blob/main/LICENSE) to see the full text.

