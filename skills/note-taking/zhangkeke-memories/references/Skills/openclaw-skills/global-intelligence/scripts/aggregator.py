#!/usr/bin/env python3
"""
global-intelligence / scripts / aggregator.py
信息聚合器 — Hermes 多源搜索 + 全文抓取版

功能：
  1. 中英文双语关键词扩展
  2. 多轮搜索策略（不同角度）
  3. 全文抓取指引（web_extract）
  4. 国内外源平衡

适配说明：Hermes 版本，使用 web_search + web_extract
"""

import json
import os
import re
import sys
from datetime import datetime
from typing import List, Dict, Any, Optional


# ── 搜索策略配置 ─────────────────────────────────────────────

# 中英文关键词映射（提高国际源命中率）
BILINGUAL_MAP = {
    "中美": ["US-China", "Sino-American"],
    "台海": ["Taiwan Strait", "cross-strait"],
    "俄乌": ["Russia-Ukraine", "Russo-Ukrainian"],
    "中东": ["Middle East", "Mideast"],
    "巴以": ["Israel-Palestine", "Israeli-Palestinian"],
    "朝鲜": ["North Korea", "DPRK"],
    "伊朗": ["Iran"],
    "日本": ["Japan"],
    "欧盟": ["EU", "European Union"],
    "北约": ["NATO"],
    "经济": ["economy", "economic"],
    "贸易": ["trade", "tariff"],
    "军事": ["military", "defense"],
    "科技": ["technology", "tech"],
    "能源": ["energy", "oil"],
    "供应链": ["supply chain"],
    "制裁": ["sanctions"],
    "外交": ["diplomacy", "diplomatic"],
    "冲突": ["conflict", "crisis"],
    "峰会": ["summit"],
    "谈判": ["negotiation", "talks"],
}

# 搜索角度（每轮不同视角）
SEARCH_PERSPECTIVES = [
    {"name": "最新动态", "suffix": "最新消息 今日"},
    {"name": "深度分析", "suffix": "分析 解读 观点"},
    {"name": "国际视角", "suffix": "英文", "lang": "en"},
    {"name": "专家评论", "suffix": "专家 学者 评论"},
    {"name": "数据事实", "suffix": "数据 统计 报告"},
]


# ── 关键词扩展 ─────────────────────────────────────────────

def expand_keywords(topic: str, max_keywords: int = 8) -> Dict[str, List[str]]:
    """
    从主题扩展中英文关键词
    
    返回：
    {
        "zh": ["中文关键词1", "中文关键词2", ...],
        "en": ["English keyword 1", "English keyword 2", ...]
    }
    """
    zh_keywords = [topic]
    en_keywords = []
    
    # 提取主题中的关键词
    zh_words = re.findall(r'[\u4e00-\u9fff]{2,6}', topic)
    
    # 查找中英文映射
    for word in zh_words:
        if word in BILINGUAL_MAP:
            en_keywords.extend(BILINGUAL_MAP[word])
    
    # 如果没有找到映射，用通用翻译提示
    if not en_keywords:
        en_keywords = [f"{topic} latest news"]
    
    # 去重
    zh_keywords = list(dict.fromkeys(zh_keywords))[:max_keywords//2]
    en_keywords = list(dict.fromkeys(en_keywords))[:max_keywords//2]
    
    return {
        "zh": zh_keywords,
        "en": en_keywords
    }


# ── 搜索策略生成 ─────────────────────────────────────────────

def generate_search_plan(topic: str) -> Dict[str, Any]:
    """
    生成完整搜索计划
    
    返回：
    {
        "topic": "原始主题",
        "rounds": [
            {
                "round": 1,
                "perspective": "最新动态",
                "queries": [
                    {"keyword": "中美局势最新消息 今日", "lang": "zh"},
                    {"keyword": "US-China latest news today", "lang": "en"}
                ]
            },
            ...
        ],
        "extract_urls": ["需要抓取全文的URL数量"],
        "total_searches": "总搜索次数"
    }
    """
    keywords = expand_keywords(topic)
    
    rounds = []
    search_count = 0
    
    # 为每个视角生成搜索轮次
    for i, perspective in enumerate(SEARCH_PERSPECTIVES[:3], 1):  # 取前3个视角
        queries = []
        
        # 中文搜索
        for zh_kw in keywords["zh"][:2]:
            query = f"{zh_kw} {perspective['suffix']}"
            queries.append({"keyword": query, "lang": "zh"})
            search_count += 1
        
        # 英文搜索（国际视角）
        if perspective.get("lang") == "en" or i <= 2:  # 前2轮都搜英文
            for en_kw in keywords["en"][:2]:
                queries.append({"keyword": en_kw, "lang": "en"})
                search_count += 1
        
        rounds.append({
            "round": i,
            "perspective": perspective["name"],
            "queries": queries
        })
    
    return {
        "topic": topic,
        "keywords": keywords,
        "rounds": rounds,
        "extract_count": 5,  # 建议抓取5篇全文
        "total_searches": search_count,
        "instructions": {
            "step1": "使用 web_search 执行以上每轮搜索",
            "step2": "从结果中筛选最相关的文章",
            "step3": "使用 web_extract 抓取前5篇高质量文章全文",
            "step4": "汇总分析，注意平衡国内外视角"
        }
    }


# ── 结果汇总模板 ─────────────────────────────────────────────

def generate_summary_template(topic: str) -> str:
    """生成结果汇总模板"""
    return f"""
## 情报汇总模板

### 主题：{topic}

### 一、搜索覆盖度
- 中文源：X 条（国内媒体/智库/专家）
- 英文源：X 条（国际媒体/智库/专家）
- 全文抓取：X 篇

### 二、关键发现（按重要性排序）

#### 🔴 高重要性
1. [发现1] — 来源：[中文/英文]，[媒体名]
2. [发现2] — 来源：...

#### 🟡 中重要性
1. ...

#### 🟢 低重要性
1. ...

### 三、国内外视角对比

| 维度 | 国内视角 | 国际视角 |
|------|---------|---------|
| 观点1 | ... | ... |
| 观点2 | ... | ... |

### 四、信息来源清单

| # | 标题 | 来源 | 语言 | 重要性 |
|---|------|------|------|--------|
| 1 | ... | ... | 中/英 | 高/中/低 |

### 五、深度分析（基于全文）

[基于抓取的全文进行深度分析]

### 六、数据与事实

[从全文中提取的关键数据和事实]
"""


# ── 主接口 ─────────────────────────────────────────────────

def get_search_plan(topic: str) -> str:
    """获取搜索计划（JSON格式，供agent使用）"""
    plan = generate_search_plan(topic)
    return json.dumps(plan, ensure_ascii=False, indent=2)


def get_summary_template(topic: str) -> str:
    """获取汇总模板"""
    return generate_summary_template(topic)


# ── CLI ────────────────────────────────────────────────────

def main():
    if len(sys.argv) < 2:
        print("用法: python3 aggregator.py <主题>")
        print("示例: python3 aggregator.py 中美局势")
        sys.exit(1)
    
    topic = sys.argv[1]
    command = sys.argv[2] if len(sys.argv) > 2 else "plan"
    
    if command == "template":
        print(get_summary_template(topic))
    else:
        print(get_search_plan(topic))


if __name__ == '__main__':
    main()
