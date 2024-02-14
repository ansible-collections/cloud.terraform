#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright (c) 2024, Aubin Bikouo <abikouo@redhat.com>
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later

DOCUMENTATION = r"""
---
module: plan_stash
version_added: 2.1.0
short_description: Handle the base64 encoding or decoding of a terraform plan file.
description:
  - This module performs base64-encoding of a terraform plan file and saves it into playbook execution stats similar
    to M(ansible.builtin.set_stats) module.
  - The module also performs base64-decoding of a terraform plan file from a variable defined into ansible facts and writes them
    into a file specified by the user.
author:
  - "Aubin Bikouo (@abikouo)"
options:
  state:
    description:
      - "O(state=stash): base64-encodes the terraform plan file and saves it into ansible stats like using the M(ansible.builtin.set_stats) module."
      - "O(state=load): base64-decodes data from variable specified in O(var_name) and writes them into terraform plan file."
    choices: [stash, load]
    default: stash
    type: str
  path:
    description:
      - The path to the terraform plan file.
    type: path
    required: true
  var_name:
    description:
      - When O(state=stash), this parameter defines the variable name to be set into stats.
      - When O(state=load), this parameter defines the variable from ansible facts containing
        the base64-encoded data of the terraform plan file.
      - Variables must start with a letter or underscore character, and contain only letters,
        numbers and underscores.
      - The module will use V(terraform_plan) as default variable name if not specified.
    type: str
  binary_data:
    description:
      - When O(state=load), this parameter defines the base64-encoded data of the terraform plan file.
      - Mutually exclusive with V(var_name).
      - Ignored when O(state=stash).
    type: raw
  per_host:
    description:
      - Whether the stats are per host or for all hosts in the run.
      - Ignored when O(state=load).
    type: bool
    default: false
notes:
  - For security reasons, this module should be used with O(no_log=true) and O(register) functionalities
    as the plan file can contain unencrypted secrets.
"""

EXAMPLES = r"""
# Encode terraform plan file into default variable 'terraform_plan'
- name: Encode a terraform plan file into terraform_plan variable
  cloud.terraform.plan_stash:
    path: /path/to/terraform_plan_file
    state: stash

# Encode terraform plan file into variable 'stashed_plan'
- name: Encode a terraform plan file into terraform_plan variable
  cloud.terraform.plan_stash:
    path: /path/to/terraform_plan_file
    var_name: stashed_plan
    state: stash

# Load terraform plan file from variable 'stashed_plan'
- name: Load a terraform plan file data from variable 'stashed_plan' into file 'tfplan'
  cloud.terraform.plan_stash:
    path: tfplan
    var_name: stashed_plan
    state: load

# Load terraform plan file from binary data
- name: Load a terraform plan file data from binary data
  cloud.terraform.plan_stash:
    path: tfplan
    binary_data: "{{ terraform_binary_data }}"
    state: load
"""

RETURN = r"""
"""

import base64

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.cloud.terraform.plugins.module_utils.plan_stash_args import PLAN_STASH_ARG_SPEC


def read_file_content(file_path: str, module: AnsibleModule, failed_on_error: bool = True) -> bytes:
    data = b""
    try:
        with open(file_path, "rb") as f:
            data = f.read()
    except FileNotFoundError:
        if failed_on_error:
            module.fail_json(msg="The following file '{0}' does not exist.".format(file_path))
    return data


def main() -> None:
    module = AnsibleModule(
        argument_spec=PLAN_STASH_ARG_SPEC,
        supports_check_mode=True,
    )

    terrafom_plan_file = module.params.get("path")
    var_name = module.params.get("var_name")
    per_host = module.params.get("per_host")
    state = module.params.get("state")

    result = {}
    if state == "stash":
        # Stash: base64-encode the terraform plan file and set stats
        data = b""
        try:
            with open(terrafom_plan_file, "rb") as f:
                data = f.read()
        except FileNotFoundError:
            module.fail_json(msg="The following file '{0}' does not exist.".format(terrafom_plan_file))

        if not data:
            module.fail_json(msg="The following file '{0}' is empty.".format(terrafom_plan_file))

        # encode binary data
        try:
            encoded_data = base64.b64encode(data)
        except Exception as e:
            module.fail_json(msg="Cannot encode data from file {0} due to: {1}".format(terrafom_plan_file, e))

        stats = {"data": {var_name: encoded_data}, "per_host": per_host}
        result = {"ansible_stats": stats, "changed": False}
    else:
        # Load: Decodes the data from the variable name and write into terraform plan file
        binary_data = module.params.get("binary_data")
        try:
            data = base64.b64decode(binary_data)
        except Exception as e:
            module.fail_json(msg="Failed to decode binary data due to: {0}".format(e))

        current_content = read_file_content(terrafom_plan_file, module, failed_on_error=False)
        changed = False
        if current_content != data:
            changed = True
            if not module.check_mode:
                try:
                    with open(terrafom_plan_file, "wb") as f:
                        f.write(data)
                    result.update({"msg": "data successfully decoded into file %s" % terrafom_plan_file})
                except Exception as e:
                    module.fail_json(msg="Failed to write data into file due to: {0}".format(e))

        result.update({"changed": changed})

    module.exit_json(**result)


if __name__ == "__main__":
    main()
