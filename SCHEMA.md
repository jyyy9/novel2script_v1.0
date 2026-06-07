# Novel2Script YAML Schema

## 剧本数据结构

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
