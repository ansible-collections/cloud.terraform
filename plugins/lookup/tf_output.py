# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

# language=yaml
DOCUMENTATION = """
name: tf_output
author: Polona Mihalič (@PolonaM)
version_added: 1.0.0
short_description: Read state file outputs.
description:
  - This lookup returns all outputs or selected output in state file.
options:
  _terms:
    description:
      - Name(s) of the output(s) to return.
      - If value is not set, all outputs will be returned in a dictionary.
    type: str
  project_path:
    description:
      - The path to the root of the Terraform directory with the terraform.tfstate file.
      - If I(state_file) and I(project_path) are not specified, the C(terraform.tfstate) file in the
        current working directory will be used.
      - The C(TF_DATA_DIR) environment variable is respected.
    type: path
  state_file:
    description:
      - Absolute path to an existing Terraform state file whose outputs will be listed.
      - If I(state_file) and I(project_path) are not specified, the C(terraform.tfstate) file in the
        current working directory will be used.
      - The C(TF_DATA_DIR) environment variable is respected.
    type: path
  binary_path:
    description:
      - The path of a terraform binary to use.
    type: path
"""

# language=yaml
EXAMPLES = """
- name: get selected output from terraform.tfstate
  ansible.builtin.debug:
    msg: "{{ lookup('cloud.terraform.tf_output', 'my_output1', project_path='path/to/project/dir/') }}"

- name: get all outputs from custom state file
  ansible.builtin.debug:
    msg: "{{ lookup('cloud.terraform.tf_output', state_file='path/to/custom/state/file') }}"

- name: get all outputs from terraform.tfstate in cwd
  ansible.builtin.debug:
    msg: "{{ lookup('cloud.terraform.tf_output') }}"
"""

# language=yaml
RETURN = """
_outputs:
  description:
    - A list of dict that contains all outputs.
  returned: when _terms is not specified
  type: list
  elements: dict
_value:
  description:
    - A list of selected output's value.
  returned: when name(s) of the output(s) is specified
  type: list
  elements: str
"""


import os
import json
import subprocess
from ansible.errors import AnsibleLookupError
from ansible.plugins.lookup import LookupBase
from ansible.module_utils.common import process


def _state_args(state_file):
    if state_file:
        if not os.path.exists(state_file):
            raise AnsibleLookupError(
                'Could not find state_file "{0}", check the path and try again.'.format(state_file)
            )
        return ["-state", state_file]
    return []


def get_outputs(terraform_binary, project_path, state_file, name=None):
    outputs_command = [
        terraform_binary,
        "output",
        "-no-color",
        "-json",
    ]
    outputs_command += _state_args(state_file) + ([name] if name else [])
    completed_process = subprocess.run(outputs_command, cwd=project_path, capture_output=True, check=False)

    if completed_process.returncode != 0:
        raise AnsibleLookupError(
            "Failure when getting Terraform outputs. Exited {0}.\nstdout: {1}\nstderr: {2}".format(
                completed_process.returncode, completed_process.stdout, completed_process.stderr
            )
        )

    return json.loads(completed_process.stdout)


class LookupModule(LookupBase):
    def run(self, terms, variables=None, **kwargs):
        self.set_options(var_options=variables, direct=kwargs)
        project_path = self.get_option("project_path")
        state_file = self.get_option("state_file")
        bin_path = self.get_option("binary_path")

        if bin_path is not None:
            terraform_binary = bin_path
        else:
            terraform_binary = process.get_bin_path("terraform", required=True)

        output = []
        if not terms:
            output.append(get_outputs(terraform_binary, project_path, state_file))
        else:
            for term in terms:
                value = get_outputs(terraform_binary, project_path, state_file, name=term)
                output.append(value)
        return output
