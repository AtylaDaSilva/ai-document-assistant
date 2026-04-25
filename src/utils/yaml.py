from yaml import safe_load
from typing import Any


def parse_yaml(file_path) -> dict[str, Any]:
    with open(file_path, 'r') as stream:
        data = safe_load(stream)
    return data