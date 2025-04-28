# Copyright (c) Ansible project
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later

import contextlib
import json
import unittest
from unittest.mock import patch

from ansible.module_utils import basic
from ansible.module_utils.common.text.converters import to_bytes


@contextlib.contextmanager
def set_module_args(args):
    """
    Context manager that sets module arguments for AnsibleModule
    """
    if "_ansible_remote_tmp" not in args:
        args["_ansible_remote_tmp"] = "/tmp"
    if "_ansible_keep_remote_files" not in args:
        args["_ansible_keep_remote_files"] = False

    try:
        from ansible.module_utils.testing import patch_module_args
    except ImportError:
        # Before data tagging support was merged, this was the way to go:
        from ansible.module_utils import basic

        serialized_args = to_bytes(json.dumps({"ANSIBLE_MODULE_ARGS": args}))
        with patch.object(basic, "_ANSIBLE_ARGS", serialized_args):
            yield
    else:
        # With data tagging support, we have a new helper for this:
        with patch_module_args(args):
            yield


class AnsibleExitJson(Exception):
    pass


class AnsibleFailJson(Exception):
    pass


def exit_json(*args, **kwargs):
    if "changed" not in kwargs:
        kwargs["changed"] = False
    raise AnsibleExitJson(kwargs)


def fail_json(*args, **kwargs):
    kwargs["failed"] = True
    raise AnsibleFailJson(kwargs)


class ModuleTestCase(unittest.TestCase):
    def setUp(self):
        self.mock_module = patch.multiple(basic.AnsibleModule, exit_json=exit_json, fail_json=fail_json)
        self.mock_module.start()
        self.mock_sleep = patch("time.sleep")
        self.mock_sleep.start()
        set_module_args({})
        self.addCleanup(self.mock_module.stop)
        self.addCleanup(self.mock_sleep.stop)
