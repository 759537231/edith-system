#!/usr/bin/env python3
"""
经典古籍下载器 - 优化版
支持 ctext.org 的多种格式获取
"""

import requests
from bs4 import BeautifulSoup
import os
import time
from datetime import datetime

BASE_DIR = "/Users/labixiaoxin/.qclaw/workspace/knowledge-base/经典书单/texts"
os.makedirs(BASE_DIR, exist_ok=True)

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
}

def download_with_text_format(title, url):
    """使用 ctext.org 的纯文本格式"""
    text_url = url.replace('/zh', '')  # 移除语言后缀获取纯文本
    
    # 尝试纯文本格式
    text_url = f"https://ctext.org/{title.replace(' ', '-').lower()}/zh?format=txt"
    
    try:
        resp = requests.get(text_url, headers=HEADERS, timeout=15)
        if resp.status_code == 200:
            content = resp.text
            if len(content) > 500:
                return content
    except:
        pass
    return None

def download_with_parser(title, url):
    """使用 HTML 解析器下载"""
    try:
        resp = requests.get(url, headers=HEADERS, timeout=15)
        resp.encoding = 'utf-8'
        
        if resp.status_code != 200:
            return None
            
        soup = BeautifulSoup(resp.text, 'html.parser')
        
        # 查找主文本区域
        main_text = soup.find('div', id='main-text')
        if not main_text:
            main_text = soup.find('div', class_=lambda x: x and 'ctext' in str(x).lower())
        
        if not main_text:
            # 尝试其他方式
            body = soup.find('body')
            if body:
                # 获取所有文本节点
                text_parts = []
                for element in body.find_all(['p', 'div', 'span']):
                    text = element.get_text(strip=True)
                    if text and len(text) > 20:
                        text_parts.append(text)
                if text_parts:
                    return '\n\n'.join(text_parts)
            return None
        
        # 提取段落
        paragraphs = []
        for p in main_text.find_all(['p', 'br']):
            # 获取直接文本（包含子元素）
            text = ''
            for content in p.contents:
                if hasattr(content, 'text'):
                    text += content.text
                else:
                    text += str(content)
            text = text.strip()
            if text and len(text) > 5:
                paragraphs.append(text)
        
        return '\n\n'.join(paragraphs)
        
    except Exception as e:
        print(f"    解析错误: {e}")
        return None

def download_book(title, url, category="其他"):
    """下载单本书"""
    category_dir = os.path.join(BASE_DIR, category.replace('/', '-'))
    os.makedirs(category_dir, exist_ok=True)
    filepath = os.path.join(category_dir, f"{title}.txt")
    
    # 检查是否已存在
    if os.path.exists(filepath):
        size = os.path.getsize(filepath)
        print(f"  ⏭️  {title} 已存在 ({size} bytes)")
        return True
    
    print(f"  下载《{title}》...")
    
    # 方法1: 直接文本格式
    content = download_with_text_format(title, url)
    
    # 方法2: HTML解析
    if not content:
        content = download_with_parser(title, url)
    
    if content and len(content) > 200:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(f"# {title}\n")
            f.write(f"# 来源: {url}\n")
            f.write(f"# 下载时间: {datetime.now().isoformat()}\n")
            f.write(f"# 分类: {category}\n\n")
            f.write(content)
        
        print(f"  ✅ {title} ({len(content)} 字)")
        return True
    
    print(f"  ⚠️ {title} 获取失败")
    return False

def main():
    print("=" * 60)
    print("经典古籍下载器")
    print("=" * 60)
    
    # 今日任务
    today_books = [
        {"name": "道德经", "category": "经部", "url": "https://ctext.org/dao-de-jing/zh"},
        {"name": "论语", "category": "经部", "url": "https://ctext.org/analects/zh"},
        {"name": "孟子", "category": "经部", "url": "https://ctext.org/mencius/zh"},
    ]
    
    print(f"\n📅 今日阅读任务:")
    for i, book in enumerate(today_books, 1):
        print(f"  {i}. 《{book['name']}》")
    
    print("\n开始下载...\n")
    
    success = 0
    for book in today_books:
        if download_book(book['name'], book['url'], book['category']):
            success += 1
        time.sleep(1)  # 礼貌延迟
    
    print(f"\n完成: {success}/{len(today_books)} 本")
    print(f"保存位置: {BASE_DIR}")
    print("=" * 60)

if __name__ == '__main__':
    main()
