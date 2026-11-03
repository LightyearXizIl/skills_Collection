# -*- coding: utf-8 -*-
"""ComfyUI 工作流校验工具集：① 连线一致性 ② safetensors 严格完整性。

用途：手改过工作流 JSON（加节点/改连线/换模型）之后，在打开 ComfyUI 之前先自检，
避免 Node 报红或 "Could not load subgraphs"。
"""
import json, os, struct


# ---------------------------------------------------------------- 工作流校验
def check_workflow(path, expect=None, verbose=True):
    """校验工作流 JSON 的连线一致性。

    expect 可选，形如 {'positive_src': 27, 'negative_src': 80}，检查 KSampler 条件来源节点。
    返回 True/False。
    """
    d = json.load(open(path, encoding='utf-8'))
    subs = d.get('definitions', {}).get('subgraphs', [])
    ok = True

    def check_graph(sg, tag):
        nonlocal ok
        nodes = {n['id']: n for n in sg.get('nodes', [])}
        links = {l['id']: l for l in sg.get('links', [])}
        orphan = []
        for n in sg.get('nodes', []):
            for i in n.get('inputs', []):
                lk = i.get('link')
                if lk is not None and lk not in links:
                    orphan.append('n%s.in %s -> %s' % (n['id'], i.get('name'), lk))
            for o in n.get('outputs', []):
                for lk in (o.get('links') or []):
                    if lk not in links:
                        orphan.append('n%s.out %s -> %s' % (n['id'], o.get('name'), lk))
        if verbose:
            print('  [%s] 节点 %d | links %d | 孤立引用: %s'
                  % (tag, len(nodes), len(links), orphan if orphan else '无'))
        if orphan:
            ok = False

        # KSampler 条件来源
        for n in sg.get('nodes', []):
            if n.get('type') == 'KSampler':
                for i in n.get('inputs', []):
                    if i.get('name') in ('positive', 'negative') and i.get('link') in links:
                        src = links[i['link']]['origin_id']
                        stype = nodes.get(src, {}).get('type')
                        if verbose:
                            print('  [%s] KSampler.%s <- node %s (%s)'
                                  % (tag, i['name'], src, stype))
                        if expect:
                            key = i['name'] + '_src'
                            if key in expect and src != expect[key]:
                                print('        !! 期望 %s，实际 %s' % (expect[key], src))
                                ok = False
        # 死节点检查（ConditioningZeroOut 意味着空负面）
        if any(n.get('type') == 'ConditioningZeroOut' for n in sg.get('nodes', [])) and verbose:
            print('  [%s] 注意：存在 ConditioningZeroOut —— 负面提示词不会生效' % tag)

    for sg in subs:
        check_graph(sg, sg.get('name') or 'subgraph')
    if not subs:
        check_graph(d, 'root')
    return ok


# ------------------------------------------------------- safetensors 完整性
def check_safetensors(path, verbose=True):
    """三层校验：字节数由调用方给；此处做头部解析 + 数据区区间覆盖检查。

    数据区覆盖检查是唯一能发现「续传拼接错位 / 文件截断」的方法。
    """
    size = os.path.getsize(path)
    with open(path, 'rb') as f:
        hlen = struct.unpack('<Q', f.read(8))[0]
        head = json.loads(f.read(hlen).decode('utf-8').rstrip('\x00'))
    keys = [k for k in head if k != '__metadata__']

    patches = sorted(head[k]['data_offsets'] for k in keys if 'data_offsets' in head[k])
    data_start = 8 + hlen
    expected = size - data_start
    cur = 0
    contiguous = True
    for s, e in patches:
        if s != cur:
            contiguous = False
        cur = max(cur, e)

    ok = contiguous and (cur == expected)
    if verbose:
        dtypes = {}
        for k in keys:
            t = head[k].get('dtype')
            dtypes[t] = dtypes.get(t, 0) + 1
        print('  %s' % os.path.basename(path))
        print('     大小 %d | 头部 %d bytes | 张量 %d' % (size, hlen, len(keys)))
        print('     数据区 %d（应 %d，实际覆盖到 %d）连续=%s'
              % (expected, expected, cur, contiguous))
        print('     dtype 分布 %s' % dtypes)
        print('     -> %s' % ('完整 ✓' if ok else '异常 ✗'))
    return ok


if __name__ == '__main__':
    import sys
    if len(sys.argv) < 2:
        print('用法: python verify-workflow.py <工作流.json> [模型.safetensors ...]')
        sys.exit(1)
    target = sys.argv[1]
    if target.endswith('.json'):
        print('=== 工作流连线一致性 ===')
        good = check_workflow(target)
        for p in sys.argv[2:]:
            good = check_safetensors(p) and good
        print('=== 结果:', 'PASS' if good else 'FAIL', '===')
