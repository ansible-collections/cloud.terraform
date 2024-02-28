# -*- coding: utf-8 -*-
# Copyright: (c) 2022, XLAB Steampunk <steampunk@xlab.si>
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from subprocess import CompletedProcess

from ansible_collections.cloud.terraform.plugins.plugin_utils.common import module_run_command


class TestModuleRunCommand:
    def test_module_run_command(self, mocker):
        cmd = ["test"]
        cwd = "test/directory"
        mocker.patch(
            "ansible_collections.cloud.terraform.plugins.plugin_utils.common.subprocess.run"
        ).return_value = CompletedProcess(
            args=cmd,
            returncode=0,
            stdout="stdout".encode("utf-8"),
            stderr="stderr".encode("utf-8"),
        )

        completed_process = module_run_command(cmd=cmd, cwd=cwd, check_rc=False)

        assert completed_process == (0, "stdout", "stderr")
