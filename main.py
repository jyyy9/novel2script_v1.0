"""
Novel2Script - 小说转剧本 AI 助手

将小说原文自动拆分为章节，通过 AI 转换为剧本格式并输出 YAML。
"""

import argparse
import json
import os
import sys

from src.novel2script.chapter_splitter import split_chapters
from src.novel2script.ai_converter import AIConverter
from src.novel2script.script_builder import build_script
from src.novel2script.yaml_writer import script_to_yaml
from src.novel2script.character_profile import load_profiles

__version__ = "1.2.0"


def main():
    """
    主函数：解析命令行参数，执行小说到剧本的转换流程。
    """
    parser = argparse.ArgumentParser(
        description='Novel2Script - Convert novel text to script'
    )
    parser.add_argument(
        '--input', required=True, help='Input novel text file path'
    )
    parser.add_argument(
        '--output', help='Output YAML file path (optional)'
    )
    parser.add_argument(
        '--author', default="未知作者", help='Original author name'
    )
    parser.add_argument(
        '--profiles', help='Character profiles JSON file path'
    )
    parser.add_argument(
        '--version', action='version', version=f'%(prog)s {__version__}'
    )
    args = parser.parse_args()

    # 检查输入文件是否存在
    if not os.path.exists(args.input):
        print(f"错误：输入文件 '{args.input}' 不存在")
        sys.exit(1)

    if not os.path.isfile(args.input):
        print(f"错误：'{args.input}' 不是有效的文件")
        sys.exit(1)

    # 读取输入文件
    try:
        with open(args.input, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"错误：读取文件 '{args.input}' 失败 - {e}")
        sys.exit(1)

    if not content.strip():
        print("错误：输入文件内容为空")
        sys.exit(1)

    # 切分章节
    chapters = split_chapters(content)
    print(f"共切分出 {len(chapters)} 个章节")

    # 检查 API Key
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        print("错误：请先设置环境变量 OPENAI_API_KEY")
        print("Windows: set OPENAI_API_KEY=your_api_key")
        print("macOS/Linux: export OPENAI_API_KEY=your_api_key")
        sys.exit(1)

    if not chapters:
        print("警告：未能识别到任何章节，将整篇作为一个章节处理")
        chapters = [{"title": "全文", "content": content}]

    # 创建 AIConverter 实例
    try:
        converter = AIConverter()
    except Exception as e:
        print(f"错误：初始化 AIConverter 失败 - {e}")
        sys.exit(1)

    # 如果提供了角色卡文件，加载并设置
    if args.profiles:
        if not os.path.exists(args.profiles):
            print(f"错误：角色卡文件 '{args.profiles}' 不存在")
            sys.exit(1)

        profiles = load_profiles(args.profiles)
        if profiles:
            print(f"已加载 {len(profiles)} 个角色")
            converter.set_characters(profiles)
        else:
            print(f"警告：未能加载角色卡 '{args.profiles}'")

    # 逐章调用 AI 转换，收集结果
    chapters_results = []
    for i, chapter in enumerate(chapters):
        print(f"正在处理第 {i+1}/{len(chapters)} 章: {chapter['title']}")
        try:
            result = converter.convert_chapter(
                title=chapter['title'],
                content=chapter['content'],
            )
            if result and isinstance(result.get("scenes"), list):
                chapters_results.append(result)
                print(f"  成功，获得 {len(result['scenes'])} 个场景")
            else:
                print(f"  失败，插入占位场景")
                chapters_results.append({
                    "scenes": [{
                        "heading": f"占位场景 - {chapter['title']}",
                        "description": "（AI 转换失败占位）",
                        "elements": [{
                            "type": "action",
                            "description": (
                                f"（此处内容来自章节：{chapter['title']}，"
                                "AI 转换失败）"
                            )
                        }]
                    }]
                })
        except Exception as e:
            print(f"  处理失败: {e}")
            chapters_results.append({
                "scenes": [{
                    "heading": f"占位场景 - {chapter['title']}",
                    "description": "（处理异常占位）",
                    "elements": [{
                        "type": "action",
                        "description": (
                            f"（章节：{chapter['title']} 处理异常: {e}）"
                        )
                    }]
                }]
            })

    # 构建完整剧本
    try:
        script = build_script(
            original_author=args.author,
            chapters_results=chapters_results
        )
        print(f"\n剧本构建完成，共 {script['metadata']['total_scenes']} 个场景")
    except Exception as e:
        print(f"错误：构建剧本失败 - {e}")
        sys.exit(1)

    # 转换为 YAML
    try:
        yaml_output = script_to_yaml(script)
    except Exception as e:
        print(f"错误：转换为 YAML 失败 - {e}")
        sys.exit(1)

    # 输出
    if args.output:
        try:
            with open(args.output, 'w', encoding='utf-8') as f:
                f.write(yaml_output)
            print(f"已写入 YAML 文件: {args.output}")
        except Exception as e:
            print(f"错误：写入文件 '{args.output}' 失败 - {e}")
            sys.exit(1)
    else:
        print(yaml_output)


if __name__ == '__main__':
    main()
