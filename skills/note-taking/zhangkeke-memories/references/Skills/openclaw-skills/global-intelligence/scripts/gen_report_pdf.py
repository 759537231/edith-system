#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Global Intelligence 中东局势分析报告 PDF"""

import sys, os
# Hermes: pdf scripts are in skill references
# sys.path.insert(0, os.path.expanduser("~/Library/Application Support/QClaw/openclaw/config/skills/pdf/scripts"))
from setup_chinese_pdf import setup_chinese_pdf

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    HRFlowable, PageBreak
)
from reportlab.lib.units import cm

OUTPUT = os.path.expanduser("~/Desktop/中东局势分析报告_GI_20260417.pdf")

def P(text, style):
    return Paragraph(text, style)

def B(text, style):
    """Bold wrapper: use HTML <b> tag so font doesn't need Bold variant"""
    return Paragraph(f"<b>{text}</b>", style)

def build_pdf():
    cn_font, styles = setup_chinese_pdf()

    body = ParagraphStyle("Body", parent=styles["Normal"],
        fontSize=10, leading=16, spaceAfter=3)
    small = ParagraphStyle("Small", parent=styles["Normal"],
        fontSize=8.5, leading=12, textColor=colors.HexColor("#555577"))
    cover_title = ParagraphStyle("CT", parent=styles["Title"],
        fontSize=24, leading=30, alignment=TA_CENTER,
        textColor=colors.HexColor("#1a1a2e"))
    cover_sub = ParagraphStyle("CS", parent=styles["Normal"],
        fontSize=13, leading=18, alignment=TA_CENTER,
        textColor=colors.HexColor("#4a4a6a"))
    cover_meta = ParagraphStyle("CM", parent=styles["Normal"],
        fontSize=9.5, leading=14, alignment=TA_CENTER,
        textColor=colors.HexColor("#8888aa"))
    sec = ParagraphStyle("Sec", parent=styles["Heading1"],
        fontSize=14, leading=20, spaceBefore=12, spaceAfter=4,
        textColor=colors.HexColor("#1a1a2e"))
    sub = ParagraphStyle("Sub", parent=styles["Heading2"],
        fontSize=11.5, leading=16, spaceBefore=8, spaceAfter=3,
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

    def cp(text):
        v = int(text.replace("%",""))
        c = T_UP if v >= 77 else T_DN if v <= 70 else colors.HexColor("#f39c12")
        return P(f"<b><font color='{c.hexval()}'>{text}</font></b>", body)

    doc = SimpleDocTemplate(
        OUTPUT, pagesize=A4,
        leftMargin=1.8*cm, rightMargin=1.8*cm,
        topMargin=2*cm, bottomMargin=2*cm,
        title="\u4e2d\u4e1c\u5c40\u52bf\u5206\u6790\u62a5\u544a"
    )
    story = []

    # ── 封面 ────────────────────────────────────────────────
    story += [
        Spacer(1, 1.5*cm),
        P("\U0001f30d \u5168\u7403\u5c40\u52bf\u5206\u6790\u62a5\u544a", cover_title),
        Spacer(1, 0.3*cm),
        P("\u4e2d\u4e1c\u5c40\u52bf \u00b7 \u672a\u6765 1/3/6 \u4e2a\u6708\u6df1\u5ea6\u5206\u6790", cover_sub),
        Spacer(1, 0.3*cm),
        HRFlowable(width="55%", thickness=2, color=GOLD, spaceAfter=0.3*cm),
        P("2026-04-17 11:50 CST  |  \u9ad8\u4f18\u5148\u7ea7  |  8\u7ef4\u4e13\u5bb6\u5e76\u884c\u5206\u6790", cover_meta),
        P("Hermes delegate_task  |  \u4f0a\u8fea\u65af\u603b\u8c03\u5ea6", cover_meta),
        Spacer(1, 0.5*cm),
        P("\U0001f30f Atlas  \U0001f4b0 Plutus  \U0001f6e1 Sentinel  \u26a1 Tesla  \u26f3 Prometheus  \U0001f4e2 Echo  \U0001f4dc Chronos  \U0001f409 Dragon", cover_meta),
        PageBreak(),
    ]

    # ── 第一章：情报摘要 ────────────────────────────────────
    story += [
        P("\u4e00\u3001\u60c5\u62a5\u6458\u8981", sec),
        HRFlowable(width="100%", thickness=1, color=ACC, spaceAfter=0.2*cm),
        P("\u6765\u6e90\uff1aweb_search \u5b9e\u65f6\u641c\u7d22\uff082026.4.17\uff09", small),
        Spacer(1, 0.2*cm),
    ]

    intel = [
        ["#","\u6807\u9898","\u6765\u6e90","\u65e5\u671f"],
        ["1","\u738b\u6bc5\u518d\u8c08\u4e2d\u4e1c\u5c40\u52bf\uff0c\u91cd\u7533\u5bf9\u8bdd\u534f\u5546\u53cd\u5bf9\u6b66\u529b","\u4f01\u9e45\u53f7","04-17"],
        ["2","\u4f0a\u671f\u542f\u7528\u66ff\u4ee3\u6e2f\u53e3\u7ed5\u8fc7\u970d\u5c14\u6728\u5179\u5c01\u9501\uff08\u9ad8\u5ea6\u5173\u952e\u4fe1\u53f7\uff09","\u4e1c\u65b9\u8d22\u5bcc\u7f51","04-15"],
        ["3","\u4ee5\u8272\u5217\u60c5\u62a5\uff1a\u4f0a\u671f\u5343\u4f59\u679a\u5f39\u9053\u5bfc\u5f39\uff08\u6d41\u661f-3\u3001\u6ce5\u77f3-2\uff09\u8986\u76d6\u5168\u5883","\u4f01\u9e45\u53f7","04-15"],
        ["4","\u5916\u4ea4\u90e8\uff1a\u7f8e\u65b9\u5b9a\u5411\u5c01\u9501\u5371\u9669\u4e0d\u8d1f\u8d23","\u4e2d\u56fd\u7f51","04-14"],
        ["5","\u4e2d\u4e1c\u5c40\u52bf\u4ee4\u6b27\u6d32\u591a\u9886\u57df\u627f\u538b\uff1a\u80fd\u6e90+\u91d1\u878d+\u519c\u4e1a\u4f9b\u5e94\u94fe","\u4f01\u9e45\u53f7","04-16"],
        ["6","\u571f\u8036\u5179\u65c5\u6e38\u4e1a\u9047\u4ea7\u5012\u6625\u5bd2\uff0c\u56fd\u9645\u6e38\u5ba2\u51fa\u884c\u610f\u613f\u4e0b\u964d","\u65b0\u534e\u7f51","04-15"],
        ["7","\u7f8e\u8054\u50a8\uff1a\u5c06\u7f8e\u4ee5\u4f0a\u51b2\u7a81\u5217\u4e3a\u7f8e\u56fd\u7ecf\u6d4e\u4e0d\u786e\u5b9a\u6027\u6765\u6e90","\u4f01\u9e45\u53f7","04-16"],
        ["8","4\u670815\u65e5\u8d77\u5c40\u52bf\u77ed\u6682\u5598\u6c14\uff0c\u9ed1\u8272\u5546\u54c1\u4f4e\u4f4d\u53cd\u6da8","\u65b0\u6d6a\u8d22\u7ecf","04-15"],
        ["9","\u80e1\u585e\u6b66\u88c5\u4ecd\u5728\u7ea2\u6d77\u6d3b\u52a8\uff0c\u4e9a\u4e01\u6e7e\u822a\u8fd0\u4fdd\u9669\u8d39\u4e0a\u534715%","\u7efc\u5408","\u6708"],
    ]

    def make_table(data, col_widths):
        rows = []
        for i, row in enumerate(data):
            if i == 0:
                rows.append([B(c, body) for c in row])
            else:
                rows.append([P(c, body) for c in row])
        t = Table(rows, colWidths=col_widths, repeatRows=1)
        t.setStyle(TableStyle([
            ("BACKGROUND",    (0,0),(-1,0), H_BG),
            ("TEXTCOLOR",    (0,0),(-1,0), H_FG),
            ("ROWBACKGROUNDS",(0,1),(-1,-1),[colors.white, ALT]),
            ("GRID",         (0,0),(-1,-1), 0.4, colors.HexColor("#ccd0ee")),
            ("VALIGN",        (0,0),(-1,-1),"TOP"),
            ("TOPPADDING",   (0,0),(-1,-1), 4),
            ("BOTTOMPADDING",(0,0),(-1,-1), 4),
            ("LEFTPADDING",  (0,0),(-1,-1), 5),
        ]))
        return t

    story.append(make_table(intel, [0.5*cm, 9.8*cm, 2.4*cm, 1.4*cm]))
    story.append(Spacer(1, 0.4*cm))

    # ── 第二章：8维专家扫描 ─────────────────────────────────
    story += [
        P("\u4e8c\u3001\u516b\u7ef4\u4e13\u5bb6\u626b\u63cf", sec),
        HRFlowable(width="100%", thickness=1, color=ACC, spaceAfter=0.2*cm),
        P("\u91c7\u7528 Hermes delegate_task \u5e76\u884c\u63a8\u7406\uff0c\u6bcf\u4e2a\u4e13\u5bb6\u57fa\u4e8e\u72ec\u7acb\u60c5\u62a5\u5206\u6790\u3002", small),
        Spacer(1, 0.2*cm),
    ]

    experts = [
        ["\u7ef4\u5ea6","\u4e13\u5bb6","\u6838\u5fc3\u5224\u65ad\u6458\u8981","\u8d8b\u52bf","\u7f6e\u4fe1"],
        ["\U0001f5fa \u5730\u8fb9","Atlas",
         "\u9ad8\u70c8\u5ea6\u4ef7\u6301\u624d\u521d\u5f00\u59cb\uff0c\u5411\u4f4e\u70c8\u5ea6\u6301\u4e45\u6218\u8fc7\u6e21\u3002\u4f0a\u671f\u6218\u7565\u8010\u529b\u8d85\u51fa\u9884\u671f\u3002",
         "\u2192\u964d\u6e29","75%"],
        ["\U0001f4b0 \u7ecf\u6d4e","Plutus",
         "1700\u4e07\u6876/\u65e5\u970d\u5c14\u6728\u5179\u662f\u5168\u7403\u4e3b\u52a8\u8109\u3002\u4f0a\u671f\u66ff\u4ee3\u6e2f\u53e3\u662f\u4e3b\u52a8\u5e03\u5c40\uff0c\u975e\u88ab\u52a8\u7ed5\u884c\u3002$72/\u6876\u4f4e\u4f4d\u7f13\u51b2\u6709\u9650\u3002",
         "\u2197\u5347\u6e29","78%"],
        ["\U0001f6e1 \u5b89\u5168","Sentinel",
         "\u6050\u60e7\u5e73\u8861\u4f46\u5931\u8861\u4e34\u754c\u3002\u94c1\u7a7a\u9762\u5bf9\u996d\u548c\u653b\u51fb\u62e3\u6226\u5931\u6548\u98ce\u9669 15-30%\u3002",
         "\u2192\u964d\u6e29","72%"],
        ["\u26a1 \u79d1\u6280","Tesla",
         "\u4f0a\u671f\u5bfc\u5f39\u5927\u91cf\u5c01\u8868\u5f00\u59cb\u542f\u52a8\u3002\u6280\u672f\u5c01\u9501\u6548\u679c\u663e\u73b0\uff0cAI\u7cbe\u786e\u5236\u5bfc\u4f18\u52bf\u6301\u7eed\u6269\u5927\u3002",
         "\u2197\u5347\u6e29","78%"],
        ["\u26f3 \u80fd\u6e90","Prometheus",
         "\u77ed\u671f\u964d\u6e29\u4f46\u7ed3\u6784\u98ce\u9669\u672a\u89e3\u9664\u30023\u4e2a\u6708\u540e\u590f\u5b63\u9ad8\u5cf0+\u6838\u8ba8\u8bba\u5347\u6e29\uff0c\u80fd\u6e90\u4ef7\u683c\u627f\u538b\u3002",
         "\u5148\u2193\u540e\u2191","75%"],
        ["\U0001f4e2 \u821e\u60c5","Echo",
         "\u53d1\u5e03\u771f\u7a7a\u671f\u5f00\u542f\uff0c\u5404\u65b9\u4e89\u5949\u8c01\u8d62\u4e86\u5b9a\u4e49\u6743\u3002",
         "\u2192\u964d\u6e29","65%"],
        ["\U0001f4dc \u5386\u53f2","Chronos",
         "\u4f0a\u671f\u73b0\u653f\u6743\u662f\u552f\u4e00\u80fd\u62bc\u5236\u6781\u7aef\u6d6a\u6f6e\u5236\u8861\u529b\u91cf\u3002\u653f\u6743\u66f4\u8fc8\u5fc5\u7136\u5236\u9020\u66f4\u60e8\u70c8\u66ff\u4ee3\u8005\u3002",
         "\u2197\u5347\u6e29","76%"],
        ["\U0001f409 \u4e2d\u56fd","Dragon",
         "\u4e09\u65b9\u5e73\u8861\u662f\u7a00\u7f3a\u8d44\u4ea7\u3002\u5916\u4ea4\u6551\u70b9\u9700\u66f4\u6709\u7259\u9f7f\uff0c\u80fd\u6e90\u5b89\u5168\u9700\u5907\u9009\u65b9\u6848\u3002",
         "\u2197\u5347\u6e29","78%"],
    ]

    def exp_row(row):
        if row == experts[0]:
            return [B(c, body) for c in row]
        styled = []
        for j, c in enumerate(row):
            if j == 3: styled.append(tp(c))
            elif j == 4: styled.append(cp(c))
            else: styled.append(P(c, body))
        return styled

    et = Table(
        [exp_row(experts[0])] + [exp_row(r) for r in experts[1:]],
        colWidths=[1.2*cm, 2.2*cm, 7.8*cm, 1.6*cm, 1.3*cm],
        repeatRows=1
    )
    et.setStyle(TableStyle([
        ("BACKGROUND",    (0,0),(-1,0), ACC),
        ("TEXTCOLOR",    (0,0),(-1,0), H_FG),
        ("ROWBACKGROUNDS",(0,1),(-1,-1),[colors.white, ALT]),
        ("GRID",         (0,0),(-1,-1), 0.4, colors.HexColor("#ccd0ee")),
        ("VALIGN",        (0,0),(-1,-1),"TOP"),
        ("TOPPADDING",   (0,0),(-1,-1), 4),
        ("BOTTOMPADDING",(0,0),(-1,-1), 4),
        ("LEFTPADDING",  (0,0),(-1,-1), 5),
        ("ALIGN",        (3,1),(4,-1),"CENTER"),
    ]))
    story.append(et)
    story.append(Spacer(1, 0.25*cm))

    # 趋势汇总
    sum_t = Table([[
        B("\u8d8b\u52bf\u6c47\u603b", body),
        P("\u2197\u5347\u6e29\u00d74\uff08\u7ecf\u6d4e/\u79d1\u6280/\u5386\u53f2/\u4e2d\u56fd\uff09", body),
        P("\u2192\u964d\u6e29\u00d74\uff08\u5730\u8fb9/\u5b89\u5168/\u80fd\u6e90/\u821e\u60c5\uff09", body),
        P("\u6574\u4f53\uff1a\u52bf\u5747\u529b\u6545\uff0c\u77ed\u671f\u6280\u672f\u5598\u6c14 vs \u4e2d\u671f\u7ed3\u6784\u538b\u529b", body),
    ]], colWidths=[1.8*cm, 4.5*cm, 4.5*cm, 3.3*cm])
    sum_t.setStyle(TableStyle([
        ("BACKGROUND",(0,0),(-1,-1), colors.HexColor("#f8f9ff")),
        ("GRID",(0,0),(-1,-1),0.5,colors.HexColor("#ccd0ee")),
        ("TOPPADDING",(0,0),(-1,-1),5),("BOTTOMPADDING",(0,0),(-1,-1),5),
        ("LEFTPADDING",(0,0),(-1,-1),5),
    ]))
    story.append(sum_t)
    story.append(Spacer(1, 0.4*cm))

    # ── 第三章：时间分层 ────────────────────────────────────
    story += [
        P("\u4e09\u3001\u65f6\u95f4\u5206\u5c42\uff1a\u672a\u6765\u8d8b\u52bf", sec),
        HRFlowable(width="100%", thickness=1, color=ACC, spaceAfter=0.15*cm),
    ]

    def time_table(data, col_widths, header_color=ACC):
        rows = []
        for i, row in enumerate(data):
            if i == 0:
                rows.append([B(c, body) for c in row])
            else:
                styled = []
                for j, c in enumerate(row):
                    if j == 1: styled.append(tp(c))
                    else: styled.append(P(c, body))
                rows.append(styled)
        t = Table(rows, colWidths=col_widths, repeatRows=1)
        t.setStyle(TableStyle([
            ("BACKGROUND",(0,0),(-1,0),header_color),
            ("TEXTCOLOR",(0,0),(-1,0),H_FG),
            ("ROWBACKGROUNDS",(0,1),(-1,-1),[colors.white, ALT]),
            ("GRID",(0,0),(-1,-1),0.4,colors.HexColor("#ccd0ee")),
            ("VALIGN",(0,0),(-1,-1),"TOP"),
            ("TOPPADDING",(0,0),(-1,-1),4),("BOTTOMPADDING",(0,0),(-1,-1),4),
            ("LEFTPADDING",(0,0),(-1,-1),5),
        ]))
        return t

    # 1个月
    story += [P("\U0001f4c5 \u672b\u6765 1 \u4e2a\u6708\uff082026.4.17\u20135.17\uff09", sub)]
    m1 = [
        ["\u7ef4\u5ea6","\u8d8b\u52bf","\u5177\u4f53\u5224\u65ad"],
        ["\u6574\u4f53\u5c40\u52bf","\u2192\u964d\u6e29","\u6280\u672f\u6027\u505c\u706b\u6846\u67b6\u5927\u6982\u7387\u8fbe\u6210\uff0c\u4e09\u6761\u7ebf\uff08\u6838\u8bbe\u65bd/\u7ea2\u6d77/\u4ee3\u7406\u6b66\u88c5\uff09\u6697\u4e2d\u535a\u5f08\u6301\u7eed"],
        ["\u80fd\u6e90\u4ef7\u683c","\u2192\u5e73\u7a33","WTI $68-78\u533a\u95f4\u8d85\u632f\uff1b\u4f0a\u671f\u51fa\u53e3\u7ef4\u6301 110-130\u4e07\u6876/\u5929\uff1b\u6682\u65e0\u65b0\u589e\u91cd\u5927\u4e2d\u65ad"],
        ["\u5b89\u5168\u5f62\u52bf","\u2192\u964d\u6e29","\u6bcf\u5468\u4e0d\u8d85\u8fc7 3 \u6b21\u6709\u9650\u8bd5\u63a2\u6027\u4ea4\u706b\uff08\u65e0\u4eba\u673a/\u706b\u7b38\u5f39\uff09\uff0c\u6574\u4f53\u4f4e\u6e29\u6162\u70e7"],
        ["\u5e02\u573a\u60c5\u7eea","\u2192\u5e73\u7a33","\u9ed1\u8272\u5546\u54c1\u4f4e\u4f4d\u53cd\u6da8\u662f\u5598\u6c14\u4fe1\u53f7\uff0c\u975e\u7ed3\u6784\u6027\u7f13\u548c\uff1b\u4e0b\u65ec\u4ee5\u8272\u5217\u884c\u52a8\u5347\u7ea7\u6982\u7387\u4ecd\u5b58"],
    ]
    story.append(time_table(m1, [2*cm, 1.8*cm, 10.4*cm]))
    story.append(P("\u26a0 \u6700\u5927\u98ce\u9669\uff1a\u4ee5\u8272\u5217 F-35I \u90e8\u7f72\u5b8c\u6210 + \u7f8e\u65b9\u518d\u52a0\u7801 \u2192 \u6cb9\u4ef7\u7ebf\u6bb5\u6025\u6da8 10-15%", small))
    story.append(Spacer(1, 0.25*cm))

    # 3个月
    story += [P("\U0001f4c5 \u672b\u6765 3 \u4e2a\u6708\uff085-8\u6708\uff09 \u2014 \u9ad8\u5371\u671f", sub)]
    m3 = [
        ["\u7ef4\u5ea6","\u8d8b\u52bf","\u5177\u4f53\u5224\u65ad"],
        ["\u6574\u4f53\u5c40\u52bf","\u2197\u5347\u6e29","\u590f\u5b63\u53d1\u7535\u9ad8\u5cf0\u6765\u4e34\uff1b\u4ee5\u8272\u5217\u5bf9\u4f0a\u671f\u6838\u8bbe\u65bd\u6253\u51fb\u8ba8\u8bba\u5347\u6e29\uff1b\u78b0\u649e\u7a81\u7834\u5f53\u524d\u9608\u503c"],
        ["\u80fd\u6e90\u4ef7\u683c","\u2197\u5347\u6e29","WTI \u7a81\u7834$90\u6982\u7387 55%+\uff1b\u6b27\u6d32\u5929\u7136\u6c14\uff08TTF\uff09\u4ece\u4f4e\u4f4d\u56de\u5347 30-40%\uff1b\u5e93\u5b58\u8fdb\u5165\u6d88\u8017\u5468\u671f"],
        ["\u5b89\u5168\u5f62\u52bf","\u2197\u5347\u6e29","\u4f0a\u671f\u66ff\u4ee3\u7269\u6d41\u901a\u9053\u521d\u6b65\u8fd0\u8f6c\u540e\u7acb\u573a\u8d8b\u5f3a\u786e\uff0c\u4ee5\u8272\u5217\u52a0\u5927\u7a7a\u88ad\uff0c\u8fdb\u5165\u6e29\u6218\u533a\u95f4"],
        ["\u7f8e\u8054\u50a8\u653f\u7b56","\u2192\u50f5\u6301","\u964d\u606f\u7a97\u53e3\u63a8\u8fdf\u81f3 2026\u5e74\u672b\uff0c\u7f8e\u5029 10Y \u2192 4.8-5.2%\uff0c\u4fe1\u7528\u5229\u5dee\u6269\u5927"],
    ]
    story.append(time_table(m3, [2*cm, 1.8*cm, 10.4*cm], header_color=WARN))
    story.append(P("\U0001f534 \u5173\u952e\u98ce\u9669\u7a97\u53e3\uff1a6-8\u6708\uff0c\u4f0a\u671f\u94d0\u6d53\u7f29\u6db2\u5ea6\u9060\u8fd1\u6b66\u5668\u7ea7 \u2192 \u5404\u65b9\u88ab\u8fbb\u64c5\u724c\u6982\u7387\u4e0a\u5347", small))
    story.append(Spacer(1, 0.25*cm))

    # 6个月
    story += [P("\U0001f4c5 \u672b\u6765 6 \u4e2a\u6708\uff088-10\u6708\uff09 \u2014 \u60c5\u666f\u5206\u5316", sub)]
    m6 = [
        ["\u60c5\u666f","\u6982\u7387","\u8d8b\u52bf","\u5173\u952e\u6761\u4ef6"],
        ["A. \u5916\u4ea4\u6551\u70b9\u6210\u529f","35%","\u2192\u964d\u6e29 \u6cb9\u4ef7\u56de\u843d$75\uff0c\u5168\u7403\u98ce\u9669\u504f\u597d\u4fee\u590d","\u52a0\u6c99\u505c\u706b\u7a97\u53e3\u51fa\u73b0\uff0c\u7f8e\u4f0a\u5bf9\u8bdd\u6e20\u9053\u6fc0\u6d3b"],
        ["B. \u4f4e\u70c8\u5ea6\u50f5\u6301\uff08\u57fa\u51c6\uff09","40%","\u2192 \u6e29\u716e\u9752\u86f9\uff0c\u4ef7\u683c\u9ad8\u4f4d\u8fd0\u884c","\u505c\u706b\u6846\u67b6\u52ab\u5f3f\u7ef4\u6301\uff0c\u5404\u65b9\u6697\u4e2d\u535a\u5f08\u6301\u7eed"],
        ["C. \u970d\u5c14\u6728\u5179\u5b9e\u8d28\u5c01\u9501","25%","\u2191 \u6cb9\u4ef7$100-130\uff0cSWIFT\u5347\u7ea7\uff0c\u4fe1\u7528\u5e02\u573a\u5c40\u90e8\u6d41\u52a8\u67af\u7edd","\u6838\u4e34\u754c\u64c5\u724c\uff0c\u7f8e\u4ee5\u519b\u4e8b\u900f\u9879\u6982\u7387\u5347\u81f3 40-50%"],
    ]
    def m6row(row):
        if row == m6[0]: return [B(c, body) for c in row]
        styled = []
        for j, c in enumerate(row):
            if j == 2:
                c2 = T_DN if "\u2192" in c or "\u2193" in c else T_UP if "\u2191" in c or "\u2197" in c else T_FLAT
                styled.append(P(f"<b><font color='{c2.hexval()}'>{c}</font></b>", body))
            else:
                styled.append(P(c, body))
        return styled
    mt6 = Table([m6row(m6[0])] + [m6row(r) for r in m6[1:]],
        colWidths=[3.5*cm, 1.4*cm, 4.8*cm, 4.5*cm], repeatRows=1)
    mt6.setStyle(TableStyle([
        ("BACKGROUND",(0,0),(-1,0),ACC),
        ("TEXTCOLOR",(0,0),(-1,0),H_FG),
        ("ROWBACKGROUNDS",(0,1),(-1,-1),[colors.white, ALT]),
        ("GRID",(0,0),(-1,-1),0.4,colors.HexColor("#ccd0ee")),
        ("VALIGN",(0,0),(-1,-1),"TOP"),
        ("TOPPADDING",(0,0),(-1,-1),4),("BOTTOMPADDING",(0,0),(-1,-1),4),
        ("LEFTPADDING",(0,0),(-1,-1),5),
    ]))
    story.append(mt6)
    story.append(P("\u7f8e\u56fd\u5927\u9009\uff0811\u6708\uff09\u5173\u952e\u53d8\u91cf\uff1a\u7279\u6717\u666e\u56de\u5f52 \u2192 \u51b2\u7a81\u6269\u5927\u6982\u7387\u5347\u81f3 45%\uff1b\u6c11\u4e3b\u515a\u5ef6\u7eed \u2192 \u5c40\u52bf\u6e29\u800c\u4e0d\u7206", small))

    story.append(PageBreak())

    # ── 第四章：犹太智囊 ─────────────────────────────────────
    story += [
        P("\u56db\u3001\u72b9\u592a\u667a\u56ca\u63a8\u6f14", sec),
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
        ["\u98ce\u9669\u7b49\u7ea7","\ud83d\udfe1 \u4e2d\u9ad8\u98ce\u9669"],
        ["\u5c3e\u90e8\u98ce\u9669\uff081\uff09","\u7f8e\u4ee5\u5bf9\u4f0a\u671f\u6838\u8bbe\u65bd\u201c\u5916\u79d1\u624b\u672f\u201d\u6253\u51fb\uff08\u6982\u7387 15-20%\uff09\uff0c\u89e6\u53d1\u5bfc\u5f39\u9984\u548c\u62a5\u590d\uff0c\u9020\u6210\u57ce\u5e02\u7ea7\u4f24\u4ea1"],
        ["\u5c3e\u90e8\u98ce\u9669\uff082\uff09","\u970d\u5c14\u6728\u5179\u5b9e\u8d28\u5c01\u9501\uff08\u6982\u7387 10-15%\uff09\uff0c\u5168\u7403\u8fdb\u5165\u80fd\u6e90\u5371\u673a\uff0c\u6cb9\u4ef7$100-130"],
        ["\u5c3e\u90e8\u98ce\u9669\uff083\uff09","\u4f0a\u671f\u5185\u90e8\u7ecf\u6d4e\u4e34\u754c\u5d29\u6e83 \u2192 \u4ee3\u7406\u4eba\u51b2\u7a81\u788b\u7247\u5316\u8411\u5ef6"],
        ["\u5c3e\u90e8\u98ce\u9669\uff084\uff09","\u8bef\u5224/\u611f\u6027\u4e8b\u4ef6\u5f15\u53d1\u87ba\u65cb\u5347\u7ea7\uff086-8\u6708\u9ad8\u5371\u7a97\u53e3\uff09"],
        ["\u5bf9\u51a0\u5efa\u8bae\uff1a\u6570\u636e\u76d1\u63a7","\u970d\u5c14\u6728\u5179\u66ff\u4ee3\u6e2f\u53e3\u7269\u6d41\u6570\u636e\u9700\u5b9e\u65f6\u76d1\u63a7 \u2014 \u8c03\u5148\u6253\u901a\u9646\u57fa\u901a\u9053\uff0c\u8c03\u6253\u534a\u5e74\u6cb9\u4ef7\u5b9a\u4ef7\u6743"],
        ["\u5bf9\u51a0\u5efa\u8bae\uff1a\u5e93\u5b58\u8865\u5145","\u6218\u7565\u5e93\u5b58\u9002\u5ea6\u8865\u5145\uff08\u5f53\u524d$72/\u6876\u4e3a\u76f8\u5bf9\u4f4e\u4f4d\u7a97\u53e3\uff09"],
        ["\u5bf9\u51a0\u5efa\u8bae\uff1a\u822a\u8fd0\u671f\u79df","\u7ea2\u6d77\u822a\u7ebf\u4fdd\u9669\u6210\u672c\u4e0a\u5347\u5df2\u6210\u5b9a\u5c40\uff0c\u822a\u8fd0\u5bc6\u96c6\u578b\u4f01\u4e1a\u63d0\u524d\u9501\u5b9a\u671f\u79df\u5408\u4ea6"],
    ]

    rot_data = [
        ["\u673a\u4f1a\u9879","\u5185\u5bb9"],
        ["\u5951\u5229\u7a7a\u95f4\uff081\uff09","[\u8ba4\u77e5\u5dee] \u4f0a\u671f\u66ff\u4ee3\u6e2f\u53e3=\u4e3b\u52a8\u5e03\u5c40\u5bf9\u51b2\uff0c\u975e\u88ab\u52a8\u7ed5\u884c \u2014 \u5e02\u573a\u5c1a\u672a\u5b8c\u5168\u5b9a\u4ef7\u6b64\u4fe1\u53f7"],
        ["\u5951\u5229\u7a7a\u95f4\uff082\uff09","[\u786e\u5b9a\u6027\u6ea2\u4ef7] 4\u4e2a\u7ef4\u5ea6\u7f6e\u4fe1\u5ea6\u2265 75%\uff0c\u53ef\u5728\u80fd\u6e90/\u91d1\u878d\u9886\u57df\u505a\u7ed3\u6784\u5e03\u5c40"],
        ["\u7acb\u5373\u884c\u52a8","\U0001f7e2 \u672b\u676572\u5c0f\u65f6\uff1a\u76d1\u63a7\u4ee5\u8272\u5217 F-35I \u90e8\u7f72\u8282\u594f\uff1b\u786e\u8ba4\u970d\u5c14\u6728\u5179\u901a\u884c\u72b6\u6001\u5b9e\u65f6\u6570\u636e"],
        ["\u77ed\u671f\u5e03\u5c40","\ud83d\udfe1 1-2\u5468\uff1aWTI $68-78\u533a\u95f4\u8d85\u632f\uff0c\u53ef\u505a\u5e93\u5b58\u8865\u5145\uff1b\u589e\u6301\u9ad8\u8d28\u91cf\u56fa\u6536\uff0c\u524a\u51cf\u9ad8\u8d1d\u5851\u80fd\u6e90\u80a1"],
        ["\u4e2d\u671f\u5e03\u5c40","\ud83d\udfe1 3-6\u4e2a\u6708\uff1a\u6cb9\u4ef7\u6574\u4f53\u627f\u538b\u4e0a\u884c\uff0c\u80fd\u6e90\u80a1/\u6cb9\u8f6e\u677f\u5757\u6709\u652f\u6491\uff1b\u5173\u6ce8\u9ec4\u91d1\u7a81\u7834$2500\u673a\u4f1a"],
        ["\u884c\u52a8\u4f18\u5148\u7ea7","\u76d1\u63a7 \u2192 \u91c7\u8d2d\u5bf9\u51a0 \u2192 \u5e03\u5c40\u80fd\u6e90\u66ff\u4ee3\u8def\u7ebf \u2192 \u7b49\u5f85\u5916\u4ea4\u7a97\u53e3"],
    ]

    story += [
        P("\U0001f3f9 \u6240\u7f57\u95e8\uff1a\u98ce\u9669\u67b6\u6784\u5e08", sub),
        kv_table(sol_data, [3*cm, 11.2*cm], H_BG),
        Spacer(1, 0.3*cm),
        P("\U0001f3f0 \u7f57\u65af\u8d1d\u5c14\u5fb7\uff1a\u673a\u4f1a\u6316\u6398\u8005", sub),
        kv_table(rot_data, [3*cm, 11.2*cm], ROT_BG),
        Spacer(1, 0.4*cm),
    ]

    # ── 第五章：行动建议 ────────────────────────────────────
    story += [
        P("\u4e94\u3001\u884c\u52a8\u5efa\u8bae", sec),
        HRFlowable(width="100%", thickness=1, color=ACC, spaceAfter=0.2*cm),
    ]

    actions = [
        ["\u4f18\u5148\u7ea7","\u65f6\u95f4","\u884c\u52a8\u9879","\u80cc\u666f"],
        ["\U0001f7e2 \u9ad8","\u7acb\u5373\n\uff0872h\uff09",
         "\u786e\u8ba4\u970d\u5c14\u6728\u5179\u901a\u884c\u72b6\u6001\u5b9e\u65f6\u6570\u636e\n\u76d1\u63a7\u4ee5\u8272\u5217 F-35I \u90e8\u7f72\u8282\u594f\n\u901a\u77e5\u80fd\u6e90\u91c7\u8d2d\u56e2\u961f\u8fdb\u5165\u5173\u6ce8\u72b6\u6001",
         "\u6cb9\u4ef7\u7ebf\u6bb5\u6025\u6da8 10-15%\u7684\u89e6\u53d1\u6761\u4ef6"],
        ["\ud83d\udfe1 \u4e2d","\u77ed\u671f\n\uff081-2\u5468\uff09",
         "\u539f\u6cb9\u957f\u7ea6\u9501\u5b9a\u6bd4\u4f8b\u63d0\u5347 20-30%\n\u589e\u6301\u9ad8\u8d28\u91cf\u56fa\u6536\uff0c\u524a\u51cf\u9ad8\u8d1d\u5851\u80fd\u6e90\u80a1\n\u5173\u6ce8\u65e5\u5143/\u745e\u90a6/\u9ec4\u91d1\u7a81\u7834\u673a\u4f1a\n\uff08\u51b2\u7a81\u5347\u7ea7\u2192\u9ec4\u91d1\u6709\u671b\u7a81\u7834$2500\uff09",
         "$72/\u6876\u4e3a\u76f8\u5bf9\u4f4e\u4f4d\u7a97\u53e3"],
        ["\ud83d\udfe1 \u4e2d","\u4e2d\u671f\n\uff083-6\u5468\uff09",
         "\u52a0\u901f\u970d\u5c14\u6728\u5179\u66ff\u4ee3\u8def\u7ebf\uff08\u4e2d\u4e9a/\u4fc4\u7f57\u65af\u9646\u8def\uff09\n\u4e2d\u56fd\u4e00\u5e26\u4e00\u8def 2000\u4ebf\u7f8e\u5143\u6295\u8d44\u5b89\u5168\u8bc4\u4f30\uff0c\u542f\u52a8\u98ce\u9669\u5206\u7ea7\u9884\u6848\n\u4f0a\u671f\u5bfc\u5f39\u7cbe\u5ea6\u76d1\u6d4b\uff08CEP 300\u7c73\u9000\u5316\u81f3 500\u7c73=\u5c01\u9501\u89c1\u6548\u786e\u7801\uff09",
         "\u591a\u60c5\u666f\u5206\u5316\uff0c\u63d0\u524d\u5e03\u5c40"],
    ]
    act_t = Table(
        [[B(c, body) for c in actions[0]]] + [[P(c, body) for c in r] for r in actions[1:]],
        colWidths=[1.8*cm, 1.8*cm, 6.5*cm, 4.1*cm], repeatRows=1
    )
    act_t.setStyle(TableStyle([
        ("BACKGROUND",(0,0),(-1,0),ACC),
        ("TEXTCOLOR",(0,0),(-1,0),H_FG),
        ("ROWBACKGROUNDS",(0,1),(-1,-1),[colors.white, ALT]),
        ("GRID",(0,0),(-1,-1),0.4,colors.HexColor("#ccd0ee")),
        ("VALIGN",(0,0),(-1,-1),"TOP"),
        ("TOPPADDING",(0,0),(-1,-1),5),("BOTTOMPADDING",(0,0),(-1,-1),5),
        ("LEFTPADDING",(0,0),(-1,-1),5),
    ]))
    story.append(act_t)
    story.append(Spacer(1, 0.4*cm))

    # ── 第六章：核心结论 ────────────────────────────────────
    story += [
        P("\u516d\u3001\u6838\u5fc3\u7ed3\u8bba", sec),
        HRFlowable(width="100%", thickness=1, color=ACC, spaceAfter=0.2*cm),
    ]

    quote_s = ParagraphStyle("QS", parent=body,
        fontSize=11, leading=17, textColor=colors.white, fontName=cn_font)
    qbox = Table([[P(
        "\u201c\u8fd9\u4e0d\u662f\u2018\u72fc\u6765\u4e86\u2019\u3002\u4f0a\u671f\u5df2\u5728\u5e03\u5c40\u66ff\u4ee3\u8def\u5f84\uff0c\u5728\u8d81\u4e00\u573a\u957f\u671f\u9ad8\u70c8\u5ea6\u80fd\u6e90\u535a\u5f08\u3002"
        "\u201d \u2014 Plutus\uff08\u7ecf\u6d4e\u91d1\u878d\u5bb6\uff09",
        quote_s)]], colWidths=[14.4*cm])
    qbox.setStyle(TableStyle([
        ("BACKGROUND",(0,0),(-1,-1),H_BG),
        ("TOPPADDING",(0,0),(-1,-1),12),("BOTTOMPADDING",(0,0),(-1,-1),12),
        ("LEFTPADDING",(0,0),(-1,-1),14),("RIGHTPADDING",(0,0),(-1,-1),14),
    ]))
    story.append(qbox)
    story.append(Spacer(1, 0.25*cm))

    story += [
        P("\u5f53\u524d\u6838\u5fc3\u77db\u76fe", sub),
        P("\u77ed\u671f\u6280\u672f\u6027\u964d\u6e29\uff08\u5e02\u573a\u5598\u6c14\uff09\u63d9\u76d6\u4e86\u4e2d\u671f\u7ed3\u6784\u6027\u5347\u6e29\uff08\u80fd\u6e90\u538b\u529b+\u6838\u4e34\u754c+\u5927\u9009\u53d8\u91cf\uff09\uff0c"
          "\u4e24\u8005\u53e0\u52a0\u6784\u6210\u300c\u5047\u7a33\u5b9a\u9677\u9631\u300d\u3002", body),
        Spacer(1, 0.15*cm),
        P("\u5bf9\u4e2d\u56fd\u6700\u91cd\u8981\u7684\u4e00\u53e5\u8bdd", sub),
    ]

    china_s = ParagraphStyle("ChS", parent=body,
        fontSize=11, leading=17, textColor=colors.HexColor("#1a1a2e"))
    cbox = Table([[P(
        "\u4f60\u662f\u552f\u4e00\u540c\u65f6\u4e0e\u4f0a\u671f\u3001\u6c99\u7279\u3001\u4ee5\u8272\u5217\u4fdd\u6301\u6218\u7565\u6c9f\u901a\u7684\u5927\u56fd \u2014 "
        "\u4e09\u65b9\u5e73\u8861\u5173\u7cfb\u662f\u7a00\u7f3a\u8d44\u4ea7\uff0c\u5e94\u4e3b\u52a8\u5165\u4f53\uff0c"
        "\u5728\u505c\u706b\u8c08\u5224\u4e2d\u4e89\u53d6\u300c\u6709\u7259\u9f7f\u7684\u5efa\u8bbe\u6027\u89d2\u8272\u300d\uff0c"
        "\u800c\u975e\u4ec5\u6b62\u4e8e\u9053\u4e49\u547c\u5401\u3002",
        china_s)]], colWidths=[14.4*cm])
    cbox.setStyle(TableStyle([
        ("BACKGROUND",(0,0),(-1,-1),colors.HexColor("#eef2ff")),
        ("TOPPADDING",(0,0),(-1,-1),12),("BOTTOMPADDING",(0,0),(-1,-1),12),
        ("LEFTPADDING",(0,0),(-1,-1),14),("RIGHTPADDING",(0,0),(-1,-1),14),
        ("BOX",(0,0),(-1,-1),1.5,ACC),
    ]))
    story.append(cbox)
    story.append(Spacer(1, 0.4*cm))

    story += [
        HRFlowable(width="100%", thickness=0.5, color=colors.HexColor("#ccd0ee"), spaceAfter=0.15*cm),
        P("Global Intelligence v0.3 | 8\u7ef4\u4e13\u5bb6\uff08QClaw\u4e91\u7aef\u5e76\u884c\uff09+ \u53cc\u72b9\u592a\u667a\u56ca | \u4f0a\u8fea\u65af\u603b\u8c03\u5ea6 | 2026-04-17", small),
    ]

    doc.build(story)
    print(f"\u2705 PDF \u5df2\u751f\u6210\uff1a{OUTPUT}")

if __name__ == "__main__":
    build_pdf()
