"""
AI 转换模块

使用 OpenAI API 将小说章节转换为剧本格式。
支持角色卡注入、自动分段处理和重试机制。
"""

import json
import os

import openai
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type


class AIConverter:
    """
    AI 小说转剧本转换器。

    负责调用 OpenAI API 将小说章节转换为剧本场景。
    支持：
    - 从环境变量或参数读取 API 配置
    - 角色卡信息注入到提示词
    - 超长章节自动分段处理
    - API 调用失败自动重试（指数退避）
    """

    def __init__(self, api_key: str = None, model: str = None, api_base: str = None):
        """
        初始化 AIConverter。

        Args:
            api_key: OpenAI API Key，优先使用传入值，否则读取环境变量 OPENAI_API_KEY
            model: 模型名称，默认 gpt-3.5-turbo，可通过 OPENAI_MODEL 环境变量覆盖
            api_base: API 端点地址，默认 https://api.openai.com/v1，
                      可通过 OPENAI_API_BASE 环境变量覆盖
        """
        self.api_key = api_key or os.environ.get("OPENAI_API_KEY")
        self.model = model or os.environ.get("OPENAI_MODEL", "gpt-3.5-turbo")
        self.api_base = api_base or os.environ.get(
            "OPENAI_API_BASE", "https://api.openai.com/v1"
        )
        self._characters_str = ""

        # 兼容 openai v1.x：使用 OpenAI 客户端
        try:
            from openai import OpenAI as _OpenAI

            self._use_client = True
            self.client = _OpenAI(api_key=self.api_key, base_url=self.api_base)
        except Exception:
            # 降级为 v0.x 写法：直接设置模块级属性
            self._use_client = False
            openai.api_key = self.api_key
            openai.api_base = self.api_base

    def set_characters(self, profiles: list[dict]):
        """
        设置角色列表，将其格式化为字符串追加到 system prompt。

        Args:
            profiles: 角色列表，每个角色包含 name, gender, age, personality, notes 等字段
        """
        if not profiles:
            self._characters_str = ""
            return

        char_lines = []
        for profile in profiles:
            name = profile.get("name", "未知")
            gender = profile.get("gender", "")
            age = profile.get("age", "")
            personality = profile.get("personality", "")
            notes = profile.get("notes", "")

            parts = [f"{name}"]
            if gender:
                parts.append(f"，{gender}")
            if age:
                parts.append(f"，{age}岁")
            if personality:
                parts.append(f"，性格{personality}")
            if notes:
                parts.append(f"，{notes}")

            char_lines.append("".join(parts))

        self._characters_str = "\n已知角色：" + "；".join(char_lines)

    def _build_system_prompt(self) -> str:
        """
        构建系统提示词。

        Returns:
            包含角色信息的完整 system prompt
        """
        base = (
            '你是一个专业编剧，将小说章节转换为剧本元素。输出严格符合以下 JSON 结构：'
            '{"scenes":[{"heading":"场标（如：日内 书房）","description":"场景环境描写",'
            '"elements":[{"type":"action","description":"动作叙述"},'
            '{"type":"dialogue","character":"角色名","line":"对白",'
            '"parenthetical":"（情绪提示，可选）"}]}]}'
        )
        if self._characters_str:
            base += self._characters_str
        return base

    def _split_text(self, text: str, max_chars: int = 2000) -> list[str]:
        """
        按段落分割文本，每段不超过指定字符数。

        Args:
            text: 要分割的文本
            max_chars: 每段最大字符数，默认 2000

        Returns:
            分割后的文本段列表
        """
        paragraphs = [p.strip() for p in text.split("\n\n") if p.strip()]

        segments = []
        current = ""
        for para in paragraphs:
            if len(current) + len(para) + 2 <= max_chars:
                current = (current + "\n\n" + para).strip() if current else para
            else:
                if current:
                    segments.append(current)
                if len(para) > max_chars:
                    # 超长段落直接按字符切分
                    for i in range(0, len(para), max_chars):
                        segments.append(para[i:i + max_chars])
                    current = ""
                else:
                    current = para
        if current:
            segments.append(current)

        return segments if segments else [text]

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10),
        retry=retry_if_exception_type(Exception),
        reraise=True,
    )
    def _api_call(self, messages: list[dict]) -> str:
        """
        调用 OpenAI API，带重试机制。

        Args:
            messages: 消息列表，包含 role 和 content

        Returns:
            API 返回的内容字符串

        Raises:
            Exception: API 调用失败时抛出异常
        """
        if self._use_client:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=0.3,
                response_format={"type": "json_object"},
            )
            return response.choices[0].message.content
        else:
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=messages,
                temperature=0.3,
                response_format={"type": "json_object"},
            )
            return response.choices[0].message.content

    def _convert_segment(
        self, segment: str, segment_idx: int, total: int, chapter_title: str
    ) -> dict:
        """
        转换章节的一个分段。

        Args:
            segment: 当前分段文本
            segment_idx: 当前分段序号（从1开始）
            total: 总分段数
            chapter_title: 章节标题

        Returns:
            包含 scenes 的字典，失败时返回空字典
        """
        try:
            system_content = self._build_system_prompt() + (
                f"\n这是同一章节「{chapter_title}」的第 {segment_idx}/{total} 部分，"
                "请直接输出 scenes 数组。"
            )
            user_content = f"章节标题：{chapter_title}（第{segment_idx}/{total}段）\n内容：\n{segment}"

            raw = self._api_call([
                {"role": "system", "content": system_content},
                {"role": "user", "content": user_content},
            ])

            return json.loads(raw)
        except Exception as e:
            print(f"  第{segment_idx}/{total}段转换失败：{e}")
            return {}

    def convert_chapter(self, title: str, content: str) -> dict:
        """
        将小说章节转换为剧本场景。

        如果章节内容超过 2000 字符，会自动分段处理，最后合并场景。

        Args:
            title: 章节标题
            content: 章节内容

        Returns:
            包含 scenes 列表的字典，失败时返回空字典

        Example:
            >>> converter = AIConverter(api_key="your_key")
            >>> result = converter.convert_chapter("第一章 开始", "内容...")
            >>> print(result["scenes"])
        """
        try:
            threshold = 2000
            if len(content) <= threshold:
                system_content = self._build_system_prompt()
                user_content = f"章节标题：{title}\n内容：\n{content}"

                raw = self._api_call([
                    {"role": "system", "content": system_content},
                    {"role": "user", "content": user_content},
                ])
                return json.loads(raw)

            segments = self._split_text(content, max_chars=threshold)
            total = len(segments)
            all_scenes = []

            for idx, segment in enumerate(segments, start=1):
                result = self._convert_segment(segment, idx, total, title)
                if result and isinstance(result.get("scenes"), list):
                    all_scenes.extend(result["scenes"])

            return {"scenes": all_scenes}
        except Exception as e:
            print(f"convert_chapter 调用失败：{e}")
            return {}
