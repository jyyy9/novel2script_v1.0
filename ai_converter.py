import json
import os

import openai


class AIConverter:
    def __init__(self, api_key: str = None, model: str = None, api_base: str = None):
        # 优先使用传入参数，否则读取环境变量
        self.api_key = api_key or os.environ.get("OPENAI_API_KEY")
        self.model = model or os.environ.get("OPENAI_MODEL", "gpt-3.5-turbo")
        self.api_base = api_base or os.environ.get(
            "OPENAI_API_BASE", "https://api.openai.com/v1"
        )

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

    def convert_chapter(self, title: str, content: str) -> dict:
        try:
            system_content = (
                '你是一个专业编剧，将小说章节转换为剧本元素。输出严格符合以下 JSON 结构：'
                '{"scenes":[{"heading":"场标（如：日内 书房）","description":"场景环境描写",'
                '"elements":[{"type":"action","description":"动作叙述"},'
                '{"type":"dialogue","character":"角色名","line":"对白",'
                '"parenthetical":"（情绪提示，可选）"}]}]}'
            )
            user_content = f"章节标题：{title}\n内容：\n{content}"

            if self._use_client:
                # openai v1.x 新版 API
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=[
                        {"role": "system", "content": system_content},
                        {"role": "user", "content": user_content},
                    ],
                    temperature=0.3,
                    response_format={"type": "json_object"},
                )
                raw = response.choices[0].message.content
            else:
                # openai v0.x 旧版 API
                response = openai.ChatCompletion.create(
                    model=self.model,
                    messages=[
                        {"role": "system", "content": system_content},
                        {"role": "user", "content": user_content},
                    ],
                    temperature=0.3,
                    response_format={"type": "json_object"},
                )
                raw = response.choices[0].message.content

            return json.loads(raw)
        except Exception as e:
            print(f"convert_chapter 调用失败：{e}")
            return {}
