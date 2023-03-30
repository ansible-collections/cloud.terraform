import enum
import json
from typing import Dict, List, Tuple, cast, Optional

from ansible.module_utils.compat.version import LooseVersion

from ansible_collections.cloud.terraform.plugins.module_utils.errors import TerraformWarning, TerraformError
from ansible_collections.cloud.terraform.plugins.module_utils.models import (
    TerraformShow,
    TerraformWorkspaceContext,
    TerraformProviderSchemaCollection,
)
from ansible_collections.cloud.terraform.plugins.module_utils.types import AnsibleRunCommandType


class WorkspaceCommand(enum.Enum):
    NEW = "new"
    SELECT = "select"
    DELETE = "delete"


class TerraformCommands:
    def __init__(self, run_command_fp: AnsibleRunCommandType, project_path: str, binary_path: str, check_mode: bool):
        self.run_command_fp = run_command_fp
        self.project_path = project_path
        self.binary_path = binary_path
        self.check_mode = check_mode

    def _run(self, *args: str, check_rc: bool) -> Tuple[int, str, str]:
        return self.run_command_fp([self.binary_path] + list(args), cwd=self.project_path, check_rc=check_rc)

    def apply_plan(
        self,
        plan_file_path: str,
        version: LooseVersion,
        parallelism: Optional[int],
        lock: bool,
        lock_timeout: Optional[int],
        targets: List[str],
        needs_application: bool,
    ) -> Tuple[str, str, str]:
        command = ["apply", "-no-color", "-input=false"]
        if version < LooseVersion("0.15.0"):
            command.append("-auto-approve=true")
        else:
            command.append("-auto-approve")

        if parallelism is not None:
            command.append("-parallelism={0}".format(parallelism))

        command.append("-lock={0}".format("true" if lock else "false"))
        if lock_timeout is not None:
            command.append("-lock-timeout={0}s".format(lock_timeout))

        for t in targets:
            command.extend(["-target", t])

        command.append(plan_file_path)

        if not needs_application:
            stdout = "plan file does not need application"
            stderr = ""
        elif self.check_mode:
            stdout = "No stdout when an application is necessary in check mode."
            stderr = "No stderr when an application is necessary in check mode."
        else:
            rc, stdout, stderr = self._run(*command, check_rc=False)
            if rc != 0:
                raise TerraformError(
                    stderr.rstrip(),
                    rc=rc,
                    stdout=stdout,
                    stdout_lines=stdout.splitlines(),
                    stderr=stderr,
                    stderr_lines=stderr.splitlines(),
                    cmd=" ".join(command),
                )

        return " ".join(command), stdout, stderr

    def init(
        self,
        backend_config: Dict[str, str],
        backend_config_files: List[str],
        reconfigure: bool,
        upgrade: bool,
        plugin_paths: List[str],
    ) -> None:
        command = ["init", "-input=false", "-no-color"]
        for key, val in backend_config.items():
            command.extend(["-backend-config", "{0}={1}".format(key, val)])
        for f in backend_config_files:
            command.extend(["-backend-config", f])
        if reconfigure:
            command.extend(["-reconfigure"])
        if upgrade:
            command.extend(["-upgrade"])
        for plugin_path in plugin_paths:
            command.extend(["-plugin-dir", plugin_path])
        self._run(*command, check_rc=True)

    def plan(
        self,
        target_plan_file_path: str,
        targets: List[str],
        destroy: bool,
        state_args: List[str],
        variables_args: List[str],
    ) -> Tuple[bool, bool, str, str]:
        command = [
            "plan",
            "-lock=true",
            "-input=false",
            "-no-color",
            "-detailed-exitcode",
            "-out",
            target_plan_file_path,
        ]
        for t in targets:
            command.extend(["-target", t])
        if destroy:
            command.append("-destroy")
        command.extend(state_args)
        command.extend(variables_args)

        rc, stdout, stderr = self._run(*command, check_rc=False)

        if rc == 0:
            # no changes
            changed = False
        elif rc == 1:
            # failure to plan
            raise TerraformError(
                "Terraform plan could not be created\nSTDOUT: {out}\nSTDERR: {err}\nCOMMAND: {cmd}".format(
                    out=stdout,
                    err=stderr,
                    cmd=" ".join(command),
                )
            )
        elif rc == 2:
            # changes, but successful
            changed = True
        else:
            raise TerraformError(
                "Terraform plan failed with unexpected exit code {rc}.\n"
                "STDOUT: {out}\nSTDERR: {err}\nCOMMAND: {cmd}".format(
                    rc=rc,
                    out=stdout,
                    err=stderr,
                    cmd=" ".join(command),
                )
            )

        if "- destroy" in stdout:
            any_destroyed = True
        else:
            any_destroyed = False

        return changed, any_destroyed, stdout, stderr

    # requires init to function
    def providers_schema(self) -> TerraformProviderSchemaCollection:
        # in the command we have "providers schema", in the schema we have "provider_schemas"
        command = ["providers", "schema", "-json"]
        rc, text, err = self._run(*command, check_rc=False)
        if rc == 1:
            raise TerraformWarning("Could not get provider schemas. " "\nstdout: {0}\nstderr: {1}".format(text, err))
        elif rc != 0:
            raise TerraformError(
                "Failure when getting provider schemas. " "Exited {0}.\nstdout: {1}\nstderr: {2}".format(rc, text, err),
                command=" ".join(command),
            )
        result = TerraformProviderSchemaCollection.from_json(json.loads(text))
        return result

    def show(self, state_or_plan_file_path: str) -> Optional[TerraformShow]:
        command = ["show", "-json", state_or_plan_file_path]
        rc, stdout, stderr = self._run(*command, check_rc=False)
        if rc == 1:
            raise TerraformWarning(
                "Could not get Terraform show from file: {0}. "
                "\nstdout: {1}\nstderr: {2}".format(state_or_plan_file_path, stdout, stderr)
            )
        elif rc != 0:
            raise TerraformError(
                "Failure when getting Terraform show output from file: {0}. "
                "Exited {1}.\nstdout: {2}\nstderr: {3}".format(state_or_plan_file_path, rc, stdout, stderr),
                command=" ".join(command),
            )
        state_json = json.loads(stdout)

        # when not initialized, this doesn't return anything useful, but also not an error
        # this is not an exceptional case in our usage, so no warning
        if len(state_json.keys()) == 1 and "format_version" in state_json:
            return None

        # handle the difference between showing a state and a plan by preprocessing the differences
        if "planned_values" in state_json:
            result = {
                key: value
                for key, value in state_json.items()
                if key
                in [
                    "format_version",
                    "terraform_version",
                    "planned_values",
                ]
            }
            # renaming planned_values to values for filtering
            result["values"] = result.pop("planned_values")
        else:
            # no changes necessary
            result = state_json

        return TerraformShow.from_json(result)

    def validate(self, version: LooseVersion, variables_args: List[str]) -> None:
        command = ["validate", "-no-color"]
        if version < LooseVersion("0.15.0"):
            command += variables_args
        self._run(*command, check_rc=True)

    def version(self) -> LooseVersion:
        rc, extract_version, stderr = self._run("version", "-json", check_rc=True)
        terraform_version = cast(str, (json.loads(extract_version))["terraform_version"])
        return LooseVersion(terraform_version)

    def workspace(self, command: WorkspaceCommand, workspace: str) -> None:
        self._run("workspace", command.value, workspace, check_rc=True)

    def workspace_list(self) -> TerraformWorkspaceContext:
        rc, out, err = self._run("workspace", "list", "-no-color", check_rc=False)
        current_workspace = "default"
        all_workspaces: List[str] = []
        if rc != 0:
            raise TerraformWarning("Failed to list Terraform workspaces:\n{0}".format(err))
        for item in out.split("\n"):
            stripped_item = item.strip()
            if not stripped_item:
                continue
            elif stripped_item.startswith("* "):
                current_workspace = stripped_item.replace("* ", "")
            else:
                all_workspaces.append(stripped_item)
        return TerraformWorkspaceContext(current=current_workspace, all=all_workspaces)
