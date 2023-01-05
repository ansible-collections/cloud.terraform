


.. _plugins_in_cloud.terraform:

Cloud.Terraform
===============

Collection version 1.0.0

.. contents::
   :local:
   :depth: 1

Description
-----------

Terraform collection for Ansible.

**Author:**

* Ansible (https://github.com/ansible)

**Supported ansible-core versions:**

* 2.13.0 or newer

.. raw:: html

  <p class="ansible-links">
    <a href="https://github.com/ansible-collections/cloud.terraform/issues" aria-role="button" target="_blank" rel="noopener external">Issue Tracker</a>
    <a href="https://github.com/ansible-collections/cloud.terraform" aria-role="button" target="_blank" rel="noopener external">Repository (Sources)</a>
    <a href="https://github.com/ansible-collections/cloud.terraform/issues/new/choose" aria-role="button" target="_blank" rel="noopener external">Report an issue</a>
  </p>



.. toctree::
    :maxdepth: 1


Plugin Index
------------

These are the plugins in the cloud.terraform collection:


Modules
~~~~~~~

* :ref:`terraform module <ansible_collections.cloud.terraform.terraform_module>` -- Manages a Terraform deployment (and plans)
* :ref:`terraform_output module <ansible_collections.cloud.terraform.terraform_output_module>` -- Returns Terraform module outputs.

.. toctree::
    :maxdepth: 1
    :hidden:

    terraform_module
    terraform_output_module


Lookup Plugins
~~~~~~~~~~~~~~

* :ref:`tf_output lookup <ansible_collections.cloud.terraform.tf_output_lookup>` -- Read state file outputs.

.. toctree::
    :maxdepth: 1
    :hidden:

    tf_output_lookup


Role Index
----------

These are the roles in the cloud.terraform collection:

* :ref:`git_plan role <ansible_collections.cloud.terraform.git_plan_role>` -- Clone a Git repository and apply a plan from it.
* :ref:`inventory_from_outputs role <ansible_collections.cloud.terraform.inventory_from_outputs_role>` -- Create an in-memory inventory from Terraform outputs.

.. toctree::
    :maxdepth: 1
    :hidden:

    git_plan_role
    inventory_from_outputs_role

