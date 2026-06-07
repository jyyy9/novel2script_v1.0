import re


def split_chapters(text: str) -> list[dict]:
    """
    返回形如 [{"title": "第三章 夜访", "content": "..."}, ...] 的列表。
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

#测试
if __name__ == "__main__":
    # 从 chapter_splitter 导入函数（如果直接在本文件测试，直接调用即可）
    # 假设函数名是 split_chapters

    # ---------- 测试文本 1：标准章节 ----------
    text_standard = """第一章 开始
这里有一些叙述。

第二章 发展
剧情正在展开。

第三章 高潮
高潮部分到来，冲突爆发。"""

    # ---------- 测试文本 2：无章节标记 ----------
    text_no_chapter = """这是一段没有任何章节标题的小说片段。
故事就这样开始了，没有第一章，也没有第二章。
只有连续的叙述和描写。"""

    # ---------- 测试文本 3：混合情况（开头无标题，后面有） ----------
    text_mixed = """在这一切发生之前，谁也没有料到会是这样的结果。
这是开头的引子，没有章节编号。

第一章 变故
变故发生了，所有人的命运都改变了。

第二章 追寻
主角踏上了追寻真相的道路。"""

    # 分别测试
    print("=" * 40)
    print("测试 1：标准章节文本")
    chapters = split_chapters(text_standard)
    print(f"章节数量：{len(chapters)}")
    for i, ch in enumerate(chapters):
        print(f"  {i+1}. 标题：'{ch['title']}'，内容长度：{len(ch['content'])} 字")
        # 可选：打印内容前50字
        preview = ch['content'][:50].replace('\n', ' ')
        print(f"     内容预览：{preview}...")

    print("\n" + "=" * 40)
    print("测试 2：无章节标记文本")
    chapters = split_chapters(text_no_chapter)
    print(f"章节数量：{len(chapters)}")
    for i, ch in enumerate(chapters):
        print(f"  {i+1}. 标题：'{ch['title']}'")
        preview = ch['content'][:50].replace('\n', ' ')
        print(f"     内容预览：{preview}...")

    print("\n" + "=" * 40)
    print("测试 3：混合情况（开头无标题）")
    chapters = split_chapters(text_mixed)
    print(f"章节数量：{len(chapters)}")
    for i, ch in enumerate(chapters):
        print(f"  {i+1}. 标题：'{ch['title']}'")
        preview = ch['content'][:50].replace('\n', ' ')
        print(f"     内容预览：{preview}...")
