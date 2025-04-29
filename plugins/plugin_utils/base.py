# -*- coding: utf-8 -*-

# (c) 2023 Red Hat Inc.
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from typing import Any

from ansible.plugins.inventory import BaseInventoryPlugin
from ansible.utils.display import Display

display = Display()


class TerraformInventoryPluginBase(BaseInventoryPlugin):  # type: ignore  # mypy ignore
    def warn(self, message: Any) -> None:
        display.warning(message)

    def debug(self, message: Any) -> None:
        display.debug(message)
