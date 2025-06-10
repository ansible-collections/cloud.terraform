import pytest
from ansible_collections.cloud.terraform.plugins.module_utils.utils import _convert_value_to_hcl, ansible_dict_to_hcl


class TestConvertToHCL:
    @pytest.mark.parametrize(
        "pyvalue, hclvalue",
        [
            (1, "1"),
            (1.23, "1.23"),
            (None, "None"),
            ("1", '"1"'),
            ("string_value", '"string_value"'),
            (True, "true"),
            (False, "false"),
            ("some\nvalue", "\n".join(["<<EOF", "some", "value", "EOF"])),
        ],
    )
    def test__convert_value_to_hcl(self, pyvalue, hclvalue):
        res = _convert_value_to_hcl(pyvalue)
        assert res == hclvalue, f"Error converting Python dict value to HCL. Expected ({hclvalue}) Got ({res})"

    @pytest.mark.parametrize(
        "value, key, expected",
        [
            (
                {"organization": "ansible"},
                None,
                "\n".join(["{", 'organization = "ansible"', "}"]),
            ),
            (
                {"organization": "ansible", "token": "9zkxXORw8Uw9cQ.atlas"},
                None,
                "\n".join(["{", 'organization = "ansible"', 'token = "9zkxXORw8Uw9cQ.atlas"', "}"]),
            ),
            (
                {"organization": "ansible"},
                "remote",
                "\n".join(["remote {", 'organization = "ansible"', "}"]),
            ),
            (
                {"organization": "ansible", "token": "9zkxXORw8Uw9cQ.atlas"},
                "cloud",
                "\n".join(["cloud {", 'organization = "ansible"', 'token = "9zkxXORw8Uw9cQ.atlas"', "}"]),
            ),
            (
                ["redhat", True],
                None,
                "\n".join(['["redhat", true]']),
            ),
            (
                ["redhat", True],
                "attributes",
                "\n".join(['attributes = ["redhat", true]']),
            ),
            (
                {"organizations": ["redhat", "ansible"]},
                None,
                "\n".join(["{", 'organizations = ["redhat", "ansible"]', "}"]),
            ),
        ],
    )
    def test__ansible_dict_to_hcl(self, value, key, expected):
        res = ansible_dict_to_hcl(value, key)
        assert res == expected, f"Error converting Python dict value to HCL. Expected ({expected}) Got ({res})"
