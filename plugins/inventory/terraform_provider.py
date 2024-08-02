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
      - If I(state_file) is not specified, Terraform will attempt to automatically find the state file in I(project_path) for use as inventory source.
      - If I(state_file) and I(project_path) are not specified, Terraform will attempt to automatically find the state file in the current working directory.
      - Accepts a string or a list of paths for use with multiple Terraform projects.
    type: raw
    version_added: 1.1.0
  state_file:
    description:
      - Path to an existing Terraform state file to be used as an inventory source.
      - If I(state_file) is not specified, Terraform will attempt to automatically find the state file in I(project_path) for use as inventory source.
      - If I(state_file) and I(project_path) are not specified, Terraform will attempt to automatically find the state file in the current working directory
    type: path
    version_added: 1.1.0
  search_child_modules:
    description:
      - Whether to include ansible_host and ansible_group resources from Terraform child modules.
    type: bool
    default: false
    version_added: 1.2.0
  binary_path:
    description:
      - The path of a terraform binary to use.
    type: path
    version_added: 1.1.0
"""

EXAMPLES = r"""
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
"""


import os
from typing import Any, List, Optional

from ansible.module_utils.common import process
from ansible_collections.cloud.terraform.plugins.module_utils.errors import TerraformError, TerraformWarning
from ansible_collections.cloud.terraform.plugins.module_utils.models import (
    TerraformAnsibleProvider,
    TerraformModuleResource,
    TerraformShow,
)
from ansible_collections.cloud.terraform.plugins.module_utils.terraform_commands import TerraformCommands
from ansible_collections.cloud.terraform.plugins.module_utils.utils import validate_bin_path
from ansible_collections.cloud.terraform.plugins.plugin_utils.base import TerraformInventoryPluginBase
from ansible_collections.cloud.terraform.plugins.plugin_utils.common import module_run_command


class InventoryModule(TerraformInventoryPluginBase):
    NAME = "cloud.terraform.terraform_provider"

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

    def _add_group(self, inventory: Any, resource: TerraformModuleResource) -> None:
        attributes = TerraformAnsibleProvider.from_json(resource)
        inventory.add_group(attributes.name)
        if attributes.children:
            for child in attributes.children:
                inventory.add_group(child)
                inventory.add_child(attributes.name, child)
        if attributes.variables:
            for key, value in attributes.variables.items():
                inventory.set_variable(attributes.name, key, value)

    def _add_host(self, inventory: Any, resource: TerraformModuleResource) -> None:
        attributes = TerraformAnsibleProvider.from_json(resource)
        # Give warning if group already exists (in case of multiple terraform projects)
        if inventory.get_host(attributes.name):
            raise TerraformWarning(
                f"Ansible Host {attributes.name} already exists elsewhere, please check your terraform project(s)"
            )
        inventory.add_host(attributes.name)
        if attributes.groups:
            for group in attributes.groups:
                inventory.add_group(group)
                inventory.add_host(attributes.name, group=group)
        if attributes.variables:
            for key, value in attributes.variables.items():
                inventory.set_variable(attributes.name, key, value)

    def create_inventory(
        self, inventory: Any, state_content: List[Optional[TerraformShow]], search_child_modules: bool
    ) -> None:
        for state in state_content:
            if state is None:
                continue
            root_resources = (
                state.values.root_module.resources
                if not search_child_modules
                else state.values.root_module.flatten_resources()
            )
            for resource in root_resources:
                if resource.type == "ansible_group":
                    self._add_group(inventory, resource)
                elif resource.type == "ansible_host":
                    self._add_host(inventory, resource)

    def parse(self, inventory, loader, path, cache=False):  # type: ignore  # mypy ignore
        super(InventoryModule, self).parse(inventory, loader, path)

        cfg = self.read_config_data(path)  # type: ignore  # mypy ignore

        project_path = cfg.get("project_path", os.getcwd())
        state_file = cfg.get("state_file", "")
        search_child_modules = cfg.get("search_child_modules", True)
        terraform_binary = cfg.get("binary_path", None)
        if terraform_binary is not None:
            validate_bin_path(terraform_binary)
        else:
            try:
                terraform_binary = process.get_bin_path("terraform")
            except ValueError:
                raise AnsibleParserError("Unable to find 'terraform' binary in the path")

        # TODO: remove when ansible provider is available
        state_content = []
        if isinstance(project_path, str):
            project_path = [project_path]
        for path in project_path:
            terraform = TerraformCommands(module_run_command, path, terraform_binary, False)
            try:
                state_content.append(terraform.show(state_file))
            except TerraformWarning as e:
                raise TerraformError(e.message)

        if state_content:  # to avoid mypy error: Item "None" of "Optional[TerraformShow]" has no attribute "values"
            self.create_inventory(inventory, state_content, search_child_modules)
