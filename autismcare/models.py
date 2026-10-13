"""数据模型与 schema 校验(pydantic v2)。

- StorySpec  : 用户输入(目标场景 + 孩子画像)
- Scene      : 一屏 = 一句社交故事(带句型标注 + 双语 + 旁白 + 画面关键词)
- StoryScript: Claude 结构化产出(整篇故事)
这些模型同时用来生成给 Claude 的工具 JSON Schema(见 generate.py)。
"""

from __future__ import annotations

import re
from enum import Enum
from pathlib import Path

from pydantic import BaseModel, Field


class SentenceType(str, Enum):
    """Carol Gray 社交故事的四种句型。"""

    descriptive = "descriptive"   # 描述句
    perspective = "perspective"   # 观点句
    affirmative = "affirmative"   # 肯定句
    directive = "directive"       # 指导句


class StorySpec(BaseModel):
    """一份社交故事的输入规格(来自 config/*.yaml)。"""

    situation: str = Field(..., description="目标场景 / 要学习的情境,如'第一次去看牙医'")
    child_name: str = Field("小朋友", description="孩子的名字")
    age: int = Field(6, ge=2, le=18, description="孩子年龄")
    goal: str = Field("", description="这份故事希望达到的学习目标(可留空由 AI 推断)")
    interests: list[str] = Field(default_factory=list, description="孩子的兴趣,用于个性化")
    sensory_notes: str = Field("", description="感官特点 / 需要照顾的地方")
    reading_level: str = Field("simple", description="simple 简单 | medium 适中")
    project_slug: str = Field("", description="输出文件夹名;留空则自动生成")

    def resolved_slug(self) -> str:
        if self.project_slug:
            return _slugify(self.project_slug)
        return _slugify(self.situation) or "story"


class Scene(BaseModel):
    """一屏(社交故事的一页 / 视频的一个场景)。"""

    index: int = Field(..., description="从 1 开始的场景序号")
    sentence_type: SentenceType = Field(..., description="该句的句型")
    text_zh: str = Field(..., description="屏幕上显示的中文句子(1-2 句,简短)")
    text_en: str = Field(..., description="对应的英文句子")
    narration_zh: str = Field(..., description="中文旁白稿(通常与 text_zh 一致或略口语)")
    narration_en: str = Field(..., description="英文旁白稿")
    visual_keyword: str = Field(..., description="画面主体的简短关键词,如'牙医椅'")
    icon: str = Field("🧩", description="代表该场景的单个 emoji(简洁、具体、正向)")
    duration_hint: float = Field(6.0, description="建议停留秒数(实际以配音时长为准)")


class StoryScript(BaseModel):
    """整篇社交故事(Claude 结构化产出)。"""

    title_zh: str
    title_en: str
    learning_goal: str = Field("", description="用一句话说明这份故事帮助孩子学会什么")
    method_id: str = Field("social_stories", description="所依据的循证方法 id")
    scenes: list[Scene]
    citations_used: list[str] = Field(default_factory=list, description="用到的引用 id")
    review_flags: list[str] = Field(default_factory=list, description="生成侧自评的注意点")


# =========================================================================
# 训练模块(Training Module)—— 「视频即康复训练」内容类型
# 依据:视频示范(Video Modeling)+ 回合式练习(提示→留白→示范→强化)
#       + 视觉支持图片 + 社交情境选择。见 knowledge/methods/video_modeling.yaml。
# =========================================================================

class TrainingSpec(BaseModel):
    """一个训练模块的输入规格(来自 config/*.yaml 或 CLI)。"""

    skill_target: str = Field("", description="要训练的具体、可观察的目标行为/技能;可留空并改用 skill_domain+skill_area 从技能库取")
    skill_domain: str = Field("", description="技能领域库 id(如 emotional_regulation / social_interaction)")
    skill_area: str = Field("", description="该领域下的技能区 id(如 regulation_strategies);据此取发展序列并自动挑方法")
    child_name: str = Field("小朋友", description="孩子的名字")
    age: int = Field(6, ge=2, le=18, description="孩子年龄")
    goal: str = Field("", description="可测量的训练目标(可留空由 AI 拟定)")
    interests: list[str] = Field(default_factory=list, description="孩子的兴趣,用于个性化情境")
    sensory_notes: str = Field("", description="感官特点 / 需照顾的地方")
    reading_level: str = Field("simple", description="simple 简单 | medium 适中")
    method_id: str = Field("", description="循证方法 id;留空则按 skill_area 自动选,再退回 video_modeling")
    project_slug: str = Field("", description="输出文件夹名;留空则自动生成")

    def resolved_slug(self) -> str:
        if self.project_slug:
            return _slugify(self.project_slug)
        return _slugify(self.skill_target or self.skill_area) or "training"


class TeachStep(BaseModel):
    """示范段的一步(Video Modeling:分步示范目标技能,只示范正确做法)。"""

    index: int = Field(..., description="从 1 开始的步骤序号")
    text_zh: str = Field(..., description="屏幕上显示的中文(简短,一步一个要点)")
    text_en: str = Field(..., description="对应英文")
    narration_zh: str = Field(..., description="中文旁白稿")
    narration_en: str = Field(..., description="英文旁白稿(仅作字幕,不朗读)")
    visual_keyword: str = Field(..., description="画面主体的简短关键词")
    icon: str = Field("✅", description="代表该步骤的单个 emoji(简洁、具体、正向)")
    duration_hint: float = Field(6.0, description="建议停留秒数")


class PracticeTrial(BaseModel):
    """一个练习回合:提示 → 留白(轮到你)→ 示范正确反应 → 鼓励强化。"""

    index: int = Field(..., description="从 1 开始的回合序号")
    prompt_zh: str = Field(..., description="给孩子的提示/提问(引出一次尝试),中文")
    prompt_en: str = Field(..., description="提示的英文")
    pause_seconds: float = Field(4.0, ge=2.0, le=10.0, description="留给孩子作答的静默秒数")
    answer_zh: str = Field(..., description="示范的正确反应,中文")
    answer_en: str = Field(..., description="示范正确反应的英文")
    reinforce_zh: str = Field(..., description="具体、正向、针对刚才行为的鼓励,中文")
    reinforce_en: str = Field(..., description="鼓励的英文")
    icon: str = Field("🌟", description="该回合的单个 emoji")


class ChoiceOption(BaseModel):
    """社交情境里的一个选择及其温和结果(无惩罚)。"""

    label_zh: str = Field(..., description="选项(孩子可能的做法),中文")
    label_en: str = Field(..., description="选项英文")
    outcome_zh: str = Field(..., description="这个选择带来的温和、写实的结果反馈,中文")
    outcome_en: str = Field(..., description="结果反馈英文")
    icon: str = Field("🙂", description="该选项的单个 emoji")


class SocialChoiceScenario(BaseModel):
    """社交情境·选择分支:给情境,每个选择都有温和反馈。"""

    scenario_zh: str = Field(..., description="社交情境描述,中文")
    scenario_en: str = Field(..., description="情境英文")
    options: list[ChoiceOption] = Field(..., description="2-3 个选项,均为正向、无惩罚")
    icon: str = Field("🤝", description="情境的单个 emoji")


class VisualCard(BaseModel):
    """配套视觉支持图片(可打印):步骤卡 / 情绪卡 / 选择卡 / 流程卡。"""

    kind: str = Field("step", description="step 步骤 | emotion 情绪 | choice 选择 | schedule 流程 | reminder 提醒")
    title_zh: str = Field(..., description="卡片标题,中文")
    title_en: str = Field(..., description="卡片标题英文")
    caption_zh: str = Field("", description="卡片说明,中文(可空)")
    caption_en: str = Field("", description="卡片说明英文(可空)")
    icon: str = Field("🧩", description="卡片主图 emoji")


class PageVisual(BaseModel):
    """单页画面覆盖:让某一页的插画忠实于该页文字所描述的场景与出场角色。

    执行标准(2026‑07‑15 起):插画必须**贴合该页文字的具体场景**,而非笼统地
    "主角+全阵容站在场景里"。当自动描述会偏离文字时(如"看墙上的步骤图"应画出
    贴着步骤图的墙+男孩仰头看;"看旁边的小朋友"应出现两个孩子、主角在看另一个孩子),
    就在模块的 page_visuals 里按页名给出精确的 visual_en 与 roles。
    """

    visual_en: str = Field("", description="覆盖该页画面英文描述(留空=用管线默认)")
    roles: list[str] | None = Field(
        None, description="覆盖该页出现的固定角色键列表(见 cast.CHARACTERS):"
        "None=用该课阵容默认;[]=不注入固定角色(纯场景);"
        "如 ['boy_ming'] 单人、['boy_ming','peer_child'] 主角+一个同伴、['boy_ming','teacher']。")
    seed: int | None = Field(
        None, description="覆盖该页出图 seed(默认全局 4242)。当某页被 Flux 画出畸形"
        "(如异常的眼睛/多余的手/脸部瑕疵)时,固定 seed 会复现同一张坏图;"
        "换个 seed 重掷、挑一张干净的填在这里,即可只修这一页而不动别页。")


class TrainingModule(BaseModel):
    """一个完整训练模块(Claude 结构化产出)。"""

    title_zh: str
    title_en: str
    learning_objective: str = Field(..., description="一句可观察、可测量的训练目标")
    method_id: str = Field("video_modeling", description="所依据的循证方法 id")
    intro_zh: str = Field(..., description="开场:今天我们要练习什么(温和、具体),中文")
    intro_en: str = Field(..., description="开场英文")
    steps: list[TeachStep] = Field(..., description="示范段:分步示范目标技能")
    practice_trials: list[PracticeTrial] = Field(..., description="练习段:数个练习回合")
    social_choice: SocialChoiceScenario | None = Field(None, description="社交情境选择段(可选)")
    visual_cards: list[VisualCard] = Field(default_factory=list, description="配套可打印图片")
    review_zh: str = Field(..., description="收尾:回顾+鼓励,中文")
    review_en: str = Field(..., description="收尾英文")
    citations_used: list[str] = Field(default_factory=list, description="用到的引用 id")
    review_flags: list[str] = Field(default_factory=list, description="生成侧自评的注意点")
    cast: str = Field("peer_play", description="视觉角色阵容 id(见 cast.py):"
                      "peer_play 同伴社交 | solo_child 单人题材 | none 不注入固定角色。"
                      "决定插画里自动复现的固定角色,保证跨页/跨视频画面一致。")
    page_visuals: dict[str, PageVisual] = Field(
        default_factory=dict,
        description="按页名覆盖画面/角色,让插画忠实于该页文字(见 PageVisual)。"
        "键=页名:title/intro/step1..N/trial{i}_prompt/trial{i}_answer/trial{i}_reinforce/"
        "choice/choice_A..N/review。仅需覆盖的页写进来即可,其余用默认。")


def _slugify(text: str) -> str:
    """把任意标题转成安全的文件夹名(保留中文,替换空白/符号为下划线)。"""
    text = text.strip()
    text = re.sub(r"[\\/:*?\"<>|]+", "", text)      # 去掉文件名非法字符
    text = re.sub(r"\s+", "_", text)
    return text[:40]


def ensure_dir(path: Path) -> Path:
    path.mkdir(parents=True, exist_ok=True)
    return path
