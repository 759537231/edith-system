# 奇门遁甲排盘 Web App

## 项目概述

2026-05-06 开始开发的奇门遁甲排盘工具。

**定位：** 纯排盘工具，不做解读。用户自己决定怎么用排盘结果。

**技术选型：** Web APP + PWA（HTML/CSS/JavaScript）

**选择理由：**
- 不需要Apple Developer账号
- 开发最简单，维护方便
- iPhone可以添加到主屏幕，像APP一样使用
- 离线可用（Service Worker）

## 项目结构

```
/Users/qianmo/qimen_app/
├── index.html          # 主界面
├── qimen.js            # 排盘核心算法
├── manifest.json       # PWA配置
├── service-worker.js   # 离线支持
└── icon.svg            # 图标
```

## 功能清单

| 功能 | 状态 | 说明 |
|------|------|------|
| 自动获取时间 | ✅ | JavaScript获取当前时间 |
| 自动获取位置 | ✅ | 浏览器Geolocation API |
| 排盘计算 | ✅ | 真太阳时、节气、局数、八门、八神、九星、三奇六仪 |
| 九宫格展示 | ✅ | 显示完整排盘结果 |
| 手动输入 | ⏳ | 可以手动输入时间+位置（用于回溯排盘） |
| 添加到主屏幕 | ✅ | PWA配置 |
| 离线使用 | ✅ | Service Worker缓存 |

## 排盘算法核心

**计算步骤：**
1. 真太阳时 = 北京时间 + (当地经度 - 120) × 4分钟
2. 时辰 = (真太阳时小时 + 1) / 2 取整，对应十二地支
3. 日干支 = 基于基准日（2026-01-01 甲子日）推算
4. 时干支 = 日干起时干口诀（甲己还加甲，乙庚丙作初...）
5. 节气 = 查表确定当前节气
6. 阴阳遁 = 冬至后阳遁，夏至后阴遁
7. 局数 = 根据节气+阴阳遁查表
8. 排地盘 = 三奇六仪根据局数排列
9. 排天盘 = 跟随值符转动
10. 排八门 = 根据局数+阴阳遁
11. 排九星 = 根据局数
12. 排八神 = 跟随时干

**已知限制：**
- 节气表是2026年硬编码，需要每年更新
- 排盘算法是简化版，可能与专业软件有差异
- 天盘转动逻辑简化，未完全实现值符跟随

## 测试方法

**本地测试：**
```bash
cd /Users/qianmo/qimen_app
python3 -m http.server 8080
# 打开浏览器访问 http://localhost:8080
```

**添加到iPhone主屏幕：**
1. 在iPhone上用Safari打开网页
2. 点击分享按钮（方框+箭头）
3. 选择"添加到主屏幕"
4. 确认添加

## 测试结果（2026-05-06）

输入：2026-05-06 10:30，经度119.57，纬度31.99

输出：
- 真太阳时：2026-05-06 10:28
- 时辰：巳时
- 日干支：己巳
- 时干支：己巳
- 节气：立夏
- 阴阳遁：阳遁
- 局数：4局

## 后续优化方向

1. **更新节气表** — 支持多年份，或用天文算法计算
2. **完善天盘算法** — 实现真正的值符跟随转动
3. **添加手动输入** — 支持回溯排盘
4. **界面美化** — 九宫格更美观，添加动画效果
5. **指南针集成** — 实时显示当前朝向，对应八门方位
6. **部署到公网** — GitHub Pages（免费、永久），解决离线首次访问问题

## iPhone部署经验（2026-05-06）

**用户预期 vs 现实：**
- 用户期望：像Mac一样"浏览器下载 .dmg → 双击安装"
- 现实：iPhone不允许侧载，必须经过苹果签名

**可行方案对比：**

| 方案 | 费用 | 麻烦程度 | 有效期 |
|------|------|---------|--------|
| Safari添加到主屏幕 | 免费 | 最简单 | 永久 |
| Xcode + 免费Apple ID | 免费 | 中等 | 7天重签 |
| Apple Developer账号 | $99/年 | 中等 | 1年 |

**推荐方案：Safari添加到主屏幕 + PWA离线**
1. 部署到GitHub Pages（永久免费）
2. iPhone用Safari打开一次
3. 分享 → 添加到主屏幕
4. 之后可离线使用（Service Worker缓存）

**⚠️ PWA离线限制：** Service Worker需要HTTPS才能工作（localhost除外）。局域网HTTP访问无法注册Service Worker，所以不能离线。必须部署到公网HTTPS地址。

**部署尝试记录（2026-05-06）：**
- localtunnel → 失败（`connection refused: localtunnel.me:17919`，防火墙问题）
- Surge → 需要登录
- Netlify → 安装CLI超时
- GitHub Pages → 需要GitHub账号（用户没有）
- **局域网访问** → 可行但有限制

**局域网访问方案：**
- Mac IP：192.168.31.204（ifconfig获取）
- 启动服务器：`python3 -m http.server 8081`（8080常被占用）
- iPhone Safari访问：`http://192.168.31.204:8081`
- 限制：需要Mac开着+同一个WiFi，不能离线

## Capacitor打包iOS APP经验（2026-05-06）

**目标：** 把Web APP打包成iOS原生APP，用户可以直接安装。

**步骤：**
```bash
cd /Users/qianmo/qimen_app
npm init -y
npm install @capacitor/core @capacitor/cli
npx cap init "奇门遁甲排盘" "com.qimen.app" --web-dir www
npm install @capacitor/ios
npx cap add ios
npx cap sync ios
```

**⚠️ 坑1：webDir配置**
- `--web-dir .` 不被接受，必须指定具体目录
- 解决：创建`www/`目录，把所有web文件复制进去
- `capacitor.config.json`中`"webDir": "www"`

**⚠️ 坑2：Xcode要求**
- `npx cap add ios` 会创建Xcode项目
- 但需要完整的Xcode（从App Store下载，~12GB）
- 只有CommandLineTools不够：`xcode-select: error: tool 'xcodebuild' requires Xcode`
- 检查方法：`xcodebuild -version`

**⚠️ 坑3：签名要求**
- 免费Apple ID可以签名，但7天需要重签
- App Store分发需要$99/年开发者账号
- 企业分发需要企业开发者账号

**最终结果：** Capacitor项目创建成功，但因为Xcode不完整，无法构建。用户需要安装完整Xcode后继续。

**教训：**
1. 告诉用户"可以做APP"之前，先确认Xcode是否完整安装
2. webDir必须是具体目录，不能用"."
3. 端口8080经常被占用，用8081更安全

## 相关对话

用户说："不要只局限在找人，就有一个排盘的功能就可以了。它的主要功能只有一个排盘。具体要拿它做什么，要看用户想做什么。"

这确立了工具的设计哲学：纯功能，不做解读。
