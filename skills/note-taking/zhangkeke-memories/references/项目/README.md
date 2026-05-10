# 音频计费系统 - 项目进度

## 项目概述
自动解析剧本 + 转写音频 + 匹配角色 + 计算配音费用

## 当前进度

| 阶段 | 状态 | 说明 |
|------|------|------|
| 剧本解析 | ✅ 完成 | 支持 docx 格式，自动提取角色和台词 |
| 角色提取 | ✅ 完成 | 测试通过（15个角色） |
| 台词提取 | ✅ 完成 | 测试通过（237条台词） |
| Whisper 安装 | ✅ 完成 | base 模型已下载 |
| ffmpeg 安装 | ✅ 完成 | 已安装到 ~/.local/bin/ |
| 音频转写 | ✅ 完成 | 测试通过 |
| 角色匹配 | ✅ 完成 | 基于文本相似度匹配 |
| 费用计算 | ✅ 完成 | 需要设置单价 |

## 文件位置

```
/Users/labixiaoxin/.qclaw/workspace/audio_billing/
├── script_parser.py     # 剧本解析器
├── audio_billing.py     # 完整计费系统
└── README.md            # 本文件
```

## 使用方法

```bash
# 设置 PATH
export PATH="$HOME/.local/bin:$PATH"

# 运行
cd /Users/labixiaoxin/.qclaw/workspace/audio_billing
python3 audio_billing.py 剧本.docx 音频.mp3 --model base
```

## 待完成

1. [ ] 设置角色单价（修改 audio_billing.py 里的 PRICE_PER_MINUTE）
2. [ ] 打包成 .app 应用
3. [ ] 支持更多剧本格式
4. [ ] 优化匹配算法

## 测试记录

- 测试剧本：魅魔-画本_第1章-第10章.docx
- 测试音频：魅魔_01-10_安祖丽斯_yx.mp3
- 测试时间：2026-03-29 23:08
- 测试结果：成功

## 依赖

- Python 3.13
- openai-whisper
- python-docx
- ffmpeg (~/.local/bin/ffmpeg)
