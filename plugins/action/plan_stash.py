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
        binary_data = new_module_args.get("binary_data")
        if var_name:
            if not isidentifier(var_name):
                result["failed"] = True
                result["msg"] = (
                    "The variable name '%s' is not valid. Variables must start with a letter or underscore character, and contain only "
                    "letters, numbers and underscores." % var_name
                )
                return result

        state = new_module_args.get("state")
        if state == "load":
            if var_name is not None and binary_data is not None:
                result["failed"] = True
                result["msg"] = "You cannot specify both 'var_name' and 'binary_data' to load the terraform plan file."
                return result

            if binary_data is None:
                var_name = new_module_args.get("var_name") or "terraform_plan"
                try:
                    value = task_vars[var_name]
                except KeyError:
                    try:
                        value = task_vars["hostvars"][task_vars["inventory_hostname"]][var_name]
                    except KeyError:
                        result["failed"] = True
                        result["msg"] = "No variable found with this name: %s" % var_name
                        return result

                new_module_args.pop("var_name")
                new_module_args["binary_data"] = value
        elif state == "stash":
            var_name = new_module_args.get("var_name") or "terraform_plan"
            new_module_args.update({"var_name": var_name})

        # Execute the plan_stash module.
        module_return = self._execute_module(
            module_name=self._task.action,
            module_args=new_module_args,
            task_vars=task_vars,
        )

        result.update(module_return)
        return result
