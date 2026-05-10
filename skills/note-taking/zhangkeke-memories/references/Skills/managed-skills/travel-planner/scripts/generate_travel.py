#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
旅行攻略表格生成脚本

用法：
    python3 generate_travel.py --output ~/Desktop/旅行攻略.xlsx --info '{"出发地":"无锡","目的地":"皖南","天数":3,...}'

参数说明：
    --output: 输出文件路径（默认：~/Desktop/旅行攻略.xlsx）
    --info: JSON格式的旅行信息

示例：
    python3 generate_travel.py --output ~/Desktop/皖南川藏线攻略.xlsx --info '{"出发地":"无锡","目的地":"皖南川藏线","天数":3,"人数":2,"预算":"1000-1500","车型":"特斯拉 Model Y","爬山":false,"收费景点":"可选"}'
"""

import argparse
import json
import sys
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side

def create_travel_xlsx(info, output_path):
    """创建旅行攻略表格"""
    wb = Workbook()
    
    # 样式定义
    title_font = Font(size=16, bold=True, color='FFFFFF')
    header_font = Font(size=12, bold=True)
    title_fill = PatternFill(start_color='2E75B6', end_color='2E75B6', fill_type='solid')
    header_fill = PatternFill(start_color='D9E1F2', end_color='D9E1F2', fill_type='solid')
    thin_border = Border(
        left=Side(style='thin'), right=Side(style='thin'),
        top=Side(style='thin'), bottom=Side(style='thin')
    )
    
    # Sheet 1: 基本信息
    ws = wb.active
    ws.title = "基本信息"
    
    ws['A1'] = f"🚗 {info.get('目的地', '旅行')}自驾攻略"
    ws['A1'].font = title_font
    ws['A1'].fill = title_fill
    ws.merge_cells('A1:B1')
    
    ws['A3'] = '项目'
    ws['B3'] = '内容'
    ws['A3'].font = header_font
    ws['B3'].font = header_font
    ws['A3'].fill = header_fill
    ws['B3'].fill = header_fill
    
    basic_info = [
        ('出发地', info.get('出发地', '')),
        ('目的地', info.get('目的地', '')),
        ('车型', info.get('车型', '')),
        ('行程天数', f"{info.get('天数', '')}天{info.get('天数', 1)-1}晚"),
        ('同行人数', f"{info.get('人数', '')}人"),
        ('预算', info.get('预算', '')),
        ('游玩方式', '自驾为主，车能到的地方都去' + ('，不爬山' if not info.get('爬山', False) else '')),
    ]
    
    for i, (k, v) in enumerate(basic_info, start=4):
        ws[f'A{i}'] = k
        ws[f'B{i}'] = v
    
    for col in ['A', 'B']:
        ws.column_dimensions[col].width = 25
    
    # 更多Sheet...（根据需要扩展）
    
    wb.save(output_path)
    return output_path

def main():
    parser = argparse.ArgumentParser(description='生成旅行攻略表格')
    parser.add_argument('--output', default='~/Desktop/旅行攻略.xlsx', help='输出文件路径')
    parser.add_argument('--info', required=True, help='JSON格式的旅行信息')
    args = parser.parse_args()
    
    try:
        info = json.loads(args.info)
    except json.JSONDecodeError as e:
        print(f"JSON解析错误: {e}", file=sys.stderr)
        sys.exit(1)
    
    # 展开路径
    output_path = args.output.replace('~', '~')
    
    result = create_travel_xlsx(info, output_path)
    print(f"已生成: {result}")

if __name__ == '__main__':
    main()