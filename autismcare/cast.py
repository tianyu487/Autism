"""视觉角色库(Character Bible 的代码化)。

把 design/visual_style_bible.md §3–§4 的**固定角色关键词块**与**场景锚点**沉淀成
可复用数据,供 pipeline 在生成每页插画时自动注入——让同一角色跨页、跨视频尽量复现。
风格与一致性的另外两根支柱在 illustrate.py:统一 STYLE 串 + 固定 seed 4242。

设计要点:
  · 角色/场景块**逐字**取自手册,每次原样复用(改措辞会让脸漂移);
  · 每个"阵容(cast)"声明:primary(每页都出现的主角)、others(互动页追加的角色)、
    scene(该系列的场景锚点);不同题材用不同阵容,避免把"同伴"错注进单人题材。
  · 新增角色 / 新阵容只改本文件,pipeline 无需改动。

诚实局限:Flux + 固定 seed 只能锁"画风/氛围",不能逐帧锁定同一张脸;本模块把一致性
做到"足够好",严格复现需升级到角色参考图 / LoRA / img2img 后端(见手册 §7)。
"""

from __future__ import annotations

# ── 角色关键词块(style bible §3;每次原样复用以最大化复现)────────────────
# 眼睛执行标准(2026‑07‑15):所有角色**睁眼**时都要有清晰的黑色瞳孔 + 可见眼白,
# 符合正常人物外貌(闭眼/眯眼仅在明确需要时由 page_visuals 覆盖)。此描述串写进每个
# 角色块,并由 illustrate.STYLE 再全局强调一遍,双保险防止 Flux 画出无神/异常的眼睛。
EYES = "clear well-defined open eyes with round dark-black pupils and visible white sclera, natural friendly gaze"

CHARACTERS: dict[str, str] = {
    # 主角男孩 · 小明("我")
    "boy_ming": (
        "a gentle young preschool boy, short soft chestnut-brown hair with side-swept bangs, "
        f"round face, rosy pink cheeks, small nose, warm ivory skin, gentle warm smile, {EYES}, "
        "soft cream short-sleeve t-shirt"
    ),
    # 同伴女孩
    "girl_friend": (
        "a friendly young preschool girl, warm brown hair in a low side ponytail with side bangs, "
        f"round face, rosy cheeks, gentle small smile, warm light skin, {EYES}, "
        "light sage-green striped short-sleeve t-shirt"
    ),
    # 同伴小朋友(通用同学/玩伴;与小明、同伴女孩外观区分开)
    "peer_child": (
        "another young preschool child classmate, neat short dark-brown hair, "
        f"round face, rosy cheeks, warm light skin, gentle friendly smile, {EYES}, "
        "a simple soft pale-blue short-sleeve t-shirt"
    ),
    # 医生(温和、不吓人;绘本风的大人)
    "doctor": (
        "a kind gentle young female doctor, warm friendly reassuring smile, neat dark hair in a low bun, "
        f"{EYES}, wearing a soft light-blue medical coat with a stethoscope, approachable and calm"
    ),
    # 老师
    "teacher": (
        "a warm friendly young female teacher, gentle kind smile, shoulder-length soft brown hair, "
        f"{EYES}, wearing a cozy soft cardigan, approachable and calm"
    ),
}

# ── 场景锚点(style bible §4;每个阵容配一个,支撑跨课"换场景")──────────────
SCENE_PLAYROOM = (
    "cozy warm indoor playroom, large window with sheer white curtains, soft golden backlight, "
    "small potted plants and soft foliage in the corners, plain warm cream background, calm quiet mood"
)
SCENE_CALM = (
    "a cozy quiet calm-down corner at home, soft cushions and a beanbag, a small plant, "
    "gentle warm soothing light, plain soft pastel wall, very calm and comforting mood"
)
SCENE_PLAYGROUND = (
    "a sunny outdoor playground with soft green grass, a slide and swings softly blurred in the background, "
    "gentle warm daylight, a few soft trees, cheerful calm mood"
)
SCENE_CLINIC = (
    "a friendly children's clinic exam room, soft pastel walls, a tidy exam table, a small growth chart, "
    "gentle warm reassuring light, calm and cozy, warm and not scary"
)
SCENE_CLASSROOM = (
    "a warm cozy preschool classroom, low wooden tables and a soft rug, picture cards on the wall, "
    "gentle daylight through a window, calm orderly and friendly mood"
)
SCENE_BATHROOM = (
    "a clean bright child-friendly bathroom, a low sink with a soap pump, soft folded towels, a small stool, "
    "gentle warm light, tidy fresh and calm mood"
)

# ── 命名阵容:primary 每页出现;others 互动页追加;scene 该系列场景锚点 ──────
CASTS: dict[str, dict] = {
    # 同伴社交题材(如"同伴想玩我的玩具"):主角男孩 + 同伴女孩
    "peer_play":  {"primary": "boy_ming", "others": ["girl_friend"], "scene": SCENE_PLAYROOM},
    # 单人题材(如自理/情绪自我调节):只有主角男孩
    "solo_child": {"primary": "boy_ming", "others": [],              "scene": SCENE_PLAYROOM},
    # 不注入固定角色(题材角色差异大时,只保留风格串,场景另配)
    "none":       {"primary": None,       "others": [],              "scene": None},
    # ↓ 批量"换场景+按题材换角色"专用阵容(主角始终小明,保系列连续)————————
    # 情绪自我调节·单人·居家安静角
    "solo_calm":        {"primary": "boy_ming", "others": [],            "scene": SCENE_CALM},
    # 同伴社交·两娃·户外游乐场
    "park_peers":       {"primary": "boy_ming", "others": ["girl_friend"], "scene": SCENE_PLAYGROUND},
    # 就医·小明+医生·诊室
    "clinic_visit":     {"primary": "boy_ming", "others": ["doctor"],    "scene": SCENE_CLINIC},
    # 课堂·小明+老师·教室
    "classroom_teacher": {"primary": "boy_ming", "others": ["teacher"],  "scene": SCENE_CLASSROOM},
    # 自理·单人·浴室
    "solo_bathroom":    {"primary": "boy_ming", "others": [],            "scene": SCENE_BATHROOM},
}

DEFAULT_CAST = "peer_play"


def resolve(name: str | None) -> dict:
    """取阵容配置;未知/空 → 回退默认阵容。"""
    return CASTS.get(name or DEFAULT_CAST, CASTS[DEFAULT_CAST])


def has_others(cast_name: str | None) -> bool:
    """该阵容在互动页是否会追加第二个角色(≥1 个 others)。

    供 pipeline 判断题材是单人还是双人,从而给每页选对画面描述:
    单人题材(自理/情绪自我调节)不应出现"和朋友一起/分享玩具"之类措辞,
    否则 Flux 会据此画出第二个孩子(见 style bible §7 主体复制)。
    """
    return bool(resolve(cast_name).get("others"))


# 单人页"只有一个孩子"强调:Flux 对单主体 prompt 偶发把主角复制成两个,
# 明确"画面中只有一个孩子"可从根源抑制这种重复(见 style bible §7)。
_SOLO_HINT = "only one single child alone in the scene, no other people"


def anchor_blocks(cast_name: str | None, *, with_others: bool = True,
                  scene: bool = True) -> str | None:
    """拼出要追加到画面描述后的"角色块 + 场景锚点"字符串(不含 STYLE,STYLE 由 illustrate 追加)。

    with_others=False → 只注入主角(单人特写/鼓励页);True → 注入整个阵容(互动页)。
    当最终只有一个角色出场时,追加"只有一个孩子"提示,抑制 Flux 主体复制。
    返回 None 表示无锚点可加(如 none 阵容且 scene=False),调用方按原样出图。
    """
    conf = resolve(cast_name)
    roles: list[str] = []
    if conf.get("primary"):
        roles.append(conf["primary"])
    if with_others:
        roles += conf.get("others", [])
    parts = [CHARACTERS[r] for r in roles if r in CHARACTERS]
    if len(parts) == 1:                       # 恰好一个角色 → 强调单人,防止复制
        parts.append(_SOLO_HINT)
    if scene and conf.get("scene"):
        parts.append(conf["scene"])
    return ", ".join(parts) if parts else None


def scene_of(cast_name: str | None) -> str | None:
    """取该阵容的场景锚点(供 page_visuals 覆盖角色时仍保留同一场景)。"""
    return resolve(cast_name).get("scene")


def anchor_from_roles(roles: list[str] | None, *, scene: str | None = None) -> str | None:
    """按**显式角色键列表**拼锚点(供 page_visuals 逐页指定出场角色)。

    roles=[] → 只保留场景(纯场景页,如"贴满步骤图的墙");
    恰好一个角色 → 追加单人提示防止复制;scene 传该课场景锚点以保持场景一致。
    """
    roles = roles or []
    parts = [CHARACTERS[r] for r in roles if r in CHARACTERS]
    if len(parts) == 1:
        parts.append(_SOLO_HINT)
    if scene:
        parts.append(scene)
    return ", ".join(parts) if parts else None


# ══════════════════════════════════════════════════════════════════════════
# 角色素材库(表情 / 动作 / 服装的可变部分)—— 供生成"角色素材图"用。
#
# 上面的 CHARACTERS 把"身份+固定微笑+默认服装"打包成一块,保证**同一节课内**
# 画面一致(pipeline 依赖,勿动)。下面把身份/服装/表情**拆开**,以便按需组合出
# 同一角色的**不同表情、不同动作、不同衣着**——用于情绪卡、角色立绘、跨课换装等。
# 身份关键词与 CHARACTERS 的身份部分一致 → 仍是同两个娃,只是可变表情/服装。
# ══════════════════════════════════════════════════════════════════════════

# 身份(不含表情/服装)——素材库在其上叠加表情+服装。
IDENTITY: dict[str, str] = {
    "boy_ming": ("a young preschool boy, short soft chestnut-brown hair with side-swept bangs, "
                 "round face, rosy pink cheeks, small nose, warm ivory skin"),
    "girl_friend": ("a young preschool girl, warm brown hair in a low side ponytail with side bangs, "
                    "round face, rosy cheeks, warm light skin"),
}

# 可替换服装(全部柔和低刺激配色);default 与 CHARACTERS 的默认装一致。
OUTFITS: dict[str, dict[str, str]] = {
    "boy_ming": {
        "default":  "a soft cream short-sleeve t-shirt",
        "stripe":   "a light blue and white striped t-shirt",
        "hoodie":   "a cozy soft mustard-yellow hoodie",
        "overalls": "denim overalls over a white t-shirt",
    },
    "girl_friend": {
        "default":  "a light sage-green striped short-sleeve t-shirt",
        "dress":    "a soft peach sundress",
        "cardigan": "a warm cream cardigan over a light dress",
        "overalls": "pink corduroy overalls over a cream t-shirt",
    },
}

# 表情 + 轻动作(纯视觉,无台词;避免触发画面文字)。可作情绪卡的一套基础表情。
EXPRESSIONS: dict[str, str] = {
    "happy":     "a big happy smile, bright cheerful eyes, waving hello",
    "calm":      "a calm gentle expression, relaxed and content",
    "sad":       "a sad expression, inner eyebrows raised up, a downturned mouth, eyes looking down, a little teary but calm and gentle",
    "surprised": "a surprised expression, wide round eyes and open mouth, hands raised",
    "thinking":  "a thoughtful curious expression, one hand on the chin, looking up",
    "proud":     "a proud confident expression, hands on hips, chin up, a small smile",
    "shy":       "a shy bashful expression, a gentle smile, hands near the cheeks",
    "excited":   "an excited joyful expression, soft warm gentle eyes, a big open smile, clapping both hands together happily",
}

# 同框互动(动作多样;纯视觉,无台词)。
TOGETHER_ACTIONS: dict[str, str] = {
    "wave":    "smiling and waving hello to each other",
    "play":    "happily playing together with a small toy",
    "comfort": "sitting side by side, one gently comforting the other with a hand on the shoulder",
    "share":   "taking turns with a small toy train, both looking content",
    "think":   "both looking curious and thinking together",
    "laugh":   "laughing together joyfully",
}

_PORTRAIT_BG = "centered, simple soft neutral pastel background, gentle even lighting"
_TOGETHER_BG = "centered, simple soft warm pastel background, gentle lighting"


def portrait_prompt(char: str, expression: str = "calm", outfit: str = "default",
                    *, full_body: bool = False) -> str:
    """一张角色素材图的画面描述(纯视觉,STYLE 由 illustrate 追加)。"""
    ident = IDENTITY[char]
    clo = OUTFITS[char].get(outfit, OUTFITS[char]["default"])
    expr = EXPRESSIONS.get(expression, EXPRESSIONS["calm"])
    frame = "full body" if full_body else "upper body portrait"
    return f"{frame} of {ident}, wearing {clo}, {expr}, {_PORTRAIT_BG}"


def together_prompt(action: str = "play", boy_outfit: str = "default",
                    girl_outfit: str = "default") -> str:
    """两个角色同框的素材图描述(纯视觉)。action 取 TOGETHER_ACTIONS 的 key 或自定义短语。"""
    act = TOGETHER_ACTIONS.get(action, action)
    b = f"{IDENTITY['boy_ming']}, wearing {OUTFITS['boy_ming'].get(boy_outfit, OUTFITS['boy_ming']['default'])}"
    g = f"{IDENTITY['girl_friend']}, wearing {OUTFITS['girl_friend'].get(girl_outfit, OUTFITS['girl_friend']['default'])}"
    return f"two young children together, one is {b}, the other is {g}, {act}, {_TOGETHER_BG}"
