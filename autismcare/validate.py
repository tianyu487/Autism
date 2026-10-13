"""社交故事 lint + 安全门禁。

产出一个 ValidationReport:
- passed        : 是否通过硬性校验(句型比、无黑名单词、有第一人称、场景数)
- blocked       : 命中硬错误(如恐吓词/句型比失衡)—— 产物会被打上 DRAFT 且不进"成品"名
- review_required: 恒为 True —— 任何产物都需专业人员审核
- errors/warnings: 明细
"""

from __future__ import annotations

from dataclasses import dataclass, field

from .knowledge import load_method, load_safety_rules
from .models import SentenceType, StoryScript, TrainingModule


@dataclass
class ValidationReport:
    passed: bool = True
    blocked: bool = False
    review_required: bool = True          # 硬性:永远需要人工审核
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

    def add_error(self, msg: str) -> None:
        self.errors.append(msg)
        self.passed = False
        self.blocked = True

    def add_warning(self, msg: str) -> None:
        self.warnings.append(msg)


def validate_script(script: StoryScript) -> ValidationReport:
    rules = load_safety_rules().get("lint", {})
    banned = load_safety_rules().get("banned_words", {})
    report = ValidationReport()

    scenes = script.scenes
    n = len(scenes)

    # 1) 场景数量
    min_scenes = int(rules.get("min_scenes", 5))
    max_scenes = int(rules.get("max_scenes", 12))
    if n < min_scenes:
        report.add_error(f"场景数过少:{n} < 最少 {min_scenes}")
    if n > max_scenes:
        report.add_warning(f"场景数偏多:{n} > 建议上限 {max_scenes}")

    # 2) 句型基本比:(描述+观点+肯定) / 指导 >= 阈值
    desc_group = {SentenceType.descriptive, SentenceType.perspective, SentenceType.affirmative}
    n_desc = sum(1 for s in scenes if s.sentence_type in desc_group)
    n_dir = sum(1 for s in scenes if s.sentence_type == SentenceType.directive)
    min_ratio = float(rules.get("min_descriptive_per_directive", 2.0))
    if n_dir > 0:
        ratio = n_desc / n_dir
        if ratio < min_ratio:
            report.add_error(
                f"句型基本比不达标:描述类/指导类 = {n_desc}/{n_dir} = {ratio:.2f} "
                f"< 要求 {min_ratio}(社交故事应描述为主、指导为辅)"
            )
    elif n_dir == 0 and n >= min_scenes:
        report.add_warning("没有任何指导句:可考虑加入 1 句温和的'我可以怎么做'。")

    # 3) 第一人称
    if rules.get("require_first_person", True):
        zh_all = " ".join(s.text_zh for s in scenes)
        en_all = " ".join(f" {s.text_en} " for s in scenes)
        zh_ok = any(m in zh_all for m in rules.get("first_person_markers_zh", ["我"]))
        en_ok = any(m in en_all for m in rules.get("first_person_markers_en", [" I "]))
        if not zh_ok:
            report.add_error("中文缺少第一人称('我'):社交故事应从孩子视角讲述。")
        if not en_ok:
            report.add_warning("英文似乎缺少第一人称(I / my / me)。")

    # 4) 单屏字数
    max_chars = int(rules.get("max_zh_chars_per_scene", 60))
    for s in scenes:
        if len(s.text_zh) > max_chars:
            report.add_warning(f"第 {s.index} 屏中文偏长({len(s.text_zh)} 字 > {max_chars}),不利阅读。")

    # 5) 负面 / 恐吓 / 绝对化黑名单
    zh_words = banned.get("zh", []) or []
    en_words = [w.lower() for w in (banned.get("en", []) or [])]
    for s in scenes:
        for w in zh_words:
            if w and w in (s.text_zh + s.narration_zh):
                report.add_error(f"第 {s.index} 屏命中负面/恐吓用语:'{w}'(社交故事应正向、留弹性)。")
        low = (s.text_en + " " + s.narration_en).lower()
        for w in en_words:
            if w and w in low:
                report.add_error(f"第 {s.index} 屏英文命中负面用语:'{w}'。")

    return report


# =====================================================================
# 训练模块(Video Modeling)校验:训练效果的硬性门禁
# =====================================================================
def _scan_banned(report: ValidationReport, banned: dict, label: str,
                 zh_text: str, en_text: str = "") -> None:
    """在一段中/英文本里扫描负面/恐吓黑名单,命中即记为硬错误。"""
    for w in banned.get("zh", []) or []:
        if w and w in zh_text:
            report.add_error(f"{label}命中负面/恐吓用语:'{w}'(应正向、留弹性)。")
    low = en_text.lower()
    for w in (banned.get("en", []) or []):
        if w and w.lower() in low:
            report.add_error(f"{label}英文命中负面用语:'{w}'。")


def validate_training(module: TrainingModule) -> ValidationReport:
    """训练模块校验:确保它真的是'能练到东西'的训练,而非被动播放。"""
    try:
        g = load_method(module.method_id or "video_modeling").get("per_module_guidance_zh", {}) or {}
    except FileNotFoundError:
        # 该 method_id 在库里无专属规则文件(如仅登记于 _registry) → 用默认阈值,不阻断
        g = {}
    banned = load_safety_rules().get("banned_words", {})
    report = ValidationReport()

    min_steps, max_steps = int(g.get("min_steps", 3)), int(g.get("max_steps", 6))
    min_trials, max_trials = int(g.get("min_trials", 2)), int(g.get("max_trials", 4))
    min_cards = int(g.get("min_cards", 3))

    # 1) 训练目标必须存在(且应可观察/可测量)
    if not module.learning_objective.strip():
        report.add_error("缺少训练目标 learning_objective(必须是一句可观察、可测量的目标)。")

    # 2) 示范步骤数
    ns = len(module.steps)
    if ns < min_steps:
        report.add_error(f"示范步骤过少:{ns} < 最少 {min_steps}(需把技能拆成清晰小步)。")
    elif ns > max_steps:
        report.add_warning(f"示范步骤偏多:{ns} > 建议上限 {max_steps}。")

    # 3) 练习回合 —— 训练效果的核心:必须有"留白让孩子练"
    nt = len(module.practice_trials)
    if nt < min_trials:
        report.add_error(f"练习回合过少:{nt} < 最少 {min_trials}(没有'留白让孩子练'就不成其为训练)。")
    elif nt > max_trials:
        report.add_warning(f"练习回合偏多:{nt} > 建议上限 {max_trials}。")
    for t in module.practice_trials:
        if not (t.prompt_zh.strip() and t.answer_zh.strip() and t.reinforce_zh.strip()):
            report.add_error(f"第 {t.index} 个练习回合缺少 提示/示范/鼓励 之一(回合结构不完整)。")
        if t.pause_seconds < 2:
            report.add_warning(f"第 {t.index} 个回合留白仅 {t.pause_seconds}s,可能太短,孩子来不及作答。")

    # 4) 社交选择段(存在则校验)
    if module.social_choice is not None:
        opts = module.social_choice.options
        if len(opts) < 2:
            report.add_error("社交情境选择至少要有 2 个选项。")
        for o in opts:
            if not o.outcome_zh.strip():
                report.add_error("社交选项缺少结果反馈 outcome(每个选择都应有温和反馈)。")

    # 5) 视觉支持卡片
    if len(module.visual_cards) < min_cards:
        report.add_warning(f"配套图片偏少:{len(module.visual_cards)} < 建议 {min_cards} 张。")

    # 6) 负面/恐吓黑名单(全模块扫描)
    _scan_banned(report, banned, "开场", module.intro_zh, module.intro_en)
    for s in module.steps:
        _scan_banned(report, banned, f"示范第 {s.index} 步",
                     s.text_zh + s.narration_zh, s.text_en + " " + s.narration_en)
    for t in module.practice_trials:
        _scan_banned(report, banned, f"练习第 {t.index} 回合",
                     t.prompt_zh + t.answer_zh + t.reinforce_zh,
                     " ".join([t.prompt_en, t.answer_en, t.reinforce_en]))
    if module.social_choice is not None:
        sc = module.social_choice
        _scan_banned(report, banned, "社交情境", sc.scenario_zh, sc.scenario_en)
        for o in sc.options:
            _scan_banned(report, banned, "社交选项",
                         o.label_zh + o.outcome_zh, o.label_en + " " + o.outcome_en)
    for c in module.visual_cards:
        _scan_banned(report, banned, f"卡片「{c.title_zh}」",
                     c.title_zh + c.caption_zh, c.title_en + " " + c.caption_en)
    _scan_banned(report, banned, "收尾", module.review_zh, module.review_en)

    return report
