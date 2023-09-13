# -*- coding: utf-8 -*-
# Copyright: (c) 2022, XLAB Steampunk <steampunk@xlab.si>
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)


import pytest
from subprocess import CompletedProcess
from ansible_collections.cloud.terraform.plugins.lookup import tf_output


class TestModuleRunCommand:
    def test_module_run_command(self, mocker):
        mocker.patch(
            "ansible_collections.cloud.terraform.plugins.lookup.tf_output.subprocess.run"
        ).return_value = CompletedProcess(
            args="args",
            returncode="returncode",
            stdout="stdout".encode("utf-8"),
            stderr="stderr".encode("utf-8"),
        )
        result = tf_output.module_run_command(["commands"], "cwd")

        assert result == ("returncode", "stdout", "stderr")


class TestLookupModuleRun:
    def test_run_with_terms(self, mocker):
        mocker.patch("ansible_collections.cloud.terraform.plugins.lookup.tf_output.LookupModule.set_options")
        mocker.patch(
            "ansible_collections.cloud.terraform.plugins.lookup.tf_output.LookupModule.get_option"
        ).side_effect = ["project_path", "state_file", "bin_path", "workspace"]
        mocker.patch("ansible_collections.cloud.terraform.plugins.lookup.tf_output.process.get_bin_path")
        mocker.patch("ansible_collections.cloud.terraform.plugins.lookup.tf_output.get_outputs").side_effect = [
            "my_output_value1",
            "my_output_value2",
        ]

        my_module = tf_output.LookupModule()
        output = my_module.run(terms=["my_output1", "my_output2"])

        assert output == ["my_output_value1", "my_output_value2"]

    def test_run_without_terms(self, mocker):
        mocker.patch("ansible_collections.cloud.terraform.plugins.lookup.tf_output.LookupModule.set_options")
        mocker.patch(
            "ansible_collections.cloud.terraform.plugins.lookup.tf_output.LookupModule.get_option"
        ).side_effect = ["project_path", "state_file", "bin_path", "workspace"]
        mocker.patch("ansible_collections.cloud.terraform.plugins.lookup.tf_output.process.get_bin_path")
        mocker.patch("ansible_collections.cloud.terraform.plugins.lookup.tf_output.get_outputs").return_value = {
            "my_output1": {"sensitive": False, "type": "string", "value": "value1"},
            "my_output2": {"sensitive": False, "type": "string", "value": "value2"},
        }

        my_module = tf_output.LookupModule()
        output = my_module.run(terms=None)

        assert output == [
            {
                "my_output1": {"sensitive": False, "type": "string", "value": "value1"},
                "my_output2": {"sensitive": False, "type": "string", "value": "value2"},
            }
        ]
