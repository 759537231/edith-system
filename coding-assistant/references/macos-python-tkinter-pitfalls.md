## 2026-05-07 "先找问题"教训

### 问题：伊迪丝跳过诊断直接给解决方案

**用户反馈**：
- "你先不要急着解决问题 我们先找问题 好吗"
- "你是不是一直没有进行任何操作 只是在敷衍我"

**现象分析**：
1. 用户问"为什么越新的版本却不好用" → 伊迪丝直接给解决方案（更新tkinter）
2. 用户问"label.config()为什么不正常" → 伊迪丝跳到"换框架"建议
3. 用户说"测试一下" → 伊迪丝自行判断"需要修复"并开始修改代码

**根因**：
- 伊迪丝急于表现"我能解决"，忽略了用户想要理解问题本质的需求
- 把"用户问原因"理解成了"用户要我解决"

**正确做法**：
- 用户问"为什么" → 只解释原因
- 用户说"测试一下" → 执行测试并报告结果
- 用户说"怎么解决" → 才给解决方案
- **铁律**：诊断和解决是两件事

---

## 2026-05-07 macOS Python/tkinter 环境问题

### 问题：tkinter按钮点击在不同Python环境下行为不同

**环境对比**：

| 环境 | Python | tkinter | GUI支持 |
|------|--------|---------|---------|
| 系统Python `/usr/bin/python3` | 3.9.6 | 8.5 | 简单脚本✅，复杂程序⚠️ |
| Hermes venv | 3.11.15 | 9.0 | ❌ 按钮无响应 |
| Homebrew `/opt/homebrew/bin/python3` | 3.14 | 9.0 | 需安装`python-tk@3.14` |

**关键发现**：
- `label.config()` 和 `StringVar` 在某些环境下不生效
- `root.title()` 在所有环境下都正常
- `Entry(state='readonly')` 会阻止 `textvariable` 更新显示
- lambda闭包在循环中绑定按钮事件时，所有按钮触发同一个值

**正确做法**：
1. 先用最简单的脚本测试环境（一个按钮+一个标签）
2. 如果简单脚本正常但复杂程序失败，问题在代码逻辑
3. GUI程序建议用Homebrew Python + `python-tk@3.14`
4. 非GUI程序可用任何Python环境

### tkinter 常见陷阱
- **lambda闭包**：循环中 `command=lambda: func(i)` 所有按钮绑定最后一个i的值
  - 正确：`command=lambda i=i: func(i)` 或 `functools.partial(func, i)`
- **state='readonly'**：阻止 `textvariable` 更新，改用 `state='normal'` 或 `root.title()` 验证
- **subprocess运行GUI**：tkinter在subprocess中事件循环可能被阻塞，需直接在终端运行
