#!/usr/bin/env python3
"""
Qwen3.5-4B 思考过程过滤器
用于过滤模型输出中的思考步骤，提取实际答案
"""

import re
from typing import Optional

def filter_thinking(text: str) -> str:
    """
    过滤思考过程，保留实际答案
    
    支持的格式：
    1. <think>...</think> 标签
    2. "Thinking Process:" 行
    3. 编号思考步骤（如 "1. **Analyze:**"）
    4. Draft 格式（如 "*Draft 1:* 中文答案"）
    
    Args:
        text: 原始模型输出
        
    Returns:
        过滤后的实际答案
    """
    # 移除 <think>...</think> 块
    text = re.sub(r'<think>.*?</think>', '', text, flags=re.DOTALL)
    text = re.sub(r'<think>.*$', '', text, flags=re.DOTALL)
    
    # 移除 "Thinking Process:" 行
    text = re.sub(r'^Thinking Process:\s*\n?', '', text, flags=re.MULTILINE)
    
    # 分割成行
    lines = text.split('\n')
    
    # 策略1：找到 'Drafting' 或 'Draft' 部分，提取中文答案
    drafting_start = -1
    for i, line in enumerate(lines):
        if 'Drafting' in line or 'Draft' in line:
            drafting_start = i
            break
    
    if drafting_start >= 0:
        last_draft = ''
        for i in range(drafting_start, len(lines)):
            line = lines[i]
            if '*Draft' in line or '*   *Draft' in line or 'Draft' in line:
                # 提取中文部分
                match = re.search(r'[\u4e00-\u9fff].*?(?=\s*\(|$)', line)
                if match:
                    last_draft = match.group(0).strip()
        
        if last_draft:
            return last_draft
    
    # 策略2：找到 'Output:' 行
    for line in lines:
        if line.strip().startswith('Output:'):
            return line.strip()[7:].strip()
    
    # 策略3：找到 'Answer:' 行
    for line in lines:
        if line.strip().startswith('Answer:'):
            return line.strip()[7:].strip()
    
    # 策略4：找到 'Final Choice:' 行
    for line in lines:
        if 'Final Choice:' in line:
            # 提取中文部分
            match = re.search(r'[\u4e00-\u9fff].*?(?=\s*\(|$)', line)
            if match:
                return match.group(0).strip()
    
    # 策略5：找到最后一行非空行（长度 > 5）
    for line in reversed(lines):
        if line.strip() and len(line.strip()) > 5:
            # 移除英文注释
            cleaned = re.sub(r'\(.*?\)', '', line.strip())
            cleaned = re.sub(r'\*.*?\*', '', cleaned)
            if cleaned.strip():
                return cleaned.strip()
    
    return text.strip()


def filter_thinking_simple(text: str) -> str:
    """
    简化版过滤器，只处理最常见的格式
    
    Args:
        text: 原始模型输出
        
    Returns:
        过滤后的实际答案
    """
    # 移除 <think>...</think> 块
    text = re.sub(r'<think>.*?</think>', '', text, flags=re.DOTALL)
    text = re.sub(r'<think>.*$', '', text, flags=re.DOTALL)
    
    # 移除 "Thinking Process:" 行
    text = re.sub(r'^Thinking Process:\s*\n?', '', text, flags=re.MULTILINE)
    
    # 分割成行
    lines = text.split('\n')
    
    # 找到 'Drafting' 或 'Draft' 部分
    drafting_start = -1
    for i, line in enumerate(lines):
        if 'Drafting' in line or 'Draft' in line:
            drafting_start = i
            break
    
    if drafting_start >= 0:
        # 找到最后一个 Draft
        last_draft = ''
        for i in range(drafting_start, len(lines)):
            line = lines[i]
            if '*Draft' in line or '*   *Draft' in line:
                # 提取中文部分
                match = re.search(r'[\u4e00-\u9fff].*?(?=\s*\(|$)', line)
                if match:
                    last_draft = match.group(0).strip()
        
        if last_draft:
            return last_draft
    
    # 如果没有找到 Drafting 部分，返回最后一行
    for line in reversed(lines):
        if line.strip() and len(line.strip()) > 5:
            # 移除英文注释
            cleaned = re.sub(r'\(.*?\)', '', line.strip())
            cleaned = re.sub(r'\*.*?\*', '', cleaned)
            if cleaned.strip():
                return cleaned.strip()
    
    return text.strip()


# 测试函数
def test_filter():
    """测试过滤函数"""
    test_cases = [
        {
            "input": """Thinking Process:

1.  **Analyze the Request:**
    *   Topic: What is Machine Learning (ML)?
    *   Constraint: Explain in one sentence.

2.  **Define Machine Learning:**
    *   Core concept: Computing systems learning from data.

3.  **Drafting:**
    *   *Draft 1:* 机器学习是一种让计算机从数据中学习规律的技术。
    *   *Draft 2:* 机器学习是让计算机通过数据自动学习规律，从而完成特定任务的技术。""",
            "expected": "机器学习是让计算机通过数据自动学习规律，从而完成特定任务的技术。"
        },
        {
            "input": """1.  **Analyze the Request:**
    *   Topic: What is machine learning (ML)?
    *   Constraint: Explain in one sentence.

2.  **Drafting:**
    *   *Draft 1:* 机器学习是一种让计算机从数据中学习规律的技术。

机器学习是让计算机通过数据自动学习规律，从而完成特定任务或做出预测的技术。""",
            "expected": "机器学习是让计算机通过数据自动学习规律，从而完成特定任务或做出预测的技术。"
        }
    ]
    
    print("🧪 测试思考过程过滤器")
    print("=" * 60)
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n📝 测试 {i}:")
        print(f"输入: {test_case['input'][:100]}...")
        
        result = filter_thinking(test_case['input'])
        print(f"输出: {result}")
        
        if result == test_case['expected']:
            print("✅ 通过")
        else:
            print(f"❌ 失败")
            print(f"期望: {test_case['expected']}")


if __name__ == "__main__":
    test_filter()
