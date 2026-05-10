#!/usr/bin/env python3
"""
经典古籍下载脚本
从 ctext.org 和 Project Gutenberg 下载公共领域经典著作
"""

import requests
from bs4 import BeautifulSoup
import os
import json
import time
from datetime import datetime

# 输出目录
BASE_DIR = "/Users/labixiaoxin/.qclaw/workspace/knowledge-base/经典书单/texts"
os.makedirs(BASE_DIR, exist_ok=True)

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
    'Accept': 'text/html,application/xhtml+xml',
}

# ctext.org 文本URL映射
CTEXT_URLS = {
    "道德经": "https://ctext.org/dao-de-jing/zh",
    "论语": "https://ctext.org/analects/zh",
    "孟子": "https://ctext.org/mencius/zh",
    "庄子": "https://ctext.org/zhuangzi/zh",
    "大学": "https://ctext.org/da-xue/zh",
    "中庸": "https://ctext.org/zhong-yong/zh",
    "尚书": "https://ctext.org/shang-shu/zh",
    "礼记": "https://ctext.org/li-ji/zh",
    "诗经": "https://ctext.org/shijing/zh",
    "春秋左传": "https://ctext.org/chunqiu-zhuan/zh",
    "孙子兵法": "https://ctext.org/sun-tzu/zh",
    "六韬": "https://ctext.org/liu-tao/zh",
    "荀子": "https://ctext.org/xunzi/zh",
    "韩非子": "https://ctext.org/han-fei-zi/zh",
    "墨子": "https://ctext.org/mozi/zh",
    "列子": "https://ctext.org/liezi/zh",
    "管子": "https://ctext.org/guanzi/zh",
    "吕氏春秋": "https://ctext.org/lu-shi-chun-qiu/zh",
    "淮南子": "https://ctext.org/huai-nan-zi/zh",
    "春秋繁露": "https://ctext.org/chunqiu-fanlu/zh",
    "近思录": "https://ctext.org/jin-si-lu/zh",
    "传习录": "https://ctext.org/zhuan-xi-lu/zh",
    "菜根谭": "https://ctext.org/caigen-tan/zh",
    "呻吟语": "https://ctext.org/shen-yin-yu/zh",
    "贞观政要": "https://ctext.org/zhen-guan-zheng-yao/zh",
    "六祖坛经": "https://ctext.org/platform-sutra/zh",
    "金刚经": "https://ctext.org/vajracchedika/zh",
    "心经": "https://ctext.org/heart-sutra/zh",
    "文心雕龙": "https://ctext.org/wenxin-diaolong/zh",
    "昭明文选": "https://ctext.org/zhaoming-wenxuan/zh",
    "古文观止": "https://ctext.org/guwen-guanzhi/zh",
}

def download_ctext(title, url, retries=3):
    """从 ctext.org 下载文本"""
    print(f"  下载《{title}》...")
    for i in range(retries):
        try:
            resp = requests.get(url, headers=HEADERS, timeout=20)
            resp.encoding = 'utf-8'
            if resp.status_code == 200:
                soup = BeautifulSoup(resp.text, 'html.parser')
                
                # 提取正文
                content_div = soup.find('div', id='main-text') or soup.find('div', class_='ctext')
                if content_div:
                    # 获取所有段落
                    paragraphs = []
                    for p in content_div.find_all(['p', 'div'], class_=lambda x: x and 'ctext' in str(x).lower()):
                        text = p.get_text(strip=True)
                        if text and len(text) > 5:
                            paragraphs.append(text)
                    
                    content = '\n\n'.join(paragraphs)
                    
                    # 保存
                    filepath = os.path.join(BASE_DIR, f"{title}.txt")
                    with open(filepath, 'w', encoding='utf-8') as f:
                        f.write(f"# {title}\n")
                        f.write(f"# 来源: {url}\n")
                        f.write(f"# 下载时间: {datetime.now().isoformat()}\n\n")
                        f.write(content)
                    
                    print(f"    ✓ {title} ({len(content)} 字)")
                    return True
        except Exception as e:
            print(f"    ⚠️ {title} 失败: {e}, 重试 {i+1}")
            time.sleep(2)
    return False

def download_gutenberg():
    """从 Project Gutenberg 下载西方经典"""
    print("\n下载西方经典...")
    
    gutenberg_books = {
        "理想国": "https://www.gutenberg.org/cache/epub/55088/pg55088.txt",
        "沉思录": "https://www.gutenberg.org/cache/epub/71422/pg71422.txt",
        "尼各马可伦理学": "https://www.gutenberg.org/cache/epub/19755/pg19755.txt",
    }
    
    for title, url in gutenberg_books.items():
        try:
            print(f"  下载《{title}》...")
            resp = requests.get(url, headers=HEADERS, timeout=30)
            if resp.status_code == 200:
                text = resp.text
                # 去除 Gutenberg 头部和尾部
                start = text.find("*** START OF THIS PROJECT")
                end = text.find("*** END OF THIS PROJECT")
                if start > 0 and end > 0:
                    text = text[end + 100:]
                
                filepath = os.path.join(BASE_DIR, "全球经典", f"{title}.txt")
                os.makedirs(os.path.dirname(filepath), exist_ok=True)
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(f"# {title}\n")
                    f.write(f"# 来源: {url}\n")
                    f.write(text[:50000])  # 限制长度
                
                print(f"    ✓ {title}")
        except Exception as e:
            print(f"    ⚠️ {title} 失败: {e}")
        time.sleep(1)

def main():
    print("=" * 60)
    print("经典古籍下载工具")
    print("=" * 60)
    
    print(f"\n输出目录: {BASE_DIR}")
    print(f"计划下载: {len(CTEXT_URLS)} 部中文经典")
    
    print("\n开始下载中文经典...")
    success = 0
    for title, url in list(CTEXT_URLS.items())[:20]:  # 先下载前20本
        if download_ctext(title, url):
            success += 1
        time.sleep(1)
    
    print(f"\n✓ 成功下载 {success}/{len(CTEXT_URLS)} 本中文经典")
    print(f"保存位置: {BASE_DIR}")
    print("=" * 60)

if __name__ == '__main__':
    main()
