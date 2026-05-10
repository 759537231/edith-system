#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
音频计费系统 - Streamlit Web界面（后台处理版）
"""

import streamlit as st
import os
import time
import re
import json
import subprocess

# 页面配置
st.set_page_config(
    page_title="音频计费系统 v2",
    page_icon="🎙️",
    layout="wide"
)

# ========== 函数定义 ==========
def show_results(all_results, job_id):
    """显示结果"""
    st.markdown("---")
    st.subheader("📊 计费结果")
    
    import pandas as pd
    
    total_cost = 0
    total_segs = sum(r['segments_count'] for r in all_results)
    total_matched = sum(r['matched_count'] for r in all_results)
    
    for r in all_results:
        m = re.search(r'总计: ([\d.]+) 元', r['report'])
        if m:
            total_cost += float(m.group(1))
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("文件数", len(all_results))
    with col2:
        st.metric("总片段", total_segs)
    with col3:
        st.metric("匹配率", f"{total_matched/total_segs*100:.1f}%" if total_segs else "0%")
    with col4:
        st.metric("总费用", f"¥{total_cost:.2f}")
    
    st.markdown("#### 📁 文件明细")
    summary_data = []
    
    for r in all_results:
        with st.expander(f"📄 {r['audio_name']}", expanded=False):
            m = re.search(r'总计: ([\d.]+) 元', r['report'])
            cost = float(m.group(1)) if m else 0
            
            col_a, col_b, col_c = st.columns(3)
            with col_a:
                st.metric("片段", r['segments_count'])
            with col_b:
                st.metric("匹配", r['matched_count'])
            with col_c:
                st.metric("费用", f"¥{cost:.2f}")
            
            lines = []
            for line in r['report'].split('\n'):
                if '计费时长:' in line or '费用:' in line:
                    lines.append(line.strip())
            if lines:
                st.code('\n'.join(lines))
            
            csv_path = f"/tmp/{job_id}/{r['audio_name']}.csv"
            if os.path.exists(csv_path):
                col_dl1, col_dl2 = st.columns(2)
                with col_dl1:
                    data = open(csv_path, 'rb').read()
                    st.download_button("📥 CSV", data, r['audio_name']+'.csv', 'text/csv')
                with col_dl2:
                    report_path = f"/tmp/{job_id}/{r['audio_name']}_report.txt"
                    if os.path.exists(report_path):
                        data = open(report_path, 'rb').read()
                        st.download_button("📥 报告", data, r['audio_name']+'_报告.txt', 'text/plain')
    
    st.markdown("#### 📋 汇总")
    for r in all_results:
        m = re.search(r'总计: ([\d.]+) 元', r['report'])
        summary_data.append({
            '文件': r['audio_name'],
            '片段': r['segments_count'],
            '匹配': r['matched_count'],
            '费用': float(m.group(1)) if m else 0
        })
    
    if summary_data:
        df = pd.DataFrame(summary_data)
        df.loc['合计'] = ['合计', df['片段'].sum(), df['匹配'].sum(), df['费用'].sum()]
        st.dataframe(df, use_container_width=True, hide_index=True)

# ========== 主界面 ==========
st.title("🎙️ 音频计费系统 v2")
st.markdown("---")

# 初始化
if 'job_id' not in st.session_state:
    st.session_state.job_id = None
if 'results' not in st.session_state:
    st.session_state.results = None

# 侧边栏
with st.sidebar:
    st.header("📖 使用说明")
    st.markdown("""
    1. 上传剧本和音频文件
    2. 设置参数（阈值、单价等）
    3. 点击开始，后台处理
    4. 刷新页面查看结果
    """)
    
    st.header("📋 剧本格式")
    st.markdown("""
    角色：【CV名】【角色名】【性别】【描述】【台词数】
    台词：【角色名-CV名】「台词内容」
    """)
    
    st.header("🔄 CV对照表格式")
    st.markdown("""
    上传CSV文件，格式：
    ```
    原CV名,标准CV名
    qianmo,阡陌
    林小燃,林小燃
    ```
    """)
    
    # 下载模板
    template_csv = "原CV名,标准CV名\nqianmo,阡陌\n"
    st.download_button("📥 下载CV对照表模板", template_csv, "cv对照表模板.csv", "text/csv")

# 主界面
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("📁 文件选择")
    script_file = st.file_uploader("剧本文件 (.docx)", type=['docx'], key="script")
    audio_files = st.file_uploader("音频文件（可多选）", 
                                   type=['mp3', 'm4a', 'wav'], 
                                   accept_multiple_files=True)
    cv_mapping_file = st.file_uploader("CV名字对照表 (.csv，可选)", 
                                       type=['csv'], 
                                       key="cv_mapping")
    
    if script_file:
        st.success(f"✅ 剧本: {script_file.name}")
    if audio_files:
        st.success(f"✅ {len(audio_files)} 个音频文件")
    if cv_mapping_file:
        st.success(f"✅ CV对照表: {cv_mapping_file.name}")

with col2:
    st.subheader("⚙️ 设置")
    cv_filter = st.text_input("CV筛选", value="", placeholder="留空匹配所有")
    
    whisper_model = st.selectbox(
        "🎤 Whisper 模型",
        options=["base", "tiny", "small"],
        index=0,
        format_func=lambda x: {"tiny": "tiny（快速，准确率低）", "base": "base（推荐，速度适中）", "small": "small（最慢，准确率高）"}[x],
        help="tiny最快但准确率低，small最慢但准确率高"
    )
    
    threshold = st.slider("匹配阈值", 0.0, 1.0, 0.5, 0.05)
    gap_seconds = st.number_input("间隔时间(秒)", 0.0, 5.0, 0.5, 0.1)
    default_price = st.number_input("默认单价(元/分钟)", 10, 200, 50, 5)

# 角色单价
st.markdown("---")
st.subheader("💰 角色单价")
roles_dict = {}

if script_file:
    temp_script = f"/tmp/{script_file.name}"
    with open(temp_script, 'wb') as f:
        f.write(script_file.getbuffer())
    
    try:
        from audio_billing import parse_script
        roles_dict, _ = parse_script(temp_script)
        
        cols = st.columns(4)
        for i, (role, info) in enumerate(roles_dict.items()):
            with cols[i % 4]:
                key = f"price_{role}"
                if key not in st.session_state:
                    st.session_state[key] = default_price
                st.number_input(
                    role,
                    value=st.session_state[key],
                    key=key,
                    help=f"CV: {info.get('cv', '?')}"
                )
    except Exception as e:
        st.error(f"解析剧本失败: {e}")

# 开始按钮
st.markdown("---")
col_btn1, col_btn2, col_btn3 = st.columns([1, 1, 1])
with col_btn2:
    start_button = st.button("🚀 开始计费", type="primary", use_container_width=True)

# 处理逻辑
if start_button:
    if not script_file or not audio_files:
        st.error("请选择剧本和音频文件！")
    else:
        script_path = f"/tmp/{script_file.name}"
        audio_paths = []
        audio_names = []
        
        for af in audio_files:
            path = f"/tmp/{af.name}"
            with open(path, 'wb') as f:
                f.write(af.getbuffer())
            audio_paths.append(path)
            audio_names.append(af.name)
        
        price_dict = {}
        for role in roles_dict.keys():
            key = f"price_{role}"
            price_dict[role] = st.session_state.get(key, default_price)
        
        # CV 对照表
        cv_mapping = {}
        if cv_mapping_file:
            temp_cv = f"/tmp/{cv_mapping_file.name}"
            with open(temp_cv, 'wb') as f:
                f.write(cv_mapping_file.getbuffer())
            
            # 读取 CSV
            import pandas as pd
            try:
                df = pd.read_csv(temp_cv)
                for _, row in df.iterrows():
                    if len(row) >= 2:
                        old_name = str(row.iloc[0]).strip()
                        new_name = str(row.iloc[1]).strip()
                        if old_name and new_name:
                            cv_mapping[old_name] = new_name
                st.success(f"✅ 已加载 {len(cv_mapping)} 条CV对照")
            except Exception as e:
                st.warning(f"CV对照表格式错误: {e}")
        
        job_id = f"job_{int(time.time())}"
        job_dir = f"/tmp/{job_id}"
        os.makedirs(job_dir, exist_ok=True)
        
        task_params = {
            'script': script_path,
            'audios': audio_paths,
            'audio_names': audio_names,
            'threshold': threshold,
            'gap_seconds': gap_seconds,
            'default_price': default_price,
            'cv_filter': cv_filter,
            'price_dict': price_dict,
            'job_dir': job_dir,
            'whisper_model': whisper_model,
            'cv_mapping': cv_mapping
        }
        
        with open(f"{job_dir}/params.json", 'w') as f:
            json.dump(task_params, f)
        
        cmd = [
            'python3',
            '/Users/labixiaoxin/.qclaw/workspace/audio_billing/worker.py',
            job_dir
        ]
        
        with open(f"{job_dir}/process.log", 'w') as log_file:
            subprocess.Popen(cmd, stdout=log_file, stderr=log_file)
        
        st.session_state.job_id = job_id
        
        st.success("✅ 任务已启动！")
        time.sleep(2)
        st.rerun()

# 显示任务状态
if st.session_state.job_id:
    job_id = st.session_state.job_id
    job_dir = f"/tmp/{job_id}"
    
    if os.path.exists(job_dir):
        progress_file = f"{job_dir}/progress"
        results_file = f"{job_dir}/results.json"
        
        if os.path.exists(progress_file):
            with open(progress_file) as f:
                content = f.read().strip()
            
            if 'complete' in content:
                st.success("🎉 任务完成！")
                
                if os.path.exists(results_file):
                    with open(results_file) as f:
                        all_results = json.load(f)
                    show_results(all_results, job_id)
                    st.session_state.job_id = None
            else:
                parts = content.split('|')
                msg = parts[1] if len(parts) > 1 else '处理中...'
                
                st.info(f"⏳ {msg}")
                
                log_file = f"{job_dir}/log.txt"
                if os.path.exists(log_file):
                    with open(log_file) as f:
                        log_content = f.read()
                    if log_content:
                        st.code(log_content[-2000:], language="")
                
                time.sleep(3)
                st.rerun()
