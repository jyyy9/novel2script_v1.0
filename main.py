import argparse
import json
import os
import sys

from chapter_splitter import split_chapters
from ai_converter import AIConverter
from script_builder import build_script
from yaml_writer import script_to_yaml
from character_profile import load_profiles


def main():
    parser = argparse.ArgumentParser(description='Novel2Script - Convert novel text to script')
    parser.add_argument('--input', required=True, help='Input novel text file path')
    parser.add_argument('--output', help='Output YAML file path (optional)')
    parser.add_argument('--author', default="未知作者", help='Original author name')
    parser.add_argument('--profiles', help='Character profiles JSON file path')
    args = parser.parse_args()

    # 读取输入文件
    with open(args.input, 'r', encoding='utf-8') as f:
        content = f.read()

    # 切分章节
    chapters = split_chapters(content)
    print(f"共切分出 {len(chapters)} 个章节")

    # 检查 API Key
    if not os.environ.get("OPENAI_API_KEY"):
        print("错误：请设置环境变量 OPENAI_API_KEY")
        sys.exit(1)

    if not chapters:
        print("没有可处理的章节")
        return

    # 创建 AIConverter 实例
    converter = AIConverter()

    # 如果提供了角色卡文件，加载并设置
    if args.profiles:
        profiles = load_profiles(args.profiles)
        if profiles:
            print(f"已加载 {len(profiles)} 个角色")
            converter.set_characters(profiles)
        else:
            print(f"警告：未能加载角色卡 {args.profiles}")

    # 逐章调用 AI 转换，收集结果
    chapters_results = []
    for i, chapter in enumerate(chapters):
        print(f"正在处理第 {i+1}/{len(chapters)} 章: {chapter['title']}")
        result = converter.convert_chapter(
            title=chapter['title'],
            content=chapter['content'],
        )
        if result:
            chapters_results.append(result)
            print(f"  成功，获得 {len(result.get('scenes', []))} 个场景")
        else:
            # 插入占位场景
            print(f"  失败，插入占位场景")
            chapters_results.append({
                "scenes": [{
                    "heading": f"占位场景 - {chapter['title']}",
                    "description": "（AI 转换失败占位）",
                    "elements": [{
                        "type": "action",
                        "description": f"（此处内容来自章节：{chapter['title']}，AI 转换失败）"
                    }]
                }]
            })

    # 构建完整剧本
    script = build_script(original_author=args.author, chapters_results=chapters_results)
    print(f"\n剧本构建完成，共 {script['metadata']['total_scenes']} 个场景")

    # 转换为 YAML
    yaml_output = script_to_yaml(script)

    # 输出
    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(yaml_output)
        print(f"已写入 YAML 文件: {args.output}")
    else:
        print(yaml_output)


if __name__ == '__main__':
    main()
