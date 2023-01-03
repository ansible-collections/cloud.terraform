
.. Document meta

:orphan:
:github_url: https://github.com/ansible-collections/cloud.terraform/edit/main/plugins/modules/terraform_output.py?description=%23%23%23%23%23%20SUMMARY%0A%3C!---%20Your%20description%20here%20--%3E%0A%0A%0A%23%23%23%23%23%20ISSUE%20TYPE%0A-%20Docs%20Pull%20Request%0A%0A%2Blabel:%20docsite_pr

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

.. _ansible_collections.cloud.terraform.terraform_output_module:

.. Anchors: short name for ansible.builtin

.. Anchors: aliases



.. Title

cloud.terraform.terraform_output module -- Returns Terraform module outputs.
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

.. Collection note

.. note::
    This module is part of the `cloud.terraform collection <https://galaxy.ansible.com/cloud/terraform>`_ (version 1.0.0).

    To install it, use: :code:`ansible-galaxy collection install cloud.terraform`.
    You need further requirements to be able to use this module,
    see :ref:`Requirements <ansible_collections.cloud.terraform.terraform_output_module_requirements>` for details.

    To use it in a playbook, specify: :code:`cloud.terraform.terraform_output`.

.. version_added


.. contents::
   :local:
   :depth: 1

.. Deprecated


Synopsis
--------

.. Description

- Returns Terraform module outputs.


.. Aliases


.. Requirements

.. _ansible_collections.cloud.terraform.terraform_output_module_requirements:

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
        <div class="ansibleOptionAnchor" id="parameter-binary_path"></div>

      .. _ansible_collections.cloud.terraform.terraform_output_module__parameter-binary_path:

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
        <div class="ansibleOptionAnchor" id="parameter-format"></div>

      .. _ansible_collections.cloud.terraform.terraform_output_module__parameter-format:

      .. rst-class:: ansible-option-title

      **format**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-format" title="Permalink to this option"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`string`

      :ansible-option-versionadded:`added in cloud.terraform 1.0.0`


      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      A flag to specify the output format. Defaults to \ :literal:`json`\ .

      \ :emphasis:`name`\  must be provided when using \ :literal:`raw`\  option.


      .. rst-class:: ansible-option-line

      :ansible-option-choices:`Choices:`

      - :ansible-option-choices-entry-default:`"json"` :ansible-option-choices-default-mark:`← (default)`
      - :ansible-option-choices-entry:`"raw"`


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-name"></div>

      .. _ansible_collections.cloud.terraform.terraform_output_module__parameter-name:

      .. rst-class:: ansible-option-title

      **name**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-name" title="Permalink to this option"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`string`

      :ansible-option-versionadded:`added in cloud.terraform 1.0.0`


      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Name of an individual output in the state file to list.


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-project_path"></div>

      .. _ansible_collections.cloud.terraform.terraform_output_module__parameter-project_path:

      .. rst-class:: ansible-option-title

      **project_path**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-project_path" title="Permalink to this option"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`path`

      :ansible-option-versionadded:`added in cloud.terraform 1.0.0`


      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      The path to the root of the Terraform directory with the .tfstate file.


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-state_file"></div>

      .. _ansible_collections.cloud.terraform.terraform_output_module__parameter-state_file:

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

      Absolute path to an existing Terraform state file whose outputs will be listed.

      If this is not specified, the default \ :literal:`terraform.tfstate`\  in the directory \ :emphasis:`project\_path`\  will be used.


      .. raw:: html

        </div>


.. Attributes


.. Notes


.. Seealso


.. Examples

Examples
--------

.. code-block:: yaml+jinja

    
    - name: List outputs from terraform.tfstate in project_dir
      cloud.terraform.terraform_output:
        project_path: project_dir

    - name: List outputs from selected state file in project_dir
      cloud.terraform.terraform_output:
        state_file: state_file

    - name: List outputs from terraform.tfstate in project_dir, use different Terraform version
      cloud.terraform.terraform_output:
        project_path: project_dir
        binary_path: terraform_binary

    - name: List value of an individual output from terraform.tfstate in project_dir
      cloud.terraform.terraform_output:
        project_path: project_dir
        name: individual_output

    - name: List value of an individual output in raw format
      cloud.terraform.terraform_output:
        project_path: project_dir
        name: individual_output
        format: raw




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
        <div class="ansibleOptionAnchor" id="return-outputs"></div>

      .. _ansible_collections.cloud.terraform.terraform_output_module__return-outputs:

      .. rst-class:: ansible-option-title

      **outputs**

      .. raw:: html

        <a class="ansibleOptionLink" href="#return-outputs" title="Permalink to this return value"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`dictionary`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      A dictionary of all the TF outputs by their assigned name. Use \ :literal:`.outputs.MyOutputName.value`\  to access the value.


      .. rst-class:: ansible-option-line

      :ansible-option-returned-bold:`Returned:` when name is not specified

      .. rst-class:: ansible-option-line
      .. rst-class:: ansible-option-sample

      :ansible-option-sample-bold:`Sample:` :ansible-rv-sample-value:`"{\\"bukkit\_arn\\": {\\"sensitive\\": false, \\"type\\": \\"string\\", \\"value\\": \\"arn:aws:s3:::tf-test-bukkit\\"}"`


      .. raw:: html

        </div>

    
  * - .. raw:: html

        <div class="ansible-option-indent"></div><div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="return-outputs/sensitive"></div>

      .. _ansible_collections.cloud.terraform.terraform_output_module__return-outputs/sensitive:

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

      .. _ansible_collections.cloud.terraform.terraform_output_module__return-outputs/type:

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

      .. _ansible_collections.cloud.terraform.terraform_output_module__return-outputs/value:

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
        <div class="ansibleOptionAnchor" id="return-value"></div>

      .. _ansible_collections.cloud.terraform.terraform_output_module__return-value:

      .. rst-class:: ansible-option-title

      **value**

      .. raw:: html

        <a class="ansibleOptionLink" href="#return-value" title="Permalink to this return value"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`string`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      A single value requested by the module using the "name" parameter


      .. rst-class:: ansible-option-line

      :ansible-option-returned-bold:`Returned:` when name is specified

      .. rst-class:: ansible-option-line
      .. rst-class:: ansible-option-sample

      :ansible-option-sample-bold:`Sample:` :ansible-rv-sample-value:`"myvalue"`


      .. raw:: html

        </div>



..  Status (Presently only deprecated)


.. Authors

Authors
~~~~~~~

- Polona Mihalič (@PolonaM)



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

