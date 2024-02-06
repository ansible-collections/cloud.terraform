# -*- coding: utf-8 -*-

# Copyright: Contributors to the Ansible project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)


from ansible.plugins.action import ActionBase
from ansible.utils.vars import isidentifier
from ansible_collections.cloud.terraform.plugins.module_utils.plan_stash_args import PLAN_STASH_ARG_SPEC


class ActionModule(ActionBase):  # type: ignore  # mypy ignore
    def run(self, tmp=None, task_vars=None):  # type: ignore  # mypy ignore
        if task_vars is None:
            task_vars = dict()

        result = super(ActionModule, self).run(tmp, task_vars)
        del tmp  # tmp no longer has any effect

        validation_result, new_module_args = self.validate_argument_spec(PLAN_STASH_ARG_SPEC)

        # Validate that 'var_name' is a valid variable name
        var_name = new_module_args.get("var_name")
        if not isidentifier(var_name):
            result["failed"] = True
            result["msg"] = (
                "The variable name '%s' is not valid. Variables must start with a letter or underscore character, and contain only "
                "letters, numbers and underscores." % var_name
            )
            return result

        # Execute the plan_stash module.
        module_return = self._execute_module(
            module_name=self._task.action,
            module_args=new_module_args,
            task_vars=task_vars,
        )

        result.update(module_return)
        result["changed"] = False
        return result
