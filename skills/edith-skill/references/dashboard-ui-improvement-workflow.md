# 可视化面板UI改进工作流

## 何时触发

用户要求评估/改进可视化面板的UI、美术设计、用户体验时使用此流程。

## 工作流

### 1. 截图+代码双取证

```
browser_navigate → browser_vision(question="分析UI设计…") → read_file(index.html)
```

必须同时获取：
- 视觉截图（整体布局、配色、动效）
- 完整HTML/CSS/JS代码（精确修改依据）

### 2. 并行派部门评估

美术设计 + 市场运营部并行执行：

```python
# 美术设计：视觉层面
delegate_task(goal="评估UI美术设计", context="知识库+截图路径+HTML路径", toolsets=["vision","file"])

# 市场运营部：体验层面
delegate_task(goal="评估用户体验", context="知识库+截图路径+HTML路径", toolsets=["vision","file"])
```

**注意**：LongCat并行≤3个（429限流）。如果一个429失败，用MiMo重试。

### 3. 综合评判+分级

将两部门评估结果综合，按优先级分级：
- P0 必改（影响可用性/视觉层次）
- P1 建议改（提升体验）
- P2 锦上添花（可选优化）

### 4. 向用户汇报，确认后执行

**关键**：用户可能排除某些P0项（如"不要新手引导"）。等确认再执行。

### 5. CSS级修改技巧

面板是单文件HTML（~900行），CSS+JS全在`<style>`和`<script>`标签内。

#### 流程连接线模式

```css
/* 水平底线条 */
.phases { position:relative; }
.phases::before {
  content:''; position:absolute; top:28px; left:20px; right:20px;
  height:2px; background:linear-gradient(90deg,var(--green),var(--sky),var(--willow));
  opacity:0.2; z-index:0;
}

/* 步骤间箭头 */
.phase-step:not(:last-child)::after {
  content:'→'; position:absolute; right:-8px; top:18px;
  color:var(--green); opacity:0.5;
}
.phase-circle { position:relative; z-index:1; } /* 圆圈在线上方 */
```

#### 当前步骤高亮模式

```css
.phase-step.active { transform:scale(1.1); z-index:2; }
.phase-step.active .phase-circle {
  background:var(--green-dark); color:var(--white);
  animation:pulse 2s infinite;
}
@keyframes pulse {
  0% { box-shadow:0 0 0 0 rgba(104,179,176,0.4); }
  70% { box-shadow:0 0 0 12px rgba(104,179,176,0); }
  100% { box-shadow:0 0 0 0 rgba(104,179,176,0); }
}
```

#### 三栏色彩体系

```css
#dept-panel h2 { border-color:var(--willow); }  /* 左=柳绿 */
#dept-panel h2::before { background:var(--willow); }
.grid>.card:nth-child(2) h2 { border-color:var(--sky); }  /* 中=天青 */
.grid>.card:nth-child(2) h2::before { background:var(--sky); }
.grid>.card:last-child h2 { border-color:var(--gold); }  /* 右=金色 */
.grid>.card:last-child h2::before { background:var(--gold); }
```

#### 发言者标签化

```css
.disc-bubble .speaker {
  display:inline-block; background:var(--green-dark);
  color:var(--white); padding:2px 8px; border-radius:12px;
  font-size:.75em; font-weight:600;
}
```

#### 按钮操作反馈（JS）

```javascript
function demo(mode){
  var btns=document.querySelectorAll('.demo-bar button');
  btns.forEach(function(b){b.disabled=true;b.style.opacity='0.6'});
  var clicked=event?event.target:btns[0];
  clicked.textContent='处理中…';
  // ... 执行逻辑 ...
  // 最终：.then(function(){restoreBtns()}).catch(function(){restoreBtns()});
}
function restoreBtns(){
  document.querySelectorAll('.demo-bar button').forEach(function(b,i){
    b.disabled=false;b.style.opacity='1';
    if(i===0)b.textContent='▶ 模拟开始';
    else if(i===1)b.textContent='▶ 模拟完整流程';
    else if(i===2)b.textContent='🔄 重置';
  });
}
```

### 6. 验证方法

#### ⚠️ 视觉分析工具不可靠验证颜色差异

`browser_vision` 无法区分细微色差（柳绿/天青/金色都被报告为"相同的绿色"）。

**正确验证方法**：用 `browser_console` 检查计算样式：

```javascript
var h2_1 = document.querySelector('#dept-panel h2');
var h2_2 = document.querySelector('.grid>.card:nth-child(2) h2');
JSON.stringify({
  dept: getComputedStyle(h2_1).borderBottomColor,
  flow: getComputedStyle(h2_2).borderBottomColor
});
```

#### 修改后必须

1. `curl http://localhost:8080` 确认页面加载
2. `browser_console` 检查关键CSS变量是否生效
3. 点击模拟按钮验证动效和交互反馈

### 7. 重启Flask

```bash
lsof -i :8080 | grep LISTEN | awk '{print $2}' | xargs kill -9 2>/dev/null
# 用 terminal(background=true) 启动
cd ~/.hermes/edith-dashboard && source venv/bin/activate && python server.py
```
