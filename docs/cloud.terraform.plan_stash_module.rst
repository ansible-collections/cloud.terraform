.. _cloud.terraform.plan_stash_module:


**************************
cloud.terraform.plan_stash
**************************

**Handle the base64 encoding or decoding of a terraform plan file**


Version added: 2.1.0

.. contents::
   :local:
   :depth: 1


Synopsis
--------
- This module performs base64-encoding of a terraform plan file and saves it into playbook execution stats similar to :ref:`ansible.builtin.set_stats <ansible.builtin.set_stats_module>` module.
- The module also performs base64-decoding of a terraform plan file from a variable defined into ansible facts and writes them into a file specified by the user.




Parameters
----------

.. raw:: html

    <table  border=0 cellpadding=0 class="documentation-table">
        <tr>
            <th colspan="1">Parameter</th>
            <th>Choices/<font color="blue">Defaults</font></th>
            <th width="100%">Comments</th>
        </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>binary_data</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">raw</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>When O(state=load), this parameter defines the base64-encoded data of the terraform plan file.</div>
                        <div>Mutually exclusive with V(var_name).</div>
                        <div>Ignored when O(state=stash).</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>path</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">path</span>
                         / <span style="color: red">required</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>The path to the terraform plan file.</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>per_host</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">boolean</span>
                    </div>
                </td>
                <td>
                        <ul style="margin: 0; padding: 0"><b>Choices:</b>
                                    <li><div style="color: blue"><b>no</b>&nbsp;&larr;</div></li>
                                    <li>yes</li>
                        </ul>
                </td>
                <td>
                        <div>Whether the stats are per host or for all hosts in the run.</div>
                        <div>Ignored when O(state=load).</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>state</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                        <ul style="margin: 0; padding: 0"><b>Choices:</b>
                                    <li><div style="color: blue"><b>stash</b>&nbsp;&larr;</div></li>
                                    <li>load</li>
                        </ul>
                </td>
                <td>
                        <div>O(state=stash): base64-encodes the terraform plan file and saves it into ansible stats like using the <span class='module'>ansible.builtin.set_stats</span> module.</div>
                        <div>O(state=load): base64-decodes data from variable specified in O(var_name) and writes them into terraform plan file.</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>var_name</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>When O(state=stash), this parameter defines the variable name to be set into stats.</div>
                        <div>When O(state=load), this parameter defines the variable from ansible facts containing the base64-encoded data of the terraform plan file.</div>
                        <div>Variables must start with a letter or underscore character, and contain only letters, numbers and underscores.</div>
                        <div>The module will use V(terraform_plan) as default variable name if not specified.</div>
                </td>
            </tr>
    </table>
    <br/>


Notes
-----

.. note::
   - For security reasons, this module should be used with *no_log=true* and *register* functionalities as the plan file can contain unencrypted secrets.



Examples
--------

.. code-block:: yaml

    # Encode terraform plan file into default variable 'terraform_plan'
    - name: Encode a terraform plan file into terraform_plan variable
      cloud.terraform.plan_stash:
        path: /path/to/terraform_plan_file
        state: stash
      no_log: true

    # Encode terraform plan file into variable 'stashed_plan'
    - name: Encode a terraform plan file into terraform_plan variable
      cloud.terraform.plan_stash:
        path: /path/to/terraform_plan_file
        var_name: stashed_plan
        state: stash
      no_log: true

    # Load terraform plan file from variable 'stashed_plan'
    - name: Load a terraform plan file data from variable 'stashed_plan' into file 'tfplan'
      cloud.terraform.plan_stash:
        path: tfplan
        var_name: stashed_plan
        state: load
      no_log: true

    # Load terraform plan file from binary data
    - name: Load a terraform plan file data from binary data
      cloud.terraform.plan_stash:
        path: tfplan
        binary_data: "{{ terraform_binary_data }}"
        state: load
      no_log: true




Status
------


Authors
~~~~~~~

- Aubin Bikouo (@abikouo)
