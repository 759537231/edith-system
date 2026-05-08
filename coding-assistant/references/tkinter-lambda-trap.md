# tkinter lambda闭包陷阱

## 问题描述
在循环中创建tkinter按钮时，使用lambda或functools.partial绑定事件，所有按钮触发同一个值。

## 根因
- lambda捕获的是变量引用，不是值
- 循环结束后，变量指向最后一个值
- macOS tkinter 8.5 + Python 3.9行为与Linux/Windows不同

## 错误写法
```python
# 方法1：lambda（失败）
for text in buttons:
    btn = tk.Button(root, text=text, command=lambda t=text: func(t))

# 方法2：functools.partial（失败）
from functools import partial
for text in buttons:
    btn = tk.Button(root, text=text, command=partial(func, text))
```

## 正确写法
不使用循环，直接创建每个按钮：
```python
btn_1 = tk.Button(root, text='1', command=lambda: func('1'))
btn_2 = tk.Button(root, text='2', command=lambda: func('2'))
# ... 每个按钮单独创建
```

## 验证环境
- macOS Sequoia
- Python 3.9.6
- tkinter 8.5

## 适用场景
- 任何需要在循环中绑定事件的tkinter应用
- 特别是macOS环境

## 替代方案
如果必须使用循环，可以尝试：
1. 使用类属性存储按钮文本
2. 使用字典映射按钮到处理函数
3. 使用第三方库（如PyQt、wxPython）
