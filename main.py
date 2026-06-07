import argparse
import json
import os
import sys

from chapter_splitter import split_chapters
from ai_converter import AIConverter


def main():
    parser = argparse.ArgumentParser(description='Novel2Script - Convert novel text to script')
    parser.add_argument('--input', required=True, help='Input novel text file path')
    args = parser.parse_args()

    # 读取并打印输入文件
    with open(args.input, 'r', encoding='utf-8') as f:
        content = f.read()

    # 切分章节并打印预览
    chapters = split_chapters(content)
    for chapter in chapters:
        print(f"【{chapter['title']}】")
        print(chapter['content'][:100])
        print('---')

    # 检查 API Key 环境变量
    if not os.environ.get("OPENAI_API_KEY"):
        print("错误：请设置环境变量 OPENAI_API_KEY")
        sys.exit(1)

    if not chapters:
        print("没有可处理的章节")
        return

    # 创建 AIConverter 实例（自动读取环境变量）
    converter = AIConverter()

    # 处理第一个章节
    first_chapter = chapters[0]
    result = converter.convert_chapter(
        title=first_chapter['title'],
        content=first_chapter['content'],
    )
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
