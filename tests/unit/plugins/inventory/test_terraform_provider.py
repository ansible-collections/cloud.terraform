# -*- coding: utf-8 -*-
# Copyright: (c) 2022, XLAB Steampunk <steampunk@xlab.si>
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

import pytest
from ansible.inventory.data import InventoryData
from ansible.template import Templar
from ansible_collections.cloud.terraform.plugins.inventory.terraform_provider import InventoryModule
from ansible_collections.cloud.terraform.plugins.module_utils.models import (
    TerraformAnsibleProvider,
    TerraformChildModule,
    TerraformChildModuleResource,
    TerraformRootModule,
    TerraformRootModuleResource,
    TerraformShow,
    TerraformShowValues,
)

# Fix this import - it should be from ansible_collections, not plugins
from ansible_collections.cloud.terraform.plugins.module_utils.errors import TerraformError, TerraformWarning


@pytest.fixture
def inventory_plugin():
    plugin = InventoryModule()
    plugin.inventory = InventoryData()
    plugin.templar = Templar(loader=None)
    return plugin


@pytest.fixture
def resource():
    return TerraformRootModuleResource(
        address=None,
        mode=None,
        type=None,
        name=None,
        provider_name=None,
        schema_version=None,
        values={},
        sensitive_values={},
        depends_on=[],
    )


# class TestInventoryModuleVerifyFile:
#     @pytest.mark.parametrize(
#         "name,valid",
#         [("terraform_provider.yaml", True), ("terraform_provider.yml", True), ("invalid.yaml", False)],
#     )
#     def test_file_name(self, inventory_plugin, tmp_path, name, valid):
#         config = tmp_path / name
#         config.write_text("plugin: cloud.terraform.terraform_provider")
#         # using to_text to avoid getting error "PosixPath object has no attribute endswith"
#         assert inventory_plugin.verify_file(to_text(config)) is valid


class TestInventoryModuleAddHost:
    def test_add_host_groups_vars(self, inventory_plugin, mocker, resource):
        mocker.patch(
            "ansible_collections.cloud.terraform.plugins.inventory.terraform_provider.TerraformAnsibleProvider.from_json"
        ).return_value = TerraformAnsibleProvider(
            name="host_name",
            groups=["group1", "group2"],
            children=[],
            variables={"host_var1": "1", "host_var2": "2"},
        )
        inventory_plugin._add_host(inventory_plugin.inventory, resource)

        my_host = inventory_plugin.inventory.get_host("host_name")

        assert my_host.vars["host_var1"] == "1"
        assert my_host.vars["host_var2"] == "2"
        assert my_host.groups[0].name == "group1"
        assert my_host.groups[1].name == "group2"

    def test_add_host_groups(self, inventory_plugin, mocker, resource):
        mocker.patch(
            "ansible_collections.cloud.terraform.plugins.inventory.terraform_provider.TerraformAnsibleProvider.from_json"
        ).return_value = TerraformAnsibleProvider(
            name="host_name",
            groups=["group1", "group2"],
            children=[],
            variables={},
        )
        inventory_plugin._add_host(inventory_plugin.inventory, resource)

        my_host = inventory_plugin.inventory.get_host("host_name")

        assert my_host.groups[0].name == "group1"
        assert my_host.groups[1].name == "group2"

    def test_add_host_vars(self, inventory_plugin, mocker, resource):
        mocker.patch(
            "ansible_collections.cloud.terraform.plugins.inventory.terraform_provider.TerraformAnsibleProvider.from_json"
        ).return_value = TerraformAnsibleProvider(
            name="host_name",
            groups=[],
            children=[],
            variables={"host_var1": "1", "host_var2": "2"},
        )
        inventory_plugin._add_host(inventory_plugin.inventory, resource)

        my_host = inventory_plugin.inventory.get_host("host_name")

        assert my_host.vars["host_var1"] == "1"
        assert my_host.vars["host_var2"] == "2"


class TestInventoryModuleAddGroup:
    def test_add_group_children_vars(self, inventory_plugin, mocker, resource):
        mocker.patch(
            "ansible_collections.cloud.terraform.plugins.inventory.terraform_provider.TerraformAnsibleProvider.from_json"
        ).return_value = TerraformAnsibleProvider(
            groups=[],
            name="group_name",
            children=["child1", "child2"],
            variables={"group_var1": "1", "group_var2": "2"},
        )
        inventory_plugin._add_group(inventory_plugin.inventory, resource)

        groups = inventory_plugin.inventory.groups

        assert groups["group_name"].child_groups[0].name == "child1"
        assert groups["group_name"].child_groups[1].name == "child2"
        assert groups["group_name"].vars["group_var1"] == "1"
        assert groups["group_name"].vars["group_var2"] == "2"

    def test_add_group_children(self, inventory_plugin, mocker, resource):
        mocker.patch(
            "ansible_collections.cloud.terraform.plugins.inventory.terraform_provider.TerraformAnsibleProvider.from_json"
        ).return_value = TerraformAnsibleProvider(
            groups=[],
            name="group_name",
            children=["child1", "child2"],
            variables={},
        )
        inventory_plugin._add_group(inventory_plugin.inventory, resource)

        groups = inventory_plugin.inventory.groups

        assert groups["group_name"].child_groups[0].name == "child1"
        assert groups["group_name"].child_groups[1].name == "child2"

    def test_add_group_vars(self, inventory_plugin, mocker, resource):
        mocker.patch(
            "ansible_collections.cloud.terraform.plugins.inventory.terraform_provider.TerraformAnsibleProvider.from_json"
        ).return_value = TerraformAnsibleProvider(
            groups=[],
            name="group_name",
            children=[],
            variables={"group_var1": "1", "group_var2": "2"},
        )
        inventory_plugin._add_group(inventory_plugin.inventory, resource)

        groups = inventory_plugin.inventory.groups

        assert groups["group_name"].vars["group_var1"] == "1"
        assert groups["group_name"].vars["group_var2"] == "2"


class TestExtractModuleName:
    def test_extract_module_name_root_resource(self, inventory_plugin):
        """Test extraction for root module resource"""
        resource = TerraformRootModuleResource(
            address="ansible_host.example",
            type="ansible_host",
            mode=None,
            name=None,
            provider_name=None,
            schema_version=None,
            values={},
            sensitive_values={},
            depends_on=[],
        )
        assert inventory_plugin._extract_module_name(resource) is None

    def test_extract_module_name_simple_module(self, inventory_plugin):
        """Test extraction for simple module resource"""
        resource = TerraformChildModuleResource(
            address="module.web_servers.ansible_host.example",
            type="ansible_host",
            mode=None,
            name=None,
            provider_name=None,
            schema_version=None,
            values={},
            sensitive_values={},
            depends_on=[],
        )
        assert inventory_plugin._extract_module_name(resource) == "web_servers"

    def test_extract_module_name_nested_module(self, inventory_plugin):
        """Test extraction for nested module resource"""
        resource = TerraformChildModuleResource(
            address="module.production.frontend.ansible_host.web1",
            type="ansible_host",
            mode=None,
            name=None,
            provider_name=None,
            schema_version=None,
            values={},
            sensitive_values={},
            depends_on=[],
        )
        assert inventory_plugin._extract_module_name(resource) == "production.frontend"

    def test_extract_module_name_data_resource(self, inventory_plugin):
        """Test extraction for data resource in module"""
        resource = TerraformChildModuleResource(
            address="data.module.database.ansible_host.db1",
            type="ansible_host",
            mode=None,
            name=None,
            provider_name=None,
            schema_version=None,
            values={},
            sensitive_values={},
            depends_on=[],
        )
        assert inventory_plugin._extract_module_name(resource) == "database"

    def test_extract_module_name_complex_nested(self, inventory_plugin):
        """Test extraction for complex nested module"""
        resource = TerraformChildModuleResource(
            address="module.environment.production.services.web.ansible_host.server1",
            type="ansible_host",
            mode=None,
            name=None,
            provider_name=None,
            schema_version=None,
            values={},
            sensitive_values={},
            depends_on=[],
        )
        assert inventory_plugin._extract_module_name(resource) == "environment.production.services.web"

    def test_extract_module_name_invalid_address(self, inventory_plugin):
        """Test extraction with invalid or empty address"""
        resource = TerraformRootModuleResource(
            address="",
            type="ansible_host",
            mode=None,
            name=None,
            provider_name=None,
            schema_version=None,
            values={},
            sensitive_values={},
            depends_on=[],
        )
        assert inventory_plugin._extract_module_name(resource) is None

    def test_extract_module_name_missing_resource_type(self, inventory_plugin):
        """Test extraction when resource type is not found in address"""
        resource = TerraformChildModuleResource(
            address="module.web_servers.something.else",
            type="ansible_host",
            mode=None,
            name=None,
            provider_name=None,
            schema_version=None,
            values={},
            sensitive_values={},
            depends_on=[],
        )
        assert inventory_plugin._extract_module_name(resource) is None


class TestShouldIncludeResource:
    def test_should_include_root_resource_no_filters(self, inventory_plugin):
        """Root resource should be included when no filters are specified"""
        resource = TerraformRootModuleResource(
            address="ansible_host.example",
            type="ansible_host",
            mode=None,
            name=None,
            provider_name=None,
            schema_version=None,
            values={},
            sensitive_values={},
            depends_on=[],
        )
        assert inventory_plugin._should_include_resource(resource, None, None) is True

    def test_should_include_root_resource_with_include_modules(self, inventory_plugin):
        """Root resource should be excluded when include_modules is specified"""
        resource = TerraformRootModuleResource(
            address="ansible_host.example",
            type="ansible_host",
            mode=None,
            name=None,
            provider_name=None,
            schema_version=None,
            values={},
            sensitive_values={},
            depends_on=[],
        )
        assert inventory_plugin._should_include_resource(resource, ["web_servers"], None) is False

    def test_should_include_module_resource_in_include_list(self, inventory_plugin):
        """Module resource should be included when in include_modules list"""
        resource = TerraformChildModuleResource(
            address="module.web_servers.ansible_host.example",
            type="ansible_host",
            mode=None,
            name=None,
            provider_name=None,
            schema_version=None,
            values={},
            sensitive_values={},
            depends_on=[],
        )
        assert inventory_plugin._should_include_resource(resource, ["web_servers", "database"], None) is True

    def test_should_exclude_module_resource_not_in_include_list(self, inventory_plugin):
        """Module resource should be excluded when not in include_modules list"""
        resource = TerraformChildModuleResource(
            address="module.api_servers.ansible_host.example",
            type="ansible_host",
            mode=None,
            name=None,
            provider_name=None,
            schema_version=None,
            values={},
            sensitive_values={},
            depends_on=[],
        )
        assert inventory_plugin._should_include_resource(resource, ["web_servers", "database"], None) is False

    def test_should_exclude_module_resource_in_exclude_list(self, inventory_plugin):
        """Module resource should be excluded when in exclude_modules list"""
        resource = TerraformChildModuleResource(
            address="module.development.ansible_host.example",
            type="ansible_host",
            mode=None,
            name=None,
            provider_name=None,
            schema_version=None,
            values={},
            sensitive_values={},
            depends_on=[],
        )
        assert inventory_plugin._should_include_resource(resource, None, ["development", "testing"]) is False

    def test_should_include_module_resource_not_in_exclude_list(self, inventory_plugin):
        """Module resource should be included when not in exclude_modules list"""
        resource = TerraformChildModuleResource(
            address="module.production.ansible_host.example",
            type="ansible_host",
            mode=None,
            name=None,
            provider_name=None,
            schema_version=None,
            values={},
            sensitive_values={},
            depends_on=[],
        )
        assert inventory_plugin._should_include_resource(resource, None, ["development", "testing"]) is True

    def test_exclude_takes_precedence_over_include(self, inventory_plugin):
        """exclude_modules should take precedence over include_modules"""
        resource = TerraformChildModuleResource(
            address="module.web_servers.ansible_host.example",
            type="ansible_host",
            mode=None,
            name=None,
            provider_name=None,
            schema_version=None,
            values={},
            sensitive_values={},
            depends_on=[],
        )
        # Even though web_servers is in include list, it's also in exclude list
        assert inventory_plugin._should_include_resource(resource, ["web_servers"], ["web_servers"]) is False

    def test_nested_module_filtering(self, inventory_plugin):
        """Test filtering with nested module names"""
        resource = TerraformChildModuleResource(
            address="module.production.frontend.ansible_host.web1",
            type="ansible_host",
            mode=None,
            name=None,
            provider_name=None,
            schema_version=None,
            values={},
            sensitive_values={},
            depends_on=[],
        )
        assert inventory_plugin._should_include_resource(resource, ["production.frontend"], None) is True
        assert inventory_plugin._should_include_resource(resource, ["production.backend"], None) is False


class TestCreateInventory:
    def test_create_inventory_with_include_modules(self, inventory_plugin):
        """Test inventory creation with include_modules filtering"""
        state_content = [
            TerraformShow(
                format_version="1.0",
                terraform_version="1.3.6",
                values=TerraformShowValues(
                    outputs={},
                    root_module=TerraformRootModule(
                        resources=[
                            TerraformRootModuleResource(
                                address="ansible_host.roothost",
                                mode="managed",
                                type="ansible_host",
                                name="roothost",
                                provider_name="terraform-ansible.com/ansibleprovider/ansible",
                                schema_version=0,
                                values={
                                    "groups": ["somegroup"],
                                    "name": "roothost",
                                    "id": "roothost",
                                    "variables": {"host_hello": "from root!"},
                                },
                                sensitive_values={"groups": [False], "variables": {}},
                                depends_on=[],
                            ),
                        ],
                        child_modules=[
                            TerraformChildModule(
                                resources=[
                                    TerraformChildModuleResource(
                                        address="module.web_servers.ansible_host.webhost",
                                        mode="managed",
                                        type="ansible_host",
                                        name="webhost",
                                        provider_name="terraform-ansible.com/ansibleprovider/ansible",
                                        schema_version=0,
                                        values={
                                            "groups": None,
                                            "name": "webhost",
                                            "id": "webhost",
                                            "variables": {"host_hello": "from web!"},
                                        },
                                        sensitive_values={},
                                        depends_on=[],
                                    ),
                                    TerraformChildModuleResource(
                                        address="module.database.ansible_host.dbhost",
                                        mode="managed",
                                        type="ansible_host",
                                        name="dbhost",
                                        provider_name="terraform-ansible.com/ansibleprovider/ansible",
                                        schema_version=0,
                                        values={
                                            "groups": None,
                                            "name": "dbhost",
                                            "id": "dbhost",
                                            "variables": {"host_hello": "from db!"},
                                        },
                                        sensitive_values={},
                                        depends_on=[],
                                    ),
                                ],
                            ),
                        ],
                    ),
                ),
            )
        ]

        inventory_plugin.inventory = InventoryData()
        # Only include web_servers module
        inventory_plugin.create_inventory(
            inventory_plugin.inventory, state_content, True, include_modules=["web_servers"]
        )

        hosts = inventory_plugin.inventory.hosts
        # Should only have webhost, not roothost or dbhost
        assert len(hosts) == 1
        assert "webhost" in hosts
        assert "roothost" not in hosts
        assert "dbhost" not in hosts

    def test_create_inventory_with_exclude_modules(self, inventory_plugin):
        """Test inventory creation with exclude_modules filtering"""
        state_content = [
            TerraformShow(
                format_version="1.0",
                terraform_version="1.3.6",
                values=TerraformShowValues(
                    outputs={},
                    root_module=TerraformRootModule(
                        resources=[
                            TerraformRootModuleResource(
                                address="ansible_host.roothost",
                                mode="managed",
                                type="ansible_host",
                                name="roothost",
                                provider_name="terraform-ansible.com/ansibleprovider/ansible",
                                schema_version=0,
                                values={
                                    "groups": ["somegroup"],
                                    "name": "roothost",
                                    "id": "roothost",
                                    "variables": {"host_hello": "from root!"},
                                },
                                sensitive_values={"groups": [False], "variables": {}},
                                depends_on=[],
                            ),
                        ],
                        child_modules=[
                            TerraformChildModule(
                                resources=[
                                    TerraformChildModuleResource(
                                        address="module.web_servers.ansible_host.webhost",
                                        mode="managed",
                                        type="ansible_host",
                                        name="webhost",
                                        provider_name="terraform-ansible.com/ansibleprovider/ansible",
                                        schema_version=0,
                                        values={
                                            "groups": None,
                                            "name": "webhost",
                                            "id": "webhost",
                                            "variables": {"host_hello": "from web!"},
                                        },
                                        sensitive_values={},
                                        depends_on=[],
                                    ),
                                    TerraformChildModuleResource(
                                        address="module.database.ansible_host.dbhost",
                                        mode="managed",
                                        type="ansible_host",
                                        name="dbhost",
                                        provider_name="terraform-ansible.com/ansibleprovider/ansible",
                                        schema_version=0,
                                        values={
                                            "groups": None,
                                            "name": "dbhost",
                                            "id": "dbhost",
                                            "variables": {"host_hello": "from db!"},
                                        },
                                        sensitive_values={},
                                        depends_on=[],
                                    ),
                                ],
                            ),
                        ],
                    ),
                ),
            )
        ]

        inventory_plugin.inventory = InventoryData()
        # Exclude database module
        inventory_plugin.create_inventory(inventory_plugin.inventory, state_content, True, exclude_modules=["database"])

        hosts = inventory_plugin.inventory.hosts
        # Should have roothost and webhost, but not dbhost
        assert len(hosts) == 2
        assert "roothost" in hosts
        assert "webhost" in hosts
        assert "dbhost" not in hosts

    def test_create_inventory_search_child_modules_false(self, inventory_plugin):
        """Test that module filtering is ignored when search_child_modules is False"""
        state_content = [
            TerraformShow(
                format_version="1.0",
                terraform_version="1.3.6",
                values=TerraformShowValues(
                    outputs={},
                    root_module=TerraformRootModule(
                        resources=[
                            TerraformRootModuleResource(
                                address="ansible_host.roothost",
                                mode="managed",
                                type="ansible_host",
                                name="roothost",
                                provider_name="terraform-ansible.com/ansibleprovider/ansible",
                                schema_version=0,
                                values={
                                    "groups": ["somegroup"],
                                    "name": "roothost",
                                    "id": "roothost",
                                    "variables": {"host_hello": "from root!"},
                                },
                                sensitive_values={"groups": [False], "variables": {}},
                                depends_on=[],
                            ),
                        ],
                        child_modules=[
                            TerraformChildModule(
                                resources=[
                                    TerraformChildModuleResource(
                                        address="module.web_servers.ansible_host.webhost",
                                        mode="managed",
                                        type="ansible_host",
                                        name="webhost",
                                        provider_name="terraform-ansible.com/ansibleprovider/ansible",
                                        schema_version=0,
                                        values={
                                            "groups": None,
                                            "name": "webhost",
                                            "id": "webhost",
                                            "variables": {"host_hello": "from web!"},
                                        },
                                        sensitive_values={},
                                        depends_on=[],
                                    ),
                                ],
                            ),
                        ],
                    ),
                ),
            )
        ]

        inventory_plugin.inventory = InventoryData()
        # search_child_modules=False should ignore module filtering
        inventory_plugin.create_inventory(
            inventory_plugin.inventory,
            state_content,
            False,  # search_child_modules=False
            include_modules=["web_servers"],
        )

        hosts = inventory_plugin.inventory.hosts
        # Should only have roothost (child modules ignored regardless of filtering)
        assert len(hosts) == 1
        assert "roothost" in hosts
        assert "webhost" not in hosts


class TestParseMethod:
    def test_parse_mutually_exclusive_options(self, inventory_plugin, mocker):
        """Test that mutually exclusive include_modules and exclude_modules raise an error"""

        # Mock the _read_config_data to return the config with both options
        mocker.patch.object(inventory_plugin, "_read_config_data").return_value = {
            "project_path": "/test/path",
            "state_file": "",
            "search_child_modules": True,
            "binary_path": None,
            "include_modules": ["web_servers"],
            "exclude_modules": ["database"],
        }

        # Mock the super().parse() call to avoid calling the parent class
        mocker.patch("ansible_collections.cloud.terraform.plugins.plugin_utils.base.TerraformInventoryPluginBase.parse")

        # Test that the error is raised with the correct message
        with pytest.raises(TerraformError, match="mutually exclusive"):
            inventory_plugin.parse(None, None, "/fake/path")

    def test_parse_with_valid_config(self, inventory_plugin, mocker):
        """Test parse method with valid configuration"""

        # Mock dependencies
        mocker.patch.object(inventory_plugin, "_read_config_data").return_value = {
            "project_path": "/test/path",
            "state_file": "",
            "search_child_modules": True,
            "binary_path": None,
            "include_modules": ["web_servers"],
            "exclude_modules": None,
        }

        # Mock the super().parse() call
        mocker.patch("ansible_collections.cloud.terraform.plugins.plugin_utils.base.TerraformInventoryPluginBase.parse")

        mock_terraform_commands = mocker.patch(
            "ansible_collections.cloud.terraform.plugins.inventory.terraform_provider.TerraformCommands"
        )
        mock_terraform_instance = mocker.Mock()
        mock_terraform_commands.return_value = mock_terraform_instance
        mock_terraform_instance.show.return_value = None

        mocker.patch(
            "ansible_collections.cloud.terraform.plugins.inventory.terraform_provider.process.get_bin_path"
        ).return_value = "/usr/bin/terraform"

        mocker.patch.object(inventory_plugin, "create_inventory")

        # Should not raise an exception
        inventory_plugin.parse(None, None, "/fake/path")

        # Verify create_inventory was called with the right parameters
        inventory_plugin.create_inventory.assert_called_once()
        call_args = inventory_plugin.create_inventory.call_args
        assert call_args[0][2] is True  # search_child_modules
        assert call_args[0][3] == ["web_servers"]  # include_modules
        assert call_args[0][4] is None  # exclude_modules

    def test_parse_include_modules_only(self, inventory_plugin, mocker):
        """Test parse method with only include_modules (should work)"""

        mocker.patch.object(inventory_plugin, "_read_config_data").return_value = {
            "project_path": "/test/path",
            "state_file": "",
            "search_child_modules": True,
            "binary_path": None,
            "include_modules": ["web_servers"],
            "exclude_modules": None,
        }

        mocker.patch("ansible_collections.cloud.terraform.plugins.plugin_utils.base.TerraformInventoryPluginBase.parse")

        mock_terraform_commands = mocker.patch(
            "ansible_collections.cloud.terraform.plugins.inventory.terraform_provider.TerraformCommands"
        )
        mock_terraform_instance = mocker.Mock()
        mock_terraform_commands.return_value = mock_terraform_instance
        mock_terraform_instance.show.return_value = None

        mocker.patch(
            "ansible_collections.cloud.terraform.plugins.inventory.terraform_provider.process.get_bin_path"
        ).return_value = "/usr/bin/terraform"

        mocker.patch.object(inventory_plugin, "create_inventory")

        # Should not raise an exception
        inventory_plugin.parse(None, None, "/fake/path")

    def test_parse_exclude_modules_only(self, inventory_plugin, mocker):
        """Test parse method with only exclude_modules (should work)"""

        mocker.patch.object(inventory_plugin, "_read_config_data").return_value = {
            "project_path": "/test/path",
            "state_file": "",
            "search_child_modules": True,
            "binary_path": None,
            "include_modules": None,
            "exclude_modules": ["database"],
        }

        mocker.patch("ansible_collections.cloud.terraform.plugins.plugin_utils.base.TerraformInventoryPluginBase.parse")

        mock_terraform_commands = mocker.patch(
            "ansible_collections.cloud.terraform.plugins.inventory.terraform_provider.TerraformCommands"
        )
        mock_terraform_instance = mocker.Mock()
        mock_terraform_commands.return_value = mock_terraform_instance
        mock_terraform_instance.show.return_value = None

        mocker.patch(
            "ansible_collections.cloud.terraform.plugins.inventory.terraform_provider.process.get_bin_path"
        ).return_value = "/usr/bin/terraform"

        mocker.patch.object(inventory_plugin, "create_inventory")

        # Should not raise an exception
        inventory_plugin.parse(None, None, "/fake/path")


# Keep the existing tests for backward compatibility
class TestCreateInventoryLegacy:
    def test_create_inventory(self, inventory_plugin):
        state_content = [
            TerraformShow(
                format_version="1.0",
                terraform_version="1.3.6",
                values=TerraformShowValues(
                    outputs={},
                    root_module=TerraformRootModule(
                        resources=[
                            TerraformRootModuleResource(
                                address="ansible_group.childlessgroup",
                                mode="managed",
                                type="ansible_group",
                                name="childlessgroup",
                                provider_name="terraform-ansible.com/ansibleprovider/ansible",
                                schema_version=0,
                                values={
                                    "children": None,
                                    "name": "childlessgroup",
                                    "id": "childlessgroup",
                                    "variables": None,
                                },
                                sensitive_values={},
                                depends_on=[],
                            ),
                            TerraformRootModuleResource(
                                address="ansible_group.group",
                                mode="managed",
                                type="ansible_group",
                                name="group",
                                provider_name="terraform-ansible.com/ansibleprovider/ansible",
                                schema_version=0,
                                values={
                                    "children": ["somechild", "anotherchild"],
                                    "name": "somegroup",
                                    "id": "somegroup",
                                    "variables": {"group_hello": "from somegroup!", "group_variable": "11"},
                                },
                                sensitive_values={"children": [False, False], "variables": {}},
                                depends_on=[],
                            ),
                            TerraformRootModuleResource(
                                address="ansible_host.anotherhost",
                                mode="managed",
                                type="ansible_host",
                                name="anotherhost",
                                provider_name="terraform-ansible.com/ansibleprovider/ansible",
                                schema_version=0,
                                values={
                                    "groups": ["somechild"],
                                    "name": "anotherhost",
                                    "id": "anotherhost",
                                    "variables": {"host_hello": "from anotherhost!", "host_variable": "5"},
                                },
                                sensitive_values={"groups": [False], "variables": {}},
                                depends_on=[],
                            ),
                            TerraformRootModuleResource(
                                address="ansible_host.host",
                                mode="managed",
                                type="ansible_host",
                                name="host",
                                provider_name="terraform-ansible.com/ansibleprovider/ansible",
                                schema_version=0,
                                values={
                                    "groups": ["somegroup", "anothergroup"],
                                    "name": "somehost",
                                    "id": "somehost",
                                    "variables": {"host_hello": "from somehost!", "host_variable": "7"},
                                },
                                sensitive_values={"groups": [False, False], "variables": {}},
                                depends_on=[],
                            ),
                            TerraformRootModuleResource(
                                address="ansible_host.ungroupedhost",
                                mode="managed",
                                type="ansible_host",
                                name="ungroupedhost",
                                provider_name="terraform-ansible.com/ansibleprovider/ansible",
                                schema_version=0,
                                values={
                                    "groups": None,
                                    "name": "ungroupedhost",
                                    "id": "ungroupedhost",
                                    "variables": None,
                                },
                                sensitive_values={},
                                depends_on=[],
                            ),
                        ],
                        child_modules=[
                            TerraformChildModule(
                                resources=[
                                    TerraformChildModuleResource(
                                        address="module.example.ansible_host[0].duplicatehost",
                                        mode="managed",
                                        type="ansible_host",
                                        name="childhost",
                                        provider_name="terraform-ansible.com/ansibleprovider/ansible",
                                        schema_version=0,
                                        values={
                                            "groups": None,
                                            "name": "childhost",
                                            "id": "childhost",
                                            "variables": None,
                                        },
                                        sensitive_values={},
                                        depends_on=[],
                                    ),
                                ],
                            ),
                        ],
                    ),
                ),
            )
        ]

        inventory_plugin.inventory = InventoryData()
        search_child_modules = True

        inventory_plugin.create_inventory(inventory_plugin.inventory, state_content, search_child_modules)

        groups = inventory_plugin.inventory.groups

        assert len(groups) == 7
        assert "all" in groups
        assert "ungrouped" in groups
        assert "childlessgroup" in groups
        assert "somegroup" in groups
        assert "anothergroup" in groups
        assert "somechild" in groups
        assert "anotherchild" in groups

        assert groups["somegroup"].child_groups[0].name == "somechild"
        assert groups["somegroup"].child_groups[1].name == "anotherchild"

        assert groups["somegroup"].vars["group_hello"] == "from somegroup!"
        assert groups["somegroup"].vars["group_variable"] == "11"

        hosts = inventory_plugin.inventory.hosts
        somehost = inventory_plugin.inventory.get_host("somehost")
        anotherhost = inventory_plugin.inventory.get_host("anotherhost")
        ungroupedhost = inventory_plugin.inventory.get_host("ungroupedhost")

        assert len(hosts) == 4
        assert "somehost" in hosts
        assert "anotherhost" in hosts
        assert "ungroupedhost" in hosts
        assert "childhost" in hosts

        assert somehost.vars["host_hello"] == "from somehost!"
        assert somehost.vars["host_variable"] == "7"
        assert anotherhost.vars["host_hello"] == "from anotherhost!"
        assert anotherhost.vars["host_variable"] == "5"

        assert somehost.groups[0].name == "somegroup"
        assert somehost.groups[1].name == "anothergroup"
        assert anotherhost.groups[0].name == "somegroup"
        assert anotherhost.groups[1].name == "somechild"
        assert len(ungroupedhost.groups) == 0

        inventory_plugin.inventory = InventoryData()
        search_child_modules = False

        inventory_plugin.create_inventory(inventory_plugin.inventory, state_content, search_child_modules)

        hosts = inventory_plugin.inventory.hosts

        assert len(hosts) == 3
        assert "childhost" not in hosts

        # Test conflicts with multiple hosts with the same name, possible when selecting
        # multiple Terraform projects into the inventory provider
        # This should raise a TerraformWarning exception
        state_content = [
            TerraformShow(
                format_version="1.0",
                terraform_version="1.3.6",
                values=TerraformShowValues(
                    outputs={},
                    root_module=TerraformRootModule(
                        resources=[],
                        child_modules=[
                            TerraformChildModule(
                                resources=[
                                    TerraformChildModuleResource(
                                        address="module.example.ansible_host[0].duplicatehost",
                                        mode="managed",
                                        type="ansible_host",
                                        name="duplicatehost",
                                        provider_name="terraform-ansible.com/ansibleprovider/ansible",
                                        schema_version=0,
                                        values={
                                            "groups": None,
                                            "name": "duplicatehost",
                                            "id": "duplicatehost",
                                            "variables": None,
                                        },
                                        sensitive_values={},
                                        depends_on=[],
                                    ),
                                ],
                            ),
                            TerraformChildModule(
                                resources=[
                                    TerraformChildModuleResource(
                                        address="module.other_example.ansible_host[0].duplicatehost",
                                        mode="managed",
                                        type="ansible_host",
                                        name="duplicatehost",
                                        provider_name="terraform-ansible.com/ansibleprovider/ansible",
                                        schema_version=0,
                                        values={
                                            "groups": None,
                                            "name": "duplicatehost",
                                            "id": "duplicatehost",
                                            "variables": None,
                                        },
                                        sensitive_values={},
                                        depends_on=[],
                                    ),
                                ],
                            ),
                        ],
                    ),
                ),
            )
        ]

        inventory_plugin.inventory = InventoryData()
        search_child_modules = True

        with pytest.raises(Exception):
            try:
                inventory_plugin.create_inventory(inventory_plugin.inventory, state_content, search_child_modules)
            except TerraformWarning as e:
                assert "already exists elsewhere" in str(e.value)
                raise
