# -*- coding: utf-8 -*-
# Copyright: (c) 2022, XLAB Steampunk <steampunk@xlab.si>
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

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

    def test_remove_single_line_comments_hash(self):
        """Test removal of single-line comments starting with #."""
        tf_content = """
resource "aws_instance" "example" {
  # This is a comment
  ami           = "ami-12345678"
  instance_type = "t2.micro"
  # Another comment
}
"""
        expected = """resource "aws_instance" "example" {
  ami           = "ami-12345678"
  instance_type = "t2.micro"
}"""

        result = clean_tf_file(tf_content)
        assert result == expected

    def test_remove_single_line_comments_double_slash(self):
        """Test removal of single-line comments starting with //."""
        tf_content = """
resource "aws_instance" "example" {
  // This is a comment
  ami           = "ami-12345678"
  instance_type = "t2.micro"
  // Another comment
}
"""
        expected = """resource "aws_instance" "example" {
  ami           = "ami-12345678"
  instance_type = "t2.micro"
}"""

        result = clean_tf_file(tf_content)
        assert result == expected

    def test_remove_multiline_comments(self):
        """Test removal of multiline comments /* */."""
        tf_content = """
resource "aws_instance" "example" {
  /* This is a
     multiline comment */
  ami           = "ami-12345678"
  instance_type = "t2.micro"
  /* Another multiline
     comment here */
}
"""
        expected = """resource "aws_instance" "example" {
  ami           = "ami-12345678"
  instance_type = "t2.micro"
}"""

        result = clean_tf_file(tf_content)
        assert result == expected

    def test_remove_mixed_comments(self):
        """Test removal of mixed comment types."""
        tf_content = """
# Top level comment
resource "aws_instance" "example" {
  /* Multiline comment
     spanning multiple lines */
  ami           = "ami-12345678"  # Inline hash comment
  instance_type = "t2.micro"     // Inline double slash comment
  # Another hash comment
}
// Bottom comment
"""
        expected = """resource "aws_instance" "example" {
  ami           = "ami-12345678"
  instance_type = "t2.micro"
}"""

        result = clean_tf_file(tf_content)
        assert result == expected

    def test_preserve_strings_with_comment_chars(self):
        """Test that comment characters inside strings are preserved."""
        tf_content = """
resource "aws_instance" "example" {
  ami           = "ami-12345678"
  user_data     = "#!/bin/bash\\necho 'Hello # World // Test'"
  instance_type = "t2.micro"
}
"""
        expected = """resource "aws_instance" "example" {
  ami           = "ami-12345678"
  user_data     = "#!/bin/bash\\necho 'Hello # World // Test'"
  instance_type = "t2.micro"
}"""

        result = clean_tf_file(tf_content)
        assert result == expected

    def test_remove_empty_lines(self):
        """Test removal of empty lines and lines with only whitespace."""
        tf_content = """

resource "aws_instance" "example" {

  ami           = "ami-12345678"

  instance_type = "t2.micro"

}

"""
        expected = """resource "aws_instance" "example" {
  ami           = "ami-12345678"
  instance_type = "t2.micro"
}"""

        result = clean_tf_file(tf_content)
        assert result == expected

    def test_empty_string(self):
        """Test handling of empty string input."""
        tf_content = ""
        expected = ""

        result = clean_tf_file(tf_content)
        assert result == expected

    def test_only_comments(self):
        """Test file with only comments."""
        tf_content = """
# This is a comment
// Another comment
/* Multiline
   comment */
"""
        expected = ""

        result = clean_tf_file(tf_content)
        assert result == expected

    def test_nested_multiline_comments(self):
        """Test handling of nested-like multiline comments."""
        tf_content = """
resource "aws_instance" "example" {
  /* Comment with /* nested-like */ content */
  ami = "ami-12345678"
}
"""
        expected = """resource "aws_instance" "example" {
  ami = "ami-12345678"
}"""

        result = clean_tf_file(tf_content)
        assert result == expected


# class TestExtractWorkspaceFromTerraformConfig:
#     """Test cases for the extract_workspace_from_terraform_config function."""

#     def test_nonexistent_directory(self):
#         """Test handling of nonexistent project directory."""
#         result = extract_workspace_from_terraform_config("/nonexistent/path")
#         assert result == (None, "cli")

#     @patch("os.path.exists")
#     @patch("os.listdir")
#     @patch("builtins.open", new_callable=mock_open)
#     def test_terraform_files_no_cloud_block(self, mock_file, mock_listdir, mock_exists):
#         """Test .tf files without cloud block."""
#         mock_exists.return_value = True
#         mock_listdir.return_value = ["main.tf"]
#         mock_file.return_value.read.return_value = """
# resource "aws_instance" "example" {
#   ami           = "ami-12345678"
#   instance_type = "t2.micro"
# }
# """

#         result = extract_workspace_from_terraform_config("/no/cloud/block")
#         assert result == (None, "cli")

#     @patch("os.path.exists")
#     @patch("os.listdir")
#     @patch("builtins.open", new_callable=mock_open)
#     def test_cloud_block_with_workspace_name(self, mock_file, mock_listdir, mock_exists):
#         """Test cloud block with workspace name."""
#         mock_exists.return_value = True
#         mock_listdir.return_value = ["main.tf"]
#         mock_file.return_value.read.return_value = """
# terraform {
#   cloud {
#     organization = "my-org"
#     workspaces {
#       name = "my-workspace"
#     }
#   }
# }

# resource "aws_instance" "example" {
#   ami           = "ami-12345678"
#   instance_type = "t2.micro"
# }
# """

#         result = extract_workspace_from_terraform_config("/with/workspace")
#         assert result == ("my-workspace", "cloud")

#     @patch("os.path.exists")
#     @patch("os.listdir")
#     @patch("builtins.open", new_callable=mock_open)
#     def test_cloud_block_without_workspace_name(self, mock_file, mock_listdir, mock_exists):
#         """Test cloud block without workspace name."""
#         mock_exists.return_value = True
#         mock_listdir.return_value = ["main.tf"]
#         mock_file.return_value.read.return_value = """
# terraform {
#   cloud {
#     organization = "my-org"
#   }
# }

# resource "aws_instance" "example" {
#   ami           = "ami-12345678"
#   instance_type = "t2.micro"
# }
# """

#         result = extract_workspace_from_terraform_config("/cloud/no/workspace")
#         assert result == (None, "cloud")

#     @patch("os.path.exists")
#     @patch("os.listdir")
#     @patch("builtins.open", new_callable=mock_open)
#     def test_cloud_block_with_comments(self, mock_file, mock_listdir, mock_exists):
#         """Test cloud block with comments that should be cleaned."""
#         mock_exists.return_value = True
#         mock_listdir.return_value = ["main.tf"]
#         mock_file.return_value.read.return_value = """
# terraform {
#   # This is a comment
#   cloud {
#     organization = "my-org"
#     /* This is a multiline
#        comment */
#     workspaces {
#       name = "production-workspace"  // Inline comment
#     }
#   }
# }
# """

#         result = extract_workspace_from_terraform_config("/with/comments")
#         assert result == ("production-workspace", "cloud")

#     @patch("os.path.exists")
#     @patch("os.listdir")
#     @patch("builtins.open", new_callable=mock_open)
#     def test_multiple_terraform_files_first_has_cloud(self, mock_file, mock_listdir, mock_exists):
#         """Test multiple .tf files where first file has cloud block."""
#         mock_exists.return_value = True
#         mock_listdir.return_value = ["main.tf", "variables.tf", "backend.tf"]

#         # Mock file reads - main.tf has cloud block
#         def side_effect(*args, **kwargs):
#             filename = args[0]
#             if "main.tf" in filename:
#                 mock_file.return_value.read.return_value = """
# terraform {
#   cloud {
#     organization = "my-org"
#     workspaces {
#       name = "dev-workspace"
#     }
#   }
# }
# """
#             else:
#                 mock_file.return_value.read.return_value = "# Just variables"
#             return mock_file.return_value

#         mock_file.side_effect = side_effect

#         result = extract_workspace_from_terraform_config("/multiple/files")
#         assert result == ("dev-workspace", "cloud")

#     @patch("os.path.exists")
#     @patch("os.listdir")
#     @patch("builtins.open", new_callable=mock_open)
#     def test_excluded_files_ignored(self, mock_file, mock_listdir, mock_exists):
#         """Test that excluded files (vars.tf, var.tf, etc.) are ignored."""
#         mock_exists.return_value = True
#         mock_listdir.return_value = ["vars.tf", "var.tf", "provider.tf", "variables.tf", "outputs.tf", "main.tf"]

#         def side_effect(*args, **kwargs):
#             filename = args[0]
#             if "main.tf" in filename:
#                 mock_file.return_value.read.return_value = """
# terraform {
#   cloud {
#     organization = "my-org"
#     workspaces {
#       name = "test-workspace"
#     }
#   }
# }
# """
#             else:
#                 # These shouldn't be read due to exclusion
#                 mock_file.return_value.read.return_value = """
# terraform {
#   cloud {
#     organization = "wrong-org"
#     workspaces {
#       name = "wrong-workspace"
#     }
#   }
# }
# """
#             return mock_file.return_value

#         mock_file.side_effect = side_effect

#         result = extract_workspace_from_terraform_config("/with/excluded")
#         assert result == ("test-workspace", "cloud")

#     @patch("os.path.exists")
#     @patch("os.listdir")
#     @patch("builtins.open")
#     def test_file_read_error(self, mock_file, mock_listdir, mock_exists):
#         """Test handling of file read errors."""
#         mock_exists.return_value = True
#         mock_listdir.return_value = ["main.tf", "backup.tf"]

#         # First file throws IOError, second file is valid
#         def side_effect(*args, **kwargs):
#             filename = args[0]
#             if "main.tf" in filename:
#                 raise IOError("Permission denied")
#             else:
#                 return mock_open(
#                     read_data="""
# terraform {
#   cloud {
#     organization = "my-org"
#     workspaces {
#       name = "backup-workspace"
#     }
#   }
# }
# """
#                 ).return_value

#         mock_file.side_effect = side_effect

#         result = extract_workspace_from_terraform_config("/with/error")
#         assert result == ("backup-workspace", "cloud")

#     @patch("os.path.exists")
#     @patch("os.listdir")
#     @patch("builtins.open")
#     def test_unicode_decode_error(self, mock_file, mock_listdir, mock_exists):
#         """Test handling of Unicode decode errors."""
#         mock_exists.return_value = True
#         mock_listdir.return_value = ["binary.tf", "text.tf"]

#         # First file throws UnicodeDecodeError, second file is valid
#         def side_effect(*args, **kwargs):
#             filename = args[0]
#             if "binary.tf" in filename:
#                 raise UnicodeDecodeError("utf-8", b"", 0, 1, "invalid start byte")
#             else:
#                 return mock_open(
#                     read_data="""
# terraform {
#   cloud {
#     organization = "my-org"
#     workspaces {
#       name = "text-workspace"
#     }
#   }
# }
# """
#                 ).return_value

#         mock_file.side_effect = side_effect

#         result = extract_workspace_from_terraform_config("/with/unicode/error")
#         assert result == ("text-workspace", "cloud")

#     @patch("os.path.exists")
#     @patch("os.listdir")
#     def test_os_error_on_listdir(self, mock_listdir, mock_exists):
#         """Test handling of OS errors when listing directory."""
#         mock_exists.return_value = True
#         mock_listdir.side_effect = OSError("Permission denied")

#         result = extract_workspace_from_terraform_config("/permission/denied")
#         assert result == (None, "cli")

#     @patch("os.path.exists")
#     @patch("os.listdir")
#     @patch("builtins.open", new_callable=mock_open)
#     def test_case_insensitive_matching(self, mock_file, mock_listdir, mock_exists):
#         """Test case-insensitive matching of cloud and workspace blocks."""
#         mock_exists.return_value = True
#         mock_listdir.return_value = ["main.tf"]
#         mock_file.return_value.read.return_value = """
# terraform {
#   CLOUD {
#     organization = "my-org"
#     WORKSPACES {
#       NAME = "case-insensitive-workspace"
#     }
#   }
# }
# """

#         result = extract_workspace_from_terraform_config("/case/insensitive")
#         assert result == ("case-insensitive-workspace", "cloud")

#     @patch("os.path.exists")
#     @patch("os.listdir")
#     @patch("builtins.open", new_callable=mock_open)
#     def test_workspace_with_special_characters(self, mock_file, mock_listdir, mock_exists):
#         """Test workspace names with special characters."""
#         mock_exists.return_value = True
#         mock_listdir.return_value = ["main.tf"]
#         mock_file.return_value.read.return_value = """
# terraform {
#   cloud {
#     organization = "my-org"
#     workspaces {
#       name = "my-workspace-123_test"
#     }
#   }
# }
# """

#         result = extract_workspace_from_terraform_config("/special/chars")
#         assert result == ("my-workspace-123_test", "cloud")

#     @patch("os.path.exists")
#     @patch("os.listdir")
#     @patch("builtins.open", new_callable=mock_open)
#     def test_malformed_cloud_block(self, mock_file, mock_listdir, mock_exists):
#         """Test handling of malformed cloud block."""
#         mock_exists.return_value = True
#         mock_listdir.return_value = ["main.tf"]
#         mock_file.return_value.read.return_value = """
# terraform {
#   cloud {
#     organization = "my-org"
#     workspaces {
#       # Missing closing brace
#       name = "malformed-workspace"
#     }
#   # Missing closing brace for cloud
# }
# """

#         # Should still detect cloud mode even if malformed
#         result = extract_workspace_from_terraform_config("/malformed")
#         assert result == ("malformed-workspace", "cloud")
