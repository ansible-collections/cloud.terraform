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

from plugins.module_utils.errors import TerraformWarning


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


class TestCreateInventory:
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
