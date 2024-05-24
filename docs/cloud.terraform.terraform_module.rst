.. _cloud.terraform.terraform_module:


*************************
cloud.terraform.terraform
*************************

**Manages a Terraform deployment (and plans)**



.. contents::
   :local:
   :depth: 1


Synopsis
--------
- Provides support for deploying resources with Terraform and pulling resource information back into Ansible.



Requirements
------------
The below requirements are needed on the host that executes this module.

- terraform


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
                    <b>backend_config</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">dictionary</span>
                    </div>
                    <div style="font-style: italic; font-size: small; color: darkgreen">added in 1.0.0</div>
                </td>
                <td>
                </td>
                <td>
                        <div>A group of key-values to provide at init stage to the -backend-config parameter.</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>backend_config_files</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">list</span>
                         / <span style="color: purple">elements=path</span>
                    </div>
                    <div style="font-style: italic; font-size: small; color: darkgreen">added in 1.0.0</div>
                </td>
                <td>
                </td>
                <td>
                        <div>The path to a configuration file to provide at init state to the -backend-config parameter. This can accept a list of paths to multiple configuration files.</div>
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
                    <div style="font-style: italic; font-size: small; color: darkgreen">added in 1.0.0</div>
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
                    <b>check_destroy</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">boolean</span>
                    </div>
                    <div style="font-style: italic; font-size: small; color: darkgreen">added in 1.0.0</div>
                </td>
                <td>
                        <ul style="margin: 0; padding: 0"><b>Choices:</b>
                                    <li><div style="color: blue"><b>no</b>&nbsp;&larr;</div></li>
                                    <li>yes</li>
                        </ul>
                </td>
                <td>
                        <div>Apply only when no resources are destroyed. Note that this only prevents &quot;destroy&quot; actions, but not &quot;destroy and re-create&quot; actions. This option is ignored when <em>state=absent</em>.</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>complex_vars</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">boolean</span>
                    </div>
                    <div style="font-style: italic; font-size: small; color: darkgreen">added in 1.0.0</div>
                </td>
                <td>
                        <ul style="margin: 0; padding: 0"><b>Choices:</b>
                                    <li><div style="color: blue"><b>no</b>&nbsp;&larr;</div></li>
                                    <li>yes</li>
                        </ul>
                </td>
                <td>
                        <div>Enable/disable capability to handle complex variable structures for <code>terraform</code>.</div>
                        <div>If <code>true</code> the <em>variables</em> also accepts dictionaries, lists, and booleans to be passed to <code>terraform</code>. Strings that are passed are correctly quoted.</div>
                        <div>When disabled, supports only simple variables (strings, integers, and floats), and passes them on unquoted.</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>force_init</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">boolean</span>
                    </div>
                    <div style="font-style: italic; font-size: small; color: darkgreen">added in 1.0.0</div>
                </td>
                <td>
                        <ul style="margin: 0; padding: 0"><b>Choices:</b>
                                    <li><div style="color: blue"><b>no</b>&nbsp;&larr;</div></li>
                                    <li>yes</li>
                        </ul>
                </td>
                <td>
                        <div>To avoid duplicating infra, if a state file can&#x27;t be found this will force a <code>terraform init</code>. Generally, this should be turned off unless you intend to provision an entirely new Terraform deployment.</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>init_reconfigure</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">boolean</span>
                    </div>
                    <div style="font-style: italic; font-size: small; color: darkgreen">added in 1.0.0</div>
                </td>
                <td>
                        <ul style="margin: 0; padding: 0"><b>Choices:</b>
                                    <li><div style="color: blue"><b>no</b>&nbsp;&larr;</div></li>
                                    <li>yes</li>
                        </ul>
                </td>
                <td>
                        <div>Forces backend reconfiguration during init.</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>lock</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">boolean</span>
                    </div>
                    <div style="font-style: italic; font-size: small; color: darkgreen">added in 1.0.0</div>
                </td>
                <td>
                        <ul style="margin: 0; padding: 0"><b>Choices:</b>
                                    <li>no</li>
                                    <li><div style="color: blue"><b>yes</b>&nbsp;&larr;</div></li>
                        </ul>
                </td>
                <td>
                        <div>Enable statefile locking, if you use a service that accepts locks (such as S3+DynamoDB) to store your statefile.</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>lock_timeout</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">integer</span>
                    </div>
                    <div style="font-style: italic; font-size: small; color: darkgreen">added in 1.0.0</div>
                </td>
                <td>
                </td>
                <td>
                        <div>How long to maintain the lock on the statefile, if you use a service that accepts locks (such as S3+DynamoDB).</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>overwrite_init</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">boolean</span>
                    </div>
                    <div style="font-style: italic; font-size: small; color: darkgreen">added in 1.0.0</div>
                </td>
                <td>
                        <ul style="margin: 0; padding: 0"><b>Choices:</b>
                                    <li>no</li>
                                    <li><div style="color: blue"><b>yes</b>&nbsp;&larr;</div></li>
                        </ul>
                </td>
                <td>
                        <div>Run init even if <code>.terraform/terraform.tfstate</code> already exists in <em>project_path</em>.</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>parallelism</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">integer</span>
                    </div>
                    <div style="font-style: italic; font-size: small; color: darkgreen">added in 1.0.0</div>
                </td>
                <td>
                </td>
                <td>
                        <div>Restrict concurrent operations when Terraform applies the plan.</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>plan_file</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">path</span>
                    </div>
                    <div style="font-style: italic; font-size: small; color: darkgreen">added in 1.0.0</div>
                </td>
                <td>
                </td>
                <td>
                        <div>The path to a Terraform plan file to apply or generate.</div>
                        <div>When &#x27;check_mode&#x27; is set to <code>True</code> or <em>state=planned</em>, a Terraform plan file will be generated and saved into the specified location.</div>
                        <div>When &#x27;check_mode&#x27; is set to <em>False</em> and <em>state</em> is set to either <code>present</code> or <code>absent</code>, The existing Terraform plan file will be applied.</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>plugin_paths</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">list</span>
                         / <span style="color: purple">elements=path</span>
                    </div>
                    <div style="font-style: italic; font-size: small; color: darkgreen">added in 1.0.0</div>
                </td>
                <td>
                </td>
                <td>
                        <div>List of paths containing Terraform plugin executable files.</div>
                        <div>Plugin executables can be downloaded from <a href='https://releases.hashicorp.com/'>https://releases.hashicorp.com/</a>.</div>
                        <div>When set, the plugin discovery and auto-download behavior of Terraform is disabled.</div>
                        <div>The directory structure in the plugin path can be tricky. The Terraform docs <a href='https://learn.hashicorp.com/tutorials/terraform/automate-terraform#pre-installed-plugins'>https://learn.hashicorp.com/tutorials/terraform/automate-terraform#pre-installed-plugins</a> show a simple directory of files, but actually, the directory structure has to follow the same structure you would see if Terraform auto-downloaded the plugins. See the examples below for a tree output of an example plugin directory.</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>project_path</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">path</span>
                         / <span style="color: red">required</span>
                    </div>
                    <div style="font-style: italic; font-size: small; color: darkgreen">added in 1.0.0</div>
                </td>
                <td>
                </td>
                <td>
                        <div>The path to the root of the Terraform directory with the vars.tf/main.tf/etc to use.</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>provider_upgrade</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">boolean</span>
                    </div>
                    <div style="font-style: italic; font-size: small; color: darkgreen">added in 1.0.0</div>
                </td>
                <td>
                        <ul style="margin: 0; padding: 0"><b>Choices:</b>
                                    <li><div style="color: blue"><b>no</b>&nbsp;&larr;</div></li>
                                    <li>yes</li>
                        </ul>
                </td>
                <td>
                        <div>Allows Terraform init to upgrade providers to versions specified in the project&#x27;s version constraints.</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>purge_workspace</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">boolean</span>
                    </div>
                    <div style="font-style: italic; font-size: small; color: darkgreen">added in 1.0.0</div>
                </td>
                <td>
                        <ul style="margin: 0; padding: 0"><b>Choices:</b>
                                    <li><div style="color: blue"><b>no</b>&nbsp;&larr;</div></li>
                                    <li>yes</li>
                        </ul>
                </td>
                <td>
                        <div>Only works with state = absent</div>
                        <div>If true, the workspace will be deleted after the &quot;terraform destroy&quot; action.</div>
                        <div>The &#x27;default&#x27; workspace will not be deleted.</div>
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
                    <div style="font-style: italic; font-size: small; color: darkgreen">added in 1.0.0</div>
                </td>
                <td>
                        <ul style="margin: 0; padding: 0"><b>Choices:</b>
                                    <li><div style="color: blue"><b>present</b>&nbsp;&larr;</div></li>
                                    <li>absent</li>
                                    <li>planned</li>
                        </ul>
                </td>
                <td>
                        <div>Goal state of given stage/project.</div>
                        <div>Option `planned` is deprecated. Its function is equivalent to running the module in check mode.</div>
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
                    <div style="font-style: italic; font-size: small; color: darkgreen">added in 1.0.0</div>
                </td>
                <td>
                </td>
                <td>
                        <div>The path to an existing Terraform state file to use when building plan. If this is not specified, the default <code>terraform.tfstate</code> will be used.</div>
                        <div>This option is ignored when plan is specified.</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>targets</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">list</span>
                         / <span style="color: purple">elements=string</span>
                    </div>
                    <div style="font-style: italic; font-size: small; color: darkgreen">added in 1.0.0</div>
                </td>
                <td>
                        <b>Default:</b><br/><div style="color: blue">[]</div>
                </td>
                <td>
                        <div>A list of specific resources to target in this plan/application. The resources selected here will also auto-include any dependencies.</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>variables</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">dictionary</span>
                    </div>
                    <div style="font-style: italic; font-size: small; color: darkgreen">added in 1.0.0</div>
                </td>
                <td>
                </td>
                <td>
                        <div>A group of key-values pairs to override template variables or those in variables files. By default, only string and number values are allowed, which are passed on unquoted.</div>
                        <div>Support complex variable structures (lists, dictionaries, numbers, and booleans) to reflect terraform variable syntax when <em>complex_vars=true</em>.</div>
                        <div>Ansible integers or floats are mapped to terraform numbers.</div>
                        <div>Ansible strings are mapped to terraform strings.</div>
                        <div>Ansible dictionaries are mapped to terraform objects.</div>
                        <div>Ansible lists are mapped to terraform lists.</div>
                        <div>Ansible booleans are mapped to terraform booleans.</div>
                        <div><b>Note</b> passwords passed as variables will be visible in the log output. Make sure to use <em>no_log=true</em> in production!</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>variables_files</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">list</span>
                         / <span style="color: purple">elements=path</span>
                    </div>
                    <div style="font-style: italic; font-size: small; color: darkgreen">added in 1.0.0</div>
                </td>
                <td>
                </td>
                <td>
                        <div>The path to a variables file for Terraform to fill into the TF configurations. This can accept a list of paths to multiple variables files.</div>
                        <div>Up until Ansible 2.9, this option was usable as <em>variables_file</em>.</div>
                        <div style="font-size: small; color: darkgreen"><br/>aliases: variables_file</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>workspace</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                    <div style="font-style: italic; font-size: small; color: darkgreen">added in 1.0.0</div>
                </td>
                <td>
                        <b>Default:</b><br/><div style="color: blue">"default"</div>
                </td>
                <td>
                        <div>The terraform workspace to work with.</div>
                </td>
            </tr>
    </table>
    <br/>


Notes
-----

.. note::
   - To just run a ``terraform plan``, use check mode.



Examples
--------

.. code-block:: yaml

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



Return Values
-------------
Common return values are documented `here <https://docs.ansible.com/ansible/latest/reference_appendices/common_return_values.html#common-return-values>`_, the following are the fields unique to this module:

.. raw:: html

    <table border=0 cellpadding=0 class="documentation-table">
        <tr>
            <th colspan="2">Key</th>
            <th>Returned</th>
            <th width="100%">Description</th>
        </tr>
            <tr>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="return-"></div>
                    <b>command</b>
                    <a class="ansibleOptionLink" href="#return-" title="Permalink to this return value"></a>
                    <div style="font-size: small">
                      <span style="color: purple">string</span>
                    </div>
                </td>
                <td>always</td>
                <td>
                            <div>Full <code>terraform</code> command built by this module, in case you want to re-run the command outside the module or debug a problem.</div>
                    <br/>
                        <div style="font-size: smaller"><b>Sample:</b></div>
                        <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">terraform apply ...</div>
                </td>
            </tr>
            <tr>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="return-"></div>
                    <b>outputs</b>
                    <a class="ansibleOptionLink" href="#return-" title="Permalink to this return value"></a>
                    <div style="font-size: small">
                      <span style="color: purple">complex</span>
                    </div>
                </td>
                <td>on success</td>
                <td>
                            <div>A dictionary of all the TF outputs by their assigned name. Use <code>.outputs.MyOutputName.value</code> to access the value.</div>
                    <br/>
                        <div style="font-size: smaller"><b>Sample:</b></div>
                        <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">{&quot;bukkit_arn&quot;: {&quot;sensitive&quot;: false, &quot;type&quot;: &quot;string&quot;, &quot;value&quot;: &quot;arn:aws:s3:::tf-test-bukkit&quot;}</div>
                </td>
            </tr>
                                <tr>
                    <td class="elbow-placeholder">&nbsp;</td>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="return-"></div>
                    <b>sensitive</b>
                    <a class="ansibleOptionLink" href="#return-" title="Permalink to this return value"></a>
                    <div style="font-size: small">
                      <span style="color: purple">boolean</span>
                    </div>
                </td>
                <td>always</td>
                <td>
                            <div>Whether Terraform has marked this value as sensitive</div>
                    <br/>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder">&nbsp;</td>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="return-"></div>
                    <b>type</b>
                    <a class="ansibleOptionLink" href="#return-" title="Permalink to this return value"></a>
                    <div style="font-size: small">
                      <span style="color: purple">string</span>
                    </div>
                </td>
                <td>always</td>
                <td>
                            <div>The type of the value (string, int, etc)</div>
                    <br/>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder">&nbsp;</td>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="return-"></div>
                    <b>value</b>
                    <a class="ansibleOptionLink" href="#return-" title="Permalink to this return value"></a>
                    <div style="font-size: small">
                      <span style="color: purple">string</span>
                    </div>
                </td>
                <td>always</td>
                <td>
                            <div>The value of the output as interpolated by Terraform</div>
                    <br/>
                </td>
            </tr>

            <tr>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="return-"></div>
                    <b>stdout</b>
                    <a class="ansibleOptionLink" href="#return-" title="Permalink to this return value"></a>
                    <div style="font-size: small">
                      <span style="color: purple">string</span>
                    </div>
                </td>
                <td>always</td>
                <td>
                            <div>Full <code>terraform</code> command stdout, in case you want to display it or examine the event log</div>
                    <br/>
                </td>
            </tr>
    </table>
    <br/><br/>


Status
------


Authors
~~~~~~~

- Ryan Scott Brown (@ryansb)
