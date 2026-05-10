#!/usr/bin/env python3
"""
global-intelligence / scripts / jewish_council.py
双犹太智囊推演引擎
"""

import json
from typing import Dict, List, Any
from dataclasses import dataclass

@dataclass
class RiskAssessment:
    tail_risks: List[Dict[str, Any]]  # 尾部风险列表
    hedging_strategies: List[str]     # 对冲策略
    warning_level: str                # 🔴🟡🟢
    key_uncertainties: List[str]      # 关键不确定性

@dataclass
class OpportunityScan:
    arbitrage_gaps: List[Dict[str, Any]]  # 套利空间
    connection_opportunities: List[str]    # 连接机会
    timing_windows: List[Dict[str, Any]]   # 时间窗口
    action_priority: str                   # 行动优先级

@dataclass
class JewishCouncilOutput:
    solomon: RiskAssessment      # 所罗门：风险视角
    rothschild: OpportunityScan  # 罗斯柴尔德：机会视角
    synthesis: str               # 综合判断


class JewishCouncil:
    """
    双犹太智囊推演系统
    
    所罗门 (Solomon): 风险架构师
    - 问：最坏情况是什么？
    - 问：如何不亏钱？
    - 问：什么会让我们全军覆没？
    
    罗斯柴尔德 (Rothschild): 机会挖掘者  
    - 问：信息差在哪？
    - 问：谁能连接谁？
    - 问：现在该押注什么？
    """
    
    def __init__(self):
        self.council_config = self._load_config()
    
    def _load_config(self) -> Dict:
        """加载智囊配置"""
        return {
            "solomon": {
                "name": "所罗门",
                "title": "风险架构师",
                "emoji": "🎩",
                "principles": [
                    "永远先想最坏情况",
                    "分散是唯一的免费午餐",
                    "流动性比收益率更重要",
                    "黑天鹅总会来，只是时间问题"
                ]
            },
            "rothschild": {
                "name": "罗斯柴尔德",
                "title": "机会挖掘者", 
                "emoji": "🏦",
                "principles": [
                    "信息就是金钱",
                    "连接创造价值",
                    "在别人恐惧时贪婪",
                    "时机比方向更重要"
                ]
            }
        }
    
    def deliberate(self, analysis_results: List[Any], topic: str) -> JewishCouncilOutput:
        """
        双智囊推演主入口
        
        Args:
            analysis_results: 8维专家分析结果
            topic: 分析主题
            
        Returns:
            双智囊综合输出
        """
        # 所罗门视角：风险分析
        solomon_view = self._solomon_analysis(analysis_results, topic)
        
        # 罗斯柴尔德视角：机会挖掘
        rothschild_view = self._rothschild_analysis(analysis_results, topic)
        
        # 综合判断
        synthesis = self._synthesize(solomon_view, rothschild_view)
        
        return JewishCouncilOutput(
            solomon=solomon_view,
            rothschild=rothschild_view,
            synthesis=synthesis
        )
    
    def _solomon_analysis(self, results: List[Any], topic: str) -> RiskAssessment:
        """所罗门：风险架构师视角"""
        
        # 收集所有风险信号
        risk_signals = []
        confidence_levels = []
        
        for r in results:
            # 恶化 or 升温 = 风险信号
            if hasattr(r, 'trend') and ('恶化' in r.trend or '升温' in r.trend):
                risk_signals.append(f"{r.expert}: {r.core_judgment}")
            if hasattr(r, 'confidence'):
                confidence_levels.append(r.confidence)
        
        avg_confidence = sum(confidence_levels) / len(confidence_levels) if confidence_levels else 50
        
        # 冲突区概率修正：不硬编码，根据实际信号动态计算
        worsening_count = len(risk_signals)
        total_experts = len(results) if results else 1
        upgrade_prob = min(40, 5 + worsening_count * 8)  # 5%基础 + 每个恶化信号+8%
        expansion_prob = min(25, 5 + worsening_count * 5)  # 5%基础 + 每个恶化信号+5%
        
        # 尾部风险识别
        tail_risks = [
            {
                "scenario": f"{topic}突然升级",
                "probability": f"{upgrade_prob}%",
                "impact": "系统性冲击",
                "trigger": "意外事件/误判/政治意愿反转",
                "political_dimension": "领导人可能因国内压力做出非理性升级"
            },
            {
                "scenario": "多方卷入扩大化",
                "probability": f"{expansion_prob}%", 
                "impact": "区域性危机",
                "trigger": "联盟激活/代理人失控/升级阶梯跃迁",
                "political_dimension": "执政联盟极端派施压、选举周期驱动"
            },
            {
                "scenario": "政治意愿反转",
                "probability": f"{min(20, 3 + worsening_count * 4)}%",
                "impact": "停火/协议撕毁",
                "trigger": "国内右翼压力/领导人支持率下滑/民族情绪事件",
                "political_dimension": "政治生存逻辑压倒国际承诺"
            }
        ]
        
        # 对冲策略
        hedging = [
            "保持情报渠道多元化，避免单一信源依赖",
            "关键决策预留缓冲期，不押注单一情景",
            "建立早期预警机制，设定关键指标阈值",
            "准备B/C计划，明确撤退/转向条件",
            "监控领导人的政治生存压力指标（支持率、执政联盟稳定性、选举时间表）"
        ]
        
        # 风险等级（同时考虑恶化和升温）
        worsening = sum(1 for r in results if hasattr(r, 'trend') and ('恶化' in r.trend or '升温' in r.trend))
        if worsening >= 3:
            warning_level = "🔴 高风险"
        elif worsening >= 1:
            warning_level = "🟡 中等风险"
        else:
            warning_level = "🟢 相对安全"
            
        return RiskAssessment(
            tail_risks=tail_risks,
            hedging_strategies=hedging,
            warning_level=warning_level,
            key_uncertainties=[
                "主要行为体的真实意图",
                "关键决策者的风险偏好",
                "外部冲击的触发时机"
            ]
        )
    
    def _rothschild_analysis(self, results: List[Any], topic: str) -> OpportunityScan:
        """罗斯柴尔德：机会挖掘者视角"""
        
        # 识别信息差和套利空间
        arbitrage_gaps = []
        
        # 检查是否有分歧信号
        trends = [r.trend for r in results if hasattr(r, 'trend')]
        if '↑恶化' in trends and '↓好转' in trends:
            arbitrage_gaps.append({
                "type": "认知差",
                "description": "不同维度信号分歧，存在信息套利空间",
                "action": "深入调查分歧根源，寻找被低估的维度"
            })
        
        # 检查高置信度机会
        high_conf = [r for r in results if hasattr(r, 'confidence') and r.confidence >= 75]
        if high_conf:
            arbitrage_gaps.append({
                "type": "确定性溢价",
                "description": f"{len(high_conf)}个维度置信度≥75%，可优先布局",
                "action": "在高置信度领域加大投入"
            })
        
        # 时间窗口
        timing_windows = [
            {
                "phase": "立即",
                "window": "未来72小时",
                "action": "密切监控关键指标变化",
                "urgency": "高"
            },
            {
                "phase": "短期", 
                "window": "未来2-4周",
                "action": "根据事态发展调整仓位",
                "urgency": "中"
            },
            {
                "phase": "中期",
                "window": "未来3-6个月", 
                "action": "结构性布局",
                "urgency": "低"
            }
        ]
        
        return OpportunityScan(
            arbitrage_gaps=arbitrage_gaps,
            connection_opportunities=[
                "连接不同维度的专家，交叉验证关键假设",
                "建立与一线信息源的直连通道",
                "寻找被主流忽视的另类视角"
            ],
            timing_windows=timing_windows,
            action_priority="监控→验证→布局" if arbitrage_gaps else "观望→等待→跟进"
        )
    
    def _synthesize(self, solomon: RiskAssessment, rothschild: OpportunityScan) -> str:
        """综合双智囊观点"""
        
        if solomon.warning_level == "🔴 高风险":
            return f"{solomon.warning_level} - 优先防御，谨慎寻找结构性机会"
        elif rothschild.arbitrage_gaps:
            return "🟡 机会与风险并存 - 选择性布局，严格止损"
        else:
            return "🟢 相对平静 - 保持监控，积累信息优势"


def format_jewish_council(output: JewishCouncilOutput) -> str:
    """格式化犹太智囊输出"""
    
    lines = ["## 二、犹太智囊推演", ""]
    
    # 所罗门
    lines.append("### 🎩 所罗门：风险架构")
    lines.append(f"**风险等级**: {output.solomon.warning_level}")
    lines.append("")
    lines.append("**尾部风险**:")
    for risk in output.solomon.tail_risks:
        lines.append(f"- {risk['scenario']} (概率{risk['probability']}) — {risk['impact']}")
    lines.append("")
    lines.append("**对冲建议**:")
    for h in output.solomon.hedging_strategies:
        lines.append(f"- {h}")
    lines.append("")
    
    # 罗斯柴尔德
    lines.append("### 🏦 罗斯柴尔德：机会挖掘")
    if output.rothschild.arbitrage_gaps:
        lines.append("**套利空间**:")
        for gap in output.rothschild.arbitrage_gaps:
            lines.append(f"- [{gap['type']}] {gap['description']}")
    else:
        lines.append("**套利空间**: 暂无显著信息差")
    lines.append("")
    lines.append("**时间窗口**:")
    for tw in output.rothschild.timing_windows:
        urgency_emoji = {"高": "🔴", "中": "🟡", "低": "🟢"}.get(tw['urgency'], "⚪")
        lines.append(f"- {urgency_emoji} **{tw['phase']}** ({tw['window']}): {tw['action']}")
    lines.append("")
    
    # 综合
    lines.append(f"**综合判断**: {output.synthesis}")
    
    return '\n'.join(lines)


def main():
    """CLI测试入口"""
    from analyzer import AnalysisResult
    
    # 模拟测试数据
    test_results = [
        AnalysisResult('atlas', '地缘战略家', '🗺️', '中美AI竞争白热化', '↑恶化', 85, [], [], ''),
        AnalysisResult('tesla', '科技竞争家', '⚡', '技术差距快速缩小', '↗️升温', 80, [], [], ''),
        AnalysisResult('plutus', '经济金融家', '💰', '资本投入差距仍大', '→平稳', 70, [], [], ''),
    ]
    
    council = JewishCouncil()
    output = council.deliberate(test_results, "中美AI竞争")
    
    print("=" * 60)
    print("双犹太智囊推演测试")
    print("=" * 60)
    print(format_jewish_council(output))


if __name__ == '__main__':
    main()
