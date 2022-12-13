import os
import json
from typing import List, Optional, Union, cast

from ansible_collections.cloud.terraform.plugins.module_utils.types import (
    TJsonBareValue,
    TJsonObject,
    AnsibleRunCommandType,
)
from ansible_collections.cloud.terraform.plugins.module_utils.errors import TerraformWarning, TerraformError


def get_state_args(state_file: Optional[str]) -> List[str]:
    if state_file is not None:
        if not os.path.exists(state_file):
            raise TerraformError('Could not find state_file "{0}", check the path and try again.'.format(state_file))
        return ["-state", state_file]
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
    outputs_command += get_state_args(state_file) + ([name] if name else [])
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
