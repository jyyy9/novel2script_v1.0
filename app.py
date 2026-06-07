import os
import json
import tempfile

import gradio as gr

from chapter_splitter import split_chapters
from ai_converter import AIConverter
from script_builder import build_script
from yaml_writer import script_to_yaml


def convert_novel_to_script(novel_text: str, profiles_file) -> tuple[str, str]:
    if not novel_text or not novel_text.strip():
        return "请输入小说原文", None

    if not os.environ.get("OPENAI_API_KEY"):
        return "错误：请先设置环境变量 OPENAI_API_KEY 后再使用", None

    chapters = split_chapters(novel_text)
    if not chapters:
        return "未能识别到任何章节内容", None

    converter = AIConverter()

    if profiles_file is not None:
        try:
            with open(profiles_file.name, "r", encoding="utf-8") as f:
                profiles = json.load(f)
            if isinstance(profiles, list) and profiles:
                converter.set_characters(profiles)
        except Exception as e:
            print(f"读取角色卡失败：{e}")

    chapters_results = []
    for idx, chapter in enumerate(chapters, start=1):
        print(f"处理章节 {idx}/{len(chapters)}: {chapter['title']}")
        result = converter.convert_chapter(
            title=chapter["title"],
            content=chapter["content"],
        )
        if result and isinstance(result.get("scenes"), list):
            chapters_results.append(result)
        else:
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

    script = build_script(
        original_author="未知作者",
        chapters_results=chapters_results,
    )
    yaml_str = script_to_yaml(script)

    with tempfile.NamedTemporaryFile(
        mode="w", suffix=".yaml", delete=False, encoding="utf-8"
    ) as f:
        f.write(yaml_str)
        output_path = f.name

    return yaml_str, output_path


def build_interface():
    with gr.Blocks(title="小说转剧本 AI 助手") as demo:
        gr.Markdown("# 小说转剧本 AI 助手")
        gr.Markdown(
            "将小说原文自动拆分为章节，并调用 AI 转换为剧本格式（YAML）。"
        )

        with gr.Row():
            with gr.Column():
                novel_input = gr.Textbox(
                    label="小说原文",
                    placeholder="在此粘贴小说文本...",
                    lines=18,
                )
                profiles_input = gr.File(
                    label="角色卡（可选，JSON 格式）",
                    file_types=[".json"],
                )
                run_btn = gr.Button("生成剧本", variant="primary")

            with gr.Column():
                yaml_output = gr.Textbox(
                    label="生成的剧本（YAML）",
                    lines=18,
                )
                file_output = gr.File(label="下载 YAML 文件")

        run_btn.click(
            fn=convert_novel_to_script,
            inputs=[novel_input, profiles_input],
            outputs=[yaml_output, file_output],
        )

    return demo


if __name__ == "__main__":
    demo = build_interface()
    demo.launch(server_name="127.0.0.1")
