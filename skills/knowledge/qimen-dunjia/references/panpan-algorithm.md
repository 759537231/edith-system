# 奇门遁甲排盘算法（JavaScript）

## 核心数据结构

```javascript
// 天干
const TIAN_GAN = ['甲', '乙', '丙', '丁', '戊', '己', '庚', '辛', '壬', '癸'];

// 地支
const DI_ZHI = ['子', '丑', '寅', '卯', '辰', '巳', '午', '未', '申', '酉', '戌', '亥'];

// 八门
const BA_MEN = ['开门', '休门', '生门', '伤门', '杜门', '景门', '死门', '惊门'];

// 八门吉凶
const MEN_JI_XIONG = {
    '开门': 'ji',
    '休门': 'ji',
    '生门': 'ji',
    '伤门': 'xiong',
    '杜门': 'xiong',
    '景门': 'zhong',
    '死门': 'xiong',
    '惊门': 'xiong'
};

// 九星
const JIU_XING = ['天蓬', '天芮', '天冲', '天辅', '天禽', '天心', '天柱', '天任', '天英'];

// 八神
const BA_SHEN = ['值符', '腾蛇', '太阴', '六合', '白虎', '玄武', '九地', '九天'];

// 三奇六仪
const SAN_QI_LIU_YI = ['戊', '己', '庚', '辛', '壬', '癸', '丁', '丙', '乙'];

// 九宫顺序（洛书）
const JIU_GONG_ORDER = ['坎一', '坤二', '震三', '巽四', '中五', '乾六', '兑七', '艮八', '离九'];
```

## 核心函数

### 真太阳时计算

```javascript
function getTrueSolarTime(datetime, longitude) {
    // 北京时间基于东经120度
    const timeDiff = (longitude - 120) * 4; // 分钟
    const trueSolarTime = new Date(datetime.getTime() + timeDiff * 60 * 1000);
    return trueSolarTime;
}
```

### 时辰计算

```javascript
function getShichen(datetime) {
    const hour = datetime.getHours();
    const shichenIndex = Math.floor((hour + 1) / 2) % 12;
    return DI_ZHI[shichenIndex];
}
```

### 日干支计算

```javascript
function getDayGanZhi(datetime) {
    // 基于已知基准日推算
    // 2026-01-01 是甲子日
    const baseDate = new Date(2026, 0, 1);
    const daysDiff = Math.floor((datetime - baseDate) / (24 * 60 * 60 * 1000));
    const ganIndex = daysDiff % 10;
    const zhiIndex = daysDiff % 12;
    return TIAN_GAN[ganIndex] + DI_ZHI[zhiIndex];
}
```

### 时干支计算

```javascript
function getHourGanZhi(datetime) {
    const dayGan = getDayGanZhi(datetime).charAt(0);
    const shichen = getShichen(datetime);
    
    // 日干起时干口诀
    // 甲己还加甲，乙庚丙作初，丙辛从戊起，丁壬庚子居
    const dayGanIndex = TIAN_GAN.indexOf(dayGan);
    const shichenIndex = DI_ZHI.indexOf(shichen);
    
    const hourGanStart = [0, 2, 4, 6, 8][dayGanIndex % 5];
    const hourGanIndex = (hourGanStart + shichenIndex) % 10;
    
    return TIAN_GAN[hourGanIndex] + shichen;
}
```

### 阴阳遁判断

```javascript
function getYinYang(jieqi) {
    // 冬至后用阳遁，夏至后用阴遁
    const yangJieqi = ['冬至', '小寒', '大寒', '立春', '雨水', '惊蛰', '春分', '清明', '谷雨', '立夏', '小满', '芒种'];
    
    if (yangJieqi.includes(jieqi)) {
        return '阳遁';
    } else {
        return '阴遁';
    }
}
```

### 局数计算

```javascript
function getJuShu(jieqi, yinYang) {
    const juMap = {
        '阳遁': {
            '冬至': 1, '小寒': 2, '大寒': 3,
            '立春': 8, '雨水': 9, '惊蛰': 1,
            '春分': 3, '清明': 4, '谷雨': 5,
            '立夏': 4, '小满': 5, '芒种': 6
        },
        '阴遁': {
            '夏至': 9, '小暑': 8, '大暑': 7,
            '立秋': 2, '处暑': 1, '白露': 9,
            '秋分': 7, '寒露': 6, '霜降': 5,
            '立冬': 6, '小雪': 5, '大雪': 4
        }
    };
    
    return juMap[yinYang][jieqi] || 1;
}
```

### 地盘排列（三奇六仪）

```javascript
function getDiPan(juShu, yinYang) {
    const result = {};
    
    // 阳遁：顺排，阴遁：逆排
    const order = yinYang === '阳遁' ? JIU_GONG_ORDER : [...JIU_GONG_ORDER].reverse();
    
    // 起始位置
    const startIndex = (juShu - 1) % 9;
    
    for (let i = 0; i < 9; i++) {
        const gongIndex = (startIndex + i) % 9;
        const gongName = order[gongIndex];
        result[gongName] = SAN_QI_LIU_YI[i];
    }
    
    return result;
}
```

## 已知限制

1. **节气表硬编码** — 只有2026年数据，需要每年更新或改用天文算法
2. **天盘转动简化** — 未完全实现值符跟随转动
3. **八门排列简化** — 使用简化算法，可能与专业软件有差异
4. **八神排列简化** — 使用简化算法

## 使用示例

```javascript
const testDate = new Date(2026, 4, 6, 10, 30);
const result = qimenPan(testDate, 119.57, 31.99);

console.log(result);
// {
//   trueSolarTime: "2026-05-06 10:28",
//   shichen: "巳时",
//   dayGanZhi: "己巳",
//   hourGanZhi: "己巳",
//   jieqi: "立夏",
//   yinYang: "阳遁",
//   ju: 4,
//   palaces: { ... }
// }
```
