# Electron桌面应用检修指南

## 检修范围

Electron应用检修需要检查以下模块：

| 模块 | 文件 | 检查项 |
|------|------|--------|
| 主进程 | main.js | IPC通信、文件操作、窗口管理、菜单 |
| 预加载脚本 | preload.js | API暴露、contextBridge |
| 渲染进程 | React组件 | UI逻辑、事件处理、状态管理 |
| 样式 | CSS | 兼容性、响应式、平台特性 |

## 常见问题与修复

### 1. 窗口拖拽问题（macOS）

**问题**：`titleBarStyle: 'hiddenInset'` 导致窗口无法拖拽

**修复**：在CSS中添加拖拽支持
```css
body {
  -webkit-app-region: drag;
}
#root {
  -webkit-app-region: no-drag;
}
```

**注意**：需要在可交互元素上设置 `no-drag`，否则按钮等无法点击

### 2. 文件上传错误处理

**问题**：上传失败时只console.error，不返回错误信息给前端

**修复**：捕获异常，返回详细错误信息
```javascript
} catch (e) {
  console.error('[书桌] 上传失败:', itemPath, e.message);
  uploaded.push({ name: path.basename(itemPath), error: e.message });
}
```

### 3. 右键菜单功能增强

**常见菜单项**：
- 📂 打开文件位置（`shell.showItemInFolder`）
- 📋 复制路径（`navigator.clipboard.writeText`）
- 🗑️ 删除（带确认对话框）

### 4. IPC通信超时

**问题**：主进程操作耗时过长，渲染进程等待超时

**修复**：
- 添加超时机制
- 使用进度回调（`webContents.send`）
- 异步操作使用 `async/await`

## 调试技巧

### 开发模式
```bash
npm run electron:dev  # 同时启动Vite和Electron
```

### 检查主进程日志
```bash
# 在main.js中添加日志
console.log('[主进程] 操作描述');
```

### 检查渲染进程日志
```javascript
// 在React组件中
console.log('[渲染进程] 状态变化', state);
```

## macOS特有问题

1. **窗口拖拽**：需要 `-webkit-app-region: drag`
2. **菜单栏**：使用 `titleBarStyle: 'hiddenInset'` 隐藏标题栏
3. **文件路径**：使用 `path.join` 和 `path.relative` 处理路径
4. **权限**：某些操作需要用户授权（如文件访问）

## 检修清单

```
□ 文件上传功能正常
□ 右键菜单功能完整
□ 窗口拖拽正常（macOS）
□ IPC通信无超时
□ 错误处理完善
□ 日志输出正常
□ 界面响应流畅
```
