from __future__ import absolute_import, division, print_function


from typing import Any, Dict, NoReturn

from ansible.module_utils.basic import AnsibleModule

__metaclass__ = type


class TerraformCollectionException(Exception):
    def __init__(self, message: str) -> None:
        self.message = message


class TerraformWarning(TerraformCollectionException):
    """An exception that results in a non-fatal warning."""


class TerraformError(TerraformCollectionException):
    """An exception that results in a fatal error."""

    def __init__(self, message: str, **kwargs: Any):
        super().__init__(message)
        if kwargs is None:
            self.kwargs: Dict[str, Any] = {}
        else:
            self.kwargs = kwargs

    def fail_json(self, module: AnsibleModule) -> NoReturn:
        module.fail_json(msg=self.message, **self.kwargs)
        # fail_json does not return, hinting to the type checker explicitly
        raise AssertionError("fail_json should have exited the process")
