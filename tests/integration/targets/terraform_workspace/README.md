# terraform_workspace integration test target

## Requirements

A valid HCP Terraform / Terraform Entreprise cloud account.
Set the variables `terraform_organization_name` and `terraform_organization_token` into `inventory.yaml`


## Workspace configuration

Create the following workspaces:

| **Name** | **Tags** |
| -------------- | --------------------- |
| ansible_default | `project=ansible` |
| ansible_default_with_tags | `project=ansible`, `default=true` |
| ansible_cloud_config |  |

