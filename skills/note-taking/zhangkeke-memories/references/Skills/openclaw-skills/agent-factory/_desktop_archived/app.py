"""
Agent 工厂 - 独立桌面版
双击 launcher.command 启动，自动打开浏览器聊天界面
支持多 Agent 切换，本地 MLX 模型驱动
"""

import os
import sys
import json
import glob
from datetime import datetime

import streamlit as st

# ── 路径 ──────────────────────────────────────────────────
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
AGENTS_DIR = os.path.join(BASE_DIR, "agents")
os.makedirs(AGENTS_DIR, exist_ok=True)

MLX_API = "http://127.0.0.1:18793/v1/chat/completions"
MLX_MODEL = "qwen3.5-4b-mlx"

# ── 工具函数 ──────────────────────────────────────────────
def load_agents():
    """加载所有已注册的 Agent"""
    agents = {}
    for cfg_path in glob.glob(os.path.join(AGENTS_DIR, "*.json")):
        with open(cfg_path, encoding="utf-8") as f:
            data = json.load(f)
            agents[data["id"]] = data
    return agents

def save_agent(agent_id: str, data: dict):
    with open(os.path.join(AGENTS_DIR, f"{agent_id}.json"), "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def load_chat_history(agent_id: str):
    path = os.path.join(AGENTS_DIR, f"{agent_id}_history.json")
    if os.path.exists(path):
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    return []

def save_chat_history(agent_id: str, history: list):
    path = os.path.join(AGENTS_DIR, f"{agent_id}_history.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(history, f, ensure_ascii=False, indent=2)

def call_mlx(messages: list, system_prompt: str = "") -> str:
    """调用本地 MLX 模型"""
    import urllib.request
    import urllib.error

    full_messages = []
    if system_prompt:
        full_messages.append({"role": "system", "content": system_prompt})
    full_messages.extend(messages)

    payload = json.dumps({
        "model": MLX_MODEL,
        "messages": full_messages,
        "temperature": 0.7,
        "max_tokens": 1024,
    }).encode("utf-8")

    try:
        req = urllib.request.Request(
            MLX_API,
            data=payload,
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        with urllib.request.urlopen(req, timeout=60) as resp:
            result = json.loads(resp.read().decode("utf-8"))
            return result["choices"][0]["message"]["content"]
    except Exception as e:
        return f"⚠️ 模型调用失败：{e}\n\n请确认本地模型服务已启动（`python3 ~/.qclaw/workspace/skills/mlx-fallback/chat.py`）"

# ── 页面配置 ──────────────────────────────────────────────
st.set_page_config(
    page_title="Agent 工厂",
    page_icon="🏭",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── 初始化 session state ───────────────────────────────────
if "current_agent" not in st.session_state:
    st.session_state.current_agent = None
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "initialized" not in st.session_state:
    st.session_state.initialized = True
    agents = load_agents()
    if agents:
        first_id = list(agents.keys())[0]
        st.session_state.current_agent = first_id
        st.session_state.chat_history = load_chat_history(first_id)

# ── 侧边栏：Agent 切换 + 管理 ──────────────────────────────
st.sidebar.title("🏭 Agent 工厂")
st.sidebar.markdown("---")

agents = load_agents()

# Agent 选择下拉
agent_options = {a["name"]: a["id"] for a in agents.values()}
if agent_options:
    selected_name = st.sidebar.selectbox(
        "当前 Agent",
        options=list(agent_options.keys()),
        index=list(agent_options.keys()).index(
            agents[st.session_state.current_agent]["name"]
        ) if st.session_state.current_agent in agents else 0,
    )
    new_id = agent_options[selected_name]
    if new_id != st.session_state.current_agent:
        st.session_state.current_agent = new_id
        st.session_state.chat_history = load_chat_history(new_id)
        st.rerun()
else:
    st.sidebar.warning("还没有 Agent，请新建一个 👇")
    st.session_state.current_agent = None

st.sidebar.markdown("---")

# 新建 Agent
st.sidebar.subheader("➕ 新建 Agent")
with st.sidebar.expander("点击新建", expanded=False):
    new_name = st.text_input("名称", key="new_name_input")
    new_type = st.selectbox("类型", ["对话型", "咨询型", "任务型"], key="new_type_input")
    new_desc = st.text_area("一句话描述", key="new_desc_input")
    if st.button("生成", key="create_agent_btn"):
        if new_name.strip():
            agent_id = new_name.strip().replace(" ", "_")
            role_prompt = f"你是「{new_name}」。\n\n{new_desc}"
            agent_data = {
                "id": agent_id,
                "name": new_name,
                "type": new_type,
                "description": new_desc,
                "role_prompt": role_prompt,
                "created_at": datetime.now().isoformat(),
                "tools": [],
            }
            save_agent(agent_id, agent_data)
            save_chat_history(agent_id, [])
            st.session_state.current_agent = agent_id
            st.session_state.chat_history = []
            st.sidebar.success(f"✅ 「{new_name}」已创建！")
            st.rerun()
        else:
            st.sidebar.error("名称不能为空")

st.sidebar.markdown("---")

# 删除 Agent
if agents and st.session_state.current_agent:
    with st.sidebar.expander("🗑 删除当前 Agent", expanded=False):
        current = agents[st.session_state.current_agent]
        st.text(f"确认删除「{current['name']}」？")
        col1, col2 = st.columns(2)
        if col1.button("删除", key="confirm_delete"):
            # 删除文件
            os.remove(os.path.join(AGENTS_DIR, f"{st.session_state.current_agent}.json"))
            hist_path = os.path.join(AGENTS_DIR, f"{st.session_state.current_agent}_history.json")
            if os.path.exists(hist_path):
                os.remove(hist_path)
            st.session_state.current_agent = None
            st.session_state.chat_history = []
            st.rerun()
        if col2.button("取消", key="cancel_delete"):
            st.rerun()

# Agent 信息
if st.session_state.current_agent and agents:
    st.sidebar.markdown("---")
    cur = agents[st.session_state.current_agent]
    st.sidebar.markdown(f"**类型**：{cur['type']}")
    st.sidebar.markdown(f"**简介**：{cur['description']}")
    st.sidebar.markdown(f"**记忆条数**：{len(st.session_state.chat_history)//2}")

# ── 主聊天区 ───────────────────────────────────────────────
if st.session_state.current_agent and agents:
    agent = agents[st.session_state.current_agent]

    st.title(f"💬 {agent['name']}")

    # 显示角色信息
    with st.expander("📋 角色设定", expanded=False):
        st.markdown(f"**类型**：{agent['type']}")
        st.markdown(f"**简介**：{agent['description']}")
        st.text_area("系统提示词", value=agent.get("role_prompt", ""),
                     height=120, disabled=True, key="role_display")

    st.markdown("---")

    # 聊天历史
    for msg in st.session_state.chat_history:
        if msg["role"] == "user":
            with st.chat_message("user"):
                st.markdown(msg["content"])
        else:
            with st.chat_message("assistant"):
                st.markdown(msg["content"])

    # 输入框
    if prompt := st.chat_input(f"对「{agent['name']}」说点什么..."):
        # 用户消息
        with st.chat_message("user"):
            st.markdown(prompt)
        st.session_state.chat_history.append({"role": "user", "content": prompt})

        # 调用模型
        with st.chat_message("assistant"):
            with st.spinner("思考中..."):
                history_for_api = [
                    {"role": m["role"], "content": m["content"]}
                    for m in st.session_state.chat_history[:-1]
                ]
                response = call_mlx(history_for_api, agent.get("role_prompt", ""))
                st.markdown(response)

        st.session_state.chat_history.append({"role": "assistant", "content": response})
        save_chat_history(st.session_state.current_agent, st.session_state.chat_history)

else:
    st.info("👈 左侧新建一个 Agent，或者选择一个已有的开始聊天")
    st.markdown("---")
    st.markdown("""
    ### 🏭 Agent 工厂 - 独立桌面版

    **特性**：
    - 💬 多 Agent 切换（左侧面板）
    - 🧠 本地模型驱动（MLX Qwen3.5-4B）
    - 📝 聊天记录本地存储
    - ➕ 随时新建 Agent

    **启动模型服务**（如未启动）：
    ```bash
    python3 ~/.qclaw/workspace/skills/mlx-fallback/chat.py
    ```
    """)
