"""
后期音频结算系统 - 核心逻辑
"""

import json
import os
import re
from pathlib import Path
from typing import Dict, List, Optional, Tuple
import subprocess
import pandas as pd

DATA_DIR = Path(__file__).parent / "data"
PRODUCTIONS_FILE = DATA_DIR / "productions.json"


def _ensure_data_dir_safe():
    """确保数据目录存在"""
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    (DATA_DIR / "output").mkdir(parents=True, exist_ok=True)


def ensure_data_dir():
    """确保数据目录存在"""
    if not PRODUCTIONS_FILE.exists():
        _ensure_data_dir_safe()
        with open(PRODUCTIONS_FILE, "w", encoding="utf-8") as f:
            json.dump({}, f, ensure_ascii=False, indent=2)


def load_productions() -> Dict:
    """加载剧组配置"""
    ensure_data_dir()
    with open(PRODUCTIONS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_productions(productions: Dict):
    """保存剧组配置"""
    _ensure_data_dir_safe()
    with open(PRODUCTIONS_FILE, "w", encoding="utf-8") as f:
        json.dump(productions, f, ensure_ascii=False, indent=2)


def get_audio_duration(file_path: str) -> Optional[float]:
    """使用 ffprobe 获取音频时长（秒）"""
    try:
        cmd = [
            "ffprobe", "-v", "error",
            "-show_entries", "format=duration",
            "-of", "default=noprint_wrappers=1:nokey=1",
            file_path
        ]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        if result.returncode == 0:
            return float(result.stdout.strip())
        return None
    except Exception:
        return None


def parse_audio_filename(filename: str) -> Optional[Dict]:
    """
    解析音频文件名，提取剧组名和集数
    
    支持格式：
    - 末日温泉第10集 MIX.mp3
    - 末日温泉第2集.mp3
    - 剧组名_第1集.mp3
    - 异世界料理养娃成神第2.5 MIX.mp3 (小数集数)
    - 异世界料理养娃成神第21.5集 MIX.mp3
    - 人皮子第一集MIX.mp3 (中文数字)
    
    返回：{"production": "末日温泉", "episode": 10} 或 None
    """
    # 中文数字映射
    cn_map = {
        '一': 1, '二': 2, '三': 3, '四': 4, '五': 5,
        '六': 6, '七': 7, '八': 8, '九': 9, '十': 10,
        '十一': 11, '十二': 12, '十三': 13, '十四': 14, '十五': 15,
        '十六': 16, '十七': 17, '十八': 18, '十九': 19, '二十': 20
    }
    
    name = Path(filename).stem
    
    # 去掉 MIX、后缀等
    name = re.sub(r'\s*MIX\s*$', '', name, flags=re.IGNORECASE)
    name = name.strip()
    
    # 提取并移除集数后面的标记（如 "第40集前"、"第1集第三版"）
    # 标记格式：第X集 + (前|后|重置|第X版|修正|改版)
    ep_suffix_pattern = re.compile(r'第(\d+\.?\d*)集(前|后|重置|第[一二三四五六七八九十\d]+版|修正|修改|改版)')
    ep_suffix_match = ep_suffix_pattern.search(name)
    ep_suffix = ''
    if ep_suffix_match:
        ep_suffix = ep_suffix_match.group(2)  # 保存标记
        # 从name中移除标记，保留"第X集"用于解析
        name = name[:ep_suffix_match.start()] + '第' + ep_suffix_match.group(1) + '集' + name[ep_suffix_match.end():]
    
    # 提取并移除剧组名后面的标记（如 "圣人重置"、"开机甲版"）
    # 在"第"字之前的后缀标记
    prod_suffix = re.search(r'^(.+?)(前|后|重置|第.+版|修正|修改|改版)$', name.split('第')[0] if '第' in name else '', re.IGNORECASE)
    
    # 先尝试中文数字
    cn_match = re.search(r'第([一二三四五六七八九十]+(?:\d+)?)集?', name)
    if cn_match:
        cn_num = cn_match.group(1)
        if cn_num in cn_map:
            episode = cn_map[cn_num]
        else:
            # 处理十一、十二等
            try:
                episode = int(cn_num)
            except:
                episode = 0
        if episode > 0:
            production = re.sub(r'第[一二三四五六七八九十\d]+集?', '', name).strip()
            # 移除剧组名后的标记（如"圣人重置"中的"重置"）
            production = re.sub(r'(重置|前|后|第[一二三四五六七八九十0-9]+版|修正|修改|改版)$', '', production)
            production = re.sub(r'[_\s\-]+$', '', production)
            production = re.sub(r'^[_\s\-]+', '', production)
            if production:
                return {"production": production, "episode": episode}
    
    # 匹配 "第X集" 或 "第X.X" 或 "第X.X集" 格式（包括小数）
    patterns = [
        r'第(\d+\.\d+)集?',      # 第2.5, 第2.5集, 第21.5, 第21.5集（小数）
        r'第(\d+)集',           # 第10集（整数）
        r'第(\d+)话',           # 第10话（日漫）
        r'_(\d+\.?\d*)$',       # _10, _2.5
    ]
    
    # 支持括号格式：第1（2）集、第2（3）集（表示补充版）
    paren_match = re.search(r'第(\d+)（(\d+)）集', name)
    if paren_match:
        episode = int(paren_match.group(1))
        production = re.sub(r'第\d+（\d+）集', '', name).strip()
        production = re.sub(r'(重置|前|后|第[一二三四五六七八九十0-9]+版|修正|修改|改版)$', '', production)
        if production:
            return {"production": production, "episode": episode}
    
    for pattern in patterns:
        match = re.search(pattern, name)
        if match:
            episode_str = match.group(1)
            if '.' in episode_str:
                episode = float(episode_str)
            else:
                episode = int(episode_str)
            production = re.sub(pattern, '', name).strip()
            # 移除剧组名后的标记
            production = re.sub(r'(重置|前|后|第[一二三四五六七八九十0-9]+版|修正|修改|改版)$', '', production)
            production = re.sub(r'[_\s\-]+$', '', production)
            production = re.sub(r'^[_\s\-]+', '', production)
            
            if production:
                return {"production": production, "episode": episode}
    
    # 匹配非集数关键词：预告、花絮、片花、PV、宣传、teaser、trailer 等
    non_episode_keywords = r'(预告|花絮|片花|宣传片?|PV|teaser|trailer|片头|片尾|OP|ED|BGM|OST)'
    ne_match = re.search(non_episode_keywords, name, re.IGNORECASE)
    if ne_match:
        production = re.sub(non_episode_keywords, '', name, flags=re.IGNORECASE).strip()
        production = re.sub(r'[_\s\-]+$', '', production)
        production = re.sub(r'^[_\s\-]+', '', production)
        if production:
            # 移除剧组名后的标记（如"圣人重置"中的"重置"）
            production = re.sub(r'(重置|前|后|第[一二三四五六七八九十0-9]+版|修正|修改|改版)$', '', production)
            return {"production": production, "episode": 0, "is_non_episode": True, "non_episode_type": ne_match.group(1)}
    
    # 处理第0集
    zero_match = re.search(r'第0集', name)
    if zero_match:
        production = re.sub(r'第0集', '', name).strip()
        production = re.sub(r'(重置|前|后|第[一二三四五六七八九十0-9]+版|修正|修改|改版)$', '', production)
        production = re.sub(r'[_\s-]+$', '', production)
        production = re.sub(r'^[_\s-]+', '', production)
        if production:
            return {'production': production, 'episode': 0}

    return None


def parse_episode_string(ep_str: str) -> Tuple[List[float], List[str]]:
    """
    解析集数字符串，返回 (数字集数列表, 原始项列表)
    原始项保留标记，用于匹配音频文件名
    支持格式：
    - 2-18 (连续)
    - 20,24,26,27 (逗号分隔)
    - 1-4.6-8 (1-4 和 6-8，中间的点会被当作分隔符)
    - 2.5,3.5 (小数集数)
    - 38-40、42、44-46、50 (中文顿号分隔)
    """
    episodes = []
    if not ep_str or pd.isna(ep_str):
        return []
    
    ep_str = str(ep_str).strip()
    
    # 处理中文顿号（、）
    ep_str = ep_str.replace('、', ',')
    
    # 处理 1-4.6-8 这种格式：只处理 .数字- 的模式
    ep_str = re.sub(r'(\d)\.(\d+)-', r'\1,\2-', ep_str)
    
    # 处理中文逗号
    ep_str = ep_str.replace('，', ',')
    
    # 分割逗号和空格
    parts = re.split(r'[,，\s]+', ep_str)
    
    for part in parts:
        part = part.strip()
        if not part:
            continue
        
        # 检查是否带后缀标记（如 "1第三版"、"40前"、"40后"、"2重置"、"5第二版"）
        suffix_match = re.match(r'^(\d+)(前|后|重置|第[一二三四五六七八九十0-9]+版|修正|修改|改版)$', part)
        if suffix_match:
            # 提取数字部分用于计数，但保留原始项用于匹配
            base = int(suffix_match.group(1))
            episodes.append(base)
        
        # 检查是否是纯小数（如 2.5、3.5）
        if re.match(r'^\d+\.\d+$', part):
            try:
                episodes.append(float(part))
            except:
                pass
        elif '-' in part:
            range_parts = part.split('-')
            if len(range_parts) == 2:
                try:
                    start_str = range_parts[0].strip()
                    end_str = range_parts[1].strip()
                    # 检查是否有后缀
                    suffix_match = re.match(r'^(\d+)(前|后|重置|第.+版|修正|修改|改版)$', end_str)
                    if suffix_match:
                        start = int(float(start_str))
                        end = int(suffix_match.group(1))
                        # 范围+后缀的情况，展开每集
                        for ep in range(start, end + 1):
                            episodes.append(ep)
                    else:
                        start = int(float(start_str))
                        end = int(float(end_str))
                        episodes.extend(range(start, end + 1))
                except:
                    pass
        else:
            try:
                # 检查括号版本号（如 "1（2）"、"1(2)"）- 提取数字
                paren_match = re.match(r'^(\d+)[（(](\d+)[）)]$', part)
                if paren_match:
                    base = int(paren_match.group(1))
                    episodes.append(base)
                elif '.' in part:
                    episodes.append(float(part))
                else:
                    episodes.append(int(float(part)))
            except:
                pass
    
    # 返回：(展开后数量, 去重episodes, original_items)
    # original_items 保留标记，用于匹配音频文件名
    original_items = [p.strip() for p in parts if p.strip()]
    # 去重但保持顺序（用于匹配）
    seen = set()
    unique_episodes = []
    for e in episodes:
        if e not in seen:
            seen.add(e)
            unique_episodes.append(e)
    # 总集数 = 原始项展开后的数量（不去重，因为40前和40后算2个文件）
    total_count = len(episodes)
    return total_count, unique_episodes, original_items


def parse_table_excel(file_path: str) -> List[Dict]:
    """
    解析表格文件，返回剧组列表
    """
    try:
        df = pd.read_excel(file_path)
        
        results = []
        for _, row in df.iterrows():
            production_name = row.get('剧组名称', '')
            if pd.isna(production_name) or not production_name:
                continue
            
            # 跳过合计行等非数据行
            prod_str = str(production_name).strip()
            if prod_str in ['合计', '总计', '总计:', '小计', '-']:
                continue
            
            episodes_str = str(row.get('本次应该结算集数', '')).strip() if not pd.isna(row.get('本次应该结算集数', '')) else ''
            
            # 检查是否是版本号（如"第3版"）而不是集数
            is_version = False
            is_title_mode = False  # 标题模式（如小咩的标题列表）
            titles = []  # 标题列表
            
            if re.match(r'^第\d+版$', episodes_str):
                is_version = True
            elif episodes_str and not re.search(r'\d', episodes_str.replace('第', '').replace('集', '').replace('版', '')):
                # 没有数字但有大段文字 → 可能是标题模式
                lines = [l.strip() for l in episodes_str.replace('\n', '\n').split('\n') if l.strip()]
                if len(lines) >= 2 or (len(lines) == 1 and len(lines[0]) > 6):
                    is_title_mode = True
                    titles = lines
            elif not episodes_str:
                # 集数列为空但有时长 → 默认第0集（如三生三世）
                episodes_str = '0'
                is_version = False
            
            # 处理时长（秒）- 列名可能含换行符
            duration_sec = 0
            for col in row.index:
                if '时长（秒）' in col:
                    duration_sec = row[col]
                    break
            try:
                if pd.isna(duration_sec) or str(duration_sec).strip() == '':
                    duration_sec = 0
                else:
                    duration_sec = float(str(duration_sec).replace(',', ''))
            except:
                duration_sec = 0
            
            # 处理单价
            price_per_sec = row.get('价格（元/秒）', 0)
            try:
                if pd.isna(price_per_sec) or str(price_per_sec).strip() == '':
                    price_per_sec = 0
                else:
                    price_per_sec = float(str(price_per_sec).replace(',', ''))
            except:
                price_per_sec = 0
            
            # 处理总金额
            total_amount = row.get('总金额（元）', 0)
            try:
                if pd.isna(total_amount) or str(total_amount).strip() == '':
                    total_amount = 0
                else:
                    total_amount = float(str(total_amount).replace(',', ''))
            except:
                total_amount = 0
            
            # 解析集数（版本号和标题模式除外）
            if is_version:
                episodes = []
            elif is_title_mode:
                episodes = list(range(1, len(titles) + 1))  # 按标题数量生成虚拟集数
                total_count = len(titles)  # 标题模式下用标题数量作为总集数
            else:
                total_count, episodes, original_items = parse_episode_string(episodes_str)
            
            results.append({
                "production": prod_str,
                "episodes_str": episodes_str,
                "episodes": episodes,
                "original_items": original_items if not is_version and not is_title_mode else [],
                "is_version": is_version,
                "is_title_mode": is_title_mode,
                "titles": titles,
                "duration_sec": float(duration_sec),
                "price_per_sec": float(price_per_sec),
                "total_amount": float(total_amount),
                "total_count": total_count if not is_version else 1
            })
        
        return results
    except Exception as e:
        print(f"解析表格出错: {e}")
        import traceback
        traceback.print_exc()
        return []


def scan_audio_folder(folder_path: str) -> List[Dict]:
    """
    扫描音频文件夹，返回音频文件列表
    """
    results = []
    
    try:
        folder = Path(folder_path)
        if not folder.exists():
            return results
        
        # 递归扫描所有MP3和WAV文件
        for mp3_file in folder.rglob("*.mp3"):
            _process_audio_file(mp3_file, "", results)
        for mp3_file in folder.rglob("*.wav"):
            _process_audio_file(mp3_file, "", results)
    
    except Exception as e:
        print(f"扫描文件夹出错: {e}")
    
    return results


def _process_audio_file(mp3_file: Path, fallback_production: str, results: List):
    """处理单个音频文件"""
    # 获取文件夹名作为备用剧组名，去掉后缀标记
    parent_name = mp3_file.parent.name
    clean_folder_name = re.sub(r'(重置|前|后|第\d+版|修正|修改|改版)$', '', parent_name)
    clean_folder_name = re.sub(r'(重置|前|后|第\d+版|修正|修改|改版)$', '', clean_folder_name)
    
    filename = mp3_file.name
    parsed = parse_audio_filename(filename)
    
    if parsed:
        # 如果解析不出剧组名，用文件夹名
        if not parsed.get("production"):
            parsed["production"] = clean_folder_name
        # 检查是否需要标题模式（文件名没有集数）
        if parsed.get("episode", 0) == 0 and not parsed.get("is_non_episode"):
            # 可能是标题模式，去掉MIX后缀作为标题
            title = Path(filename).stem
            title = re.sub(r'\s*MIX\s*$', '', title, flags=re.IGNORECASE).strip()
            parsed["is_title"] = True
            parsed["title"] = title
    else:
        # 如果完全解析不出，尝试标题模式
        title = Path(filename).stem
        title = re.sub(r'\s*MIX\s*$', '', title, flags=re.IGNORECASE).strip()
        parsed = {
            "filename": filename,
            "filepath": str(mp3_file),
            "production": clean_folder_name,
            "episode": 0,
            "duration_sec": 0,
            "duration_min": 0,
            "is_title": True,
            "title": title
        }
    
    # 获取时长
    duration = get_audio_duration(str(mp3_file)) or 0
    parsed["duration_sec"] = round(duration, 1)
    parsed["duration_min"] = round(duration / 60, 2)
    parsed["filepath"] = str(mp3_file)
    
    results.append(parsed)
    
    return results


def fuzzy_match_title(title: str, filename: str, threshold: float = 0.5) -> bool:
    """
    模糊匹配标题与音频文件名
    title: 表格中的标题（如"小咩：草原蜱虫怎么预防和处理"）
    filename: 音频文件名（如"小咩：草原蜱虫怎么预防和处理.mp3"）
    threshold: 匹配阈值（0-1），默认0.5
    """
    # 去掉扩展名
    fname = Path(filename).stem
    fname_clean = re.sub(r'\s*(MIX|mix|final|Final)\s*', '', fname).strip()
    
    # 去掉剧组名前缀（如"小咩："）
    title_clean = title.strip()
    
    # 直接包含
    if title_clean in fname_clean or fname_clean in title_clean:
        return True
    
    # 计算字符重叠率
    title_chars = set(title_clean)
    fname_chars = set(fname_clean)
    if not title_chars or not fname_chars:
        return False
    
    overlap = len(title_chars & fname_chars)
    ratio = overlap / max(len(title_chars), len(fname_chars))
    
    return ratio >= threshold


def match_episode_item(item_str: str, filename: str) -> bool:
    """
    用表格里的原始集数项匹配音频文件名
    item_str: 如 "2重置", "6-10重置", "1第三版", "40前", "4-39"
    filename: 音频文件名
    """
    from pathlib import Path
    fname = Path(filename).stem
    fname = re.sub(r'\s*(MIX|mix|final|Final)\s*', '', fname).strip()
    
    # 1. 范围+后缀（如 "6-10重置"）→ 匹配 6重置、7重置...10重置
    m = re.match(r'^(\d+)-(\d+)(前|后|重置|第.+版|修正|修改|改版)$', item_str)
    if m:
        start, end, suffix = int(m.group(1)), int(m.group(2)), m.group(3)
        for ep in range(start, end + 1):
            # 文件名包含数字和后缀
            if str(ep) in fname and suffix in fname:
                return True
        return False
    
    # 2. 单集+后缀（如 "2重置", "1第三版", "40前"）
    m = re.match(r'^(\d+)(前|后|重置|第.+版|修正|修改|改版)$', item_str)
    if m:
        ep, suffix = m.group(1), m.group(2)
        return ep in fname and suffix in fname
    
    # 3. 纯范围（如 "4-39"）→ 匹配 4、5、6...39
    m = re.match(r'^(\d+)-(\d+)$', item_str)
    if m:
        start, end = int(m.group(1)), int(m.group(2))
        for ep in range(start, end + 1):
            if str(ep) in fname:
                return True
        return False
    
    # 4. 纯数字（如 "17"）
    if item_str.isdigit():
        return item_str in fname
    
    # 5. 其他：直接包含
    return item_str in fname


def calculate_comparison(table_data: List[Dict], audio_data: List[Dict]) -> Dict:
    """
    对比表格数据和音频数据，返回对比结果
    """
    # 按剧组分组
    audio_by_prod = {}
    for item in audio_data:
        prod = item.get("production", "未知")
        if prod not in audio_by_prod:
            audio_by_prod[prod] = []
        audio_by_prod[prod].append(item)
    
    results = []
    
    for table_item in table_data:
        prod_name = table_item["production"]
        is_version = table_item.get("is_version", False)
        
        # 找到对应的音频数据（支持模糊匹配，如"叛逆玫瑰"匹配"叛逆玫瑰：女王的加冕"）
        audio_items = audio_by_prod.get(prod_name, [])
        if not audio_items:
            # 尝试模糊匹配
            for audio_prod, items in audio_by_prod.items():
                if prod_name in audio_prod or audio_prod in prod_name:
                    audio_items = items
                    break
        
        if is_version:
            # 版本号模式：只比对数量和时长
            audio_count = len(audio_items)
            table_count = table_item.get("total_count", 1)
            audio_duration = sum(item.get("duration_sec", 0) for item in audio_items)
            table_duration = table_item.get("duration_sec", 0)
            
            results.append({
                "production": prod_name,
                "is_version": True,
                "version_str": table_item.get("episodes_str", ""),
                "table_episodes": [],
                "audio_episodes": [],
                "matched_count": min(audio_count, table_count),
                "missing_count": max(0, table_count - audio_count),
                "extra_count": max(0, audio_count - table_count),
                "missing_episodes": [],
                "extra_episodes": [],
                "table_duration_sec": round(table_duration, 1),
                "audio_duration_sec": round(audio_duration, 1),
                "duration_diff_sec": round(audio_duration - table_duration, 1),
                "table_total": table_item.get("total_amount", 0),
                "price_per_sec": table_item.get("price_per_sec", 0),
                "non_episode_count": 0,
                "non_episode_duration_sec": 0,
                "non_episode_types": []
            })
        else:
            is_title_mode = table_item.get("is_title_mode", False)
            titles = table_item.get("titles", [])

            if is_title_mode and titles:
                # 标题模式：在全部音频文件中匹配标题
                matched_titles = []
                missing_titles = []
                matched_audio_paths = set()
                total_audio_duration = 0
                
                for title in titles:
                    found = False
                    for audio_item in audio_data:
                        if audio_item.get("filepath") in matched_audio_paths:
                            continue
                        fname = Path(audio_item.get("filepath", "")).name
                        if fuzzy_match_title(title, fname):
                            matched_titles.append(title)
                            matched_audio_paths.add(audio_item.get("filepath"))
                            total_audio_duration += audio_item.get("duration_sec", 0)
                            found = True
                            break
                    if not found:
                        missing_titles.append(title)
                
                extra_files = [Path(a.get("filepath", "")).name
                               for a in audio_data if a.get("filepath") not in matched_audio_paths]

                results.append({
                    "production": prod_name,
                    "is_version": False,
                    "is_title_mode": True,
                    "table_episodes": list(range(1, len(titles) + 1)),
                    "audio_episodes": list(range(1, len(matched_titles) + 1)),
                    "matched_count": len(matched_titles),
                    "missing_count": len(missing_titles),
                    "extra_count": 0,
                    "missing_episodes": [],
                    "extra_episodes": extra_files[:3],
                    "missing_titles": missing_titles,
                    "matched_titles": matched_titles,
                    "table_duration_sec": round(table_item["duration_sec"], 1),
                    "audio_duration_sec": round(total_audio_duration, 1),
                    "duration_diff_sec": round(total_audio_duration - table_item["duration_sec"], 1),
                    "table_total": table_item.get("total_amount", 0),
                    "price_per_sec": table_item.get("price_per_sec", 0)
                })
            else:
                # 正常集数模式 - 用原始项匹配音频文件名
                original_items = table_item.get("original_items", [])
                matched_audio_indices = set()
                matched_items = []
                
                if original_items:
                    # 用原始项逐个匹配音频文件
                    for item_str in original_items:
                        for idx, audio_item in enumerate(audio_items):
                            if idx in matched_audio_indices:
                                continue
                            fname = Path(audio_item.get("filepath", "")).name
                            if match_episode_item(item_str, fname):
                                matched_items.append(item_str)
                                matched_audio_indices.add(idx)
                                break
                else:
                    # 没有原始项，用数字集数匹配
                    for ep in table_item.get("episodes", []):
                        ep_int = int(ep) if isinstance(ep, float) and ep == int(ep) else ep
                        for idx, audio_item in enumerate(audio_items):
                            if idx in matched_audio_indices:
                                continue
                            if audio_item.get("episode") == ep_int:
                                matched_audio_indices.add(idx)
                                matched_items.append(str(ep_int))
                                break
                
                table_episodes = set(table_item.get("episodes", []))
                audio_episodes = set(item["episode"] for item in audio_items if item.get("episode") is not None)

                # 非集数文件（预告、花絮等）
                non_episode_items = [item for item in audio_items if item.get("is_non_episode", False)]
                non_episode_duration = sum(item["duration_sec"] for item in non_episode_items)
                non_episode_types = list(set(item.get("non_episode_type", "未知") for item in non_episode_items))

                # 计算差异
                missing_episodes = table_episodes - audio_episodes
                extra_episodes = audio_episodes - table_episodes
                matched_episodes = table_episodes & audio_episodes

                # 计算时长（只算集数，不算非集数）
                audio_duration = sum(item["duration_sec"] for item in audio_items if item.get("episode", 0) > 0)
                table_duration = table_item["duration_sec"]

                results.append({
                    "production": prod_name,
                    "is_version": False,
                    "is_title_mode": False,
                    "table_episodes": sorted(table_episodes),
                    "audio_episodes": sorted(audio_episodes),
                    "matched_count": len(matched_episodes),
                    "missing_count": len(missing_episodes),
                    "extra_count": len(extra_episodes),
                    "missing_episodes": sorted(missing_episodes) if missing_episodes else [],
                    "extra_episodes": sorted(extra_episodes) if extra_episodes else [],
                    "table_duration_sec": round(table_duration, 1),
                    "audio_duration_sec": round(audio_duration, 1),
                    "duration_diff_sec": round(audio_duration - table_duration, 1),
                    "table_total": table_item.get("total_amount", 0),
                    "price_per_sec": table_item.get("price_per_sec", 0)
                })

    return results