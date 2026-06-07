# Novel2Script - 小说转剧本 AI 助手

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue)](https://www.python.org/)
[![OpenAI](https://img.shields.io/badge/OpenAI-API-green)](https://platform.openai.com/)
[![Gradio](https://img.shields.io/badge/Gradio-4.0%2B-purple)](https://www.gradio.app/)

将小说原文自动拆分为章节，通过 AI 转换为专业剧本格式并输出 YAML。

## 🌟 功能亮点

- 📖 **智能章节切分**：自动识别「第X章」格式的章节标题，支持中文数字和阿拉伯数字
- 🎭 **角色一致性注入**：支持导入角色卡，确保剧本中角色性格、设定的一致性
- 📝 **自动分段处理**：超长章节自动分段转换，合并场景结果
- 🔄 **智能重试机制**：API 调用失败时自动重试（指数退避）
- 🖥️ **友好 Web 界面**：基于 Gradio 的可视化操作界面
- 📤 **多格式输出**：支持控制台输出和 YAML 文件导出

## 📦 依赖库列表

| 库名       | 版本要求     | 用途            |
| -------- | -------- | ------------- |
| openai   | >= 1.0.0 | 调用 OpenAI API |
| pyyaml   | >= 6.0   | YAML 文件处理     |
| tenacity | >= 8.0   | 重试机制          |
| gradio   | ==3.50.2 | Web 界面        |

## 🛠️ 安装步骤

```bash
# 克隆项目
git clone <repository-url>
cd Novel2Script

# 安装依赖
pip install -r requirements.txt
```

## 🔧 配置 API Key

### Windows

```bash
set OPENAI_API_KEY=your_api_key_here
```

### macOS / Linux

```bash
export OPENAI_API_KEY=your_api_key_here
```

### 可选环境变量

| 变量名               | 默认值                         | 说明       |
| ----------------- | --------------------------- | -------- |
| OPENAI\_MODEL     | gpt-3.5-turbo               | 使用的模型名称  |
| OPENAI\_API\_BASE | <https://api.openai.com/v1> | API 端点地址 |

## 🚀 运行方式

### 方式一：Web 界面（推荐）

```bash
python app.py
```

启动后在浏览器中打开显示的本地地址（默认 <http://127.0.0.1:7860）。>

**界面预览：**

- 左侧：小说原文输入框 + 角色卡上传
- 右侧：剧本预览 + 下载按钮
- 点击「生成剧本」一键转换

### 方式二：命令行

```bash
python main.py --input novel.txt --output script.yaml --author "鲁迅" --profiles characters.json
```

#### 参数说明

| 参数         | 说明            | 必填            |
| ---------- | ------------- | ------------- |
| --input    | 输入小说文本文件路径    | ✅ 是           |
| --output   | 输出 YAML 文件路径  | ❌ 否           |
| --author   | 原作者署名         | ❌ 否（默认"未知作者"） |
| --profiles | 角色卡 JSON 文件路径 | ❌ 否           |
| --version  | 显示版本号         | ❌ 否           |

## 📖 使用示例

### 输入示例（小说片段）

```
第一章 秋夜

窗外的雨声淅淅沥沥，林晚棠坐在窗前，手中的茶杯已经凉了。她望着窗外的梧桐树，思绪飘回到十年前。

"小姐，该用晚膳了。" 丫鬟小翠轻轻推门进来。

林晚棠回过神来，点了点头。
```

### 角色卡示例（JSON）

```json
[
  {"name": "林晚棠", "gender": "女", "age": 28, "personality": "温婉", "notes": "主角，书香门第小姐"},
  {"name": "小翠", "gender": "女", "age": 18, "personality": "机灵", "notes": "林晚棠的贴身丫鬟"}
]
```

### 输出示例（YAML）

```yaml
metadata:
  author: "鲁迅"
  total_scenes: 1
scenes:
  - scene_id: S001
    heading: "夜内 林府书房"
    description: "书房内灯火昏黄，窗外雨声淅沥。林晚棠坐在窗前，神情有些恍惚。"
    elements:
      - element_id: A001
        type: action
        description: "林晚棠望着窗外的梧桐树，手中的茶杯已经凉透。"
      - element_id: D001
        type: dialogue
        character: "小翠"
        line: "小姐，该用晚膳了。"
      - element_id: A002
        type: action
        description: "小翠轻轻推门进来，手里端着一个食盒。"
      - element_id: D002
        type: dialogue
        character: "林晚棠"
        line: "知道了。"
        parenthetical: "（轻轻点头）"
```

## 🧠 原创功能说明

### 1. 章节切分规则

使用正则表达式 `r'第[零一二三四五六七八九十百千万\d]+章[^\n]*'` 匹配章节标题：

- 支持中文数字：第一章、第二十章
- 支持阿拉伯数字：第1章、第100章
- 支持标题后缀：第三章 夜访、第五章·重逢

### 2. 角色一致性注入

角色卡信息会被追加到 AI 的 system prompt 中：

```
已知角色：张三，男，25岁，性格冲动；李四，女，20岁，性格温柔
```

确保 AI 在生成剧本时能参考角色设定，保持角色性格和行为的一致性。

### 3. 自动分段处理

当章节内容超过 2000 字符时，系统会：

1. 按段落分割文本（以 `\n\n` 为分隔符）
2. 逐段调用 AI 转换，标记当前段位置（第X/Y段）
3. 合并所有段的场景结果

### 4. Gradio 界面

提供直观的可视化操作界面：

- 实时预览转换结果
- 支持上传角色卡文件
- 一键下载 YAML 文件
- 友好的错误提示

## 📁 项目结构

```
Novel2Script/
├── src/                    # 源代码包
│   └── novel2script/       # 核心模块包
│       ├── __init__.py     # 包初始化
│       ├── chapter_splitter.py   # 章节切分模块
│       ├── ai_converter.py       # AI 转换模块
│       ├── script_builder.py     # 剧本构建模块
│       ├── yaml_writer.py        # YAML 输出模块
│       └── character_profile.py   # 角色卡处理模块
├── examples/               # 示例文件
│   ├── example.txt         # 示例小说文本
│   └── characters.json     # 示例角色卡
├── main.py                 # 命令行入口
├── app.py                  # Gradio 界面入口
├── requirements.txt        # 依赖列表
├── README.md               # 项目说明
└── SCHEMA.md               # 数据结构说明
```

## 📝 版本历史

- v1.0.0：初始版本，支持章节切分、AI 转换、YAML 输出
- v1.1.0：添加角色卡支持、自动分段、重试机制
- v1.2.0：添加 Gradio Web 界面

## 📄 许可证

MIT License
