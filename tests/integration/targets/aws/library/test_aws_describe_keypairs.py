#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: Ansible Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

DOCUMENTATION = r"""
---
module: test_aws_describe_keypairs
short_description: Describes an EC2 key pair
description:
  - Describes the specified key pairs or all of your key pairs.
  - The use of this file is restricted to the integration test of collection cloud.terraform.
options:
  name:
    description:
      - Name of the key pair.
    required: true
    type: list
    elements: str

author:
  - "Aubin Bikouo (@abikouo)"
"""

EXAMPLES = r"""
- name: Describes an EC2 key pair
  test_aws_describe_keypairs:
    name: my_keypair

"""

RETURN = r"""
"""

from ansible_collections.amazon.aws.plugins.module_utils.modules import AnsibleAWSModule
from ansible_collections.amazon.aws.plugins.module_utils.botocore import is_boto3_error_code
from ansible_collections.amazon.aws.plugins.module_utils.retries import AWSRetry


def find_key_pair(ec2_client, names):
    try:
        key = ec2_client.describe_key_pairs(aws_retry=True, KeyNames=names)
    except is_boto3_error_code("InvalidKeyPair.NotFound"):
        return []
    except IndexError:
        return []

    return key["KeyPairs"]


def main():
    argument_spec = dict(
        name=dict(required=True, type="list", elements="str"),
    )

    module = AnsibleAWSModule(argument_spec=argument_spec, supports_check_mode=True)

    ec2_client = module.client("ec2", retry_decorator=AWSRetry.jittered_backoff())
    name = module.params["name"]

    try:
        result = find_key_pair(ec2_client, name)
        module.exit_json(keypairs=result)

    except Exception as err:
        module.fail_json(err)


if __name__ == "__main__":
    main()
