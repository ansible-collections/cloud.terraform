#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright (c) 2017, Ryan Scott Brown <ryansb@redhat.com>
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later

# language=yaml
DOCUMENTATION = r"""
---
module: terraform_output
short_description: Returns Terraform module outputs.
description:
  - Returns Terraform module outputs.
options:
  project_path:
    description:
      - The path to the root of the Terraform directory with the .tfstate file.
    type: path
    version_added: 1.0.0
  name:
    description:
      - Name of an individual output in the state file to list.
    type: str
    version_added: 1.0.0
  format:
    description:
      - A flag to specify the output format. Defaults to C(json).
      - I(name) must be provided when using C(raw) option.
    choices: [ json, raw ]
    default: json
    type: str
    version_added: 1.0.0
  binary_path:
    description:
      - The path of a terraform binary to use.
    type: path
    version_added: 1.0.0
  state_file:
    description:
      - Absolute path to an existing Terraform state file whose outputs will be listed.
      - If this is not specified, the default C(terraform.tfstate) in the directory I(project_path) will be used.
    type: path
    version_added: 1.0.0
requirements: [ "terraform" ]
author: "Polona Mihalič (@PolonaM)"
"""

# language=yaml
EXAMPLES = """
- name: List outputs from terraform.tfstate in project_dir
  cloud.terraform.terraform_output:
    project_path: project_dir

- name: List outputs from selected state file in project_dir
  cloud.terraform.terraform_output:
    state_file: state_file

- name: List outputs from terraform.tfstate in project_dir, use different Terraform version
  cloud.terraform.terraform_output:
    project_path: project_dir
    binary_path: terraform_binary

- name: List value of an individual output from terraform.tfstate in project_dir
  cloud.terraform.terraform_output:
    project_path: project_dir
    name: individual_output

- name: List value of an individual output in raw format
  cloud.terraform.terraform_output:
    project_path: project_dir
    name: individual_output
    format: raw
"""

# language=yaml
RETURN = """
outputs:
  type: dict
  description: A dictionary of all the TF outputs by their assigned name. Use C(.outputs.MyOutputName.value) to access the value.
  returned: when name is not specified
  sample: '{"bukkit_arn": {"sensitive": false, "type": "string", "value": "arn:aws:s3:::tf-test-bukkit"}'
  contains:
    sensitive:
      type: bool
      returned: always
      description: Whether Terraform has marked this value as sensitive
    type:
      type: str
      returned: always
      description: The type of the value (string, int, etc)
    value:
      type: str
      returned: always
      description: The value of the output as interpolated by Terraform
value:
  type: str
  description: A single value requested by the module using the "name" parameter
  sample: "myvalue"
  returned: when name is specified
"""


from typing import Optional

from ansible.module_utils.basic import AnsibleModule

from ansible_collections.cloud.terraform.plugins.module_utils.errors import TerraformWarning, TerraformError
from ansible_collections.cloud.terraform.plugins.module_utils.utils import (
    get_outputs,
    validate_project_path,
    validate_bin_path,
)


def main() -> None:
    module = AnsibleModule(
        argument_spec=dict(
            project_path=dict(type="path"),
            name=dict(type="str"),
            format=dict(type="str", choices=["json", "raw"], default="json"),
            binary_path=dict(type="path"),
            state_file=dict(type="path"),
        ),
        required_if=[("format", "raw", ("name",))],
        required_one_of=[("project_path", "state_file")],
    )

    project_path: Optional[str] = module.params.get("project_path")
    bin_path: Optional[str] = module.params.get("binary_path")
    state_file: Optional[str] = module.params.get("state_file")
    name: Optional[str] = module.params.get("name")
    output_format: str = module.params.get("format")

    if bin_path is not None:
        terraform_binary = bin_path
    else:
        terraform_binary = module.get_bin_path("terraform", required=True)
    validate_bin_path(terraform_binary)

    try:
        outputs = get_outputs(
            module.run_command,
            terraform_binary=terraform_binary,
            project_path=project_path,
            state_file=state_file,
            name=name,
            output_format=output_format,
        )
    except TerraformWarning as e:
        module.warn(e.message)
    except TerraformError as e:
        e.fail_json(module)

    if name:
        module.exit_json(value=outputs)
    else:
        module.exit_json(outputs=outputs)


if __name__ == "__main__":
    main()
