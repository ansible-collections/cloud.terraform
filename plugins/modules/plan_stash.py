#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright (c) 2024, Aubin Bikouo <abikouo>
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later

DOCUMENTATION = r"""
---
module: plan_stash
version_added: 2.1.0
short_description: Handle the base64-encoding of a terraform plan file and save it into playbook execution stats.
description:
  - This module performs base64-encoding of a terraform plan file and save it into playbook execution stats similar
    to M(ansible.builtin.set_stats) module.
author:
  - "Aubin Bikouo (@abikouo)"
options:
  path:
    description:
      - The path to the terraform plan file.
    type: path
    required: true
  var_name:
    description:
      - The variable name to be set into stats.
      - Variables must start with a letter or underscore character, and contain only letters,
        numbers and underscores.
      - By default the module will set the I(terraform_plan) with the base64-encoded data of the
        terraform plan file.
    type: str
    default: terraform_plan
  per_host:
    description:
      - whether the stats are per host or for all hosts in the run.
    type: bool
    default: false
"""

EXAMPLES = r"""
- name: Encode a terraform plan file into terraform_plan variable
  cloud.terraform.plan_stash:
    path: /path/to/terraform_plan_file
    var_name: terrafrom_plan
"""

RETURN = r"""
"""

import base64

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.cloud.terraform.plugins.module_utils.plan_stash_args import PLAN_STASH_ARG_SPEC


def main() -> None:
    module = AnsibleModule(
        argument_spec=PLAN_STASH_ARG_SPEC,
        supports_check_mode=True,
    )

    terrafom_plan_file = module.params.get("path")
    var_name = module.params.get("var_name")
    per_host = module.params.get("per_host")

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
        module.fail_json(msg="Cannot encode data from file {0} due to {1}".format(terrafom_plan_file, e))

    stats = {"data": {var_name: encoded_data}, "per_host": per_host}
    module.exit_json(ansible_stats=stats, changed=False)


if __name__ == "__main__":
    main()
