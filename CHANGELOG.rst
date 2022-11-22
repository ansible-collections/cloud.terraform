============================================
The cloud.terraform collection Release Notes
============================================

.. contents:: Topics


v1.0.0
======

Major Changes
-------------

- Added the git_plan role to apply a Terraform plan stored in a Git repository.
- Added the inventory_from_outputs role to construct an in-memory inventory from Terraform outputs.
- Added the terraform_output module which parses values from terraform outputs.
- Check mode now works as intended and produces correct "changed" output and results.

Minor Changes
-------------

- Slight code reorganization to always run terraform plan, and then optionally apply the generated plan.

Deprecated Features
-------------------

- state=planned is deprecated. Use check_mode=true at the module level instead.

Bugfixes
--------

- Integration tests to test support of AWS, Azure and GCP.
- Several integration tests were added to test end-to-end behaviour.
