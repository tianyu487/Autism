# -*- coding: utf-8 -*-
"""Phase 1:逐语言成片。

读 v2 内容(content_v2)+ 已生成的**无字底帧**(output/<slug>/_illus/),
按语言各出一支自配速的 MP4(免费档形态 A':一语言一个文件、哪都能放、切=换文件)。

- 底帧语言无关(text-free 插画),同一张配任意语言字幕 → 不必逐语言重出图。
- 复用现有 render(烧该语言字幕)/ tts(该语言配音)/ video(合成),**不改核心 pipeline**。
- 中/英已在内容里;粤语二期只要给 narration.yue/字幕 yue 填值即可复用本模块(见下方派生词表)。

前置:该课的 output/<slug>/_illus/ 需已补齐(先跑 train --scenes-only + gen_until_complete)。
"""
from __future__ import annotations

import shutil
from dataclasses import dataclass
from pathlib import Path

from . import render, tts, video
from .content_v2 import ContentModuleV2, I18N, load_v2
from .models import ensure_dir

# 每语言的画面小提示 & 旁白派生词(中文行为与 pipeline.emit 完全一致;英文用原文;粤语二期填)
YOUR_TURN_NOTE = {"zh": "⏳ 轮到你,试试看 · Your turn",
                  "en": "⏳ Your turn — give it a try",
                  "yue": "⏳ 轮到你,试吓 · Your turn"}
REVIEW_NOTE = {"zh": "本内容为辅助/教育工具,不替代专业诊疗。",
               "en": "An educational aid — not a substitute for professional care.",
               "yue": "本内容为辅助/教育工具,唔代替专业诊疗。"}


def _t(x: I18N, lang: str) -> str:
    return x.get(lang) or ""


# —— 旁白派生:中文对 answer/choice/outcome 加语气词(与 emit 对齐);其它语言用原文 ——
def _answer_narr(a: I18N, lang: str) -> str:
    return ("可以这样说:" + _t(a, "zh")) if lang == "zh" else _t(a, lang)


def _choice_narr(s: I18N, lang: str) -> str:
    return (_t(s, "zh") + " 你会怎么做呢?") if lang == "zh" else _t(s, lang)


def _outcome_narr(label: I18N, outcome: I18N, lang: str) -> str:
    return (f"如果{_t(label,'zh')},{_t(outcome,'zh')}") if lang == "zh" else _t(outcome, lang)


@dataclass
class Beat:
    idx: int                 # 运行序号 → 对应 _illus/{idx:02d}_{name}.png
    name: str                # beat 名(title/intro/step1/trial1_prompt/choice/choice_A/review…)
    subtitle: I18N           # 烧在画面上的字幕(按语言取)
    narr: dict               # lang -> 旁白文本(已派生)
    note: dict               # lang -> 画面下方小提示("" = 无)
    tail: float              # 该页结尾静默/留白秒数


def build_beats(m: ContentModuleV2, langs: list[str]) -> list[Beat]:
    """由 v2 内容派生规范 beat 序列(与 pipeline.emit / page_visuals 键、顺序一致)。"""
    beats: list[Beat] = []
    i = 0

    def add(name, subtitle, narr_src, note=None, tail=video.SCENE_TAIL):
        nonlocal i
        narr = {L: (narr_src(L) if callable(narr_src) else _t(narr_src, L)) for L in langs}
        note = note or {}
        beats.append(Beat(i, name, subtitle, narr, {L: note.get(L, "") for L in langs}, tail))
        i += 1

    add("title", m.title, m.title)
    add("intro", m.intro, m.intro)
    for s in m.steps:
        add(s.id, s.text, s.narration)                       # 字幕=text,旁白=narration
    for t in m.practice_trials:
        add(f"{t.id}_prompt", t.prompt, t.prompt,
            note=YOUR_TURN_NOTE, tail=float(t.pause_seconds or video.SCENE_TAIL))
        add(f"{t.id}_answer", t.answer, (lambda L, a=t.answer: _answer_narr(a, L)))
        add(f"{t.id}_reinforce", t.reinforce, t.reinforce)
    if m.social_choice:
        sc = m.social_choice
        opt_note = {L: "   ".join(f"{o.id}. {_t(o.label, L)}" for o in sc.options) for L in langs}
        add("choice", sc.scenario, (lambda L, s=sc.scenario: _choice_narr(s, L)), note=opt_note)
        for o in sc.options:
            add(f"choice_{o.id}", o.outcome,
                (lambda L, lb=o.label, ou=o.outcome: _outcome_narr(lb, ou, L)),
                note={L: f"{o.id}. {_t(o.label, L)}" for L in langs})
    add("review", m.review, m.review, note=REVIEW_NOTE)
    return beats


def render_frames(beats: list[Beat], lang: str, illus_dir: Path, scenes_dir: Path) -> list[Path]:
    """逐 beat:取无字底帧 + 烧该语言字幕 → scenes_<lang>/。缺底帧则报错(先补齐插画)。"""
    ensure_dir(scenes_dir)
    frames: list[Path] = []
    for b in beats:
        illus = Path(illus_dir) / f"{b.idx:02d}_{b.name}.png"
        out = Path(scenes_dir) / f"{b.idx:02d}_{b.name}.png"
        if not (illus.exists() and illus.stat().st_size > 2000):
            raise FileNotFoundError(
                f"缺少底帧 {illus};请先把该课插画补齐到 19/19(train --scenes-only + gen_until_complete)。")
        render.render_illustrated(illus, zh=_t(b.subtitle, lang), en="", out_path=out,
                                  note=b.note.get(lang, ""))
        frames.append(out)
    return frames


def build_language_video(slug: str, lang: str, beats: list[Beat],
                         out_root: Path = Path("output")) -> Path:
    """出一支该语言 MP4:逐 beat 渲染画面 + 配音 + 合成,汇总到 videos/<slug>.<lang>.mp4。"""
    out_dir = ensure_dir(Path(out_root) / slug)
    illus_dir = out_dir / "_illus"
    scenes_dir = out_dir / f"scenes_{lang}"
    work = ensure_dir(out_dir / f"_work_{lang}")

    frames = render_frames(beats, lang, illus_dir, scenes_dir)
    clips: list[Path] = []
    for b, frame in zip(beats, frames):
        mp3 = tts.synth(b.narr[lang], lang, work / f"a_{b.idx:02d}.mp3")
        audio = video.make_scene_audio(mp3, None, work / f"audio_{b.idx:02d}.m4a", tail=b.tail)
        clips.append(video.make_scene_clip(frame, audio, work / f"clip_{b.idx:02d}.mp4"))
    final = video.concat_clips(clips, out_dir / f"final_{lang}.mp4", work)

    videos_dir = ensure_dir(Path(out_root).resolve().parent / "videos")
    dst = videos_dir / f"{slug}.{lang}.mp4"
    shutil.copy2(final, dst)
    shutil.rmtree(work, ignore_errors=True)
    return dst


def build_all(script_path: str | Path, slug: str, langs=("zh", "en"),
              out_root: Path = Path("output")) -> dict:
    """读 v2 文件 → 为每种语言各出一支 MP4。返回 {lang: mp4_path}。"""
    m = load_v2(script_path)
    beats = build_beats(m, list(langs))
    return {L: build_language_video(slug, L, beats, out_root) for L in langs}
