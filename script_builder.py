"""
剧本构建模块

将多个章节的 AI 转换结果合并为完整的剧本结构。
负责生成 scene_id 和 element_id，确保剧本格式统一。
"""

import copy


def build_script(original_author: str, chapters_results: list[dict]) -> dict:
    """
    将所有章节的 AI 返回结果合并为完整剧本。

    Args:
        original_author: 原小说作者名
        chapters_results: 每个元素是 convert_chapter 返回的 dict，
                         应包含 'scenes' 列表

    Returns:
        完整的剧本字典，包含：
        - metadata: {"author": original_author, "total_scenes": N}
        - scenes: 合并后的场景列表，每个场景增加 scene_id (S001, S002...)
                  每个 elements 内的元素增加 element_id (如 A001, D001...)

    Example:
        >>> chapters_results = [{"scenes": [{"heading": "...", ...}]}]
        >>> script = build_script("鲁迅", chapters_results)
        >>> print(script["metadata"]["total_scenes"])
    """
    all_scenes = []
    scene_counter = 1

    for chapter_result in chapters_results:
        if not chapter_result or not isinstance(chapter_result, dict):
            continue
        scenes = chapter_result.get("scenes", [])
        if not scenes:
            continue

        for scene in scenes:
            scene_id = f"S{scene_counter:03d}"
            scene_counter += 1

            new_scene = copy.deepcopy(scene)
            new_scene["scene_id"] = scene_id

            if "elements" in new_scene and isinstance(new_scene["elements"], list):
                elem_counter = 1
                for elem in new_scene["elements"]:
                    elem_type = elem.get("type", "action")
                    prefix = "A" if elem_type == "action" else "D"
                    elem["element_id"] = f"{prefix}{elem_counter:03d}"
                    elem_counter += 1

            all_scenes.append(new_scene)

    return {
        "metadata": {
            "author": original_author,
            "total_scenes": len(all_scenes),
        },
        "scenes": all_scenes,
    }
