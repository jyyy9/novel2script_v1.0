"""
角色卡模块

提供读取和处理角色卡 JSON 文件的功能。
"""

import json


def load_profiles(filepath: str) -> list[dict]:
    """
    读取角色卡 JSON 文件。

    Args:
        filepath: JSON 文件路径，内容应为数组，每个对象包含：
                  name, gender, age, personality, notes 等字段

    Returns:
        角色列表，每个角色是包含上述字段的字典。
        读取失败时返回空列表。

    Example:
        >>> profiles = load_profiles("characters.json")
        >>> print(profiles[0]["name"])
    """
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        if isinstance(data, list):
            return data
        else:
            print(f"警告：{filepath} 不是有效的 JSON 数组")
            return []
    except Exception as e:
        print(f"读取角色卡失败：{e}")
        return []
