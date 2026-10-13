"""输出打包:把脚本、引用、使用指南、免责声明写进产物目录。

让产出成为一个可用、可售卖(经审核后)的完整包,而不只是一个 mp4。
所有产物默认标注为“需专业审核的草稿”。
"""

from __future__ import annotations

import json
from pathlib import Path

from .knowledge import citation_text, load_method, load_safety_rules
from .models import StoryScript, TrainingModule
from .validate import ValidationReport

_SENTENCE_ZH = {
    "descriptive": "描述句",
    "perspective": "观点句",
    "affirmative": "肯定句",
    "directive": "指导句",
}


def write_script_json(script: StoryScript, out_dir: Path) -> Path:
    path = Path(out_dir) / "script.json"
    path.write_text(script.model_dump_json(indent=2), encoding="utf-8")
    return path


def write_script_md(script: StoryScript, out_dir: Path) -> Path:
    lines = [
        f"# {script.title_zh} / {script.title_en}",
        "",
        f"**学习目标**:{script.learning_goal}",
        "",
        "> 草稿 · 需专业审核(Draft · needs professional review)",
        "",
    ]
    for s in script.scenes:
        st = _SENTENCE_ZH.get(s.sentence_type.value, s.sentence_type.value)
        lines += [
            f"## 第 {s.index} 屏 · {st}({s.sentence_type.value}) {s.icon}",
            f"- **中文**:{s.text_zh}",
            f"- **English**: {s.text_en}",
            f"- 旁白(zh):{s.narration_zh}",
            f"- 旁白(en):{s.narration_en}",
            f"- 画面:{s.visual_keyword}",
            "",
        ]
    path = Path(out_dir) / "script.md"
    path.write_text("\n".join(lines), encoding="utf-8")
    return path


def write_citations_md(script: StoryScript, out_dir: Path) -> Path:
    method = load_method(script.method_id)
    used = script.citations_used or method.get("citations", [])
    lines = [
        "# 引用来源 / References",
        "",
        f"方法:{method.get('name_zh','')} / {method.get('name_en','')}"
        f"(证据水平:{method.get('evidence_level','')})",
        "",
        "本内容依据以下文献/标准编写:",
        "",
    ]
    for cid in used:
        lines.append(f"- {citation_text(cid)}")
    lines += [
        "",
        "> ⚠️ 商用售卖前,请核对每条引用的卷期/页码/DOI 原文,勿在未核实的情况下对外承诺具体疗效数据。",
    ]
    path = Path(out_dir) / "citations.md"
    path.write_text("\n".join(lines), encoding="utf-8")
    return path


def write_disclaimer(out_dir: Path) -> Path:
    safety = load_safety_rules()
    d = safety.get("disclaimer", {})
    text = (d.get("zh", "").strip() + "\n\n" + d.get("en", "").strip()).strip() + "\n"
    path = Path(out_dir) / "DISCLAIMER.txt"
    path.write_text(text, encoding="utf-8")
    return path


def write_guide(script: StoryScript, report: ValidationReport, out_dir: Path) -> Path:
    method = load_method(script.method_id)
    safety = load_safety_rules()
    reminders = safety.get("review_reminders_zh", [])

    status = "✅ 通过基础校验" if report.passed else "⚠️ 未通过基础校验(见下方问题,需修改后再用)"
    lines = [
        f"# 使用指南 · {script.title_zh}",
        "",
        f"**学习目标**:{script.learning_goal}",
        "",
        "## 这是什么",
        f"这是一份「{method.get('name_zh','社交故事')}」——{method.get('one_line_zh','')}",
        "它属于被研究证据支持的干预方法(见 citations.md)。",
        "",
        "## 怎么用(给家长/老师)",
        "- 在情境发生**之前**,和孩子一对一、平静地一起看这段视频或读文字。",
        "- 可以多次重复观看,建立熟悉感与预期。",
        "- 让孩子按自己的节奏参与:可以指一指画面、跟读句子。",
        "- 保持环境低刺激(柔和光线、较小音量),配音语速已调慢。",
        "- 把故事里的说法和孩子真实会遇到的流程对应起来(如就诊流程、老师称呼)。",
        "",
        "## 校验结果",
        f"- 状态:{status}",
        f"- 是否需专业审核:{'是(所有产物默认需专业人员审核)' if report.review_required else '否'}",
    ]
    if report.errors:
        lines.append("- 需修正的问题:")
        lines += [f"  - {e}" for e in report.errors]
    if report.warnings:
        lines.append("- 提醒(warning):")
        lines += [f"  - {w}" for w in report.warnings]

    lines += ["", "## 售卖/正式使用前的复核清单"]
    lines += [f"- {r}" for r in reminders]
    if script.review_flags:
        lines += ["", "## 生成侧自评注意点"]
        lines += [f"- {f}" for f in script.review_flags]

    lines += [
        "",
        "---",
        "⚠️ 本内容为辅助/教育工具,不替代专业评估、诊断或治疗,不做任何疗效承诺。详见 DISCLAIMER.txt。",
    ]
    path = Path(out_dir) / "guide.md"
    path.write_text("\n".join(lines), encoding="utf-8")
    return path


def write_all(script: StoryScript, report: ValidationReport, out_dir: Path) -> dict:
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    return {
        "script_json": write_script_json(script, out_dir),
        "script_md": write_script_md(script, out_dir),
        "citations_md": write_citations_md(script, out_dir),
        "guide_md": write_guide(script, report, out_dir),
        "disclaimer": write_disclaimer(out_dir),
    }


# =====================================================================
# 训练模块(Video Modeling)打包:模块 JSON / 可读脚本 / 引用 / 训练指南+记录表
# =====================================================================
_CARD_KIND_ZH = {
    "step": "步骤卡", "emotion": "情绪卡", "choice": "选择卡",
    "schedule": "流程卡", "reminder": "提醒卡",
}


def write_training_json(module: TrainingModule, out_dir: Path) -> Path:
    path = Path(out_dir) / "module.json"
    path.write_text(module.model_dump_json(indent=2), encoding="utf-8")
    return path


def write_training_md(module: TrainingModule, out_dir: Path) -> Path:
    L = [
        f"# {module.title_zh} / {module.title_en}",
        "",
        f"**训练目标(可测量)**:{module.learning_objective}",
        "",
        "> 草稿 · 需专业审核(Draft · needs professional review)",
        "",
        "## 开场", module.intro_zh, f"*{module.intro_en}*", "",
        "## 示范段(Video Modeling)",
    ]
    for s in module.steps:
        L.append(f"{s.index}. {s.icon} {s.text_zh} — {s.text_en}")
    L += ["", "## 练习段(提示 → 留白 → 示范 → 鼓励)"]
    for t in module.practice_trials:
        L += [
            f"### 回合 {t.index}",
            f"- 提示:{t.prompt_zh}",
            f"- 留白:{t.pause_seconds:.0f} 秒(轮到孩子作答)",
            f"- 示范:{t.answer_zh}",
            f"- 鼓励:{t.reinforce_zh}",
            "",
        ]
    if module.social_choice is not None:
        sc = module.social_choice
        L += ["## 社交情境 · 选择", sc.scenario_zh, ""]
        for i, o in enumerate(sc.options):
            L.append(f"- {'ABCD'[i]}. {o.label_zh} → {o.outcome_zh}")
        L.append("")
    L += ["## 收尾", module.review_zh, ""]
    if module.visual_cards:
        L += ["## 配套视觉卡片(见 images/)"]
        for c in module.visual_cards:
            kind = _CARD_KIND_ZH.get(c.kind, "卡片")
            L.append(f"- [{kind}] {c.title_zh}:{c.caption_zh}")
    path = Path(out_dir) / "script.md"
    path.write_text("\n".join(L), encoding="utf-8")
    return path


def write_training_citations_md(module: TrainingModule, out_dir: Path) -> Path:
    method = load_method(module.method_id)
    used = module.citations_used or method.get("citations", [])
    lines = [
        "# 引用来源 / References",
        "",
        f"方法:{method.get('name_zh','')} / {method.get('name_en','')}"
        f"(证据水平:{method.get('evidence_level','')})",
        "",
        "本训练模块依据以下文献/标准编写:",
        "",
    ]
    for cid in used:
        lines.append(f"- {citation_text(cid)}")
    lines += [
        "",
        "> ⚠️ 商用售卖前,请核对每条引用的卷期/页码/DOI 原文,勿在未核实的情况下对外承诺具体疗效数据。",
    ]
    path = Path(out_dir) / "citations.md"
    path.write_text("\n".join(lines), encoding="utf-8")
    return path


def write_training_guide(module: TrainingModule, report: ValidationReport, out_dir: Path) -> Path:
    method = load_method(module.method_id)
    safety = load_safety_rules()
    reminders = safety.get("review_reminders_zh", [])
    status = "✅ 通过基础校验" if report.passed else "⚠️ 未通过基础校验(见下方问题,需修改后再用)"

    lines = [
        f"# 训练指南 · {module.title_zh}",
        "",
        f"**训练目标(可测量)**:{module.learning_objective}",
        "",
        "## 这是什么",
        f"这是一个「{method.get('name_zh','视频示范训练')}」训练模块——{method.get('one_line_zh','')}",
        "视频本身就是一次结构化的康复训练:先示范,再让孩子在“轮到你”的留白处练习。",
        "",
        "## 怎么带孩子做(给训练师/家长)",
        "1. **一对一、低刺激环境**:柔和光线、较小音量,和孩子并排坐,一起看。",
        "2. **示范段**:陪孩子安静看完“示范”几步,可以指一指画面、跟读关键句。",
        "3. **练习段(核心)**:每到“⏳ 轮到你”画面,视频会**留白静默**——鼓励孩子自己说/做。",
        "   - 若孩子没反应,用**由少到多的提示**:先等一等 → 用眼神/手势 → 说出开头一个字 → 完整示范。",
        "   - 孩子一旦有尝试,**立刻具体地表扬**(如“你自己说出来了!”);之后视频也会给出示范与鼓励。",
        "4. **社交选择段**:和孩子讨论每个选择会怎样,强调“都可以,只是……更合适”。",
        "5. **迁移到真实生活**:当天在真实情境里再练 1–2 次(换人物/场景),帮助泛化。",
        "6. 可**多次重复观看**,建立熟悉与预期;把视频里的说法对应到孩子真实会遇到的情境。",
        "",
        "## 配套图片(images/)",
        "把 images/ 里的视觉卡片打印出来,贴在墙上或做成小卡,离屏时也能随时提示、练习。",
        "",
        "## 练习记录表(可复印)",
        "每次练习给孩子的每个回合打勾,便于观察进步:",
        "",
        "| 日期 | 回合/技能 | 独立完成 | 需提示 | 未反应 | 备注 |",
        "|------|-----------|:------:|:----:|:----:|------|",
    ]
    for t in module.practice_trials:
        lines.append(f"| ____ | 回合{t.index} | ☐ | ☐ | ☐ | ____ |")
    lines += [
        "",
        "> 目标示例:连续 2–3 次练习中,多数回合能“独立完成”即可视为初步掌握,再逐步撤除提示与视频支持。",
        "",
        "## 校验结果",
        f"- 状态:{status}",
        f"- 是否需专业审核:{'是(所有产物默认需专业人员审核)' if report.review_required else '否'}",
    ]
    if report.errors:
        lines.append("- 需修正的问题:")
        lines += [f"  - {e}" for e in report.errors]
    if report.warnings:
        lines.append("- 提醒(warning):")
        lines += [f"  - {w}" for w in report.warnings]

    lines += ["", "## 售卖/正式使用前的复核清单"]
    lines += [f"- {r}" for r in reminders]
    if module.review_flags:
        lines += ["", "## 生成侧自评注意点"]
        lines += [f"- {f}" for f in module.review_flags]

    lines += [
        "",
        "---",
        "⚠️ 本内容为辅助/教育工具,不替代专业评估、诊断或治疗,不做任何疗效承诺。详见 DISCLAIMER.txt。",
    ]
    path = Path(out_dir) / "guide.md"
    path.write_text("\n".join(lines), encoding="utf-8")
    return path


def write_all_training(module: TrainingModule, report: ValidationReport, out_dir: Path) -> dict:
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    return {
        "module_json": write_training_json(module, out_dir),
        "script_md": write_training_md(module, out_dir),
        "citations_md": write_training_citations_md(module, out_dir),
        "guide_md": write_training_guide(module, report, out_dir),
        "disclaimer": write_disclaimer(out_dir),
    }
