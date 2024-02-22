# -*- coding: utf-8 -*-
# Copyright: (c) 2022, XLAB Steampunk <steampunk@xlab.si>
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)


import pytest
from ansible.module_utils import basic
from ansible_collections.cloud.terraform.plugins.module_utils.errors import TerraformError, TerraformWarning
from ansible_collections.cloud.terraform.plugins.modules import terraform_output
from ansible_collections.cloud.terraform.tests.unit.plugins.modules.utils import (
    AnsibleExitJson,
    AnsibleFailJson,
    exit_json,
    fail_json,
    set_module_args,
)


class TestTerraformOutputMain:
    def test_return_selected_output(self, mocker):
        mocker.patch.multiple(basic.AnsibleModule, exit_json=exit_json, fail_json=fail_json)
        set_module_args(
            {
                "project_path": "path/to/project",
                "name": "my_output",
                "format": "json",
                "binary_path": "terraform/binary/path",
                "state_file": "mystate.tfstate",
            }
        )
        mocker.patch("ansible_collections.cloud.terraform.plugins.modules.terraform_output.validate_bin_path")
        mocker.patch(
            "ansible_collections.cloud.terraform.plugins.modules.terraform_output.get_outputs"
        ).return_value = "my_output_value"

        with pytest.raises(AnsibleExitJson) as exc:
            terraform_output.main()

        assert exc.value.args[0]["value"] == "my_output_value"

    def test_return_all_outputs(self, mocker):
        mocker.patch.multiple(basic.AnsibleModule, exit_json=exit_json, fail_json=fail_json)
        set_module_args(
            {
                "project_path": "path/to/project",
                "format": "json",
                "binary_path": "terraform/binary/path",
                "state_file": "mystate.tfstate",
            }
        )
        mocker.patch("ansible_collections.cloud.terraform.plugins.modules.terraform_output.validate_bin_path")
        mocker.patch(
            "ansible_collections.cloud.terraform.plugins.modules.terraform_output.get_outputs"
        ).return_value = {"my_output": {"sensitive": False, "type": "string", "value": "file generated"}}

        with pytest.raises(AnsibleExitJson) as exc:
            terraform_output.main()

        assert exc.value.args[0]["outputs"] == {
            "my_output": {"sensitive": False, "type": "string", "value": "file generated"}
        }

    def test_required_if(self, mocker):
        mocker.patch.multiple(basic.AnsibleModule, exit_json=exit_json, fail_json=fail_json)
        set_module_args(
            {
                "project_path": "path/to/project",
                "format": "raw",
                "binary_path": "terraform/binary/path",
                "state_file": "mystate.tfstate",
            }
        )
        mocker.patch("ansible_collections.cloud.terraform.plugins.modules.terraform_output.validate_bin_path")
        mocker.patch("ansible_collections.cloud.terraform.plugins.modules.terraform_output.get_outputs")

        with pytest.raises(AnsibleFailJson) as exc:
            terraform_output.main()

        assert exc.value.args[0]["msg"] == "format is raw but all of the following are missing: name"

    def test_except_terraform_warning(self, mocker):
        mocker.patch.multiple(basic.AnsibleModule, exit_json=exit_json, fail_json=fail_json)
        set_module_args(
            {
                "project_path": "path/to/project",
                "name": "my_output",
                "format": "json",
                "binary_path": "terraform/binary/path",
                "state_file": "mystate.tfstate",
            }
        )
        mocker.patch("ansible_collections.cloud.terraform.plugins.modules.terraform_output.validate_bin_path")
        mocker.patch("ansible_collections.cloud.terraform.plugins.modules.terraform_output.get_outputs").side_effect = (
            TerraformWarning("Could not get Terraform outputs.")
        )

        with pytest.raises(AnsibleExitJson) as exc:
            terraform_output.main()

        assert exc.value.args[0]["value"] is None

    def test_except_terraform_error(self, mocker):
        mocker.patch.multiple(basic.AnsibleModule, exit_json=exit_json, fail_json=fail_json)
        set_module_args(
            {
                "project_path": "path/to/project",
                "name": "my_output",
                "format": "json",
                "binary_path": "terraform/binary/path",
                "state_file": "mystate.tfstate",
            }
        )
        mocker.patch("ansible_collections.cloud.terraform.plugins.modules.terraform_output.validate_bin_path")
        mocker.patch("ansible_collections.cloud.terraform.plugins.modules.terraform_output.get_outputs").side_effect = (
            TerraformError("Failure when getting Terraform outputs.")
        )

        with pytest.raises(AnsibleFailJson) as exc:
            terraform_output.main()

        assert exc.value.args[0]["msg"] == "Failure when getting Terraform outputs."
