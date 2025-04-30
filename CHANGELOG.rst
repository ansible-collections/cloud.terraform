============================================
The cloud.terraform collection Release Notes
============================================

.. contents:: Topics

v3.1.0
======

Release Summary
---------------

This release includes bug fixes and new feature for the ``terraform_state`` inventory plugin.

Minor Changes
-------------

- Bump version of ansible-lint to minimum 25.1.2 (https://github.com/ansible-collections/cloud.terraform/pull/176).
- inventory/terraform_provider - Remove custom `read_config_data()` method (https://github.com/ansible-collections/cloud.terraform/pull/181).
- inventory/terraform_state - Remove custom `read_config_data()` method (https://github.com/ansible-collections/cloud.terraform/pull/181).
- inventory/terraform_state - Support for custom Terraform providers (https://github.com/ansible-collections/cloud.terraform/pull/146).

Bugfixes
--------

- inventory/terraform_state - use ``terraform pull`` instead of ``terraform show`` to parse raw state file to avoid provider versioning constraints (https://github.com/ansible-collections/cloud.terraform/issues/151).

v2.2.0
======

Release Summary
---------------

This release includes bug fixes and new feature for the ``terraform_state`` inventory plugin.

Minor Changes
-------------

- Bump version of ansible-lint to minimum 25.1.2 (https://github.com/ansible-collections/cloud.terraform/pull/176).
- inventory/terraform_provider - Remove custom `read_config_data()` method (https://github.com/ansible-collections/cloud.terraform/pull/181).
- inventory/terraform_state - Remove custom `read_config_data()` method (https://github.com/ansible-collections/cloud.terraform/pull/181).
- inventory/terraform_state - Support for custom Terraform providers (https://github.com/ansible-collections/cloud.terraform/pull/146).

Bugfixes
--------

- inventory/terraform_state - use ``terraform pull`` instead of ``terraform show`` to parse raw state file to avoid provider versioning constraints (https://github.com/ansible-collections/cloud.terraform/issues/151).

v3.0.0
======

Release Summary
---------------

This major release drops support for ``ansible-core < 2.15``.

Breaking Changes / Porting Guide
--------------------------------

- Drop support for ansible-core < 2.15 (https://github.com/ansible-collections/cloud.terraform/pull/138).

v2.1.0
======

Release Summary
---------------

The cloud.terraform 2.1.0 release includes a new module to ``plan_stash`` and a new inventory plugin ``terraform_state``.

New Plugins
-----------

Inventory
~~~~~~~~~

- terraform_state - Builds an inventory from resources created by cloud providers.

New Modules
-----------

- plan_stash - Handle the base64 encoding or decoding of a terraform plan file

v2.0.0
======

Breaking Changes / Porting Guide
--------------------------------

- Remove support for ansible-core < 2.14 (https://github.com/ansible-collections/cloud.terraform/pull/102).

Major Changes
-------------

- terraform_provider  - Allow ``project_path`` in terraform_provider inventory plugin to accept a list of paths (https://github.com/ansible-collections/cloud.terraform/pull/55).
- terraform_provider - Added ``search_child_modules`` option (https://github.com/ansible-collections/cloud.terraform/pull/55).

Minor Changes
-------------

- Removed integration tests workaround in terrform_provider. (https://github.com/ansible-collections/cloud.terraform/pull/84)
- Set default of ``state_file`` in terraform_provider inventory plugin to a blank string (https://github.com/ansible-collections/cloud.terraform/pull/55).
- terraform  - add support for ``workspace`` when running ``terraform output`` (https://github.com/ansible-collections/cloud.terraform/issues/85).
- terraform - cleanup temporary file create during module execution. (https://github.com/ansible-collections/cloud.terraform/issues/2)
- terraform_output -  add support for ``workspace`` when running ``terraform output`` (https://github.com/ansible-collections/cloud.terraform/issues/85).
- tf_output - add support for ``workspace`` when running ``terraform output`` (https://github.com/ansible-collections/cloud.terraform/issues/85).

Bugfixes
--------

- module_utils - Accept Terraform executables present on PATH passed in as ``binary_path`` without specifying their absolute path. (https://github.com/ansible-collections/cloud.terraform/issues/49)
- module_utils - Allow ``nested_type`` attribute in terraform schema. (https://github.com/ansible-collections/cloud.terraform/issues/93)
- module_utils - Fix AWS SQS queue creation. The ``values`` attribute in terraform output is optional. SQS is one of (rare) cases where ``values`` is absent. (https://github.com/ansible-collections/cloud.terraform/issues/86)
- move test requirements out of the requirements.txt file (https://github.com/ansible-collections/cloud.terraform/pull/67).
- terraform - fix issue with ``plan_file`` option specified with ``check_mode=true`` and ``state`` set to one of ``present`` and ``absent``, the module is enable now to generate a Terraform file to the specified location (https://github.com/ansible-collections/cloud.terraform/issues/87).
- terraform - fix spaces between characters in command field in result (https://github.com/ansible-collections/cloud.terraform/pull/76).

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
