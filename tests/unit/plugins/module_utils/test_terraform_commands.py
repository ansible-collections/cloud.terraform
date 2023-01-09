from unittest.mock import MagicMock
from ansible.module_utils.compat.version import LooseVersion
from ansible_collections.cloud.terraform.plugins.module_utils.terraform_commands import TerraformCommands


class TestTerraformCommands:
    def setup_method(self):
        self.mock = MagicMock()
        self.tf = TerraformCommands(self.mock, "/project/path", "/binary/path", False)

    def test_run(self):
        args = ["apply", "-no-color", "-input=false"]
        self.tf._run(*args, check_rc=False)

        # Testing if self.run_command_fp(...) was called.
        # self.run_command_fp(...) should be called in this method,
        # therefore the test will pass if self.run_command_fp(...) was called
        self.mock.assert_called_with(["/binary/path"] + args, cwd="/project/path", check_rc=False)

    def test_apply_plan(self):
        self.mock.return_value = (0, "", "")
        self.tf._run = self.mock
        self.tf.apply_plan(
            plan_file_path=".",
            version=LooseVersion("0.15.0"),
            parallelism=0,
            lock=False,
            lock_timeout=0,
            targets=["."],
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
            ".",
            ".",
        ]

        self.mock.assert_called_with(*expected_cmd, check_rc=False)

    # Test init method; NOT __init__
    def test_init(self):
        self.tf._run = self.mock
        self.tf.init(
            backend_config={"test_val": "test"},
            backend_config_files=["."],
            reconfigure=True,
            upgrade=True,
            plugin_paths=["."],
        )

        expected_cmd = [
            "init",
            "-input=false",
            "-no-color",
            "-backend-config",
            "test_val=test",
            "-backend-config",
            ".",
            "-reconfigure",
            "-upgrade",
            "-plugin-dir",
            ".",
        ]

        self.mock.assert_called_with(*expected_cmd, check_rc=True)

    def test_plan(self):
        self.mock.return_value = (0, "", "")
        self.tf._run = self.mock
        self.tf.plan(target_plan_file_path=".", targets=["."], destroy=True, state_args=[""], variables_args=[""])

        expected_cmd = [
            "plan",
            "-lock=true",
            "-input=false",
            "-no-color",
            "-detailed-exitcode",
            "-out",
            ".",
            "-target",
            ".",
            "-destroy",
            "",
            "",
        ]

        self.mock.assert_called_with(*expected_cmd, check_rc=False)

    def test_providers_schema(self):
        self.mock.return_value = (0, '{"format_version":"1.0"}', "")
        self.tf._run = self.mock
        self.tf.providers_schema()

        expected_cmd = ["providers", "schema", "-json"]

        self.mock.assert_called_with(*expected_cmd, check_rc=False)

    def test_show(self):
        self.mock.return_value = (0, '{"format_version":"1.0"}', "")
        self.tf._run = self.mock
        self.tf.show(".")

        expected_cmd = ["show", "-json", "."]

        self.mock.assert_called_with(*expected_cmd, check_rc=False)

    def test_validate(self):
        self.tf._run = self.mock
        self.tf.validate(LooseVersion("0.15.0"), ["."])

        expected_cmd = ["validate"]

        self.mock.assert_called_with(*expected_cmd, check_rc=True)

    def test_version(self):
        extract_version = '{ \
              "terraform_version": "1.3.6", \
              "platform": "linux_amd64", \
              "provider_selections": {}, \
              "terraform_outdated": true \
            }'
        self.mock.return_value = (0, extract_version, "")
        self.tf._run = self.mock

        self.tf.version()

        expected_cmd = ["version", "-json"]
        self.mock.assert_called_with(*expected_cmd, check_rc=True)

    def test_workspace(self):
        self.tf._run = self.mock
        self.tf.workspace(self.mock.WorkspaceCommand.NEW, ".")
        expected_cmd = ["workspace", self.mock.WorkspaceCommand.NEW.value, "."]
        self.mock.assert_called_with(*expected_cmd, check_rc=True)

    def test_workspace_list(self):
        self.mock.return_value = (0, "", "")
        self.tf._run = self.mock
        self.tf.workspace_list()
        expected_cmd = ["workspace", "list", "-no-color"]
        self.mock.assert_called_with(*expected_cmd, check_rc=False)
