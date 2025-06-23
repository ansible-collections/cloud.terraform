# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or https://www.gnu.org/licenses/gpl-3.0.txt)

# language=yaml
DOCUMENTATION = """
name: tf_output
author: Polona Mihalič (@PolonaM)
version_added: 1.0.0
short_description: Reads state file outputs.
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
      - The path to an existing Terraform state file whose outputs will be listed.
      - If I(state_file) and I(project_path) are not specified, the C(terraform.tfstate) file in the
        current working directory will be used.
      - The C(TF_DATA_DIR) environment variable is respected.
      - This option is not comptabile for remote states.
    type: path
  binary_path:
    description:
      - The path of a terraform binary to use.
    type: path
  workspace:
    description:
      - The terraform workspace to work with.
    type: str
    version_added: 1.2.0
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

- name: get all outputs from terraform.tfstate in workspace 'dev'
  ansible.builtin.debug:
    msg: "{{ lookup('cloud.terraform.tf_output', workspace='dev') }}"
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
import subprocess
from typing import Dict, List, Optional, Tuple

from ansible.module_utils.common import process
from ansible.plugins.lookup import LookupBase
from ansible_collections.cloud.terraform.plugins.module_utils.types import AnyJsonType
from ansible_collections.cloud.terraform.plugins.module_utils.utils import get_outputs


# no module available here, mock functionality to be consistent throughout the rest of the codebase
def module_run_command(
    cmd: List[str], cwd: str, environ_update: Optional[Dict[str, str]] = None
) -> Tuple[int, str, str]:
    env = os.environ.copy()
    env.update(environ_update or {})
    completed_process = subprocess.run(cmd, capture_output=True, check=False, cwd=cwd, env=env)
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
        workspace = self.get_option("workspace")

        if bin_path is not None:
            terraform_binary = bin_path
        else:
            terraform_binary = process.get_bin_path("terraform", required=True)

        output: List[AnyJsonType] = []
        if not terms:
            output.append(
                get_outputs(
                    module_run_command,
                    terraform_binary,
                    project_path,
                    state_file,
                    output_format="json",
                    workspace=workspace,
                )
            )
        else:
            for term in terms:
                value = get_outputs(
                    module_run_command,
                    terraform_binary,
                    project_path,
                    state_file,
                    name=term,
                    output_format="json",
                    workspace=workspace,
                )
                output.append(value)
        return output
