# -*- coding: utf-8 -*-

# Copyright: Contributors to the Ansible project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)


import os
from copy import deepcopy

from ansible.errors import AnsibleActionFail, AnsibleError
from ansible.module_utils.parsing.convert_bool import boolean
from ansible.module_utils.six import string_types
from ansible.plugins.action import ActionBase
from ansible.utils.vars import isidentifier


class ActionModule(ActionBase):  # type: ignore  # mypy ignore
    def get_file_realpath(self, file_path: str) -> str:
        if os.path.exists(file_path):
            return file_path

        try:
            # find in expected paths
            return str(self._find_needle("files", file_path))
        except AnsibleError:
            raise AnsibleActionFail("%s does not exist in local filesystem" % file_path)

    def run(self, tmp=None, task_vars=None):  # type: ignore  # mypy ignore
        if task_vars is None:
            task_vars = dict()

        result = super(ActionModule, self).run(tmp, task_vars)
        del tmp  # tmp no longer has any effect

        if self._task.args:
            var_name = self._task.args.get("var_name", "terraform_plan")
            path = self._task.args.get("path", "")
            per_host = self._task.args.get("per_host", None)

            new_module_args = deepcopy(self._task.args)

            if var_name:
                if not isinstance(var_name, string_types):
                    result["failed"] = True
                    result["msg"] = "The 'var_name' option needs to be a string"
                    return result
                var_name = self._templar.template(var_name, convert_bare=False, fail_on_undefined=True)
                if not isidentifier(var_name):
                    result["failed"] = True
                    result["msg"] = (
                        "The variable name '%s' is not valid. Variables must start with a letter or underscore character, and contain only "
                        "letters, numbers and underscores." % var_name
                    )
                    return result
                new_module_args.update({"var_name": var_name})

            if path:
                path = self._templar.template(path, convert_bare=False, fail_on_undefined=True)
                path = self.get_file_realpath(path)
                new_module_args.update({"path": path})

            if per_host is not None and not isinstance(per_host, bool):
                per_host = boolean(self._templar.template(per_host), strict=False)
                new_module_args.update({"per_host": per_host})

            # Execute the plan_stash module.
            module_return = self._execute_module(
                module_name=self._task.action,
                module_args=new_module_args,
                task_vars=task_vars,
            )

            result.update(module_return)
            return result

        result["changed"] = False
        return result
