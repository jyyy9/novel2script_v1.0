"""
章节切分模块

提供将小说文本按章节标题切分的功能。
"""

import re


def split_chapters(text: str) -> list[dict]:
    """
    将小说文本按章节标题切分为多个章节。

    使用正则表达式匹配章节标题（如「第X章」、「第1章」等），
    并将每个标题及其后续内容作为一个章节。

    Args:
        text: 小说原文文本

    Returns:
        章节列表，每个章节是包含 title 和 content 的字典：
        [{"title": "第三章 夜访", "content": "..."}, ...]

    Example:
        >>> text = "第一章 开始\\n内容...\\n\\n第二章 发展\\n内容..."
        >>> split_chapters(text)
        [{"title": "第一章 开始", "content": "内容..."}, {"title": "第二章 发展", "content": "内容..."}]
    """
    pattern = r'第[零一二三四五六七八九十百千万\d]+章[^\n]*'
    matches = list(re.finditer(pattern, text))

    if not matches:
        return [{"title": "全文", "content": text.strip()}]

    chapters: list[dict] = []
    for i, match in enumerate(matches):
        title = match.group().strip()
        start = match.end()
        if i + 1 < len(matches):
            end = matches[i + 1].start()
        else:
            end = len(text)
        content = text[start:end].strip()
        chapters.append({"title": title, "content": content})

    return chapters
