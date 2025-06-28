# -*- coding: utf-8 -*-
# Copyright: (c) 2022, XLAB Steampunk <steampunk@xlab.si>
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from unittest.mock import MagicMock, patch

import pytest
from ansible_collections.cloud.terraform.plugins.module_utils.models import (
    TerraformAttributeSpec,
    TerraformBlockSensitive,
    TerraformNestedAttributeSpec,
    TerraformOutput,
    TerraformProviderSchema,
    TerraformProviderSchemaCollection,
    TerraformResourceSchema,
    TerraformRootModule,
    TerraformRootModuleResource,
    TerraformShow,
    TerraformShowValues,
    TerraformSimpleAttributeSpec,
    TerraformWorkspaceContext,
)
from ansible_collections.cloud.terraform.plugins.modules.terraform import (
    filter_outputs,
    filter_resource_attributes,
    is_attribute_in_sensitive_values,
    is_attribute_sensitive_in_providers_schema,
    main,
    sanitize_state,
)


@pytest.fixture
def sensitive_root_module_resource():
    return TerraformRootModuleResource(
        address="local_sensitive_file.sensitive_foo",
        mode="managed",
        type="local_sensitive_file",
        name="sensitive_foo",
        provider_name="registry.terraform.io/hashicorp/local",
        schema_version=0,
        values={
            "content": "sensitive_content",
            "content_base64": None,
            "directory_permission": "0700",
            "file_permission": "0700",
            "filename": "./sensitive_file_name.txt",
            "id": "ba2561b92867583049c9d0ac9cd46a9cc17e38be",
            "source": None,
            "resource_block": [{"resource_block_attribute": {"resource_block_nested_attribute": "value"}}],
            "missing_in_providers_schema": "value",
        },
        sensitive_values={
            "filename": True,
            "resource_block": [{"resource_block_attribute": {"resource_block_nested_attribute": True}}],
            "missing_in_providers_schema": True,
        },
        depends_on=[],
    )


@pytest.fixture
def root_module_resource():
    return TerraformRootModuleResource(
        address="local_file.foo",
        mode="managed",
        type="local_file",
        name="foo",
        provider_name="registry.terraform.io/hashicorp/local",
        schema_version=0,
        values={
            "content": "content",
            "content_base64": None,
            "directory_permission": "0700",
            "file_permission": "0700",
            "filename": "./file_name.txt",
            "id": "ba2561b92867583049c9d0ac9cd46a9cc17e38be",
            "source": None,
            "resource_block": [{"resource_block_attribute": {"resource_block_nested_attribute": "value"}}],
            "missing_in_providers_schema": "value",
        },
        sensitive_values={"resource_block": []},
        depends_on=[],
    )


@pytest.fixture
def provider_schemas():
    return TerraformProviderSchemaCollection(
        format_version="1.0",
        provider_schemas={
            "registry.terraform.io/hashicorp/local": TerraformProviderSchema(
                resource_schemas={
                    "local_file": TerraformResourceSchema(
                        version=0,
                        attributes={
                            "content": TerraformSimpleAttributeSpec(
                                type="string",
                                description_kind="plain",
                                description="Content to store in the file, expected to be an UTF-8 encoded string.",
                                optional=True,
                                required=False,
                                deprecated=False,
                                sensitive=False,
                                computed=False,
                            ),
                            "content_base64": TerraformSimpleAttributeSpec(
                                type="string",
                                description_kind="plain",
                                description="Content to store in the file, expected to be binary encoded as base64 string.",
                                optional=True,
                                required=False,
                                deprecated=False,
                                sensitive=False,
                                computed=False,
                            ),
                            "directory_permission": TerraformSimpleAttributeSpec(
                                type="string",
                                description_kind="plain",
                                description="Permissions to set for directories created (in numeric notation).",
                                optional=True,
                                required=False,
                                deprecated=False,
                                sensitive=False,
                                computed=False,
                            ),
                            "file_permission": TerraformSimpleAttributeSpec(
                                type="string",
                                description_kind="plain",
                                description="Permissions to set for the output file (in numeric notation).",
                                optional=True,
                                required=False,
                                deprecated=False,
                                sensitive=False,
                                computed=False,
                            ),
                            "filename": TerraformSimpleAttributeSpec(
                                type="string",
                                description_kind="plain",
                                description="The path to the file that will be created.",
                                optional=False,
                                required=True,
                                deprecated=False,
                                sensitive=False,
                                computed=False,
                            ),
                            "id": TerraformSimpleAttributeSpec(
                                type="string",
                                description_kind="plain",
                                description="description",
                                optional=True,
                                required=False,
                                deprecated=False,
                                sensitive=False,
                                computed=True,
                            ),
                            "sensitive_content": TerraformSimpleAttributeSpec(
                                type="string",
                                description_kind="plain",
                                description="Sensitive content to store in the file, expected to be an UTF-8 encoded string.",
                                optional=True,
                                required=False,
                                deprecated=True,
                                sensitive=True,
                                computed=False,
                            ),
                            "source": TerraformSimpleAttributeSpec(
                                type="string",
                                description_kind="plain",
                                description="Path to file to use as source for the one we are creating.",
                                optional=True,
                                required=False,
                                deprecated=False,
                                sensitive=False,
                                computed=False,
                            ),
                            "description": "Generates a local file with the given content.",
                            "description_kind": "plain",
                            "resource_block": TerraformBlockSensitive(sensitive=False),
                        },
                    ),
                    "local_sensitive_file": TerraformResourceSchema(
                        version=0,
                        attributes={
                            "content": TerraformSimpleAttributeSpec(
                                type="string",
                                description_kind="plain",
                                description="Content to store in the file, expected to be an UTF-8 encoded string.",
                                optional=True,
                                required=False,
                                deprecated=False,
                                sensitive=True,
                                computed=False,
                            ),
                            "content_base64": TerraformSimpleAttributeSpec(
                                type="string",
                                description_kind="plain",
                                description="Content to store in the file, expected to be binary encoded as base64 string.",
                                optional=True,
                                required=False,
                                deprecated=False,
                                sensitive=True,
                                computed=False,
                            ),
                            "directory_permission": TerraformSimpleAttributeSpec(
                                type="string",
                                description_kind="plain",
                                description="Permissions to set for directories created (in numeric notation).",
                                optional=True,
                                required=False,
                                deprecated=False,
                                sensitive=False,
                                computed=False,
                            ),
                            "file_permission": TerraformSimpleAttributeSpec(
                                type="string",
                                description_kind="plain",
                                description="Permissions to set for the output file (in numeric notation).",
                                optional=True,
                                required=False,
                                deprecated=False,
                                sensitive=False,
                                computed=False,
                            ),
                            "filename": TerraformSimpleAttributeSpec(
                                type="string",
                                description_kind="plain",
                                description="The path to the file that will be created.",
                                optional=False,
                                required=True,
                                deprecated=False,
                                sensitive=False,
                                computed=False,
                            ),
                            "id": TerraformSimpleAttributeSpec(
                                type="string",
                                description_kind="plain",
                                description="description",
                                optional=True,
                                required=False,
                                deprecated=False,
                                sensitive=False,
                                computed=True,
                            ),
                            "source": TerraformSimpleAttributeSpec(
                                type="string",
                                description_kind="plain",
                                description="Path to file to use as source for the one we are creating.",
                                optional=True,
                                required=False,
                                deprecated=False,
                                sensitive=False,
                                computed=False,
                            ),
                            "description": "Generates a local file with the given sensitive content.",
                            "description_kind": "plain",
                            "resource_block": TerraformBlockSensitive(sensitive=True),
                        },
                    ),
                },
            ),
        },
    )


@pytest.fixture
def state_contents(root_module_resource, sensitive_root_module_resource):
    return TerraformShow(
        format_version="1.0",
        terraform_version="1.3.6",
        values=TerraformShowValues(
            outputs={
                "my_output": TerraformOutput(sensitive=False, value="my_value", type="string"),
                "my_sensitive_output": TerraformOutput(sensitive=True, value="my_sensitive_value", type="string"),
            },
            root_module=TerraformRootModule(
                resources=[root_module_resource, sensitive_root_module_resource], child_modules=[]
            ),
        ),
    )


class TestIsAttributeSensitiveInProvidersSchema:
    @pytest.mark.parametrize(
        "attribute, expected_result",
        [
            ("content", False),
            ("resource_block", False),
            ("missing_in_providers_schema", False),
        ],
    )
    def test_not_sensitive_attributes(self, provider_schemas, root_module_resource, attribute, expected_result):
        result = is_attribute_sensitive_in_providers_schema(provider_schemas, root_module_resource, attribute=attribute)
        assert result == expected_result

    @pytest.mark.parametrize(
        "attribute, expected_result",
        [
            ("content", True),
            ("content_base64", True),
            ("resource_block", True),
        ],
    )
    def test_sensitive_attributes(self, provider_schemas, sensitive_root_module_resource, attribute, expected_result):
        result = is_attribute_sensitive_in_providers_schema(
            provider_schemas, sensitive_root_module_resource, attribute=attribute
        )
        assert result == expected_result


class TestIsAttributeInSensitiveValues:
    @pytest.mark.parametrize(
        "attribute, expected_result",
        [
            ("content", False),
            ("content_base64", False),
            ("resource_block", False),
        ],
    )
    def test_not_in_sensitive_values(self, root_module_resource, attribute, expected_result):
        result = is_attribute_in_sensitive_values(root_module_resource, attribute=attribute)
        assert result == expected_result

    @pytest.mark.parametrize(
        "attribute, expected_result",
        [
            ("content", False),
            ("filename", True),
            ("resource_block", True),
            ("missing_in_providers_schema", True),
        ],
    )
    def test_in_sensitive_values(self, sensitive_root_module_resource, attribute, expected_result):
        result = is_attribute_in_sensitive_values(sensitive_root_module_resource, attribute=attribute)
        assert result == expected_result


class TestFilterResourceAttributes:
    def test_filter_resource_attributes(self, state_contents, provider_schemas):
        filtered_attributes = filter_resource_attributes(state_contents, provider_schemas)
        assert filtered_attributes.values.root_module.resources[0] == TerraformRootModuleResource(
            address="local_file.foo",
            mode="managed",
            type="local_file",
            name="foo",
            provider_name="registry.terraform.io/hashicorp/local",
            schema_version=0,
            values={
                "content": "content",
                "content_base64": None,
                "directory_permission": "0700",
                "file_permission": "0700",
                "filename": "./file_name.txt",
                "id": "ba2561b92867583049c9d0ac9cd46a9cc17e38be",
                "source": None,
                "resource_block": [{"resource_block_attribute": {"resource_block_nested_attribute": "value"}}],
                "missing_in_providers_schema": "value",
            },
            sensitive_values={"resource_block": []},
            depends_on=[],
        )
        assert filtered_attributes.values.root_module.resources[1] == TerraformRootModuleResource(
            address="local_sensitive_file.sensitive_foo",
            mode="managed",
            type="local_sensitive_file",
            name="sensitive_foo",
            provider_name="registry.terraform.io/hashicorp/local",
            schema_version=0,
            values={
                "content": None,  # Filtered
                "content_base64": None,
                "directory_permission": "0700",
                "file_permission": "0700",
                "filename": None,  # Filtered
                "id": "ba2561b92867583049c9d0ac9cd46a9cc17e38be",
                "source": None,
                "resource_block": None,  # Filtered
                "missing_in_providers_schema": None,  # Filtered
            },
            sensitive_values={
                "filename": True,
                "resource_block": [{"resource_block_attribute": {"resource_block_nested_attribute": True}}],
                "missing_in_providers_schema": True,
            },
            depends_on=[],
        )


class TestFilterOutputs:
    def test_filter_outputs(self, state_contents):
        filtered_outputs = filter_outputs(state_contents)
        assert filtered_outputs.values.outputs["my_output"].value == "my_value"
        assert filtered_outputs.values.outputs["my_sensitive_output"].value is None


class TestSanitizeState:
    def test_sanitize_state(self, state_contents, provider_schemas):
        filtered_state = sanitize_state(state_contents, provider_schemas)
        assert filtered_state == TerraformShow(
            format_version="1.0",
            terraform_version="1.3.6",
            values=TerraformShowValues(
                outputs={
                    "my_output": TerraformOutput(sensitive=False, value="my_value", type="string"),
                    "my_sensitive_output": TerraformOutput(sensitive=True, value=None, type="string"),
                },
                root_module=TerraformRootModule(
                    resources=[
                        TerraformRootModuleResource(
                            address="local_file.foo",
                            mode="managed",
                            type="local_file",
                            name="foo",
                            provider_name="registry.terraform.io/hashicorp/local",
                            schema_version=0,
                            values={
                                "content": "content",
                                "content_base64": None,
                                "directory_permission": "0700",
                                "file_permission": "0700",
                                "filename": "./file_name.txt",
                                "id": "ba2561b92867583049c9d0ac9cd46a9cc17e38be",
                                "source": None,
                                "resource_block": [
                                    {"resource_block_attribute": {"resource_block_nested_attribute": "value"}}
                                ],
                                "missing_in_providers_schema": "value",
                            },
                            sensitive_values={"resource_block": []},
                            depends_on=[],
                        ),
                        TerraformRootModuleResource(
                            address="local_sensitive_file.sensitive_foo",
                            mode="managed",
                            type="local_sensitive_file",
                            name="sensitive_foo",
                            provider_name="registry.terraform.io/hashicorp/local",
                            schema_version=0,
                            values={
                                "content": None,  # Filtered
                                "content_base64": None,
                                "directory_permission": "0700",
                                "file_permission": "0700",
                                "filename": None,  # Filtered
                                "id": "ba2561b92867583049c9d0ac9cd46a9cc17e38be",
                                "source": None,
                                "resource_block": None,  # Filtered
                                "missing_in_providers_schema": None,  # Filtered
                            },
                            sensitive_values={
                                "filename": True,
                                "resource_block": [
                                    {"resource_block_attribute": {"resource_block_nested_attribute": True}}
                                ],
                                "missing_in_providers_schema": True,
                            },
                            depends_on=[],
                        ),
                    ],
                    child_modules=[],
                ),
            ),
        )


class TestTerraformResourceSchema:
    def test_from_json(self):
        resource = {
            "version": "version",
            "block": {
                "attributes": {
                    "attribute_name": {
                        "type": "type",
                        "description_kind": "description_kind",
                        "description": "description",
                        "required": True,
                        "optional": False,
                        "computed": True,
                        "sensitive": False,
                    },
                },
                "block_types": {
                    "block_name": {
                        "nesting_mode": "list",
                        "block": {
                            "attributes": {
                                "block_attribute_name": {
                                    "type": "block_type",
                                    "description_kind": "block_description_kind",
                                    "description": "block_description",
                                    "required": False,
                                    "optional": True,
                                    "computed": False,
                                    "sensitive": True,
                                },
                            },
                            "block_types": {
                                "nested_block_name": {
                                    "nesting_mode": "list",
                                    "block": "block-representation",
                                    "min_items": 1,
                                    "max_items": 3,
                                },
                            },
                        },
                        "min_items": 1,
                        "max_items": 3,
                    },
                },
            },
        }

        expected_terraform_resource_schema = TerraformResourceSchema(
            version="version",
            attributes={
                "attribute_name": TerraformSimpleAttributeSpec(
                    type="type",
                    description_kind="description_kind",
                    description="description",
                    required=True,
                    optional=False,
                    computed=True,
                    sensitive=False,
                    deprecated=False,
                ),
                "block_name": TerraformBlockSensitive(sensitive=True),
            },
        )

        terraform_resource_schema = TerraformResourceSchema.from_json(resource)

        assert terraform_resource_schema == expected_terraform_resource_schema


class TestTerraformAttributeSpec:
    def test_from_json_nested(self):
        # terraform providers schema -json | \
        # jq '.provider_schemas["registry.terraform.io/hashicorp/waypoint"].resource_schemas.waypoint_project.block.attributes.git_auth_basic'
        resource = {
            "nested_type": {
                "attributes": {
                    "password": {
                        "type": "string",
                        "description": "Git password",
                        "description_kind": "plain",
                        "required": True,
                        "sensitive": True,
                    },
                    "username": {
                        "type": "string",
                        "description": "Git username",
                        "description_kind": "plain",
                        "required": True,
                    },
                },
                "nesting_mode": "single",
            },
            "description": "Basic authentication details for Git consisting of `username` and `password`",
            "description_kind": "plain",
            "optional": True,
            "sensitive": True,
        }

        expected_terraform_attribute_spec = TerraformNestedAttributeSpec(
            nested_attributes={
                "password": TerraformSimpleAttributeSpec(
                    type="string",
                    description_kind="plain",
                    description="Git password",
                    required=True,
                    optional=False,
                    computed=False,
                    sensitive=True,
                    deprecated=False,
                ),
                "username": TerraformSimpleAttributeSpec(
                    type="string",
                    description_kind="plain",
                    description="Git username",
                    required=True,
                    optional=False,
                    computed=False,
                    sensitive=False,
                    deprecated=False,
                ),
            },
            description_kind="plain",
            description="Basic authentication details for Git consisting of `username` and `password`",
            required=False,
            optional=True,
            computed=False,
            sensitive=True,
            deprecated=False,
        )

        terraform_attribute_spec = TerraformAttributeSpec.from_json(resource)

        assert terraform_attribute_spec == expected_terraform_attribute_spec


class TestTerraformMain:
    @patch("ansible_collections.cloud.terraform.plugins.modules.terraform.TerraformCommands")
    @patch("ansible_collections.cloud.terraform.plugins.modules.terraform.AnsibleModule")
    @patch("os.path.isdir", return_value=True)  # Mock directory existence check
    def test_non_default_workspace_selection(self, mock_isdir, mock_ansible_module, mock_terraform_commands):
        """
        Tests that the module correctly selects a non-default workspace when specified.
        """
        mock_module_instance = MagicMock()
        mock_module_instance.params = {
            "project_path": "/tmp/project",
            "workspace": "staging",
            "state": "present",
            "binary_path": None,
            "plugin_paths": None,
            "purge_workspace": False,
            "variables": {},
            "complex_vars": False,
            "variables_files": None,
            "plan_file": None,
            "state_file": None,
            "force_init": False,
            "backend_config": None,
            "backend_config_files": None,
            "init_reconfigure": False,
            "overwrite_init": True,
            "check_destroy": False,
            "provider_upgrade": False,
            "targets": [],
            "lock": True,
            "lock_timeout": None,
            "parallelism": None,
        }
        mock_module_instance.check_mode = True
        mock_module_instance.get_bin_path.return_value = "/usr/bin/terraform"  # Mock terraform binary path
        mock_ansible_module.return_value = mock_module_instance

        mock_tf_instance = MagicMock()
        mock_terraform_commands.return_value = mock_tf_instance

        mock_tf_instance.version.return_value = "1.3.0"
        mock_tf_instance.providers_schema.return_value = TerraformProviderSchemaCollection(
            format_version="1.0", provider_schemas={}
        )
        mock_tf_instance.show.return_value = None  # Simulate no initial state

        # Mock workspace list to simulate being in 'default' but 'staging' exists
        mock_tf_instance.workspace_list.return_value = TerraformWorkspaceContext(
            current="default", all=["default", "staging"]
        )

        # Mock the plan command to return 'no changes' for simplicity
        mock_tf_instance.plan.return_value = (False, False, "plan stdout", "plan stderr")

        # Run the module's main function
        with pytest.raises(SystemExit):  # main() calls module.exit_json which raises SystemExit
            main()

        # Verify that workspace selection was called correctly
        mock_tf_instance.workspace.assert_any_call("select", "staging")

        # Check that the module would exit with changed=False because the plan had no changes
        mock_module_instance.exit_json.assert_called_with(
            changed=False,  # Because our mocked plan returned changed=False
            diff=dict(before={}, after={}),
            state="present",
            workspace="staging",
            outputs={},
            stdout="plan stdout",
            stderr="plan stderr",
            command=None,  # command is from apply_plan, which is skipped in check_mode
        )
