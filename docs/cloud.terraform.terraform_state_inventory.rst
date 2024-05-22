.. _cloud.terraform.terraform_state_inventory:


*******************************
cloud.terraform.terraform_state
*******************************

**Builds an inventory from resources created by cloud providers.**


Version added: 2.1.0

.. contents::
   :local:
   :depth: 1


Synopsis
--------
- This plugin works with an existing state file to create an inventory from resources created by cloud providers.
- The plugin accepts a Terraform backend config to an existing state file or a path to an existing state file.
- Uses a YAML configuration file that ends with terraform_state.(yml|yaml).
- To read the state file command ``Terraform show`` is used.
- Does not support caching.




Parameters
----------

.. raw:: html

    <table  border=0 cellpadding=0 class="documentation-table">
        <tr>
            <th colspan="2">Parameter</th>
            <th>Choices/<font color="blue">Defaults</font></th>
                <th>Configuration</th>
            <th width="100%">Comments</th>
        </tr>
            <tr>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>backend_config</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">dictionary</span>
                    </div>
                </td>
                <td>
                </td>
                    <td>
                    </td>
                <td>
                        <div>A group of key-values used to configure the backend.</div>
                        <div>These values will be provided at init stage to the -backend-config parameter.</div>
                </td>
            </tr>
            <tr>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>backend_config_files</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">list</span>
                         / <span style="color: purple">elements=path</span>
                    </div>
                </td>
                <td>
                </td>
                    <td>
                    </td>
                <td>
                        <div>The absolute path to a configuration file to provide at init state to the -backend-config parameter. This can accept a list of paths to multiple configuration files.</div>
                </td>
            </tr>
            <tr>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>backend_type</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                         / <span style="color: red">required</span>
                    </div>
                </td>
                <td>
                </td>
                    <td>
                    </td>
                <td>
                        <div>The Terraform backend type from which the state file will be retrieved.</div>
                </td>
            </tr>
            <tr>
                <td colspan="2">
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
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>compose</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">dictionary</span>
                    </div>
                </td>
                <td>
                        <b>Default:</b><br/><div style="color: blue">{}</div>
                </td>
                    <td>
                    </td>
                <td>
                        <div>Create vars from jinja2 expressions.</div>
                </td>
            </tr>
            <tr>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>groups</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">dictionary</span>
                    </div>
                </td>
                <td>
                        <b>Default:</b><br/><div style="color: blue">{}</div>
                </td>
                    <td>
                    </td>
                <td>
                        <div>Add hosts to group based on Jinja2 conditionals.</div>
                </td>
            </tr>
            <tr>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>hostnames</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">list</span>
                         / <span style="color: purple">elements=raw</span>
                    </div>
                </td>
                <td>
                        <b>Default:</b><br/><div style="color: blue">[]</div>
                </td>
                    <td>
                    </td>
                <td>
                        <div>A list in order of precedence for hostname variables.</div>
                        <div>The elements of the list can be a dict with the keys mentioned below or a string.</div>
                        <div>Can be one of the options specified in <a href='https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/instance#argument-reference'>https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/instance#argument-reference</a>.</div>
                        <div>If value provided does not exist in the above options, it will be used as a literal string.</div>
                        <div>To use tags as hostnames use the syntax tag:Name=Value to use the hostname Name_Value, or tag:Name to use the value of the Name tag.</div>
                        <div>If not provided the final hostname will be <code>terraform resource type</code> + <code>_</code> + <code>terraform resource name</code></div>
                </td>
            </tr>
                                <tr>
                    <td class="elbow-placeholder"></td>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>name</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                         / <span style="color: red">required</span>
                    </div>
                </td>
                <td>
                </td>
                    <td>
                    </td>
                <td>
                        <div>Name of the host.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>prefix</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                        <b>Default:</b><br/><div style="color: blue">""</div>
                </td>
                    <td>
                    </td>
                <td>
                        <div>Prefix to prepend to <em>name</em>. Same options as <em>name</em>.</div>
                        <div>If <em>prefix</em> is specified, final hostname will be <em>prefix</em> +  <em>separator</em> + <em>name</em>.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>separator</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                        <b>Default:</b><br/><div style="color: blue">"_"</div>
                </td>
                    <td>
                    </td>
                <td>
                        <div>Value to separate <em>prefix</em> and <em>name</em> when <em>prefix</em> is specified.</div>
                </td>
            </tr>

            <tr>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>keyed_groups</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">list</span>
                         / <span style="color: purple">elements=dictionary</span>
                    </div>
                </td>
                <td>
                        <b>Default:</b><br/><div style="color: blue">[]</div>
                </td>
                    <td>
                    </td>
                <td>
                        <div>Add hosts to group based on the values of a variable.</div>
                </td>
            </tr>
                                <tr>
                    <td class="elbow-placeholder"></td>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>default_value</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                    <div style="font-style: italic; font-size: small; color: darkgreen">added in 2.12</div>
                </td>
                <td>
                </td>
                    <td>
                    </td>
                <td>
                        <div>The default value when the host variable&#x27;s value is an empty string.</div>
                        <div>This option is mutually exclusive with O(keyed_groups[].trailing_separator).</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>key</b>
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
                        <div>The key from input dictionary used to generate groups</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>parent_group</b>
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
                        <div>parent group for keyed group</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>prefix</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                        <b>Default:</b><br/><div style="color: blue">""</div>
                </td>
                    <td>
                    </td>
                <td>
                        <div>A keyed group name will start with this prefix</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>separator</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                        <b>Default:</b><br/><div style="color: blue">"_"</div>
                </td>
                    <td>
                    </td>
                <td>
                        <div>separator used to build the keyed group name</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>trailing_separator</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">boolean</span>
                    </div>
                    <div style="font-style: italic; font-size: small; color: darkgreen">added in 2.12</div>
                </td>
                <td>
                        <ul style="margin: 0; padding: 0"><b>Choices:</b>
                                    <li>no</li>
                                    <li><div style="color: blue"><b>yes</b>&nbsp;&larr;</div></li>
                        </ul>
                </td>
                    <td>
                    </td>
                <td>
                        <div>Set this option to V(False) to omit the O(keyed_groups[].separator) after the host variable when the value is an empty string.</div>
                        <div>This option is mutually exclusive with O(keyed_groups[].default_value).</div>
                </td>
            </tr>

            <tr>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>leading_separator</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">boolean</span>
                    </div>
                    <div style="font-style: italic; font-size: small; color: darkgreen">added in 2.11</div>
                </td>
                <td>
                        <b>Default:</b><br/><div style="color: blue">"yes"</div>
                </td>
                    <td>
                    </td>
                <td>
                        <div>Use in conjunction with keyed_groups.</div>
                        <div>By default, a keyed group that does not have a prefix or a separator provided will have a name that starts with an underscore.</div>
                        <div>This is because the default prefix is &quot;&quot; and the default separator is &quot;_&quot;.</div>
                        <div>Set this option to False to omit the leading underscore (or other separator) if no prefix is given.</div>
                        <div>If the group name is derived from a mapping the separator is still used to concatenate the items.</div>
                        <div>To not use a separator in the group name at all, set the separator for the keyed group to an empty string instead.</div>
                </td>
            </tr>
            <tr>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>plugin</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                         / <span style="color: red">required</span>
                    </div>
                </td>
                <td>
                        <ul style="margin: 0; padding: 0"><b>Choices:</b>
                                    <li>cloud.terraform.terraform_state</li>
                        </ul>
                </td>
                    <td>
                    </td>
                <td>
                        <div>The name of the Inventory Plugin.</div>
                        <div>This should always be <code>cloud.terraform.terraform_state</code>.</div>
                </td>
            </tr>
            <tr>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>search_child_modules</b>
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
                    </td>
                <td>
                        <div>Whether to include resources from Terraform child modules.</div>
                </td>
            </tr>
            <tr>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>strict</b>
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
                    </td>
                <td>
                        <div>If V(yes) make invalid entries a fatal error, otherwise skip and continue.</div>
                        <div>Since it is possible to use facts in the expressions they might not always be available and we ignore those errors by default.</div>
                </td>
            </tr>
            <tr>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>use_extra_vars</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">boolean</span>
                    </div>
                    <div style="font-style: italic; font-size: small; color: darkgreen">added in 2.11</div>
                </td>
                <td>
                        <ul style="margin: 0; padding: 0"><b>Choices:</b>
                                    <li><div style="color: blue"><b>no</b>&nbsp;&larr;</div></li>
                                    <li>yes</li>
                        </ul>
                </td>
                    <td>
                            <div> ini entries:
                                    <p>[inventory_plugins]<br>use_extra_vars = no</p>
                            </div>
                                <div>env:ANSIBLE_INVENTORY_USE_EXTRA_VARS</div>
                    </td>
                <td>
                        <div>Merge extra vars into the available variables for composition (highest precedence).</div>
                </td>
            </tr>
    </table>
    <br/>




Examples
--------

.. code-block:: yaml

    # Inventory with state file stored into http backend
    - name: Create an inventory from state file stored into http backend
      plugin: cloud.terraform.terraform_state
      backend_type: http
      backend_config:
        address: https://localhost:8043/api/v2/state/3/
        skip_cert_verification: true
        username: ansible
        password: test123!

      # Running command `ansible-inventory -i basic_terraform_state.yaml --graph --vars` would then produce the inventory:
      # @all:
      # |--@ungrouped:
      # |  |--aws_instance_test
      # |  |  |--{ami = ami-01d00f1bdb42735ac}
      # |  |  |--{arn = arn:aws:ec2:us-east-1:721066863947:instance/i-09c4a5b5d74c9b941}
      # |  |  |--{associate_public_ip_address = True}
      # |  |  |--{availability_zone = us-east-1b}
      # |  |  |--{capacity_reservation_specification = [{'capacity_reservation_preference': 'open', 'capacity_reservation_target': []}]}
      # |  |  |--{cpu_core_count = 1}
      # |  |  |--{cpu_options = [{'amd_sev_snp': '', 'core_count': 1, 'threads_per_core': 1}]}
      # |  |  |--{cpu_threads_per_core = 1}
      # |  |  |--{credit_specification = [{'cpu_credits': 'standard'}]}
      # |  |  |--{disable_api_stop = False}
      # |  |  |--{disable_api_termination = False}
      # |  |  |--{ebs_block_device = []}
      # |  |  |--{ebs_optimized = False}
      # |  |  |--{enclave_options = [{'enabled': False}]}
      # |  |  |--{ephemeral_block_device = []}
      # |  |  |--{get_password_data = False}
      # |  |  |--{hibernation = False}
      # |  |  |--{host_id = }
      # |  |  |--{host_resource_group_arn = None}
      # |  |  |--{iam_instance_profile = }
      # |  |  |--{id = i-09c4a5b5d74c9b941}
      # |  |  |--{instance_initiated_shutdown_behavior = stop}
      # |  |  |--{instance_lifecycle = }
      # |  |  |--{instance_market_options = []}
      # |  |  |--{instance_state = running}
      # |  |  |--{instance_type = t2.micro}
      # |  |  |--{ipv6_address_count = 0}
      # |  |  |--{ipv6_addresses = []}
      # |  |  |--{key_name = connect-key-20231127}
      # |  |  |--{launch_template = []}
      # |  |  |--{maintenance_options = [{'auto_recovery': 'default'}]}
      # |  |  |--{metadata_options = [{...}]}
      # |  |  |--{monitoring = False}
      # |  |  |--{network_interface = []}
      # |  |  |--{outpost_arn = }
      # |  |  |--{password_data = }
      # |  |  |--{placement_group = }
      # |  |  |--{placement_partition_number = 0}
      # |  |  |--{primary_network_interface_id = eni-0d5ccb55032b5e01c}
      # |  |  |--{private_dns = ip-168-10-1-178.us-east-1.compute.internal}
      # |  |  |--{private_dns_name_options = [{...}]}
      # |  |  |--{private_ip = 168.10.1.178}
      # |  |  |--{public_dns = }
      # |  |  |--{public_ip = 34.244.225.201}
      # |  |  |--{root_block_device = [{...}]}
      # |  |  |--{secondary_private_ips = []}
      # |  |  |--{security_groups = []}
      # |  |  |--{source_dest_check = True}
      # |  |  |--{spot_instance_request_id = }
      # |  |  |--{subnet_id = subnet-0e5159474f5fc6a17}
      # |  |  |--{tags = {'Inventory': 'terraform_state', 'Name': 'test-ec2', 'Phase': 'integration'}}
      # |  |  |--{tags_all = {'Inventory': 'terraform_state', 'Name': 'test-ec2', 'Phase': 'integration'}}
      # |  |  |--{tenancy = default}
      # |  |  |--{timeouts = None}
      # |  |  |--{user_data = None}
      # |  |  |--{user_data_base64 = None}
      # |  |  |--{user_data_replace_on_change = False}
      # |  |  |--{volume_tags = None}
      # |  |  |--{vpc_security_group_ids = ['sg-0795c8f75883b0927']}


    # Example using constructed features to set ansible_host
    - name: Using compose feature to set the ansible_host
      plugin: cloud.terraform.terraform_state
      backend_type: s3
      backend_config:
        region: us-east-1
        key: terraform/state
        bucket: my-sample-bucket
      compose:
        ansible_host: public_ip

      # Running command `ansible-inventory -i compose_terraform_state.yaml --graph --vars` would then produce the inventory:
      # @all:
      # |--@ungrouped:
      # |  |--aws_instance_test
      # |  |  |--{ami = ami-01d00f1bdb42735ac}
      # |  |  |--{ansible_host = 34.244.225.201}
      # (...)
      # |  |  |--{public_ip = 34.244.225.201}
      # (...)

    # Example using constructed features to create inventory groups
    - name: Using keyed_groups feature to add host into group
      plugin: cloud.terraform.terraform_state
      backend_type: s3
      backend_config:
        region: us-east-1
        key: terraform/state
        bucket: my-sample-bucket
      keyed_groups:
        - key: instance_state
          prefix: state

      # Running command `ansible-inventory -i keyed_terraform_state.yaml --graph` would then produce the inventory:
      # @all:
      # |--@ungrouped:
      # |--@state_running:
      # |  |--aws_instance_test

    # Example using hostnames feature to define inventory hostname
    - name: Using hostnames feature to define inventory hostname
      plugin: cloud.terraform.terraform_state
      backend_type: s3
      backend_config:
        region: us-east-1
        key: terraform/state
        bucket: my-sample-bucket
      hostnames:
        - name: 'tag:Phase'
          separator: "-"
          prefix: 'instance_state'

      # Running command `ansible-inventory -i hostnames_terraform_state.yaml --graph` would then produce the inventory:
      # @all:
      # |--@ungrouped:
      # |  |--running-integration

    # Example using backend_config_files option to configure the backend
    - name: Using backend_config_files to configure the backend
      plugin: cloud.terraform.terraform_state
      backend_type: s3
      backend_config:
        region: us-east-1
      backend_config_files:
        - /path/to/config1
        - /path/to/config2

      # With the following content for config1
      #
      # key = "terraform/tfstate"
      # bucket = "my-tf-backend-bucket"
      #
      # and the following content for config2
      #
      # access_key = "xxxxxxxxxxxxxx"
      # secret_key = "xxxxxxxxxxxxxx"
      # token = "xxxxxxxxxxxxx"
    # Inventory built from state file containing AWS, AzureRM and GCP instances
    - name: Create inventory from state file containing AWS, AzureRM and GCP instances
      plugin: cloud.terraform.terraform_state
      backend_type: azurerm
      backend_config:
        resource_group_name: my-resource-group
        storage_account_name: mystorageaccount
        container_name: terraformstate
        key: inventory.tfstate
      # Running command `ansible-inventory -i aws_and_azure_terraform_state.yaml --graph --vars` would then produce the inventory:
      # @all:
      # |--@ungrouped:
      # |  |--aws_instance_test
      # |  |  |--{ami = ami-01d00f1bdb42735ac}
      # |  |  |--{arn = arn:aws:ec2:us-east-1:721066863947:instance/i-09c4a5b5d74c9b941}
      # |  |  |--{associate_public_ip_address = True}
      # |  |  |--{availability_zone = us-east-1b}
      # |  |  |--{capacity_reservation_specification = [{'capacity_reservation_preference': 'open', 'capacity_reservation_target': []}]}
      # |  |  |--{cpu_core_count = 1}
      # |  |  |--{cpu_options = [{'amd_sev_snp': '', 'core_count': 1, 'threads_per_core': 1}]}
      # |  |  |--{cpu_threads_per_core = 1}
      # |  |  |--{credit_specification = [{'cpu_credits': 'standard'}]}
      # |  |  |--{disable_api_stop = False}
      # |  |  |--{disable_api_termination = False}
      # |  |  |--{ebs_block_device = []}
      # |  |  |--{ebs_optimized = False}
      # |  |  |--{enclave_options = [{'enabled': False}]}
      # |  |  |--{ephemeral_block_device = []}
      # |  |  |--{get_password_data = False}
      # |  |  |--{hibernation = False}
      # |  |  |--{host_id = }
      # |  |  |--{host_resource_group_arn = None}
      # |  |  |--{iam_instance_profile = }
      # |  |  |--{id = i-09c4a5b5d74c9b941}
      # |  |  |--{instance_initiated_shutdown_behavior = stop}
      # |  |  |--{instance_lifecycle = }
      # |  |  |--{instance_market_options = []}
      # |  |  |--{instance_state = running}
      # |  |  |--{instance_type = t2.micro}
      # |  |  |--{ipv6_address_count = 0}
      # |  |  |--{ipv6_addresses = []}
      # |  |  |--{key_name = connect-key-20231127}
      # |  |  |--{launch_template = []}
      # |  |  |--{maintenance_options = [{'auto_recovery': 'default'}]}
      # |  |  |--{metadata_options = [{...}]}
      # |  |  |--{monitoring = False}
      # |  |  |--{network_interface = []}
      # |  |  |--{outpost_arn = }
      # |  |  |--{password_data = }
      # |  |  |--{placement_group = }
      # |  |  |--{placement_partition_number = 0}
      # |  |  |--{primary_network_interface_id = eni-0d5ccb55032b5e01c}
      # |  |  |--{private_dns = ip-168-10-1-178.us-east-1.compute.internal}
      # |  |  |--{private_dns_name_options = [{...}]}
      # |  |  |--{private_ip = 168.10.1.178}
      # |  |  |--{public_dns = }
      # |  |  |--{public_ip = 34.244.225.201}
      # |  |  |--{root_block_device = [{...}]}
      # |  |  |--{secondary_private_ips = []}
      # |  |  |--{security_groups = []}
      # |  |  |--{source_dest_check = True}
      # |  |  |--{spot_instance_request_id = }
      # |  |  |--{subnet_id = subnet-0e5159474f5fc6a17}
      # |  |  |--{tags = {'Inventory': 'terraform_state', 'Name': 'test-ec2', 'Phase': 'integration'}}
      # |  |  |--{tags_all = {'Inventory': 'terraform_state', 'Name': 'test-ec2', 'Phase': 'integration'}}
      # |  |  |--{tenancy = default}
      # |  |  |--{timeouts = None}
      # |  |  |--{user_data = None}
      # |  |  |--{user_data_base64 = None}
      # |  |  |--{user_data_replace_on_change = False}
      # |  |  |--{volume_tags = None}
      # |  |  |--{vpc_security_group_ids = ['sg-0795c8f75883b0927']}
      # |  |--azurerm_virtual_machine_main
      # |  |  |--{additional_capabilities = []}
      # |  |  |--{availability_set_id = None}
      # |  |  |--{boot_diagnostics = []}
      # |  |  |--{delete_data_disks_on_termination = True}
      # |  |  |--{delete_os_disk_on_termination = True}
      # |  |  |--{id = /subscriptions/xxxxx-xxxx-xxxx-xxxx-xxxxxxxx/resourceGroups/rg/providers/Microsoft.Compute/virtualMachines/test-vm}
      # |  |  |--{identity = []}
      # |  |  |--{license_type = None}
      # |  |  |--{location = westeurope}
      # |  |  |--{name = test-vm}
      # |  |  |--{network_interface_ids = ['/subscriptions/xxxxx-xxxx-xxxx-xxxx-xxxxxxxx/resourceGroups/rg/providers/Microsoft.Network/networkInterfaces/test']}
      # |  |  |--{os_profile = [{'admin_password': '', 'admin_username': 'ansible', 'computer_name': 'hostname', 'custom_data': ''}]}
      # |  |  |--{os_profile_linux_config = [{'disable_password_authentication': False, 'ssh_keys': []}]}
      # |  |  |--{os_profile_secrets = []}
      # |  |  |--{os_profile_windows_config = []}
      # |  |  |--{plan = []}
      # |  |  |--{primary_network_interface_id = None}
      # |  |  |--{proximity_placement_group_id = None}
      # |  |  |--{resource_group_name = rg}
      # |  |  |--{storage_data_disk = []}
      # |  |  |--{storage_image_reference = [{'id': '', 'offer': 'xxxxx', 'publisher': 'Canonical', 'sku': '22_04-lts', 'version': 'latest'}]}
      # |  |  |--{timeouts = None}
      # |  |  |--{vm_size = Standard_DS1_v2}
      # |  |  |--{zones = []}
      # |  |--google_compute_instance_default
      # |  |  |--{advanced_machine_features = []}
      # |  |  |--{allow_stopping_for_update = None}
      # |  |  |--{attached_disk = []}
      # |  |  |--{boot_disk = [{'auto_delete': True, 'device_name': 'persistent-disk-0', 'disk_encryption_key_raw': ''}]
      # |  |  |--{can_ip_forward = False}
      # |  |  |--{confidential_instance_config = []}
      # |  |  |--{cpu_platform = Intel Cascade Lake}
      # |  |  |--{current_status = RUNNING}
      # |  |  |--{deletion_protection = False}
      # |  |  |--{description = }
      # |  |  |--{desired_status = None}
      # |  |  |--{effective_labels = {}}
      # |  |  |--{enable_display = False}
      # |  |  |--{guest_accelerator = []}
      # |  |  |--{hostname = }
      # |  |  |--{id = projects/xxxx/zones/us-east1-c/instances/ansible-cloud-001}
      # |  |  |--{instance_id = 0123456789012345678}
      # |  |  |--{label_fingerprint = 42WmSpB8rSM=}
      # |  |  |--{labels = {}}
      # |  |  |--{machine_type = n2-standard-2}
      # |  |  |--{metadata = {}}
      # |  |  |--{metadata_fingerprint = WP5-7HGjCUM=}
      # |  |  |--{metadata_startup_script = None}
      # |  |  |--{min_cpu_platform = }
      # |  |  |--{name = ansible-cloud-001}
      # |  |  |--{network_performance_config = []}
      # |  |  |--{params = []}
      # |  |  |--{project = agcp-001-dev}
      # |  |  |--{reservation_affinity = []}
      # |  |  |--{resource_policies = []}
      # |  |  |--{scratch_disk = [{'device_name': 'local-ssd-0', 'interface': 'NVME', 'size': 375}]}
      # |  |  |--{service_account = []}
      # |  |  |--{tags = []}
      # |  |  |--{tags_fingerprint = 42WmSpB8rSM=}
      # |  |  |--{terraform_labels = {}}
      # |  |  |--{timeouts = None}
      # |  |  |--{zone = us-east1-c}




Status
------


Authors
~~~~~~~

- Aubin Bikouo (@abikouo)


.. hint::
    Configuration entries for each entry type have a low to high priority order. For example, a variable that is lower in the list will override a variable that is higher up.
