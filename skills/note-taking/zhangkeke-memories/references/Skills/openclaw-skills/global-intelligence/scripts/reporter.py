#!/usr/bin/env python3
"""
global-intelligence / scripts / reporter.py
报告生成器 — 整合8维分析+犹太智囊，输出结构化报告
"""

import json
import os
from datetime import datetime
from typing import List, Dict, Any
from dataclasses import asdict

from analyzer import AnalysisResult, format_analysis_table
from jewish_council import JewishCouncilOutput, format_jewish_council


class ReportGenerator:
    """报告生成器"""
    
    def __init__(self, skill_path: str):
        self.skill_path = skill_path
        self.output_dir = os.path.join(skill_path, 'data', 'reports')
        os.makedirs(self.output_dir, exist_ok=True)
    
    def generate(
        self,
        topic: str,
        intelligence: List[Dict],
        analysis_results: List[AnalysisResult],
        council_output: JewishCouncilOutput,
        priority: str = "中等"
    ) -> str:
        """
        生成完整分析报告
        
        Args:
            topic: 分析主题
            intelligence: 原始情报
            analysis_results: 8维分析结果
            council_output: 犹太智囊输出
            priority: 优先级 (高/中/低)
            
        Returns:
            报告文件路径
        """
        
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M CST')
        report_id = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        # 生成情景预判
        scenarios = self._generate_scenarios(analysis_results, topic)
        
        # 生成行动建议
        actions = self._generate_actions(analysis_results, council_output)
        
        # 组装报告
        report = self._assemble_report(
            topic=topic,
            timestamp=timestamp,
            priority=priority,
            intelligence_summary=intelligence[:5],
            analysis_table=format_analysis_table(analysis_results),
            jewish_council=format_jewish_council(council_output),
            scenarios=scenarios,
            actions=actions
        )
        
        # ── 同主题去重：只保留最新 ─────────────────────
        safe_topic = topic.replace(' ', '_').replace('/', '_')
        existing = [
            f for f in os.listdir(self.output_dir)
            if f.startswith(f"report_{safe_topic}_") and f.endswith('.md')
        ]
        for old_file in existing:
            old_path = os.path.join(self.output_dir, old_file)
            import shutil
            trash_dir = os.path.expanduser("~/.Trash")
            shutil.move(old_path, os.path.join(trash_dir, old_file))
            print(f"   🗑️  归档旧报告: {old_file}")

        # 保存报告
        filename = f"report_{safe_topic}_{report_id}.md" 
        filepath = os.path.join(self.output_dir, filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(report)
            
        return filepath
    
    def _generate_scenarios(
        self, 
        results: List[AnalysisResult], 
        topic: str,
        politico_verification: Dict = None
    ) -> List[Dict[str, Any]]:
        """生成A/B/C三种情景，冲突区使用双基线"""
        
        # 判定是否为冲突区
        is_conflict_zone = False
        conflict_evidence = []
        if politico_verification:
            is_conflict_zone = politico_verification.get("is_conflict_zone", False)
            conflict_evidence = politico_verification.get("conflict_evidence", [])
        
        # 备用冲突区判定：基于sentinel/admiral的趋势
        if not is_conflict_zone:
            for r in results:
                if r.dimension in ("sentinel", "admiral") and ("恶化" in r.trend or "升温" in r.trend):
                    is_conflict_zone = True
                    conflict_evidence.append(f"{r.expert}趋势={r.trend}")
                    break
        
        # 基于趋势分布推断情景概率
        trends = [r.trend for r in results]
        worsen_count = sum(1 for t in trends if '恶化' in t or '升温' in t)
        improve_count = sum(1 for t in trends if '好转' in t)
        
        if is_conflict_zone:
            # 冲突区双基线：不默认乐观
            scenarios = [
                {
                    "name": "A. 乐观情景",
                    "trigger": "强降温信号出现（双边停火+国际监督+领导人承诺，三者缺一不可）",
                    "probability": "15-20%",
                    "description": f"{topic}超预期缓和，对话渠道恢复",
                    "china_response": "抓住机遇，扩大合作"
                },
                {
                    "name": "B. 现状延续",
                    "trigger": "冲突维持当前烈度，无重大突破", 
                    "probability": "40%",
                    "description": f"{topic}持续紧张，低烈度交火成为新常态",
                    "china_response": "保持战略定力，积蓄力量"
                },
                {
                    "name": "C. 升级情景",
                    "trigger": "政治意愿反转/误判/升级阶梯跃迁",
                    "probability": "30-35%",
                    "description": f"{topic}急剧恶化，冲突规模扩大",
                    "china_response": "启动应急响应，做好最坏准备"
                }
            ]
        else:
            # 非冲突区：传统概率分布
            total = len(trends) if trends else 1
            scenarios = [
                {
                    "name": "A. 乐观情景",
                    "trigger": "各方保持克制，对话渠道畅通",
                    "probability": f"{max(10, 20 - worsen_count * 5)}%",
                    "description": f"{topic}趋于缓和，合作空间扩大",
                    "china_response": "抓住机遇，扩大合作"
                },
                {
                    "name": "B. 基准情景", 
                    "trigger": "维持现状，有限摩擦但可控",
                    "probability": f"{max(40, 60 - abs(worsen_count - improve_count) * 5)}%",
                    "description": f"{topic}持续紧张但无重大突破",
                    "china_response": "保持战略定力，积蓄力量"
                },
                {
                    "name": "C. 悲观情景",
                    "trigger": "误判/意外事件导致升级",
                    "probability": f"{min(30, 10 + worsen_count * 5)}%",
                    "description": f"{topic}急剧恶化，冲突风险上升",
                    "china_response": "做好最坏准备，争取最好结果"
                }
            ]
        
        return scenarios
    
    def _generate_actions(
        self,
        results: List[AnalysisResult],
        council: JewishCouncilOutput
    ) -> Dict[str, List[Dict[str, str]]]:
        """生成分级行动建议 — 结构化对象（含负责人+验收标准）"""
        
        actions = {
            "immediate": [
                {
                    "action": "确认关键情报来源可靠性",
                    "deadline": "24小时内",
                    "owner": "情报分析师",
                    "acceptance": "完成3个以上独立信源交叉验证，输出验证报告"
                },
                {
                    "action": "设定监控指标和预警阈值",
                    "deadline": "48小时内",
                    "owner": "风险监控员",
                    "acceptance": "建立至少2个量化指标（如运价波动率、冲突事件频次），设定红/黄/绿三级阈值"
                },
                {
                    "action": "通知相关方进入关注状态",
                    "deadline": "立即",
                    "owner": "协调员",
                    "acceptance": "向业务、运营、风控3个方向发送预警通知，确认收悉"
                }
            ],
            "short_term": [
                {
                    "action": "持续跟踪事态发展",
                    "deadline": "每日更新，持续1周",
                    "owner": "情报分析师",
                    "acceptance": "每日18:00前提交当日摘要，关键变化即时上报"
                },
                {
                    "action": "交叉验证多源信息",
                    "deadline": "3个工作日内",
                    "owner": "研究分析师",
                    "acceptance": "同一事件至少3个独立信源确认，标注信源可信度等级"
                },
                {
                    "action": "评估对现有布局的影响",
                    "deadline": "5个工作日内",
                    "owner": "战略分析师",
                    "acceptance": "输出影响评估矩阵（高/中/低×概率），明确需调整的布局项"
                }
            ],
            "medium_term": [
                {
                    "action": "根据情景演化调整策略",
                    "deadline": "2周内",
                    "owner": "战略主管",
                    "acceptance": "基于A/B/C情景更新策略文档，明确触发条件和响应动作"
                },
                {
                    "action": "强化高置信度领域的投入",
                    "deadline": "1个月内",
                    "owner": "投资/运营负责人",
                    "acceptance": "识别置信度≥75%的维度，制定资源倾斜方案并执行"
                },
                {
                    "action": "建立更系统的监测机制",
                    "deadline": "1个月内",
                    "owner": "产品经理",
                    "acceptance": "上线自动化监控看板，覆盖至少5个核心指标，支持邮件/微信告警"
                }
            ]
        }
        
        # 根据风险等级调整
        if council.solomon.warning_level == "🔴 高风险":
            actions["immediate"].insert(0, {
                "action": "🔴 启动应急响应机制",
                "deadline": "立即",
                "owner": "应急指挥官",
                "acceptance": "召开应急会议（30分钟内），启动危机响应流程，指定专人跟进"
            })
            actions["short_term"].insert(0, {
                "action": "准备多套应对预案",
                "deadline": "3个工作日内",
                "owner": "战略分析师",
                "acceptance": "制定A/B/C三套预案，每套明确触发条件、执行步骤、资源需求"
            })
        
        if council.rothschild.arbitrage_gaps:
            actions["short_term"].append({
                "action": "布局识别出的套利机会",
                "deadline": "1周内",
                "owner": "投资负责人",
                "acceptance": "完成套利机会可行性分析，制定进入方案，明确资金规模和退出条件"
            })
            
        return actions
    
    def _assemble_report(
        self,
        topic: str,
        timestamp: str,
        priority: str,
        intelligence_summary: List[Dict],
        analysis_table: str,
        jewish_council: str,
        scenarios: List[Dict],
        actions: Dict[str, List[str]],
        politico_section: str = ""
    ) -> str:
        """组装完整报告"""
        
        priority_emoji = {"高": "🔴", "中": "🟡", "低": "🟢"}.get(priority, "⚪")
        
        lines = [
            f"# 🌍 全球局势分析报告",
            f"",
            f"**主题**: {topic}",
            f"**时间**: {timestamp}",
            f"**优先级**: {priority_emoji} {priority}",
            f"**报告ID**: GI-{datetime.now().strftime('%Y%m%d-%H%M%S')}",
            f"",
            "---",
            f"",
            "## 一、情报摘要",
            f"",
        ]
        
        # 情报摘要
        for i, intel in enumerate(intelligence_summary, 1):
            title = intel.get('title', '未知')
            source = intel.get('source', '未知来源')
            lines.append(f"{i}. **{title}** — {source}")
        lines.append("")
        
        # 8维分析
        lines.append("## 二、8维专家扫描")
        lines.append("")
        lines.append(analysis_table)
        lines.append("")
        
        # 犹太智囊（跳过内部的 ## 二、 因为这里已经用过 二了）
        jewish_section = jewish_council.replace('## 二、犹太智囊推演', '## 三、犹太智囊推演')
        lines.append(jewish_section)
        lines.append("")
        
        # Politico 校验层
        if politico_section:
            lines.append("## 四、🏛️ Politico 政治现实校验")
            lines.append("")
            lines.append(politico_section)
            lines.append("")
        
        # 情景预判
        scenario_chapter = "五" if politico_section else "四"
        lines.append(f"## {scenario_chapter}、情景预判")
        lines.append("")
        lines.append("| 情景 | 触发条件 | 概率 | 中国应对 |")
        lines.append("|------|---------|------|---------|")
        for s in scenarios:
            lines.append(f"| **{s['name']}** | {s['trigger']} | {s['probability']} | {s['china_response']} |")
        lines.append("")
        
        for s in scenarios:
            lines.append(f"**{s['name']}**: {s['description']}")
            lines.append("")
        
        # 行动建议
        action_chapter = "六" if politico_section else "五"
        lines.append(f"## {action_chapter}、行动建议")
        lines.append("")
        lines.append("**立即行动（<1周）**:")
        for a in actions["immediate"]:
            lines.append(f"- **{a['action']}**")
            lines.append(f"  - 截止时间：{a['deadline']} | 负责人：{a['owner']}")
            lines.append(f"  - 验收标准：{a['acceptance']}")
        lines.append("")
        lines.append("**短期布局（1-3月）**:")
        for a in actions["short_term"]:
            lines.append(f"- **{a['action']}**")
            lines.append(f"  - 截止时间：{a['deadline']} | 负责人：{a['owner']}")
            lines.append(f"  - 验收标准：{a['acceptance']}")
        lines.append("")
        lines.append("**中期规划（3-6月）**:")
        for a in actions["medium_term"]:
            lines.append(f"- **{a['action']}**")
            lines.append(f"  - 截止时间：{a['deadline']} | 负责人：{a['owner']}")
            lines.append(f"  - 验收标准：{a['acceptance']}")
        lines.append("")
        
        # 页脚
        lines.append("---")
        lines.append("")
        lines.append(f"*报告由 Global Intelligence 系统自动生成*")
        lines.append(f"*9维专家 + 双犹太智囊 + Politico校验 | 伊迪丝总调度*")
        
        return '\n'.join(lines)


def main():
    """CLI测试入口"""
    from analyzer import ExpertAnalyzer, AnalysisResult
    from jewish_council import JewishCouncil
    
    skill_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    # 模拟数据
    test_intel = [
        {"title": "中美AI差距仅剩2.7%", "source": "Reuters"},
        {"title": "美国考虑扩大芯片管制", "source": "Bloomberg"},
        {"title": "阿里AI贡献全球第三", "source": "TechCrunch"},
    ]
    
    test_results = [
        AnalysisResult('atlas', '地缘战略家', '🗺️', '中美AI竞争白热化', '↑恶化', 85, [], [], ''),
        AnalysisResult('tesla', '科技竞争家', '⚡', '技术差距快速缩小', '↗️升温', 80, [], [], ''),
        AnalysisResult('plutus', '经济金融家', '💰', '资本投入差距仍大', '→平稳', 70, [], [], ''),
        AnalysisResult('sentinel', '安全情报家', '🛡️', '技术封锁风险上升', '↑恶化', 75, [], [], ''),
        AnalysisResult('dragon', '中国影响家', '🐉', '自主可控加速推进', '↗️升温', 78, [], [], ''),
    ]
    
    council = JewishCouncil()
    council_output = council.deliberate(test_results, "中美AI竞争")
    
    generator = ReportGenerator(skill_path)
    report_path = generator.generate(
        topic="中美AI竞争态势",
        intelligence=test_intel,
        analysis_results=test_results,
        council_output=council_output,
        priority="高"
    )
    
    print(f"✅ 报告已生成: {report_path}")
    
    # 显示报告预览
    with open(report_path) as f:
        content = f.read()
        print("\n" + "=" * 60)
        print("报告预览 (前30行):")
        print("=" * 60)
        print('\n'.join(content.split('\n')[:30]))


if __name__ == '__main__':
    main()
