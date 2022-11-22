#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright (c) 2017, Ryan Scott Brown <ryansb@redhat.com>
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import absolute_import, division, print_function

__metaclass__ = type

# language=yaml
DOCUMENTATION = r'''
---
module: terraform
short_description: Manages a Terraform deployment (and plans)
description:
     - Provides support for deploying resources with Terraform and pulling
       resource information back into Ansible.
options:
  state:
    choices: ['present', 'absent', 'planned']
    description:
      - Goal state of given stage/project.
      - Option `planned` is deprecated.
        Its function is equivalent to running the module in check mode.
    type: str
    default: present
    version_added: 1.0.0
  binary_path:
    description:
      - The path of a terraform binary to use.
    type: path
    version_added: 1.0.0
  project_path:
    description:
      - The path to the root of the Terraform directory with the
        vars.tf/main.tf/etc to use.
    type: path
    required: true
    version_added: 1.0.0
  plugin_paths:
    description:
      - List of paths containing Terraform plugin executable files.
      - Plugin executables can be downloaded from U(https://releases.hashicorp.com/).
      - When set, the plugin discovery and auto-download behavior of Terraform is disabled.
      - The directory structure in the plugin path can be tricky. The Terraform docs
        U(https://learn.hashicorp.com/tutorials/terraform/automate-terraform#pre-installed-plugins)
        show a simple directory of files, but actually, the directory structure
        has to follow the same structure you would see if Terraform auto-downloaded the plugins.
        See the examples below for a tree output of an example plugin directory.
    type: list
    elements: path
    version_added: 1.0.0
  workspace:
    description:
      - The terraform workspace to work with.
    type: str
    default: default
    version_added: 1.0.0
  purge_workspace:
    description:
      - Only works with state = absent
      - If true, the workspace will be deleted after the "terraform destroy" action.
      - The 'default' workspace will not be deleted.
    default: false
    type: bool
    version_added: 1.0.0
  plan_file:
    description:
      - The path to an existing Terraform plan file to apply. If this is not
        specified, Ansible will build a new TF plan and execute it.
      - Note that this option is required if 'state' has the 'planned' value.
        In this case, the plan file is only generated, but not applied.
    type: path
    version_added: 1.0.0
  state_file:
    description:
      - The path to an existing Terraform state file to use when building plan.
        If this is not specified, the default C(terraform.tfstate) will be used.
      - This option is ignored when plan is specified.
    type: path
    version_added: 1.0.0
  variables_files:
    description:
      - The path to a variables file for Terraform to fill into the TF
        configurations. This can accept a list of paths to multiple variables files.
      - Up until Ansible 2.9, this option was usable as I(variables_file).
    type: list
    elements: path
    aliases: [ 'variables_file' ]
    version_added: 1.0.0
  variables:
    description:
      - A group of key-values pairs to override template variables or those in variables files.
        By default, only string and number values are allowed, which are passed on unquoted.
      - Support complex variable structures (lists, dictionaries, numbers, and booleans) to reflect terraform variable syntax when I(complex_vars=true).
      - Ansible integers or floats are mapped to terraform numbers.
      - Ansible strings are mapped to terraform strings.
      - Ansible dictionaries are mapped to terraform objects.
      - Ansible lists are mapped to terraform lists.
      - Ansible booleans are mapped to terraform booleans.
      - "B(Note) passwords passed as variables will be visible in the log output. Make sure to use I(no_log=true) in production!"
    type: dict
    version_added: 1.0.0
  complex_vars:
    description:
      - Enable/disable capability to handle complex variable structures for C(terraform).
      - If C(true) the I(variables) also accepts dictionaries, lists, and booleans to be passed to C(terraform).
        Strings that are passed are correctly quoted.
      - When disabled, supports only simple variables (strings, integers, and floats), and passes them on unquoted.
    type: bool
    default: false
    version_added: 1.0.0
  targets:
    description:
      - A list of specific resources to target in this plan/application. The
        resources selected here will also auto-include any dependencies.
    type: list
    elements: str
    version_added: 1.0.0
  lock:
    description:
      - Enable statefile locking, if you use a service that accepts locks (such
        as S3+DynamoDB) to store your statefile.
    type: bool
    default: true
    version_added: 1.0.0
  lock_timeout:
    description:
      - How long to maintain the lock on the statefile, if you use a service
        that accepts locks (such as S3+DynamoDB).
    type: int
    version_added: 1.0.0
  force_init:
    description:
      - To avoid duplicating infra, if a state file can't be found this will
        force a C(terraform init). Generally, this should be turned off unless
        you intend to provision an entirely new Terraform deployment.
    default: false
    type: bool
    version_added: 1.0.0
  overwrite_init:
    description:
      - Run init even if C(.terraform/terraform.tfstate) already exists in I(project_path).
    default: true
    type: bool
    version_added: 1.0.0
  backend_config:
    description:
      - A group of key-values to provide at init stage to the -backend-config parameter.
    type: dict
    version_added: 1.0.0
  backend_config_files:
    description:
      - The path to a configuration file to provide at init state to the -backend-config parameter.
        This can accept a list of paths to multiple configuration files.
    type: list
    elements: path
    version_added: 1.0.0
  provider_upgrade:
    description:
      - Allows Terraform init to upgrade providers to versions specified in the project's version constraints.
    default: false
    type: bool
    version_added: 1.0.0
  init_reconfigure:
    description:
      - Forces backend reconfiguration during init.
    default: false
    type: bool
    version_added: 1.0.0
  check_destroy:
    description:
      - Apply only when no resources are destroyed. Note that this only prevents "destroy" actions,
        but not "destroy and re-create" actions. This option is ignored when I(state=absent).
    type: bool
    default: false
    version_added: 1.0.0
  parallelism:
    description:
      - Restrict concurrent operations when Terraform applies the plan.
    type: int
    version_added: 1.0.0
notes:
   - To just run a C(terraform plan), use check mode.
requirements: [ "terraform" ]
author: "Ryan Scott Brown (@ryansb)"
'''

# language=yaml
EXAMPLES = """
- name: Basic deploy of a service
  cloud.terraform.terraform:
    project_path: '{{ project_dir }}'
    state: present

- name: Define the backend configuration at init
  cloud.terraform.terraform:
    project_path: 'project/'
    state: "{{ state }}"
    force_init: true
    backend_config:
      region: "eu-west-1"
      bucket: "some-bucket"
      key: "random.tfstate"

- name: Define the backend configuration with one or more files at init
  cloud.terraform.terraform:
    project_path: 'project/'
    state: "{{ state }}"
    force_init: true
    backend_config_files:
      - /path/to/backend_config_file_1
      - /path/to/backend_config_file_2

- name: Disable plugin discovery and auto-download by setting plugin_paths
  cloud.terraform.terraform:
    project_path: 'project/'
    state: "{{ state }}"
    force_init: true
    plugin_paths:
      - /path/to/plugins_dir_1
      - /path/to/plugins_dir_2

- name: Complex variables example
  cloud.terraform.terraform:
    project_path: '{{ project_dir }}'
    state: present
    camplex_vars: true
    variables:
      vm_name: "{{ inventory_hostname }}"
      vm_vcpus: 2
      vm_mem: 2048
      vm_additional_disks:
        - label: "Third Disk"
          size: 40
          thin_provisioned: true
          unit_number: 2
        - label: "Fourth Disk"
          size: 22
          thin_provisioned: true
          unit_number: 3
    force_init: true

### Example directory structure for plugin_paths example
# $ tree /path/to/plugins_dir_1
# /path/to/plugins_dir_1/
# └── registry.terraform.io
#     └── hashicorp
#         └── vsphere
#             ├── 1.24.0
#             │   └── linux_amd64
#             │       └── terraform-provider-vsphere_v1.24.0_x4
#             └── 1.26.0
#                 └── linux_amd64
#                     └── terraform-provider-vsphere_v1.26.0_x4
"""

# language=yaml
RETURN = """
outputs:
  type: complex
  description: A dictionary of all the TF outputs by their assigned name. Use C(.outputs.MyOutputName.value) to access the value.
  returned: on success
  sample: '{"bukkit_arn": {"sensitive": false, "type": "string", "value": "arn:aws:s3:::tf-test-bukkit"}'
  contains:
    sensitive:
      type: bool
      returned: always
      description: Whether Terraform has marked this value as sensitive
    type:
      type: str
      returned: always
      description: The type of the value (string, int, etc)
    value:
      type: str
      returned: always
      description: The value of the output as interpolated by Terraform
stdout:
  type: str
  description: Full C(terraform) command stdout, in case you want to display it or examine the event log
  returned: always
  sample: ''
command:
  type: str
  description: Full C(terraform) command built by this module, in case you want to re-run the command outside the module or debug a problem.
  returned: always
  sample: terraform apply ...
"""

import os
import json
import tempfile
from ansible.module_utils.six.moves import shlex_quote
from ansible.module_utils.six import integer_types

from ansible.module_utils.basic import AnsibleModule

from ansible_collections.cloud.terraform.plugins.module_utils.version import LooseVersion

module = None  # type: AnsibleModule


def get_version(bin_path):
    extract_version = module.run_command([bin_path, 'version', '-json'])
    terraform_version = (json.loads(extract_version[1]))['terraform_version']
    return terraform_version


def preflight_validation(bin_path, project_path, version, variables_args=None, plan_file=None):
    if project_path is None or '/' not in project_path:
        module.fail_json(msg="Path for Terraform project can not be None or ''.")
    if not os.path.exists(bin_path):
        module.fail_json(
            msg="Path for Terraform binary '{0}' doesn't exist on this host - check the path and try again please.".format(
                bin_path))
    if not os.path.isdir(project_path):
        module.fail_json(
            msg="Path for Terraform project '{0}' doesn't exist on this host - check the path and try again please.".format(
                project_path))
    if LooseVersion(version) < LooseVersion('0.15.0'):
        rc, out, err = module.run_command([bin_path, 'validate'] + variables_args, check_rc=True, cwd=project_path)
    else:
        rc, out, err = module.run_command([bin_path, 'validate'], check_rc=True, cwd=project_path)


def _state_args(state_file):
    if state_file and os.path.exists(state_file):
        return ['-state', state_file]
    if state_file and not os.path.exists(state_file):
        module.fail_json(msg='Could not find state_file "{0}", check the path and try again.'.format(state_file))
    return []


def init_plugins(bin_path, project_path, backend_config, backend_config_files, init_reconfigure, provider_upgrade,
                 plugin_paths):
    command = [bin_path, 'init', '-input=false', '-no-color']
    if backend_config:
        for key, val in backend_config.items():
            command.extend([
                '-backend-config',
                '{0}={1}'.format(key, val)
            ])
    if backend_config_files:
        for f in backend_config_files:
            command.extend(['-backend-config', f])
    if init_reconfigure:
        command.extend(['-reconfigure'])
    if provider_upgrade:
        command.extend(['-upgrade'])
    if plugin_paths:
        for plugin_path in plugin_paths:
            command.extend(['-plugin-dir', plugin_path])
    rc, out, err = module.run_command(command, check_rc=True, cwd=project_path)


def get_workspace_context(bin_path, project_path):
    workspace_ctx = {"current": "default", "all": []}
    command = [bin_path, 'workspace', 'list', '-no-color']
    rc, out, err = module.run_command(command, cwd=project_path)
    if rc != 0:
        module.warn("Failed to list Terraform workspaces:\n{0}".format(err))
    for item in out.split('\n'):
        stripped_item = item.strip()
        if not stripped_item:
            continue
        elif stripped_item.startswith('* '):
            workspace_ctx["current"] = stripped_item.replace('* ', '')
        else:
            workspace_ctx["all"].append(stripped_item)
    return workspace_ctx


def _workspace_cmd(bin_path, project_path, action, workspace):
    command = [bin_path, 'workspace', action, workspace, '-no-color']
    rc, out, err = module.run_command(command, check_rc=True, cwd=project_path)
    return rc, out, err


def create_workspace(bin_path, project_path, workspace):
    _workspace_cmd(bin_path, project_path, 'new', workspace)


def select_workspace(bin_path, project_path, workspace):
    _workspace_cmd(bin_path, project_path, 'select', workspace)


def remove_workspace(bin_path, project_path, workspace):
    _workspace_cmd(bin_path, project_path, 'delete', workspace)


def build_plan(terraform_binary, project_path, variables_args, state_file, targets, state):
    f, plan_file_path = tempfile.mkstemp(suffix='.tfplan')

    plan_command = [
        terraform_binary, 'plan', '-lock=true', '-input=false', '-no-color', '-detailed-exitcode',
        '-out', plan_file_path
    ]

    for t in targets:
        plan_command.extend(['-target', t])
    if state == "absent":
        plan_command.append("-destroy")
    plan_command.extend(_state_args(state_file))

    rc, stdout, stderr = module.run_command(plan_command + variables_args, cwd=project_path)

    if rc == 0:
        # no changes
        changed = False
    elif rc == 1:
        # failure to plan
        module.fail_json(
            msg='Terraform plan could not be created\nSTDOUT: {out}\nSTDERR: {err}\nCOMMAND: {cmd} {args}'.format(
                out=stdout,
                err=stderr,
                cmd=' '.join(plan_command),
                args=' '.join([shlex_quote(arg) for arg in variables_args])
            )
        )
    elif rc == 2:
        # changes, but successful
        changed = True
    else:
        module.fail_json(
            msg='Terraform plan failed with unexpected exit code {rc}.\nSTDOUT: {out}\nSTDERR: {err}\nCOMMAND: {cmd} {args}'.format(
                rc=rc,
                out=stdout,
                err=stderr,
                cmd=' '.join(plan_command),
                args=' '.join([shlex_quote(arg) for arg in variables_args])
            ))

    if "- destroy" in stdout:
        any_destroyed = True
    else:
        any_destroyed = False

    return plan_file_path, changed, any_destroyed, stdout, stderr


def execute_plan(terraform_binary, prebuilt_command, project_path, workspace, workspace_ctx):
    rc, out, err = module.run_command(prebuilt_command, check_rc=False, cwd=project_path)
    if rc != 0:
        if workspace_ctx["current"] != workspace:
            select_workspace(terraform_binary, project_path, workspace_ctx["current"])
        module.fail_json(msg=err.rstrip(), rc=rc, stdout=out,
                         stdout_lines=out.splitlines(), stderr=err,
                         stderr_lines=err.splitlines(),
                         cmd=' '.join(prebuilt_command))
    return out, err


def get_outputs(terraform_binary, project_path, state_file):
    outputs_command = [terraform_binary, 'output', '-no-color', '-json'] + _state_args(state_file)
    rc, outputs_text, outputs_err = module.run_command(outputs_command, cwd=project_path)
    if rc == 1:
        module.warn(
            "Could not get Terraform outputs. "
            "This usually means none have been defined.\nstdout: {0}\nstderr: {1}".format(
                outputs_text, outputs_err
            )
        )
        outputs = {}
    elif rc != 0:
        module.fail_json(
            msg="Failure when getting Terraform outputs. "
                "Exited {0}.\nstdout: {1}\nstderr: {2}".format(rc, outputs_text, outputs_err),
            command=' '.join(outputs_command))
    else:
        outputs = json.loads(outputs_text)

    return outputs


def main():
    global module
    module = AnsibleModule(
        argument_spec=dict(
            project_path=dict(required=True, type='path'),
            binary_path=dict(type='path'),
            plugin_paths=dict(type='list', elements='path'),
            workspace=dict(type='str', default='default'),
            purge_workspace=dict(type='bool', default=False),
            state=dict(default='present', choices=['present', 'absent', 'planned']),
            variables=dict(type='dict'),
            complex_vars=dict(type='bool', default=False),
            variables_files=dict(aliases=['variables_file'], type='list', elements='path'),
            plan_file=dict(type='path'),
            state_file=dict(type='path'),
            targets=dict(type='list', elements='str', default=[]),
            lock=dict(type='bool', default=True),
            lock_timeout=dict(type='int'),
            force_init=dict(type='bool', default=False),
            backend_config=dict(type='dict'),
            backend_config_files=dict(type='list', elements='path'),
            init_reconfigure=dict(type='bool', default=False),
            overwrite_init=dict(type='bool', default=True),
            check_destroy=dict(type='bool', default=False),
            parallelism=dict(type='int'),
            provider_upgrade=dict(type='bool', default=False),
        ),
        required_if=[('state', 'planned', ['plan_file'])],
        supports_check_mode=True,
    )

    project_path = module.params.get('project_path')
    bin_path = module.params.get('binary_path')
    plugin_paths = module.params.get('plugin_paths')
    workspace = module.params.get('workspace')
    purge_workspace = module.params.get('purge_workspace')
    variables = module.params.get('variables') or {}
    complex_vars = module.params.get('complex_vars')
    variables_files = module.params.get('variables_files')
    plan_file = module.params.get('plan_file')
    state_file = module.params.get('state_file')
    force_init = module.params.get('force_init')
    backend_config = module.params.get('backend_config')
    backend_config_files = module.params.get('backend_config_files')
    init_reconfigure = module.params.get('init_reconfigure')
    overwrite_init = module.params.get('overwrite_init')
    check_destroy = module.params.get('check_destroy')
    provider_upgrade = module.params.get('provider_upgrade')
    state = module.params.get('state')

    if state == 'planned':
        computed_check_mode = True
        computed_state = 'present'
        module.deprecate(
            'The value `planned` for the parameter "state" is deprecated. This will be an error in the future',
            version='6.0.0',
            collection_name='cloud.terraform'
        )
    else:
        computed_check_mode = module.check_mode
        computed_state = state

    if bin_path is not None:
        terraform_binary = bin_path
    else:
        terraform_binary = module.get_bin_path('terraform', required=True)
    final_apply_command = [terraform_binary]

    checked_version = get_version(terraform_binary)

    if LooseVersion(checked_version) < LooseVersion('0.15.0'):
        apply_args = ('apply', '-no-color', '-input=false', '-auto-approve=true')
    else:
        apply_args = ('apply', '-no-color', '-input=false', '-auto-approve')
    final_apply_command.extend(apply_args)

    if computed_state == 'present' and module.params.get('parallelism') is not None:
        final_apply_command.append('-parallelism=%d' % module.params.get('parallelism'))

    if module.params.get('lock', False):
        final_apply_command.append('-lock=true')
    else:
        final_apply_command.append('-lock=false')

    if module.params.get('lock_timeout') is not None:
        final_apply_command.append('-lock-timeout=%ds' % module.params.get('lock_timeout'))

    for t in (module.params.get('targets') or []):
        final_apply_command.extend(['-target', t])

    if force_init:
        if overwrite_init or not os.path.isfile(os.path.join(project_path, ".terraform", "terraform.tfstate")):
            init_plugins(terraform_binary, project_path, backend_config, backend_config_files, init_reconfigure,
                         provider_upgrade, plugin_paths)

    workspace_ctx = get_workspace_context(terraform_binary, project_path)
    if workspace_ctx["current"] != workspace:
        if workspace not in workspace_ctx["all"]:
            create_workspace(terraform_binary, project_path, workspace)
        else:
            select_workspace(terraform_binary, project_path, workspace)

    def format_args(vars):
        if isinstance(vars, str):
            return '"{string}"'.format(string=vars.replace('\\', '\\\\').replace('"', '\\"'))
        elif isinstance(vars, bool):
            if vars:
                return 'true'
            else:
                return 'false'
        return str(vars)

    def process_complex_args(vars):
        ret_out = []
        if isinstance(vars, dict):
            for k, v in vars.items():
                if isinstance(v, dict):
                    ret_out.append('{0}={{{1}}}'.format(k, process_complex_args(v)))
                elif isinstance(v, list):
                    ret_out.append("{0}={1}".format(k, process_complex_args(v)))
                elif isinstance(v, (integer_types, float, str, bool)):
                    ret_out.append('{0}={1}'.format(k, format_args(v)))
                else:
                    # only to handle anything unforeseen
                    module.fail_json(
                        msg="Supported types are, dictionaries, lists, strings, integer_types, boolean and float.")
        if isinstance(vars, list):
            l_out = []
            for item in vars:
                if isinstance(item, dict):
                    l_out.append("{{{0}}}".format(process_complex_args(item)))
                elif isinstance(item, list):
                    l_out.append("{0}".format(process_complex_args(item)))
                elif isinstance(item, (str, integer_types, float, bool)):
                    l_out.append(format_args(item))
                else:
                    # only to handle anything unforeseen
                    module.fail_json(
                        msg="Supported types are, dictionaries, lists, strings, integer_types, boolean and float.")

            ret_out.append("[{0}]".format(",".join(l_out)))
        return ",".join(ret_out)

    variables_args = []
    if complex_vars:
        for k, v in variables.items():
            if isinstance(v, dict):
                variables_args.extend([
                    '-var',
                    '{0}={{{1}}}'.format(k, process_complex_args(v))
                ])
            elif isinstance(v, list):
                variables_args.extend([
                    '-var',
                    '{0}={1}'.format(k, process_complex_args(v))
                ])
            # on the top-level we need to pass just the python string with necessary
            # terraform string escape sequences
            elif isinstance(v, str):
                variables_args.extend([
                    '-var',
                    "{0}={1}".format(k, v)
                ])
            else:
                variables_args.extend([
                    '-var',
                    '{0}={1}'.format(k, format_args(v))
                ])
    else:
        for k, v in variables.items():
            variables_args.extend([
                '-var',
                '{0}={1}'.format(k, v)
            ])

    if variables_files:
        for f in variables_files:
            variables_args.extend(['-var-file', f])

    # only use an existing plan file if we're not in the deprecated "planned" mode
    if plan_file and state != "planned":
        if not any([os.path.isfile(project_path + "/" + plan_file), os.path.isfile(plan_file)]):
            module.fail_json(msg='Could not find plan_file "{0}", check the path and try again.'.format(plan_file))

        plan_file_needs_application = True
        plan_file_to_apply = plan_file
    else:
        new_plan_file, plan_result_changed, plan_result_any_destroyed, plan_stdout, plan_stderr = build_plan(
            terraform_binary=terraform_binary,
            project_path=project_path,
            variables_args=variables_args,
            state_file=state_file,
            targets=module.params.get('targets'),
            state=computed_state
        )

        # if we have an explicit plan file specified, copy over the temporary one
        if plan_file:
            module.preserved_copy(new_plan_file, project_path + "/" + plan_file)

        if computed_state == 'present' and plan_result_any_destroyed and check_destroy:
            module.fail_json(msg="Aborting command because it would destroy some resources. "
                                 "Consider switching the 'check_destroy' to false to suppress this error")

        plan_file_needs_application = plan_result_changed
        plan_file_to_apply = new_plan_file
        out = plan_stdout
        err = plan_stderr

    final_apply_command.append(plan_file_to_apply)

    preflight_validation(terraform_binary, project_path, checked_version, variables_args)

    if plan_file_needs_application and not computed_check_mode:
        apply_stdout, apply_stderr = execute_plan(
            terraform_binary=terraform_binary,
            prebuilt_command=final_apply_command,
            project_path=project_path,
            workspace=workspace,
            workspace_ctx=workspace_ctx
        )

        out = apply_stdout
        err = apply_stderr

    outputs = get_outputs(
        terraform_binary=terraform_binary,
        project_path=project_path,
        state_file=state_file
    )

    # Restore the Terraform workspace found when running the module
    if workspace_ctx["current"] != workspace:
        select_workspace(terraform_binary, project_path, workspace_ctx["current"])
    if computed_state == 'absent' and workspace != 'default' and purge_workspace is True:
        remove_workspace(terraform_binary, project_path, workspace)

    module.exit_json(changed=plan_file_needs_application, state=computed_state, workspace=workspace, outputs=outputs,
                     stdout=out, stderr=err, command=' '.join(final_apply_command))


if __name__ == '__main__':
    main()
