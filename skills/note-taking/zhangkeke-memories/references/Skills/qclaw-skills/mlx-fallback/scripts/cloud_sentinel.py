#!/usr/bin/env python3
"""
cloud_sentinel.py — 云端 API 守护脚本
自动检测云端 API 是否可用，故障时切换到本地张二壳，恢复后切回。

用法：
  python3 cloud_sentinel.py              # 前台运行（测试用）
  python3 cloud_sentinel.py --install    # 安装 launchd 开机自启
  python3 cloud_sentinel.py --uninstall  # 卸载 launchd
  python3 cloud_sentinel.py --status     # 查看当前状态
"""

import json
import os
import ssl
import subprocess
import sys
import time
import urllib.request
import urllib.error
from pathlib import Path

# 跳过 SSL 验证（检测用，不传敏感数据）
SSL_CTX = ssl.create_default_context()
SSL_CTX.check_hostname = False
SSL_CTX.verify_mode = ssl.CERT_NONE

# ============ 配置 ============
CONFIG_PATH = Path.home() / ".openclaw" / "openclaw.json"
STATUS_FILE = Path.home() / ".qclaw" / "workspace" / "data" / "sentinel_status.json"

# 云端检测：网络出网 + QClaw modelroute 上游可达
# QClaw modelroute 走阿里云 DashScope，检测其 API 域名即可
CLOUD_CHECK_URLS = [
    "https://dashscope.aliyuncs.com/compatible-mode/v1/models",  # Qwen API
    "https://www.baidu.com",                                       # 出网兜底
]
CLOUD_CHECK_TIMEOUT = 10  # 秒

# 本地张二壳检测地址
LOCAL_CHECK_URL = "http://127.0.0.1:18793/v1/models"
LOCAL_CHECK_TIMEOUT = 5

# 容错阈值
FAIL_THRESHOLD = 3        # 连续失败 N 次触发切换
CHECK_INTERVAL = 60       # 检测间隔（秒）
RECOVERY_WAIT = 180       # 切回前确认云端稳定等待时间

# 模型标识
CLOUD_MODEL = "ollama/qwen3.5:0.8b"    # 云端默认模型
LOCAL_MODEL = "zhangerkq/zhangerkq"     # 本地张二壳

# Launchd
PLIST_NAME = "com.qclaw.cloud-sentinel"
PLIST_PATH = Path.home() / "Library" / "LaunchAgents" / f"{PLIST_NAME}.plist"
SCRIPT_PATH = Path(__file__).resolve()


# ============ 工具函数 ============

def log(msg):
    ts = time.strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{ts}] {msg}", flush=True)


def write_status(state, detail=""):
    STATUS_FILE.parent.mkdir(parents=True, exist_ok=True)
    data = {
        "state": state,  # "cloud" | "local" | "unknown"
        "detail": detail,
        "updated_at": time.strftime("%Y-%m-%dT%H:%M:%S"),
    }
    STATUS_FILE.write_text(json.dumps(data, indent=2, ensure_ascii=False))


def read_status():
    if STATUS_FILE.exists():
        try:
            return json.loads(STATUS_FILE.read_text())
        except Exception:
            pass
    return {"state": "unknown", "detail": ""}


def ping_url(url, timeout):
    """HTTP GET 检测，返回 True/False"""
    try:
        req = urllib.request.Request(url, method="GET")
        req.add_header("User-Agent", "cloud-sentinel/1.0")
        with urllib.request.urlopen(req, timeout=timeout, context=SSL_CTX) as resp:
            return resp.status < 500  # 2xx/3xx/4xx 都算网络通
    except Exception:
        return False


def is_cloud_ok():
    """综合检测云端是否可用"""
    for url in CLOUD_CHECK_URLS:
        if ping_url(url, CLOUD_CHECK_TIMEOUT):
            return True
    return False


def get_current_primary():
    """读取当前 openclaw.json 的 primary 模型"""
    try:
        cfg = json.loads(CONFIG_PATH.read_text())
        return cfg.get("agents", {}).get("defaults", {}).get("model", {}).get("primary", "")
    except Exception:
        return ""


def switch_model(model_id):
    """修改 openclaw.json 切换 primary 模型，并重启 gateway"""
    try:
        cfg = json.loads(CONFIG_PATH.read_text())
    except Exception as e:
        log(f"❌ 读取配置失败: {e}")
        return False

    current = cfg.get("agents", {}).get("defaults", {}).get("model", {}).get("primary", "")
    if current == model_id:
        log(f"已经是 {model_id}，无需切换")
        return True

    # 修改配置
    if "agents" not in cfg:
        cfg["agents"] = {}
    if "defaults" not in cfg["agents"]:
        cfg["agents"]["defaults"] = {}
    if "model" not in cfg["agents"]["defaults"]:
        cfg["agents"]["defaults"]["model"] = {}
    cfg["agents"]["defaults"]["model"]["primary"] = model_id

    # 写回
    try:
        CONFIG_PATH.write_text(json.dumps(cfg, indent=2, ensure_ascii=False))
        log(f"✅ 配置已修改: {current} → {model_id}")
    except Exception as e:
        log(f"❌ 写入配置失败: {e}")
        return False

    # 重启 gateway
    log("🔄 重启 gateway...")
    try:
        result = subprocess.run(
            ["openclaw", "gateway", "restart"],
            capture_output=True, text=True, timeout=30
        )
        if result.returncode == 0:
            log("✅ Gateway 已重启")
        else:
            log(f"⚠️ Gateway 重启可能有异常: {result.stderr.strip()}")
    except Exception as e:
        log(f"❌ Gateway 重启失败: {e}")
        return False

    return True


# ============ 主循环 ============

def run_sentinel():
    log("🛡️ 云端守护脚本启动")
    log(f"   检测间隔: {CHECK_INTERVAL}s | 失败阈值: {FAIL_THRESHOLD}次")
    log(f"   云端模型: {CLOUD_MODEL} | 本地模型: {LOCAL_MODEL}")

    # 初始化状态
    current_primary = get_current_primary()
    if "zhangerkq" in current_primary:
        write_status("local", f"启动时已是本地模式: {current_primary}")
        log(f"📍 当前处于本地模式: {current_primary}")
    else:
        write_status("cloud", f"启动时处于云端模式: {current_primary}")
        log(f"📍 当前处于云端模式: {current_primary}")

    fail_count = 0
    recovery_count = 0
    is_on_local = "zhangerkq" in current_primary

    while True:
        # 检测云端
        cloud_ok = is_cloud_ok()

        if is_on_local:
            # ---- 当前在本地模式，等云端恢复 ----
            if cloud_ok:
                recovery_count += 1
                log(f"☁️ 云端可达 ({recovery_count}/{FAIL_THRESHOLD})")
                if recovery_count >= FAIL_THRESHOLD:
                    log("☁️ 云端已稳定恢复，切回云端...")
                    if switch_model(CLOUD_MODEL):
                        is_on_local = False
                        write_status("cloud", "云端恢复，已切回")
                        log("✅ 已切回云端模式")
                    recovery_count = 0
            else:
                recovery_count = 0
                log("☁️ 云端仍不可达，保持本地模式")
        else:
            # ---- 当前在云端模式，监测故障 ----
            if cloud_ok:
                fail_count = 0
            else:
                fail_count += 1
                log(f"⚠️ 云端不可达 ({fail_count}/{FAIL_THRESHOLD})")

                if fail_count >= FAIL_THRESHOLD:
                    # 先检测本地张二壳是否可用
                    local_ok = ping_url(LOCAL_CHECK_URL, LOCAL_CHECK_TIMEOUT)
                    if not local_ok:
                        log("❌ 云端挂了但本地张二壳也没启动，无法切换")
                        log("   提示：需手动启动 api_server.py")
                        write_status("cloud", "云端故障且本地不可用，等待恢复")
                        fail_count = 0  # 重置，避免反复刷日志
                        time.sleep(RECOVERY_WAIT)
                        continue

                    log("🔄 云端故障，切换到本地张二壳...")
                    if switch_model(LOCAL_MODEL):
                        is_on_local = True
                        write_status("local", f"云端故障，已切换到本地 (失败{fail_count}次)")
                        log("✅ 已切换到本地模式")
                    fail_count = 0
                    recovery_count = 0

        time.sleep(CHECK_INTERVAL)


# ============ Launchd 安装/卸载 ============

def install_launchd():
    """安装为 launchd 开机自启服务"""
    python_path = sys.executable
    plist_content = f"""<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>{PLIST_NAME}</string>
    <key>ProgramArguments</key>
    <array>
        <string>{python_path}</string>
        <string>{SCRIPT_PATH}</string>
    </array>
    <key>RunAtLoad</key>
    <true/>
    <key>KeepAlive</key>
    <true/>
    <key>StandardOutPath</key>
    <string>/tmp/cloud-sentinel.log</string>
    <key>StandardErrorPath</key>
    <string>/tmp/cloud-sentinel.err</string>
    <key>EnvironmentVariables</key>
    <dict>
        <key>PATH</key>
        <string>/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin</string>
    </dict>
</dict>
</plist>"""

    PLIST_PATH.parent.mkdir(parents=True, exist_ok=True)
    PLIST_PATH.write_text(plist_content)
    log(f"✅ plist 已写入: {PLIST_PATH}")

    # 加载
    subprocess.run(["launchctl", "unload", str(PLIST_PATH)], capture_output=True)
    result = subprocess.run(["launchctl", "load", str(PLIST_PATH)], capture_output=True, text=True)
    if result.returncode == 0:
        log("✅ launchd 服务已加载，开机自启生效")
    else:
        log(f"⚠️ 加载可能有问题: {result.stderr.strip()}")

    log(f"📝 日志位置: /tmp/cloud-sentinel.log")


def uninstall_launchd():
    """卸载 launchd 服务"""
    subprocess.run(["launchctl", "unload", str(PLIST_PATH)], capture_output=True)
    if PLIST_PATH.exists():
        PLIST_PATH.unlink()
        log("✅ plist 已删除")
    log("✅ launchd 服务已卸载")


def show_status():
    """显示当前状态"""
    status = read_status()
    current = get_current_primary()
    print(f"当前模型: {current}")
    print(f"守护状态: {json.dumps(status, indent=2, ensure_ascii=False)}")
    
    # 检测云端
    cloud_ok = is_cloud_ok()
    print(f"云端 API: {'✅ 可达' if cloud_ok else '❌ 不可达'}")
    
    # 检测本地
    local_ok = ping_url(LOCAL_CHECK_URL, LOCAL_CHECK_TIMEOUT)
    print(f"本地张二壳: {'✅ 可达' if local_ok else '❌ 未启动'}")
    
    # 检查 launchd
    running = PLIST_PATH.exists()
    print(f"开机自启: {'✅ 已安装' if running else '❌ 未安装'}")


# ============ 入口 ============

if __name__ == "__main__":
    if len(sys.argv) > 1:
        cmd = sys.argv[1]
        if cmd == "--install":
            install_launchd()
        elif cmd == "--uninstall":
            uninstall_launchd()
        elif cmd == "--status":
            show_status()
        else:
            print(__doc__)
    else:
        try:
            run_sentinel()
        except KeyboardInterrupt:
            log("🛑 守护脚本已停止")
            write_status("unknown", "手动停止")
