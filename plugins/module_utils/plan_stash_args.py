PLAN_STASH_ARG_SPEC = {
    "path": {"required": True, "type": "path"},
    "var_name": {},
    "per_host": {"type": "bool", "default": False},
    "state": {"choices": ["stash", "load"], "default": "stash"},
    "binary_data": {"type": "raw"},
}
