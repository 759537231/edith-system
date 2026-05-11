# 飞书文件发送 Pitfalls

## 当前限制（2026-05-03 确认）

### 1. MEDIA 附件不支持
```
send_message(target="feishu:xxx", message="MEDIA:/path/to/file.pdf")
```
结果：消息发送成功，但附件被忽略。警告：
> "MEDIA attachments were omitted for feishu; native send_message media delivery is currently only supported for telegram, discord, matrix, weixin, signal and yuanbao"

### 2. 飞书云盘上传需要 drive 权限
应用 `cli_a97f63c797381cc4` 未开通 `drive:drive` / `drive:file` / `drive:file:upload` 权限。
调用 `/open-apis/drive/v1/files/upload_all` 返回 99991672 错误。

### 3. Base64 编码不可行
PDF 文件 base64 编码约 214K 字符，超出消息长度限制。

## 可行方案

### 方案A：飞书 IM API 直传音频/文件（已验证可用）

音频文件（WAV/MP3/OGG）可通过飞书 IM API 直接发送为语音消息：

```python
import json
import urllib.request
import subprocess

app_id = "cli_a97f63c797381cc4"
app_secret = "3E2xIZg1XiB6mk5S5sJtthPz4IUmBu2c"
chat_id = "oc_6f0ea7a70225f5283fe5488e2ae7a750"

# 1. 获取 tenant_access_token
token_url = "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal"
req = urllib.request.Request(token_url,
    data=json.dumps({"app_id": app_id, "app_secret": app_secret}).encode(),
    headers={'Content-Type': 'application/json'})
with urllib.request.urlopen(req) as resp:
    token = json.loads(resp.read())['tenant_access_token']

# 2. 上传文件（file_type=opus 用于音频）
result = subprocess.run(
    f'curl -s "https://open.feishu.cn/open-apis/im/v1/files" '
    f'-H "Authorization: Bearer {token}" '
    f'-F "file_type=opus" '
    f'-F "file_name=audio.wav" '
    f'-F "file=@/path/to/audio.wav"',
    shell=True, capture_output=True, text=True)
file_key = json.loads(result.stdout)['data']['file_key']

# 3. 发送音频消息
msg_url = f"https://open.feishu.cn/open-apis/im/v1/messages?receive_id_type=chat_id"
msg_data = json.dumps({
    "receive_id": chat_id,
    "msg_type": "audio",
    "content": json.dumps({"file_key": file_key})
}).encode()

msg_req = urllib.request.Request(msg_url, data=msg_data, headers={
    'Authorization': f'Bearer {token}',
    'Content-Type': 'application/json'
})
with urllib.request.urlopen(msg_req) as resp:
    print(json.loads(resp.read()))  # code=0 表示成功
```

**已验证**：2026-05-03 成功发送 13.8MB WAV 音频文件（红楼梦有声书）

### 方案B：富文本消息（已验证可用）
```python
# 用飞书 API 发送 post 类型消息
msg_data = {
    "receive_id": chat_id,
    "msg_type": "post",
    "content": json.dumps({
        "zh_cn": {
            "title": "标题",
            "content": [[{"tag": "text", "text": "内容"}]]
        }
    })
}
```

### 方案B：告知用户文件位置
直接告诉用户本地文件路径，让用户自行获取：
- Finder 中打开
- AirDrop 发送
- 邮件发送

### 方案C：申请飞书权限（长期方案）
在飞书开放平台为应用开通 `drive:file:upload` 权限，即可上传文件到云盘并发送 file_key。

### 方案D：音频文件通过 IM API 发送（已验证可用 ✅）

音频文件（WAV/MP3）可以用 `file_type=opus` 上传到飞书 IM，然后以 `audio` 消息类型发送：

```python
# 1. 获取 tenant_access_token
token_url = "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal"
# POST {"app_id": "...", "app_secret": "..."} → tenant_access_token

# 2. 上传文件
upload_url = "https://open.feishu.cn/open-apis/im/v1/files"
# curl -F "file_type=opus" -F "file_name=xxx.wav" -F "file=@/path/to/file.wav"
# → file_key

# 3. 发送音频消息
msg_url = "https://open.feishu.cn/open-apis/im/v1/messages?receive_id_type=chat_id"
# {"receive_id": chat_id, "msg_type": "audio", "content": {"file_key": "..."}}
```

**实测**（2026-05-03）：13.8 MB WAV 文件上传+发送成功，飞书客户端显示为可播放的语音消息。

**限制**：仅音频文件可用此路径。PDF/图片等仍需走方案A/B/C。

## 待办
- [ ] 为飞书应用申请 drive 权限（通用文件上传）
- [ ] 权限通过后，实现文件上传 + file_key 发送流程
