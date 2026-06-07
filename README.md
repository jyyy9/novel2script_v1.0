# Novel2Script - 小说转剧本 AI 助手

将小说原文自动拆分为章节，通过 AI 转换为剧本格式并输出 YAML。

## 安装依赖

```bash
pip install -r requirements.txt
```

## 配置 API Key

```bash
# Windows
set OPENAI_API_KEY=your_api_key_here

# macOS / Linux
export OPENAI_API_KEY=your_api_key_here
```

可选的其他环境变量：

- `OPENAI_MODEL`：模型名称，默认 `gpt-3.5-turbo`
- `OPENAI_API_BASE`：API 端点地址，默认 `https://api.openai.com/v1`

## 使用 Web 界面（Gradio）

```bash
python app.py
```

启动后在浏览器中打开显示的本地地址（默认 http://127.0.0.1:7860）。

在界面中：
- **小说原文**：粘贴小说文本（必填）
- **角色卡**：上传 JSON 格式的角色卡文件（可选）
- 点击"生成剧本"按钮，右侧将显示生成的 YAML 剧本，并提供下载链接

## 使用命令行

```bash
python main.py --input novel.txt --output script.yaml --author "作者名" --profiles characters.json
```

参数说明：
- `--input`：输入小说文本文件（必填）
- `--output`：输出 YAML 文件路径（可选，不填则打印到控制台）
- `--author`：原作者署名（可选，默认"未知作者"）
- `--profiles`：角色卡 JSON 文件路径（可选）

## 角色卡 JSON 格式示例

```json
[
  {"name": "张三", "gender": "男", "age": 25, "personality": "冲动", "notes": "主角"},
  {"name": "李四", "gender": "女", "age": 20, "personality": "温柔"}
]
```
