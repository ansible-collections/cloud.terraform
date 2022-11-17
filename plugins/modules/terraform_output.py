#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright (c) 2017, Ryan Scott Brown <ryansb@redhat.com>
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import absolute_import, division, print_function

__metaclass__ = type

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
      - A flag to specify the output format. Defaults to -json.
      - I(name) must be provided when using -raw option.
    choices: [ json, raw ]
    default: json
    type: str
    version_added: 1.0.0
  binary_path:
    description:
      - The path of a terraform binary to use, relative to the 'service_path' unless you supply an absolute path.
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

import os
import json

from ansible.module_utils.basic import AnsibleModule

module = None  # type: AnsibleModule


def _state_args(state_file):
    if state_file and os.path.exists(state_file):
        return ["-state", state_file]
    if state_file and not os.path.exists(state_file):
        module.fail_json(
            msg='Could not find state_file "{0}", check the path and try again.'.format(
                state_file
            )
        )
    return []


def get_outputs(terraform_binary, project_path, state_file, output_format, name=None):
    outputs_command = [
        terraform_binary,
        "output",
        "-no-color",
        "-{0}".format(output_format)
    ]
    outputs_command += ([name] if name else []) + _state_args(state_file)
    rc, outputs_text, outputs_err = module.run_command(
        outputs_command, cwd=project_path
    )
    if rc == 1:
        module.warn(
            "Could not get Terraform outputs. "
            "This usually means none have been defined.\ncommand: {0}\nstdout: {1}\nstderr: {2}".format(
                outputs_command, outputs_text, outputs_err
            )
        )
        outputs = {}
    elif rc != 0:
        module.fail_json(
            msg="Failure when getting Terraform outputs. Exited {0}.\nstdout: {1}\nstderr: {2}".format(
                rc, outputs_text, outputs_err
            ),
            command=" ".join(outputs_command),
        )
    else:
        if output_format == "raw":
            return outputs_text
        outputs = json.loads(outputs_text)
    return outputs


def main():
    global module
    module = AnsibleModule(
        argument_spec=dict(
            project_path=dict(type="path"),
            name=dict(type="str"),
            format=dict(type="str", choices=["json", "raw"], default="json"),
            binary_path=dict(type="path"),
            state_file=dict(type="path"),
        ),
        required_if=[
            ("format", "raw", ("name",))
        ],
        required_one_of=[
            ("project_path", "state_file")
        ]
    )

    project_path = module.params.get("project_path")
    bin_path = module.params.get("binary_path")
    state_file = module.params.get("state_file")
    name = module.params.get("name")
    output_format = module.params.get("format")

    if bin_path is not None:
        terraform_binary = bin_path
    else:
        terraform_binary = module.get_bin_path("terraform", required=True)

    outputs = get_outputs(
        terraform_binary=terraform_binary,
        project_path=project_path,
        state_file=state_file,
        name=name,
        output_format=output_format,
    )

    if name:
        module.exit_json(value=outputs)
    else:
        module.exit_json(outputs=outputs)


if __name__ == "__main__":
    main()
