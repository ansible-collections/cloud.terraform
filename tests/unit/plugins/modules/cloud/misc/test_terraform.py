# Copyright (c) 2019, Ansible Project
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later
import json

import pytest
from ansible_collections.cloud.terraform.plugins.modules import terraform
from ansible_collections.cloud.terraform.tests.unit.plugins.modules.utils import set_module_args


def test_terraform_without_argument(capfd):
    set_module_args({})
    with pytest.raises(SystemExit):
        terraform.main()

    out, err = capfd.readouterr()
    assert not err
    assert json.loads(out)["failed"]
    assert "project_path" in json.loads(out)["msg"]
