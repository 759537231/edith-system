#!/usr/bin/env python3
"""
global-intelligence / main.py
主入口 — 协调8维专家+犹太智囊，生成完整分析报告
"""

import sys
import os
import json
import argparse
from typing import Optional

# 确保可以导入scripts模块
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'scripts'))

from analyzer import ExpertAnalyzer, format_analysis_table
from jewish_council import JewishCouncil, format_jewish_council
from reporter import ReportGenerator
from aggregator import fetch_intelligence
from vector_store import store_report, search_similar, stats as vector_stats


class GlobalIntelligence:
    """全球局势分析系统主类"""
    
    def __init__(self):
        self.skill_path = os.path.dirname(os.path.abspath(__file__))
        self.analyzer = ExpertAnalyzer(self.skill_path)
        self.council = JewishCouncil()
        self.reporter = ReportGenerator(self.skill_path)
        self._vector_store_enabled = True  # 可通过环境变量关闭
    
    def analyze(
        self, 
        topic: str, 
        intelligence: Optional[list] = None,
        priority: str = "中等",
        keywords: Optional[list] = None
    ) -> str:
        """
        执行完整分析流程
        
        Args:
            topic: 分析主题 (如 "中美AI竞争", "俄乌局势")
            intelligence: 预抓取的情报列表，None则自动抓取
            priority: 报告优先级 (高/中/低)
            keywords: 额外搜索关键词
            
        Returns:
            生成的报告文件路径
        """
        print(f"🌍 Global Intelligence 启动")
        print(f"   主题: {topic}")
        print(f"   时间: {self._now()}")
        print()
        
        # Step 1: 情报获取
        if intelligence is None:
            print("📡 正在抓取情报...")
            intelligence = fetch_intelligence(topic, keywords)
            print(f"   获取 {len(intelligence)} 条情报")
        else:
            print(f"📡 使用预置情报: {len(intelligence)} 条")
        
        if not intelligence:
            print("⚠️ 未能获取情报，使用默认数据")
            intelligence = [{"title": f"{topic}态势分析", "snippet": "暂无实时数据", "source": "系统"}]
        
        print()
        
        # Step 2: 8维专家分析
        print("🧠 启动8维专家并行分析...")
        analysis_results = self.analyzer.analyze(intelligence, topic)
        print(f"   完成 {len(analysis_results)} 个维度分析")
        print()
        
        # Step 3: 犹太智囊推演
        print("🎩 启动双犹太智囊推演...")
        council_output = self.council.deliberate(analysis_results, topic)
        print(f"   风险等级: {council_output.solomon.warning_level}")
        print(f"   套利空间: {len(council_output.rothschild.arbitrage_gaps)} 个")
        print()
        
        # Step 4: 生成报告
        print("📄 生成分析报告...")
        report_path = self.reporter.generate(
            topic=topic,
            intelligence=intelligence,
            analysis_results=analysis_results,
            council_output=council_output,
            priority=priority
        )
        print(f"   ✅ 报告已保存: {report_path}")
        
        # Step 5: 向量存储（长期情报积累）
        self._store_to_vector(topic, intelligence, analysis_results, council_output)
        
        return report_path
    
    def quick_scan(self, topic: str, keywords: list = None) -> dict:
        """
        快速扫描 — 返回结构化结果
        
        Args:
            topic: 分析主题
            keywords: 额外关键词
            
        Returns:
            结构化分析结果字典
        """
        intelligence = fetch_intelligence(topic, keywords)
        analysis_results = self.analyzer.analyze(intelligence, topic)
        council_output = self.council.deliberate(analysis_results, topic)
        
        return {
            "topic": topic,
            "timestamp": self._now(),
            "intelligence_count": len(intelligence),
            "dimensions": [
                {
                    "name": r.dimension,
                    "expert": r.expert,
                    "emoji": r.emoji,
                    "judgment": r.core_judgment,
                    "trend": r.trend,
                    "confidence": r.confidence
                }
                for r in analysis_results
            ],
            "risk_level": council_output.solomon.warning_level,
            "opportunities": len(council_output.rothschild.arbitrage_gaps),
            "synthesis": council_output.synthesis
        }
    
    def _now(self) -> str:
        """当前时间字符串"""
        from datetime import datetime
        return datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    def _store_to_vector(self, topic, intelligence, analysis_results, council_output):
        """将分析结果存入向量数据库，供后续语义检索"""
        if not self._vector_store_enabled:
            return
        
        try:
            # 构造摘要文本
            dim_texts = [
                f"{r.emoji}{r.expert}: {r.core_judgment}"
                for r in analysis_results
                if r.confidence >= 50
            ]
            summary = (
                f"主题: {topic}\n"
                f"风险等级: {council_output.solomon.warning_level}\n"
                f"核心判断: {council_output.synthesis[:300]}\n"
                f"各维度分析: {' | '.join(dim_texts[:4])}"
            )
            
            # 判断主题分类
            topic_keywords = {
                '科技': ['AI', '芯片', '半导体', '技术', '算力', '大模型', '量子'],
                '地缘': ['战争', '军事', '冲突', '联盟', '岛屿', '海峡', '俄乌', '中东', '台海'],
                '经济': ['经济', '金融', '资本', '制裁', '债务', '产业链', '贸易'],
                '能源': ['能源', '石油', '天然气', '稀土', '矿产', '新能源'],
            }
            detected_topic = '综合'
            for cat, kw_list in topic_keywords.items():
                if any(kw in topic for kw in kw_list):
                    detected_topic = cat
                    break
            
            doc_id = store_report(
                title=topic,
                topic=detected_topic,
                priority='高',
                summary=summary,
                embedding_text=summary  # 用摘要做嵌入
            )
            print(f"   🧠 情报入库: [{doc_id}] topic={detected_topic}")
            
            # 顺便检索一下相关历史情报
            similar = search_similar(topic, topk=3)
            if similar:
                print(f"   📚 历史相关情报: {len(similar)} 条")
                for r in similar[:2]:
                    print(f"      - [{r['score']:.3f}] {r['title']}")
                    
        except Exception as e:
            print(f"   ⚠️  向量存储失败（不影响主流程）: {e}")


def main():
    """CLI入口"""
    parser = argparse.ArgumentParser(description='Global Intelligence 全球局势分析')
    parser.add_argument('topic', help='分析主题 (如 "中美AI竞争")')
    parser.add_argument('--priority', '-p', default='中等', 
                       choices=['高', '中', '低'],
                       help='报告优先级')
    parser.add_argument('--quick', '-q', action='store_true',
                       help='快速扫描模式，只返回结构化结果')
    parser.add_argument('--keywords', '-k', nargs='+',
                       help='额外搜索关键词')
    parser.add_argument('--output', '-o', help='输出报告路径')
    
    args = parser.parse_args()
    
    gi = GlobalIntelligence()
    
    if args.quick:
        result = gi.quick_scan(args.topic, args.keywords)
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        report_path = gi.analyze(
            args.topic, 
            priority=args.priority,
            keywords=args.keywords
        )
        
        # 显示报告内容
        with open(report_path) as f:
            content = f.read()
            print("\n" + "=" * 70)
            print(content)


if __name__ == '__main__':
    main()
