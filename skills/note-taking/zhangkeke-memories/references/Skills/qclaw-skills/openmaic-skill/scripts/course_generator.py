#!/usr/bin/env python3
"""
OpenMAIC Skill - 课程生成器
基于清华OpenMAIC项目的核心逻辑，Python版本实现
"""

import json
import re
from pathlib import Path
from typing import Optional, Dict, List, Any
from dataclasses import dataclass, field


@dataclass
class CourseConfig:
    """课程配置"""
    language: str = "zh-CN"
    duration_minutes: int = 20
    target_audience: str = "general"
    style: str = "interactive"
    visual_style: str = "professional"


@dataclass
class SceneOutline:
    """场景大纲"""
    id: str
    type: str  # slide, quiz, interactive, pbl
    title: str
    description: str
    key_points: List[str] = field(default_factory=list)
    order: int = 0
    estimated_duration: int = 120


def read_prompt_template(template_name: str) -> str:
    """读取Prompt模板"""
    skill_dir = Path(__file__).parent.parent
    prompt_path = skill_dir / "prompts" / f"{template_name}.md"
    
    if prompt_path.exists():
        return prompt_path.read_text(encoding='utf-8')
    return ""


def format_outline_prompt(
    requirement: str,
    pdf_content: Optional[str] = None,
    config: Optional[CourseConfig] = None
) -> Dict[str, str]:
    """
    格式化大纲生成Prompt
    
    返回: {"system": "系统提示", "user": "用户提示"}
    """
    if config is None:
        config = CourseConfig()
    
    # 简化的系统提示
    system_prompt = """# 场景大纲生成器

你是专业的课程内容设计师，擅长将用户需求转化为结构化的场景大纲。

## 输出要求

必须输出JSON数组：
```json
[
  {
    "id": "scene_1",
    "type": "slide",
    "title": "场景标题",
    "description": "教学目的",
    "keyPoints": ["要点1", "要点2"],
    "order": 1
  }
]
```

场景类型：
- slide: 幻灯片
- quiz: 测验
- interactive: 交互式

## 规则

1. 必须输出有效JSON
2. 使用指定语言
3. 每2-3分钟一个场景"""

    # 用户提示
    user_prompt = f"""请根据以下需求生成课程大纲：

## 用户需求
{requirement}

## 语言
{config.language}

## 参考材料
{pdf_content[:2000] if pdf_content else '无'}

请生成JSON格式的场景大纲。"""

    return {"system": system_prompt, "user": user_prompt}


def parse_outline_response(response: str) -> List[SceneOutline]:
    """解析大纲响应"""
    # 尝试提取JSON
    try:
        # 查找JSON数组
        json_match = re.search(r'\[\s*\{.*\}\s*\]', response, re.DOTALL)
        if json_match:
            data = json.loads(json_match.group())
            scenes = []
            for i, item in enumerate(data):
                scene = SceneOutline(
                    id=item.get('id', f'scene_{i+1}'),
                    type=item.get('type', 'slide'),
                    title=item.get('title', f'场景{i+1}'),
                    description=item.get('description', ''),
                    key_points=item.get('keyPoints', item.get('key_points', [])),
                    order=item.get('order', i+1)
                )
                scenes.append(scene)
            return scenes
    except json.JSONDecodeError:
        pass
    
    # 解析失败，返回空列表
    return []


def format_slide_prompt(
    outline: SceneOutline,
    config: Optional[CourseConfig] = None
) -> Dict[str, str]:
    """格式化幻灯片内容生成Prompt"""
    
    system_prompt = """# 幻灯片内容生成器

你是教育内容设计师，生成结构清晰的幻灯片组件。

## 输出格式

```json
{
  "background": {"type": "solid", "color": "#ffffff"},
  "elements": [
    {
      "id": "text_001",
      "type": "text",
      "left": 60,
      "top": 80,
      "width": 880,
      "height": 60,
      "content": "<p>标题</p>"
    }
  ]
}
```

## 规则

- 文字简洁，每条不超过20字
- 不写演讲稿内容
- 坐标合理，不超出画布"""

    user_prompt = f"""请为以下场景生成幻灯片内容：

## 场景信息
- 标题：{outline.title}
- 描述：{outline.description}
- 要点：{', '.join(outline.key_points)}

生成JSON格式的幻灯片结构。"""

    return {"system": system_prompt, "user": user_prompt}


def generate_course(
    requirement: str,
    pdf_content: Optional[str] = None,
    config: Optional[CourseConfig] = None
) -> Dict[str, Any]:
    """
    生成课程（入口函数）
    
    Args:
        requirement: 用户需求描述
        pdf_content: PDF内容（可选）
        config: 课程配置
    
    Returns:
        {
            "outlines": [...],
            "prompts": {
                "outline": {"system": ..., "user": ...},
                "slides": [{"scene_id": ..., "system": ..., "user": ...}]
            }
        }
    """
    if config is None:
        config = CourseConfig()
    
    result = {
        "outlines": [],
        "prompts": {
            "outline": format_outline_prompt(requirement, pdf_content, config),
            "slides": []
        }
    }
    
    # 注意：实际的大纲生成需要调用AI模型
    # 这里只返回Prompt，由调用者执行
    
    return result


if __name__ == "__main__":
    # 测试
    requirement = "教我量子物理的基本概念"
    result = generate_course(requirement)
    
    print("=== 大纲生成Prompt ===")
    print("System:", result["prompts"]["outline"]["system"][:100], "...")
    print("User:", result["prompts"]["outline"]["user"][:100], "...")
