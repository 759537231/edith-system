#!/usr/bin/env python3
"""
经典古籍阅读进度追踪器
自动下载 + 阅读 + 内化
"""

import os
import json
from datetime import datetime, timedelta

BASE_DIR = "/Users/labixiaoxin/.qclaw/workspace/knowledge-base/经典书单/texts"

# 完整书单（按优先级排序）
BOOKS = [
    # ===== 经部（儒家核心）=====
    {"name": "道德经", "category": "经部", "priority": 1, "url": "https://ctext.org/dao-de-jing/zh"},
    {"name": "论语", "category": "经部", "priority": 2, "url": "https://ctext.org/analects/zh"},
    {"name": "孟子", "category": "经部", "priority": 3, "url": "https://ctext.org/mencius/zh"},
    {"name": "大学", "category": "经部", "priority": 4, "url": "https://ctext.org/da-xue/zh"},
    {"name": "中庸", "category": "经部", "priority": 5, "url": "https://ctext.org/zhong-yong/zh"},
    {"name": "周易", "category": "经部", "priority": 6, "url": "https://ctext.org/yijing/zh"},
    {"name": "尚书", "category": "经部", "priority": 7, "url": "https://ctext.org/shang-shu/zh"},
    {"name": "诗经", "category": "经部", "priority": 8, "url": "https://ctext.org/shijing/zh"},
    {"name": "礼记", "category": "经部", "priority": 9, "url": "https://ctext.org/li-ji/zh"},
    {"name": "春秋左传", "category": "经部", "priority": 10, "url": "https://ctext.org/chunqiu-zhuan/zh"},
    {"name": "荀子", "category": "经部", "priority": 11, "url": "https://ctext.org/xunzi/zh"},
    {"name": "近思录", "category": "经部", "priority": 12, "url": "https://ctext.org/jin-si-lu/zh"},
    {"name": "传习录", "category": "经部", "priority": 13, "url": "https://ctext.org/zhuan-xi-lu/zh"},
    
    # ===== 史部 =====
    {"name": "资治通鉴", "category": "史部", "priority": 14, "url": "https://ctext.org/tongjian/zh"},
    {"name": "史记", "category": "史部", "priority": 15, "url": "https://ctext.org/shiji/zh"},
    {"name": "贞观政要", "category": "史部", "priority": 16, "url": "https://ctext.org/zhen-guan-zheng-yao/zh"},
    {"name": "读通鉴论", "category": "史部", "priority": 17, "url": "https://ctext.org/du-tongjian-lun/zh"},
    {"name": "廿二史札记", "category": "史部", "priority": 18, "url": "https://ctext.org/ershi-er-shi-zha-ji/zh"},
    
    # ===== 子部（道家）=====
    {"name": "庄子", "category": "子部-道家", "priority": 19, "url": "https://ctext.org/zhuangzi/zh"},
    {"name": "列子", "category": "子部-道家", "priority": 20, "url": "https://ctext.org/liezi/zh"},
    
    # ===== 子部（兵家）=====
    {"name": "孙子兵法", "category": "子部-兵家", "priority": 21, "url": "https://ctext.org/sun-tzu/zh"},
    {"name": "六韬", "category": "子部-兵家", "priority": 22, "url": "https://ctext.org/liu-tao/zh"},
    {"name": "三略", "category": "子部-兵家", "priority": 23, "url": "https://ctext.org/san-lue/zh"},
    
    # ===== 子部（法家）=====
    {"name": "韩非子", "category": "子部-法家", "priority": 24, "url": "https://ctext.org/han-fei-zi/zh"},
    
    # ===== 子部（其他）=====
    {"name": "墨子", "category": "子部-墨家", "priority": 25, "url": "https://ctext.org/mozi/zh"},
    {"name": "管子", "category": "子部-杂家", "priority": 26, "url": "https://ctext.org/guanzi/zh"},
    {"name": "吕氏春秋", "category": "子部-杂家", "priority": 27, "url": "https://ctext.org/lu-shi-chun-qiu/zh"},
    {"name": "淮南子", "category": "子部-杂家", "priority": 28, "url": "https://ctext.org/huai-nan-zi/zh"},
    
    # ===== 子部（佛道）=====
    {"name": "六祖坛经", "category": "子部-佛家", "priority": 29, "url": "https://ctext.org/platform-sutra/zh"},
    {"name": "金刚经", "category": "子部-佛家", "priority": 30, "url": "https://ctext.org/vajracchedika/zh"},
    {"name": "心经", "category": "子部-佛家", "priority": 31, "url": "https://ctext.org/heart-sutra/zh"},
    {"name": "法句经", "category": "子部-佛家", "priority": 32, "url": "https://ctext.org/dhammapada/zh"},
    
    # ===== 子部（实用）=====
    {"name": "菜根谭", "category": "子部-处世", "priority": 33, "url": "https://ctext.org/caigen-tan/zh"},
    {"name": "呻吟语", "category": "子部-处世", "priority": 34, "url": "https://ctext.org/shen-yin-yu/zh"},
    {"name": "齐民要术", "category": "子部-农艺", "priority": 35, "url": "https://ctext.org/qimin-yaoshu/zh"},
    
    # ===== 集部 =====
    {"name": "文心雕龙", "category": "集部", "priority": 36, "url": "https://ctext.org/wenxin-diaolong/zh"},
    {"name": "古文观止", "category": "集部", "priority": 37, "url": "https://ctext.org/guwen-guanzhi/zh"},
    
    # ===== 毛泽东著作 =====
    {"name": "实践论", "category": "毛选", "priority": 38, "url": "https://www.marxists.org/chinese/maozedong/1937/index.htm"},
    {"name": "矛盾论", "category": "毛选", "priority": 39, "url": "https://www.marxists.org/chinese/maozedong/1937/index2.htm"},
    {"name": "反对本本主义", "category": "毛选", "priority": 40, "url": "https://www.marxists.org/chinese/maozedong/1930/index.htm"},
    {"name": "论持久战", "category": "毛选", "priority": 41, "url": "https://www.marxists.org/chinese/maozedong/1938/index.htm"},
    
    # ===== 全球经典（西方哲学）=====
    {"name": "理想国", "category": "全球-哲学", "priority": 42, "url": "https://ctext.org/republic/zh"},
    {"name": "尼各马可伦理学", "category": "全球-哲学", "priority": 43, "url": "https://ctext.org/nicomachean-ethics/zh"},
    {"name": "沉思录", "category": "全球-哲学", "priority": 44, "url": "https://ctext.org/meditations/zh"},
    {"name": "忏悔录", "category": "全球-哲学", "priority": 45, "url": "https://ctext.org/confessions/zh"},
    {"name": "社会契约论", "category": "全球-政治", "priority": 46, "url": "https://ctext.org/social-contract/zh"},
    {"name": "君主论", "category": "全球-政治", "priority": 47, "url": "https://ctext.org/prince/zh"},
    {"name": "存在与虚无", "category": "全球-哲学", "priority": 48, "url": "https://ctext.org/being-and-nothingness/zh"},
    {"name": "西西弗神话", "category": "全球-哲学", "priority": 49, "url": "https://ctext.org/myth-of-sisyphus/zh"},
    {"name": "查拉图斯特拉如是说", "category": "全球-哲学", "priority": 50, "url": "https://ctext.org/thus-spoke-zarathustra/zh"},
]

def get_progress():
    """获取阅读进度"""
    progress_file = os.path.join(BASE_DIR, "..", "reading_progress.json")
    if os.path.exists(progress_file):
        with open(progress_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {
        "started": datetime.now().isoformat(),
        "total_books": len(BOOKS),
        "completed": [],
        "daily_goal": 3,  # 每天3本
        "schedule_days": 30  # 30天完成
    }

def save_progress(progress):
    """保存进度"""
    progress_file = os.path.join(BASE_DIR, "..", "reading_progress.json")
    os.makedirs(os.path.dirname(progress_file), exist_ok=True)
    with open(progress_file, 'w', encoding='utf-8') as f:
        json.dump(progress, f, ensure_ascii=False, indent=2)

def get_today_books(progress):
    """获取今天的阅读任务"""
    completed_count = len(progress['completed'])
    remaining = [b for b in BOOKS if b['name'] not in progress['completed']]
    
    today_books = remaining[:progress['daily_goal']]
    return today_books

def main():
    progress = get_progress()
    
    # 显示今日任务
    today_books = get_today_books(progress)
    completed_count = len(progress['completed'])
    
    print(f"""
📚 经典阅读计划
{'='*40}
总进度: {completed_count}/{len(BOOKS)} 本 ({completed_count*100//len(BOOKS)}%)
每日目标: {progress['daily_goal']} 本
计划周期: {progress['schedule_days']} 天
开始时间: {progress['started'][:10]}

🎯 今日任务 ({datetime.now().strftime('%Y-%m-%d')}):
""")
    
    for i, book in enumerate(today_books, 1):
        print(f"  {i}. 《{book['name']}》[{book['category']}]")
    
    print(f"""
{'='*40}
剩余: {len(BOOKS) - completed_count} 本
预计完成: {(len(BOOKS) - completed_count) / progress['daily_goal']:.0f} 天
""")
    
    # 生成 cron 任务建议
    print("\n💡 建议设置每日定时任务，自动下载今日书籍")
    return today_books

if __name__ == '__main__':
    main()
