# -*- coding: utf-8 -*-

# Copyright: Ansible Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)


import random
from typing import List
from unittest.mock import ANY, MagicMock, call

import pytest
from ansible.inventory.data import InventoryData
from ansible.module_utils._text import to_text
from ansible.template import Templar
from ansible_collections.cloud.terraform.plugins.inventory.terraform_state import (
    InventoryModule,
    ProvidersMapping,
    TerraformProviderInstance,
    create_providers_list,
    filter_instances,
    get_preferred_hostname,
    get_tag_hostname,
    write_terraform_config,
)
from ansible_collections.cloud.terraform.plugins.module_utils.models import (
    TerraformChildModule,
    TerraformModuleResource,
    TerraformRootModule,
    TerraformShow,
    TerraformShowValues,
)

from plugins.module_utils.errors import TerraformError


@pytest.fixture
def inventory_plugin():
    plugin = InventoryModule()
    plugin.inventory = InventoryData()
    plugin.templar = Templar(loader=None)
    return plugin


@pytest.fixture
def terraform_module_resource():
    return TerraformModuleResource(
        address="aws_instance.test",
        mode="managed",
        type="aws_instance",
        name="test",
        provider_name="registry.terraform.io/hashicorp/aws",
        schema_version="0",
        sensitive_values={},
        depends_on=[],
        values={
            "ami": "ami-01d00f1bdb42735ac",
            "arn": "arn:aws:ec2:us-east-1:012345678901:instance/i-01abcdef012345678",
            "associate_public_ip_address": False,
            "availability_zone": "us-east-1a",
            "cpu_core_count": 1,
            "disable_api_stop": False,
            "id": "i-08adbeb438548f001",
            "instance_state": "running",
            "instance_type": "t2.micro",
            "private_dns": "ip-168-10-1-147.us-east-1.compute.internal",
            "private_ip": "168.10.1.147",
            "public_dns": "",
            "public_ip": "",
            "subnet_id": "subnet-059a78661bffed8ca",
            "tags": {
                "Name": "ansible_host",
                "Phase": "dev",
            },
            "tags_all": {
                "Name": "ansible_host",
                "Phase": "dev",
            },
        },
    )


@pytest.fixture
def terraform_backend_config():
    return (
        "backend 'http' {"
        "address = 'https://localhost:8043/api/v2/state/3/'"
        "skip_cert_verification = true"
        "username = 'ansible'"
        "password = 'test123!'"
        "}"
    )


class TestFilterInstances:
    def generate_module_resources(self, types: List[str]) -> List[TerraformModuleResource]:
        return [
            TerraformModuleResource(
                address=f"{type}.test_{i}",
                mode="managed",
                type=type,
                name=f"test{i}",
                provider_name=self.compute_provider_name(type),
                schema_version="0",
                sensitive_values={},
                depends_on=[],
                values={},
            )
            for i, type in enumerate(types)
        ]

    def compute_provider_name(self, instance_type: str) -> str:
        return f"registry.terraform.io/hashicorp/{instance_type.split('_')[0]}"

    @pytest.mark.parametrize(
        "number_instance",
        range(5),
    )
    def test_filter_instances(self, number_instance):
        _types = ["aws_instance", "azurerm_virtual_machine", "google_compute_instance"]
        resources = self.generate_module_resources(random.choices(_types, k=number_instance))
        TerraformProviderInstance
        for t in _types:
            assert all(
                item.type == t
                for item in filter_instances(
                    resources, [TerraformProviderInstance(provider_name=self.compute_provider_name(t), types=[t])]
                )
            )


class TestGetTagHostName:
    @pytest.mark.parametrize(
        "preference,result",
        [
            ("tag:Name", "ansible_host"),
            ("tag:Name=ansible_host", "Name_ansible_host"),
            ("tag:Name=ansible", None),
            ("tag:Name=runner,Phase", "dev"),
            ("tag:Name,Phase=dev", "Phase_dev"),
        ],
    )
    def test_get_tag_hostname(self, terraform_module_resource, preference, result):
        assert get_tag_hostname(terraform_module_resource, preference) == result


class TestGetPreferredHostName:
    def test_hostnames_not_provided(self, terraform_module_resource):
        expected = terraform_module_resource.type + "_" + terraform_module_resource.name
        assert get_preferred_hostname(terraform_module_resource) == expected

    @pytest.mark.parametrize(
        "tag_hostnames,get_tag_hostname",
        [
            ("tag:Name", "ansible_host"),
            ("tag:Name=ansible_host", "Name_ansible_host"),
            ("tag:Name=ansible", None),
            ("tag:Name=runner,Phase", "dev"),
            ("tag:Name,Phase=dev", "Phase_dev"),
        ],
    )
    def test_with_tag_prefix(self, terraform_module_resource, mocker, tag_hostnames, get_tag_hostname):
        get_tag_hostname_patch = mocker.patch(
            "ansible_collections.cloud.terraform.plugins.inventory.terraform_state.get_tag_hostname"
        )
        get_tag_hostname_patch.return_value = get_tag_hostname
        assert get_preferred_hostname(terraform_module_resource, [tag_hostnames]) == get_tag_hostname

    def test_with_literal_value(self, terraform_module_resource, mocker):
        get_tag_hostname_patch = mocker.patch(
            "ansible_collections.cloud.terraform.plugins.inventory.terraform_state.get_tag_hostname"
        )
        hostname = "some_literal_value_not_part_of_terraform_module_resource_value"
        assert get_preferred_hostname(terraform_module_resource, [hostname]) == hostname
        get_tag_hostname_patch.assert_not_called()

    def test_with_prefix_containig_tag(self, terraform_module_resource, mocker):
        get_tag_hostname_patch = mocker.patch(
            "ansible_collections.cloud.terraform.plugins.inventory.terraform_state.get_tag_hostname"
        )
        get_tag_hostname_patch.return_value = "ansible_host"
        hostname = {"name": "tag:Name"}
        assert get_preferred_hostname(terraform_module_resource, [hostname]) == "ansible_host"

    def test_with_prefix_and_separator(self, terraform_module_resource):
        hostname = {"name": "instance_type", "prefix": "instance_state", "separator": "."}
        assert get_preferred_hostname(terraform_module_resource, [hostname]) == terraform_module_resource.values.get(
            "instance_state"
        ) + "." + terraform_module_resource.values.get("instance_type")

    def test_with_prefix_missing_name_key(self, terraform_module_resource):
        hostname = {"key": "private_ip"}
        with pytest.raises(Exception):
            try:
                get_preferred_hostname(terraform_module_resource, [hostname])
            except TerraformError as e:
                assert "A 'name' key must be defined in a hostnames dictionary." in str(e.value)
                raise


class TestInventoryModuleVerifyFile:
    @pytest.mark.parametrize(
        "name,valid",
        [("terraform_state.yaml", True), ("terraform_state.yml", True), ("invalid.yaml", False)],
    )
    def test_file_name(self, inventory_plugin, tmp_path, name, valid):
        config = tmp_path / name
        config.write_text("plugin: cloud.terraform.terraform_provider")
        # using to_text to avoid getting error "PosixPath object has no attribute endswith"
        assert inventory_plugin.verify_file(to_text(config)) is valid


class TestInventoryModuleSanitizeHostname:
    @pytest.mark.parametrize(
        "value",
        ["simple_hostname", "hostname:2"],
    )
    def test_sanitize_hostname(self, inventory_plugin, mocker, value):
        if ":" not in value:
            assert inventory_plugin._sanitize_hostname(value) == value
        else:
            expected = value.split(":", 1)[0]
            mocker.patch(
                "ansible_collections.cloud.terraform.plugins.inventory.terraform_state.InventoryModule._sanitize_group_name"
            ).return_value = expected
            assert inventory_plugin._sanitize_hostname(value) == expected


class TestInventoryModuleCreateInventory:
    class ansibleInventory:
        def __init__(self):
            self.inventory = {}

        def add_host(self, name):
            self.inventory[name] = {}

        def set_variable(self, name, k, v):
            if name not in self.inventory:
                raise TerraformError(f"name '{name}' is missing from inventory dictionnary")
            self.inventory[name][k] = v

        def assert_value(self, name, value):
            assert name in self.inventory
            assert value == self.inventory[name]

    def create_instance(self, name, values):
        return TerraformModuleResource(
            address=f"aws_instance.{name}",
            mode="managed",
            type="aws_instance",
            name=name,
            provider_name="registry.terraform.io/hashicorp/aws",
            schema_version="0",
            sensitive_values={},
            depends_on=[],
            values=values,
        )

    def test_create_inventory(self, inventory_plugin, mocker):
        hostnames = MagicMock()
        keyed_groups = MagicMock()
        strict = MagicMock()
        compose = MagicMock()

        config = {f"id{id}": {"hostvar": f"fromInstanceId{id}"} for id in range(5)}
        instances = [self.create_instance(name=n, values=v) for n, v in config.items()]
        get_preferred_hostname_patch = mocker.patch(
            "ansible_collections.cloud.terraform.plugins.inventory.terraform_state.get_preferred_hostname"
        )
        get_preferred_hostname_patch.side_effect = lambda i, _: i.name

        inventory_plugin._set_composite_vars = MagicMock()
        inventory_plugin._add_host_to_keyed_groups = MagicMock()
        inventory_plugin.inventory = self.ansibleInventory()

        inventory_plugin.create_inventory(instances, hostnames, compose, keyed_groups, strict)

        for name, value in config.items():
            inventory_plugin.inventory.assert_value(name, value)

        get_preferred_hostname_patch.assert_has_calls(
            [call(i, hostnames) for i in instances],
            any_order=True,
        )
        inventory_plugin._set_composite_vars.assert_has_calls(
            [call(compose, vars, name, strict=strict) for name, vars in config.items()],
            any_order=True,
        )
        inventory_plugin._add_host_to_keyed_groups.assert_has_calls(
            [call(keyed_groups, vars, name, strict=strict) for name, vars in config.items()],
            any_order=True,
        )


class TestWriteTerraformConfig:
    def test_write_terraform_config(self, terraform_backend_config, tmp_path):
        main_tf = tmp_path / "main.tf"
        write_terraform_config(terraform_backend_config, str(main_tf))

        assert main_tf.read_text() == "terraform {\n" + terraform_backend_config + "\n}"


class TestCreateProvidersList:
    @pytest.mark.parametrize(
        "include_filters,exclude_filters,expected",
        [
            ([], [], "all"),
            (["aws"], [], ["aws"]),
            (["aws"], ["aws"], []),
            ([], ["aws"], ["azurerm", "google"]),
        ],
    )
    def test_create_providers_list(self, include_filters, exclude_filters, expected):
        if expected == "all":
            result = [v for k, v in ProvidersMapping.items()]
        else:
            result = [v for name, v in ProvidersMapping.items() if name in expected]
        computed = create_providers_list(include_filters, exclude_filters)
        print("Computed: %s" % computed)
        print("Expected: %s" % result)
        assert result == computed


class TestInventoryModuleQuery:
    @pytest.mark.parametrize(
        "search_child_modules",
        [True, False],
    )
    def test__query(self, inventory_plugin, terraform_backend_config, mocker, search_child_modules):
        write_terraform_config_patch = mocker.patch(
            "ansible_collections.cloud.terraform.plugins.inventory.terraform_state.write_terraform_config"
        )
        write_terraform_config_patch.return_value = True
        instances = MagicMock()
        filter_instances_patch = mocker.patch(
            "ansible_collections.cloud.terraform.plugins.inventory.terraform_state.filter_instances"
        )
        filter_instances_patch.return_value = instances

        terraform_commands = MagicMock()
        terraform_commands.show.return_value = TerraformShow(
            format_version="4",
            terraform_version="1.6.3",
            values=TerraformShowValues(
                outputs={},
                root_module=TerraformRootModule(
                    resources=MagicMock(),
                    child_modules=[TerraformChildModule(resources=MagicMock())],
                ),
            ),
        )
        terraform_command_patch = mocker.patch(
            "ansible_collections.cloud.terraform.plugins.inventory.terraform_state.TerraformCommands"
        )
        terraform_command_patch.return_value = terraform_commands

        terraform_binary = MagicMock()
        result = inventory_plugin._query(
            terraform_binary,
            terraform_backend_config,
            search_child_modules,
            [
                TerraformProviderInstance(
                    provider_name=MagicMock(),
                    types=MagicMock(),
                )
            ],
        )
        assert instances == result
        write_terraform_config_patch.assert_called_once_with(terraform_backend_config, ANY)
        terraform_commands.init.assert_called_once()
        terraform_commands.show.assert_called_once()


class TestInventoryModuleParse:
    @pytest.mark.parametrize(
        "has_backend_config",
        [True, False],
    )
    @pytest.mark.parametrize(
        "has_binary_path",
        [True, False],
    )
    def test_parse(self, inventory_plugin, mocker, has_backend_config, has_binary_path):
        loader = MagicMock()
        path = MagicMock()
        inventory = MagicMock()
        cache = MagicMock()

        config = {
            "backend_config": MagicMock(),
            "binary_path": MagicMock(),
            "search_child_modules": MagicMock(),
        }

        if not has_backend_config:
            del config["backend_config"]

        if not has_binary_path:
            del config["binary_path"]

        read_config_data_patch = mocker.patch(
            "ansible_collections.cloud.terraform.plugins.inventory.terraform_state.InventoryModule.read_config_data"
        )
        read_config_data_patch.side_effect = lambda _: config
        validate_bin_patch = mocker.patch(
            "ansible_collections.cloud.terraform.plugins.inventory.terraform_state.validate_bin_path"
        )
        validate_bin_patch.return_value = True

        super_parse_patch = mocker.patch(
            "ansible_collections.cloud.terraform.plugins.inventory.terraform_state.TerraformInventoryPluginBase.parse"
        )
        super_parse_patch.return_value = True

        process_patch = mocker.patch("ansible_collections.cloud.terraform.plugins.inventory.terraform_state.process")
        process_patch.get_bin_path = MagicMock()
        terraform_bin_mock = MagicMock()
        process_patch.get_bin_path.return_value = terraform_bin_mock

        create_providers_list_patch = mocker.patch(
            "ansible_collections.cloud.terraform.plugins.inventory.terraform_state.create_providers_list"
        )
        providers = MagicMock()
        create_providers_list_patch.return_value = providers

        if not has_backend_config:
            with pytest.raises(Exception):
                try:
                    inventory_plugin.parse(inventory, loader, path, cache=cache)
                except TerraformError as e:
                    assert "'backend_config' option is required to read existing state file." in str(e.value)
                    raise
        else:
            instances = MagicMock()
            inventory_plugin._query = MagicMock()
            inventory_plugin._query.return_value = instances
            inventory_plugin.create_inventory = MagicMock()
            inventory_plugin.parse(inventory, loader, path, cache=cache)

            inventory_plugin._query.assert_called_once_with(
                config.get("binary_path") or terraform_bin_mock,
                config.get("backend_config"),
                config.get("search_child_modules"),
                providers,
            )
            inventory_plugin.create_inventory.assert_called_once_with(
                instances,
                config.get("hostnames"),
                config.get("compose"),
                config.get("keyed_groups"),
                config.get("strict"),
            )

            if has_binary_path:
                validate_bin_patch.assert_called_once_with(config.get("binary_path"))
                process_patch.get_bin_path.assert_not_called()
            else:
                process_patch.get_bin_path.assert_called_once_with("terraform")
                validate_bin_patch.assert_not_called()

        super_parse_patch.assert_called_once_with(inventory, loader, path, cache=cache)
        read_config_data_patch.assert_called_once_with(path)
