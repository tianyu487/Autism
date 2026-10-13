# -*- coding: utf-8 -*-
"""逐语言出片 CLI(Phase 1)。

读 v2 内容 + 已有的**无字底帧**(output/<slug>/_illus/),为每种语言各出一支 MP4,
汇总到 videos/<slug>.<lang>.mp4。中/英已在内容里;粤语二期填 yue 后加进 --langs 即可。

前置:该课 output/<slug>/_illus/ 需已补齐(train --scenes-only + gen_until_complete)。
用法:
  python packlang.py --script output\\calm_breathing\\module.v2.json --slug calm_breathing --langs zh,en
"""
from __future__ import annotations

import argparse
from pathlib import Path

try:
    from dotenv import load_dotenv
    load_dotenv()
except Exception:
    pass

from autismcare import multilang


def main() -> int:
    ap = argparse.ArgumentParser(prog="packlang", description="逐语言成片(中/英;粤二期)。")
    ap.add_argument("--script", required=True, help="v2 内容文件(*.v2.json)")
    ap.add_argument("--slug", required=True, help="课程 slug;须已有 output/<slug>/_illus 底帧")
    ap.add_argument("--langs", default="zh,en", help="逗号分隔,如 zh,en(默认 zh,en)")
    ap.add_argument("--out", default="output", help="输出根目录(默认 output)")
    a = ap.parse_args()

    langs = [x.strip() for x in a.langs.split(",") if x.strip()]
    print(f"· 逐语言出片:{a.slug}  langs={langs}")
    res = multilang.build_all(a.script, a.slug, langs, Path(a.out))
    print("\n=== 完成 ===")
    for L, p in res.items():
        print(f"  {L}: {p}")
    print("集中视频库:videos/<slug>.<lang>.mp4")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
