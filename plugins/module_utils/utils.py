import json
import os
import shutil
from typing import List, Optional, Union, cast

from ansible.module_utils.common.text.converters import to_text
from ansible.module_utils.compat.version import LooseVersion
from ansible_collections.cloud.terraform.plugins.module_utils.errors import TerraformError, TerraformWarning
from ansible_collections.cloud.terraform.plugins.module_utils.terraform_commands import TerraformCommands
from ansible_collections.cloud.terraform.plugins.module_utils.types import (
    AnsibleRunCommandType,
    TJsonBareValue,
    TJsonList,
    TJsonObject,
)


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
    workspace: Optional[str] = None,
) -> Union[TJsonObject, TJsonBareValue]:
    outputs_command = [terraform_binary, "output", "-no-color", "-{0}".format(output_format)]
    outputs_command += get_state_args(state_file) + ([name] if name else [])
    if workspace:
        tf_env = {"TF_WORKSPACE": workspace}
        rc, outputs_text, outputs_err = run_command_fp(outputs_command, cwd=project_path, environ_update=tf_env)
    else:
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


def validate_project_path(project_path: str) -> None:
    if project_path is None or "/" not in project_path:
        raise TerraformError("Path for Terraform project can not be None or ''.")

    if not os.path.isdir(project_path):
        raise TerraformError(
            "Path for Terraform project '{0}' doesn't exist on this host - check the path and try again please.".format(
                project_path
            )
        )


def validate_bin_path(bin_path: str) -> None:
    if not shutil.which(bin_path):
        raise TerraformError(
            "Path for Terraform binary '{0}' doesn't exist on this host - check the path and try again please.".format(
                bin_path
            )
        )


def preflight_validation(
    terraform: TerraformCommands,
    bin_path: str,
    project_path: str,
    version: LooseVersion,
    variables_args: List[str],
) -> None:
    validate_project_path(project_path)
    validate_bin_path(bin_path)
    terraform.validate(version, variables_args)


def _convert_value_to_hcl(value: TJsonBareValue) -> str:
    """Convert variable into HCL
    1 -> 1, "some" -> "some", True -> true
    """
    if isinstance(value, bool):
        return str(to_text(value).lower())
    if isinstance(value, str):
        return f"<<EOF\n{value}\nEOF" if "\n" in value else f'"{value}"'
    return str(to_text(value))


def ansible_dict_to_hcl(data: Union[TJsonObject, TJsonBareValue, TJsonList], object_key: Optional[str] = None) -> str:
    """Convert python dict to HCL (HashiCorp configuration language.)
    https://github.com/hashicorp/hcl

    :param data: ansible dict
    :param object_key: The object key
    :return: HCL formatted string
    """
    result = []
    if isinstance(data, dict):
        result.append(object_key + " {" if object_key else "{")
        result += [ansible_dict_to_hcl(val, key) for key, val in data.items()]
        result.append("}")
    elif isinstance(data, list):
        value = object_key + " = [" if object_key else "["
        value += ", ".join([ansible_dict_to_hcl(v) for v in data]) + "]"
        result.append(value)
    else:
        value = ""
        if object_key:
            value += f"{object_key} = "
        value += _convert_value_to_hcl(data)
        result.append(value)

    return "\n".join(result)
