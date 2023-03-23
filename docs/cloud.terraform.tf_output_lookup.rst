.. _cloud.terraform.tf_output_lookup:


*************************
cloud.terraform.tf_output
*************************

**Reads state file outputs.**


Version added: 1.0.0

.. contents::
   :local:
   :depth: 1


Synopsis
--------
- This lookup returns all outputs or selected output in state file.




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
                    <b>_terms</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                    <td>
                    </td>
                <td>
                        <div>Name(s) of the output(s) to return.</div>
                        <div>If value is not set, all outputs will be returned in a dictionary.</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>binary_path</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">path</span>
                    </div>
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
                    <b>project_path</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">path</span>
                    </div>
                </td>
                <td>
                </td>
                    <td>
                    </td>
                <td>
                        <div>The path to the root of the Terraform directory with the terraform.tfstate file.</div>
                        <div>If <em>state_file</em> and <em>project_path</em> are not specified, the <code>terraform.tfstate</code> file in the current working directory will be used.</div>
                        <div>The <code>TF_DATA_DIR</code> environment variable is respected.</div>
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
                </td>
                <td>
                </td>
                    <td>
                    </td>
                <td>
                        <div>The path to an existing Terraform state file whose outputs will be listed.</div>
                        <div>If <em>state_file</em> and <em>project_path</em> are not specified, the <code>terraform.tfstate</code> file in the current working directory will be used.</div>
                        <div>The <code>TF_DATA_DIR</code> environment variable is respected.</div>
                </td>
            </tr>
    </table>
    <br/>




Examples
--------

.. code-block:: yaml

    - name: get selected output from terraform.tfstate
      ansible.builtin.debug:
        msg: "{{ lookup('cloud.terraform.tf_output', 'my_output1', project_path='path/to/project/dir/') }}"

    - name: get all outputs from custom state file
      ansible.builtin.debug:
        msg: "{{ lookup('cloud.terraform.tf_output', state_file='path/to/custom/state/file') }}"

    - name: get all outputs from terraform.tfstate in cwd
      ansible.builtin.debug:
        msg: "{{ lookup('cloud.terraform.tf_output') }}"



Return Values
-------------
Common return values are documented `here <https://docs.ansible.com/ansible/latest/reference_appendices/common_return_values.html#common-return-values>`_, the following are the fields unique to this lookup:

.. raw:: html

    <table border=0 cellpadding=0 class="documentation-table">
        <tr>
            <th colspan="1">Key</th>
            <th>Returned</th>
            <th width="100%">Description</th>
        </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="return-"></div>
                    <b>_outputs</b>
                    <a class="ansibleOptionLink" href="#return-" title="Permalink to this return value"></a>
                    <div style="font-size: small">
                      <span style="color: purple">list</span>
                       / <span style="color: purple">elements=dictionary</span>
                    </div>
                </td>
                <td>when _terms is not specified</td>
                <td>
                            <div>A list of dict that contains all outputs.</div>
                    <br/>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="return-"></div>
                    <b>_value</b>
                    <a class="ansibleOptionLink" href="#return-" title="Permalink to this return value"></a>
                    <div style="font-size: small">
                      <span style="color: purple">list</span>
                       / <span style="color: purple">elements=string</span>
                    </div>
                </td>
                <td>when name(s) of the output(s) is specified</td>
                <td>
                            <div>A list of selected output&#x27;s value.</div>
                    <br/>
                </td>
            </tr>
    </table>
    <br/><br/>


Status
------


Authors
~~~~~~~

- Polona Mihalič (@PolonaM)


.. hint::
    Configuration entries for each entry type have a low to high priority order. For example, a variable that is lower in the list will override a variable that is higher up.
