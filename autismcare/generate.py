"""脚本生成:用循证方法库约束 Claude,产出结构化的中英双语社交故事。

生成方式:循证模板库(骨架/硬约束)+ Claude(个性化填充)。
用 output_config.format(json_schema)强制结构化输出,再用 pydantic 校验。
提供 --no-ai 用的内置样例脚本,便于在无密钥/离线时验证媒体管线。
"""

from __future__ import annotations

import json
import os

from .knowledge import (
    citation_text, find_skill_area, get_skill_area, list_skill_domains,
    load_method, load_safety_rules, load_skill_domain, pick_method_for_area,
)
from .models import (
    ChoiceOption, PracticeTrial, Scene, SentenceType, SocialChoiceScenario,
    StorySpec, StoryScript, TeachStep, TrainingModule, TrainingSpec, VisualCard,
)

DEFAULT_MODEL = os.environ.get("AUTISMCARE_MODEL", "claude-opus-4-8")

# ---- 给 Claude 的结构化输出 JSON Schema(手写,精确控制 required/additionalProperties)----
_SCENE_SCHEMA = {
    "type": "object",
    "properties": {
        "index": {"type": "integer", "description": "从 1 开始的场景序号"},
        "sentence_type": {
            "type": "string",
            "enum": [t.value for t in SentenceType],
            "description": "该句的句型",
        },
        "text_zh": {"type": "string", "description": "屏幕上显示的中文句子(简短)"},
        "text_en": {"type": "string", "description": "对应英文句子"},
        "narration_zh": {"type": "string", "description": "中文旁白稿"},
        "narration_en": {"type": "string", "description": "英文旁白稿"},
        "visual_keyword": {"type": "string", "description": "画面主体的简短关键词"},
        "icon": {"type": "string", "description": "代表该场景的单个 emoji"},
        "duration_hint": {"type": "number", "description": "建议停留秒数"},
    },
    "required": [
        "index", "sentence_type", "text_zh", "text_en",
        "narration_zh", "narration_en", "visual_keyword", "icon", "duration_hint",
    ],
    "additionalProperties": False,
}

STORY_SCHEMA = {
    "type": "object",
    "properties": {
        "title_zh": {"type": "string"},
        "title_en": {"type": "string"},
        "learning_goal": {"type": "string", "description": "一句话说明这份故事帮孩子学会什么"},
        "scenes": {"type": "array", "items": _SCENE_SCHEMA},
        "citations_used": {
            "type": "array",
            "items": {"type": "string"},
            "description": "用到的引用 id(从提供的方法库引用列表里选)",
        },
        "review_flags": {
            "type": "array",
            "items": {"type": "string"},
            "description": "生成侧自评、提醒人工复核的注意点",
        },
    },
    "required": ["title_zh", "title_en", "learning_goal", "scenes", "citations_used", "review_flags"],
    "additionalProperties": False,
}


def build_system_prompt(method_id: str = "social_stories") -> str:
    """把循证方法库的规则拼成系统提示(骨架/硬约束)。"""
    m = load_method(method_id)
    safety = load_safety_rules()
    lint = safety.get("lint", {})

    # 句型定义
    st_lines = []
    for key, info in (m.get("sentence_types") or {}).items():
        st_lines.append(f"- {key}({info.get('zh','')}):{info.get('desc_zh','')}")

    # 引用清单(给模型可选的 id)
    cite_lines = []
    for cid in m.get("citations", []):
        cite_lines.append(f"- {cid}: {citation_text(cid)}")

    rules = "\n".join(f"- {r}" for r in m.get("writing_rules_zh", []))
    ratio = lint.get("min_descriptive_per_directive", 2.0)

    return f"""你是一名精通自闭症循证干预的专家,尤其擅长按 Carol Gray 的「社交故事(Social Stories™)」标准撰写内容。
你的产出会被特教老师/康复师使用,并可能面向自闭症儿童家庭售卖,因此必须严格循证、正向、可靠。

【硬性写作规则】
{rules}

【句型系统】每一屏(scene)必须标注 sentence_type,取值只能是下列之一:
{chr(10).join(st_lines)}

【句型基本比(务必满足)】(描述句 descriptive + 观点句 perspective + 肯定句 affirmative)的数量 / 指导句 directive 的数量 >= {ratio}。
也就是:描述为主、指导为辅,让故事是在“分享信息”而不是“下命令”。指导句要少而正向(如“我可以试着…”)。

【语言】所有内容中英双语:text_zh/narration_zh 为中文,text_en/narration_en 为对应英文(自然、地道、适合朗读)。
narration 用于配音,可比屏幕文字略口语一点,但意思一致。

【结构】按真实先后顺序组织:标题 → 引入(说明这是安全、平常的情境)→ 过程分步(每屏一个要点)→ 结尾用肯定/安心的话赋能收束。
场景数量控制在 {lint.get('min_scenes',5)}–{lint.get('max_scenes',12)} 屏;单屏中文尽量不超过 {lint.get('max_zh_chars_per_scene',60)} 字。

【个性化】自然地融入孩子的名字与兴趣(用写实、贴切的方式,不要夸张或比喻失真),并照顾其感官特点。

【禁止】不得出现恐吓、负面或绝对化表达(如“很可怕”“必须每次”“打针很疼”);不得做任何“治愈/疗效”承诺。

【引用】citations_used 从下列 id 中挑选本故事所依据的方法来源(可多选):
{chr(10).join(cite_lines)}

【icon】每屏给一个简洁、具体、正向的单个 emoji 代表画面主体(如 🦷 🪑 👩‍⚕️ 🚗 🦕)。

只通过结构化输出返回 StoryScript,不要输出多余文字。"""


def build_user_prompt(spec: StorySpec) -> str:
    interests = "、".join(spec.interests) if spec.interests else "(未提供)"
    goal = spec.goal or "(未指定,请你根据情境合理推断一个正向、具体的学习目标)"
    return f"""请为下面这个孩子创作一份「社交故事」并按结构化格式返回。

- 目标场景 / 情境:{spec.situation}
- 学习目标:{goal}
- 孩子名字:{spec.child_name}
- 年龄:{spec.age} 岁
- 兴趣:{interests}
- 感官特点 / 需照顾的地方:{spec.sensory_notes or "(未提供)"}
- 阅读水平:{spec.reading_level}(simple=更简单;medium=适中)

请严格遵守系统提示中的所有循证规则(尤其是句型基本比与正向、字面表达)。"""


def generate_script(spec: StorySpec, model: str | None = None) -> StoryScript:
    """调用 Claude 生成结构化社交故事脚本。"""
    import anthropic  # 延迟导入,--no-ai 模式无需安装/联网

    client = anthropic.Anthropic()  # 从环境读取 ANTHROPIC_API_KEY
    model = model or DEFAULT_MODEL

    response = client.messages.create(
        model=model,
        max_tokens=16000,
        thinking={"type": "adaptive"},   # 让模型自行决定思考深度,提升对约束的遵守
        system=build_system_prompt(spec_method(spec)),
        messages=[{"role": "user", "content": build_user_prompt(spec)}],
        output_config={"format": {"type": "json_schema", "schema": STORY_SCHEMA}},
    )

    # output_config.format 保证首个 text 块是合法 JSON(可能前面有 thinking 块)
    text = next((b.text for b in response.content if b.type == "text"), None)
    if not text:
        raise RuntimeError("模型未返回结构化文本内容。")
    data = json.loads(text)
    return StoryScript(**data)


def spec_method(spec: StorySpec) -> str:
    """当前只做社交故事竖线;预留按 spec 选择方法的扩展点。"""
    return "social_stories"


# ---------------------------------------------------------------------------
# 内置样例脚本(--no-ai):用于在无密钥/离线时验证 TTS+画面+合成 媒体管线
# ---------------------------------------------------------------------------
def sample_script() -> StoryScript:
    scenes = [
        Scene(index=1, sentence_type=SentenceType.descriptive,
              text_zh="今天,我要去看牙医。", text_en="Today, I am going to the dentist.",
              narration_zh="今天,我要去看牙医。", narration_en="Today, I am going to see the dentist.",
              visual_keyword="牙医诊所", icon="🦷", duration_hint=6),
        Scene(index=2, sentence_type=SentenceType.descriptive,
              text_zh="牙医的诊所里,有一把可以往后躺的椅子。", text_en="At the dentist, there is a chair that leans back.",
              narration_zh="牙医的诊所里,有一把可以往后躺的椅子。", narration_en="At the dentist's office, there is a chair that leans back.",
              visual_keyword="牙科椅", icon="🪑", duration_hint=6),
        Scene(index=3, sentence_type=SentenceType.perspective,
              text_zh="牙医阿姨想帮我把牙齿照顾得很健康。", text_en="The dentist wants to help keep my teeth healthy.",
              narration_zh="牙医阿姨想帮我,把我的牙齿照顾得很健康。", narration_en="The dentist wants to help keep my teeth healthy.",
              visual_keyword="牙医", icon="👩‍⚕️", duration_hint=6),
        Scene(index=4, sentence_type=SentenceType.descriptive,
              text_zh="她会用小镜子,轻轻看看我的牙齿。", text_en="She uses a small mirror to gently look at my teeth.",
              narration_zh="她会用一面小镜子,轻轻地看看我的牙齿。", narration_en="She uses a small mirror to gently look at my teeth.",
              visual_keyword="小镜子", icon="🪞", duration_hint=6),
        Scene(index=5, sentence_type=SentenceType.affirmative,
              text_zh="检查牙齿是安全的,这很好。", text_en="Checking my teeth is safe. That is good.",
              narration_zh="检查牙齿是安全的,这很好。", narration_en="Checking my teeth is safe. That is good.",
              visual_keyword="安心", icon="😊", duration_hint=6),
        Scene(index=6, sentence_type=SentenceType.directive,
              text_zh="我可以试着张大嘴巴,像小恐龙打哈欠一样。", text_en="I can try to open wide, like a little dinosaur yawning.",
              narration_zh="我可以试着张大嘴巴,就像小恐龙打哈欠一样。", narration_en="I can try to open my mouth wide, like a little dinosaur yawning.",
              visual_keyword="张大嘴", icon="🦕", duration_hint=7),
        Scene(index=7, sentence_type=SentenceType.affirmative,
              text_zh="看完牙医,我做得很棒。", text_en="After the dentist, I did a great job.",
              narration_zh="看完牙医以后,我做得很棒。", narration_en="After seeing the dentist, I did a great job.",
              visual_keyword="做得好", icon="⭐", duration_hint=6),
    ]
    return StoryScript(
        title_zh="我第一次去看牙医",
        title_en="My First Visit to the Dentist",
        learning_goal="帮助孩子了解看牙医的流程,知道会发生什么、自己可以怎么做,从而减少焦虑。",
        method_id="social_stories",
        scenes=scenes,
        citations_used=["gray_2015_newbook", "wong_2015", "nac_2015"],
        review_flags=["内置样例,仅用于管线演示;正式使用前需专业人员按孩子情况调整。"],
    )


# ======================================================================
# 训练模块(Video Modeling)生成:schema + 受约束 Prompt + 内置样例
# ======================================================================
_TEACH_STEP_SCHEMA = {
    "type": "object",
    "properties": {
        "index": {"type": "integer"},
        "text_zh": {"type": "string", "description": "屏幕中文(简短,一步一个要点)"},
        "text_en": {"type": "string"},
        "narration_zh": {"type": "string", "description": "中文旁白"},
        "narration_en": {"type": "string", "description": "英文旁白(仅字幕)"},
        "visual_keyword": {"type": "string"},
        "icon": {"type": "string", "description": "单个 emoji"},
        "duration_hint": {"type": "number"},
    },
    "required": ["index", "text_zh", "text_en", "narration_zh", "narration_en",
                 "visual_keyword", "icon", "duration_hint"],
    "additionalProperties": False,
}

_PRACTICE_TRIAL_SCHEMA = {
    "type": "object",
    "properties": {
        "index": {"type": "integer"},
        "prompt_zh": {"type": "string", "description": "引出一次尝试的提示/提问"},
        "prompt_en": {"type": "string"},
        "pause_seconds": {"type": "number", "description": "留白静默秒数(2-10)"},
        "answer_zh": {"type": "string", "description": "示范的正确反应"},
        "answer_en": {"type": "string"},
        "reinforce_zh": {"type": "string", "description": "具体、正向的鼓励"},
        "reinforce_en": {"type": "string"},
        "icon": {"type": "string"},
    },
    "required": ["index", "prompt_zh", "prompt_en", "pause_seconds", "answer_zh",
                 "answer_en", "reinforce_zh", "reinforce_en", "icon"],
    "additionalProperties": False,
}

_CHOICE_OPTION_SCHEMA = {
    "type": "object",
    "properties": {
        "label_zh": {"type": "string"},
        "label_en": {"type": "string"},
        "outcome_zh": {"type": "string", "description": "温和、写实的结果反馈(无惩罚)"},
        "outcome_en": {"type": "string"},
        "icon": {"type": "string"},
    },
    "required": ["label_zh", "label_en", "outcome_zh", "outcome_en", "icon"],
    "additionalProperties": False,
}

_SOCIAL_CHOICE_SCHEMA = {
    "type": "object",
    "properties": {
        "scenario_zh": {"type": "string"},
        "scenario_en": {"type": "string"},
        "options": {"type": "array", "items": _CHOICE_OPTION_SCHEMA},
        "icon": {"type": "string"},
    },
    "required": ["scenario_zh", "scenario_en", "options", "icon"],
    "additionalProperties": False,
}

_VISUAL_CARD_SCHEMA = {
    "type": "object",
    "properties": {
        "kind": {"type": "string", "description": "step|emotion|choice|schedule|reminder"},
        "title_zh": {"type": "string"},
        "title_en": {"type": "string"},
        "caption_zh": {"type": "string"},
        "caption_en": {"type": "string"},
        "icon": {"type": "string"},
    },
    "required": ["kind", "title_zh", "title_en", "caption_zh", "caption_en", "icon"],
    "additionalProperties": False,
}

TRAINING_SCHEMA = {
    "type": "object",
    "properties": {
        "title_zh": {"type": "string"},
        "title_en": {"type": "string"},
        "learning_objective": {"type": "string", "description": "一句可观察、可测量的训练目标"},
        "intro_zh": {"type": "string"},
        "intro_en": {"type": "string"},
        "steps": {"type": "array", "items": _TEACH_STEP_SCHEMA},
        "practice_trials": {"type": "array", "items": _PRACTICE_TRIAL_SCHEMA},
        "social_choice": _SOCIAL_CHOICE_SCHEMA,
        "visual_cards": {"type": "array", "items": _VISUAL_CARD_SCHEMA},
        "review_zh": {"type": "string"},
        "review_en": {"type": "string"},
        "citations_used": {"type": "array", "items": {"type": "string"}},
        "review_flags": {"type": "array", "items": {"type": "string"}},
    },
    "required": ["title_zh", "title_en", "learning_objective", "intro_zh", "intro_en",
                 "steps", "practice_trials", "social_choice", "visual_cards",
                 "review_zh", "review_en", "citations_used", "review_flags"],
    "additionalProperties": False,
}


def build_training_system_prompt(method_id: str = "video_modeling", extra_citations=None) -> str:
    m = load_method(method_id)
    g = m.get("per_module_guidance_zh", {}) or {}
    rules = "\n".join(f"- {r}" for r in m.get("writing_rules_zh", []))
    reinforce = "\n".join(f"- {r}" for r in m.get("reinforcement_rules_zh", []))
    cite_ids = list(m.get("citations", []))
    for c in (extra_citations or []):
        if c not in cite_ids:
            cite_ids.append(c)
    cite_lines = "\n".join(f"- {cid}: {citation_text(cid)}" for cid in cite_ids)
    name_zh = m.get("name_zh", "循证方法")
    one_line = m.get("one_line_zh", "")
    comps = m.get("method_components_zh") or {}
    comp_lines = "\n".join(f"- {v}" for v in comps.values()) if isinstance(comps, dict) else ""
    method_block = f"\n\n【{name_zh} · 方法要点】\n{comp_lines}" if comp_lines else ""
    return f"""你是一名精通自闭症循证干预的专家,尤其擅长把【{name_zh}】做成"看完就能练到技能"的训练模块——用视频分步示范 + 回合式练习(提示→留白→示范→强化)+ 视觉支持来承载。{one_line}
你的产出会被特教老师/康复师使用,并可能面向自闭症儿童家庭售卖,因此必须严格循证、正向、安全:视频本身就是一次康复训练。{method_block}

【硬性设计规则】
{rules}

【正向强化规则】
{reinforce}

【模块结构】按顺序产出:
- intro 开场:**直接进入故事**——用第一人称、写实地把孩子带入这个情境本身(像故事开头就发生了什么)。严禁出现"今天我们要练习/学习""这是可以学会的"等元话语或说教口吻。
- steps 示范段:把目标技能做任务分析,拆成 {g.get('min_steps', 3)}–{g.get('max_steps', 6)} 个小步骤,一步一屏,只示范正确做法。
- practice_trials 练习段:{g.get('min_trials', 2)}–{g.get('max_trials', 4)} 个回合。每回合 = prompt 给一次尝试机会 → 留白 pause_seconds 秒(建议 {g.get('pause_seconds_default', 4)} 秒,让孩子自己做)→ answer 示范正确反应 → reinforce 针对刚才行为的具体鼓励。跨回合让提示逐步减少、情境略变以促进泛化。
- social_choice 社交选择段:一个真实、贴近孩子的社交情境 + 2–3 个选项;每个选项都给温和、写实的结果反馈,不设"错误惩罚",可自然点出更合适的做法。
- visual_cards 视觉支持:{g.get('min_cards', 3)}–{g.get('max_cards', 6)} 张可打印卡片(kind 取 step/emotion/choice/schedule/reminder),每张配简短说明与一个具体 emoji。
- review 收尾:用第一人称、故事化地收束(情境圆满解决),给孩子成就感与温暖鼓励;不要用"今天我们练习了"之类的总结说教。

【目标 learning_objective】必须是一句可观察、可测量的行为目标(谁、在什么情境、做出什么、达到什么程度)。

【语言】全中英双语:narration_zh 用于朗读,英文仅作画面字幕。用词、句长匹配孩子年龄与阅读水平;一屏一个要点。

【个性化】自然融入孩子的名字与兴趣(写实、贴切,不夸张),照顾其感官特点。

【禁止】不得出现恐吓、负面或绝对化表达;不得演示错误做法;不得做任何"治愈/疗效"承诺。

【引用】citations_used 从下列 id 中挑选本模块所依据来源(可多选):
{cite_lines}

只通过结构化输出返回 TrainingModule,不要输出多余文字。"""


def _skill_context_block(skill_ctx: dict) -> str:
    """把技能库上下文(发展序列目标 + 先决/例子/达标指标 + 层级)拼成注入用户提示的文本块。"""
    area = skill_ctx["area"]
    parts: list[str] = []
    for t in area.get("targets", []):
        parts.append(f"  · [层级 {t.get('level','')}] {t.get('zh','')}")
        if t.get("prereq_zh"):
            parts.append(f"      先决技能:{t['prereq_zh']}")
        if t.get("indicator_zh"):
            parts.append(f"      达标指标:{t['indicator_zh']}")
        exs = t.get("examples_zh") or []
        if exs:
            parts.append(f"      情境例子:{' / '.join(exs)}")
    tgt_lines = "\n".join(parts)
    lvl_defs = "、".join(
        f"{l.get('key')}={l.get('zh')}" for l in skill_ctx.get("levels", [])
    )
    return f"""

【本模块的技能定位(来自技能库 · 循证发展序列)】
- 领域:{skill_ctx.get('domain_name_zh','')}
- 技能:{area.get('name_zh','')} / {area.get('name_en','')}
- 该技能的发展目标(请依孩子当前水平,选其中 1 个作为本模块焦点;可参考其"情境例子"构建故事与练习回合,用其"达标指标"帮助写出可测量的 learning_objective):
{tgt_lines}
- 发展层级参考:{lvl_defs}
请让 learning_objective 对齐上述某个具体目标,并确保内容难度与该层级一致。"""


def build_training_user_prompt(spec: TrainingSpec, skill_ctx: dict | None = None) -> str:
    interests = "、".join(spec.interests) if spec.interests else "(未提供)"
    goal = spec.goal or "(未指定,请你据训练技能拟定一个正向、具体、可测量的目标)"
    target = spec.skill_target or (skill_ctx["area"].get("name_zh", "") if skill_ctx else "")
    prompt = f"""请为下面这个孩子设计一个「训练模块」(视频分步示范 + 练习回合 + 社交选择 + 视觉卡片),并按结构化格式返回。

- 要训练的技能 / 目标行为:{target}
- 训练目标(可测量):{goal}
- 孩子名字:{spec.child_name}
- 年龄:{spec.age} 岁
- 兴趣:{interests}
- 感官特点 / 需照顾的地方:{spec.sensory_notes or "(未提供)"}
- 阅读水平:{spec.reading_level}(simple=更简单;medium=适中)"""
    if skill_ctx:
        prompt += _skill_context_block(skill_ctx)
    prompt += """

请严格遵守系统提示中的所有循证规则:视频要能"练到东西",练习段必须有真实的"留白让孩子做"。"""
    return prompt


def resolve_skill_context(spec: TrainingSpec) -> dict | None:
    """据 spec 的 skill_domain/skill_area 从技能库取上下文;未指定技能区则返回 None。

    返回:{domain_id, domain_name_zh, area, method_id(自动选), citations, levels}。
    """
    if not spec.skill_area:
        return None
    if spec.skill_domain:
        domain_id, area = spec.skill_domain, get_skill_area(spec.skill_domain, spec.skill_area)
    else:
        domain_id, area = find_skill_area(spec.skill_area)
    if not area:
        avail = []
        for d in list_skill_domains():
            for a in load_skill_domain(d).get("skill_areas", []) or []:
                avail.append(f"{d}/{a.get('id')}")
        raise SystemExit(
            f"技能区未找到:{spec.skill_area}。可用技能区:\n  " + "\n  ".join(avail)
        )
    dom = load_skill_domain(domain_id)
    return {
        "domain_id": domain_id,
        "domain_name_zh": dom.get("name_zh", ""),
        "area": area,
        "method_id": pick_method_for_area(area),
        "citations": area.get("citations", []) or [],
        "levels": dom.get("developmental_levels", []) or [],
    }


def generate_training(spec: TrainingSpec, model: str | None = None) -> TrainingModule:
    """调用 Claude 生成结构化训练模块;可据 skill_area 从技能库取目标并自动选方法。"""
    import anthropic  # 延迟导入,--no-ai 模式无需安装/联网

    skill_ctx = resolve_skill_context(spec)
    method_id = spec.method_id or (skill_ctx["method_id"] if skill_ctx else "") or "video_modeling"
    extra_cites = skill_ctx["citations"] if skill_ctx else None

    client = anthropic.Anthropic()
    model = model or DEFAULT_MODEL
    response = client.messages.create(
        model=model,
        max_tokens=16000,
        thinking={"type": "adaptive"},
        system=build_training_system_prompt(method_id, extra_citations=extra_cites),
        messages=[{"role": "user", "content": build_training_user_prompt(spec, skill_ctx)}],
        output_config={"format": {"type": "json_schema", "schema": TRAINING_SCHEMA}},
    )
    text = next((b.text for b in response.content if b.type == "text"), None)
    if not text:
        raise RuntimeError("模型未返回结构化文本内容。")
    module = TrainingModule(**json.loads(text))
    module.method_id = method_id     # 记录实际所用方法,供校验/打包/引用使用
    return module


def sample_training() -> TrainingModule:
    """内置训练模块样例(--no-ai):同伴想玩玩具时的社交回应,用于离线验证管线。"""
    steps = [
        TeachStep(index=1, text_zh="先停一下,深呼吸。", text_en="First, pause and take a breath.",
                  narration_zh="遇到这种情况,我先停一下,深呼吸。", narration_en="First, I pause and take a breath.",
                  visual_keyword="深呼吸", icon="😌", duration_hint=6),
        TeachStep(index=2, text_zh="看看小朋友,听他说什么。", text_en="Look at my friend and listen.",
                  narration_zh="我看看小朋友,听他想说什么。", narration_en="I look at my friend and listen to what they say.",
                  visual_keyword="倾听", icon="👀", duration_hint=6),
        TeachStep(index=3, text_zh="我可以说“我们一起玩”或“等我一下”。", text_en="I can say 'Let's play together' or 'Wait a moment.'",
                  narration_zh="我可以说,我们一起玩;或者说,等我一下。", narration_en="I can say, let's play together, or, wait a moment.",
                  visual_keyword="说出来", icon="🗣️", duration_hint=7),
        TeachStep(index=4, text_zh="用平和的声音说出来。", text_en="I say it in a calm voice.",
                  narration_zh="我用平和的声音,把它说出来。", narration_en="I say it in a calm, gentle voice.",
                  visual_keyword="平和", icon="🙂", duration_hint=6),
    ]
    trials = [
        PracticeTrial(index=1,
                      prompt_zh="小明走过来说:“我可以玩这个小汽车吗?”轮到你,试着说说看。",
                      prompt_en="A friend asks: 'Can I play with this car?' Your turn — give it a try.",
                      pause_seconds=4,
                      answer_zh="我们可以一起玩!", answer_en="We can play together!",
                      reinforce_zh="你用平和的声音说出来了,做得很好。",
                      reinforce_en="You said it in a calm voice. Well done.", icon="🌟"),
        PracticeTrial(index=2,
                      prompt_zh="你还在拼恐龙,朋友想现在就玩。你可以怎么说?",
                      prompt_en="You are still building your dinosaur and a friend wants it now. What can you say?",
                      pause_seconds=4,
                      answer_zh="等我一下,我拼完这块就给你。", answer_en="Wait a moment, I'll give it to you after this piece.",
                      reinforce_zh="你说了“等我一下”,这样朋友就明白了,真棒。",
                      reinforce_en="You said 'wait a moment', so your friend understands. Great job.", icon="🌟"),
        PracticeTrial(index=3,
                      prompt_zh="如果你还想再玩一会儿,又不想让朋友难过,你会怎么说?",
                      prompt_en="If you want to play a bit longer but don't want your friend to feel sad, what could you say?",
                      pause_seconds=5,
                      answer_zh="我再玩两分钟,然后换你,好吗?", answer_en="I'll play two more minutes, then it's your turn, okay?",
                      reinforce_zh="你想到了一个大家都开心的办法,很了不起。",
                      reinforce_en="You found a way that makes everyone happy. That's wonderful.", icon="🌟"),
    ]
    social = SocialChoiceScenario(
        scenario_zh="小朋友想玩你手里的玩具……你可以怎么做?",
        scenario_en="A friend wants the toy in your hands... what can you do?",
        icon="🤝",
        options=[
            ChoiceOption(label_zh="一起玩", label_en="Play together",
                         outcome_zh="你们一起玩,很快成了好朋友。", outcome_en="You play together and soon become good friends.", icon="😊"),
            ChoiceOption(label_zh="说“等我一下”", label_en="Say 'wait a moment'",
                         outcome_zh="小朋友点点头愿意等你,你也玩得很安心。", outcome_en="Your friend nods and waits, and you feel at ease.", icon="👍"),
        ],
    )
    cards = [
        VisualCard(kind="step", title_zh="我可以说的话", title_en="What I can say",
                   caption_zh="“我们一起玩” / “等我一下”", caption_en="'Let's play together' / 'Wait a moment'", icon="🗣️"),
        VisualCard(kind="schedule", title_zh="遇到这种情况的四步", title_en="Four steps",
                   caption_zh="停 → 看 → 说 → 平和地说出来", caption_en="Pause → Look → Say → Say it calmly", icon="🪜"),
        VisualCard(kind="emotion", title_zh="朋友的心情", title_en="My friend's feeling",
                   caption_zh="一起玩,大家都开心。", caption_en="Playing together makes everyone happy.", icon="😊"),
        VisualCard(kind="reminder", title_zh="我做得到", title_en="I can do it",
                   caption_zh="我可以用平和的话回应。", caption_en="I can respond with calm words.", icon="🌟"),
    ]
    return TrainingModule(
        title_zh="当同伴想玩我的玩具时",
        title_en="When a Friend Wants My Toy",
        learning_objective="当同伴想玩孩子正在玩的玩具时,孩子能用平和的话回应(如“我们一起玩”或“等我一下”),而不是抢夺或哭闹。",
        method_id="video_modeling",
        intro_zh="我正在玩我最喜欢的小汽车,玩得很开心。这时,一个小朋友走过来,看着我手里的玩具。",
        intro_en="I'm happily playing with my favorite car. Just then, a friend comes over and looks at the toy in my hands.",
        steps=steps,
        practice_trials=trials,
        social_choice=social,
        visual_cards=cards,
        review_zh="小朋友笑了,我们一起开开心心地玩。我用平和的话和朋友相处,做得很好。",
        review_en="My friend smiles, and we play together happily. I got along with my friend using calm words — I did great.",
        citations_used=["bellini_akullian_2007", "charlop_christy_2000", "wong_2015", "nac_2015"],
        review_flags=["内置样例,仅用于管线演示;正式使用前需专业人员按孩子情况与真实同伴互动调整。"],
    )
