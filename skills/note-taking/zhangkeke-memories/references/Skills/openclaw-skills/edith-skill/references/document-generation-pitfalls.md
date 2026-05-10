# 文档生成 Pitfalls（PDF/报告/策划案）

## fpdf2 + 中文字体

### 字体路径
```python
# ✅ 正确：系统中文字体
pdf.add_font('chinese', '', '/System/Library/Fonts/STHeiti Medium.ttc')

# ❌ 错误：PingFang.ttc 不在 /System/Library/Fonts/
# ❌ 错误：用 uni=True 参数（已废弃）
```

### 编码陷阱
```python
# ❌ 错误：对中文内容用 courier 字体
pdf.set_font('courier', '', 9)  # 会报 FPDFUnicodeEncodingException

# ✅ 正确：所有含中文的文本都用中文字体
pdf.set_font('chinese', '', 9)
```

### cell 参数更新
```python
# ❌ 错误：ln 参数已废弃
pdf.cell(0, 10, 'text', 0, 1, 'C')  # DeprecationWarning

# ✅ 正确：用 new_x/new_y
pdf.cell(0, 10, 'text', new_x="LMARGIN", new_y="NEXT", align='C')
```

### bullet_point 空间不足
```python
# ❌ 错误：先 cell 再 multi_cell 可能空间不足
def bullet_point(self, text):
    self.cell(10, 8, '•', 0, 0)
    self.multi_cell(0, 8, text)  # Not enough horizontal space

# ✅ 正确：直接拼接
def bullet_point(self, text):
    self.multi_cell(0, 8, f'• {text}')
```

## reportlab

- `pip3 install reportlab` 可能超时（网络问题）
- 回退方案：用 fpdf2（更轻量，安装快）

## 通用建议

1. **先测试小样本**——不要直接生成完整 PDF，先用 1-2 页测试字体和编码
2. **检查文件大小**——中文字体嵌入会增大文件，STHeiti 约 150K/份
3. **输出路径用绝对路径**——避免工作目录问题
