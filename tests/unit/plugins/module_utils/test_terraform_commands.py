from unittest.mock import MagicMock

import pytest
from ansible.module_utils.compat.version import LooseVersion
from ansible_collections.cloud.terraform.plugins.module_utils.terraform_commands import (
    TerraformCommands,
    WorkspaceCommand,
)


class TestTerraformCommands:
    def setup_method(self):
        self.mock = MagicMock()
        self.tf = TerraformCommands(self.mock, "/project/path", "/binary/path", False)
        self.rc, self.stdout, self.stderr = 0, "", ""

    def test_run(self):
        args = ["apply", "-no-color", "-input=false"]
        self.tf._run(*args, check_rc=False)

        # Testing if self.run_command_fp(...) was called.
        # self.run_command_fp(...) should be called in this method,
        # therefore the test will pass if self.run_command_fp(...) was called
        self.mock.assert_called_with(["/binary/path"] + args, cwd="/project/path", check_rc=False)

    def test_apply_plan(self):
        self.mock.return_value = (self.rc, self.stdout, self.stderr)
        self.tf._run = self.mock
        self.tf.apply_plan(
            plan_file_path="/plan/path",
            version=LooseVersion("0.15.0"),
            parallelism=0,
            lock=False,
            lock_timeout=0,
            targets=["target_file"],
            needs_application=True,
        )

        # Expected command to be called with self._run(...)
        expected_cmd = [
            "apply",
            "-no-color",
            "-input=false",
            "-auto-approve",
            "-parallelism=0",
            "-lock=false",
            "-lock-timeout=0s",
            "-target",
            "target_file",
            "/plan/path",
        ]

        self.mock.assert_called_with(*expected_cmd, check_rc=False)

    # Test init method; NOT __init__
    def test_init(self):
        self.tf._run = self.mock
        self.tf.init(
            backend_config={"test_val": "test"},
            backend_config_files=["config_file"],
            reconfigure=True,
            upgrade=True,
            plugin_paths=["/plugin/path"],
        )

        expected_cmd = [
            "init",
            "-input=false",
            "-no-color",
            "-backend-config",
            "test_val=test",
            "-backend-config",
            "config_file",
            "-reconfigure",
            "-upgrade",
            "-plugin-dir",
            "/plugin/path",
        ]

        self.mock.assert_called_with(*expected_cmd, check_rc=True)

    def test_plan(self):
        self.mock.return_value = (self.rc, self.stdout, self.stderr)
        self.tf._run = self.mock
        self.tf.plan(
            target_plan_file_path="/target/plan/file",
            targets=["target_file"],
            destroy=True,
            state_args=["state_arg"],
            variables_args=["var_arg"],
        )

        expected_cmd = [
            "plan",
            "-lock=true",
            "-input=false",
            "-no-color",
            "-detailed-exitcode",
            "-out",
            "/target/plan/file",
            "-target",
            "target_file",
            "-destroy",
            "state_arg",
            "var_arg",
        ]

        self.mock.assert_called_with(*expected_cmd, check_rc=False)

    def test_providers_schema(self):
        self.stdout = '{"format_version":"1.0"}'
        self.mock.return_value = (self.rc, self.stdout, self.stderr)
        self.tf._run = self.mock
        self.tf.providers_schema()

        expected_cmd = ["providers", "schema", "-json"]

        self.mock.assert_called_with(*expected_cmd, check_rc=False)

    def test_show(self):
        self.stdout = '{"format_version":"1.0"}'
        self.mock.return_value = (self.rc, self.stdout, self.stderr)
        self.tf._run = self.mock
        self.tf.show("/state/or/plan/file")

        expected_cmd = ["show", "-json", "/state/or/plan/file"]

        self.mock.assert_called_with(*expected_cmd, check_rc=False)

    def test_validate(self):
        self.tf._run = self.mock
        self.tf.validate(LooseVersion("0.15.0"), ["var_arg"])

        expected_cmd = ["validate"]

        self.mock.assert_called_with(*expected_cmd, check_rc=True)

    def test_version(self):
        self.stdout = '{ \
              "terraform_version": "1.3.6", \
              "platform": "linux_amd64", \
              "provider_selections": {}, \
              "terraform_outdated": true \
            }'
        self.mock.return_value = (self.rc, self.stdout, self.stderr)
        self.tf._run = self.mock

        self.tf.version()

        expected_cmd = ["version", "-json"]
        self.mock.assert_called_with(*expected_cmd, check_rc=True)

    @pytest.mark.parametrize(
        "test_workspace_cmd, expected_workspace_cmd_value",
        [(WorkspaceCommand.NEW, "new"), (WorkspaceCommand.SELECT, "select"), (WorkspaceCommand.DELETE, "delete")],
    )
    def test_workspace(self, test_workspace_cmd, expected_workspace_cmd_value):
        self.tf._run = self.mock
        self.tf.workspace(test_workspace_cmd, "/workspace/path")
        expected_cmd = ["workspace", expected_workspace_cmd_value, "/workspace/path"]
        self.mock.assert_called_with(*expected_cmd, check_rc=True)

    def test_workspace_list(self):
        self.mock.return_value = (self.rc, self.stdout, self.stderr)
        self.tf._run = self.mock
        self.tf.workspace_list()
        expected_cmd = ["workspace", "list", "-no-color"]
        self.mock.assert_called_with(*expected_cmd, check_rc=False)
