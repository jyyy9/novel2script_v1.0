"""
YAML 输出模块

提供将剧本字典转换为 YAML 字符串的功能。
"""

import yaml


def script_to_yaml(script: dict) -> str:
    """
    将剧本字典转换为 YAML 字符串。

    Args:
        script: 剧本字典，包含 metadata 和 scenes

    Returns:
        YAML 格式的字符串，保持中文可读性

    Example:
        >>> script = {"metadata": {...}, "scenes": [...]}
        >>> yaml_str = script_to_yaml(script)
    """
    return yaml.dump(script, allow_unicode=True, sort_keys=False)
