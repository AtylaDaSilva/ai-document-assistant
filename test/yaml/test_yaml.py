from src.utils.yaml import parse_yaml


def test_basic_yaml_parse():
    yaml_path = "test/yaml/test.yaml"
    data = parse_yaml(yaml_path)
    assert isinstance(data, dict) and len(data) > 0