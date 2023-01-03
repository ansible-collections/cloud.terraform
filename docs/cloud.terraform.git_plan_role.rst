
.. Document meta

:orphan:
:github_url: https://github.com/ansible-collections/cloud.terraform/edit/main/roles/git_plan/meta/argument_specs.yml?description=%23%23%23%23%23%20SUMMARY%0A%3C!---%20Your%20description%20here%20--%3E%0A%0A%0A%23%23%23%23%23%20ISSUE%20TYPE%0A-%20Docs%20Pull%20Request%0A%0A%2Blabel:%20docsite_pr

.. role:: ansible-option-type
.. role:: ansible-option-elements
.. role:: ansible-option-required
.. role:: ansible-option-versionadded
.. role:: ansible-option-aliases
.. role:: ansible-option-choices
.. role:: ansible-option-choices-default-mark
.. role:: ansible-option-default-bold

.. Anchors

.. _ansible_collections.cloud.terraform.git_plan_role:

.. Anchors: aliases


.. Title

cloud.terraform.git_plan role -- Clone a Git repository and apply a plan from it.
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

.. Collection note

.. note::
    This role is part of the `cloud.terraform collection <https://galaxy.ansible.com/cloud/terraform>`_ (version 1.0.0).

    To install it use: :code:`ansible-galaxy collection install cloud.terraform`.

    To use it in a playbook, specify: :code:`cloud.terraform.git_plan`.

.. contents::
   :local:
   :depth: 2


.. Entry point title

Entry point ``main`` -- Clone a Git repository and apply a plan from it.
------------------------------------------------------------------------

.. version_added


.. Deprecated


Synopsis
^^^^^^^^

.. Description

- Clone a Git repository and apply a plan from it.

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
        <div class="ansibleOptionAnchor" id="parameter-main--git_options"></div>

      .. _ansible_collections.cloud.terraform.git_plan_role__parameter-main__git_options:

      .. rst-class:: ansible-option-title

      **git_options**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-main--git_options" title="Permalink to this option"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`dictionary`

      :ansible-option-versionadded:`added in cloud.terraform 1.0.0`





      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Options to configure ansible.builtin.git.
          Names correspond to module arguments.
          See ansible.builtin.git documentation for details.
          


      .. raw:: html

        </div>
    
  * - .. raw:: html

        <div class="ansible-option-indent"></div><div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-main--git_options/accept_hostkey"></div>

      .. _ansible_collections.cloud.terraform.git_plan_role__parameter-main__git_options/accept_hostkey:

      .. rst-class:: ansible-option-title

      **accept_hostkey**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-main--git_options/accept_hostkey" title="Permalink to this option"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`boolean`

      :ansible-option-versionadded:`added in cloud.terraform 1.0.0`





      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-indent-desc"></div><div class="ansible-option-cell">


      .. rst-class:: ansible-option-line

      :ansible-option-choices:`Choices:`

      - :ansible-option-choices-entry:`false`
      - :ansible-option-choices-entry:`true`


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-indent"></div><div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-main--git_options/accept_newhostkey"></div>

      .. _ansible_collections.cloud.terraform.git_plan_role__parameter-main__git_options/accept_newhostkey:

      .. rst-class:: ansible-option-title

      **accept_newhostkey**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-main--git_options/accept_newhostkey" title="Permalink to this option"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`boolean`

      :ansible-option-versionadded:`added in cloud.terraform 1.0.0`





      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-indent-desc"></div><div class="ansible-option-cell">


      .. rst-class:: ansible-option-line

      :ansible-option-choices:`Choices:`

      - :ansible-option-choices-entry:`false`
      - :ansible-option-choices-entry:`true`


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-indent"></div><div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-main--git_options/depth"></div>

      .. _ansible_collections.cloud.terraform.git_plan_role__parameter-main__git_options/depth:

      .. rst-class:: ansible-option-title

      **depth**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-main--git_options/depth" title="Permalink to this option"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`integer`

      :ansible-option-versionadded:`added in cloud.terraform 1.0.0`





      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-indent-desc"></div><div class="ansible-option-cell">


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-indent"></div><div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-main--git_options/executable"></div>

      .. _ansible_collections.cloud.terraform.git_plan_role__parameter-main__git_options/executable:

      .. rst-class:: ansible-option-title

      **executable**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-main--git_options/executable" title="Permalink to this option"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`string`

      :ansible-option-versionadded:`added in cloud.terraform 1.0.0`





      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-indent-desc"></div><div class="ansible-option-cell">


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-indent"></div><div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-main--git_options/force"></div>

      .. _ansible_collections.cloud.terraform.git_plan_role__parameter-main__git_options/force:

      .. rst-class:: ansible-option-title

      **force**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-main--git_options/force" title="Permalink to this option"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`boolean`

      :ansible-option-versionadded:`added in cloud.terraform 1.0.0`





      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-indent-desc"></div><div class="ansible-option-cell">


      .. rst-class:: ansible-option-line

      :ansible-option-choices:`Choices:`

      - :ansible-option-choices-entry:`false`
      - :ansible-option-choices-entry:`true`


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-indent"></div><div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-main--git_options/gpg_whitelist"></div>

      .. _ansible_collections.cloud.terraform.git_plan_role__parameter-main__git_options/gpg_whitelist:

      .. rst-class:: ansible-option-title

      **gpg_whitelist**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-main--git_options/gpg_whitelist" title="Permalink to this option"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`list` / :ansible-option-elements:`elements=string`

      :ansible-option-versionadded:`added in cloud.terraform 1.0.0`





      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-indent-desc"></div><div class="ansible-option-cell">


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-indent"></div><div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-main--git_options/key_file"></div>

      .. _ansible_collections.cloud.terraform.git_plan_role__parameter-main__git_options/key_file:

      .. rst-class:: ansible-option-title

      **key_file**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-main--git_options/key_file" title="Permalink to this option"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`string`

      :ansible-option-versionadded:`added in cloud.terraform 1.0.0`





      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-indent-desc"></div><div class="ansible-option-cell">


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-indent"></div><div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-main--git_options/remote"></div>

      .. _ansible_collections.cloud.terraform.git_plan_role__parameter-main__git_options/remote:

      .. rst-class:: ansible-option-title

      **remote**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-main--git_options/remote" title="Permalink to this option"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`string`

      :ansible-option-versionadded:`added in cloud.terraform 1.0.0`





      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-indent-desc"></div><div class="ansible-option-cell">


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-indent"></div><div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-main--git_options/separate_git_dir"></div>

      .. _ansible_collections.cloud.terraform.git_plan_role__parameter-main__git_options/separate_git_dir:

      .. rst-class:: ansible-option-title

      **separate_git_dir**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-main--git_options/separate_git_dir" title="Permalink to this option"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`string`

      :ansible-option-versionadded:`added in cloud.terraform 1.0.0`





      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-indent-desc"></div><div class="ansible-option-cell">


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-indent"></div><div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-main--git_options/ssh_opts"></div>

      .. _ansible_collections.cloud.terraform.git_plan_role__parameter-main__git_options/ssh_opts:

      .. rst-class:: ansible-option-title

      **ssh_opts**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-main--git_options/ssh_opts" title="Permalink to this option"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`string`

      :ansible-option-versionadded:`added in cloud.terraform 1.0.0`





      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-indent-desc"></div><div class="ansible-option-cell">


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-indent"></div><div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-main--git_options/track_submodules"></div>

      .. _ansible_collections.cloud.terraform.git_plan_role__parameter-main__git_options/track_submodules:

      .. rst-class:: ansible-option-title

      **track_submodules**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-main--git_options/track_submodules" title="Permalink to this option"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`boolean`

      :ansible-option-versionadded:`added in cloud.terraform 1.0.0`





      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-indent-desc"></div><div class="ansible-option-cell">


      .. rst-class:: ansible-option-line

      :ansible-option-choices:`Choices:`

      - :ansible-option-choices-entry:`false`
      - :ansible-option-choices-entry:`true`


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-indent"></div><div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-main--git_options/verify_commit"></div>

      .. _ansible_collections.cloud.terraform.git_plan_role__parameter-main__git_options/verify_commit:

      .. rst-class:: ansible-option-title

      **verify_commit**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-main--git_options/verify_commit" title="Permalink to this option"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`boolean`

      :ansible-option-versionadded:`added in cloud.terraform 1.0.0`





      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-indent-desc"></div><div class="ansible-option-cell">


      .. rst-class:: ansible-option-line

      :ansible-option-choices:`Choices:`

      - :ansible-option-choices-entry:`false`
      - :ansible-option-choices-entry:`true`


      .. raw:: html

        </div>


  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-main--plan_file"></div>

      .. _ansible_collections.cloud.terraform.git_plan_role__parameter-main__plan_file:

      .. rst-class:: ansible-option-title

      **plan_file**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-main--plan_file" title="Permalink to this option"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`string` / :ansible-option-required:`required`

      :ansible-option-versionadded:`added in cloud.terraform 1.0.0`





      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      The plan file to use. This must exist.


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-main--repo_dir"></div>

      .. _ansible_collections.cloud.terraform.git_plan_role__parameter-main__repo_dir:

      .. rst-class:: ansible-option-title

      **repo_dir**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-main--repo_dir" title="Permalink to this option"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`string` / :ansible-option-required:`required`

      :ansible-option-versionadded:`added in cloud.terraform 1.0.0`





      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      The directory to clone the Git repository into.


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-main--repo_url"></div>

      .. _ansible_collections.cloud.terraform.git_plan_role__parameter-main__repo_url:

      .. rst-class:: ansible-option-title

      **repo_url**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-main--repo_url" title="Permalink to this option"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`string` / :ansible-option-required:`required`

      :ansible-option-versionadded:`added in cloud.terraform 1.0.0`





      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      The URL of the repository to clone.


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-main--terraform_options"></div>

      .. _ansible_collections.cloud.terraform.git_plan_role__parameter-main__terraform_options:

      .. rst-class:: ansible-option-title

      **terraform_options**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-main--terraform_options" title="Permalink to this option"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`string`




      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Options to configure terraform execution.


      .. raw:: html

        </div>
    
  * - .. raw:: html

        <div class="ansible-option-indent"></div><div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-main--terraform_options/binary_path"></div>

      .. _ansible_collections.cloud.terraform.git_plan_role__parameter-main__terraform_options/binary_path:

      .. rst-class:: ansible-option-title

      **binary_path**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-main--terraform_options/binary_path" title="Permalink to this option"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`string`

      :ansible-option-versionadded:`added in cloud.terraform 1.0.0`





      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-indent-desc"></div><div class="ansible-option-cell">


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-indent"></div><div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-main--terraform_options/force_init"></div>

      .. _ansible_collections.cloud.terraform.git_plan_role__parameter-main__terraform_options/force_init:

      .. rst-class:: ansible-option-title

      **force_init**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-main--terraform_options/force_init" title="Permalink to this option"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`boolean`

      :ansible-option-versionadded:`added in cloud.terraform 1.0.0`





      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-indent-desc"></div><div class="ansible-option-cell">


      .. rst-class:: ansible-option-line

      :ansible-option-choices:`Choices:`

      - :ansible-option-choices-entry:`false`
      - :ansible-option-choices-entry:`true`


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-indent"></div><div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-main--terraform_options/lock"></div>

      .. _ansible_collections.cloud.terraform.git_plan_role__parameter-main__terraform_options/lock:

      .. rst-class:: ansible-option-title

      **lock**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-main--terraform_options/lock" title="Permalink to this option"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`boolean`

      :ansible-option-versionadded:`added in cloud.terraform 1.0.0`





      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-indent-desc"></div><div class="ansible-option-cell">


      .. rst-class:: ansible-option-line

      :ansible-option-choices:`Choices:`

      - :ansible-option-choices-entry:`false`
      - :ansible-option-choices-entry:`true`


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-indent"></div><div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-main--terraform_options/lock_timeout"></div>

      .. _ansible_collections.cloud.terraform.git_plan_role__parameter-main__terraform_options/lock_timeout:

      .. rst-class:: ansible-option-title

      **lock_timeout**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-main--terraform_options/lock_timeout" title="Permalink to this option"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`integer`

      :ansible-option-versionadded:`added in cloud.terraform 1.0.0`





      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-indent-desc"></div><div class="ansible-option-cell">


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-indent"></div><div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-main--terraform_options/parallelism"></div>

      .. _ansible_collections.cloud.terraform.git_plan_role__parameter-main__terraform_options/parallelism:

      .. rst-class:: ansible-option-title

      **parallelism**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-main--terraform_options/parallelism" title="Permalink to this option"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`integer`

      :ansible-option-versionadded:`added in cloud.terraform 1.0.0`





      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-indent-desc"></div><div class="ansible-option-cell">


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-indent"></div><div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-main--terraform_options/plugin_paths"></div>

      .. _ansible_collections.cloud.terraform.git_plan_role__parameter-main__terraform_options/plugin_paths:

      .. rst-class:: ansible-option-title

      **plugin_paths**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-main--terraform_options/plugin_paths" title="Permalink to this option"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`list` / :ansible-option-elements:`elements=path`

      :ansible-option-versionadded:`added in cloud.terraform 1.0.0`





      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-indent-desc"></div><div class="ansible-option-cell">


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-indent"></div><div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-main--terraform_options/state_file"></div>

      .. _ansible_collections.cloud.terraform.git_plan_role__parameter-main__terraform_options/state_file:

      .. rst-class:: ansible-option-title

      **state_file**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-main--terraform_options/state_file" title="Permalink to this option"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`string`

      :ansible-option-versionadded:`added in cloud.terraform 1.0.0`





      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-indent-desc"></div><div class="ansible-option-cell">

      An optional state file to use, overriding the default.


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-indent"></div><div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-main--terraform_options/workspace"></div>

      .. _ansible_collections.cloud.terraform.git_plan_role__parameter-main__terraform_options/workspace:

      .. rst-class:: ansible-option-title

      **workspace**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-main--terraform_options/workspace" title="Permalink to this option"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`string`

      :ansible-option-versionadded:`added in cloud.terraform 1.0.0`





      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-indent-desc"></div><div class="ansible-option-cell">


      .. raw:: html

        </div>


  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-main--version"></div>

      .. _ansible_collections.cloud.terraform.git_plan_role__parameter-main__version:

      .. rst-class:: ansible-option-title

      **version**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-main--version" title="Permalink to this option"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`string`

      :ansible-option-versionadded:`added in cloud.terraform 1.0.0`





      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      The ref of the repository to use. Defaults to the remote HEAD.


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

