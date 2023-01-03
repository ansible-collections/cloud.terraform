
.. Document meta

:orphan:
:github_url: https://github.com/ansible-collections/cloud.terraform/edit/main/plugins/modules/terraform.py?description=%23%23%23%23%23%20SUMMARY%0A%3C!---%20Your%20description%20here%20--%3E%0A%0A%0A%23%23%23%23%23%20ISSUE%20TYPE%0A-%20Docs%20Pull%20Request%0A%0A%2Blabel:%20docsite_pr

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

.. _ansible_collections.cloud.terraform.terraform_module:

.. Anchors: short name for ansible.builtin

.. Anchors: aliases



.. Title

cloud.terraform.terraform module -- Manages a Terraform deployment (and plans)
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

.. Collection note

.. note::
    This module is part of the `cloud.terraform collection <https://galaxy.ansible.com/cloud/terraform>`_ (version 1.0.0).

    To install it, use: :code:`ansible-galaxy collection install cloud.terraform`.
    You need further requirements to be able to use this module,
    see :ref:`Requirements <ansible_collections.cloud.terraform.terraform_module_requirements>` for details.

    To use it in a playbook, specify: :code:`cloud.terraform.terraform`.

.. version_added


.. contents::
   :local:
   :depth: 1

.. Deprecated


Synopsis
--------

.. Description

- Provides support for deploying resources with Terraform and pulling resource information back into Ansible.


.. Aliases


.. Requirements

.. _ansible_collections.cloud.terraform.terraform_module_requirements:

Requirements
------------
The below requirements are needed on the host that executes this module.

- terraform






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
        <div class="ansibleOptionAnchor" id="parameter-backend_config"></div>

      .. _ansible_collections.cloud.terraform.terraform_module__parameter-backend_config:

      .. rst-class:: ansible-option-title

      **backend_config**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-backend_config" title="Permalink to this option"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`dictionary`

      :ansible-option-versionadded:`added in cloud.terraform 1.0.0`


      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      A group of key-values to provide at init stage to the -backend-config parameter.


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-backend_config_files"></div>

      .. _ansible_collections.cloud.terraform.terraform_module__parameter-backend_config_files:

      .. rst-class:: ansible-option-title

      **backend_config_files**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-backend_config_files" title="Permalink to this option"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`list` / :ansible-option-elements:`elements=path`

      :ansible-option-versionadded:`added in cloud.terraform 1.0.0`


      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      The path to a configuration file to provide at init state to the -backend-config parameter. This can accept a list of paths to multiple configuration files.


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-binary_path"></div>

      .. _ansible_collections.cloud.terraform.terraform_module__parameter-binary_path:

      .. rst-class:: ansible-option-title

      **binary_path**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-binary_path" title="Permalink to this option"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`path`

      :ansible-option-versionadded:`added in cloud.terraform 1.0.0`


      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      The path of a terraform binary to use.


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-check_destroy"></div>

      .. _ansible_collections.cloud.terraform.terraform_module__parameter-check_destroy:

      .. rst-class:: ansible-option-title

      **check_destroy**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-check_destroy" title="Permalink to this option"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`boolean`

      :ansible-option-versionadded:`added in cloud.terraform 1.0.0`


      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Apply only when no resources are destroyed. Note that this only prevents "destroy" actions, but not "destroy and re-create" actions. This option is ignored when \ :emphasis:`state=absent`\ .


      .. rst-class:: ansible-option-line

      :ansible-option-choices:`Choices:`

      - :ansible-option-choices-entry-default:`false` :ansible-option-choices-default-mark:`← (default)`
      - :ansible-option-choices-entry:`true`


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-complex_vars"></div>

      .. _ansible_collections.cloud.terraform.terraform_module__parameter-complex_vars:

      .. rst-class:: ansible-option-title

      **complex_vars**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-complex_vars" title="Permalink to this option"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`boolean`

      :ansible-option-versionadded:`added in cloud.terraform 1.0.0`


      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Enable/disable capability to handle complex variable structures for \ :literal:`terraform`\ .

      If \ :literal:`true`\  the \ :emphasis:`variables`\  also accepts dictionaries, lists, and booleans to be passed to \ :literal:`terraform`\ . Strings that are passed are correctly quoted.

      When disabled, supports only simple variables (strings, integers, and floats), and passes them on unquoted.


      .. rst-class:: ansible-option-line

      :ansible-option-choices:`Choices:`

      - :ansible-option-choices-entry-default:`false` :ansible-option-choices-default-mark:`← (default)`
      - :ansible-option-choices-entry:`true`


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-force_init"></div>

      .. _ansible_collections.cloud.terraform.terraform_module__parameter-force_init:

      .. rst-class:: ansible-option-title

      **force_init**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-force_init" title="Permalink to this option"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`boolean`

      :ansible-option-versionadded:`added in cloud.terraform 1.0.0`


      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      To avoid duplicating infra, if a state file can't be found this will force a \ :literal:`terraform init`\ . Generally, this should be turned off unless you intend to provision an entirely new Terraform deployment.


      .. rst-class:: ansible-option-line

      :ansible-option-choices:`Choices:`

      - :ansible-option-choices-entry-default:`false` :ansible-option-choices-default-mark:`← (default)`
      - :ansible-option-choices-entry:`true`


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-init_reconfigure"></div>

      .. _ansible_collections.cloud.terraform.terraform_module__parameter-init_reconfigure:

      .. rst-class:: ansible-option-title

      **init_reconfigure**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-init_reconfigure" title="Permalink to this option"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`boolean`

      :ansible-option-versionadded:`added in cloud.terraform 1.0.0`


      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Forces backend reconfiguration during init.


      .. rst-class:: ansible-option-line

      :ansible-option-choices:`Choices:`

      - :ansible-option-choices-entry-default:`false` :ansible-option-choices-default-mark:`← (default)`
      - :ansible-option-choices-entry:`true`


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-lock"></div>

      .. _ansible_collections.cloud.terraform.terraform_module__parameter-lock:

      .. rst-class:: ansible-option-title

      **lock**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-lock" title="Permalink to this option"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`boolean`

      :ansible-option-versionadded:`added in cloud.terraform 1.0.0`


      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Enable statefile locking, if you use a service that accepts locks (such as S3+DynamoDB) to store your statefile.


      .. rst-class:: ansible-option-line

      :ansible-option-choices:`Choices:`

      - :ansible-option-choices-entry:`false`
      - :ansible-option-choices-entry-default:`true` :ansible-option-choices-default-mark:`← (default)`


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-lock_timeout"></div>

      .. _ansible_collections.cloud.terraform.terraform_module__parameter-lock_timeout:

      .. rst-class:: ansible-option-title

      **lock_timeout**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-lock_timeout" title="Permalink to this option"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`integer`

      :ansible-option-versionadded:`added in cloud.terraform 1.0.0`


      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      How long to maintain the lock on the statefile, if you use a service that accepts locks (such as S3+DynamoDB).


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-overwrite_init"></div>

      .. _ansible_collections.cloud.terraform.terraform_module__parameter-overwrite_init:

      .. rst-class:: ansible-option-title

      **overwrite_init**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-overwrite_init" title="Permalink to this option"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`boolean`

      :ansible-option-versionadded:`added in cloud.terraform 1.0.0`


      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Run init even if \ :literal:`.terraform/terraform.tfstate`\  already exists in \ :emphasis:`project\_path`\ .


      .. rst-class:: ansible-option-line

      :ansible-option-choices:`Choices:`

      - :ansible-option-choices-entry:`false`
      - :ansible-option-choices-entry-default:`true` :ansible-option-choices-default-mark:`← (default)`


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-parallelism"></div>

      .. _ansible_collections.cloud.terraform.terraform_module__parameter-parallelism:

      .. rst-class:: ansible-option-title

      **parallelism**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-parallelism" title="Permalink to this option"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`integer`

      :ansible-option-versionadded:`added in cloud.terraform 1.0.0`


      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Restrict concurrent operations when Terraform applies the plan.


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-plan_file"></div>

      .. _ansible_collections.cloud.terraform.terraform_module__parameter-plan_file:

      .. rst-class:: ansible-option-title

      **plan_file**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-plan_file" title="Permalink to this option"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`path`

      :ansible-option-versionadded:`added in cloud.terraform 1.0.0`


      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      The path to an existing Terraform plan file to apply. If this is not specified, Ansible will build a new TF plan and execute it.

      Note that this option is required if 'state' has the 'planned' value. In this case, the plan file is only generated, but not applied.


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-plugin_paths"></div>

      .. _ansible_collections.cloud.terraform.terraform_module__parameter-plugin_paths:

      .. rst-class:: ansible-option-title

      **plugin_paths**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-plugin_paths" title="Permalink to this option"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`list` / :ansible-option-elements:`elements=path`

      :ansible-option-versionadded:`added in cloud.terraform 1.0.0`


      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      List of paths containing Terraform plugin executable files.

      Plugin executables can be downloaded from \ https://releases.hashicorp.com/\ .

      When set, the plugin discovery and auto-download behavior of Terraform is disabled.

      The directory structure in the plugin path can be tricky. The Terraform docs \ https://learn.hashicorp.com/tutorials/terraform/automate-terraform#pre-installed-plugins\  show a simple directory of files, but actually, the directory structure has to follow the same structure you would see if Terraform auto-downloaded the plugins. See the examples below for a tree output of an example plugin directory.


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-project_path"></div>

      .. _ansible_collections.cloud.terraform.terraform_module__parameter-project_path:

      .. rst-class:: ansible-option-title

      **project_path**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-project_path" title="Permalink to this option"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`path` / :ansible-option-required:`required`

      :ansible-option-versionadded:`added in cloud.terraform 1.0.0`


      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      The path to the root of the Terraform directory with the vars.tf/main.tf/etc to use.


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-provider_upgrade"></div>

      .. _ansible_collections.cloud.terraform.terraform_module__parameter-provider_upgrade:

      .. rst-class:: ansible-option-title

      **provider_upgrade**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-provider_upgrade" title="Permalink to this option"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`boolean`

      :ansible-option-versionadded:`added in cloud.terraform 1.0.0`


      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Allows Terraform init to upgrade providers to versions specified in the project's version constraints.


      .. rst-class:: ansible-option-line

      :ansible-option-choices:`Choices:`

      - :ansible-option-choices-entry-default:`false` :ansible-option-choices-default-mark:`← (default)`
      - :ansible-option-choices-entry:`true`


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-purge_workspace"></div>

      .. _ansible_collections.cloud.terraform.terraform_module__parameter-purge_workspace:

      .. rst-class:: ansible-option-title

      **purge_workspace**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-purge_workspace" title="Permalink to this option"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`boolean`

      :ansible-option-versionadded:`added in cloud.terraform 1.0.0`


      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Only works with state = absent

      If true, the workspace will be deleted after the "terraform destroy" action.

      The 'default' workspace will not be deleted.


      .. rst-class:: ansible-option-line

      :ansible-option-choices:`Choices:`

      - :ansible-option-choices-entry-default:`false` :ansible-option-choices-default-mark:`← (default)`
      - :ansible-option-choices-entry:`true`


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-state"></div>

      .. _ansible_collections.cloud.terraform.terraform_module__parameter-state:

      .. rst-class:: ansible-option-title

      **state**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-state" title="Permalink to this option"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`string`

      :ansible-option-versionadded:`added in cloud.terraform 1.0.0`


      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Goal state of given stage/project.

      Option \`planned\` is deprecated. Its function is equivalent to running the module in check mode.


      .. rst-class:: ansible-option-line

      :ansible-option-choices:`Choices:`

      - :ansible-option-choices-entry-default:`"present"` :ansible-option-choices-default-mark:`← (default)`
      - :ansible-option-choices-entry:`"absent"`
      - :ansible-option-choices-entry:`"planned"`


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-state_file"></div>

      .. _ansible_collections.cloud.terraform.terraform_module__parameter-state_file:

      .. rst-class:: ansible-option-title

      **state_file**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-state_file" title="Permalink to this option"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`path`

      :ansible-option-versionadded:`added in cloud.terraform 1.0.0`


      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      The path to an existing Terraform state file to use when building plan. If this is not specified, the default \ :literal:`terraform.tfstate`\  will be used.

      This option is ignored when plan is specified.


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-targets"></div>

      .. _ansible_collections.cloud.terraform.terraform_module__parameter-targets:

      .. rst-class:: ansible-option-title

      **targets**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-targets" title="Permalink to this option"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`list` / :ansible-option-elements:`elements=string`

      :ansible-option-versionadded:`added in cloud.terraform 1.0.0`


      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      A list of specific resources to target in this plan/application. The resources selected here will also auto-include any dependencies.


      .. rst-class:: ansible-option-line

      :ansible-option-default-bold:`Default:` :ansible-option-default:`[]`

      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-variables"></div>

      .. _ansible_collections.cloud.terraform.terraform_module__parameter-variables:

      .. rst-class:: ansible-option-title

      **variables**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-variables" title="Permalink to this option"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`dictionary`

      :ansible-option-versionadded:`added in cloud.terraform 1.0.0`


      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      A group of key-values pairs to override template variables or those in variables files. By default, only string and number values are allowed, which are passed on unquoted.

      Support complex variable structures (lists, dictionaries, numbers, and booleans) to reflect terraform variable syntax when \ :emphasis:`complex\_vars=true`\ .

      Ansible integers or floats are mapped to terraform numbers.

      Ansible strings are mapped to terraform strings.

      Ansible dictionaries are mapped to terraform objects.

      Ansible lists are mapped to terraform lists.

      Ansible booleans are mapped to terraform booleans.

      \ :strong:`Note`\  passwords passed as variables will be visible in the log output. Make sure to use \ :emphasis:`no\_log=true`\  in production!


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-variables_files"></div>
        <div class="ansibleOptionAnchor" id="parameter-variables_file"></div>

      .. _ansible_collections.cloud.terraform.terraform_module__parameter-variables_file:
      .. _ansible_collections.cloud.terraform.terraform_module__parameter-variables_files:

      .. rst-class:: ansible-option-title

      **variables_files**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-variables_files" title="Permalink to this option"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-aliases:`aliases: variables_file`

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`list` / :ansible-option-elements:`elements=path`

      :ansible-option-versionadded:`added in cloud.terraform 1.0.0`


      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      The path to a variables file for Terraform to fill into the TF configurations. This can accept a list of paths to multiple variables files.

      Up until Ansible 2.9, this option was usable as \ :emphasis:`variables\_file`\ .


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-workspace"></div>

      .. _ansible_collections.cloud.terraform.terraform_module__parameter-workspace:

      .. rst-class:: ansible-option-title

      **workspace**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-workspace" title="Permalink to this option"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`string`

      :ansible-option-versionadded:`added in cloud.terraform 1.0.0`


      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      The terraform workspace to work with.


      .. rst-class:: ansible-option-line

      :ansible-option-default-bold:`Default:` :ansible-option-default:`"default"`

      .. raw:: html

        </div>


.. Attributes


.. Notes

Notes
-----

.. note::
   - To just run a \ :literal:`terraform plan`\ , use check mode.

.. Seealso


.. Examples

Examples
--------

.. code-block:: yaml+jinja

    
    - name: Basic deploy of a service
      cloud.terraform.terraform:
        project_path: '{{ project_dir }}'
        state: present

    - name: Define the backend configuration at init
      cloud.terraform.terraform:
        project_path: 'project/'
        state: "{{ state }}"
        force_init: true
        backend_config:
          region: "eu-west-1"
          bucket: "some-bucket"
          key: "random.tfstate"

    - name: Define the backend configuration with one or more files at init
      cloud.terraform.terraform:
        project_path: 'project/'
        state: "{{ state }}"
        force_init: true
        backend_config_files:
          - /path/to/backend_config_file_1
          - /path/to/backend_config_file_2

    - name: Disable plugin discovery and auto-download by setting plugin_paths
      cloud.terraform.terraform:
        project_path: 'project/'
        state: "{{ state }}"
        force_init: true
        plugin_paths:
          - /path/to/plugins_dir_1
          - /path/to/plugins_dir_2

    - name: Complex variables example
      cloud.terraform.terraform:
        project_path: '{{ project_dir }}'
        state: present
        complex_vars: true
        variables:
          vm_name: "{{ inventory_hostname }}"
          vm_vcpus: 2
          vm_mem: 2048
          vm_additional_disks:
            - label: "Third Disk"
              size: 40
              thin_provisioned: true
              unit_number: 2
            - label: "Fourth Disk"
              size: 22
              thin_provisioned: true
              unit_number: 3
        force_init: true

    ### Example directory structure for plugin_paths example
    # $ tree /path/to/plugins_dir_1
    # /path/to/plugins_dir_1/
    # └── registry.terraform.io
    #     └── hashicorp
    #         └── vsphere
    #             ├── 1.24.0
    #             │   └── linux_amd64
    #             │       └── terraform-provider-vsphere_v1.24.0_x4
    #             └── 1.26.0
    #                 └── linux_amd64
    #                     └── terraform-provider-vsphere_v1.26.0_x4




.. Facts


.. Return values

Return Values
-------------
Common return values are documented :ref:`here <common_return_values>`, the following are the fields unique to this module:

.. rst-class:: ansible-option-table

.. list-table::
  :width: 100%
  :widths: auto
  :header-rows: 1

  * - Key
    - Description

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="return-command"></div>

      .. _ansible_collections.cloud.terraform.terraform_module__return-command:

      .. rst-class:: ansible-option-title

      **command**

      .. raw:: html

        <a class="ansibleOptionLink" href="#return-command" title="Permalink to this return value"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`string`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Full \ :literal:`terraform`\  command built by this module, in case you want to re-run the command outside the module or debug a problem.


      .. rst-class:: ansible-option-line

      :ansible-option-returned-bold:`Returned:` always

      .. rst-class:: ansible-option-line
      .. rst-class:: ansible-option-sample

      :ansible-option-sample-bold:`Sample:` :ansible-rv-sample-value:`"terraform apply ..."`


      .. raw:: html

        </div>


  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="return-outputs"></div>

      .. _ansible_collections.cloud.terraform.terraform_module__return-outputs:

      .. rst-class:: ansible-option-title

      **outputs**

      .. raw:: html

        <a class="ansibleOptionLink" href="#return-outputs" title="Permalink to this return value"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`complex`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      A dictionary of all the TF outputs by their assigned name. Use \ :literal:`.outputs.MyOutputName.value`\  to access the value.


      .. rst-class:: ansible-option-line

      :ansible-option-returned-bold:`Returned:` on success

      .. rst-class:: ansible-option-line
      .. rst-class:: ansible-option-sample

      :ansible-option-sample-bold:`Sample:` :ansible-rv-sample-value:`"{\\"bukkit\_arn\\": {\\"sensitive\\": false, \\"type\\": \\"string\\", \\"value\\": \\"arn:aws:s3:::tf-test-bukkit\\"}"`


      .. raw:: html

        </div>

    
  * - .. raw:: html

        <div class="ansible-option-indent"></div><div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="return-outputs/sensitive"></div>

      .. _ansible_collections.cloud.terraform.terraform_module__return-outputs/sensitive:

      .. rst-class:: ansible-option-title

      **sensitive**

      .. raw:: html

        <a class="ansibleOptionLink" href="#return-outputs/sensitive" title="Permalink to this return value"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`boolean`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-indent-desc"></div><div class="ansible-option-cell">

      Whether Terraform has marked this value as sensitive


      .. rst-class:: ansible-option-line

      :ansible-option-returned-bold:`Returned:` always


      .. raw:: html

        </div>


  * - .. raw:: html

        <div class="ansible-option-indent"></div><div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="return-outputs/type"></div>

      .. _ansible_collections.cloud.terraform.terraform_module__return-outputs/type:

      .. rst-class:: ansible-option-title

      **type**

      .. raw:: html

        <a class="ansibleOptionLink" href="#return-outputs/type" title="Permalink to this return value"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`string`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-indent-desc"></div><div class="ansible-option-cell">

      The type of the value (string, int, etc)


      .. rst-class:: ansible-option-line

      :ansible-option-returned-bold:`Returned:` always


      .. raw:: html

        </div>


  * - .. raw:: html

        <div class="ansible-option-indent"></div><div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="return-outputs/value"></div>

      .. _ansible_collections.cloud.terraform.terraform_module__return-outputs/value:

      .. rst-class:: ansible-option-title

      **value**

      .. raw:: html

        <a class="ansibleOptionLink" href="#return-outputs/value" title="Permalink to this return value"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`string`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-indent-desc"></div><div class="ansible-option-cell">

      The value of the output as interpolated by Terraform


      .. rst-class:: ansible-option-line

      :ansible-option-returned-bold:`Returned:` always


      .. raw:: html

        </div>



  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="return-stdout"></div>

      .. _ansible_collections.cloud.terraform.terraform_module__return-stdout:

      .. rst-class:: ansible-option-title

      **stdout**

      .. raw:: html

        <a class="ansibleOptionLink" href="#return-stdout" title="Permalink to this return value"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`string`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Full \ :literal:`terraform`\  command stdout, in case you want to display it or examine the event log


      .. rst-class:: ansible-option-line

      :ansible-option-returned-bold:`Returned:` always

      .. rst-class:: ansible-option-line
      .. rst-class:: ansible-option-sample

      :ansible-option-sample-bold:`Sample:` :ansible-rv-sample-value:`""`


      .. raw:: html

        </div>



..  Status (Presently only deprecated)


.. Authors

Authors
~~~~~~~

- Ryan Scott Brown (@ryansb)



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

