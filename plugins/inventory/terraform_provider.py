# -*- coding: utf-8 -*-

# Copyright: (c) 2022, XLAB Steampunk <steampunk@xlab.si>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)


DOCUMENTATION = r"""
name: terraform_provider
author:
  - Polona Mihalič (@PolonaM)
short_description: Builds an inventory from Terraform state file.
description:
  - Builds an inventory from specified state file.
  - To read state file command "Terraform show" is used, thus requiring initialized working directory.
  - Does not support caching.
version_added: 1.1.0
seealso: []
options:
  plugin:
    description:
      - The name of the Inventory Plugin.
      - This should always be C(cloud.terraform.terraform_provider).
    required: true
    type: str
    choices: [ cloud.terraform.terraform_provider ]
    version_added: 1.1.0
  project_path:
    description:
      - The path to the initialized Terraform directory with the .tfstate file.
      - If I(state_file) is not specified, C(terraform.tfstate) in I(project_path) is used as an inventory source.
      - If I(state_file) and I(project_path) are not specified, C(terraform.tfstate) file in the current
        working directory is used as an inventory source.
    type: path
    version_added: 1.1.0
  state_file:
    description:
      - Path to an existing Terraform state file to be used as an inventory source.
      - If I(state_file) is not specified, C(terraform.tfstate) in I(project_path) is used as an inventory source.
      - If I(state_file) and I(project_path) are not specified, C(terraform.tfstate) file in the current
        working directory is used as an inventory source.
    type: path
    version_added: 1.1.0
  binary_path:
    description:
      - The path of a terraform binary to use.
    type: path
    version_added: 1.1.0
"""

EXAMPLES = r"""
# Example configuration file inventory.yml, that creates an inventory from terraform.tfstate file in cwd
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

# Example configuration file that creates an inventory from terraform.tfstate file in selected project directory
plugin: cloud.terraform.terraform_provider
project_path: some/project/path

# Example configuration file that creates an inventory from specified state file
plugin: cloud.terraform.terraform_provider
state_file: some/state/file/path

# Example configuration file that creates an inventory from mycustomstate.tfstate file in selected project directory
plugin: cloud.terraform.terraform_provider
project_path: some/project/path
state_file: mycustomstate.tfstate
"""


import os
import subprocess
from typing import List, Tuple, Any
import yaml

from ansible.errors import AnsibleParserError
from ansible.plugins.inventory import BaseInventoryPlugin
from ansible.module_utils.common import process
from ansible_collections.cloud.terraform.plugins.module_utils.utils import validate_bin_path
from ansible_collections.cloud.terraform.plugins.module_utils.terraform_commands import TerraformCommands
from ansible_collections.cloud.terraform.plugins.module_utils.errors import TerraformWarning, TerraformError
from ansible_collections.cloud.terraform.plugins.module_utils.models import (
    TerraformRootModuleResource,
    TerraformAnsibleProvider,
    TerraformShow,
)


# no module available here, mock functionality to be consistent throughout the rest of the codebase
def module_run_command(cmd: List[str], cwd: str, check_rc: bool) -> Tuple[int, str, str]:
    completed_process = subprocess.run(cmd, capture_output=True, check=check_rc, cwd=cwd)
    return (
        completed_process.returncode,
        completed_process.stdout.decode("utf-8"),
        completed_process.stderr.decode("utf-8"),
    )


class InventoryModule(BaseInventoryPlugin):  # type: ignore  # mypy ignore
    NAME = "terraform_provider"

    # instead of self._read_config_data(path), which reads paths as absolute thus creating problems
    # in case if project_path is provided and state_file is provided as relative path
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

    # If check of the name of the cfg file is needed, this should be uncommented
    # def verify_file(self, path):
    #     """
    #     return true/false if this is possibly a valid file for this plugin to consume
    #     """
    #     valid = False
    #     if super(InventoryModule, self).verify_file(path):
    #         # base class verifies that file exists and is readable by current user
    #         if path.endswith(("terraform_provider.yaml", "terraform_provider.yml")):
    #             valid = True
    #     return valid

    def _add_group(self, inventory: Any, resource: TerraformRootModuleResource) -> None:
        attributes = TerraformAnsibleProvider.from_json(resource)
        inventory.add_group(attributes.name)
        if attributes.children:
            for child in attributes.children:
                inventory.add_group(child)
                inventory.add_child(attributes.name, child)
        if attributes.variables:
            for key, value in attributes.variables.items():
                inventory.set_variable(attributes.name, key, value)

    def _add_host(self, inventory: Any, resource: TerraformRootModuleResource) -> None:
        attributes = TerraformAnsibleProvider.from_json(resource)
        inventory.add_host(attributes.name)
        if attributes.groups:
            for group in attributes.groups:
                inventory.add_group(group)
                inventory.add_host(attributes.name, group=group)
        if attributes.variables:
            for key, value in attributes.variables.items():
                inventory.set_variable(attributes.name, key, value)

    def create_inventory(self, inventory: Any, state_content: TerraformShow) -> None:
        for resource in state_content.values.root_module.resources:
            if resource.type == "ansible_group":
                self._add_group(inventory, resource)
            elif resource.type == "ansible_host":
                self._add_host(inventory, resource)

    def parse(self, inventory, loader, path, cache=False):  # type: ignore  # mypy ignore
        super(InventoryModule, self).parse(inventory, loader, path)

        cfg = self.read_config_data(path)  # type: ignore  # mypy ignore

        project_path = cfg.get("project_path", os.getcwd())
        state_file = cfg.get("state_file", "terraform.tfstate")
        terraform_binary = cfg.get("binary_path", None)
        if terraform_binary is not None:
            validate_bin_path(terraform_binary)
        else:
            terraform_binary = process.get_bin_path("terraform", required=True)

        terraform = TerraformCommands(module_run_command, project_path, terraform_binary, False)

        try:
            state_content = terraform.show(state_file)
        except TerraformWarning as e:
            raise TerraformError(e.message)

        if state_content:  # to avoid mypy error: Item "None" of "Optional[TerraformShow]" has no attribute "values"
            self.create_inventory(inventory, state_content)
