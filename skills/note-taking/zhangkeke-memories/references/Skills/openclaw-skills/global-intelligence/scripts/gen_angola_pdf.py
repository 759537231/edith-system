#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""中国安哥拉货代专项分析报告 PDF"""

import sys, os
sys.path.insert(0, os.path.expanduser("~/Library/Application Support/QClaw/openclaw/config/skills/pdf/scripts"))
from setup_chinese_pdf import setup_chinese_pdf

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    HRFlowable, PageBreak
)
from reportlab.lib.units import cm

OUTPUT = os.path.expanduser("~/Desktop/中国安哥拉货代专项分析报告_GI_20260418.pdf")

def P(text, style):
    return Paragraph(text, style)

def B(text, style):
    return Paragraph(f"<b>{text}</b>", style)

def build_pdf():
    cn_font, styles = setup_chinese_pdf()

    body = ParagraphStyle("Body", parent=styles["Normal"],
        fontSize=10, leading=16, spaceAfter=3)
    small = ParagraphStyle("Small", parent=styles["Normal"],
        fontSize=8.5, leading=12, textColor=colors.HexColor("#555577"))
    cover_title = ParagraphStyle("CT", parent=styles["Title"],
        fontSize=22, leading=28, alignment=TA_CENTER,
        textColor=colors.HexColor("#1a1a2e"))
    cover_sub = ParagraphStyle("CS", parent=styles["Normal"],
        fontSize=13, leading=18, alignment=TA_CENTER,
        textColor=colors.HexColor("#4a4a6a"))
    cover_meta = ParagraphStyle("CM", parent=styles["Normal"],
        fontSize=9.5, leading=14, alignment=TA_CENTER,
        textColor=colors.HexColor("#8888aa"))
    sec = ParagraphStyle("Sec", parent=styles["Heading1"],
        fontSize=13.5, leading=20, spaceBefore=12, spaceAfter=4,
        textColor=colors.HexColor("#1a1a2e"))
    sub = ParagraphStyle("Sub", parent=styles["Heading2"],
        fontSize=11, leading=16, spaceBefore=8, spaceAfter=3,
        textColor=colors.HexColor("#2d4a8a"))

    H_BG   = colors.HexColor("#1a1a2e")
    H_FG   = colors.white
    ALT    = colors.HexColor("#f4f5fb")
    T_UP   = colors.HexColor("#e74c3c")
    T_DN   = colors.HexColor("#27ae60")
    T_FLAT = colors.HexColor("#7f8c8d")
    ACC    = colors.HexColor("#2d4a8a")
    GOLD   = colors.HexColor("#c9a84c")
    WARN   = colors.HexColor("#8B0000")
    ROT_BG = colors.HexColor("#3d2b1f")

    def tp(text):
        c = T_UP if "\u2191" in text or "\u2197" in text else T_DN if "\u2192" in text or "\u2193" in text else T_FLAT
        return P(f"<b><font color='{c.hexval()}'>{text}</font></b>", body)

    doc = SimpleDocTemplate(
        OUTPUT, pagesize=A4,
        leftMargin=1.8*cm, rightMargin=1.8*cm,
        topMargin=2*cm, bottomMargin=2*cm,
        title="\u4e2d\u56fd\u5b89\u54e5\u62c9\u8d27\u4ee3\u4e13\u9879\u5206\u6790\u62a5\u544a"
    )
    story = []

    # ── 封面 ────────────────────────────────────────────────
    story += [
        Spacer(1, 1.5*cm),
        P("\U0001f30d \u4e2d\u56fd\u5b89\u54e5\u62c9\u8d27\u4ee3\u4e13\u9879\u5206\u6790", cover_title),
        Spacer(1, 0.3*cm),
        P("\u4e2d\u4e1c\u5c40\u52bf \u00b7 \u5168\u7403\u822a\u8fd0 \u00b7 GI\u56db\u56e2\u961f10\u4e13\u5bb6", cover_sub),
        Spacer(1, 0.3*cm),
        HRFlowable(width="55%", thickness=2, color=GOLD, spaceAfter=0.3*cm),
        P("2026-04-18 CST  |  \u9ad8\u4f18\u5148\u7ea7  |  \u9690\u79c9\u8c03\u5ea6\u5458\uff08QClaw\uff09", cover_meta),
        P("\u5730\u8fb9\u6218\u7565\uff0b\u7ecf\u6d4e\u8d44\u6e90\uff0b\u5b89\u5168\u519b\u4e8b\uff0b\u821e\u60c5\u4e2d\u56fd\uff084\u56e2\u961f\uff09", cover_meta),
        Spacer(1, 0.5*cm),
        P("\U0001f5fa Atlas\uff08\u5730\u8fb9\uff09  \U0001f4dc Chronos\uff08\u5386\u53f2\uff09  \U0001f4b0 Plutus\uff08\u7ecf\u6d4e\uff09  \u26f3 Prometheus\uff08\u80fd\u6e90\uff09  \U0001f69e Mariner\uff08\u6d77\u8fd0\uff09", cover_meta),
        P("\U0001f6e1 Sentinel\uff08\u5b89\u5168\uff09  \u2693 Admiral\uff08\u6d77\u4e8b\uff09  \u26a1 Tesla\uff08\u79d1\u6280\uff09  \U0001f4e2 Echo\uff08\u821e\u60c5\uff09  \U0001f409 Dragon\uff08\u4e2d\u56fd\uff09", cover_meta),
        Spacer(1, 0.4*cm),
        P("\u4f5c\u4e1a\uff1a\u4f0a\u8fea\u65af \u00b7 GI v2.0 \u56e2\u961f\u5236 \u00b7 \u9694\u79bb\u8c03\u5ea6\u5458", small),
        PageBreak(),
    ]

    # ── 第一章：核心结论 ────────────────────────────────────
    story += [
        P("\u4e00\u3001\u6838\u5fc3\u7ed3\u8bba", sec),
        HRFlowable(width="100%", thickness=1, color=ACC, spaceAfter=0.2*cm),
    ]

    quote_s = ParagraphStyle("QS", parent=body,
        fontSize=11, leading=17, textColor=colors.white, fontName=cn_font)
    qbox = Table([[P(
        "\u201c\u4e2d\u4e1c\u5c40\u52bf\u5bf9\u4e2d\u56fd-\u5b89\u54e5\u62c9\u822a\u7ebf\u5f71\u54cd\u6709\u9650\uff0c\u4e3b\u8981\u98ce\u9669\u5728\u7ea2\u6d77-\u66fc\u5fb7\u6d77\u5ce1\u6bb5\uff1b\u5efa\u8bae\u91c7\u7528\u597d\u671b\u89d2\u7ed5\u884c\u6216\u5370\u5ea6\u6d0b\u76f4\u8fbe\u897f\u975e\u822a\u7ebf\uff0c\u907f\u5f00\u7ea2\u6d77\u9ad8\u98ce\u9669\u533a\uff0c\u5229\u7528\u4e2d\u5b89\u77ff\u6cb9\u8d38\u6613\u7ed3\u6784\u548c\u4e00\u5e26\u4e00\u8def\u653f\u7b56\u7ea2\u5229\u5207\u5165\u5e02\u573a\uff0c6\u4e2a\u6708\u5185\u822a\u8fd0\u4ef7\u9884\u8ba1\u7a33\u6709\u964d\u3002\u201d",
        quote_s)]], colWidths=[14.4*cm])
    qbox.setStyle(TableStyle([
        ("BACKGROUND",(0,0),(-1,-1),H_BG),
        ("TOPPADDING",(0,0),(-1,-1),12),("BOTTOMPADDING",(0,0),(-1,-1),12),
        ("LEFTPADDING",(0,0),(-1,-1),14),("RIGHTPADDING",(0,0),(-1,-1),14),
    ]))
    story.append(qbox)
    story.append(Spacer(1, 0.3*cm))

    # ── 第二章：团队综合分析 ───────────────────────────────
    story += [
        P("\u4e8c\u3001\u56e2\u961f\u7efc\u5408\u5206\u6790", sec),
        HRFlowable(width="100%", thickness=1, color=ACC, spaceAfter=0.15*cm),
    ]

    # 团队概览表
    overview = [
        ["\u56e2\u961f","\u9886\u961f","\u6838\u5fc3\u5224\u65ad","\u8d8b\u52bf","\u7f6e\u4fe1"],
        ["\U0001f5fa \u5730\u8fb9\u6218\u7565",
         "Atlas",
         "\u822a\u7ebf\u53ef\u89c4\u907f\u4e2d\u4e1c\u5e72\u6270\uff0c\u9a6c\u516d\u7532\u2192\u597d\u671b\u89d2\u2192\u7f57\u5b89\u8fbe\uff0c\u5168\u7a0b\u907f\u5f00\u5b89\u5168\u533a",
         "\u2192\u964d\u6e29","75%"],
        ["\U0001f4b0 \u7ecf\u6d4e\u8d44\u6e90",
         "Plutus+Mariner",
         "\u5f53\u524d$2500-3000/FEU\uff0c6\u4e2a\u6708\u540e$2000-2500\uff1bCNCA\u5fc5\u529e\uff0c6\u5de5\u4f5c\u65e5\u529e\u7406",
         "\u2192\u964d\u6e29","72%"],
        ["\U0001f6e1 \u5b89\u5168\u519b\u4e8b",
         "Sentinel+Admiral",
         "\u66fc\u5fb7\u6d77\u5ce1\u9ad8\u98ce\u9669\uff0c\u5b89\u54e5\u62c9\u6d77\u5cb8\u4f4e\u98ce\u9669\uff0c\u89e3\u653e\u519b\u57fa\u5730\u62a4\u822a",
         "\u2192\u964d\u6e29","78%"],
        ["\U0001f4e2 \u821e\u60c5\u4e2d\u56fd",
         "Echo+Dragon",
         "\u4e00\u5e26\u4e00\u8def+\u4e2d\u975e\u5408\u4f5c\u8bba\u575b\uff0c\u653f\u7b56\u7ea2\u5229\u660e\u663e\uff0c\u4e2d\u5b89\u8d38\u6613\u7ed3\u6784\u6709\u5229",
         "\u2192\u5e73\u7a33","70%"],
    ]
    def orow(row, is_header=False):
        if is_header: return [B(c, body) for c in row]
        styled = []
        for j, c in enumerate(row):
            if j == 3: styled.append(tp(c))
            else: styled.append(P(c, body))
        return styled
    ot = Table(
        [orow(overview[0], True)] + [orow(r) for r in overview[1:]],
        colWidths=[2.2*cm, 2.5*cm, 7.2*cm, 1.6*cm, 1.6*cm],
        repeatRows=1
    )
    ot.setStyle(TableStyle([
        ("BACKGROUND",(0,0),(-1,0),ACC),
        ("TEXTCOLOR",(0,0),(-1,0),H_FG),
        ("ROWBACKGROUNDS",(0,1),(-1,-1),[colors.white, ALT]),
        ("GRID",(0,0),(-1,-1),0.4,colors.HexColor("#ccd0ee")),
        ("VALIGN",(0,0),(-1,-1),"TOP"),
        ("TOPPADDING",(0,0),(-1,-1),4),("BOTTOMPADDING",(0,0),(-1,-1),4),
        ("LEFTPADDING",(0,0),(-1,-1),5),
    ]))
    story.append(ot)
    story.append(Spacer(1, 0.3*cm))

    # ── 各团队详细内容 ─────────────────────────────────────
    # 地缘战略
    story += [
        P("\U0001f5fa \u5730\u8fb9\u6218\u7565\u56e2\u961f\uff08Atlas + Chronos\uff09", sub),
        P("\U0001f5fa <b>Atlas</b>\uff1a\u822a\u7ebf\u5bf9\u4e2d\u4e1c\u5c40\u52bf\u7684\u5f71\u54cd\u662f\u95f4\u63a5\u7684\u3001\u53ef\u89c4\u907f\u7684\u3002\u4e2d\u56fd-\u897f\u975e\u822a\u7ebf\u4e0d\u4f9d\u8d56\u82cf\u4f0a\u58eb\u578b\u6cb9\uff0c\u6838\u5fc3\u54bd\u558a\u8981\u9053\u662f\u9a6c\u516d\u7532\u6d77\u5ce1\uff08\u4e2d\u56fd\u5df2\u6709\u6548\u63a7\u5236\uff09\u548c\u597d\u671b\u89d2\uff08\u4e2d\u7acb\u6c34\u57df\uff09\u3002\u66fc\u5fb7\u6d77\u5ce1\u548c\u970d\u5c14\u6728\u5179\u7684\u98ce\u9669\u4e3b\u8981\u5f71\u54cd\u4e2d\u4e1c-\u4e9a\u6d32\u80fd\u6e90\u822a\u7ebf\uff0c\u5bf9\u4e2d\u56fd-\u5b89\u54e5\u62c9\u8d27\u8f66\u4e0d\u6784\u6210\u76f4\u63a5\u963b\u65ad\u3002", body),
        P("\U0001f4dc <b>Chronos</b>\uff1a\u5386\u53f2\u7c7b\u6bd4\u2014\u20141973\u5e74\u77f3\u6cb9\u5371\u673a\u540e\uff0c\u897f\u65b9\u822a\u8fd0\u4e1a\u901a\u8fc7\u7ed5\u884c\u597d\u671b\u89d2\u548c\u5f00\u53d1\u66ff\u4ee3\u822a\u7ebf\u5316\u89e3\u5316\u82cf\u4f0a\u4e2d\u65ad\u98ce\u9669\u3002\u5f53\u524d\u5c40\u52bf\u4e0e1980\u5e74\u4ee3\u201c\u6cb9\u8f6e\u6218\u4e89\u201d\u65f6\u671f\u76f8\u4f3c\u5ea6\u8f83\u9ad8\uff1a\u4f0a\u671f\u544a\u544a\u66fc\u5fb7\u6d77\u5ce1\u3001\u80e1\u585e\u88c5\u5907\u5bf9\u7ea2\u6d77\u822a\u7ebf\u88ad\u6270\u3002\u4f46\u4e2d\u56fd-\u5b89\u54e5\u62c9\u822a\u7ebf\u53ef\u201c\u590d\u523b\u5386\u53f2\u8def\u5f84\u201d\uff1a\u4ece\u4e2d\u56fd\u6e2f\u53e3\u51fa\u53d1\uff0c\u7ecf\u9a6c\u516d\u7532\u2192\u5370\u5ea6\u6d0b\u2192\u597d\u671f\u89d2\u2192\u5927\u897f\u6d0b\u2192\u7f57\u5b89\u8fbe\uff0c\u5168\u7a0b\u907f\u5f00\u4e2d\u4e1c\u5b89\u5168\u533a\u3002", body),
        Spacer(1, 0.15*cm),
    ]

    # 经济资源
    story += [
        P("\U0001f4b0 \u7ecf\u6d4e\u8d44\u6e90\u56e2\u961f\uff08Plutus + Prometheus + Mariner\uff09", sub),
        P("\U0001f4b0 <b>Plutus</b>\uff1a\u4e2d\u4e1c\u51b2\u7a81\u5bf9\u5168\u7403\u822a\u8fd0\u7684\u4f20\u5bfc\u673a\u5236\u662f\u201c\u4fdd\u9669\u8d39\u2192\u822a\u8fd0\u4ef7\u2192\u4f9b\u5e94\u94fe\u6210\u672c\u201d\u3002\u5f53\u524d\u4e9a\u4e01\u6e7e\u822a\u8fd0\u4fdd\u9669\u8d39\u4e0a\u6da815%\uff0c\u4f46\u4e3b\u8981\u5f71\u54cd\u7ea2\u6d77\u822a\u7ebf\u3002\u4e2d\u56fd-\u5b89\u54e5\u62c9\u822a\u7ebf\u82e5\u7ed5\u884c\u597d\u671b\u89d2\uff0c\u4fdd\u9669\u8d39\u6ea2\u4ef7\u53ef\u63a7\u5236\u57285%\u4ee5\u5185\u3002", body),
        P("\u26f3 <b>Prometheus</b>\uff1a\u5b89\u54e5\u62c9\u662fOPEC\u6210\u5458\uff0c\u4f46\u77f3\u6cb9\u4ea7\u91cf\u4ece2015\u5e74180\u4e07\u6876/\u65e5\u964d\u81f32024\u5e74\u7ea6110\u4e07\u6876/\u65e5\u3002\u8fd9\u610f\u5473\u7740\uff1a\u5b89\u54e5\u62c9\u5bf9\u4e2d\u56fd\u51fa\u53e3\u4ee5\u539f\u6cb9\u4e3a\u4e3b\uff0c\u56de\u7a0b\u8d27\uff08\u5de5\u4e1a\u54c1\u3001\u673a\u68b0\u8bbe\u5907\uff09\u9700\u6c42\u7a33\u5b9a\u3002\u77f3\u6cb9\u4ea7\u91cf\u4e0b\u964d\u2192\u5b89\u54e5\u62c9\u653f\u5e9c\u8d22\u6536\u627f\u538b\u2192\u53ef\u80fd\u653e\u5bb3\u8fdb\u53e3\u653f\u7b56\u5237\u6fc0\u7ecf\u6d4e\u3002", body),
        P("\U0001f69e <b>Mariner</b>\uff1a\u5f53\u524dSCFI\uff08\u4e0a\u6d77\u96c6\u88c5\u8fd0\u4ef7\u6307\u6570\uff09\u7ea6<b>$1800-2200\u70b9</b>\uff0c\u8f832022\u5e74\u9ad8\u70b9\u56de\u843d60%\u3002\u4e2d\u4e1c\u51b2\u7a81\u5bf9\u8fd0\u4ef7\u7684\u5f71\u54cd\u662f<b>\u7ed3\u6784\u6027\u5206\u5316</b>\uff1a\u7ea2\u6d77\u822a\u7ebf\u8fd0\u4ef7\u4e0a\u6da820-30%\uff1b\u975e\u6d32\u822a\u7ebf\u8fd0\u4ef7\u76f8\u5bf9\u7a33\u5b9a\uff0c\u751a\u81f3\u56e0\u8239\u8239\u8c03\u914d\u6709\u5c0f\u5e45\u4e0b\u884c\u538b\u529b\u3002", body),
        Spacer(1, 0.15*cm),
    ]

    # 安全军事
    story += [
        P("\U0001f6e1 \u5b89\u5168\u519b\u4e8b\u56e2\u961f\uff08Sentinel + Admiral + Tesla\uff09", sub),
        P("\U0001f6e1 <b>Sentinel</b>\uff1a\u66fc\u5fb7\u6d77\u5ce1\u5f53\u524d\u98ce\u9669\u7b49\u7ea7\ud83d\udfe1\u9ad8\u3002\u80e1\u585e\u6b66\u88c5\u4ecd\u63a7\u5236\u4e5f\u95e8\u897f\u90e8\u6d77\u5cb8\uff0c\u4f0a\u671f\u9769\u547d\u536b\u961f\u5df2\u5411\u6297\u62d4\u9635\u7ebf\u53d1\u51fa\u8b66\u544a\uff0c\u610f\u5473\u7740<b>\u975e\u56fd\u5bb6\u884c\u4e3a\u4f53</b>\u5bf9\u5546\u8239\u7684\u5a01\u80c1\u6301\u7eed\u5b58\u5728\u3002\u6700\u574f\u60c5\u666f\uff1a\u4f0a\u671f\u6216\u80e1\u585e\u6b66\u88c5\u9488\u5bf9\u201c\u4e0e\u4ee5\u8272\u5217\u76f8\u5173\u201d\u5546\u8239\uff0c\u4e2d\u56fd\u5546\u8239\u82e5\u88ab\u8bef\u5224\u53ef\u80fd\u6ca1\u5165\u6b66\u88c5\u88ab\u88ad\u3002", body),
        P("\u2693 <b>Admiral</b>\uff1a\u7ea2\u6d77-\u4e9a\u4e01\u6e7e-\u5370\u5ea6\u6d0b\u822a\u7ebf\u5b89\u5168\u8bc4\u4f30\uff1a\u66fc\u5fb7\u6d77\u5ce1\uff08\u54bd\u558a\u5bb3\u5bb3\u5ea6\u4ec530\u516c\u91cc\uff0c\u6613\u88ab\u6c34\u96f7\uff0c\u81ea\u6740\u5f0f\u65e0\u4eba\u8239\u5c01\u9501\uff0c\u5f53\u524d\u98ce\u9669\u7b49\u7ea7\ud83d\udfe1\u9ad8\uff09\uff1b\u4e9a\u4e01\u6e7e\uff08\u56fd\u964d\u62a4\u8239\u529b\u91cf\u5b58\u5728\uff0c\u4e2d\u56fd\u519b\u62a4\u822a\u7f16\u961f\uff09\uff0c\u98ce\u9669\u7b49\u7ea7\ud83d\udfe1\u4e2d\uff09\uff1b\u5370\u5ea6\u6d0b\uff08\u5e7f\u9614\u6c34\u57df\uff0c\u6d77\u76d7\u98ce\u9669\u4f4e\uff0c\u4e2d\u56fd\u5409\u5e03\u63d0\u57fa\u5730\u53ef\u63d0\u4f9b\u8865\u7ed9\u548c\u5e94\u6025\u652f\u63f4\uff0c\u98ce\u9669\u7b49\u7ea7\ud83d\udfe2\u4f4e\uff09\u3002", body),
        P("\u26a1 <b>Tesla</b>\uff1a\u4f0a\u671f\u5bfc\u5f39\u80fd\u529b\uff08\u6d41\u661f-3\u3001\u6ce5\u77f3-2\uff0c\u5c04\u7a0b2000\u516c\u91cc\uff09\u5bf9\u5546\u8239<b>\u65e0\u76f4\u63a5\u5a01\u80c1</b>\uff0c\u5bfc\u5f39\u4e3b\u8981\u9488\u5bf9\u9646\u5730\u76ee\u6807\u3002\u4f46\u9700\u5173\u6ce8\u201c<b>\u65e0\u4eba\u8239\u548c\u6c34\u96f7</b>\u201d\u6280\u672f\u6269\u6563\uff1a\u80e1\u585e\u6b66\u88c5\u5df2\u5c55\u793a\u4f7f\u7528\u4f0a\u671f\u63d0\u4f9b\u7684\u65e0\u4eba\u8239\u88ad\u51fb\u5546\u8239\u80fd\u529b\u3002\u5efa\u8bae\u4e2d\u56fd\u5546\u8239\u5e94\u914d\u5907<b>\u88ab\u52a8\u9632\u5fa1\u8bbe\u5907</b>\uff08\u5982\u58f0\u5b66\u5e72\u6270\u5668\u3001\u9632\u6c34\u96f7\u62d6\u7080\u88c5\u7f6e\uff09\uff0c\u6210\u672c\u7ea2$5-10\u4e07/\u8239\u3002", body),
        Spacer(1, 0.15*cm),
    ]

    # 舆情中国
    story += [
        P("\U0001f4e2 \u821e\u60c5\u4e2d\u56fd\u56e2\u961f\uff08Echo + Dragon\uff09", sub),
        P("\U0001f4e2 <b>Echo</b>\uff1a\u4e2d\u4e1c\u5c40\u52bf\u7684\u56fd\u9645\u821e\u60c5\u53d1\u5c55\u662f\u201c\u4f0a\u671fvs\u7f8e\u4ee5\u201d\u4e8c\u5143\u5bf9\u7acb\uff0c\u4e2d\u56fd\u88ab\u897f\u65b9\u5a92\u4f53\u57ab\u7ed8\u4e3a\u201c\u4f0a\u671f\u652f\u6301\u8005\u201d\uff08\u56e0\u4e2d\u4f0a\u80fd\u6e90\u5408\u4f5c\uff09\u3002\u4f46\u4e2d\u56fd\u5916\u4ea4\u90e8\u8868\u6001\u201c\u5bf9\u8bdd\u534f\u5546\u3001\u53cd\u5bf9\u6b66\u529b\u201d\uff0c\u5728\u963f\u62c9\u4f2f\u4e16\u754c\u821e\u60c5\u4e2d\u5f62\u8c61\u300c\u4e2d\u6027\u504f\u6b63\u9762\u300d\u3002\u5bf9\u4e2d\u56fd-\u5b89\u54e5\u62c9\u8d27\u4ee3\u4e1a\u52a1\u7684\u5f71\u54cd\uff1a<b>\u65e0\u76f4\u63a5\u821e\u60c5\u98ce\u9669</b>\uff0c\u4f46\u9700\u907f\u514d\u627f\u8fd0\u201c\u53ef\u80fd\u88ab\u8ba4\u5b9a\u4e3a\u4e0e\u4ee5\u8272\u5217\u76f8\u5173\u201d\u7684\u8d27\u7269\uff08\u5982\u4ee5\u8272\u5217\u54c1\u724c\u4ea7\u54c1\u3001\u7ecf\u4ee5\u8272\u5217\u6e2f\u53e3\u8f6c\u8fd0\u7684\u8d27\u7269\uff09\u3002", body),
        P("\U0001f409 <b>Dragon</b>\uff1a\u4e2d\u56fd\u5bf9\u975e\u6d32\u8d38\u6613\u653f\u7b56\u6846\u67b6\uff1a\uff081\uff09<b>\u4e00\u5e26\u4e00\u8def</b>\uff1a\u5b89\u54e5\u62c9\u662f\u91cd\u8981\u8282\u70b9\uff0c\u4e2d\u56fd\u5df2\u6295\u8d44\u5b89\u54e5\u62c9\u57fa\u7845\u8bbe\u65bd\uff08\u7f57\u5b89\u8fbe\u6e2f\u6269\u5efa\u3001\u672c\u683c\u62c9\u94c2\u8def\u94c5\u590d\uff09\uff1b\uff082\uff09<b>\u4e2d\u975e\u5408\u4f5c\u8bba\u575b</b>\uff1a2024\u5e74\u5317\u4eac\u5cf0\u4f1a\u63d0\u51fa\u201c\u5341\u5927\u4f19\u4f34\u884c\u52a8\u201d\uff0c\u5305\u62ec\u201c\u8d38\u6613\u7e41\u8363\u4f19\u4f34\u884c\u52a8\u201d\uff0c\u5bf9\u975e\u6d32\u8d38\u6613\u6295\u8d44\u4fbf\u5229\u5316\u6301\u7eed\u63a8\u8fdb\uff1b\uff083\uff09<b>\u503a\u52a1\u7f6e\u6362\u534f\u8bae</b>\uff1a\u4e2d\u56fd\u8fdb\u51fa\u53e3\u94f6\u884c\u4e0e\u5b89\u54e5\u62c9\u653f\u5e9c\u7b7e\u7f6e\u503a\u52a1\u7f6e\u6362\u534f\u8bae\uff0c\u5b89\u54e5\u62c9\u4ee5\u77f3\u6cb9\u507f\u8fd8\u90e8\u5206\u503a\u52a1\uff0c\u8fd9\u610f\u5473\u7740\u4e2d\u5b89\u8d38\u6613\u7ed3\u6784\u662f<b>\u201c\u77f3\u6cb9\u6362\u57fa\u7845+\u5de5\u4e1a\u54c1\u8fdb\u53e3\u201d</b>\u3002", body),
        Spacer(1, 0.3*cm),
    ]

    story.append(PageBreak())

    # ── 第三章：犹太智囊 ────────────────────────────────────
    story += [
        P("\u4e09\u3001\u72b9\u592a\u667a\u56ca\u63a8\u6f14", sec),
        HRFlowable(width="100%", thickness=1, color=ACC, spaceAfter=0.15*cm),
    ]

    def kv_table(data, col_widths, hdr_color=H_BG):
        rows = [[B(c, body) for c in data[0]]]
        for row in data[1:]:
            rows.append([B(row[0], body), P(row[1], body)])
        t = Table(rows, colWidths=col_widths)
        t.setStyle(TableStyle([
            ("BACKGROUND",(0,0),(-1,0),hdr_color),
            ("TEXTCOLOR",(0,0),(-1,0),H_FG if hdr_color==H_BG else GOLD),
            ("ROWBACKGROUNDS",(0,1),(-1,-1),[colors.white, ALT]),
            ("GRID",(0,0),(-1,-1),0.4,colors.HexColor("#ccd0ee")),
            ("VALIGN",(0,0),(-1,-1),"TOP"),
            ("TOPPADDING",(0,0),(-1,-1),5),("BOTTOMPADDING",(0,0),(-1,-1),5),
            ("LEFTPADDING",(0,0),(-1,-1),5),
        ]))
        return t

    sol_data = [
        ["\u98ce\u9669\u9879","\u5185\u5bb9"],
        ["\u6700\u5927\u5c3e\u90e8\u98ce\u9669\uff081\uff09","\u7ea2\u6d77\u822a\u7ebf\u4e2d\u65ad\uff08\u6982\u7387 30%\uff09\uff1b\u80e1\u585e\u6b66\u88c5\u5347\u7ea7\u88ad\u6270\uff0c\u4fdd\u9669\u8d39\u66db\u589e50%+\uff0c\u7ed5\u884c\u597d\u671b\u89d2\u589e\u52a07-10\u5929\u822a\u7a0b"],
        ["\u6700\u5927\u5c3e\u90e8\u98ce\u9669\uff082\uff09","\u5b89\u54e5\u62c9\u653f\u7b56\u53d8\u5316\uff08\u6982\u7387 15%\uff09\uff1bOPEC\u51cf\u4ea7\u538b\u529b\u52a0\u5927\uff0c\u5b89\u54e5\u62c9\u653f\u5e9c\u8d22\u653f\u5371\u673a\uff0c\u53ef\u80fd\u8c03\u6574\u8fdb\u53e3\u5173\u7a0e\u6216CNCA\u8981\u6c42"],
        ["\u6700\u5927\u5c3e\u90e8\u98ce\u9669\uff083\uff09","\u6e05\u5173\u969c\u788d\uff08\u6982\u7387 20%\uff09\uff1bCNCA\u529e\u7406\u5ef6\u8bef\u6216\u6587\u4ef6\u9519\u8bef\uff0c\u8d27\u7269\u6d6e\u7559\u6e2f\u53e3\uff0c\u4ed3\u50a8\u8d39$50-100/\u67dc/\u5929"],
        ["\u5bf9\u51a0\u5efa\u8bae","\u822a\u7ebf\u591a\u5143\u5316\uff1a\u540c\u65f6\u8fd0\u8425\u597d\u671b\u89d2\u7ebf\u548c\u5370\u5ea6\u6d0b\u76f4\u8fbe\u7ebf\uff0c\u5206\u6563\u98ce\u9669"],
        ["\u5bf9\u51a0\u5efa\u8bae","\u672c\u5730\u5316\u6e05\u5173\uff1a\u5728\u7f57\u5b89\u8fbe\u8bbe\u7acb\u6e05\u5173\u56e2\u961f\uff0c\u51cf\u5c11\u5bf9\u4ee3\u529e\u673a\u6784\u4f9d\u8d56"],
        ["\u5bf9\u51a0\u5efa\u8bae","\u6c47\u7387\u9501\u5b9a\uff1a\u4e0e\u5ba2\u6237\u7b7e\u8ba2\u4eba\u6c11\u5e01\u6216\u7f8e\u5143\u8ba1\u4ef7\u5408\u540c\uff0c\u89c4\u907f\u5bbd\u7a9d\u6c47\u7387\u98ce\u9669"],
    ]

    rot_data = [
        ["\u673a\u4f1a\u9879","\u5185\u5bb9"],
        ["\u5951\u5229\u7a7a\u95f4\uff081\uff09","\u822a\u8fd0\u4ef7\u5206\u5316\uff1a\u7ea2\u6d77\u822a\u7ebf\u8fd0\u4ef7\u4e0a\u6da820-30%\uff0c\u53ef\u627f\u63a5\u4ece\u7ea2\u6d77\u8f6c\u79fb\u7684\u8d27\u91cf"],
        ["\u5951\u5229\u7a7a\u95f4\uff082\uff09","\u56de\u7a0b\u8d27\u4e0d\u8db3\uff1a\u5b89\u54e5\u62c9\u5bf9\u534e\u51fa\u53e3\u4ee5\u539f\u6cb9\u4e3b\uff08\u6cb9\u8f6e\u8fd0\u8f93\uff09\uff0c\u96c6\u88c5\u7b7e\u56de\u7a0b\u8d27\u9700\u6c42\u671b\u80dc\uff0c\u822a\u8fd0\u4ef7\u6709\u4e0b\u884c\u7a7a\u95f4"],
        ["\u6700\u4f73\u5207\u5165\u65f6\u673a","\u672b\u6765 3-6 \u4e2a\u6708\uff1b\u4e2d\u4e1c\u5c40\u52bf\u53ef\u80fd\u7f13\u548c\uff0c\u822a\u8fd0\u4ef7\u4ece\u9ad8\u70b9\u56de\u843d\uff1b\u5b89\u54e5\u62c9\u653f\u5e9c\u53ef\u80fd\u653e\u5bb3\u8fdb\u53e3\u653f\u7b56\u5237\u6fc0\u7ecf\u6d4e"],
        ["\u5dee\u5f02\u5316\u7ade\u4e89\u4f18\u52bf","\u53cc\u6e05\u80fd\u529b\uff1a\u63d0\u4f9b\u4e2d\u56fd\u51fa\u53e3\u62a5\u5173+\u5b89\u54e5\u62c9\u8fdb\u53e3\u6e05\u5173\u4e00\u7ad9\u5f0f\u670d\u52a1"],
        ["\u5dee\u5f02\u5316\u7ade\u4e89\u4f18\u52bf","CNCA\u4e13\u4e1a\u670d\u52a1\uff1a\u5efa\u7acbCNCA\u5feb\u901f\u529e\u7406\u901a\u9053\uff0c\u627f\u8bfa5\u4e2a\u5de5\u4f5c\u65e5\u5185\u5b8c\u6210\u529e\u7406"],
        ["\u5dee\u5f02\u5316\u7ade\u4e89\u4f18\u52bf","\u672c\u5730\u5316\u670d\u52a1\uff1a\u5728\u7f57\u5b89\u8fbe\u8bbe\u5206\u516c\u53f8\uff0c\u63d0\u4f9b\u76ee\u7684\u6e2f\u62d6\u8f66\u3001\u4ed3\u50a8\u3001\u914d\u9001\u670d\u52a1"],
    ]

    story += [
        P("\U0001f3f9 \u6240\u7f57\u95e8\uff1a\u98ce\u9669\u67b6\u6784\u5e08", sub),
        kv_table(sol_data, [3*cm, 11.2*cm], H_BG),
        Spacer(1, 0.3*cm),
        P("\U0001f3f0 \u7f57\u65af\u8d1d\u5c14\u5fb7\uff1a\u673a\u4f1a\u6316\u6398\u8005", sub),
        kv_table(rot_data, [3*cm, 11.2*cm], ROT_BG),
        Spacer(1, 0.3*cm),
    ]

    story.append(PageBreak())

    # ── 第四章：情景预判 ────────────────────────────────────
    story += [
        P("\u56db\u3001\u60c5\u666f\u9884\u5224\uff08A/B/C\uff09", sec),
        HRFlowable(width="100%", thickness=1, color=ACC, spaceAfter=0.2*cm),
    ]

    scenarios = [
        ["\u60c5\u666f","\u6982\u7387","\u89e6\u53d1\u6761\u4ef6","\u5bf9\u8d27\u4ee3\u4e1a\u52a1\u7684\u5f71\u54cd"],
        ["A. \u4e2d\u4e1c\u5c40\u52bf\u7f13\u548c",
         "40%","\u4f0a\u671f-\u4ee5\u8272\u5217\u8fbe\u6210\u505c\u706b\uff0c\u80e1\u585e\u6b66\u88c5\u505c\u6b62\u88ad\u6270",
         "\u822a\u8fd0\u4ef7\u56de\u843d10-15%\uff0c\u82cf\u4f0a\u58eb\u822a\u7ebf\u6062\u590d\uff0c\u7ade\u4e89\u52a0\u5267\uff0c\u9700\u5feb\u901f\u631b\u5360\u5e02\u573a\u4efd\u989d"],
        ["B. \u4e2d\u4e1c\u5c40\u52bf\u50f5\u6301",
         "45%","\u51b2\u7a81\u6301\u7eed\u4f46\u672a\u5347\u7ea7\uff0c\u7ea2\u6d77\u822a\u7ebf\u7ef4\u6301\u9ad8\u98ce\u9669",
         "\u822a\u8fd0\u4ef7\u7a33\u5b9a\uff0c\u597d\u671b\u89d2\u7ebf\u6210\u4e3a\u4e3b\u6d41\uff0c\u79ef\u6781\u6269\u5927\u5ba2\u6237\u57fa\u7840\uff0c\u63a8\u8350"],
        ["C. \u4e2d\u4e1c\u5c40\u52bf\u5347\u7ea7",
         "15%","\u4f0a\u671f-\u4ee5\u8272\u5217\u5168\u9762\u51b2\u7a81\uff0c\u66fc\u5fb7\u6d77\u5ce1\u88ab\u5c01\u9501",
         "\u822a\u8fd0\u4ef7\u66db\u6da815-30%\uff0c\u4fdd\u9669\u8d39\u7ffb\u500d\uff0c\u9700\u5feb\u901f\u8c03\u6574\u822a\u7ebf\uff0c\u77ed\u671f\u5229\u6da1\u4e0a\u5347\u4f46\u5ba2\u6237\u6d41\u5931\u98ce\u9669\u9ad8"],
    ]

    def srow(row, is_h=False):
        if is_h: return [B(c, body) for c in row]
        styled = []
        for j, c in enumerate(row):
            if j == 1:
                prob = int(c.replace("%",""))
                c2 = T_DN if prob <= 20 else T_UP if prob >= 40 else T_FLAT
                styled.append(P(f"<b><font color='{c2.hexval()}'>{c}</font></b>", body))
            else:
                styled.append(P(c, body))
        return styled

    st = Table(
        [srow(scenarios[0], True)] + [srow(r) for r in scenarios[1:]],
        colWidths=[3.5*cm, 1.2*cm, 4.8*cm, 5.6*cm],
        repeatRows=1
    )
    st.setStyle(TableStyle([
        ("BACKGROUND",(0,0),(-1,0),ACC),
        ("TEXTCOLOR",(0,0),(-1,0),H_FG),
        ("ROWBACKGROUNDS",(0,1),(-1,-1),[colors.white, ALT]),
        ("GRID",(0,0),(-1,-1),0.4,colors.HexColor("#ccd0ee")),
        ("VALIGN",(0,0),(-1,-1),"TOP"),
        ("TOPPADDING",(0,0),(-1,-1),5),("BOTTOMPADDING",(0,0),(-1,-1),5),
        ("LEFTPADDING",(0,0),(-1,-1),5),
        ("ALIGN",(1,1),(1,-1),"CENTER"),
    ]))
    story.append(st)
    story.append(Spacer(1, 0.3*cm))

    # ── 第五章：行动建议 ────────────────────────────────────
    story += [
        P("\u4e94\u3001\u8d27\u4ee3\u4e1a\u52a1\u884c\u52a8\u5efa\u8bae", sec),
        HRFlowable(width="100%", thickness=1, color=ACC, spaceAfter=0.2*cm),
    ]

    actions = [
        ["\u4f18\u5148\u7ea7","\u65f6\u95f4","\u884c\u52a8\u9879","\u80cc\u666f"],
        ["\U0001f7e2 \u9ad8","\u7acb\u5373\uff081\u4e2a\u6708\u5185\uff09",
         "\u516c\u53f8\u8c03\u7814\uff1a\u8c03\u7814\u4e2d\u56fd-\u5b89\u54e5\u62c9\u8d27\u8f66\u5e02\u573a\uff0c\u8bc6\u522b\u4e3b\u8981\u8d27\u4e3b\uff08\u673a\u68b0\u8bbe\u5907\u3001\u5efa\u6750\u3001\u6d88\u8d39\u54c1\u51fa\u53e3\u5546\uff09\u548c\u7ade\u4e89\u5bf9\u624b\uff08\u6df1\u573a\u4e45\u9f0e\u3001\u9e3f\u6d77\u8d27\u4ee3\u3001\u9752\u5c9b\u767e\u4e8b\u7b49\uff09\n\u5408\u4f5c\u4f19\u4f34\u7b5b\u9009\uff1a\u4f18\u5148\u8003\u865c\u5728\u7f57\u5b89\u8fbe\u6709\u5206\u516c\u53f8\u7684\u5408\u4f5c\u4f19\u4f34\uff0c\u4f18\u5148\u8003\u865c\u5728\u7f57\u5b89\u8fbe\u6709\u5206\u516c\u53f8\u640f\u6258\u5173\u7cfb\u7684\u4f01\u4e1a",
         "\u9996\u6b21\u63a5\u89e6\uff0c\u5efa\u7acb\u4fe1\u606f\u5e93\u5e95"],
        ["\U0001f7e2 \u9ad8","\u7acb\u5373\uff081\u4e2a\u6708\u5185\uff09",
         "\u822a\u7ebf\u65b9\u6848\u8bbe\u8ba1\uff1a\u8bbe\u8ba1\u201c\u597d\u671b\u89d2\u7a33\u5b9a\u7ebf\u201d\uff0835-40\u5929\uff09\u548c\u201c\u5370\u5ea6\u6d0b\u5feb\u6377\u7ebf\u201d\uff0830-35\u5929\uff09\u4e24\u79cd\u65b9\u6848\uff0c\u83b7\u53d6\u8239\u4e1c\u62a5\u4ef7\nCNCA\u80fd\u529b\u5efa\u8bbe\uff1a\u5efa\u7acbCNCA\u529e\u7406\u6d41\u7a0b\uff0c\u57f9\u8bad\u64cd\u4f5c\u4eba\u5458\uff0c\u4e89\u53d65\u4e2a\u5de5\u4f5c\u65e5\u5185\u5b8c\u6210\u529e\u7406",
         "\u4e24\u7ebf\u8f93\u5165\u6d4e\u6d41\u7a0b\uff0c\u786e\u4fddCNCA\u901f\u5ea6"],
        ["\ud83d\udfe1 \u4e2d","\u77ed\u671f\uff081-3\u4e2a\u6708\uff09",
         "\u5ba2\u6237\u5f00\u53d1\uff1a\u53c2\u52a0\u4e2d\u56fd-\u975e\u6d32\u8d38\u6613\u5c55\u4f1a\uff0c\u63a5\u89e6\u6f5c\u5728\u5ba2\u6237\uff0c\u91cd\u70b9\u63a8\u8386\u201c\u53cc\u6e05+CNCA\u4e00\u7ad9\u5f0f\u670d\u52a1\u201d\n\u8fd0\u4ef7\u9501\u5b9a\uff1a\u4e0e\u8239\u4e1c\u7b7e\u8ba2<b>3-6\u4e2a\u6708\u822a\u8fd0\u4ef7\u534f\u8bae</b>\uff0c\u9501\u5b9a$2200-2800/FEU\u533a\u95f4\uff0c\u89c4\u907f\u77ed\u671f\u6ce2\u52a8\n\u4fdd\u9669\u914d\u7f6e\uff1a\u6295\u4fdd\u201c\u6218\u4e89\u9669\u201d\u548c\u201c\u7f3a\u5de5\u9669\u201d\uff0c\u8986\u76d6\u6781\u7aef\u60c5\u666f\u635f\u5931\uff0c\u4fdd\u8d39\u7ea2$50-80/\u67dc",
         "\u6700\u91cd\u8981\u7684\u7ed3\u7b97\u6761\u6b65\uff0c\u786e\u4fdd\u5229\u6da1\u5e73\u53f0"],
        ["\ud83d\udfe1 \u4e2d","\u77ed\u671f\uff081-3\u4e2a\u6708\uff09",
         "\u672c\u5730\u5316\u5c55\u5f00\uff1a\u8003\u5bdf\u7f57\u5b89\u8fbe\u6e2f\uff0c\u8bc4\u4f30\u8bbe\u7acb\u5206\u516c\u53f8\u7684\u53ef\u884c\u6027\uff0c\u4f18\u5148\u62db\u8058\u6709\u5b89\u54e5\u62c9\u6e05\u5173\u7ecf\u9a8c\u7684\u672c\u5730\u5458\u5de5\n\u8f6c\u53e3\u5f00\u53d1\uff1a\u5b9a\u5411\u673a\u68b0\u8bbe\u5907\u3001\u5efa\u6750\u3001\u6d88\u8d39\u54c1\u7b49\u4e3b\u6d41\u8d27\u7c7b\uff0c\u8fd9\u4e9b\u8d27\u7c7b\u5bf9\u5b89\u54e5\u62c9\u6765\u8bf4\u662f\u786e\u5b9a\u9700\u6c42\u589e\u957f\u7684",
         "\u7ecf\u9a8c\u548c\u5ba2\u6237\u5173\u7cfb\u540c\u65f6\u5efa\u8bae"],
        ["\ud83d\udfe2 \u4f4e","\u4e2d\u671f\uff083-6\u4e2a\u6708\uff09",
         "\u5206\u516c\u53f8\u8bbe\u7acb\uff1a\u5728\u7f57\u5b89\u8fbe\u8bbe\u7acb\u5206\u516c\u53f8\uff0c\u63d0\u4f9b\u76ee\u7684\u6e2f\u62d6\u8f66\u3001\u4ed3\u50a8\u3001\u914d\u9001\u670d\u52a1\uff0c\u63d0\u5347\u672c\u5730\u5316\u670d\u52a1\u80fd\u529b\n\u6570\u5b57\u5316\u7cfb\u7edf\uff1a\u5efa\u7acb\u8d27\u8fd0\u8ffd\u8e2a\u7cfb\u7edf\uff0c\u5b9e\u65f6\u66f4\u65b0\u8d27\u7269\u72b6\u6001\uff0c\u63d0\u5347\u5ba2\u6237\u4f53\u9a8c\n\u822a\u7ebf\u6269\u5c55\uff1a\u8bc4\u4f30\u6269\u5c55\u81f3\u5361\u5bbe\u8fbe\u6e2f\u3001\u7eb1\u7c7b\u5382\u6c83\u5c14\u7ebd\u65af\u6e2f\u7684\u53ef\u884c\u6027\uff0c\u6269\u5927\u670d\u52a1\u8303\u56f4",
         "\u6839\u57fa\u7840\u5411\u7b51\u9886\u5730\u54c1\u724c\u8f6c\u578b"],
    ]

    def arow(row, is_h=False):
        if is_h: return [B(c, body) for c in row]
        return [P(c, body) for c in row]

    at = Table(
        [arow(actions[0], True)] + [arow(r) for r in actions[1:]],
        colWidths=[1.8*cm, 2.2*cm, 6.2*cm, 3.9*cm],
        repeatRows=1
    )
    at.setStyle(TableStyle([
        ("BACKGROUND",(0,0),(-1,0),ACC),
        ("TEXTCOLOR",(0,0),(-1,0),H_FG),
        ("ROWBACKGROUNDS",(0,1),(-1,-1),[colors.white, ALT]),
        ("GRID",(0,0),(-1,-1),0.4,colors.HexColor("#ccd0ee")),
        ("VALIGN",(0,0),(-1,-1),"TOP"),
        ("TOPPADDING",(0,0),(-1,-1),5),("BOTTOMPADDING",(0,0),(-1,-1),5),
        ("LEFTPADDING",(0,0),(-1,-1),5),
    ]))
    story.append(at)
    story.append(Spacer(1, 0.3*cm))

    # ── 第六章：运价成本参考 ─────────────────────────────────
    story += [
        P("\u516d\u3001\u822a\u8fd0\u4e0e\u6210\u672c\u53c2\u8003", sec),
        HRFlowable(width="100%", thickness=1, color=ACC, spaceAfter=0.2*cm),
    ]

    freight = [
        ["\u822a\u7ebf","\u5f53\u524d\u8fd0\u4ef7\u533a\u95f4","3\u4e2a\u6708\u9884\u6d4b","6\u4e2a\u6708\u9884\u6d4b","\u5907\u6ce8"],
        ["\u4e2d\u56fd\u2192\u7f57\u5b89\u8fbe\uff08\u597d\u671b\u89d2\u7ebf\uff09","$2500-3000/FEU","$2200-2800/FEU","$2000-2500/FEU","\u7a33\u5b9a\u53ef\u9760\uff0c\u63a8\u8350"],
        ["\u4e2d\u56fd\u2192\u7f57\u5b89\u8fbe\uff08\u5370\u5ea6\u6d0b\u76f4\u8fbe\uff09","$2200-2800/FEU","$2000-2500/FEU","$1800-2300/FEU","\u6548\u7387\u6700\u4f18\uff0c\u63a8\u8350"],
        ["\u4e2d\u56fd\u2192\u5361\u5bbe\u8fbe","$2800-3500/FEU","$2500-3000/FEU","$2300-3000/FEU","\u541e\u5408\u91cf\u5c0f\uff0c\u5099\u9009"],
        ["CNCA\u529e\u7406\u8d39\u7528","$150-200/\u7968","$150-200/\u7968","$150-200/\u7968","\u56fa\u5b9a\u8d39\u7528"],
        ["\u5b89\u54e5\u62c9\u6e2f\u6742\u8d39","$300-500/\u67dc","$300-500/\u67dc","$300-500/\u67dc","THC\u3001DOC\u3001CIS\u7b49"],
        ["\u6e05\u5173\u4ee3\u7406\u8d39","$200-400/\u7968","$200-400/\u7968","$200-400/\u7968","\u5efa\u8bae\u672c\u5730\u5316\u540e\u964d\u4f4e"],
    ]

    def frow(row, is_h=False):
        if is_h: return [B(c, body) for c in row]
        styled = []
        for j, c in enumerate(row):
            if j in [1, 2, 3]:
                styled.append(P(f"<b>{c}</b>", body))
            else:
                styled.append(P(c, body))
        return styled

    ft = Table(
        [frow(freight[0], True)] + [frow(r) for r in freight[1:]],
        colWidths=[4*cm, 3*cm, 3*cm, 3*cm, 2.5*cm],
        repeatRows=1
    )
    ft.setStyle(TableStyle([
        ("BACKGROUND",(0,0),(-1,0),ACC),
        ("TEXTCOLOR",(0,0),(-1,0),H_FG),
        ("ROWBACKGROUNDS",(0,1),(-1,-1),[colors.white, ALT]),
        ("GRID",(0,0),(-1,-1),0.4,colors.HexColor("#ccd0ee")),
        ("VALIGN",(0,0),(-1,-1),"TOP"),
        ("TOPPADDING",(0,0),(-1,-1),4),("BOTTOMPADDING",(0,0),(-1,-1),4),
        ("LEFTPADDING",(0,0),(-1,-1),5),
    ]))
    story.append(ft)
    story.append(Spacer(1, 0.4*cm))

    # ── 页脚 ────────────────────────────────────────────────
    story += [
        HRFlowable(width="100%", thickness=0.5, color=colors.HexColor("#ccd0ee"), spaceAfter=0.15*cm),
        P("Global Intelligence v2.0 | \u56e2\u961f\u5236\uff08\u5730\u8fb9\u6218\u7565+\u7ecf\u6d4e\u8d44\u6e90+\u5b89\u5168\u519b\u4e8b+\u821e\u60c5\u4e2d\u56fd\uff09| \u9694\u79bb\u8c03\u5ea6\u5458 | \u4f0a\u8fea\u65af\u603b\u8c03\u5ea6 | 2026-04-18", small),
    ]

    doc.build(story)
    print(f"\u2705 PDF \u5df2\u751f\u6210\uff1a{OUTPUT}")

if __name__ == "__main__":
    build_pdf()
