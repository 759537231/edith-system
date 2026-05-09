#!/usr/bin/env python3
"""
伊迪丝工具函数 — 知识库自动注入
自动读取部门知识库，返回摘要用于delegate_task的context
"""
import os
import re
from pathlib import Path

SKILLS_DIR = Path.home() / '.hermes' / 'skills' / 'departments'

# 部门名到目录名的映射
DEPT_MAP = {
    '美术设计': 'meishusheji',
    'meishusheji': 'meishusheji',
    '交互设计': 'jiaohusheji',
    'jiaohusheji': 'jiaohusheji',
    '工部': 'coding-assistant',
    'coding-assistant': 'coding-assistant',
    '户部': 'hubu',
    'hubu': 'hubu',
    '市场运营部': 'shichangyunyingbu',
    'shichangyunyingbu': 'shichangyunyingbu',
    '通商部': 'tongshangbu',
    'tongshangbu': 'tongshangbu',
    '刑部': 'xingbu',
    'xingbu': 'xingbu',
    '门下省': 'menxiasheng',
    'menxiasheng': 'menxiasheng',
    '视频创作部': 'shipinchuangzuobu',
    'shipinchuangzuobu': 'shipinchuangzuobu',
}

def extract_summary(content: str, max_lines: int = 50) -> str:
    """提取Markdown文件的核心内容摘要"""
    lines = content.split('\n')
    summary_lines = []
    in_table = False
    table_count = 0
    
    for line in lines:
        # 保留标题
        if line.startswith('#'):
            summary_lines.append(line)
            in_table = False
            continue
        
        # 保留表格（最多3个）
        if '|' in line and line.strip().startswith('|'):
            if not in_table:
                in_table = True
                table_count += 1
            if table_count <= 3:
                summary_lines.append(line)
            continue
        else:
            in_table = False
        
        # 保留列表项
        if line.strip().startswith(('-', '*', '1.', '2.', '3.')):
            summary_lines.append(line)
            continue
        
        # 保留代码块标记
        if line.strip().startswith('```'):
            summary_lines.append(line)
            continue
        
        # 跳过空行
        if line.strip():
            # 保留有强调标记的行
            if '**' in line or '定义' in line or '原则' in line:
                summary_lines.append(line)
    
    # 截断
    if len(summary_lines) > max_lines:
        summary_lines = summary_lines[:max_lines]
        summary_lines.append('... (更多内容见完整文件)')
    
    return '\n'.join(summary_lines)


def auto_inject_knowledge(dept_name: str) -> str:
    """
    自动读取部门知识库，返回摘要
    
    Args:
        dept_name: 部门名（中文或英文）
    
    Returns:
        格式化的知识库摘要，可直接注入delegate_task的context
    """
    # 映射部门目录
    dept_dir_name = DEPT_MAP.get(dept_name, dept_name)
    dept_path = SKILLS_DIR / dept_dir_name
    
    if not dept_path.exists():
        return f"[知识库未找到: {dept_name}]"
    
    knowledge_dir = dept_path / 'knowledge'
    if not knowledge_dir.exists():
        return f"[{dept_name}暂无知识库]"
    
    # 读取所有知识文件
    knowledge_files = sorted(knowledge_dir.glob('*.md'))
    if not knowledge_files:
        return f"[{dept_name}知识库为空]"
    
    # 构建摘要
    result = f"## {dept_name}知识库摘要\n\n"
    
    for kf in knowledge_files:
        try:
            content = kf.read_text(encoding='utf-8')
            # 提取文件名作为标题
            title = kf.stem  # 如 "01-色彩理论"
            summary = extract_summary(content, max_lines=30)
            result += f"### {title}\n{summary}\n\n"
        except Exception as e:
            result += f"### {kf.stem}\n[读取失败: {e}]\n\n"
    
    return result


def build_dept_context(dept_name: str, task_description: str) -> str:
    """
    构建部门任务的完整context，包含知识库摘要
    
    Args:
        dept_name: 部门名
        task_description: 任务描述
    
    Returns:
        完整的context字符串
    """
    knowledge = auto_inject_knowledge(dept_name)
    
    context = f"""## 任务背景

{task_description}

## 参考知识

{knowledge}

## 执行要求

请基于以上知识库内容执行任务，确保输出符合专业规范。
"""
    return context


if __name__ == '__main__':
    # 测试
    print(auto_inject_knowledge('美术设计'))
