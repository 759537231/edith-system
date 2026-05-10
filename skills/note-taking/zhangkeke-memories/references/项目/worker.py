#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
后台任务处理脚本
"""

import sys
import json
import os
import time

# 设置镜像源
os.environ['HF_ENDPOINT'] = 'https://hf-mirror.com'

sys.path.insert(0, '/Users/labixiaoxin/.qclaw/workspace/audio_billing')

from audio_billing import parse_script, transcribe_audio, SemanticMatcher, calculate_cost, save_results

def process_job(job_dir):
    """处理任务"""
    params_file = f"{job_dir}/params.json"
    log_file = f"{job_dir}/log.txt"
    
    if not os.path.exists(params_file):
        return
    
    with open(params_file) as f:
        params = json.load(f)
    
    def log(msg):
        timestamp = time.strftime("%H:%M:%S")
        with open(log_file, 'a') as f:
            f.write(f"[{timestamp}] {msg}\n")
        with open(f"{job_dir}/progress", 'w') as f:
            f.write(msg)
    
    log("parse|解析剧本...")
    roles, dialogues = parse_script(params['script'])
    log(f"transcribe|剧本解析完成，找到 {len(dialogues)} 条台词")
    
    # CV 对照表
    cv_mapping = params.get('cv_mapping', {})
    if cv_mapping:
        log(f"transcribe|已加载CV对照表: {cv_mapping}")
    
    total_files = len(params['audios'])
    all_results = []
    
    for i, (audio_path, audio_name) in enumerate(zip(params['audios'], params['audio_names'])):
        log(f"transcribe|转写音频 {i+1}/{total_files}: {audio_name}")
        
        model_name = params.get('whisper_model', 'base')
        segments = transcribe_audio(audio_path, model_name)
        
        log(f"match|匹配角色 {i+1}/{total_files}...")
        
        matcher = SemanticMatcher("all-MiniLM-L6-v2")
        cv_filter = params['cv_filter'] if params['cv_filter'] else None
        matched = matcher.match(segments, dialogues, threshold=params['threshold'], cv_filter=cv_filter)
        
        # 应用 CV 对照表
        for m in matched:
            if m.get('cv') and m['cv'] in cv_mapping:
                old_cv = m['cv']
                m['cv'] = cv_mapping[old_cv]
                log(f"billing|标准化CV: {old_cv} -> {m['cv']}")
        
        log(f"billing|计算费用 {i+1}/{total_files}...")
        
        report, role_seconds = calculate_cost(
            matched, roles,
            params['gap_seconds'],
            params['default_price'],
            params['price_dict']
        )
        
        csv_file = f"{job_dir}/{audio_name}.csv"
        save_results(matched, csv_file)
        
        report_file = f"{job_dir}/{audio_name}_report.txt"
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write(report)
        
        all_results.append({
            'audio_name': audio_name,
            'report': report,
            'matched_count': len([m for m in matched if m['role'] != '未匹配']),
            'segments_count': len(segments)
        })
        
        log(f"done|完成 {i+1}/{total_files}: {audio_name}")
    
    with open(f"{job_dir}/results.json", 'w') as f:
        json.dump(all_results, f)
    
    log("complete|全部完成！")

if __name__ == '__main__':
    if len(sys.argv) > 1:
        process_job(sys.argv[1])
