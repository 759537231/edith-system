#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
剧本解析器 - 修复版
支持【异口同声】格式：一行多个角色说同一句话
"""

import re
from pathlib import Path

def parse_script(file_path):
    """解析剧本文件"""
    from docx import Document
    
    doc = Document(file_path)
    
    # 角色定义：【CV名】【角色名】【性别】【描述】【台词数】
    role_pattern = re.compile(r'【(.+?)】【(.+?)】【(.+?)】【(.+?)】【(\d+)】')
    
    # 中文引号
    LEFT_QUOTE = '\u201C'   # "
    RIGHT_QUOTE = '\u201D'  # "
    
    # 角色匹配：【角色名-CV名】
    role_cv_pattern = re.compile(r'【([^【】]+?)-([^【】]+?)】')
    
    roles = {}
    dialogues = []
    
    for para in doc.paragraphs:
        text = para.text
        if not text or len(text) < 5:
            continue
        
        # 提取角色定义
        m = role_pattern.match(text.strip())
        if m:
            cv, role, gender, desc, count = m.groups()
            roles[role] = {'cv': cv, 'gender': gender}
            continue
        
        # 提取台词（支持一行多个角色）
        # 找到所有【角色-CV】的位置
        matches = list(role_cv_pattern.finditer(text))
        
        for i, match in enumerate(matches):
            role, cv = match.groups()
            start_pos = match.end()  # 【】之后的位置
            
            # 找这句台词的结束位置
            # 如果有下一个【角色-CV】，则到那里结束；否则到行尾
            if i + 1 < len(matches):
                end_pos = matches[i + 1].start()
                chunk = text[start_pos:end_pos]
            else:
                chunk = text[start_pos:]
            
            # 在 chunk 里找引号内的台词
            q1 = chunk.find(LEFT_QUOTE)
            q2 = chunk.rfind(RIGHT_QUOTE)
            
            if q1 >= 0 and q2 > q1:
                line = chunk[q1+1:q2]
                dialogues.append({'role': role, 'cv': cv, 'line': line})
    
    return roles, dialogues


if __name__ == '__main__':
    import sys
    if len(sys.argv) < 2:
        print("用法: python3 script_parser.py 剧本.docx")
        sys.exit(1)
    
    roles, dialogues = parse_script(sys.argv[1])
    
    print(f"角色: {len(roles)}")
    for role in list(roles.keys())[:5]:
        print(f"  - {role}")
    
    print(f"\n台词: {len(dialogues)}")
    
    # 统计每个角色的台词数
    from collections import Counter
    role_counts = Counter(d['role'] for d in dialogues)
    print("\n各角色台词数:")
    for role, count in role_counts.most_common(10):
        print(f"  {role}: {count}句")
