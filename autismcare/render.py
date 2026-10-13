"""画面层:用 Pillow 渲染低刺激、感官友好的中英双语幻灯 PNG。

设计原则(循证:自闭症视觉支持宜简洁、低刺激、一致、具体):
- 柔和低对比背景 + 清晰大字;
- 布局每屏一致、可预期;
- 一个简单具体的图标(emoji)代表画面主体;
- 右上角进度指示(1 / 7),增强可预期性;
- 底部固定标注“示范·需专业审核 / Draft·needs review”。
"""

from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

from .models import Scene, StoryScript

# ---- 画布与配色(柔和、低刺激)----
W, H = 1280, 720
BG = (245, 241, 233)          # 暖米白
ACCENT = (127, 160, 152)      # 柔和鼠尾草绿
TEXT_ZH = (51, 58, 64)        # 深灰,阅读友好
TEXT_EN = (108, 118, 116)     # 更柔和的灰绿
FOOTER = (168, 164, 156)      # 低调页脚

# ---- 字体候选路径(Windows 系统字体兜底;推荐额外安装 Noto Sans SC)----
_CJK_FONTS = [
    "C:/Windows/Fonts/msyh.ttc",       # 微软雅黑
    "C:/Windows/Fonts/msyhl.ttc",
    "assets/fonts/NotoSansSC-Regular.otf",
    "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
]
_CJK_BOLD = [
    "C:/Windows/Fonts/msyhbd.ttc",
    "C:/Windows/Fonts/msyh.ttc",
]
_EMOJI_FONTS = [
    "C:/Windows/Fonts/seguiemj.ttf",   # Segoe UI Emoji(彩色)
]


def _first_existing(paths: list[str]) -> str | None:
    for p in paths:
        if Path(p).exists():
            return p
    return None


def _load_font(candidates: list[str], size: int) -> ImageFont.FreeTypeFont:
    path = _first_existing(candidates)
    if path is None:
        # 实在找不到就用 Pillow 默认字体(不含中文,仅兜底避免崩溃)
        return ImageFont.load_default()
    return ImageFont.truetype(path, size)


def _emoji_font(size: int) -> ImageFont.FreeTypeFont | None:
    path = _first_existing(_EMOJI_FONTS)
    if path is None:
        return None
    try:
        return ImageFont.truetype(path, size)
    except OSError:
        return None


# 行首禁则(避头):这些标点不应出现在一行的开头,应回退到上一行末尾。
_LEADING_FORBIDDEN = set("、。,.!?;:)]}】》」』’”%）!?;:,")


def _fix_leading_punct(lines: list[str]) -> list[str]:
    """把落在行首的中文标点回收到上一行末尾(中文排版避头规则)。"""
    for i in range(1, len(lines)):
        while lines[i] and lines[i][0] in _LEADING_FORBIDDEN:
            lines[i - 1] += lines[i][0]
            lines[i] = lines[i][1:]
    return [ln for ln in lines if ln != ""]


def wrap_text(draw: ImageDraw.ImageDraw, text: str, font: ImageFont.FreeTypeFont,
              max_width: int) -> list[str]:
    """贪心换行:优先按空格断词;过长的连续串(如中文)再按字符断;最后做避头处理。"""
    lines: list[str] = []
    for paragraph in text.split("\n"):
        cur = ""
        for word in paragraph.split(" "):
            candidate = word if not cur else cur + " " + word
            if draw.textlength(candidate, font=font) <= max_width:
                cur = candidate
                continue
            if cur:
                lines.append(cur)
                cur = ""
            if draw.textlength(word, font=font) <= max_width:
                cur = word
            else:  # 单词/中文串本身超宽 → 按字符断
                chunk = ""
                for ch in word:
                    if draw.textlength(chunk + ch, font=font) <= max_width:
                        chunk += ch
                    else:
                        lines.append(chunk)
                        chunk = ch
                cur = chunk
        lines.append(cur)
    return _fix_leading_punct(lines)


def _draw_centered_block(draw, lines, font, fill, top, line_gap=1.35) -> int:
    """居中绘制多行文本,返回结束的 y 坐标。"""
    line_h = int(font.size * line_gap)
    y = top
    for line in lines:
        w = draw.textlength(line, font=font)
        draw.text(((W - w) / 2, y), line, font=font, fill=fill)
        y += line_h
    return y


def _draw_emoji(img: ImageDraw.ImageDraw, base: Image.Image, emoji: str, cy: int, size: int) -> None:
    """在水平居中位置绘制彩色 emoji;失败则画一个柔和的圆形占位。"""
    font = _emoji_font(size)
    if font is not None and emoji:
        try:
            bbox = img.textbbox((0, 0), emoji, font=font, embedded_color=True)
            w = bbox[2] - bbox[0]
            x = (W - w) / 2 - bbox[0]
            img.text((x, cy - bbox[1]), emoji, font=font, embedded_color=True)
            return
        except Exception:
            pass
    # 占位:柔和圆形
    r = size // 2
    img.ellipse([(W // 2 - r, cy), (W // 2 + r, cy + 2 * r)], fill=ACCENT)


def _base_slide() -> tuple[Image.Image, ImageDraw.ImageDraw]:
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    # 顶部细色条,统一的视觉锚点
    d.rectangle([(0, 0), (W, 8)], fill=ACCENT)
    return img, d


def _draw_footer(d: ImageDraw.ImageDraw) -> None:
    font = _load_font(_CJK_FONTS, 22)
    text = "示范 · 需专业审核  |  Draft · needs professional review"
    w = d.textlength(text, font=font)
    d.text(((W - w) / 2, H - 46), text, font=font, fill=FOOTER)


def _draw_progress(d: ImageDraw.ImageDraw, index: int, total: int) -> None:
    font = _load_font(_CJK_FONTS, 26)
    text = f"{index} / {total}"
    w = d.textlength(text, font=font)
    d.text((W - w - 40, 30), text, font=font, fill=ACCENT)


def render_title(script: StoryScript, out_path: Path) -> Path:
    img, d = _base_slide()
    _draw_emoji(d, d, script.scenes[0].icon if script.scenes else "🧩", cy=150, size=170)
    zh_font = _load_font(_CJK_BOLD, 60)
    en_font = _load_font(_CJK_FONTS, 34)
    tag_font = _load_font(_CJK_FONTS, 26)

    # 小标签:社交故事
    tag = "社交故事 · Social Story"
    tw = d.textlength(tag, font=tag_font)
    d.text(((W - tw) / 2, 360), tag, font=tag_font, fill=ACCENT)

    zh_lines = wrap_text(d, script.title_zh, zh_font, W - 200)
    y = _draw_centered_block(d, zh_lines, zh_font, TEXT_ZH, top=410)
    en_lines = wrap_text(d, script.title_en, en_font, W - 200)
    _draw_centered_block(d, en_lines, en_font, TEXT_EN, top=y + 10)

    _draw_footer(d)
    out_path = Path(out_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    img.save(out_path)
    return out_path


def render_scene(scene: Scene, total: int, out_path: Path) -> Path:
    img, d = _base_slide()
    _draw_progress(d, scene.index, total)
    _draw_emoji(d, d, scene.icon, cy=90, size=180)

    zh_font = _load_font(_CJK_FONTS, 52)
    en_font = _load_font(_CJK_FONTS, 30)

    zh_lines = wrap_text(d, scene.text_zh, zh_font, W - 220)
    y = _draw_centered_block(d, zh_lines, zh_font, TEXT_ZH, top=340)
    en_lines = wrap_text(d, scene.text_en, en_font, W - 220)
    _draw_centered_block(d, en_lines, en_font, TEXT_EN, top=y + 16)

    _draw_footer(d)
    out_path = Path(out_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    img.save(out_path)
    return out_path


def render_closing(out_path: Path,
                   zh="这个故事到这里就结束啦。你做得很好!",
                   en="This is the end of the story. You did great!") -> Path:
    img, d = _base_slide()
    _draw_emoji(d, d, "🌈", cy=140, size=170)
    zh_font = _load_font(_CJK_FONTS, 46)
    en_font = _load_font(_CJK_FONTS, 28)
    small = _load_font(_CJK_FONTS, 22)

    zh_lines = wrap_text(d, zh, zh_font, W - 240)
    y = _draw_centered_block(d, zh_lines, zh_font, TEXT_ZH, top=360)
    en_lines = wrap_text(d, en, en_font, W - 240)
    y = _draw_centered_block(d, en_lines, en_font, TEXT_EN, top=y + 14)

    note = "本内容为辅助/教育工具,不替代专业诊疗。"
    nw = d.textlength(note, font=small)
    d.text(((W - nw) / 2, y + 20), note, font=small, fill=FOOTER)

    _draw_footer(d)
    out_path = Path(out_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    img.save(out_path)
    return out_path


# =====================================================================
# 训练模块渲染:示范 / 练习(轮到你留白)/ 社交选择 / 收尾 幻灯 + 可打印卡片
# =====================================================================
_CARD_KIND_ZH = {
    "step": "步骤卡", "emotion": "情绪卡", "choice": "选择卡",
    "schedule": "流程卡", "reminder": "提醒卡",
}


def _draw_tag(d: ImageDraw.ImageDraw, text: str, y: int = 34) -> None:
    """顶部居中的小标签,标示当前阶段(示范 / 练习 / 想一想…)。"""
    font = _load_font(_CJK_FONTS, 26)
    w = d.textlength(text, font=font)
    d.text(((W - w) / 2, y), text, font=font, fill=ACCENT)


def _training_slide(out_path, *, tag, emoji, zh, en="", emoji_cy=90, emoji_size=170,
                    zh_size=50, en_size=30, top=340, progress=None, note=""):
    """训练模块通用文本幻灯:阶段标签 + emoji + 中文(大)+ 英文(小,字幕)+ 可选提示。"""
    img, d = _base_slide()
    if progress is not None:
        _draw_progress(d, progress[0], progress[1])
    if tag:
        _draw_tag(d, tag)
    _draw_emoji(d, d, emoji or "🧩", cy=emoji_cy, size=emoji_size)
    zh_font = _load_font(_CJK_FONTS, zh_size)
    en_font = _load_font(_CJK_FONTS, en_size)
    zh_lines = wrap_text(d, zh, zh_font, W - 220)
    y = _draw_centered_block(d, zh_lines, zh_font, TEXT_ZH, top=top)
    if en:
        en_lines = wrap_text(d, en, en_font, W - 220)
        y = _draw_centered_block(d, en_lines, en_font, TEXT_EN, top=y + 14)
    if note:
        note_font = _load_font(_CJK_FONTS, 30)
        nl = wrap_text(d, note, note_font, W - 260)
        _draw_centered_block(d, nl, note_font, ACCENT, top=y + 20)
    _draw_footer(d)
    out_path = Path(out_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    img.save(out_path)
    return out_path


def render_training_title(module, out_path):
    img, d = _base_slide()
    _draw_emoji(d, d, module.steps[0].icon if module.steps else "🎯", cy=130, size=150)
    _draw_tag(d, "训练模块 · Training", y=320)
    zh_font = _load_font(_CJK_BOLD, 56)
    en_font = _load_font(_CJK_FONTS, 30)
    zh_lines = wrap_text(d, module.title_zh, zh_font, W - 200)
    y = _draw_centered_block(d, zh_lines, zh_font, TEXT_ZH, top=360)
    en_lines = wrap_text(d, module.title_en, en_font, W - 200)
    _draw_centered_block(d, en_lines, en_font, TEXT_EN, top=y + 8)
    _draw_footer(d)
    out_path = Path(out_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    img.save(out_path)
    return out_path


def render_training_intro(module, out_path):
    # 直接进入故事:无说教标签,用情境相关的 emoji,像故事开头一样呈现。
    icon = (module.social_choice.icon if module.social_choice
            else (module.steps[0].icon if module.steps else "🌈"))
    return _training_slide(out_path, tag="", emoji=icon,
                           zh=module.intro_zh, en=module.intro_en,
                           emoji_cy=90, emoji_size=170, zh_size=46, top=330)


def render_training_step(step, index, total, out_path):
    return _training_slide(out_path, tag="", emoji=step.icon,
                           zh=step.text_zh, en=step.text_en,
                           zh_size=50, top=340, progress=(index, total))


def render_practice_prompt(trial, out_path):
    return _training_slide(out_path, tag="", emoji=trial.icon or "❓",
                           zh=trial.prompt_zh, en=trial.prompt_en, zh_size=46, top=300,
                           note="⏳ 轮到你,试试看 · Your turn")


def render_practice_answer(trial, out_path):
    return _training_slide(out_path, tag="可以这样说 · Like this", emoji="💬",
                           zh=trial.answer_zh, en=trial.answer_en, zh_size=50, top=340)


def render_practice_reinforce(trial, out_path):
    return _training_slide(out_path, tag="做得好 · Great job", emoji="🌟",
                           zh=trial.reinforce_zh, en=trial.reinforce_en, zh_size=48, top=340)


def render_choice_scenario(sc, out_path):
    img, d = _base_slide()
    _draw_tag(d, "想一想 · Choose")
    _draw_emoji(d, d, sc.icon or "🤝", cy=70, size=130)
    zh_font = _load_font(_CJK_FONTS, 44)
    en_font = _load_font(_CJK_FONTS, 26)
    zh_lines = wrap_text(d, sc.scenario_zh, zh_font, W - 220)
    y = _draw_centered_block(d, zh_lines, zh_font, TEXT_ZH, top=250)
    en_lines = wrap_text(d, sc.scenario_en, en_font, W - 220)
    y = _draw_centered_block(d, en_lines, en_font, TEXT_EN, top=y + 8)
    opt_font = _load_font(_CJK_FONTS, 36)
    y += 26
    for i, o in enumerate(sc.options[:4]):
        line = f"{'ABCD'[i]}.  {o.label_zh}   {o.label_en}"
        if d.textlength(line, font=opt_font) > W - 160:
            line = f"{'ABCD'[i]}.  {o.label_zh}"
        w = d.textlength(line, font=opt_font)
        d.text(((W - w) / 2, y), line, font=opt_font, fill=ACCENT)
        y += int(opt_font.size * 1.5)
    _draw_footer(d)
    out_path = Path(out_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    img.save(out_path)
    return out_path


def render_choice_outcome(letter, option, out_path):
    return _training_slide(out_path, tag=f"选 {letter}:{option.label_zh}", emoji=option.icon or "🙂",
                           zh=option.outcome_zh, en=option.outcome_en, zh_size=46, top=330)


def render_training_review(module, out_path):
    return _training_slide(out_path, tag="", emoji="🌈",
                           zh=module.review_zh, en=module.review_en, zh_size=44, top=320,
                           note="本内容为辅助/教育工具,不替代专业诊疗。")


def render_card(card, out_path):
    """把一张视觉支持卡渲染成可打印的 PNG(大图标 + 标题 + 说明)。"""
    img, d = _base_slide()
    _draw_tag(d, _CARD_KIND_ZH.get(card.kind, "卡片") + " · Card")
    _draw_emoji(d, d, card.icon or "🧩", cy=130, size=210)
    zh_font = _load_font(_CJK_BOLD, 52)
    en_font = _load_font(_CJK_FONTS, 30)
    zh_lines = wrap_text(d, card.title_zh, zh_font, W - 200)
    y = _draw_centered_block(d, zh_lines, zh_font, TEXT_ZH, top=400)
    en_lines = wrap_text(d, card.title_en, en_font, W - 200)
    y = _draw_centered_block(d, en_lines, en_font, TEXT_EN, top=y + 6)
    if card.caption_zh:
        cap_font = _load_font(_CJK_FONTS, 30)
        cz = wrap_text(d, card.caption_zh, cap_font, W - 240)
        y = _draw_centered_block(d, cz, cap_font, ACCENT, top=y + 16)
    if card.caption_en:
        ce_font = _load_font(_CJK_FONTS, 24)
        ce = wrap_text(d, card.caption_en, ce_font, W - 240)
        _draw_centered_block(d, ce, ce_font, FOOTER, top=y + 6)
    _draw_footer(d)
    out_path = Path(out_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    img.save(out_path)
    return out_path


# =====================================================================
# 插画页:一张绘本插画铺满整页 + 底部柔和字幕带(中英)。用于"精美配图"模式。
# =====================================================================
_CAPTION_BAND = (250, 246, 238, 130)      # 半透明奶白字幕带:alpha 130,更通透、少遮挡背景插画


def _cover_fit(im: Image.Image, w: int, h: int) -> Image.Image:
    """等比缩放并居中裁剪,使图片恰好铺满 w×h(cover)。"""
    r = max(w / im.width, h / im.height)
    im = im.resize((max(1, int(im.width * r)), max(1, int(im.height * r))), Image.LANCZOS)
    x = (im.width - w) // 2
    y = (im.height - h) // 2
    return im.crop((x, y, x + w, y + h))


def _illustration_base(image_png) -> Image.Image:
    """底帧:载入插画 → cover 铺满 1280x720 → 加顶部品牌色条;返回 RGBA(不含任何文字)。
    render_illustrated 与 render_base_frame 共用它,保证两条路的底图完全一致。"""
    base = Image.open(image_png).convert("RGB")
    base = _cover_fit(base, W, H).convert("RGBA")
    d0 = ImageDraw.Draw(base)
    d0.rectangle([(0, 0), (W, 8)], fill=ACCENT + (255,))          # 顶部品牌色条
    return base


def render_illustrated(image_png, zh: str, en: str = "", out_path=None,
                       progress=None, note: str = "") -> Path:
    """把一张插画合成为成品页:插画铺满 + 顶部色条 + 底部柔和字幕带(中英 + 可选提示)。"""
    base = _illustration_base(image_png)

    zh_font = _load_font(_CJK_BOLD, 42)
    en_font = _load_font(_CJK_FONTS, 26)
    note_font = _load_font(_CJK_FONTS, 26)

    tmp = ImageDraw.Draw(base)
    zh_lines = wrap_text(tmp, zh, zh_font, W - 140)
    en_lines = wrap_text(tmp, en, en_font, W - 140) if en else []
    note_lines = wrap_text(tmp, note, note_font, W - 160) if note else []
    lh_zh, lh_en, lh_note = int(zh_font.size * 1.35), int(en_font.size * 1.35), int(note_font.size * 1.3)

    band_h = (22 + len(zh_lines) * lh_zh
              + (8 + len(en_lines) * lh_en if en_lines else 0)
              + (10 + len(note_lines) * lh_note if note_lines else 0)
              + 58)
    band_top = H - band_h

    overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    od = ImageDraw.Draw(overlay)
    od.rounded_rectangle([(24, band_top), (W - 24, H - 12)], radius=28, fill=_CAPTION_BAND)
    base = Image.alpha_composite(base, overlay)

    d = ImageDraw.Draw(base)
    # 不在成品插画页右上角画“k / N”页码(用户要求:生成照片不出现该数字)。
    # progress 参数保留仅为签名兼容,不再绘制。

    y = band_top + 16
    for ln in zh_lines:
        w = d.textlength(ln, font=zh_font)
        d.text(((W - w) / 2, y), ln, font=zh_font, fill=TEXT_ZH)
        y += lh_zh
    if en_lines:
        y += 8
        for ln in en_lines:
            w = d.textlength(ln, font=en_font)
            d.text(((W - w) / 2, y), ln, font=en_font, fill=TEXT_EN)
            y += lh_en
    if note_lines:
        y += 10
        for ln in note_lines:
            w = d.textlength(ln, font=note_font)
            d.text(((W - w) / 2, y), ln, font=note_font, fill=ACCENT)
            y += lh_note

    # 说明:插画页不再叠加底部“示范·需专业审核”标注,保持画面干净整洁。
    # 免责/草稿声明仍保留在 DISCLAIMER.txt、使用指南与收尾页,合规不受影响。

    out_path = Path(out_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    base.convert("RGB").save(out_path)
    return out_path


def render_base_frame(image_png, out_path) -> Path:
    """底帧模式:只输出插画本体(cover + 顶部色条),**不烧任何字幕**。
    供付费互动播放器 / 软字幕(可切中/粤/英)路复用——字幕在运行时叠加或作独立轨,
    因此同一张底帧能配任意语言,不必为每种语言各烧一版画面。"""
    base = _illustration_base(image_png)
    out_path = Path(out_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    base.convert("RGB").save(out_path)
    return out_path
