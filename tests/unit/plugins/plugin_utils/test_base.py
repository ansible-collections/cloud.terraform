# -*- coding: utf-8 -*-
# Copyright: (c) 2022, XLAB Steampunk <steampunk@xlab.si>
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

import pytest
from ansible.errors import AnsibleParserError
from ansible.inventory.data import InventoryData
from ansible.template import Templar
from ansible_collections.cloud.terraform.plugins.plugin_utils.base import TerraformInventoryPluginBase


@pytest.fixture
def inventory_plugin():
    plugin = TerraformInventoryPluginBase()
    plugin.inventory = InventoryData()
    plugin.templar = Templar(loader=None)
    return plugin


class TestInventoryModuleReadConfigData:
    def test_read_config_data(self, inventory_plugin, mocker, tmp_path):
        mocker.patch(
            "ansible_collections.cloud.terraform.plugins.plugin_utils.base.yaml.safe_load"
        ).return_value = dict(plugin="cloud.terraform.terraform_provider", state_file="mystate.tfstate")
        my_path = tmp_path / "terraform_provider.yaml"
        my_path.write_text("plugin: cloud.terraform.terraform_provider")

        cfg = inventory_plugin.read_config_data(my_path)

        assert cfg == dict(plugin="cloud.terraform.terraform_provider", state_file="mystate.tfstate")

    def test_read_config_data_parse_error(self, inventory_plugin, mocker, tmp_path):
        with pytest.raises(AnsibleParserError):
            inventory_plugin.read_config_data(tmp_path)
