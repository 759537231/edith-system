# MEMORY.md - 长期记忆

## 用户信息
- 称呼：张壳壳（我叫壳壳，他是用户）
- 时区：Asia/Shanghai
- 居住地：江苏省镇江市丹阳市双井巷16号
- 创业地：江苏省无锡市惠山区
- 现有业务：置地有声后期工作室（音频后期制作，服务14个剧组）
- 新兴方向：Edith AI 系统开发
- 沟通偏好：复杂任务先列步骤再动手，每步汇报

---

## 项目清单

### 1. 番茄小说大纲
- **状态**：已终止 ❌（2026-04-06 删除）
- **原进度**：完成43章后果断终止，删除全部内容
- **位置**：`~/Desktop/番茄小说大纲/`（已删除）
- **设定**：都市重生+系统流+后宫，6个女主
- **终止原因**：用户在"兴趣探索"与"聚焦主业"间做出明确取舍
- **已完成**：
  - AI味词汇清理（第2章3处、第4章2处）
  - 第一部分"重生觉醒"（1-20章）
  - 第二部分"校园称霸"21-40章
- **启示**：果断止损，不做沉没成本留恋

### 2. Agent工厂（Agent Builder）
- **状态**：开发中 🔨（2026-04-15启动）
- **定位**：一句话生成可运行的OpenClaw Agent Skill
- **用户需求**：独立桌面版（双击可用）+ 本地MLX模型推理 + 直接切换agent的独立窗口
- **技术路线**：对话式需求收集 → Python模板生成 → 自动安装
- **长期愿景**：脱离OpenClaw的独立桌面工具，使用本地LLM API（通义千问/OpenAI/Qwen3.5-4B MLX）
- **触发词**：「造一个Agent」「创建一个智能体」

### 3. 有声书主播AI协作计划
- **状态**：待启动
- **用户声音**：青年音、温暖、阳光
- **规划**：12周三阶段（克隆声音→提升产能→打造IP）
- **启动信号**：用户说"开始第一阶段"

### 4. 置地有声后期工作室
- **状态**：运营中（实体业务）
- **业务**：音频后期制作
- **规模**：服务14个剧组
- **工具**：后期音频结算系统（8502端口）
- **特点**：测试到投产仅1天，决策-执行链路极短

### 5. MLX 本地模型部署
- **状态**：已完成 ✅（2026-04-06 部署成功）
- **模型**：Qwen3.5-4B-mlx-vlm（约 5.5GB）
- **位置**：`~/.qclaw/workspace/skills/mlx-fallback/`
- **用途**：云API额度用完时的 fallback
- **脚本**：check_model.py、chat.py、test_image.py、fallback.py
- **张二壳知识手册**（2026-04-25完成注入）：system prompt 已扩展至~2200字，覆盖用户档案/4个项目/记账铁律/工具速查/沟通风格/重要教训
- **云端守护脚本** cloud_sentinel.py（2026-04-25部署→2026-04-29关闭）：每60秒检测云端API，连续3次失败自动切换至 zhangerkq provider + 重启 gateway。因8GB Mac无法同时跑MLX+其他服务，全自动守护价值有限，用户决定关闭（launchctl unload）。脚本保留在 `~/.qclaw/workspace/skills/mlx-fallback/scripts/cloud_sentinel.py`，需要时可 `--install` 重新启用
- **QwenPaw 已卸载**（2026-04-25）：8GB RAM 无法同时跑 MLX+QwenPaw，内存压力导致重启。MLX 单独使用足够
- **验证**：2026-04-06 成功切换并测试本地模型
- **注意**：切换本地模型后记忆能力不变，只是换了"思考的大脑"

### 6. 音频计费系统（有声书）
- **状态**：封存（核心完成，待优化）
- **位置**：`~/.qclaw/workspace/audio_billing/`
- **用途**：有声书台词计费（CV配音、Whisper转写、Embedding语义匹配角色）
- **启动**：`cd ~/.qclaw/workspace/audio_billing && streamlit run app.py`
- **访问**：http://localhost:8501

### 7. 后期音频结算系统
- **状态**：已完成 ✅
- **位置**：`~/.qclaw/workspace/audio_settlement/`
- **访问**：http://localhost:8502
- **功能**：后期音频时长结算，支持Excel表格+MP3/WAV
- **支持格式**：小数集数、中文数字、中文顿号、WAV格式
- **测试结果**：19/19 完美匹配

### 8. 机械臂项目
- **状态**：滑杆控制demo进行中（2026-04-23）
- **最终选择**：方案B（Arduino+舵机自制），¥1000预算内
- **调整**：原含遥操作（模仿手臂动作），因复杂度过高放弃，改为先做滑杆控制demo
- **用户需求**：遥操作+零基础但要实体成品+进阶功能，后简化为零基础实体成品
- **历史方案**：四阶段方案（入门验证→IK→视觉→APP），总预算2000–3600元
- **最高风险**：复杂度膨胀，预算超支

### 9. 记账系统 3.0（重大升级 2026-04-12）

**核心文件**：
- `~/.qclaw/workspace/data/ledger.json` — 账本（金额已迁移为分整数存储）
- `~/.qclaw/workspace/data/ledger.py` — 核心操作层（唯一写入入口）
- `~/.qclaw/workspace/data/correction_rules.json` — 自我学习规则
- `~/.qclaw/workspace/data/to_excel.py` — Excel 导出

**架构变更**：
- ✅ 金额存分（整数），彻底消除浮点精度问题
- ✅ 语义强绑定：note含「预算外/报销/代付」→ 自动 in_budget=False
- ✅ 自我学习：用户纠正时自动追加规则到 correction_rules.json
- ✅ 待确认抽屉：OCR条目先进抽屉，微信DM确认后才入账

**学习规则**（种子 3 条）：洗手液/逗猫棒/女士睡衣 → 预算外

**Excel**：桌面 `4月账单_最新.xlsx`，新增「来源」列

**P2 流程**：截图→OCR→入待确认抽屉→微信DM→「确认N」入账 / 「跳过N」丢弃

**用户明确规则**：**默认预算内，只有用户说"算预算外"才算预算外**，不要自行判断

**4月核查教训**：
- OCR 日期识别易错（截图重叠导致4/10→4/11），每条必须先确认日期
- 录账前必须先确认「预算内/预算外/报销相抵」三类
- 不要闷头入库，每录一条都等用户确认
- 山姆购物顺手买的零食/食品不计预算内
- AI先确认日期时间再录入，避免日期混淆（2026-04-19教训）

**周预算制**（2026-04-14起）：
- 每周预算 ¥1000
- **重置节奏由用户控制**：每周二晚上用户主动提醒，壳壳不主动干预预算重置
- 旧账本存档：`ledger_2026_04_archived_1776162449.json`（4月1-14日，47条，预算内¥933.46，预算外¥545.23）
- 新账本：`ledger.json`（空白，周预算¥1000）
- Excel存档：桌面 `第16周账单_2026-04-14~04-20.xlsx`
- **账本差额悬而未决**（2026-04-25）：账本¥395.27 vs 微信¥323.17，差¥72.10；已确认拼多多多记¥23.45；¥48.65来源不明（用户说"差不多就行"）

---
- 联合会诊 Skill 已扩展至13科（新增肥胖科、减重科、营养科），核心原则：单科能解决的不硬凑四科

## 知识库架构

### IMA 知识库（云端，存细节）
- **凭证位置**：`~/Library/Application Support/QClaw/openclaw/config/skills/ima/client_id` + `api_key`
- **笔记本列表**：
  1. 📋 个人档案（note_id: 7445487753888816）
  2. 🚀 项目清单（note_id: 7445487800025530）
  3. 🛠 工具配置（note_id: 7445487821022408）
  4. 💡 灵感备忘（note_id: 7445487858747880）
  5. 📝 工作日志（note_id: 7445487930073705）
- **使用原则**：概要存 MEMORY.md，细节存 IMA
- **番茄小说大纲不同步 IMA**，直接看电脑文件

### 本地记忆（MEMORY.md，存概要）
- 概要、索引、快速检索
- 项目状态一行摘要

### 记忆宫殿流程
- **时机**：重要对话结束时主动整理（不等压缩）
- **触发**：用户说"整理一下"或我判断对话有重要内容
- **职责**：整理当前对话（当下），auto-dream 整理 daily logs（过去）
- **流程**：大纲 → MEMORY.md（本地），详细 → IMA（云端）
- **标记**：整理后在 daily log 标记 `<!-- consolidated -->`
- **优点**：压缩后只留大纲省 token，详细云端备份不丢失
- 详见 IMA「灵感备忘」笔记

---

## 系统

### 伊迪丝（EDITH）
- 触发词：「唤醒伊迪丝」「启动EDITH」开启，「关闭伊迪丝」关闭
- 人格架构：SOUL.md（核心人格） + persona.md（用户画像）
- 12个部门：枢密院、督察院、产品部、工部、通商部等
- 知识库在 `~/.openclaw/team_knowledge/`
- 治理特点：多部门制衡架构（类似三权分立）
- 详细规则见 SOUL.md

### 伊迪丝（EDITH）系统优化（2026-04-22~23）
- **原始问题**：角色卡加载太重，实测28.2k tokens输入→886 tokens输出→2分钟超时
- **重构成果**（2026-04-22）：
  - SKILL.md：396行→104行（-74%），总量1782→1078行（-39%）
  - 督察院.md吸收错误响应SOP+升级机制（74→95行），门下省.md精简（124→87行）
  - 用户明确12部门不合并，产品部职责修正（市场视角≠枢密院需求拆解）
- **性能对比**：输入Token 28.2k→22.4k（-20%），输出Token 886→2500-3200（+185%~261%），超时→1分28秒
- **四步优化完成**：按需加载规则上线、知识库扩容（药物交互8→35条+ICD全13科+检查参考12科49项）、SKILL.md精简、病例存储目录建立
- **自检+9项修复**：SKILL.md加L1-L4分级表、调度器新增依赖注入规范、通商部加信息来源速查表、工部加超时重试规范、新建学习日志.md
- **用户明确伊迪丝定位**：复杂任务走最高质量路径，简单任务问壳壳，不需要任务分级机制
- **当前状态**（2026-04-23极端测试后）：
  - 完成率从50%→100%（4部门并行测试）
  - SKILL.md：157行
  - 角色卡：13个（含调度器、学习日志），总计841行
  - 部门超时预设：枢密院180s/工部180s/通商部150s/产品部120s/其他120s
  - 工部超时建议提到240s（180s只够第一阶段：Schema+函数签名）
- **学习日志**：`roles/学习日志.md`
- **最新备份**：`~/Desktop/edith-backup-20260423-000704/`
- **极端测试验证**（2026-04-23）：完成率50%→100%，4部门并行稳定，SKILL.md 157行，角色卡13个841行
- **aggregator.py修复**：顶部添加 `import sys`（sys模块仅在底部导入，import模式无法使用）
- **P0漏洞修复**（2026-04-24）：①审核分级安全盲区（新增🟡中风险-系统等级，修改系统配置→督察院+刑部轻量审查）②工部时间缓冲（300→330秒+30秒缓冲阶段）③错误处理SOP统一（决策树SKILL.md与调度器一致化）

### 环境信息
- macOS arm64，Python 3.13
- OpenClaw 运行在 QClaw Electron

### IMA OpenAPI 凭证
- 已配置（2026-04-02）
- 存储位置：`~/Library/Application Support/QClaw/openclaw/config/skills/ima/`

---
- 伊迪丝只有分理能力（任务拆解、流程约束、记忆隔离），没有强化能力；真正增强需走四条路径：知识库外挂、专用工具、模型分层、跨部门并行

## 用户个人
- 皖南川藏线自驾 4/18-20（已完成）
- 皖南攻略初稿：`皖南川藏线自驾攻略（不爬山版）.xlsx` 已生成（2026-04-09）
- 座驾：特斯拉 Model Y
- 创业补贴：2026-04-06 首次查询无锡惠山区创业补贴政策

---
- 对AI本质、神经可塑性、脑机接口有深度兴趣，关注人机共生与道家思想×科技交叉（2026-04-15深度对话）
- 用户即将结婚

## 回青岛待办（过几天，具体日期待定）
- 🌶️ 去融创吃酸菜
- 💻 回家拿苹果小电脑和显示器
- 🧥 拿羽绒服回来
- 🧹 拿一个除螨仪
- 🫗 拿香油带回青岛
- 备注：想起来再补充

## 待探索地点
- **十五大街农贸市场**（青岛）
  - 📍 山东省青岛市市北区明霞路37号
  - ⏰ 06:00-18:00
  - ⭐ 4.7分，扫街榜市北区集市场第3名，价格便宜
  - 备注：用户想去（2026-04-21）

## 技术研究

### 大模型本地微调路径（2026-04-15）
- **状态**：调研完成，待启动
- **三层方案**：Fine-tuning（微调）、Train from Scratch（从零训练）、LoRA/QLoRA（轻量微调）
- **当前硬件**：Mac M系列芯片 + MLX框架 + Qwen3.5-4B MLX模型
- **最小可行实验**：用LoRA微调一个「张壳壳风格版」，数据来源为工作室聊天记录
- **方向确认**：AI应用落地走智能体开发路线更实用，不需要训练自己的大模型，可在现有模型基础上搭应用层

### 苹果设备「二合一」探索（搁置）
- **状态**：搁置
- **历程**：用户想用 Exo 框架将两台 8GB Mac 组集群跑分布式推理，突破内存限制
- **结论**：Exo 理论上可行（pipeline parallelism 层切分），但设置复杂度高，8GB+8GB≠16GB可用内存（模型权重需完整加载）
- **替代建议**：M4 Mac Mini 16G(¥3000+)/32G(¥4000+)是最优路径
- **Exo 安装**：因 uv/rust/macmon 依赖未安装完而中断，用户未决定是否继续

### 分布式AI Agent网络（2026-04-15）
- **架构**：Mac Mini为主节点（常驻7×24）+ 多终端（手机/电脑/树莓派）接入MLX本地模型
- **调度层**：通过OpenClaw统一调度各终端Agent
- **能力边界**：能实现分布式终端操作和应急备份协议；无法做到硬件级系统底层改写
- **进度**：Mac Mini即将到位，待设备到达后部署OpenClaw常驻节点

### 张二壳配置调试（2026-04-10）
- **状态**：已完成 ✅
- **问题**：`session_status` 工具报错 "Model not allowed" for zhangerkq
- **根因**：Gateway 进程内存缓存旧配置（不含 zhangerkq 白名单）
- **解决**：删除 `~/.openclaw/openclaw.json` 中 `agents.defaults.models` allowlist，使 `allowAny=true`
- **API 服务**：http://127.0.0.1:18793，Qwen3.5 4B MLX，已验证可用
- **三角色定位**：壳壳（云端大模型/本体）+ 伊迪丝（多部门协作模式）+ 张二壳（本地轻量模型/工具优先）

### Claude Code 源码研读（2026-04-08）
- **状态**：全部完成 ✅
- **源码来源**：v2.1.88 源码泄露（2026-03-31）
- **研读范围**：核心模块 10,497 行 TypeScript
- **提炼成果**：
  - Feature Flags 系统 ✅ 已封装成 Skill
  - 上下文自动注入 ✅ 已封装成 Skill
  - 权限系统双层架构 ✅ 已封装成 Skill
  - Generator 流式查询 ✅ 已封装成 Skill
- **Skill 位置**：`~/.openclaw/workspace/skills/`（4个 Skill）
- **配置位置**：`~/.qclaw/features.json`
- **启示**：编译时裁剪、流式输出、权限分层、Skill 封装自动加载

### Coze Space 2.5 / Agent World（字节）
- **状态**：已了解（2026-04-12）
- **发布时间**：2026-04-07
- **内容**：字节新一代 Agent 开发平台

### Qwen3.6-35B-A3B 开源（2026-04-18）
- **架构**：MoE，总参350亿激活30亿
- **能力**：智能体编程+多模态感知
- **Mac可用性**：MLX框架理论可跑，量化后约15-20GB显存需求
- **关注**：MoE架构在端侧的可行性，与Agent工厂本地推理方案相关

### Zvec 向量库实测（2026-04-17）
- **版本**：v0.3.0
- **核心发现**：文档与实现严重不符，必须实测验证
- **关键规则**：PK必须STRING、doc.fields赋值、query必须传list非np.array、zvec.open()替代create_and_open()、col.close()不存在
- ### 全球局势分析 Skill（Global Intelligence）
- **版本**：v3.0（2026-04-29升级）
- **核心升级**：新增Politico政治现实校验器（第9维专家），冲突区双基线（现状延续40%+升级30%+缓和30%），月度反馈校准闭环
- **Politico定位**：政治压力测试专家，识别假设盲区、补充被忽视的政治变量、量化概率修正，不是唱反调
- **设计哲学**：准确是唯一标准，不是为了自嗨
- **中东预测准确率评估**（v2.2）：宏观趋势~70%，短期政治~20%，综合40-50%
- **位置**：~/.openclaw/workspace/skills/global-intelligence/
- **架构**：9维专家(QClaw sessions_spawn) + 双犹太智囊 + ProSearch 情报 + Zvec 向量存储 + Politico独立校验层
- **核心文件**：
  - main.py — CLI 入口
  - scripts/aggregator.py — 情报抓取
  - scripts/analyzer.py — prompt构建器 + LLM解析器
  - scripts/jewish_council.py — 结构化汇总 + 规则推演
  - scripts/reporter.py — 报告生成
  - scripts/validate_report.py — 13条校验规则
  - personas/*.json — 9个专家人设
  - config/sources.json — 搜索关键词配置
- **QClaw调用性能**：8次并行，每次<5秒，总计<1分钟
- **v3.0中东复测**（2026-04-29）：冲突区默认升级逻辑生效，Politico识别内塔尼亚胡司法腐败案动机，双基线取代乐观默认
- **预测偏差对比**（2026-05-01）：用户指出前几天预测报告与目前实际情况存在偏差，需对比分析偏差内容

---
- DeepSeek V4于2026-04-24发布并开源，含V4-Pro（1.6万亿总参/490亿激活）和V4-Flash（1万亿总参/370亿激活）两个版本，上下文100万tokens，Agent能力大幅提升

### ProSearch 与独立搜索入口（2026-05-01）
- **ProSearch本质**：QClaw内置联网搜索，走网关认证，17引擎（8国内+9国际），无需额外安装
- **用户需求**：想做一个独立运行的搜索入口（不依赖QClaw对话界面）
- **方案A**：脚本调QClaw ProSearch（类似GI aggregator.py），简单但离不开网关
- **方案B**：searXNG自托管搜索引擎（Docker一键部署，完全独立，隐私友好）
- **RSS源已全被墙**（BBC/CNN/Reuters/Guardian），ProSearch可替代RSS做情报采集
- **状态**：等Mac Mini到位再考虑部署searXNG

### Hermes Agent / 赫尔摩斯智能体（2026-04-25）
- **状态**：已安装，待初始化
- **来源**：ClawHub（QClaw技能市场），基于 [NousResearch Hermes](https://github.com/NousResearch/Hermes)（53K star）
- **已安装**：hermes-agent（学习型循环，记忆→反思→技能晋升）+ hermes-full（协作进化架构，偏概念层需CLI）
- **路径**：`~/.qclaw/skills/hermes-agent/`、`~/.qclaw/skills/hermes-full/`
- **核心能力**：工作前读记忆→不重复犯错，做完写反思→教训变规则，成功3次→自动晋升技能
- **与OpenClaw区别**：Hermes是跑在OpenClaw里的学习型智能体，具有记忆反思和技能自动晋升机制；OpenClaw是底层调度平台
- **新电脑安装计划**（2026-05-02）：用户另一台电脑（16GB），建议官方命令安装：`curl -fsSL https://raw.githubusercontent.com/NousResearch/hermes-agent/main/scripts/install.sh | bash`
- **待办**：初始化 `~/hermes-agent/` 目录（用户尚未确认）
- **当前总技能数**：52个
- 用户于 2026-05-01 指出 GI 预测报告与实际发展存在偏差，分析师需对比分析偏差内容（待完成）

## Skills

### 全球局势分析 Skill（Global Intelligence）
- Global Intelligence Skill 升级至 v2.0（2026-04-18），团队制重构：10维专家分4团队（地缘战略/经济资源/安全军事/舆情中国），新增海运物流师（Mariner）和海事安全官（Admiral）
- **位置**：~/.openclaw/workspace/skills/global-intelligence/
- **架构**：8维专家(QClaw sessions_spawn) + 双犹太智囊 + ProSearch 情报 + Zvec 向量存储
- **核心文件**：
  - main.py — CLI 入口（数据准备，不含推理）
  - scripts/aggregator.py — 情报抓取（ProSearch搜索，RSS已移除因被墙）
  - scripts/analyzer.py — prompt构建器 + LLM解析器（供sessions_spawn使用）
  - scripts/jewish_council.py — 结构化汇总 + 规则推演
  - scripts/reporter.py — 报告生成
  - scripts/vector_store.py — Zvec 向量存储
  - personas/*.json — 8个专家人设（persona.identity 嵌套结构）
  - config/sources.json — 搜索关键词配置
- **MLX 服务**：已弃用，MLX 不再维护
- **Zvec API 实测要点**：
  - PK 必须是 STRING（int 报 TypeError）
  - doc.fields['key'] = value, doc.vectors['vec'] = np.array
  - Collection.query(vectors=[VectorQuery(...)], topk=N, filter=...)
  - 传 np.array 有 bool bug，必须转 list
  - zvec.open() 用于打开已存在集合（create_and_open() 路径冲突）
- **嵌入优先级**：Zvec-Qwen → DashScope → OpenAI → MLX → 随机（当前随机，无DashScope Key）
- **升级日志（2026-04-18 v1.0）**：
  - 移除MLX fallback，Python脚本改为纯数据工具
  - AI agent通过sessions_spawn驱动全流程
  - analyzer.py重写为prompt构建器
  - aggregator重写（去RSS+关键词扩展）
  - reporter增加自动去重
  - 清理3份测试历史报告
- **升级日志（2026-04-17 v0.3）**：
  - analyzer: 规则引擎→LLM驱动，persona字段规范化（`_normalize_persona`处理嵌套`persona.identity`），prompt注入identity/expertise/framework/style
  - aggregator: 过滤逻辑简化为子串匹配，RSS已移除（被墙），保底展示全部搜索结果
  - vector_store: zvec.open()替代create_and_open()，Zvec QwenDenseEmbedding集成，10KB模块
  - jewish_council: 风险等级计入↗️升温
  - reporter: 中文变量名bug修复（worsen_count/improve_count），章节序号修正
  - 清理：scripts/jewish-council.py残留、scripts/data/vectors/测试产物、test_output/
- **QClaw调用性能**：8次并行，每次<5秒，总计<1分钟
- **记忆污染方案**：方案B隔离调度员架构——spawn独立调度员管理子智能体，结果不回流主会话，防止上下文膨胀；伊迪丝系统也采用同机制
- **测试验证（2026-04-17）**：台海局势端到端测试通过（8维分析+双智囊+向量存储+报告生成）
- **遗留**：
  - embed_text()降级为随机向量（需DashScope或OpenAI API Key）
  - 趋势解析：LLM输出`"🔴升温"`含引号，已加容错
  - Zvec内嵌Qwen需DashScope Key才生效
- **超时配置**（2026-04-23）：全链路统一300s，解决子任务超时问题
- **完整测试验证**（2026-04-23）：aggregator✅/analyzer✅/reporter✅，中美局势分析完整报告生成
- **生产级报告**（2026-04-23）：第二次完整工作流2分6秒，输出 `global-intelligence-report_2026-04-23_1118.md`
- **核心结论**（2026-04-23）：中美脱钩结构性不可逆，台海最大灰犀牛，稀土中方核心杠杆
- **伊迪丝三部门评估**（2026-04-23）：枢密院✅/督察院🟡/刑部🢢，GI Skill「可用偏中」
- **GI Skill待修复**：①行动建议补负责人+验收标准 ②概率数字补充来源说明
- **三大优化项目收尾**（2026-04-23）：伊迪丝✅/MDT会诊✅/GI Skill✅，全部可交付

### Agent工厂（Agent Builder Skill）
- **状态**：开发中 🔨（2026-04-15启动）
- **位置**：`~/.qclaw/workspace/skills/agent-factory/`
- **定位**：用Python代码生成新Agent，对话式+问卷式需求收集，自动安装到OpenClaw
- **核心模块**：元Agent接收需求 → Python模板库 → 文件生成器 → 自动安装器
- **最小可行版**：对话问卷工作流 + 1个通用对话型模板 + 生成+安装脚本
- **目标输出**：用户说需求 → 自动生成可运行的OpenClaw Skill
- **用户明确**：想要定制智能体，支持按需定制；生成的agent目前是OpenClaw专属格式
- **长期目标**：独立桌面版（双击可运行）+ 本地MLX模型推理 + 直接切换agent的独立窗口
- **触发词**：用户说「造一个Agent」「创建一个智能体」

### travel-planner（旅行规划）
- **状态**：已完成 ✅（2026-04-09）
- **位置**：`~/.qclaw/skills/travel-planner/`
- **打包文件**：`~/Desktop/travel-planner.skill`
- **触发条件**：用户说「帮我规划XX旅行」「做个旅行攻略」
- **工作流程**：
  1. 自动发送前置问卷（见 `references/questionnaire.md`）
  2. 收集必要信息（出发地、目的地、天数、人数、预算、自驾/公交、爬山偏好、收费景点态度）
  3. 生成xlsx攻略表格（见 `assets/travel-template.xlsx`）
- **表格内容**：基本信息、每日行程、景点门票（可选项）、住宿推荐、费用明细、重要电话、充电提示、出行准备、紧急备案
- **核心理念**：车能到的地方都去，不爬山，简单溜达，收费景点可进可不进

---

## 联合会诊（医疗健康 Skill）
- **状态**：优化中
- **核心原则**：单科能解决的不硬凑四科
- **规模**：10科（含心脏/呼吸/肾脏/急诊重症，2026-04-14扩展），后扩展至13科（新增肥胖科、减重科、营养科）
- **数据库接入**：PubMed / ClinicalTrials / OpenFDA（2026-04-14完成）
- **已修复**：drug_interactions.json bug（2026-04-14）
- **输出优化**（2026-04-14）：
  - 直接给结论+具体方案（方案A/B/C，含做什么/怎么做/频率/去哪做/费用/医生需确认）
  - 完整PDF诊断书按需生成，不每次都输出
  - 砍掉：共识与分歧、证据等级说明表、重复性免责声明
- **病例存储**：`data/medical_cases/` 目录
- **典型病例**：糖尿病视网膜脱离术后视力波动（2026-04-14），结论为器质性+功能性叠加
- **待存储病例**：女性30岁，眼科手术+减肥，同一人
- **病例存储目录**：`data/medical_cases/` 已建立

### QClaw 计费透明度
- Agent无法访问历史token消耗账单（session_status仅当前会话实时数据）
- QClaw计费体系对内部agent不透明（1积分=?token 未知）
- 用户需通过官方客户端积分/套餐页面查权威账单

### 跨 Channel 架构限制
- webchat和微信是不同channel，各有独立LCM和上下文，互不共享
- 用户在微信问任务，webchat会话看不到 → 跨channel协作需人工转达或统一入口
- 微信端完成的任务，其他端看不到结果
- 解决方案：task-summary文件或LCM摘要同步

### 系统 Bug 记录
- **QClaw 内部推理泄露**（2026-04-14）：用户在对话中看到英文内容，系内部推理过程被系统泄露到对话界面，属 OpenClaw/QClaw 消息发送逻辑 Bug，待官方修复
- **微信会话 context_window_exceeded**（2026-04-22）：旧会话LCM残留7.5M tokens数据注入新会话致崩溃，已清理，增加LCM健康监控（一周一次）

---

## 待办与开放线程

### 值得精简
- [ ] MLX本地模型部署——几乎未使用，考虑精简或移除
- [ ] IMA残留——清理不再使用的IMA相关配置
- [ ] 龙虾安装包——中断任务，需决定是否继续

### 需定夺
- [ ] Agent工厂长期目标与架构冲突——独立桌面版 vs OpenClaw Skill 格式的优先级
- [x] 伊迪丝部门架构简化——用户明确不合并，12部门保留（2026-04-22）
- [ ] 联合会诊按需加载优化——13科全量加载消耗资源
- [ ] 伊迪丝方案③（预合成上下文，枢密院/工部指令内嵌SKILL.md）——待决策（当前104行已够用，可暂缓）

### 长期待推进
- [ ] 有声书主播AI协作计划——待启动超过30天，需用户明确时机
- [ ] MLX Fallback自动切换——等待QClaw API检测支持
- [ ] DashScope API Key——GI语义检索和Zvec嵌入的前提条件
- [ ] GI Skill修复——行动建议结构+概率来源（本周内，2026-04-23评估）
- [ ] 记账系统自动导出Excel + 周日晚提醒
- [ ] 机械臂项目——待用户确认具体用途后再启动
- [ ] hermes-agent初始化——已安装，待初始化 ~/hermes-agent/ 目录（2026-04-25，用户尚未确认）

---

## 小米 MiMo Orbit 申请（2026-04-29）
- **活动**：小米百万Token创造者激励计划（2026.4.28-5.28）
- **申请地址**：https://mimo.cn
- **使用证明材料**（3份Word文档，桌面）：
  1. 置地有声工作室_AI工具体系.docx（14剧组、结算8502、音频计费8501、AI工作流）
  2. EDITH智能商业系统.docx（十二部门、13科会诊、GI Skill、性能数据）
  3. AI个人效率工具与自动化.docx（记账3.0、周预算、OCR入账、MLX、知识管理）
- **状态**：用户其他部分还没填完，等用户发来一起润色

---

_Last updated: 2026-05-02（Dream #25）_
