from ansible_collections.cloud.terraform.plugins.module_utils.models import (
    TerraformModuleResource,
)


class TestTerraformModuleResource:
    def test_from_json(self):
        json_data = {
            "address": "aws_iam_role.this",
            "mode": "managed",
            "type": "aws_iam_role",
            "name": "this",
            "provider_name": "registry.terraform.io/hashicorp/aws",
            "schema_version": 0,
            "values": {
                "assume_role_policy": (
                    '{"Statement":[{"Action":"sts:AssumeRole","Effect":"Allow",'
                    '"Principal":{"Service":"lambda.amazonaws.com"},"Sid":""}],"Version":"2012-10-17"}'
                ),
                "description": None,
                "force_detach_policies": False,
                "max_session_duration": 3600,
                "name": "ansible-test-59219564-jcpc-sqs-role",
                "path": "/",
                "permissions_boundary": None,
                "tags": {
                    "Name": "ansible-test-59219564-jcpc-sqs",
                    "cloud_terraform_integration": "true",
                },
                "tags_all": {
                    "Name": "ansible-test-59219564-jcpc-sqs",
                    "cloud_terraform_integration": "true",
                },
            },
            "sensitive_values": {
                "inline_policy": [],
                "managed_policy_arns": [],
                "tags": {},
                "tags_all": {},
            },
        }

        tfm = TerraformModuleResource.from_json(json_data)

        assert "aws_iam_role.this" == tfm.address
        assert "managed" == tfm.mode
        assert "aws_iam_role" == tfm.type
        assert "this" == tfm.name
        assert "registry.terraform.io/hashicorp/aws" == tfm.provider_name
        assert 0 == tfm.schema_version
        # potentially undefined
        assert json_data["values"] == tfm.values
        assert json_data["sensitive_values"] == tfm.sensitive_values
        assert [] == tfm.depends_on

    def test_from_json__missing_values(self):
        json_data = {
            "address": "aws_sqs_queue_policy.this",
            "mode": "managed",
            "type": "aws_sqs_queue_policy",
            "name": "this",
            "provider_name": "registry.terraform.io/hashicorp/aws",
            "schema_version": 1,
            "sensitive_values": {},
        }

        tfm = TerraformModuleResource.from_json(json_data)

        assert "aws_sqs_queue_policy.this" == tfm.address
        assert "managed" == tfm.mode
        assert "aws_sqs_queue_policy" == tfm.type
        assert "this" == tfm.name
        assert "registry.terraform.io/hashicorp/aws" == tfm.provider_name
        assert 1 == tfm.schema_version
        # potentially undefined
        assert {} == tfm.values
        assert {} == tfm.sensitive_values
        assert [] == tfm.depends_on
