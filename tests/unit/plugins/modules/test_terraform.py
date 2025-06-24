# -*- coding: utf-8 -*-
# Copyright: (c) 2022, XLAB Steampunk <steampunk@xlab.si>
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

import os
import tempfile

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
)
from ansible_collections.cloud.terraform.plugins.modules.terraform import (
    clean_tf_file,
    extract_workspace_from_terraform_config,
    filter_outputs,
    filter_resource_attributes,
    is_attribute_in_sensitive_values,
    is_attribute_sensitive_in_providers_schema,
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
                resources=[root_module_resource, sensitive_root_module_resource],
                child_modules=[],
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
    def test_sensitive_attributes(
        self,
        provider_schemas,
        sensitive_root_module_resource,
        attribute,
        expected_result,
    ):
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


class TestCleanTfFile:
    """Test cases for the clean_tf_file function."""

    @pytest.mark.parametrize(
        "tf_content,expected",
        [
            (
                """
resource "aws_instance" "example" {
  # This is a comment
  ami           = "ami-12345678"
  instance_type = "t2.micro"
  # Another comment
}
""",
                """resource "aws_instance" "example" {
  ami           = "ami-12345678"
  instance_type = "t2.micro"
}""",
            ),
            (
                """
resource "aws_instance" "example" {
  // This is a comment
  ami           = "ami-12345678"
  instance_type = "t2.micro"
  // Another comment
}
""",
                """resource "aws_instance" "example" {
  ami           = "ami-12345678"
  instance_type = "t2.micro"
}""",
            ),
            (
                """
resource "aws_instance" "example" {
  /* This is a
     multiline comment */
  ami           = "ami-12345678"
  instance_type = "t2.micro"
  /* Another multiline
     comment here */
}
""",
                """resource "aws_instance" "example" {
  ami           = "ami-12345678"
  instance_type = "t2.micro"
}""",
            ),
            (
                """
# Top level comment
resource "aws_instance" "example" {
  /* Multiline comment
     spanning multiple lines */
  ami           = "ami-12345678"  # Inline hash comment
  instance_type = "t2.micro"     // Inline double slash comment
  # Another hash comment
}
// Bottom comment
""",
                """resource "aws_instance" "example" {
  ami           = "ami-12345678"
  instance_type = "t2.micro"
}""",
            ),
            (
                """
resource "aws_instance" "example" {
  ami           = "ami-12345678"
  user_data     = "#!/bin/bash\\necho 'Hello # World // Test'"
  instance_type = "t2.micro"
}
""",
                """resource "aws_instance" "example" {
  ami           = "ami-12345678"
  user_data     = "#!/bin/bash\\necho 'Hello # World // Test'"
  instance_type = "t2.micro"
}""",
            ),
            (
                """

resource "aws_instance" "example" {

  ami           = "ami-12345678"

  instance_type = "t2.micro"

}

""",
                """resource "aws_instance" "example" {
  ami           = "ami-12345678"
  instance_type = "t2.micro"
}""",
            ),
            (
                "",
                "",
            ),
            (
                """
# This is a comment
// Another comment
/* Multiline
   comment */
""",
                "",
            ),
        ],
    )
    def test_clean_tf_file(self, tf_content, expected):
        result = clean_tf_file(tf_content)
        assert result == expected


class TestExtractWorkspaceFromTerraformConfig:
    """Test cases for the extract_workspace_from_terraform_config function using real files."""

    def test_terraform_files_no_cloud_block(self):
        """Test .tf files without cloud block."""
        tf_content = """
        resource "aws_instance" "example" {
          ami           = "ami-12345678"
          instance_type = "t2.micro"
        }
        """
        with tempfile.TemporaryDirectory() as tmpdir:
            file_path = os.path.join(tmpdir, "main.tf")
            with open(file_path, "w") as f:
                f.write(tf_content)

            result = extract_workspace_from_terraform_config(tmpdir)
            assert result == (None, "cli")

    def test_cloud_block_with_workspace_name(self):
        """Test cloud block with workspace name."""
        tf_content = """
        terraform {
          cloud {
            organization = "my-org"
            workspaces {
              name = "my-workspace"
            }
          }
        }
        """
        with tempfile.TemporaryDirectory() as tmpdir:
            file_path = os.path.join(tmpdir, "main.tf")
            with open(file_path, "w") as f:
                f.write(tf_content)

            result = extract_workspace_from_terraform_config(tmpdir)
            assert result == ("my-workspace", "cloud")

    def test_cloud_block_with_comments(self):
        """Test cloud block with comments that should be cleaned."""
        tf_content = """
        terraform {
          # This is a comment
          cloud {
            organization = "my-org"
            /* This is a multiline
               comment */
            workspaces {
              name = "production-workspace"  // Inline comment
            }
          }
        }
        """
        with tempfile.TemporaryDirectory() as tmpdir:
            file_path = os.path.join(tmpdir, "main.tf")
            with open(file_path, "w") as f:
                f.write(tf_content)

            result = extract_workspace_from_terraform_config(tmpdir)
            assert result == ("production-workspace", "cloud")

    def test_workspace_with_special_characters(self):
        """Test workspace names with special characters."""
        tf_content = """
        terraform {
          cloud {
            organization = "my-org"
            workspaces {
              name = "my-workspace-123_test"
            }
          }
        }
        """
        with tempfile.TemporaryDirectory() as tmpdir:
            file_path = os.path.join(tmpdir, "main.tf")
            with open(file_path, "w") as f:
                f.write(tf_content)

            result = extract_workspace_from_terraform_config(tmpdir)
            assert result == ("my-workspace-123_test", "cloud")
    
    def test_cloud_block_without_workspace(self):
        """Test workspace names with special characters."""
        tf_content = """
        terraform {
          cloud {
            organization = "my-org"
          }
        }
        """
        with tempfile.TemporaryDirectory() as tmpdir:
            file_path = os.path.join(tmpdir, "main.tf")
            with open(file_path, "w") as f:
                f.write(tf_content)

            result = extract_workspace_from_terraform_config(tmpdir)
            assert result == (None, "cloud")