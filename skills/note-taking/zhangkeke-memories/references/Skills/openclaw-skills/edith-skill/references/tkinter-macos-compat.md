# tkinter macOS 兼容性问题（2026-05-07 验证）

## 环境对比

| 环境 | Python | tkinter | Tcl/Tk | 按钮command | label.config() |
|------|--------|---------|--------|-------------|----------------|
| 系统Python `/usr/bin/python3` | 3.9.6 | 8.5 | 8.5 | ✅ 有效 | ❌ 不生效 |
| Hermes虚拟环境 `~/.hermes/hermes-agent/venv/bin/python3` | 3.11.15 | 9.0 | 9.0 | ❌ 不触发 | 未测试 |

## 已验证的工作模式

### 系统Python (tkinter 8.5) — 按钮command可用
```python
# ✅ 有效：root.title() + command=函数
def on_click():
    root.title("点击了！")
btn = tk.Button(root, text="点击", command=on_click)

# ✅ 有效：lambda + root.title()
btn = tk.Button(root, text="点击", command=lambda: root.title("点击了！"))

# ❌ 无效：label.config() 不更新显示
label.config(text="新文本")  # 不生效

# ❌ 无效：StringVar + Label(textvariable=) — 按钮不显示
text_var = tk.StringVar()
label = tk.Label(root, textvariable=text_var)
btn = tk.Button(root, text="点击", command=lambda: text_var.set("新文本"))
# 按钮本身不渲染
```

### Hermes虚拟环境 (tkinter 9.0) — 按钮command完全不触发
```python
# ❌ 所有command都不触发
# 包括 lambda、partial、bind("<Button-1>") 均失败
# 窗口显示正常，按钮渲染正常，但点击无反应
```

## 结论

1. **tkinter 9.0在macOS上有严重bug** — 按钮事件完全不工作
2. **tkinter 8.5部分功能受限** — `label.config()`不生效，`StringVar`绑定按钮有渲染问题
3. **可靠的操作**：`root.title()` + `command=func` 在tkinter 8.5下可靠

## 建议

- GUI开发避免使用Hermes虚拟环境的Python
- 使用 `/usr/bin/python3` 运行tkinter程序
- 测试GUI功能时，先用 `root.title()` 验证事件循环是否正常
- 避免 `label.config()` 更新显示，改用其他反馈方式（如窗口标题、弹窗）
- 复杂GUI考虑用 PyQt/PySide 替代 tkinter
