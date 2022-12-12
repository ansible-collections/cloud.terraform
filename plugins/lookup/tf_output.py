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
from typing import Optional, List, Union, cast, Tuple, Dict

from ansible.plugins.lookup import LookupBase
from ansible.module_utils.common import process
from ansible_collections.cloud.terraform.plugins.module_utils.types import (
    AnyJsonType,
    TJsonBareValue,
    TJsonObject,
    AnsibleRunCommandType,
)
from ansible_collections.cloud.terraform.plugins.module_utils.errors import TerraformWarning, TerraformError


def _state_args(state_file: Optional[str]) -> List[str]:
    if state_file and os.path.exists(state_file):
        return ["-state", state_file]
    if state_file and not os.path.exists(state_file):
        raise TerraformError('Could not find state_file "{0}", check the path and try again.'.format(state_file))
    return []


def get_outputs(
    run_command_fp: AnsibleRunCommandType,
    terraform_binary: str,
    project_path: Optional[str],
    state_file: Optional[str],
    output_format: str,
    name: Optional[str] = None,
) -> Union[TJsonObject, TJsonBareValue]:
    outputs_command = [terraform_binary, "output", "-no-color", "-{0}".format(output_format)]
    outputs_command += _state_args(state_file) + ([name] if name else [])
    rc, outputs_text, outputs_err = run_command_fp(outputs_command, cwd=project_path)
    if rc == 1:
        message = (
            "Could not get Terraform outputs. "
            "This usually means none have been defined.\ncommand: {0}\nstdout: {1}\nstderr: {2}".format(
                outputs_command, outputs_text, outputs_err
            )
        )
        raise TerraformWarning(message)
    elif rc != 0:
        message = "Failure when getting Terraform outputs. Exited {0}.\nstdout: {1}\nstderr: {2}".format(
            rc, outputs_text, outputs_err
        )
        raise TerraformError(message, command=" ".join(outputs_command))
    else:
        if output_format == "raw":
            return cast(TJsonObject, outputs_text)
        else:
            outputs = cast(TJsonObject, json.loads(outputs_text))
            return outputs


# no module available here, mock functionality to be consistent throughout the rest of the codebase
def module_run_command(cmd: List[str], cwd: str) -> Tuple[int, str, str]:
    completed_process = subprocess.run(cmd, capture_output=True, check=False, cwd=cwd)
    return (
        completed_process.returncode,
        completed_process.stdout.decode("utf-8"),
        completed_process.stderr.decode("utf-8"),
    )


class LookupModule(LookupBase):  # type: ignore  # cannot subclass without available type (implicitly Any)
    def run(self, terms: List[str], variables: Optional[Dict[str, str]] = None, **kwargs: str) -> List[AnyJsonType]:
        self.set_options(var_options=variables, direct=kwargs)
        project_path = self.get_option("project_path")
        state_file = self.get_option("state_file")
        bin_path = self.get_option("binary_path")

        if bin_path is not None:
            terraform_binary = bin_path
        else:
            terraform_binary = process.get_bin_path("terraform", required=True)

        output: List[AnyJsonType] = []
        if not terms:
            output.append(
                get_outputs(module_run_command, terraform_binary, project_path, state_file, output_format="json")
            )
        else:
            for term in terms:
                value = get_outputs(
                    module_run_command, terraform_binary, project_path, state_file, name=term, output_format="json"
                )
                output.append(value)
        return output
