# 技能：图形界面控制

## 关闭图形界面
**触发词：**
- "关闭电脑图形界面"
- "关闭图形界面"
- "关掉图形界面"
- "关闭 GUI"

**执行命令：**
```bash
sudo launchctl stop com.apple.WindowServer
```

## 打开图形界面
**触发词：**
- "打开图形界面"
- "开启图形界面"
- "启动 GUI"
- "打开 GUI"

**执行命令：**
```bash
sudo launchctl start com.apple.WindowServer
```

## 说明
执行后会关闭/开启 macOS 的图形界面（相当于登出/登录当前用户）。

## 注意事项
- 需要管理员密码
- 关闭时会中断当前所有未保存的工作
- 关闭后需要重新登录