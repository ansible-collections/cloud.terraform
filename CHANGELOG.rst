============================================
The cloud.terraform collection Release Notes
============================================

.. contents:: Topics


v1.1.0
======

Major Changes
-------------

- Added the git_plan role to apply a Terraform plan stored in a Git repository.
- Added the inventory_from_outputs role to construct an in-memory inventory from Terraform outputs.
- Added the terraform_output module which parses values from terraform outputs.
- Check mode now works as intended and produces correct "changed" output and results.
- Inventory plugin cloud.terraform.terraform_provider added. (https://github.com/ansible-collections/cloud.terraform/pull/22)
- Support diff mode in cloud.terraform.terraform both in check mode and in non-check mode. (https://github.com/ansible-collections/cloud.terraform/pull/11)
- Terraform output lookup module added (https://github.com/ansible-collections/cloud.terraform/pull/12).

Minor Changes
-------------

- Removed "required_one_of" condition from terraform_output module. (https://github.com/ansible-collections/cloud.terraform/pull/31).
- Slight code reorganization to always run terraform plan, and then optionally apply the generated plan.
- Terraform output lookup module - documentation for state_file option updated. (https://github.com/ansible-collections/cloud.terraform/pull/29).
- git_plan and inventory_from_outputs role's argument_spec.yml updated to be able to generate documentation (https://github.com/ansible-collections/cloud.terraform/pull/28)
- meta/runtime.yml - Drop space in requires_ansible that was preventing the upload on Galaxy (https://github.com/ansible-collections/cloud.terraform/pull/8).

Deprecated Features
-------------------

- state=planned is deprecated. Use check_mode=true at the module level instead.

Bugfixes
--------

- Integration tests to test support of AWS, Azure and GCP.
- Major refactoring of the cloud.terraform collection, restructuring and compartmentalizing code.
- Removed "mutually exclusive" condition for state_file and project_path in inventory_from_outputs role, since terraform_output module doesn't require this. (https://github.com/ansible-collections/cloud.terraform/pull/39)
- Several integration tests were added to test end-to-end behaviour.
- Terraform module - fix now allows the possibility that the key "value" is not always present in the terraform plan thus avoiding KeyError. (https://github.com/ansible-collections/cloud.terraform/pull/45)
- Terraform module - fix now expands the providers schema with block_types section so when checking if (block) attribute is sensitive in providers schema KeyError is now avoided. (https://github.com/ansible-collections/cloud.terraform/pull/46)
- Terraform_output - fix now sets "outputs" variable to None in case of TerraformWarning to avoid undefined variable error. (https://github.com/ansible-collections/cloud.terraform/pull/31)
- Type hints added to the cloud.terraform collection for easier future maintenance and reliability.
- Updated host and group name in cloud.terraform.terraform_provider inventory plugin. (https://github.com/ansible-collections/cloud.terraform/pull/34)
- terraform_output module - when providing name and state_file parameters, the value of the requested output wasn't returned. This issue was solved by changing the order of the name and state parameters in the invoked Terraform command (https://github.com/ansible-collections/cloud.terraform/pull/19).

New Plugins
-----------

Inventory
~~~~~~~~~

- terraform_provider - Builds an inventory from Terraform state file.
