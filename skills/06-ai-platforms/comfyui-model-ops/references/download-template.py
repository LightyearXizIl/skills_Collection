# -*- coding: utf-8 -*-
"""ComfyUI 大模型下载模板：断点续传 + 自动重试 + 进度反馈 + 收尾校验。

用法：改 JOBS 列表的 (目标路径, URL)，然后直接跑。
注意：必须用 Python 而不是 bash curl —— 本机 Git Bash 的 curl -w 经常无输出。
"""
import os, ssl, time, urllib.request

# 关键：清空代理变量，否则国内镜像不通
for k in ('http_proxy', 'https_proxy', 'HTTP_PROXY', 'HTTPS_PROXY', 'ALL_PROXY', 'all_proxy'):
    os.environ.pop(k, None)

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

JOBS = [
    (r'D:\path\to\models\diffusion_models\model.safetensors',
     'https://hf-mirror.com/<repo>/resolve/main/<subpath>/model.safetensors'),
]


def remote_size(url):
    req = urllib.request.Request(url, method='HEAD', headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req, timeout=30, context=ctx) as r:
        return int(r.headers.get('Content-Length'))


def fetch(url, dst, attempt=5):
    """带 Range 续传与重试的下载。返回 True 表示完整。"""
    total = remote_size(url)
    for tries in range(attempt):
        have = os.path.getsize(dst) if os.path.exists(dst) else 0
        if have >= total:
            print('  [已完成] %s  %d bytes' % (os.path.basename(dst), have), flush=True)
            return True
        headers = {'User-Agent': 'Mozilla/5.0'}
        if have > 0:
            headers['Range'] = 'bytes=%d-' % have
        try:
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, timeout=60, context=ctx) as r, open(dst, 'ab') as f:
                t0 = time.time()
                last = t0
                while True:
                    chunk = r.read(1024 * 512)
                    if not chunk:
                        break
                    f.write(chunk)
                    have += len(chunk)
                    now = time.time()
                    if now - last >= 30:          # 每 30 秒报一次进度
                        last = now
                        print('    %s  %.2f/%.2f GB  (%.1f MB/s)'
                              % (os.path.basename(dst), have / 1e9, total / 1e9,
                                 have / max(now - t0, 1) / 1e6), flush=True)
        except Exception as e:
            # 常见：SSL: UNEXPECTED_EOF_WHILE_READING（镜像断流）—— 续传重试即可
            print('  [重试 %d/%d] %s : %s'
                  % (tries + 1, attempt, os.path.basename(dst), str(e)[:100]), flush=True)
            time.sleep(5)
            continue
    have = os.path.getsize(dst) if os.path.exists(dst) else 0
    print('  [%s] %s  %d / %d'
          % ('已完成' if have >= total else '未完成', os.path.basename(dst), have, total), flush=True)
    return have >= total


if __name__ == '__main__':
    print('=== 开始下载 ===', flush=True)
    ok = True
    for dst, url in JOBS:
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        print('-> %s  (%.2f GB)' % (os.path.basename(dst), remote_size(url) / 1e9), flush=True)
        if not fetch(url, dst):
            ok = False
    print('=== 全部完成 ===' if ok else '=== 有文件未完成 ===', flush=True)
