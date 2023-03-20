from typing import Any, Dict, List, Union, Optional
from dataclasses import dataclass

from ansible_collections.cloud.terraform.plugins.module_utils.types import AnyJsonType, TJsonObject


@dataclass
class TerraformWorkspaceContext:
    current: str
    all: List[str]


@dataclass
class TerraformOutput:
    sensitive: bool
    value: Any
    # as string is shown "string"
    # a list of strings is shown as ["list", "string"]
    type: Union[str, List[str]]

    @classmethod
    def from_json(cls, json: TJsonObject) -> "TerraformOutput":
        return cls(sensitive=json.get("sensitive"), value=json.get("value"), type=json.get("type"))


@dataclass
class TerraformRootModuleResource:
    address: str
    mode: str
    type: str
    name: str
    provider_name: str
    schema_version: int
    values: Dict[str, AnyJsonType]

    # potentially undefined
    sensitive_values: Dict[str, Union[bool, List[bool], Dict[str, bool]]]
    depends_on: List[str]

    @classmethod
    def from_json(cls, json: TJsonObject) -> "TerraformRootModuleResource":
        return cls(
            address=json["address"],
            mode=json["mode"],
            type=json["type"],
            name=json["name"],
            provider_name=json["provider_name"],
            schema_version=json["schema_version"],
            values=json["values"],
            sensitive_values=json.get("sensitive_values", {}),
            depends_on=json.get("depends_on", []),
        )


@dataclass
class TerraformAnsibleProvider:
    name: str
    groups: List[str]
    children: List[str]
    variables: Dict[str, str]

    @classmethod
    def from_json(cls, json: TerraformRootModuleResource) -> "TerraformAnsibleProvider":
        return cls(
            name=json.values.get("name", None),
            groups=json.values.get("groups", []),
            children=json.values.get("children", []),
            variables=json.values.get("variables", {}),
        )


@dataclass
class TerraformRootModule:
    resources: List[TerraformRootModuleResource]

    @classmethod
    def from_json(cls, json: TJsonObject) -> "TerraformRootModule":
        return cls(resources=[TerraformRootModuleResource.from_json(r) for r in json.get("resources", [])])


@dataclass
class TerraformShowValues:
    outputs: Dict[str, TerraformOutput]
    root_module: TerraformRootModule

    @classmethod
    def from_json(cls, json: TJsonObject) -> "TerraformShowValues":
        return cls(
            outputs={
                output_name: TerraformOutput.from_json(output_value)
                for output_name, output_value in json.get("outputs", {}).items()
            },
            root_module=TerraformRootModule.from_json(json["root_module"]),
        )


@dataclass
class TerraformShow:
    format_version: str
    terraform_version: str
    values: TerraformShowValues

    @classmethod
    def from_json(cls, json: TJsonObject) -> "TerraformShow":
        return cls(
            format_version=json["format_version"],
            terraform_version=json["terraform_version"],
            values=TerraformShowValues.from_json(json["values"]),
        )


@dataclass
class TerraformAttributeSpec:
    type: Union[str, List[str]]
    description_kind: str

    # potentially undefined
    description: Optional[str]
    optional: bool
    required: bool
    deprecated: bool
    sensitive: bool
    computed: bool

    @classmethod
    def from_json(cls, json: TJsonObject) -> "TerraformAttributeSpec":
        return cls(
            type=json["type"],
            description_kind=json["description_kind"],
            description=json.get("description"),
            optional=json.get("optional", False),
            required=json.get("required", False),
            deprecated=json.get("deprecated", False),
            sensitive=json.get("sensitive", False),
            computed=json.get("computed", False),
        )


@dataclass
class TerraformBlockSensitive:
    sensitive: bool

    @classmethod
    def create(cls, block_sensitive: bool) -> "TerraformBlockSensitive":
        return cls(sensitive=block_sensitive)


@dataclass
class TerraformResourceSchema:
    version: int
    # this de-nests the "block" and the "block_type" subelement
    # but "block_type" is simplified - contains only sensitive attribute
    attributes: Dict[str, Union[TerraformAttributeSpec, TerraformBlockSensitive]]

    @classmethod
    def from_json(cls, json: TJsonObject) -> "TerraformResourceSchema":
        attributes: Dict[str, Union[TerraformAttributeSpec, TerraformBlockSensitive]] = {
            attr_name: TerraformAttributeSpec.from_json(attr_value)
            for attr_name, attr_value in json.get("block", {}).get("attributes", {}).items()
        }
        for block_name, block_value in json.get("block", {}).get("block_types", {}).items():
            block_attributes = {
                block_attr_name: TerraformAttributeSpec.from_json(block_attr_value)
                for block_attr_name, block_attr_value in block_value.get("block", {}).get("attributes", {}).items()
            }
            sensitive_list = [
                block_attribute_value.sensitive
                for block_attribute_name, block_attribute_value in block_attributes.items()
            ]
            # if one attribute is sensitive, we make the whole block sensitive
            attributes[block_name] = TerraformBlockSensitive.create(any(sensitive_list))

        return cls(
            version=json["version"],
            attributes=attributes,
        )


@dataclass
class TerraformProviderSchema:
    resource_schemas: Dict[str, TerraformResourceSchema]

    @classmethod
    def from_json(cls, json: TJsonObject) -> "TerraformProviderSchema":
        return cls(
            resource_schemas={
                schema_name: TerraformResourceSchema.from_json(schema_value)
                for schema_name, schema_value in json.get("resource_schemas", {}).items()
            }
        )


@dataclass
class TerraformProviderSchemaCollection:
    format_version: str
    provider_schemas: Dict[str, TerraformProviderSchema]

    @classmethod
    def from_json(cls, json: TJsonObject) -> "TerraformProviderSchemaCollection":
        return cls(
            format_version=json["format_version"],
            provider_schemas={
                schema_name: TerraformProviderSchema.from_json(schema_value)
                for schema_name, schema_value in json.get("provider_schemas", {}).items()
            },
        )
