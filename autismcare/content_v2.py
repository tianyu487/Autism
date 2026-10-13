# -*- coding: utf-8 -*-
"""内容模型 v2 的读取层(pydantic v2)+ 到当前 TrainingModule 的桥接。

设计(见 phase0/content_model_v2.md):
- v2 是未来的唯一真源:稳定 beat id + 语言键值容器 i18n(区分字幕/旁白)+ 时间轴无关 + 预留粤语/分支。
- 现有管线仍吃扁平 TrainingModule;本模块提供:
    load_v2(path)            -> ContentModuleV2
    ContentModuleV2.to_legacy_dict() -> 扁平 dict(可直接喂 TrainingModule(**dict))
    load_training_any(path)  -> TrainingModule   # v1 直通、v2 自动降级;管线的单一接入点
- 只“新增读取能力”,不改 models.py、不改管线行为。零风险。
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Optional

from pydantic import BaseModel

from .models import TrainingModule


# ---------------------------------------------------------------- v2 模型
class I18N(BaseModel):
    """一个可本地化文本:语言 -> 文本。zh 通常有;en/yue 可为空(未提供)。"""
    zh: Optional[str] = None
    en: Optional[str] = None
    yue: Optional[str] = None

    def get(self, lang: str, fallback: str = "zh") -> Optional[str]:
        """取某语言文本;缺失时回退到 fallback 语言(默认中文)。"""
        return getattr(self, lang, None) or getattr(self, fallback, None)


class StepV2(BaseModel):
    id: str
    index: int
    text: I18N                 # 屏幕字幕
    narration: I18N            # 旁白稿(可与字幕不同,尤其粤语)
    visual_keyword: Optional[str] = None
    icon: Optional[str] = None
    min_seconds: Optional[float] = None


class TrialV2(BaseModel):
    id: str
    index: int
    prompt: I18N
    answer: I18N
    reinforce: I18N
    pause_seconds: Optional[float] = None
    icon: Optional[str] = None


class OptionV2(BaseModel):
    id: str
    label: I18N
    outcome: I18N
    icon: Optional[str] = None
    goto: Optional[str] = None   # 互动分支目标 beat-id;None=线性继续(二期用)


class SocialChoiceV2(BaseModel):
    id: str = "choice"
    scenario: I18N
    icon: Optional[str] = None
    options: list[OptionV2]


class VisualCardV2(BaseModel):
    kind: str
    title: I18N
    caption: I18N
    icon: Optional[str] = None


class PageVisualV2(BaseModel):
    visual_en: str = ""
    roles: Optional[list[str]] = None
    seed: Optional[int] = None


class ContentModuleV2(BaseModel):
    schema_version: int = 2
    id: Optional[str] = None
    languages: list[str] = ["zh", "en"]
    method_id: str
    cast: Optional[str] = None
    learning_objective: I18N
    title: I18N
    intro: I18N
    review: I18N
    steps: list[StepV2]
    practice_trials: list[TrialV2]
    social_choice: Optional[SocialChoiceV2] = None
    visual_cards: list[VisualCardV2] = []
    citations_used: list[str] = []
    review_flags: list[I18N] = []
    page_visuals: dict[str, PageVisualV2] = {}
    # 兼容:转换器写入的 _present 记账键(以及未来任何附加键)一律忽略,不报错。
    model_config = {"extra": "ignore"}

    # ---- 规范 beat 序列(与 pipeline.emit / page_visuals 键一致)----
    def beat_order(self) -> list[str]:
        ids = ["title", "intro"]
        ids += [s.id for s in self.steps]
        for t in self.practice_trials:
            ids += [f"{t.id}_prompt", f"{t.id}_answer", f"{t.id}_reinforce"]
        if self.social_choice:
            ids.append("choice")
            ids += [f"choice_{o.id}" for o in self.social_choice.options]
        ids.append("review")
        return ids

    # ---- 降级为当前扁平 module.json(可直接喂 TrainingModule(**dict))----
    def to_legacy_dict(self, lang: str = "zh") -> dict:
        """把 v2 摊平回当前扁平结构。lang 决定“中文槽”取哪种语言(默认 zh);
        英文槽固定取 en(现有管线把英文当字幕)。粤语出片时可传 lang='yue'。"""
        L = lambda x: x.get(lang)          # 主语言(中文槽)
        E = lambda x: x.en                 # 英文槽

        m: dict = {
            "title_zh": L(self.title), "title_en": E(self.title),
            "learning_objective": L(self.learning_objective),
            "method_id": self.method_id,
            "intro_zh": L(self.intro), "intro_en": E(self.intro),
            "steps": [
                {
                    "index": s.index,
                    "text_zh": L(s.text), "text_en": E(s.text),
                    "narration_zh": L(s.narration), "narration_en": E(s.narration),
                    "visual_keyword": s.visual_keyword,
                    "icon": s.icon,
                    "duration_hint": s.min_seconds,
                }
                for s in self.steps
            ],
            "practice_trials": [
                {
                    "index": t.index,
                    "prompt_zh": L(t.prompt), "prompt_en": E(t.prompt),
                    "pause_seconds": t.pause_seconds,
                    "answer_zh": L(t.answer), "answer_en": E(t.answer),
                    "reinforce_zh": L(t.reinforce), "reinforce_en": E(t.reinforce),
                    "icon": t.icon,
                }
                for t in self.practice_trials
            ],
            "visual_cards": [
                {
                    "kind": c.kind,
                    "title_zh": L(c.title), "title_en": E(c.title),
                    "caption_zh": L(c.caption), "caption_en": E(c.caption),
                    "icon": c.icon,
                }
                for c in self.visual_cards
            ],
            "review_zh": L(self.review), "review_en": E(self.review),
            "citations_used": list(self.citations_used),
            "review_flags": [L(f) for f in self.review_flags],
            "cast": self.cast,
            "page_visuals": {
                k: {"visual_en": pv.visual_en, "roles": pv.roles, "seed": pv.seed}
                for k, pv in self.page_visuals.items()
            },
        }
        if self.social_choice is not None:
            sc = self.social_choice
            m["social_choice"] = {
                "scenario_zh": L(sc.scenario), "scenario_en": E(sc.scenario),
                "options": [
                    {
                        "label_zh": L(o.label), "label_en": E(o.label),
                        "outcome_zh": L(o.outcome), "outcome_en": E(o.outcome),
                        "icon": o.icon,
                    }
                    for o in sc.options
                ],
                "icon": sc.icon,
            }
        return m

    def to_training_module(self, lang: str = "zh") -> TrainingModule:
        """构造当前管线用的 TrainingModule 对象。"""
        return TrainingModule(**self.to_legacy_dict(lang=lang))


# ------------------------------------------------------------------- 加载
def load_v2(path: str | Path) -> ContentModuleV2:
    return ContentModuleV2(**json.loads(Path(path).read_text(encoding="utf-8")))


def _looks_v2(data: dict) -> bool:
    return int(data.get("schema_version", 0)) >= 2 or "title" in data and isinstance(data.get("title"), dict)


def load_training_any(path: str | Path, lang: str = "zh") -> TrainingModule:
    """管线的单一接入点:v1 扁平 module.json 直通;v2 自动降级。都返回 TrainingModule。

    之后把 pipeline.load_training_json 换成本函数即可让管线同时吃 v1/v2(行为对 v1 不变)。"""
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    if _looks_v2(data):
        return ContentModuleV2(**data).to_training_module(lang=lang)
    return TrainingModule(**data)
