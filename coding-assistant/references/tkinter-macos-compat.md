# tkinter macOS 环境对比（2026-05-07 实测）

## Python环境

| 环境 | 路径 | Python | tkinter | Tcl/Tk |
|------|------|--------|---------|--------|
| 系统Python | `/usr/bin/python3` | 3.9.6 | 8.5 | 8.5 |
| Hermes venv | `~/.hermes/hermes-agent/venv/bin/python3` | 3.11.15 | 9.0 | 9.0 |

## 功能对比

| 功能 | tkinter 8.5 (系统) | tkinter 9.0 (venv) |
|------|--------------------|--------------------|
| `root.title()` 更新 | ✅ | 未测试 |
| `label.config(text=)` | ❌ 不生效 | 未测试 |
| `StringVar` + `Label(textvariable=)` | ❌ 按钮不渲染 | 未测试 |
| `Button(command=func)` | ✅ (简单脚本) | ❌ 完全不触发 |
| `Button(command=lambda:)` | ✅ (简单脚本) | ❌ 完全不触发 |
| `Button(command=partial())` | ❌ | ❌ |
| `bind("<Button-1>")` | 未测试 | ❌ |

## 验证方法

```bash
# 检查当前Python版本
which python3
python3 -c "import tkinter; print(tkinter.TkVersion)"

# 检查系统Python
/usr/bin/python3 -c "import tkinter; print(tkinter.TkVersion)"

# 检查Hermes venv
~/.hermes/hermes-agent/venv/bin/python3 -c "import tkinter; print(tkinter.TkVersion)"
```

## 结论

1. tkinter 9.0 (Hermes venv) 在macOS上按钮事件完全不工作
2. tkinter 8.5 (系统Python) 部分功能受限
3. GUI开发应优先考虑Web界面或PyQt/PySide替代方案
