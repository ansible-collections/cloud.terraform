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
    no_log: true
  search_child_modules:
    description:
      - Whether to include resources from Terraform child modules.
    type: bool
    default: false
  binary_path:
    description:
      - The path of a terraform binary to use.
    type: path
"""

EXAMPLES = r"""
# Minimal example using backend configuration
plugin: cloud.terraform.terraform_state
backend_config: |
  backend "http" {
      address = "https://localhost:8043/api/v2/state/3/"
      skip_cert_verification = true
      username = "ansible"
      password = "test123!"
  }

# Example using constructed features to set ansible_host
plugin: cloud.terraform.terraform_state
backend_config: |
  backend "http" {
      address = "https://localhost:8043/api/v2/state/3/"
      skip_cert_verification = true
      username = "ansible"
      password = "test123!"
  }
# Set individual variables with compose
compose:
  # Use the public IP address to connect to the host
  ansible_host: public_ip
"""


import os
from tempfile import TemporaryDirectory
from typing import Dict, List, Optional

import yaml
from ansible.errors import AnsibleParserError
from ansible.module_utils.common import process
from ansible.plugins.inventory import BaseInventoryPlugin, Constructable
from ansible_collections.cloud.terraform.plugins.module_utils.errors import TerraformError, TerraformWarning
from ansible_collections.cloud.terraform.plugins.module_utils.models import TerraformModuleResource
from ansible_collections.cloud.terraform.plugins.module_utils.terraform_commands import TerraformCommands
from ansible_collections.cloud.terraform.plugins.module_utils.utils import validate_bin_path
from ansible_collections.cloud.terraform.plugins.plugin_utils.common import module_run_command


def filter_instances(resources: List[TerraformModuleResource], types: List[str]) -> List[TerraformModuleResource]:
    # should we add additional filtering on provider (provider_name='registry.terraform.io/hashicorp/aws') ?
    return [r for r in resources if r.type in types]


class InventoryModule(BaseInventoryPlugin, Constructable):  # type: ignore  # mypy ignore
    NAME = "terraform_state"

    # instead of self._read_config_data(path), which reads paths as absolute thus creating problems
    # in case if backend_config is provided and state_file is provided as relative path
    def read_config_data(self, path):  # type: ignore  # mypy ignore
        """
        Reads and validates the inventory source file,
        storing the provided configuration as options.
        """
        try:
            with open(path, "r") as inventory_src:
                cfg = yaml.safe_load(inventory_src)
            return cfg
        except Exception as e:
            raise AnsibleParserError(e)

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
        resources_types: List[str] = ["aws_instance"],
    ) -> List[TerraformModuleResource]:
        with TemporaryDirectory() as temp_dir:
            tf_config_path = os.path.join(temp_dir, "main.tf")
            tf_config = "terraform {\n" + backend_config + "\n}"
            with open(tf_config_path, "w") as temp_file:
                temp_file.write(tf_config)

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

    def create_inventory(self, instances: List[TerraformModuleResource], compose: Optional[Dict[str, str]]) -> None:
        for instance in instances:
            name = f"aws_instance_{instance.name}"
            self.inventory.add_host(name)
            host_vars = instance.values

            # Set individuals host variables
            for k, v in host_vars.items():
                self.inventory.set_variable(name, k, v)

            # Use constructed if applicable
            strict = self.get_option("strict")

            # Composed variables
            self._set_composite_vars(compose, host_vars, name, strict=strict)

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
        self.create_inventory(instances, cfg.get("compose"))
