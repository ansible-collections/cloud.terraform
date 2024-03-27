# -*- coding: utf-8 -*-

# Copyright: Ansible Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)


DOCUMENTATION = r"""
name: terraform_state
author:
  - Aubin Bikouo (@abikouo)
short_description: Builds an inventory from resources created by cloud providers.
description:
  - This plugin works with an existing state file to create an inventory from resources created by cloud providers.
  - The plugin accepts a Terraform backend config to an existing state file or a path to an existing state file.
  - Uses a YAML configuration file that ends with terraform_state.(yml|yaml).
  - To read the state file command ``Terraform show`` is used.
  - Does not support caching.
extends_documentation_fragment:
  - constructed
version_added: 2.1.0
options:
  plugin:
    description:
      - The name of the Inventory Plugin.
      - This should always be C(cloud.terraform.terraform_state).
    required: true
    type: str
    choices: [ cloud.terraform.terraform_state ]
  backend_type:
    description:
      - The Terraform backend type from which the state file will be retrieved.
    type: str
    required: true
  backend_config:
    description:
      - A group of key-values used to configure the backend.
      - These values will be provided at init stage to the -backend-config parameter.
    type: dict
  backend_config_files:
    description:
      - The path to a configuration file to provide at init state to the -backend-config parameter.
        This can accept a list of paths to multiple configuration files.
    type: list
    elements: path
  search_child_modules:
    description:
      - Whether to include resources from Terraform child modules.
    type: bool
    default: false
  binary_path:
    description:
      - The path of a terraform binary to use.
    type: path
  hostnames:
    description:
      - A list in order of precedence for hostname variables.
      - The elements of the list can be a dict with the keys mentioned below or a string.
      - Can be one of the options specified in U(https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/instance#argument-reference).
      - If value provided does not exist in the above options, it will be used as a literal string.
      - To use tags as hostnames use the syntax tag:Name=Value to use the hostname Name_Value, or tag:Name to use the value of the Name tag.
      - If not provided the final hostname will be C(terraform resource type) + C(_) + C(terraform resource name)
    type: list
    elements: raw
    default: []
    suboptions:
      name:
        description:
          - Name of the host.
        type: str
        required: True
      prefix:
        description:
          - Prefix to prepend to I(name). Same options as I(name).
          - If I(prefix) is specified, final hostname will be I(prefix) +  I(separator) + I(name).
        type: str
        default: ''
        required: False
      separator:
        description:
          - Value to separate I(prefix) and I(name) when I(prefix) is specified.
        type: str
        default: '_'
        required: False
"""

EXAMPLES = r"""
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
"""


import os
from dataclasses import dataclass
from tempfile import TemporaryDirectory
from typing import Any, Dict, List, Optional

from ansible.module_utils._text import to_text
from ansible.module_utils.common import process
from ansible.plugins.inventory import Constructable
from ansible_collections.cloud.terraform.plugins.module_utils.errors import TerraformError, TerraformWarning
from ansible_collections.cloud.terraform.plugins.module_utils.models import TerraformModuleResource
from ansible_collections.cloud.terraform.plugins.module_utils.terraform_commands import TerraformCommands
from ansible_collections.cloud.terraform.plugins.module_utils.utils import validate_bin_path
from ansible_collections.cloud.terraform.plugins.plugin_utils.base import TerraformInventoryPluginBase
from ansible_collections.cloud.terraform.plugins.plugin_utils.common import module_run_command


@dataclass
class TerraformProviderInstance:
    provider_name: str
    types: List[str]


ProvidersMapping = {
    "aws": TerraformProviderInstance(provider_name="registry.terraform.io/hashicorp/aws", types=["aws_instance"]),
    "azurerm": TerraformProviderInstance(
        provider_name="registry.terraform.io/hashicorp/azurerm",
        types=["azurerm_virtual_machine", "azurerm_linux_virtual_machine", "azurerm_windows_virtual_machine"],
    ),
    "google": TerraformProviderInstance(
        provider_name="registry.terraform.io/hashicorp/google", types=["google_compute_instance"]
    ),
}


def filter_instances(
    resources: List[TerraformModuleResource], providers: List[TerraformProviderInstance]
) -> List[TerraformModuleResource]:
    return [
        r
        for r in resources
        if any(r.type in provider.types and r.provider_name == provider.provider_name for provider in providers)
    ]


def get_tag_hostname(instance: TerraformModuleResource, preference: str) -> Optional[str]:
    # from 'tag:Name=Tag1,Name=Tag2' to ['Name=Tag1', 'Name=Tag2']
    tag_hostnames = preference.split("tag:", 1)[1].split(",")
    instance_tags: Dict[str, str] = instance.values.get("tags", {})  # type: ignore  # mypy ignore
    hostname = None
    for v in tag_hostnames:
        items = v.split("=", 1)
        if len(items) > 1:
            if instance_tags.get(items[0]) == items[1]:
                hostname = to_text(items[0]) + "_" + to_text(items[1])
        elif instance_tags.get(v):
            hostname = instance_tags.get(v)
    return hostname


def get_preferred_hostname(instance: TerraformModuleResource, hostnames: Optional[List[Any]] = None) -> Optional[str]:
    if not hostnames:
        return instance.type + "_" + instance.name

    hostname = None
    for preference in hostnames:
        if isinstance(preference, dict):
            if "name" not in preference:
                raise TerraformError("A 'name' key must be defined in a hostnames dictionary.")
            hostname = get_preferred_hostname(instance, [preference["name"]])
            hostname_from_prefix = None
            if hostname and "prefix" in preference:
                hostname_from_prefix = get_preferred_hostname(instance, [preference["prefix"]])
                separator = preference.get("separator", "_")
                if hostname_from_prefix:
                    hostname = hostname_from_prefix + separator + hostname
        elif preference.startswith("tag:"):
            hostname = get_tag_hostname(instance, preference)
        else:
            hostname = preference
            if preference in instance.values:
                hostname = str(instance.values.get(preference, ""))
        if hostname:
            break
    return hostname


def write_terraform_config(backend_type: str, path: str) -> None:
    tf_config = "terraform {\n"
    tf_config += 'backend "%s" {}' % backend_type
    tf_config += "\n}"
    with open(path, "w") as temp_file:
        temp_file.write(tf_config)


class InventoryModule(TerraformInventoryPluginBase, Constructable):  # type: ignore  # mypy ignore
    NAME = "cloud.terraform.terraform_state"

    def verify_file(self, path):  # type: ignore  # mypy ignore
        """
        return true/false if this is possibly a valid file for this plugin to consume
        """
        valid = False
        if super(InventoryModule, self).verify_file(path):
            # base class verifies that file exists and is readable by current user
            if path.endswith(("terraform_state.yaml", "terraform_state.yml")):
                valid = True
        return valid

    def _query(
        self,
        terraform_binary: str,
        backend_type: str,
        backend_config: Optional[Dict[str, str]],
        backend_config_files: Optional[List[str]],
        search_child_modules: bool,
        providers: List[TerraformProviderInstance],
    ) -> List[TerraformModuleResource]:
        with TemporaryDirectory() as temp_dir:
            write_terraform_config(backend_type, os.path.join(temp_dir, "main.tf"))
            terraform = TerraformCommands(module_run_command, temp_dir, terraform_binary, False)
            try:
                terraform.init(backend_config=backend_config, backend_config_files=backend_config_files)
                result = terraform.show()
                instances: List[TerraformModuleResource] = []
                if result:
                    root_module = result.values.root_module
                    resources = root_module.resources if not search_child_modules else root_module.flatten_resources()
                    instances = filter_instances(resources, providers)
                return instances
            except TerraformWarning as e:
                raise TerraformError(e.message)

    def _sanitize_hostname(self, hostname: str) -> str:
        if ":" in to_text(hostname):
            return str(self._sanitize_group_name(to_text(hostname)))
        else:
            return str(to_text(hostname))

    def create_inventory(
        self,
        instances: List[TerraformModuleResource],
        hostnames: Optional[List[Any]],
        compose: Optional[Dict[str, str]],
        keyed_groups: List[Dict[str, Any]],
        strict: bool,
    ) -> None:
        for instance in instances:
            name = get_preferred_hostname(instance, hostnames)
            if name:
                name = self._sanitize_hostname(name)
                self.inventory.add_host(name)
                host_vars = instance.values

                # Set individuals host variables
                for k, v in host_vars.items():
                    self.inventory.set_variable(name, k, v)

                # Composed variables
                self._set_composite_vars(compose, host_vars, name, strict=strict)

                # Create groups based on variable values and add the corresponding hosts to it
                self._add_host_to_keyed_groups(keyed_groups, host_vars, name, strict=strict)

    def parse(self, inventory, loader, path, cache=False):  # type: ignore  # mypy ignore
        super(InventoryModule, self).parse(inventory, loader, path, cache=cache)

        cfg = self.read_config_data(path)  # type: ignore  # mypy ignore

        backend_config = cfg.get("backend_config")
        backend_config_files = cfg.get("backend_config_files")
        backend_type = cfg.get("backend_type")
        terraform_binary = cfg.get("binary_path")
        search_child_modules = cfg.get("search_child_modules", False)

        if not backend_type:
            raise TerraformError("The parameter 'backend_type' is required to use this inventory plugin.")

        if not backend_config and not backend_config_files:
            raise TerraformError(
                "At least one of 'backend_config' or 'backend_config_files' option is required to configure the Terraform backend."
            )

        if terraform_binary is not None:
            validate_bin_path(terraform_binary)
        else:
            terraform_binary = process.get_bin_path("terraform")

        # Transform the backend_config_files from Str to List[Str]
        if backend_config_files and not isinstance(backend_config_files, list):
            backend_config_files = [backend_config_files]

        providers = [v for k, v in ProvidersMapping.items()]
        instances = self._query(
            terraform_binary,
            backend_type,
            backend_config,
            backend_config_files,
            search_child_modules,
            providers,
        )
        self.create_inventory(
            instances, cfg.get("hostnames"), cfg.get("compose"), cfg.get("keyed_groups"), cfg.get("strict")
        )
