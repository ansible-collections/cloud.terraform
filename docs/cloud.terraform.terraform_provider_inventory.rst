
.. Document meta

:orphan:
:github_url: https://github.com/ansible-collections/cloud.terraform/edit/main/plugins/inventory/terraform_provider.py?description=%23%23%23%23%23%20SUMMARY%0A%3C!---%20Your%20description%20here%20--%3E%0A%0A%0A%23%23%23%23%23%20ISSUE%20TYPE%0A-%20Docs%20Pull%20Request%0A%0A%2Blabel:%20docsite_pr

.. |antsibull-internal-nbsp| unicode:: 0xA0
    :trim:

.. role:: ansible-attribute-support-label
.. role:: ansible-attribute-support-property
.. role:: ansible-attribute-support-full
.. role:: ansible-attribute-support-partial
.. role:: ansible-attribute-support-none
.. role:: ansible-attribute-support-na
.. role:: ansible-option-type
.. role:: ansible-option-elements
.. role:: ansible-option-required
.. role:: ansible-option-versionadded
.. role:: ansible-option-aliases
.. role:: ansible-option-choices
.. role:: ansible-option-choices-default-mark
.. role:: ansible-option-default-bold
.. role:: ansible-option-configuration
.. role:: ansible-option-returned-bold
.. role:: ansible-option-sample-bold

.. Anchors

.. _ansible_collections.cloud.terraform.terraform_provider_inventory:

.. Anchors: short name for ansible.builtin

.. Anchors: aliases



.. Title

cloud.terraform.terraform_provider inventory -- Builds an inventory from Terraform state file.
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

.. Collection note

.. note::
    This inventory plugin is part of the `cloud.terraform collection <https://galaxy.ansible.com/cloud/terraform>`_ (version 1.0.0).

    To install it, use: :code:`ansible-galaxy collection install cloud.terraform`.

    To use it in a playbook, specify: :code:`cloud.terraform.terraform_provider`.

.. version_added

.. rst-class:: ansible-version-added

New in cloud.terraform 1.1.0

.. contents::
   :local:
   :depth: 1

.. Deprecated


Synopsis
--------

.. Description

- Builds an inventory from specified state file.
- To read state file command "Terraform show" is used, thus requiring initialized working directory.
- Does not support caching.


.. Aliases


.. Requirements






.. Options

Parameters
----------


.. rst-class:: ansible-option-table

.. list-table::
  :width: 100%
  :widths: auto
  :header-rows: 1

  * - Parameter
    - Comments

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-binary_path"></div>

      .. _ansible_collections.cloud.terraform.terraform_provider_inventory__parameter-binary_path:

      .. rst-class:: ansible-option-title

      **binary_path**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-binary_path" title="Permalink to this option"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`path`

      :ansible-option-versionadded:`added in cloud.terraform 1.1.0`





      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      The path of a terraform binary to use.


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-plugin"></div>

      .. _ansible_collections.cloud.terraform.terraform_provider_inventory__parameter-plugin:

      .. rst-class:: ansible-option-title

      **plugin**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-plugin" title="Permalink to this option"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`string` / :ansible-option-required:`required`

      :ansible-option-versionadded:`added in cloud.terraform 1.1.0`





      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      The name of the Inventory Plugin.

      This should always be \ :literal:`cloud.terraform.terraform\_provider`\ .


      .. rst-class:: ansible-option-line

      :ansible-option-choices:`Choices:`

      - :ansible-option-choices-entry:`"cloud.terraform.terraform\_provider"`


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-project_path"></div>

      .. _ansible_collections.cloud.terraform.terraform_provider_inventory__parameter-project_path:

      .. rst-class:: ansible-option-title

      **project_path**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-project_path" title="Permalink to this option"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`path`

      :ansible-option-versionadded:`added in cloud.terraform 1.1.0`





      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      The path to the initialized Terraform directory with the .tfstate file.

      If \ :emphasis:`state\_file`\  is not specified, \ :literal:`terraform.tfstate`\  in \ :emphasis:`project\_path`\  is used as an inventory source.

      If \ :emphasis:`state\_file`\  and \ :emphasis:`project\_path`\  are not specified, \ :literal:`terraform.tfstate`\  file in the current working directory is used as an inventory source.


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-state_file"></div>

      .. _ansible_collections.cloud.terraform.terraform_provider_inventory__parameter-state_file:

      .. rst-class:: ansible-option-title

      **state_file**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-state_file" title="Permalink to this option"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`path`

      :ansible-option-versionadded:`added in cloud.terraform 1.1.0`





      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Path to an existing Terraform state file to be used as an inventory source.

      If \ :emphasis:`state\_file`\  is not specified, \ :literal:`terraform.tfstate`\  in \ :emphasis:`project\_path`\  is used as an inventory source.

      If \ :emphasis:`state\_file`\  and \ :emphasis:`project\_path`\  are not specified, \ :literal:`terraform.tfstate`\  file in the current working directory is used as an inventory source.


      .. raw:: html

        </div>


.. Attributes


.. Notes


.. Seealso


.. Examples

Examples
--------

.. code-block:: yaml+jinja

    
    # Example configuration file inventory.yml, that creates an inventory from terraform.tfstate file in cwd
    plugin: cloud.terraform.terraform_provider
    # Running command `ansible-inventory -i inventory.yml --graph --vars` would then produce the inventory:
    # @all:
    #   |--@anothergroup:
    #   |  |--somehost
    #   |  |  |--{group_hello = from group!}
    #   |  |  |--{group_variable = 11}
    #   |  |  |--{host_hello = from host!}
    #   |  |  |--{host_variable = 7}
    #   |--@childlessgroup:
    #   |--@somegroup:
    #   |  |--@anotherchild:
    #   |  |--@somechild:
    #   |  |  |--anotherhost
    #   |  |  |  |--{group_hello = from group!}
    #   |  |  |  |--{group_variable = 11}
    #   |  |  |  |--{host_hello = from anotherhost!}
    #   |  |  |  |--{host_variable = 5}
    #   |  |--somehost
    #   |  |  |--{group_hello = from group!}
    #   |  |  |--{group_variable = 11}
    #   |  |  |--{host_hello = from host!}
    #   |  |  |--{host_variable = 7}
    #   |  |--{group_hello = from group!}
    #   |  |--{group_variable = 11}
    #   |--@ungrouped:
    #   |  |--ungrupedhost

    # Example configuration file that creates an inventory from terraform.tfstate file in selected project directory
    plugin: cloud.terraform.terraform_provider
    project_path: some/project/path

    # Example configuration file that creates an inventory from specified state file
    plugin: cloud.terraform.terraform_provider
    state_file: some/state/file/path

    # Example configuration file that creates an inventory from mycustomstate.tfstate file in selected project directory
    plugin: cloud.terraform.terraform_provider
    project_path: some/project/path
    state_file: mycustomstate.tfstate




.. Facts


.. Return values


..  Status (Presently only deprecated)


.. Authors

Authors
~~~~~~~

- Polona Mihalič (@PolonaM)


.. hint::
    Configuration entries for each entry type have a low to high priority order. For example, a variable that is lower in the list will override a variable that is higher up.

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

