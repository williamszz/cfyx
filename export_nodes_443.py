import base64
import re
import requests
from urllib.parse import unquote

# === 订阅地址 ===
url = "https://sub.danfeng.eu.org/sub?uuid=b5544203-55e3-426e-92f1-0684c93f9829&host=snippet.danfeng.site"

# === 自定义请求头（可自行修改） ===
headers = {
    "User-Agent": "V2RayN/6.37",
    "Accept": "*/*",
    "Connection": "keep-alive",
}

def maybe_b64decode(text: str) -> str:
    """尝试 Base64 解码"""
    try:
        t = text.strip()
        if re.fullmatch(r"[A-Za-z0-9+/=\r\n]+", t):
            return base64.b64decode(t).decode("utf-8", errors="ignore")
    except Exception:
        pass
    return text

def extract_nodes(decoded_text: str):
    """提取 IP:端口#备注"""
    results = []
    for line in decoded_text.splitlines():
        line = line.strip()
        if not line or not line.startswith(("vless://", "vmess://", "trojan://", "ss://")):
            continue
        m = re.search(r'@([^:]+):(\d+).*?#(.+)', line)
        if m:
            host, port, name = m.groups()
            name = unquote(name)
            results.append(f"{host}:{port}#{name}")
    return results

def main():
    print(f"📡 正在从订阅地址获取数据：{url}")
    resp = requests.get(url, headers=headers, timeout=15)
    resp.raise_for_status()
    raw_text = resp.text

    decoded = maybe_b64decode(raw_text)
    nodes = extract_nodes(decoded)

    if not nodes:
        print("⚠️ 未提取到任何节点，请检查订阅内容或编码格式。")
        return

    with open("nodes.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(nodes))

    print(f"✅ 已提取 {len(nodes)} 个节点，结果已保存至 nodes.txt\n")
    for n in nodes:
        print(n)

if __name__ == "__main__":
    main()
