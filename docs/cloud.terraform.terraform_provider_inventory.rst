.. _cloud.terraform.terraform_provider_inventory:


**********************************
cloud.terraform.terraform_provider
**********************************

**Builds an inventory from Terraform state file.**


Version added: 1.1.0

.. contents::
   :local:
   :depth: 1


Synopsis
--------
- Builds an inventory from specified state file.
- To read state file command "Terraform show" is used, thus requiring initialized working directory.
- Does not support caching.




Parameters
----------

.. raw:: html

    <table  border=0 cellpadding=0 class="documentation-table">
        <tr>
            <th colspan="1">Parameter</th>
            <th>Choices/<font color="blue">Defaults</font></th>
                <th>Configuration</th>
            <th width="100%">Comments</th>
        </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>binary_path</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">path</span>
                    </div>
                    <div style="font-style: italic; font-size: small; color: darkgreen">added in 1.1.0</div>
                </td>
                <td>
                </td>
                    <td>
                    </td>
                <td>
                        <div>The path of a terraform binary to use.</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>plugin</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                         / <span style="color: red">required</span>
                    </div>
                    <div style="font-style: italic; font-size: small; color: darkgreen">added in 1.1.0</div>
                </td>
                <td>
                        <ul style="margin: 0; padding: 0"><b>Choices:</b>
                                    <li>cloud.terraform.terraform_provider</li>
                        </ul>
                </td>
                    <td>
                    </td>
                <td>
                        <div>The name of the Inventory Plugin.</div>
                        <div>This should always be <code>cloud.terraform.terraform_provider</code>.</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>project_path</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">raw</span>
                    </div>
                    <div style="font-style: italic; font-size: small; color: darkgreen">added in 1.1.0</div>
                </td>
                <td>
                </td>
                    <td>
                    </td>
                <td>
                        <div>The path to the initialized Terraform directory with the .tfstate file.</div>
                        <div>If <em>state_file</em> is not specified, Terraform will attempt to automatically find the state file in <em>project_path</em> for use as inventory source.</div>
                        <div>If <em>state_file</em> and <em>project_path</em> are not specified, Terraform will attempt to automatically find the state file in the current working directory.</div>
                        <div>Accepts a string or a list of paths for use with multiple Terraform projects.</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>search_child_modules</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">boolean</span>
                    </div>
                    <div style="font-style: italic; font-size: small; color: darkgreen">added in 1.2.0</div>
                </td>
                <td>
                        <ul style="margin: 0; padding: 0"><b>Choices:</b>
                                    <li><div style="color: blue"><b>no</b>&nbsp;&larr;</div></li>
                                    <li>yes</li>
                        </ul>
                </td>
                    <td>
                    </td>
                <td>
                        <div>Whether to include ansible_host and ansible_group resources from Terraform child modules.</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>state_file</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">path</span>
                    </div>
                    <div style="font-style: italic; font-size: small; color: darkgreen">added in 1.1.0</div>
                </td>
                <td>
                </td>
                    <td>
                    </td>
                <td>
                        <div>Path to an existing Terraform state file to be used as an inventory source.</div>
                        <div>If <em>state_file</em> is not specified, Terraform will attempt to automatically find the state file in <em>project_path</em> for use as inventory source.</div>
                        <div>If <em>state_file</em> and <em>project_path</em> are not specified, Terraform will attempt to automatically find the state file in the current working directory</div>
                </td>
            </tr>
    </table>
    <br/>




Examples
--------

.. code-block:: yaml

    - name: Create an inventory from state file in current directory
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

    - name: Create an inventory from state file in provided directory
      plugin: cloud.terraform.terraform_provider
      project_path: some/project/path

    - name: Create an inventory from state file in multiple provided directories
      plugin: cloud.terraform.terraform_provider
      project_path:
        - some/project/path
        - some/other/project/path

    - name: Create an inventory from provided state file
      plugin: cloud.terraform.terraform_provider
      state_file: some/state/file/path

    - name: Create an inventory from state file in provided project directory
      plugin: cloud.terraform.terraform_provider
      project_path: some/project/path
      state_file: mycustomstate.tfstate




Status
------


Authors
~~~~~~~

- Polona Mihalič (@PolonaM)


.. hint::
    Configuration entries for each entry type have a low to high priority order. For example, a variable that is lower in the list will override a variable that is higher up.
