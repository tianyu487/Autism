# -*- coding: utf-8 -*-
"""
autismcare 内容模型 v1(扁平 module.json) <-> v2(内容契约)转换器。

设计要点(见 content_model_v2.md):
- v2 是"未来的唯一真源":每个 beat 有稳定 id;每个可本地化文本变成语言键值容器
  i18n = {"zh":..., "en":..., "yue":...};并把"字幕(text)"与"旁白(narration)"分开。
- 向后兼容靠 to_legacy(v2) -> 精确复原当前扁平 module.json,现有管线原样能跑,零风险。
- 粤语(yue)与分支(goto)先留位、默认 null,二期再填,不改结构。

用法:
  python convert_module.py upgrade   in_module.json   out.v2.json
  python convert_module.py downgrade in.v2.json       out_module.json
  python convert_module.py selftest  module.json [module2.json ...]   # 往返无损校验
  python convert_module.py batch     <dir-with-module.json>           # 批量升级为 *.v2.json
"""
from __future__ import annotations
import json, sys, copy
from pathlib import Path

SCHEMA_VERSION = 2


def i18n(zh, en=None, yue=None):
    """一个可本地化文本:语言 -> 文本。yue(粤语)先留位。"""
    return {"zh": zh, "en": en, "yue": yue}


# ---------------------------------------------------------------- upgrade v1 -> v2
def upgrade(m: dict, *, slug: str | None = None) -> dict:
    v2: dict = {
        "schema_version": SCHEMA_VERSION,
        "id": slug,                                  # 复原时忽略(扁平无此字段)
        "languages": ["zh", "en"],                   # 已填充的语言;粤语二期加 "yue"
        "method_id": m["method_id"],
        "cast": m.get("cast"),
        "learning_objective": i18n(m["learning_objective"]),   # 多语言家长/教师指南要用,故本地化(先只填 zh)
        "title":  i18n(m["title_zh"],  m["title_en"]),
        "intro":  i18n(m["intro_zh"],  m["intro_en"]),
        "review": i18n(m["review_zh"], m["review_en"]),
        "steps": [
            {
                "id": f"step{s['index']}",
                "index": s["index"],
                "text":      i18n(s["text_zh"],      s["text_en"]),        # 屏幕字幕
                "narration": i18n(s["narration_zh"], s["narration_en"]),   # 旁白稿(可与字幕不同)
                "visual_keyword": s.get("visual_keyword"),
                "icon": s.get("icon"),
                "min_seconds": s.get("duration_hint"),   # 由“固定时长”降级为“建议下限”,真实时长在装配时按音频定
            }
            for s in m["steps"]
        ],
        "practice_trials": [
            {
                "id": f"trial{t['index']}",
                "index": t["index"],
                "prompt":    i18n(t["prompt_zh"],    t["prompt_en"]),
                "answer":    i18n(t["answer_zh"],    t["answer_en"]),
                "reinforce": i18n(t["reinforce_zh"], t["reinforce_en"]),
                "pause_seconds": t.get("pause_seconds"),   # “轮到你”留白下限
                "icon": t.get("icon"),
            }
            for t in m["practice_trials"]
        ],
        "social_choice": None,
        "visual_cards": [
            {
                "kind": c["kind"],
                "title":   i18n(c["title_zh"],   c["title_en"]),
                "caption": i18n(c["caption_zh"], c["caption_en"]),
                "icon": c.get("icon"),
            }
            for c in m["visual_cards"]
        ],
        "citations_used": m.get("citations_used", []),   # 引用 id,语言中性,不本地化
        "review_flags": [i18n(x) for x in m.get("review_flags", [])],   # 草稿提示会进指南,故本地化
        "page_visuals": m.get("page_visuals", {}),   # 画面提示保持英文原样,不本地化
    }

    sc = m.get("social_choice")
    if sc is not None:
        v2["social_choice"] = {
            "id": "choice",
            "scenario": i18n(sc["scenario_zh"], sc["scenario_en"]),
            "icon": sc.get("icon"),
            "options": [
                {
                    "id": "ABCD"[k],
                    "label":   i18n(o["label_zh"],   o["label_en"]),
                    "outcome": i18n(o["outcome_zh"], o["outcome_en"]),
                    "icon": o.get("icon"),
                    "goto": None,             # 互动分支目标 beat-id;null=线性继续。二期用。
                }
                for k, o in enumerate(sc["options"])
            ],
        }

    # 记录原文件里"可选键"的实际存在情况,保证 downgrade 能精确复原(不多不少)
    v2["_present"] = {
        "cast": "cast" in m,
        "social_choice": "social_choice" in m,
        "page_visuals": "page_visuals" in m,
        "citations_used": "citations_used" in m,
        "review_flags": "review_flags" in m,
    }
    return v2


# -------------------------------------------------------------- downgrade v2 -> v1
def to_legacy(v2: dict) -> dict:
    """精确复原当前扁平 module.json(丢弃 v2 专属的 id/tracks/yue/goto/schema_version)。"""
    present = v2.get("_present", {})
    always = lambda key: True

    m: dict = {
        "title_zh": v2["title"]["zh"], "title_en": v2["title"]["en"],
        "learning_objective": v2["learning_objective"]["zh"],
        "method_id": v2["method_id"],
        "intro_zh": v2["intro"]["zh"], "intro_en": v2["intro"]["en"],
        "steps": [
            {
                "index": s["index"],
                "text_zh": s["text"]["zh"], "text_en": s["text"]["en"],
                "narration_zh": s["narration"]["zh"], "narration_en": s["narration"]["en"],
                "visual_keyword": s["visual_keyword"],
                "icon": s["icon"],
                "duration_hint": s["min_seconds"],
            }
            for s in v2["steps"]
        ],
        "practice_trials": [
            {
                "index": t["index"],
                "prompt_zh": t["prompt"]["zh"], "prompt_en": t["prompt"]["en"],
                "pause_seconds": t["pause_seconds"],
                "answer_zh": t["answer"]["zh"], "answer_en": t["answer"]["en"],
                "reinforce_zh": t["reinforce"]["zh"], "reinforce_en": t["reinforce"]["en"],
                "icon": t["icon"],
            }
            for t in v2["practice_trials"]
        ],
    }
    if present.get("social_choice", v2.get("social_choice") is not None) and v2.get("social_choice"):
        sc = v2["social_choice"]
        m["social_choice"] = {
            "scenario_zh": sc["scenario"]["zh"], "scenario_en": sc["scenario"]["en"],
            "options": [
                {
                    "label_zh": o["label"]["zh"], "label_en": o["label"]["en"],
                    "outcome_zh": o["outcome"]["zh"], "outcome_en": o["outcome"]["en"],
                    "icon": o["icon"],
                }
                for o in sc["options"]
            ],
            "icon": sc["icon"],
        }
    m["visual_cards"] = [
        {
            "kind": c["kind"],
            "title_zh": c["title"]["zh"], "title_en": c["title"]["en"],
            "caption_zh": c["caption"]["zh"], "caption_en": c["caption"]["en"],
            "icon": c["icon"],
        }
        for c in v2["visual_cards"]
    ]
    m["review_zh"] = v2["review"]["zh"]
    m["review_en"] = v2["review"]["en"]
    if present.get("citations_used", True):
        m["citations_used"] = v2.get("citations_used", [])
    if present.get("review_flags", True):
        m["review_flags"] = [x["zh"] for x in v2.get("review_flags", [])]
    if present.get("cast", v2.get("cast") is not None):
        m["cast"] = v2.get("cast")
    if present.get("page_visuals", True):
        m["page_visuals"] = v2.get("page_visuals", {})
    return m


# ----------------------------------------------------------------- beat 顺序(文档化)
def beat_order(v2: dict) -> list[str]:
    """由语义结构派生的规范 beat 序列 —— 与 pipeline.emit 及 page_visuals 的键完全一致。"""
    ids = ["title", "intro"]
    ids += [s["id"] for s in v2["steps"]]
    for t in v2["practice_trials"]:
        ids += [f"{t['id']}_prompt", f"{t['id']}_answer", f"{t['id']}_reinforce"]
    if v2.get("social_choice"):
        ids.append("choice")
        ids += [f"choice_{o['id']}" for o in v2["social_choice"]["options"]]
    ids.append("review")
    return ids


# ------------------------------------------------------------------------- 命令行
def _load(p): return json.loads(Path(p).read_text(encoding="utf-8"))
def _dump(obj, p): Path(p).write_text(json.dumps(obj, ensure_ascii=False, indent=2), encoding="utf-8")


def selftest(paths: list[str]) -> bool:
    ok = True
    for p in paths:
        orig = _load(p)
        v2 = upgrade(orig, slug=Path(p).stem)
        back = to_legacy(v2)
        same = (orig == back)
        # page_visuals 键是否与派生 beat 序列一致(有 page_visuals 时校验)
        pv = orig.get("page_visuals") or {}
        beats = beat_order(v2)
        pv_ok = (not pv) or (set(pv.keys()) == set(beats))
        print(f"  {'OK ' if (same and pv_ok) else 'FAIL'}  {Path(p).name:22s} "
              f"round-trip={'lossless' if same else 'LOSSY'}  "
              f"beats={len(beats)}  page_visuals={'—' if not pv else ('match' if pv_ok else 'MISMATCH')}")
        if not same:
            ok = False
            # 指出第一处差异
            for k in sorted(set(orig) | set(back)):
                if orig.get(k) != back.get(k):
                    print(f"        diff at top-level key: {k}")
        if not pv_ok:
            ok = False
            print(f"        page_visuals extra={set(pv)-set(beats)} missing={set(beats)-set(pv)}")
    return ok


def main(argv):
    if not argv:
        print(__doc__); return 1
    cmd = argv[0]
    if cmd == "upgrade":
        _dump(upgrade(_load(argv[1]), slug=Path(argv[1]).stem), argv[2]); print("wrote", argv[2])
    elif cmd == "downgrade":
        _dump(to_legacy(_load(argv[1])), argv[2]); print("wrote", argv[2])
    elif cmd == "selftest":
        print("== round-trip self-test =="); ok = selftest(argv[1:]); print("ALL OK" if ok else "FAILURES"); return 0 if ok else 2
    elif cmd == "batch":
        d = Path(argv[1]); files = sorted(d.glob("*.json"))
        for f in files:
            if f.name.endswith(".v2.json"): continue
            _dump(upgrade(_load(f), slug=f.stem), f.with_suffix(".v2.json")); print("upgraded", f.name)
    else:
        print("unknown cmd", cmd); return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
