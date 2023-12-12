# -*- coding: utf-8 -*-

# (c) 2023 Red Hat Inc.
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from typing import Any

import yaml
from ansible.errors import AnsibleParserError
from ansible.plugins.inventory import BaseInventoryPlugin
from ansible.utils.display import Display

display = Display()


class TerraformInventoryPluginBase(BaseInventoryPlugin):  # type: ignore  # mypy ignore
    def warn(self, message: Any) -> None:
        display.warning(message)

    def debug(self, message: Any) -> None:
        display.debug(message)

    # instead of self._read_config_data(path), which reads paths as absolute thus creating problems
    # in case if backend_config is provided and state_file is provided as relative path
    def read_config_data(self, path):  # type: ignore  # mypy ignore
        """
        Reads and validates the inventory source file,
        storing the provided configuration as options.
        """
        try:
            with open(path, "r") as inventory_src:
                cfg = yaml.safe_load(inventory_src)
            return cfg
        except Exception as e:
            raise AnsibleParserError(e)
