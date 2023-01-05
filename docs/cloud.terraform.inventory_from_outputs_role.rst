
.. Document meta

:orphan:
:github_url: https://github.com/ansible-collections/cloud.terraform/edit/main/roles/inventory_from_outputs/meta/argument_specs.yml?description=%23%23%23%23%23%20SUMMARY%0A%3C!---%20Your%20description%20here%20--%3E%0A%0A%0A%23%23%23%23%23%20ISSUE%20TYPE%0A-%20Docs%20Pull%20Request%0A%0A%2Blabel:%20docsite_pr

.. role:: ansible-option-type
.. role:: ansible-option-elements
.. role:: ansible-option-required
.. role:: ansible-option-versionadded
.. role:: ansible-option-aliases
.. role:: ansible-option-choices
.. role:: ansible-option-choices-default-mark
.. role:: ansible-option-default-bold

.. Anchors

.. _ansible_collections.cloud.terraform.inventory_from_outputs_role:

.. Anchors: aliases


.. Title

cloud.terraform.inventory_from_outputs role -- Create an in-memory inventory from Terraform outputs.
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

.. Collection note

.. note::
    This role is part of the `cloud.terraform collection <https://galaxy.ansible.com/cloud/terraform>`_ (version 1.0.0).

    To install it use: :code:`ansible-galaxy collection install cloud.terraform`.

    To use it in a playbook, specify: :code:`cloud.terraform.inventory_from_outputs`.

.. contents::
   :local:
   :depth: 2


.. Entry point title

Entry point ``main`` -- Create an in-memory inventory from Terraform outputs.
-----------------------------------------------------------------------------

.. version_added


.. Deprecated


Synopsis
^^^^^^^^

.. Description

- Create an in-memory inventory from Terraform outputs.

.. Requirements


.. Options

Parameters
^^^^^^^^^^

.. rst-class:: ansible-option-table

.. list-table::
  :width: 100%
  :widths: auto
  :header-rows: 1

  * - Parameter
    - Comments

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-main--mapping_variables"></div>

      .. _ansible_collections.cloud.terraform.inventory_from_outputs_role__parameter-main__mapping_variables:

      .. rst-class:: ansible-option-title

      **mapping_variables**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-main--mapping_variables" title="Permalink to this option"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`dictionary` / :ansible-option-required:`required`

      :ansible-option-versionadded:`added in cloud.terraform 1.0.0`





      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Names that define the mapping between Terraform output variables and inventory host variables.


      .. raw:: html

        </div>
    
  * - .. raw:: html

        <div class="ansible-option-indent"></div><div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-main--mapping_variables/group"></div>

      .. _ansible_collections.cloud.terraform.inventory_from_outputs_role__parameter-main__mapping_variables/group:

      .. rst-class:: ansible-option-title

      **group**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-main--mapping_variables/group" title="Permalink to this option"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`string` / :ansible-option-required:`required`

      :ansible-option-versionadded:`added in cloud.terraform 1.0.0`





      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-indent-desc"></div><div class="ansible-option-cell">

      The Terraform variable that contains the group the resulting host will be a member of.


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-indent"></div><div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-main--mapping_variables/host_list"></div>

      .. _ansible_collections.cloud.terraform.inventory_from_outputs_role__parameter-main__mapping_variables/host_list:

      .. rst-class:: ansible-option-title

      **host_list**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-main--mapping_variables/host_list" title="Permalink to this option"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`string` / :ansible-option-required:`required`

      :ansible-option-versionadded:`added in cloud.terraform 1.0.0`





      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-indent-desc"></div><div class="ansible-option-cell">

      The Terraform variable that contains the list of hosts to be processed into the in-memory inventory.

      Other keys in the mapping\_variables parameter refer to properties of the items of this list.


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-indent"></div><div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-main--mapping_variables/ip"></div>

      .. _ansible_collections.cloud.terraform.inventory_from_outputs_role__parameter-main__mapping_variables/ip:

      .. rst-class:: ansible-option-title

      **ip**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-main--mapping_variables/ip" title="Permalink to this option"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`string` / :ansible-option-required:`required`

      :ansible-option-versionadded:`added in cloud.terraform 1.0.0`





      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-indent-desc"></div><div class="ansible-option-cell">

      The Terraform variable that contains the IP or hostname of the resulting inventory host.

      Maps directly to ansible\_host.


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-indent"></div><div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-main--mapping_variables/name"></div>

      .. _ansible_collections.cloud.terraform.inventory_from_outputs_role__parameter-main__mapping_variables/name:

      .. rst-class:: ansible-option-title

      **name**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-main--mapping_variables/name" title="Permalink to this option"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`string` / :ansible-option-required:`required`

      :ansible-option-versionadded:`added in cloud.terraform 1.0.0`





      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-indent-desc"></div><div class="ansible-option-cell">

      The Terraform variable that contains the name of the resulting inventory host.


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-indent"></div><div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-main--mapping_variables/user"></div>

      .. _ansible_collections.cloud.terraform.inventory_from_outputs_role__parameter-main__mapping_variables/user:

      .. rst-class:: ansible-option-title

      **user**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-main--mapping_variables/user" title="Permalink to this option"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`string` / :ansible-option-required:`required`

      :ansible-option-versionadded:`added in cloud.terraform 1.0.0`





      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-indent-desc"></div><div class="ansible-option-cell">

      The Terraform variable that contains the username of the resulting inventory host.

      Maps directly to ansible\_user.


      .. raw:: html

        </div>


  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-main--project_path"></div>

      .. _ansible_collections.cloud.terraform.inventory_from_outputs_role__parameter-main__project_path:

      .. rst-class:: ansible-option-title

      **project_path**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-main--project_path" title="Permalink to this option"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`path`

      :ansible-option-versionadded:`added in cloud.terraform 1.0.0`





      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      The path to the root of the Terraform directory with the .tfstate file.

      Mutually exclusive with state\_file.


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-main--state_file"></div>

      .. _ansible_collections.cloud.terraform.inventory_from_outputs_role__parameter-main__state_file:

      .. rst-class:: ansible-option-title

      **state_file**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-main--state_file" title="Permalink to this option"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`path`

      :ansible-option-versionadded:`added in cloud.terraform 1.0.0`





      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      An absolute path to an existing Terraform state file.

      Mutually exclusive with project\_path.


      .. raw:: html

        </div>


.. Notes


.. Seealso




.. Extra links

Collection links
~~~~~~~~~~~~~~~~

.. raw:: html

  <p class="ansible-links">
    <a href="https://github.com/ansible-collections/cloud.terraform/issues" aria-role="button" target="_blank" rel="noopener external">Issue Tracker</a>
    <a href="https://github.com/ansible-collections/cloud.terraform" aria-role="button" target="_blank" rel="noopener external">Repository (Sources)</a>
    <a href="https://github.com/ansible-collections/cloud.terraform/issues/new/choose" aria-role="button" target="_blank" rel="noopener external">Report an issue</a>
  </p>

.. Parsing errors

