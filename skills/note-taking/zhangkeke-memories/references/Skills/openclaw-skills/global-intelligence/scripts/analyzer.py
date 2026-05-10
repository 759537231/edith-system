#!/usr/bin/env python3
"""
Global Intelligence — 8维专家 prompt 构建器 + 结果解析器

实际推理：AI agent 通过 delegate_task 调用 QClaw 云端模型
此脚本：提供 persona 加载 + prompt 模板 + 解析函数
"""

import json
import os
import re
from dataclasses import dataclass, field
from typing import List, Dict


# ── 数据模型 ────────────────────────────────────────────

@dataclass
class AnalysisResult:
    dimension: str
    expert: str
    emoji: str
    core_judgment: str
    trend: str           # ↑恶化 / ↓好转 / →平稳 / ↗️升温 / ↘️降温
    confidence: int      # 0-100
    key_factors: List[str] = field(default_factory=list)
    implications: List[str] = field(default_factory=list)
    raw_analysis: str = ""
    used_llm: bool = False


# ── Persona 加载 ─────────────────────────────────────────

def load_personas(skill_path: str) -> Dict:
    personas = {}
    pdir = os.path.join(skill_path, "personas")
    if not os.path.isdir(pdir):
        return personas
    for fname in os.listdir(pdir):
        if not fname.endswith(".json"):
            continue
        with open(os.path.join(pdir, fname), encoding="utf-8") as f:
            raw = json.load(f)
        name = raw.get("name", fname[:-5])
        personas[name] = _normalize(raw)
    return personas


def _normalize(raw: Dict) -> Dict:
    out = {
        "name": raw.get("name", ""),
        "display_name": raw.get("display_name", raw.get("title", "")),
        "emoji": raw.get("emoji", "?"),
        "title": raw.get("title", ""),
        "focus": raw.get("focus", ""),
    }
    nested = raw.get("persona", {})
    identity = nested.get("identity", {})
    bg = nested.get("origin") or identity.get("origin") or identity.get("career")
    if not bg:
        bg = raw.get("bio") or raw.get("description", "")
    out["background"] = bg

    meth = nested.get("analysis_methodology", {})
    if meth:
        steps = [v for k, v in meth.items() if k.startswith("step_")]
        out["thinking_framework"] = " | ".join(steps) if steps else nested.get("thinking_framework", "")
    else:
        out["thinking_framework"] = nested.get("thinking_framework", "")

    exp_obj = nested.get("expertise", {})
    if isinstance(exp_obj, dict):
        all_exp = list(exp_obj.get("primary", [])) + list(exp_obj.get("secondary", [])) + list(exp_obj.get("frameworks", []))
        out["expertise"] = ", ".join(str(e) for e in all_exp[:8])
    elif isinstance(exp_obj, list):
        out["expertise"] = ", ".join(str(e) for e in exp_obj[:8])
    else:
        out["expertise"] = str(exp_obj) if exp_obj else ""

    pers = nested.get("personality", {})
    out["language_style"] = pers.get("沟通风格", pers.get("communication_style", ""))
    if not out.get("background"):
        out["background"] = raw.get("bio", raw.get("description", ""))
    if not out.get("expertise"):
        er = raw.get("expertise", [])
        if isinstance(er, list):
            out["expertise"] = ", ".join(er)
    return out


# ── Prompt 构建器 ───────────────────────────────────────

def build_expert_prompt(persona: Dict, intelligence: List[Dict], topic: str) -> str:
    if intelligence:
        lines = []
        for i, item in enumerate(intelligence, 1):
            t = item.get("title", "")
            s = item.get("snippet", "")
            src = item.get("source", "")
            lines.append(f"[{i}] {t}（来源:{src}）: {s[:180]}")
        intel_text = "\n".join(lines)
    else:
        intel_text = "（暂无直接相关情报，请基于通用知识推断）"

    expertise = persona.get("expertise", persona.get("focus", ""))[:100]
    background = persona.get("background", "")[:300]
    framework = persona.get("thinking_framework", "")[:250]
    style = persona.get("language_style", "")[:80]
    focus = persona.get("focus", "")
    display = persona.get("display_name", persona.get("name", "?"))

    return (
        f"你是{display}，代号{persona['name']}，擅长{expertise}。\n\n"
        f"背景：{background}\n"
        f"分析方法：{framework}\n"
        f"说话风格：{style}\n"
        f"核心关注：{focus}\n\n"
        f"---\n"
        f"当前任务：分析「{topic}」\n\n"
        f"相关情报（共{len(intelligence)}条）：\n"
        f"{intel_text}\n\n"
        f"---\n"
        f"请用中文回答。格式（严格按此格式）：\n"
        f"核心判断：[一句话，50字以内]\n"
        f"趋势：[↑恶化 / ↓好转 / →平稳 / ↗️升温 / ↘️降温]\n"
        f"置信度：[0-100整数]\n"
        f"关键因素：[2-4个，用分号分隔]\n"
        f"启示：[1-2条]\n"
        f"分析：[100-200字，展开推理过程]"
    )


# ── 结果解析器 ───────────────────────────────────────────

def parse_llm_response(text: str, persona: Dict) -> Dict:
    result = {
        "core_judgment": "",
        "trend": "→平稳",
        "confidence": 50,
        "key_factors": [],
        "implications": [],
        "raw_analysis": text,
    }

    # 核心判断
    for pat in [r"核心判断[：:]\s*(.+?)(?=\n\[|\Z)", r"\[核心判断\]\s*(.+?)(?=\n\[|\Z)"]:
        m = re.search(pat, text, re.DOTALL)
        if m:
            val = m.group(1).strip()
            if val and "[" not in val[:5]:
                result["core_judgment"] = re.sub(r"^[🎯🔍💡📊]\s*", "", val)
                break
    if not result["core_judgment"]:
        result["core_judgment"] = persona.get("focus", "需持续关注")

    # 趋势（全文扫描）
    trend_map = {
        "↑恶化": "↑恶化",
        "↓好转": "↓好转",
        "→平稳": "→平稳",
        "↗️升温": "↗️升温",
        "↘️降温": "↘️降温",
    }
    for raw_t, trend in trend_map.items():
        if raw_t in text:
            result["trend"] = trend
            break

    # 置信度
    m = re.search(r"置信度[：:]\s*[:：]?\s*(\d{1,3})", text)
    if m:
        result["confidence"] = min(100, max(0, int(m.group(1))))

    # 关键因素
    m = re.search(r"关键因素[：:]\s*(.+?)(?=\n\[启示|\n分析|\[置信度\]|\[|\Z)", text, re.DOTALL)
    if m:
        raw = m.group(1).strip()
        items = [f.strip() for f in re.split(r"[,，、;；\n]", raw) if len(f.strip()) > 3]
        result["key_factors"] = items[:4]

    # 启示
    m = re.search(r"启示[：:]\s*(.+?)(?=\n\[|\Z)", text, re.DOTALL)
    if m:
        raw = m.group(1).strip()
        items = [i.strip() for i in re.split(r"[,，、;；\n]", raw) if len(i.strip()) > 3]
        result["implications"] = items[:2]

    return result


# ── 分析器 ─────────────────────────────────────────────

class ExpertAnalyzer:
    DIM_KEYWORDS = {
        "atlas":      ["地缘", "外交", "联盟", "边界", "领土", "军事基地", "势力范围", "峰会", "北约", "G7", "欧盟", "大国"],
        "plutus":     ["经济", "金融", "GDP", "通胀", "汇率", "产业链", "贸易", "制裁", "关税", "货币", "债务"],
        "sentinel":   ["安全", "军事", "冲突", "演习", "武器", "恐怖主义", "战争", "部队", "舰队", "导弹", "核"],
        "tesla":      ["科技", "AI", "芯片", "半导体", "技术封锁", "专利", "航天", "量子", "大模型", "研发"],
        "prometheus": ["能源", "石油", "天然气", "新能源", "OPEC", "稀土", "电力", "核能", "光伏", "储能"],
        "echo":       ["舆情", "舆论", "社媒", "Twitter", "X", "热搜", "情绪", "认知", "宣传", "信息战", "假新闻"],
        "chronos":    ["历史", "类比", "周期", "冷战", "危机", "教训", "当年", "曾经", "往事", "前车之鉴"],
        "dragon":     ["中国", "对华", "一带一路", "RCEP", "中美", "台海", "南海", "习近平", "中国外长", "中国领导"],
        "mariner":    ["海运", "航运", "运价", "港口", "集装箱", "SCFI", "船", "航线", "供应链", "物流", "货运"],
        "admiral":    ["海峡", "航道", "海军", "封锁", "海盗", "水雷", "航母", "军舰", "护航", "咽喉要道", "马六甲", "苏伊士", "亚丁湾"],
        "politico":   ["政治", "选举", "领导人", "执政", "国内压力", "停火", "谈判", "民意", "右翼", "保守派", "改革派", "联盟稳定", "政治危机"],
    }

    def __init__(self, skill_path: str):
        self.skill_path = skill_path
        self.personas = load_personas(skill_path)

    def analyze(self, intelligence: List[Dict], topic: str) -> List[AnalysisResult]:
        """构建所有专家的 prompt（供 delegate_task 使用）"""
        results = []
        for dim, keywords in self.DIM_KEYWORDS.items():
            persona = self.personas.get(dim)
            if not persona:
                continue
            relevant = [
                i for i in intelligence
                if any(kw in (i.get("title", "") + i.get("snippet", ""))
                   for kw in keywords)
            ][:6]
            prompt = build_expert_prompt(persona, relevant, topic)
            results.append(AnalysisResult(
                dimension=dim,
                expert=persona["display_name"],
                emoji=persona["emoji"],
                core_judgment="（需调用LLM）",
                trend="→平稳",
                confidence=50,
                key_factors=[],
                implications=[],
                raw_analysis=prompt,
                used_llm=False,
            ))
        return results

    def parse_response(self, dim: str, raw_text: str) -> AnalysisResult:
        persona = self.personas.get(dim, {})
        parsed = parse_llm_response(raw_text, persona)
        return AnalysisResult(
            dimension=dim,
            expert=persona.get("display_name", dim),
            emoji=persona.get("emoji", "?"),
            core_judgment=parsed["core_judgment"],
            trend=parsed["trend"],
            confidence=parsed["confidence"],
            key_factors=parsed["key_factors"],
            implications=parsed["implications"],
            raw_analysis=raw_text,
            used_llm=True,
        )


# ── 格式化 ────────────────────────────────────────────

def format_analysis_table(results: List[AnalysisResult]) -> str:
    trend_emoji = {
        "↑恶化": "🔴", "↓好转": "🟢", "→平稳": "⚪",
        "↗️升温": "🟠", "↘️降温": "🔵",
    }
    rows = ["| 维度 | 专家 | 核心判断 | 趋势 | 置信度 | LLM |",
            "|------|------|---------|------|--------|-----|"]
    for r in results:
        te = trend_emoji.get(r.trend, "⚪")
        llm = "🧠" if r.used_llm else "📋"
        j = r.core_judgment[:38] + ("..." if len(r.core_judgment) > 38 else "")
        rows.append(
            f"| {r.emoji} {r.dimension} | {r.expert} | "
            f"{j} | {te} {r.trend} | {r.confidence}% | {llm} |"
        )
    return "\n".join(rows)


# ── CLI ────────────────────────────────────────────────

if __name__ == "__main__":
    skill_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    topic = "中美AI竞争"
    test_intel = [
        {"title": "斯坦福HAI报告：中美AI差距缩小", "snippet": "AI指数全面对比", "source": "Stanford HAI"},
        {"title": "美国扩大芯片出口管制", "snippet": "H20等高端芯片受限", "source": "Reuters"},
    ]
    analyzer = ExpertAnalyzer(skill_path)
    results = analyzer.analyze(test_intel, topic)
    print(f"✅ 加载 {len(analyzer.personas)} persona，生成 {len(results)} prompt：")
    for r in results:
        print(f"  {r.emoji} {r.expert}: prompt长度={len(r.raw_analysis)}字")


# ── Politico 校验 Prompt 构建器 ─────────────────────────────

def build_politico_verification_prompt(
    persona: Dict,
    intelligence: List[Dict],
    topic: str,
    expert_summaries: List[Dict]
) -> str:
    """
    构建 Politico 校验层专用 prompt。
    
    Args:
        persona: Politico 角色卡
        intelligence: 原始情报
        topic: 分析主题
        expert_summaries: 8位专家的核心结论列表
            [{"dimension": "atlas", "judgment": "...", "trend": "↑恶化", "confidence": 85}]
    
    Returns:
        Politico 校验 prompt
    """
    # 情报摘要
    if intelligence:
        intel_lines = []
        for i, item in enumerate(intelligence, 1):
            t = item.get("title", "")
            s = item.get("snippet", "")
            src = item.get("source", "")
            intel_lines.append(f"[{i}] {t}（来源:{src}）: {s[:180]}")
        intel_text = "\n".join(intel_lines)
    else:
        intel_text = "（暂无直接相关情报）"
    
    # 专家结论摘要
    summary_lines = []
    for s in expert_summaries:
        summary_lines.append(
            f"- {s.get('emoji', '?')} {s.get('dimension', '?')}（{s.get('expert', '?')}）: "
            f"{s.get('judgment', '未出结论')} | 趋势{s.get('trend', '?')} | 置信度{s.get('confidence', '?')}%"
        )
    summaries_text = "\n".join(summary_lines)
    
    display = persona.get("display_name", persona.get("name", "Politico"))
    focus = persona.get("focus", "")
    background = persona.get("background", "")[:300]
    
    return (
        f"你是{display}，代号politico，政治现实校验器。\n"
        f"你的使命不是唱反调，是压力测试——让最终预测对准真实。\n\n"
        f"背景：{background}\n"
        f"核心关注：{focus}\n\n"
        f"---\n"
        f"当前任务：校验「{topic}」分析的政治可行性\n\n"
        f"相关情报：\n{intel_text}\n\n"
        f"---\n"
        f"8位专家的核心结论：\n{summaries_text}\n\n"
        f"---\n"
        f"请按以下格式输出（严格）：\n\n"
        f"## 政治摩擦力清单\n"
        f"列出其他专家假设中忽略的政治变量（国内压力、选举周期、联盟约束、领导人风险偏好、民族情绪等），每条：\n"
        f"- 变量名：[具体描述] | 影响方向：[上修/下修/不变] | 影响幅度：[高/中/低]\n\n"
        f"## 压力测试\n"
        f"对每项高置信度（≥75%）结论进行三问：\n"
        f"1. 什么条件下这个结论会崩塌？\n"
        f"2. 触发信号是什么？\n"
        f"3. 政治意愿反转的前提是什么？\n\n"
        f"## 概率修正\n"
        f"基于政治约束，调整各项预测的概率（可上可下，关键是对准真实）：\n"
        f"- [维度] 原始概率X% → 修正后Y% | 修正依据：[一句话]\n\n"
        f"## 冲突区判定\n"
        f"当前议题是否属于冲突区？（冲突区=活跃武装冲突/停火脆弱/升级阶梯已启动）\n"
        f"如果是冲突区：短期预测基线为 现状延续40%+升级30%+缓和30%（不默认乐观）\n"
        f"判定：[是/否] | 依据：[一句话]\n\n"
        f"## 政治触发信号\n"
        f"列出2-3个会改变政治成本计算的关键事件，每个：\n"
        f"- 事件：[描述] | 概率：[高/中/低] | 影响方向：[升级/降级/转向]\n"
    )
