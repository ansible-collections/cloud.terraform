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
import json
import requests

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

TESTING_STATE_FILE = os.environ.get("TESTING_STATE_FILE", False)

GITLAB_API_URL = "https://gitlab.example.com/api/v4"
GITLAB_PROJECT_ID = "<your_gitlab_project_id>"
GITLAB_STATE_NAME = "<your_gitlab_state_name>"
GITLAB_ACCESS_TOKEN = "<your_gitlab_personal_access_token>"


def module_run_command(cmd: List[str], cwd: str, check_rc: bool) -> Tuple[int, str, str]:
    completed_process = subprocess.run(cmd, capture_output=True, check=check_rc, cwd=cwd)
    return (
        completed_process.returncode,
        completed_process.stdout.decode("utf-8"),
        completed_process.stderr.decode("utf-8"),
    )


def get_gitlab_tfstate() -> str:
    url = f"{GITLAB_API_URL}/projects/{GITLAB_PROJECT_ID}/terraform/state/{GITLAB_STATE_NAME}"
    headers = {"Private-Token": GITLAB_ACCESS_TOKEN}
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        raise TerraformError(f"Error fetching Terraform state from GitLab: {response.content.decode('utf-8')}")

    return response.content.decode("utf-8")


def put_gitlab_tfstate(tfstate: str) -> None:
    url = f"{GITLAB_API_URL}/projects/{GITLAB_PROJECT_ID}/terraform/state/{GITLAB_STATE_NAME}"
    headers = {"Private-Token": GITLAB_ACCESS_TOKEN, "Content-Type": "application/json"}
    response = requests.put(url, headers=headers, data=tfstate)

    if response.status_code != 200:
        raise TerraformError(f"Error uploading Terraform state to GitLab: {response.content.decode('utf-8')}")


class InventoryModule(BaseInventoryPlugin):
    NAME = "terraform_provider"

    def read_config_data(self, path):
        try:
            with open(path, "r") as inventory_src:
                cfg = yaml.safe_load(inventory_src)
            return cfg
        except Exception as e:
            raise AnsibleParserError(e)

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

    def parse(self, inventory, loader, path, cache=False):
        super(InventoryModule, self).parse(inventory, loader, path)

        cfg = self.read_config_data(path)

        project_path = cfg.get("project_path", os.getcwd())
        state_file = cfg.get("state_file", "terraform.tfstate")
        terraform_binary = cfg.get("binary_path", None)
        if terraform_binary is not None:
            validate_bin_path(terraform_binary)
        else:
            terraform_binary = process.get_bin_path("terraform", required=True)

        terraform = TerraformCommands(module_run_command, project_path, terraform_binary, False)

        # Fetch state from GitLab
        gitlab_tfstate = get_gitlab_tfstate()

        # Save fetched state to a temporary file
        with open("temp.tfstate", "w") as temp_state_file:
            temp_state_file.write(gitlab_tfstate)

        try:
            state_content = terraform.show("temp.tfstate")
        except TerraformWarning as e:
            raise TerraformError(e.message)
        finally:
            os.remove("temp.tfstate")

        if state_content:
            self.create_inventory(inventory, state_content)
