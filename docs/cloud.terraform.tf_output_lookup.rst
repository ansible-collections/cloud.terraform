
.. Document meta

:orphan:
:github_url: https://github.com/ansible-collections/cloud.terraform/edit/main/plugins/lookup/tf_output.py?description=%23%23%23%23%23%20SUMMARY%0A%3C!---%20Your%20description%20here%20--%3E%0A%0A%0A%23%23%23%23%23%20ISSUE%20TYPE%0A-%20Docs%20Pull%20Request%0A%0A%2Blabel:%20docsite_pr

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

.. _ansible_collections.cloud.terraform.tf_output_lookup:

.. Anchors: short name for ansible.builtin

.. Anchors: aliases



.. Title

cloud.terraform.tf_output lookup -- Read state file outputs.
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

.. Collection note

.. note::
    This lookup plugin is part of the `cloud.terraform collection <https://galaxy.ansible.com/cloud/terraform>`_ (version 1.0.0).

    To install it, use: :code:`ansible-galaxy collection install cloud.terraform`.

    To use it in a playbook, specify: :code:`cloud.terraform.tf_output`.

.. version_added

.. rst-class:: ansible-version-added

New in cloud.terraform 1.0.0

.. contents::
   :local:
   :depth: 1

.. Deprecated


Synopsis
--------

.. Description

- This lookup returns all outputs or selected output in state file.


.. Aliases


.. Requirements




.. Terms

Terms
-----

.. rst-class:: ansible-option-table

.. list-table::
  :width: 100%
  :widths: auto
  :header-rows: 1

  * - Parameter
    - Comments

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-_terms"></div>

      .. _ansible_collections.cloud.terraform.tf_output_lookup__parameter-_terms:

      .. rst-class:: ansible-option-title

      **Terms**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-_terms" title="Permalink to this option"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`string`




      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Name(s) of the output(s) to return.

      If value is not set, all outputs will be returned in a dictionary.


      .. raw:: html

        </div>





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

      .. _ansible_collections.cloud.terraform.tf_output_lookup__parameter-binary_path:

      .. rst-class:: ansible-option-title

      **binary_path**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-binary_path" title="Permalink to this option"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`path`




      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      The path of a terraform binary to use.


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-project_path"></div>

      .. _ansible_collections.cloud.terraform.tf_output_lookup__parameter-project_path:

      .. rst-class:: ansible-option-title

      **project_path**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-project_path" title="Permalink to this option"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`path`




      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      The path to the root of the Terraform directory with the terraform.tfstate file.

      If \ :emphasis:`state\_file`\  and \ :emphasis:`project\_path`\  are not specified, the \ :literal:`terraform.tfstate`\  file in the current working directory will be used.

      The \ :literal:`TF\_DATA\_DIR`\  environment variable is respected.


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-state_file"></div>

      .. _ansible_collections.cloud.terraform.tf_output_lookup__parameter-state_file:

      .. rst-class:: ansible-option-title

      **state_file**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-state_file" title="Permalink to this option"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`path`




      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Absolute path to an existing Terraform state file whose outputs will be listed.

      If \ :emphasis:`state\_file`\  and \ :emphasis:`project\_path`\  are not specified, the \ :literal:`terraform.tfstate`\  file in the current working directory will be used.

      The \ :literal:`TF\_DATA\_DIR`\  environment variable is respected.


      .. raw:: html

        </div>


.. Attributes


.. Notes


.. Seealso


.. Examples

Examples
--------

.. code-block:: yaml+jinja

    
    - name: get selected output from terraform.tfstate
      ansible.builtin.debug:
        msg: "{{ lookup('cloud.terraform.tf_output', 'my_output1', project_path='path/to/project/dir/') }}"

    - name: get all outputs from custom state file
      ansible.builtin.debug:
        msg: "{{ lookup('cloud.terraform.tf_output', state_file='path/to/custom/state/file') }}"

    - name: get all outputs from terraform.tfstate in cwd
      ansible.builtin.debug:
        msg: "{{ lookup('cloud.terraform.tf_output') }}"




.. Facts


.. Return values

Return Value
------------

.. rst-class:: ansible-option-table

.. list-table::
  :width: 100%
  :widths: auto
  :header-rows: 1

  * - Key
    - Description

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="return-_outputs"></div>

      .. _ansible_collections.cloud.terraform.tf_output_lookup__return-_outputs:

      .. rst-class:: ansible-option-title

      **_outputs**

      .. raw:: html

        <a class="ansibleOptionLink" href="#return-_outputs" title="Permalink to this return value"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`list` / :ansible-option-elements:`elements=dictionary`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      A list of dict that contains all outputs.


      .. rst-class:: ansible-option-line

      :ansible-option-returned-bold:`Returned:` when \_terms is not specified


      .. raw:: html

        </div>


  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="return-_value"></div>

      .. _ansible_collections.cloud.terraform.tf_output_lookup__return-_value:

      .. rst-class:: ansible-option-title

      **_value**

      .. raw:: html

        <a class="ansibleOptionLink" href="#return-_value" title="Permalink to this return value"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`list` / :ansible-option-elements:`elements=string`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      A list of selected output's value.


      .. rst-class:: ansible-option-line

      :ansible-option-returned-bold:`Returned:` when name(s) of the output(s) is specified


      .. raw:: html

        </div>



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

