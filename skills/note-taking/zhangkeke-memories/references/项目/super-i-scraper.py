#!/usr/bin/env python3
"""
Super-i.cn 知识库抓取脚本
抓取刺猬星球网站的所有教程和资源内容
"""

import requests
from bs4 import BeautifulSoup
import json
import os
import time
from urllib.parse import urljoin
from datetime import datetime

BASE_URL = "https://www.super-i.cn"
OUTPUT_DIR = "/Users/labixiaoxin/.qclaw/workspace/knowledge-base/super-i"
os.makedirs(OUTPUT_DIR, exist_ok=True)

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
}

def fetch_page(url, retries=3):
    """获取页面内容"""
    for i in range(retries):
        try:
            resp = requests.get(url, headers=HEADERS, timeout=15)
            resp.encoding = 'utf-8'
            if resp.status_code == 200:
                return resp.text
            print(f"  ⚠️ 状态码 {resp.status_code}, 重试 {i+1}/{retries}")
        except Exception as e:
            print(f"  ⚠️ 请求失败: {e}, 重试 {i+1}/{retries}")
        time.sleep(2)
    return None

def parse_tutorial_list(html):
    """解析教程列表页，获取文章链接"""
    soup = BeautifulSoup(html, 'html.parser')
    articles = []
    
    # 查找所有文章条目
    for item in soup.find_all(['a', 'div'], class_=lambda x: x and ('item' in str(x).lower() or 'card' in str(x).lower())):
        link = item.find('a')
        if link and link.get('href'):
            url = link.get('href')
            if '/info-' in url:
                articles.append(url)
    
    # 备用方法：直接搜索包含 /info- 的链接
    if not articles:
        for a in soup.find_all('a', href=True):
            if '/info-' in a['href']:
                articles.append(a['href'])
    
    return list(set(articles))

def parse_article_detail(html, url):
    """解析文章详情页"""
    soup = BeautifulSoup(html, 'html.parser')
    
    # 提取标题
    title = ""
    for tag in soup.find_all(['h1', 'h2', 'h3', 'title']):
        if tag.get_text(strip=True):
            title = tag.get_text(strip=True)
            break
    
    # 提取正文内容
    content = []
    article_body = soup.find('div', class_=lambda x: x and ('content' in str(x).lower() or 'article' in str(x).lower() or 'detail' in str(x).lower()))
    
    if not article_body:
        # 尝试找主要内容区域
        main = soup.find('main') or soup.find('article') or soup.find('div', id=lambda x: x and ('content' in str(x).lower() or 'main' in str(x).lower()))
        if main:
            article_body = main
    
    if article_body:
        # 获取所有文本段落
        for p in article_body.find_all(['p', 'h1', 'h2', 'h3', 'h4', 'li', 'span', 'div']):
            text = p.get_text(strip=True)
            if text and len(text) > 5:
                content.append(text)
    
    # 提取标签
    tags = []
    for tag_el in soup.find_all(['span', 'a', 'div'], class_=lambda x: x and 'tag' in str(x).lower()):
        tag_text = tag_el.get_text(strip=True)
        if tag_text and len(tag_text) < 20:
            tags.append(tag_text)
    
    return {
        'title': title,
        'url': url,
        'content': '\n'.join(content[:100]),  # 限制内容长度
        'tags': list(set(tags))[:10],
        'scraped_at': datetime.now().isoformat()
    }

def scrape_tool_list_pages():
    """抓取教程列表的所有页面"""
    print("📚 开始抓取教程列表...")
    
    all_articles = []
    
    # 抓取前5页（核心内容）
    for page in range(1, 6):
        print(f"  抓取第 {page} 页...")
        if page == 1:
            url = f"{BASE_URL}/tool.html"
        else:
            url = f"{BASE_URL}/toollist({page})"
        
        html = fetch_page(url)
        if html:
            articles = parse_tutorial_list(html)
            all_articles.extend(articles)
            print(f"    找到 {len(articles)} 个文章链接")
        time.sleep(1)
    
    # 去重
    all_articles = list(set(all_articles))
    print(f"  共找到 {len(all_articles)} 篇文章\n")
    return all_articles

def scrape_articles(article_urls):
    """抓取所有文章详情"""
    print(f"📝 开始抓取 {len(article_urls)} 篇文章详情...")
    
    articles_data = []
    for i, url in enumerate(article_urls[:30], 1):  # 限制抓取数量
        full_url = url if url.startswith('http') else BASE_URL + url
        print(f"  [{i}/{min(len(article_urls), 30)}] 抓取: {full_url}")
        
        html = fetch_page(full_url)
        if html:
            article = parse_article_detail(html, full_url)
            if article['title']:
                articles_data.append(article)
                print(f"    ✓ {article['title'][:40]}...")
        
        time.sleep(0.5)
    
    return articles_data

def scrape_tool_categories():
    """抓取工具分类"""
    print("\n🛠️ 抓取工具分类...")
    
    html = fetch_page(f"{BASE_URL}/tool.html")
    if not html:
        return []
    
    soup = BeautifulSoup(html, 'html.parser')
    tools = []
    
    # 查找工具列表
    for tool in soup.find_all(['a', 'div'], class_=lambda x: x and 'tool' in str(x).lower()):
        name = tool.get_text(strip=True)
        link = tool.find('a') or tool
        href = link.get('href', '') if hasattr(link, 'get') else ''
        
        if name and len(name) < 50 and href:
            tools.append({
                'name': name,
                'url': href if href.startswith('http') else BASE_URL + href
            })
    
    # 去重并保存
    unique_tools = {t['name']: t for t in tools}.values()
    return list(unique_tools)

def save_knowledge_base(articles, tools):
    """保存知识库"""
    print("\n💾 保存知识库...")
    
    # 保存为 JSON
    kb_data = {
        'source': 'super-i.cn',
        'scraped_at': datetime.now().isoformat(),
        'total_articles': len(articles),
        'total_tools': len(tools),
        'articles': articles,
        'tools': tools
    }
    
    json_path = os.path.join(OUTPUT_DIR, 'knowledge-base.json')
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(kb_data, f, ensure_ascii=False, indent=2)
    
    # 保存为 Markdown
    md_path = os.path.join(OUTPUT_DIR, 'knowledge-base.md')
    with open(md_path, 'w', encoding='utf-8') as f:
        f.write(f"# Super-i.cn 知识库\n\n")
        f.write(f"> 来源: https://super-i.cn\n")
        f.write(f"> 抓取时间: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n")
        
        f.write(f"## 工具资源 ({len(tools)} 个)\n\n")
        for tool in tools:
            f.write(f"- **{tool['name']}**: {tool['url']}\n")
        
        f.write(f"\n## 教程文章 ({len(articles)} 篇)\n\n")
        for i, article in enumerate(articles, 1):
            f.write(f"### {i}. {article['title']}\n\n")
            f.write(f"来源: {article['url']}\n\n")
            if article['tags']:
                f.write(f"标签: {', '.join(article['tags'])}\n\n")
            if article['content']:
                f.write(f"{article['content'][:500]}...\n")
            f.write(f"\n---\n\n")
    
    print(f"  ✓ JSON: {json_path}")
    print(f"  ✓ Markdown: {md_path}")
    
    return json_path, md_path

def main():
    print("=" * 60)
    print("🚀 Super-i.cn 知识库抓取工具")
    print("=" * 60)
    print()
    
    start_time = time.time()
    
    # 1. 抓取教程列表
    article_urls = scrape_tool_list_pages()
    
    # 2. 抓取文章详情
    articles = scrape_articles(article_urls)
    
    # 3. 抓取工具分类
    tools = scrape_tool_categories()
    
    # 4. 保存知识库
    json_path, md_path = save_knowledge_base(articles, tools)
    
    elapsed = time.time() - start_time
    print()
    print("=" * 60)
    print(f"✅ 完成! 用时 {elapsed:.1f} 秒")
    print(f"📊 抓取文章: {len(articles)} 篇")
    print(f"📊 抓取工具: {len(tools)} 个")
    print(f"📁 保存位置: {OUTPUT_DIR}")
    print("=" * 60)

if __name__ == '__main__':
    main()
