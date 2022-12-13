from typing import Union, Dict, List, Callable, Tuple

AnyJsonType = Union[Dict[str, "AnyJsonType"], List["AnyJsonType"], str, int, float, bool, None]
TJsonObject = Dict[str, AnyJsonType]
TJsonList = List[AnyJsonType]
TJsonBareValue = Union[str, int, float, bool, None]

AnsibleRunCommandType = Callable[..., Tuple[int, str, str]]
