# 可视化面板CSS改进速查

## 脉冲动画（当前步骤高亮）
```css
@keyframes pulse {
  0% { box-shadow: 0 0 0 0 rgba(104, 179, 176, 0.4); }
  70% { box-shadow: 0 0 0 12px rgba(104, 179, 176, 0); }
  100% { box-shadow: 0 0 0 0 rgba(104, 179, 176, 0); }
}

.phase-step.active {
  transform: scale(1.1);
  z-index: 2;
}
.phase-step.active .phase-circle {
  background: var(--green-dark);
  color: var(--white);
  animation: pulse 2s infinite;
}
```

## 流程连接线
```css
.phases { position: relative; }
.phases::before {  /* 渐变底线 */
  content: '';
  position: absolute;
  top: 28px; left: 20px; right: 20px;
  height: 2px;
  background: linear-gradient(90deg, var(--green), var(--sky), var(--willow));
  opacity: 0.2;
  z-index: 0;
}
.phase-circle { position: relative; z-index: 1; }  /* 圆圈在线上层 */
.phase-step:not(:last-child)::after {  /* 箭头连接 */
  content: '→';
  position: absolute;
  right: -8px; top: 18px;
  color: var(--green); opacity: 0.5;
}
/* 换行处断开：第N个步骤 content:'' */
```

## 三栏色彩体系
```css
#dept-panel h2 { border-color: var(--willow); }
#dept-panel h2::before { background: var(--willow); }
.grid>.card:nth-child(2) h2 { border-color: var(--sky); }
.grid>.card:nth-child(2) h2::before { background: var(--sky); }
.grid>.card:last-child h2 { border-color: var(--gold); }
.grid>.card:last-child h2::before { background: var(--gold); }
```

## 按钮实色+操作反馈
```css
.demo-bar button {
  background: var(--green-dark);
  color: var(--white);
  border: none;
  font-weight: 600;
}
```
```javascript
// JS: 按钮反馈
var btns = document.querySelectorAll('.demo-bar button');
btns.forEach(function(b) { b.disabled = true; b.style.opacity = '0.6'; });
clicked.textContent = '处理中…';
// 完成后 restoreBtns()
```

## 发言者标签化
```css
.disc-bubble .speaker {
  display: inline-block;
  background: var(--green-dark);
  color: var(--white);
  padding: 2px 8px;
  border-radius: 12px;
  font-size: 0.75em;
  font-weight: 600;
}
```

## 里程碑弹跳
```css
@keyframes bounce {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-4px); }
}
.mile.active { animation: bounce 1s ease infinite; }
```

## 验证方法
```javascript
// getComputedStyle 验证颜色（browser_vision 看不出细微色差）
var el = document.querySelector('#dept-panel h2');
getComputedStyle(el).borderBottomColor;  // → rgb(120, 146, 98)
```
