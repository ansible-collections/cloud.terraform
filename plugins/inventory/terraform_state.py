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
  backend_config:
    description:
      - A Terraform backend configuration to an existing state file.
    type: str
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
# Example using constructed features to set ansible_host
plugin: cloud.terraform.terraform_state
backend_config: |
  backend "http" {
      address = "https://localhost:8043/api/v2/state/3/"
      skip_cert_verification = true
      username = "ansible"
      password = "test123!"
  }
compose:
  # Use the public IP address to connect to the host
  ansible_host: public_ip
"""


import os
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


def filter_instances(resources: List[TerraformModuleResource], types: List[str]) -> List[TerraformModuleResource]:
    # should we add additional filtering on provider (provider_name='registry.terraform.io/hashicorp/aws') ?
    return [r for r in resources if r.type in types]


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


def write_terraform_config(backend_config: str, path: str) -> None:
    tf_config = "terraform {\n" + backend_config + "\n}"
    with open(path, "w") as temp_file:
        temp_file.write(tf_config)


class InventoryModule(TerraformInventoryPluginBase, Constructable):  # type: ignore  # mypy ignore
    NAME = "terraform_state"

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
        backend_config: str,
        search_child_modules: bool,
        resources_types: Optional[List[str]] = None,
    ) -> List[TerraformModuleResource]:
        if resources_types is None:
            resources_types = ["aws_instance"]
        with TemporaryDirectory() as temp_dir:
            write_terraform_config(backend_config, os.path.join(temp_dir, "main.tf"))
            terraform = TerraformCommands(module_run_command, temp_dir, terraform_binary, False)
            try:
                terraform.init()
                result = terraform.show()
                instances: List[TerraformModuleResource] = []
                if result:
                    root_module = result.values.root_module
                    resources = root_module.resources if not search_child_modules else root_module.flatten_resources()
                    instances = filter_instances(resources, resources_types)
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
        terraform_binary = cfg.get("binary_path")
        search_child_modules = cfg.get("search_child_modules", False)

        if not backend_config:
            raise TerraformError("'backend_config' option is required to read existing state file.")

        if terraform_binary is not None:
            validate_bin_path(terraform_binary)
        else:
            terraform_binary = process.get_bin_path("terraform", required=True)

        instances = self._query(terraform_binary, backend_config, search_child_modules)
        self.create_inventory(
            instances, cfg.get("hostnames"), cfg.get("compose"), cfg.get("keyed_groups"), cfg.get("strict")
        )
