# Novel2Script YAML Schema

## 1. 设计目标

- **可读性**：作者和开发人员能直接看懂，无需复杂工具。
- **完整性**：覆盖剧本写作的核心元素（场景标题、动作描写、对白、角色情绪/动作提示）。
- **可编辑性**：每个元素都有唯一 ID，方便后续工具（如编辑器、版本控制）进行定位和修改。
- **可扩展性**：未来可以无缝增加镜头、转场、音效等新元素，不破坏现有结构。

## 2.剧本数据结构

### 顶层结构

```yaml
metadata:
  author: "作者名"
  total_scenes: 场景总数（整数）
scenes:
  - scene_id: S001
    heading: "场标（如：日内 书房）"
    description: "场景环境描写"
    elements:
      - element_id: A001
        type: action
        description: "动作叙述"
      - element_id: D001
        type: dialogue
        character: "角色名"
        line: "对白内容"
        parenthetical: "（情绪提示，可选）"
```

### 字段说明

#### metadata（元数据）

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| author | string | 是 | 原小说作者名 |
| total_scenes | int | 是 | 剧本包含的场景总数 |

#### scenes（场景列表）

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| scene_id | string | 是 | 场景唯一标识，格式 S+三位数字（如 S001） |
| heading | string | 是 | 场标，格式为「时间 地点」（如：日内 书房） |
| description | string | 是 | 场景环境描写 |
| elements | list | 是 | 场景包含的剧本元素列表 |

#### elements（剧本元素）

剧本元素分为两种类型：

##### action（动作）

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| element_id | string | 是 | 元素唯一标识，格式 A+三位数字（如 A001） |
| type | string | 是 | 值为 "action" |
| description | string | 是 | 动作叙述内容 |

##### dialogue（对白）

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| element_id | string | 是 | 元素唯一标识，格式 D+三位数字（如 D001） |
| type | string | 是 | 值为 "dialogue" |
| character | string | 是 | 角色名称 |
| line | string | 是 | 对白内容 |
| parenthetical | string | 否 | 情绪提示，如「（略带嘲讽）」 |

### 完整示例

```yaml
metadata:
  author: "鲁迅"
  total_scenes: 2
scenes:
  - scene_id: S001
    heading: "日内 鲁镇酒店"
    description: "咸亨酒店内，柜台擦得锃亮，三三两两的酒客坐在桌旁。"
    elements:
      - element_id: A001
        type: action
        description: "孔乙己拖着断腿，慢慢挪进酒店，在柜台前的凳子上坐下。"
      - element_id: D001
        type: dialogue
        character: "孔乙己"
        line: "温两碗酒，要一碟茴香豆。"
        parenthetical: "（声音低微却带着几分傲气）"
      - element_id: A002
        type: action
        description: "掌柜从柜台里拿出酒碗，筛了两碗酒。"
  - scene_id: S002
    heading: "傍晚 孔乙己家"
    description: "一间破败的小屋，墙角堆着几卷旧书。"
    elements:
      - element_id: A003
        type: action
        description: "孔乙己躺在床上，望着屋顶的破洞发呆。"
      - element_id: D002
        type: dialogue
        character: "孔乙己"
        line: "多乎哉？不多也……"
```

## JSON Schema 规范（API 响应格式）

AI 转换章节时返回的 JSON 格式：

```json
{
  "scenes": [
    {
      "heading": "场标",
      "description": "场景环境描写",
      "elements": [
        {"type": "action", "description": "动作叙述"},
        {"type": "dialogue", "character": "角色名", "line": "对白", "parenthetical": "（情绪提示，可选）"}
      ]
    }
  ]
}
```
## 3. 设计原因

​		这套设计的核心思想主要有五点。第一，用统一的 `elements` 列表而不是把 `dialogues` 和 `actions` 分开存储，是因为剧本本质上是一条时间线，对白和动作往往交织在一起，统一列表能严格保留它们在剧情中的先后顺序，方便播放器按序朗读或按时间线呈现，这也是好莱坞主流剧本工具（如 Final Draft）采用的“元素流”思路。第二，每个元素都带上 `id`，主要是为了方便作者精确修改和版本管理——作者可以直接说“改一下第七场第三句对白”而不用费力描述位置，用 Git 等工具做 diff 时也能精确到每个元素，未来如果需要多人协作编辑，这些 `id` 也能作为锚点使用。第三，保留 `parenthetical` 字段是因为它在剧本写作中常用来标注角色的语气、动作或情绪（比如“愤怒地”“低声说”），虽然看起来是个小细节，但对演员表演和 AI 生成都很有价值，AI 可以根据上下文自动推测这类提示，帮作者省掉不少手写功夫，让初稿更有现场感。第四，在顶层保留 `adaptor` 和 `date` 字段，是为了明确这份剧本是 AI 辅助生成的初稿而非最终成品，保留完整的创作链条信息，让作者清楚知道稿子的来源和生成时间，方便在此基础上自由修改。第五，从小说到剧本的映射过程，是通过大语言模型将小说的叙述段落先拆解成一个个场景，再在每个场景里区分出动作描写和角色对白，同时尝试识别角色名字和情绪提示——整个过程是可解释、可回溯的，作者随时可以对照原文章节，看看 AI 是怎么转换的，从而做针对性调整。