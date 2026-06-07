import yaml


def script_to_yaml(script: dict) -> str:
    """
    将 script 字典转换为 YAML 字符串，保持中文可读性。
    """
    return yaml.dump(script, allow_unicode=True, sort_keys=False)
