# -*- coding: utf-8 -*-
# Copyright: (c) 2022, XLAB Steampunk <steampunk@xlab.si>
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

import pytest
from ansible_collections.cloud.terraform.plugins.module_utils.models import (
    TerraformRootModule,
    TerraformOutput,
    TerraformRootModuleResource,
    TerraformResourceSchema,
    TerraformShow,
    TerraformShowValues,
    TerraformProviderSchema,
    TerraformProviderSchemaCollection,
    TerraformAttributeSpec,
)
from ansible_collections.cloud.terraform.plugins.modules.terraform import (
    is_attribute_sensitive_in_providers_schema,
    is_attribute_in_sensitive_values,
    filter_resource_attributes,
    filter_outputs,
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
        },
        sensitive_values={"filename": True},
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
        },
        sensitive_values={},
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
                            "content": TerraformAttributeSpec(
                                type="string",
                                description_kind="plain",
                                description="Content to store in the file, expected to be an UTF-8 encoded string.",
                                optional=True,
                                required=False,
                                deprecated=False,
                                sensitive=False,
                                computed=False,
                            ),
                            "content_base64": TerraformAttributeSpec(
                                type="string",
                                description_kind="plain",
                                description="Content to store in the file, expected to be binary encoded as base64 string.",
                                optional=True,
                                required=False,
                                deprecated=False,
                                sensitive=False,
                                computed=False,
                            ),
                            "directory_permission": TerraformAttributeSpec(
                                type="string",
                                description_kind="plain",
                                description="Permissions to set for directories created (in numeric notation).",
                                optional=True,
                                required=False,
                                deprecated=False,
                                sensitive=False,
                                computed=False,
                            ),
                            "file_permission": TerraformAttributeSpec(
                                type="string",
                                description_kind="plain",
                                description="Permissions to set for the output file (in numeric notation).",
                                optional=True,
                                required=False,
                                deprecated=False,
                                sensitive=False,
                                computed=False,
                            ),
                            "filename": TerraformAttributeSpec(
                                type="string",
                                description_kind="plain",
                                description="The path to the file that will be created.",
                                optional=False,
                                required=True,
                                deprecated=False,
                                sensitive=False,
                                computed=False,
                            ),
                            "id": TerraformAttributeSpec(
                                type="string",
                                description_kind="plain",
                                description="description",
                                optional=True,
                                required=False,
                                deprecated=False,
                                sensitive=False,
                                computed=True,
                            ),
                            "sensitive_content": TerraformAttributeSpec(
                                type="string",
                                description_kind="plain",
                                description="Sensitive content to store in the file, expected to be an UTF-8 encoded string.",
                                optional=True,
                                required=False,
                                deprecated=True,
                                sensitive=True,
                                computed=False,
                            ),
                            "source": TerraformAttributeSpec(
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
                        },
                        block_types={},
                    ),
                    "local_sensitive_file": TerraformResourceSchema(
                        version=0,
                        attributes={
                            "content": TerraformAttributeSpec(
                                type="string",
                                description_kind="plain",
                                description="Content to store in the file, expected to be an UTF-8 encoded string.",
                                optional=True,
                                required=False,
                                deprecated=False,
                                sensitive=True,
                                computed=False,
                            ),
                            "content_base64": TerraformAttributeSpec(
                                type="string",
                                description_kind="plain",
                                description="Content to store in the file, expected to be binary encoded as base64 string.",
                                optional=True,
                                required=False,
                                deprecated=False,
                                sensitive=True,
                                computed=False,
                            ),
                            "directory_permission": TerraformAttributeSpec(
                                type="string",
                                description_kind="plain",
                                description="Permissions to set for directories created (in numeric notation).",
                                optional=True,
                                required=False,
                                deprecated=False,
                                sensitive=False,
                                computed=False,
                            ),
                            "file_permission": TerraformAttributeSpec(
                                type="string",
                                description_kind="plain",
                                description="Permissions to set for the output file (in numeric notation).",
                                optional=True,
                                required=False,
                                deprecated=False,
                                sensitive=False,
                                computed=False,
                            ),
                            "filename": TerraformAttributeSpec(
                                type="string",
                                description_kind="plain",
                                description="The path to the file that will be created.",
                                optional=False,
                                required=True,
                                deprecated=False,
                                sensitive=False,
                                computed=False,
                            ),
                            "id": TerraformAttributeSpec(
                                type="string",
                                description_kind="plain",
                                description="description",
                                optional=True,
                                required=False,
                                deprecated=False,
                                sensitive=False,
                                computed=True,
                            ),
                            "source": TerraformAttributeSpec(
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
                        },
                        block_types={},
                    ),
                }
            )
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
            root_module=TerraformRootModule(resources=[root_module_resource, sensitive_root_module_resource]),
        ),
    )


class TestIsAttributeSensitiveInProvidersSchema:
    def test_is_attribute_sensitive_in_providers_schema_false(self, provider_schemas, root_module_resource):
        assert not is_attribute_sensitive_in_providers_schema(
            provider_schemas, root_module_resource, attribute="content"
        )

    def test_is_attribute_sensitive_in_providers_schema_true(self, provider_schemas, sensitive_root_module_resource):
        assert is_attribute_sensitive_in_providers_schema(
            provider_schemas, sensitive_root_module_resource, attribute="content"
        )


class TestIsAttributeInSensitiveValues:
    def test_is_attribute_in_sensitive_values_false(self, root_module_resource):
        assert not is_attribute_in_sensitive_values(root_module_resource, attribute="filename")

    def test_is_attribute_in_sensitive_values_true(self, sensitive_root_module_resource):
        assert is_attribute_in_sensitive_values(sensitive_root_module_resource, attribute="filename")


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
            },
            sensitive_values={},
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
            },
            sensitive_values={"filename": True},
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
                            },
                            sensitive_values={},
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
                            },
                            sensitive_values={"filename": True},
                            depends_on=[],
                        ),
                    ]
                ),
            ),
        )
