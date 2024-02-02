#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright (c) 2017, Ryan Scott Brown <ryansb@redhat.com>
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later

# language=yaml
DOCUMENTATION = r"""
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
      - The path to a Terraform plan file to apply or generate.
      - When 'check_mode' is set to I(True) or I(state=planned), a Terraform plan file will be generated and
        saved into the specified location.
      - When 'check_mode' is set to I(False) and I(state) is set to either C(present) or C(absent),
        The existing Terraform plan file will be applied.
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
    default: []
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
"""

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
    complex_vars: true
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

import dataclasses
import os
import tempfile
from typing import List

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.six import integer_types
from ansible_collections.cloud.terraform.plugins.module_utils.errors import TerraformError, TerraformWarning
from ansible_collections.cloud.terraform.plugins.module_utils.models import (
    TerraformModuleResource,
    TerraformProviderSchemaCollection,
    TerraformShow,
    TerraformWorkspaceContext,
)
from ansible_collections.cloud.terraform.plugins.module_utils.terraform_commands import (
    TerraformCommands,
    WorkspaceCommand,
)
from ansible_collections.cloud.terraform.plugins.module_utils.types import AnyJsonType, TJsonBareValue
from ansible_collections.cloud.terraform.plugins.module_utils.utils import (
    get_outputs,
    get_state_args,
    preflight_validation,
)


def is_attribute_sensitive_in_providers_schema(
    schemas: TerraformProviderSchemaCollection, resource: TerraformModuleResource, attribute: str
) -> bool:
    for provider_schema in schemas.provider_schemas:
        resource_schemas = schemas.provider_schemas[provider_schema].resource_schemas
        for resource_schema_name, resource_schema in resource_schemas.items():
            if resource_schema_name == resource.type:
                # it can happen that attribute is not in the providers schema
                if resource_schema.attributes.get(attribute):
                    sensitive = resource_schema.attributes[attribute].sensitive
                else:
                    sensitive = False
                return sensitive
    return False


def is_attribute_in_sensitive_values(resource: TerraformModuleResource, attribute: str) -> bool:
    # In case if one attribute inside of block is sensitive, the whole block is sensitive - example: ephemeral_block_device
    # or only selected attribute is sensitive - example: credit_specification, capacity_reservation_specification
    # Also in case of lists - example: security_groups, if one element is sensitive, the whole attribute is sensitive
    # Example of the sensitive_values
    # "sensitive_values":{"capacity_reservation_specification":[{"capacity_reservation_target":[{"capacity_reservation_id":true}]}],
    # "credit_specification":[{"cpu_credits":true}],"ebs_block_device":[],"enclave_options":[],"ephemeral_block_device":true,"ipv6_addresses":[],
    # "launch_template":[],"maintenance_options":[],"metadata_options":[],"network_interface":[],"private_dns_name_options":[],
    # "root_block_device":[],"secondary_private_ips":[],"security_groups":true,"tags":{},"tags_all":{},"vpc_security_group_ids":[]}}
    # to make code simpler, also in the case when only certain attributes in block are listed as sensitive, we make the whole block sensitive
    if attribute in resource.sensitive_values:
        if resource.sensitive_values[attribute]:  # is Truthy (True or not an empty [] or {})
            return True
    return False


def filter_resource_attributes(
    state_contents: TerraformShow, provider_schemas: TerraformProviderSchemaCollection
) -> TerraformShow:
    # using .get() in case there is no existing .tfstate before apply
    for resource in state_contents.values.root_module.resources:
        attributes_to_remove = []
        for attribute in resource.values:
            if is_attribute_sensitive_in_providers_schema(
                provider_schemas, resource, attribute
            ) or is_attribute_in_sensitive_values(resource, attribute):
                attributes_to_remove.append(attribute)
        for attribute in attributes_to_remove:
            resource.values[attribute] = None
    return state_contents


def filter_outputs(state_contents: TerraformShow) -> TerraformShow:
    outputs_to_remove: List[str] = []
    # using .get() in case there is no existing .tfstate before apply
    for output_key, output_value in state_contents.values.outputs.items():
        if output_value.sensitive:
            outputs_to_remove.append(output_key)

    for output in outputs_to_remove:
        state_contents.values.outputs[output].value = None

    return state_contents


def sanitize_state(
    show_state: TerraformShow,
    provider_schemas: TerraformProviderSchemaCollection,
) -> TerraformShow:
    show_state = filter_resource_attributes(show_state, provider_schemas)
    show_state = filter_outputs(show_state)
    return show_state


def format_args(terraform_variables: TJsonBareValue) -> str:
    if isinstance(terraform_variables, str):
        return '"{string}"'.format(string=terraform_variables.replace("\\", "\\\\").replace('"', '\\"'))
    elif isinstance(terraform_variables, bool):
        if terraform_variables:
            return "true"
        else:
            return "false"
    return str(terraform_variables)


def process_complex_args(terraform_variables: AnyJsonType) -> str:
    ret_out = []
    if isinstance(terraform_variables, dict):
        for k, v in terraform_variables.items():
            if isinstance(v, dict):
                ret_out.append("{0}={{{1}}}".format(k, process_complex_args(v)))
            elif isinstance(v, list):
                ret_out.append("{0}={1}".format(k, process_complex_args(v)))
            elif isinstance(v, (integer_types, float, str, bool)):
                ret_out.append("{0}={1}".format(k, format_args(v)))
            else:
                # only to handle anything unforeseen
                raise TerraformError(
                    "Supported types are, dictionaries, lists, strings, integer_types, boolean and float."
                )
    if isinstance(terraform_variables, list):
        l_out = []
        for item in terraform_variables:
            if isinstance(item, dict):
                l_out.append("{{{0}}}".format(process_complex_args(item)))
            elif isinstance(item, list):
                l_out.append("{0}".format(process_complex_args(item)))
            elif isinstance(item, (str, integer_types, float, bool)):
                l_out.append(format_args(item))
            else:
                # only to handle anything unforeseen
                raise TerraformError(
                    "Supported types are, dictionaries, lists, strings, integer_types, boolean and float."
                )

        ret_out.append("[{0}]".format(",".join(l_out)))
    return ",".join(ret_out)


def main() -> None:
    module = AnsibleModule(
        argument_spec=dict(
            project_path=dict(required=True, type="path"),
            binary_path=dict(type="path"),
            plugin_paths=dict(type="list", elements="path"),
            workspace=dict(type="str", default="default"),
            purge_workspace=dict(type="bool", default=False),
            state=dict(default="present", choices=["present", "absent", "planned"]),
            variables=dict(type="dict"),
            complex_vars=dict(type="bool", default=False),
            variables_files=dict(aliases=["variables_file"], type="list", elements="path"),
            plan_file=dict(type="path"),
            state_file=dict(type="path"),
            targets=dict(type="list", elements="str", default=[]),
            lock=dict(type="bool", default=True),
            lock_timeout=dict(type="int"),
            force_init=dict(type="bool", default=False),
            backend_config=dict(type="dict"),
            backend_config_files=dict(type="list", elements="path"),
            init_reconfigure=dict(type="bool", default=False),
            overwrite_init=dict(type="bool", default=True),
            check_destroy=dict(type="bool", default=False),
            parallelism=dict(type="int"),
            provider_upgrade=dict(type="bool", default=False),
        ),
        required_if=[("state", "planned", ["plan_file"])],
        supports_check_mode=True,
    )

    project_path = module.params.get("project_path")
    bin_path = module.params.get("binary_path")
    plugin_paths = module.params.get("plugin_paths")
    workspace = module.params.get("workspace")
    purge_workspace = module.params.get("purge_workspace")
    variables = module.params.get("variables") or {}
    complex_vars = module.params.get("complex_vars")
    variables_files = module.params.get("variables_files")
    plan_file = module.params.get("plan_file")
    state_file = module.params.get("state_file")
    force_init = module.params.get("force_init")
    backend_config = module.params.get("backend_config")
    backend_config_files = module.params.get("backend_config_files")
    init_reconfigure = module.params.get("init_reconfigure")
    overwrite_init = module.params.get("overwrite_init")
    check_destroy = module.params.get("check_destroy")
    provider_upgrade = module.params.get("provider_upgrade")
    state = module.params.get("state")

    if state == "planned":
        computed_check_mode = True
        computed_state = "present"
        module.deprecate(
            'The value `planned` for the parameter "state" is deprecated. This will be an error in the future',
            version="6.0.0",
            collection_name="cloud.terraform",
        )
    else:
        computed_check_mode = module.check_mode
        computed_state = state

    if bin_path is not None:
        terraform_binary = bin_path
    else:
        terraform_binary = module.get_bin_path("terraform", required=True)

    terraform = TerraformCommands(module.run_command, project_path, terraform_binary, computed_check_mode)

    checked_version = terraform.version()

    if force_init:
        if overwrite_init or not os.path.isfile(os.path.join(project_path, ".terraform", "terraform.tfstate")):
            terraform.init(
                backend_config or {},
                backend_config_files or [],
                init_reconfigure,
                provider_upgrade,
                plugin_paths or [],
            )

    out = None
    err = None
    try:
        provider_schemas = terraform.providers_schema()
        try:
            initial_state = terraform.show(state_file)
            if initial_state is not None:
                initial_state = sanitize_state(initial_state, provider_schemas)
        except TerraformWarning as e:
            module.warn(e.message)
            initial_state = None

        try:
            workspace_ctx = terraform.workspace_list()
        except TerraformWarning as e:
            module.warn(e.message)
            workspace_ctx = TerraformWorkspaceContext(current="default", all=[])

        if workspace_ctx.current != workspace:
            if workspace not in workspace_ctx.all:
                terraform.workspace(WorkspaceCommand.NEW, workspace)
            else:
                terraform.workspace(WorkspaceCommand.SELECT, workspace)

        variables_args = []
        if complex_vars:
            for k, v in variables.items():
                if isinstance(v, dict):
                    variables_args.extend(["-var", "{0}={{{1}}}".format(k, process_complex_args(v))])
                elif isinstance(v, list):
                    variables_args.extend(["-var", "{0}={1}".format(k, process_complex_args(v))])
                # on the top-level we need to pass just the python string with necessary
                # terraform string escape sequences
                elif isinstance(v, str):
                    variables_args.extend(["-var", "{0}={1}".format(k, v)])
                else:
                    variables_args.extend(["-var", "{0}={1}".format(k, format_args(v))])
        else:
            for k, v in variables.items():
                variables_args.extend(["-var", "{0}={1}".format(k, v)])

        if variables_files:
            for f in variables_files:
                variables_args.extend(["-var-file", f])

        # only use an existing plan file if we're not in the deprecated "planned" mode
        # or if check_mode is set to False
        if plan_file and not computed_check_mode:
            if not any([os.path.isfile(project_path + "/" + plan_file), os.path.isfile(plan_file)]):
                raise TerraformError('Could not find plan_file "{0}", check the path and try again.'.format(plan_file))

            plan_file_needs_application = True
            plan_file_to_apply = plan_file
        else:
            plan_file_to_apply = plan_file
            if not plan_file:
                f, new_plan_file = tempfile.mkstemp(suffix=".tfplan")
                module.add_cleanup_file(new_plan_file)
                plan_file_to_apply = new_plan_file

            plan_result_changed, plan_result_any_destroyed, plan_stdout, plan_stderr = terraform.plan(
                target_plan_file_path=plan_file_to_apply,
                targets=module.params.get("targets"),
                destroy=state == "absent",
                state_args=get_state_args(state_file),
                variables_args=variables_args,
            )

            if computed_state == "present" and plan_result_any_destroyed and check_destroy:
                raise TerraformError(
                    "Aborting command because it would destroy some resources. "
                    "Consider switching the 'check_destroy' to false to suppress this error"
                )

            plan_file_needs_application = plan_result_changed
            out = plan_stdout
            err = plan_stderr

        preflight_validation(terraform, terraform_binary, project_path, checked_version, variables_args)

        try:
            planned_state = terraform.show(plan_file_to_apply)
            if planned_state is not None:
                planned_state = sanitize_state(planned_state, provider_schemas)
        except TerraformWarning as e:
            module.warn(e.message)
            planned_state = None

        try:
            # obeys check mode
            final_apply_command, apply_stdout, apply_stderr = terraform.apply_plan(
                plan_file_path=plan_file_to_apply,
                version=checked_version,
                parallelism=module.params.get("parallelism"),
                lock=module.params.get("lock", False),
                lock_timeout=module.params.get("lock_timeout"),
                targets=module.params.get("targets") or [],
                needs_application=plan_file_needs_application,
            )
        except TerraformError as e:
            if not computed_check_mode:
                if workspace_ctx.current != workspace:
                    terraform.workspace(WorkspaceCommand.SELECT, workspace_ctx.current)
            raise e

        if not computed_check_mode:
            applied_state = terraform.show(state_file)
            if applied_state is not None:
                applied_state = sanitize_state(applied_state, provider_schemas)
            final_state = applied_state
            out = apply_stdout
            err = apply_stderr
        else:
            final_state = planned_state

        outputs = get_outputs(
            run_command_fp=module.run_command,
            terraform_binary=terraform_binary,
            project_path=project_path,
            state_file=state_file,
            output_format="json",
            workspace=workspace,
        )

        # Restore the Terraform workspace found when running the module
        if workspace_ctx.current != workspace:
            terraform.workspace(WorkspaceCommand.SELECT, workspace_ctx.current)
        if computed_state == "absent" and workspace != "default" and purge_workspace is True:
            terraform.workspace(WorkspaceCommand.DELETE, workspace)

        diff = dict(
            before=dataclasses.asdict(initial_state) if initial_state is not None else {},
            after=dataclasses.asdict(final_state) if final_state is not None else {},
        )

        module.exit_json(
            changed=plan_file_needs_application,
            diff=diff,
            state=computed_state,
            workspace=workspace,
            outputs=outputs,
            stdout=out,
            stderr=err,
            command=final_apply_command,
        )
    except TerraformError as e:
        e.fail_json(module)


if __name__ == "__main__":
    main()
