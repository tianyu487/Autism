"""端到端编排:社交故事规格 → 双语成品视频 + 完整产物包。

流程:生成/取样脚本 → 校验 → 渲染幻灯 → 双语配音 → 合成片段 → 拼接成片 → 打包。
"""

from __future__ import annotations

import json
import shutil
from pathlib import Path

from . import cast, game, illustrate, package, render, tts, video
from .generate import generate_script, generate_training, sample_script, sample_training
from .models import StorySpec, StoryScript, TrainingModule, TrainingSpec, ensure_dir
from .models import _slugify
from .validate import validate_script, validate_training


def load_script_json(path: str | Path) -> StoryScript:
    """从 script.json 载入一份已生成好的脚本(供 --script / Claude Code 现场生成使用)。"""
    with open(path, "r", encoding="utf-8") as f:
        return StoryScript(**json.load(f))

# 结尾页的旁白(与 render.render_closing 的默认文案一致)
CLOSING_ZH = "这个故事到这里就结束啦。你做得很好!"
CLOSING_EN = "This is the end of the story. You did great!"


def run_pipeline(spec: StorySpec | None = None, script: StoryScript | None = None,
                 out_root: Path = Path("output"), no_ai: bool = False,
                 keep_temp: bool = False, model: str | None = None,
                 slug: str | None = None, narrate_english: bool = False) -> dict:
    # 1) 取得脚本(优先级:显式传入 > --no-ai 样例 > 调 Claude 生成)
    if script is not None:
        print("· 使用已提供的脚本(--script / Claude Code 现场生成)")
    elif no_ai:
        print("· 使用内置样例脚本(--no-ai,不调用 Claude)")
        script = sample_script()
    else:
        if spec is None:
            raise ValueError("需要提供 spec(或 --script / --no-ai)。")
        print(f"· 调用 Claude 生成脚本(model={model or '默认'})…")
        script = generate_script(spec, model=model)
    print(f"  标题:{script.title_zh} / {script.title_en}({len(script.scenes)} 屏)")

    # 决定输出文件夹名
    if slug:
        slug = _slugify(slug)
    elif spec is not None:
        slug = spec.resolved_slug()
    else:
        slug = _slugify(script.title_zh) or "story"
    out_dir = ensure_dir(Path(out_root) / slug)
    scenes_dir = ensure_dir(out_dir / "scenes")
    work_dir = ensure_dir(out_dir / "_work")

    # 2) 校验 + 安全门禁
    report = validate_script(script)
    if report.errors:
        print("  ⚠️ 校验发现问题(将标记为草稿):")
        for e in report.errors:
            print("    -", e)
    for w in report.warnings:
        print("    · 提醒:", w)

    # 3) 渲染幻灯 + 组织“片段清单”:标题 → 各屏 → 结尾
    print("· 渲染幻灯画面…")
    clips_spec: list[tuple[Path, str, str]] = []

    title_png = render.render_title(script, scenes_dir / "scene_00_title.png")
    clips_spec.append((title_png, script.title_zh, script.title_en))

    total = len(script.scenes)
    for s in script.scenes:
        png = render.render_scene(s, total, scenes_dir / f"scene_{s.index:02d}.png")
        clips_spec.append((png, s.narration_zh, s.narration_en))

    closing_png = render.render_closing(scenes_dir / "scene_99_closing.png")
    clips_spec.append((closing_png, CLOSING_ZH, CLOSING_EN))

    # 4) 逐屏:配音 → 合成片段(默认只读中文,英文仅作画面字幕)
    print("· 生成配音并合成片段…" + ("(中英双语)" if narrate_english else "(仅中文旁白,英文只做字幕)"))
    clips: list[Path] = []
    for i, (png, nz, ne) in enumerate(clips_spec):
        zh_mp3 = tts.synth(nz, "zh", work_dir / f"a_{i:02d}_zh.mp3")
        en_mp3 = tts.synth(ne, "en", work_dir / f"a_{i:02d}_en.mp3") if narrate_english else None
        scene_audio = video.make_scene_audio(zh_mp3, en_mp3, work_dir / f"audio_{i:02d}.m4a")
        clip = video.make_scene_clip(png, scene_audio, work_dir / f"clip_{i:02d}.mp4")
        clips.append(clip)
        print(f"    片段 {i + 1}/{len(clips_spec)} 完成")

    # 5) 拼接成片(未通过校验则命名为草稿,提示需修正)
    final_name = "final.mp4" if report.passed else "final_DRAFT_needs_fix.mp4"
    final_mp4 = video.concat_clips(clips, out_dir / final_name, work_dir)
    print(f"· 成片:{final_mp4}")

    # 6) 打包脚本/引用/指南/免责
    print("· 打包脚本、引用、使用指南、免责声明…")
    artifacts = package.write_all(script, report, out_dir)

    # 7) 清理临时文件
    if not keep_temp:
        shutil.rmtree(work_dir, ignore_errors=True)

    result = {
        "out_dir": out_dir,
        "final_mp4": final_mp4,
        "passed": report.passed,
        "blocked": report.blocked,
        "review_required": report.review_required,
        "scenes_dir": scenes_dir,
        **{k: v for k, v in artifacts.items()},
    }
    return result


# =====================================================================
# 训练模块(Video Modeling)端到端编排:模块 → 训练视频 + 可打印图片卡 + 产物包
# =====================================================================
def load_training_json(path: str | Path) -> TrainingModule:
    """从 module.json 载入一个训练模块(供 --script 使用)。

    自动识别内容模型版本:v1 扁平 module.json 直通;v2(content_model_v2)自动降级;
    两者都返回同一个 TrainingModule —— 对 v1 文件行为完全不变。
    """
    from .content_v2 import load_training_any
    return load_training_any(path)


def collect_video(final_mp4: Path, slug: str, passed: bool, out_root: Path) -> Path:
    """把一节课的成片额外复制一份到**集中视频库**:与 out_root 同级的 `videos/<slug>.mp4`。

    这样所有课程的成片都在同一个文件夹里,便于统一查看/分发;不影响各课自己的产物包。
    未通过校验的加 `_DRAFT` 后缀,避免与正式片混淆。原成片保持不动(只复制、不移动)。
    """
    videos_dir = ensure_dir(Path(out_root).resolve().parent / "videos")
    dst = videos_dir / (f"{slug}.mp4" if passed else f"{slug}_DRAFT.mp4")
    shutil.copy2(final_mp4, dst)
    return dst


def run_training_pipeline(spec: TrainingSpec | None = None, module: TrainingModule | None = None,
                          out_root: Path = Path("output"), no_ai: bool = False,
                          keep_temp: bool = False, model: str | None = None,
                          slug: str | None = None, narrate_english: bool = False,
                          scenes_only: bool = False, reuse_scenes: bool = False) -> dict:
    """scenes_only=True:只渲染场景插画后返回(不配音/不合成),供先审图;
    满意后用相同 slug 再跑(scenes_only=False)会命中 _illus/ 缓存,不重复请求图像。

    reuse_scenes=True:某页 scenes/NN_name.png 已存在则**原样复用、绝不重绘**
    (保留人工手改过的成品页),只对缺失的页重新出图渲染 → 再据此配音合成。
    用于"手改某几张画面后,保留手改、只重新合成视频"。"""
    # 1) 取得训练模块
    if module is not None:
        print("· 使用已提供的训练模块(--script)")
    elif no_ai:
        print("· 使用内置训练模块样例(--no-ai,不调用 Claude)")
        module = sample_training()
    else:
        if spec is None:
            raise ValueError("需要提供 spec(或 --script / --no-ai)。")
        print(f"· 调用 Claude 生成训练模块(model={model or '默认'})…")
        module = generate_training(spec, model=model)
    print(f"  标题:{module.title_zh} / {module.title_en}")

    if slug:
        slug = _slugify(slug)
    elif spec is not None:
        slug = spec.resolved_slug()
    else:
        slug = _slugify(module.title_zh) or "training"
    out_dir = ensure_dir(Path(out_root) / slug)
    scenes_dir = ensure_dir(out_dir / "scenes")
    images_dir = ensure_dir(out_dir / "images")
    work_dir = ensure_dir(out_dir / "_work")

    # 2) 校验 + 安全门禁
    report = validate_training(module)
    if report.errors:
        print("  ⚠️ 校验发现问题(将标记为草稿):")
        for e in report.errors:
            print("    -", e)
    for w in report.warnings:
        print("    · 提醒:", w)

    # 3) 逐页:生成插画(失败自动回退到极简图标页)→ 组织“片段清单”
    #    标题 → 开场 → 示范 → 练习(提示/留白·示范·鼓励)→ 社交选择 → 收尾
    #    每个 beat = (png, 中文旁白, 英文字幕稿, 结尾静默秒数)
    print("· 生成插画并渲染幻灯…(首次较慢,插画会缓存到 _illus/)")
    illus_dir = ensure_dir(out_dir / "_illus")
    beats: list[tuple[Path, str, str, float]] = []
    i = 0
    base_scene = module.social_choice.scenario_en if module.social_choice else module.title_en
    cast_name = getattr(module, "cast", cast.DEFAULT_CAST)   # 该模块的固定视觉角色阵容
    peer_cast = cast.has_others(cast_name)                    # 双人题材才在画面里带"朋友/分享玩具"
    print(f"  视觉角色阵容:{cast_name}({'双人' if peer_cast else '单人'};固定角色/场景由 cast.py 自动注入,seed={illustrate.SEED})")

    page_visuals = getattr(module, "page_visuals", {}) or {}

    def emit(name, *, disp_zh, disp_en, narr_zh, narr_en, img_desc, fallback,
             note="", progress=None, tail=video.SCENE_TAIL, solo=False):
        """生成一页:有插画则用插画页,否则回退到图标页;登记为一个片段。

        solo=True → 只注入主角(单人特写/鼓励页);默认注入整个阵容(互动页)。
        若 module.page_visuals 里按页名给了覆盖,则用其 visual_en 作画面描述、
        用其 roles 决定出场角色——让插画忠实于该页文字所述场景(执行标准 2026‑07‑15)。
        """
        nonlocal i
        png_path = scenes_dir / f"{i:02d}_{name}.png"
        if reuse_scenes and png_path.exists() and png_path.stat().st_size > 2000:
            # 复用已有成品页(含人工手改),不重绘、不请求插画。
            beats.append((png_path, narr_zh, narr_en, tail))
            print(f"    第 {i + 1} 页:{name}(复用已有画面,未重绘)")
            i += 1
            return
        pv = page_visuals.get(name)
        if pv is not None and pv.roles is not None:
            anchors = cast.anchor_from_roles(pv.roles, scene=cast.scene_of(cast_name))
        else:
            anchors = cast.anchor_blocks(cast_name, with_others=not solo)
        if pv is not None and pv.visual_en:
            img_desc = pv.visual_en
        page_seed = pv.seed if (pv is not None and pv.seed is not None) else None
        illus = illustrate.illustration(img_desc, illus_dir / f"{i:02d}_{name}.png",
                                        seed=page_seed, anchors=anchors)
        if illus is not None:
            render.render_illustrated(illus, disp_zh, disp_en, png_path,
                                      progress=progress, note=note)
        else:
            fallback(png_path)
        beats.append((png_path, narr_zh, narr_en, tail))
        print(f"    第 {i + 1} 页:{name} {'(插画)' if illus else '(图标)'} 完成")
        i += 1

    emit("title", disp_zh=module.title_zh, disp_en=module.title_en,
         narr_zh=module.title_zh, narr_en=module.title_en,
         img_desc=f"{module.title_en}, a happy young child, warm cozy cheerful scene",
         fallback=lambda p: render.render_training_title(module, p))

    emit("intro", disp_zh=module.intro_zh, disp_en=module.intro_en,
         narr_zh=module.intro_zh, narr_en=module.intro_en,
         img_desc=module.intro_en,
         fallback=lambda p: render.render_training_intro(module, p))

    total = len(module.steps)
    for k, s in enumerate(module.steps, 1):
        emit(f"step{k}", disp_zh=s.text_zh, disp_en=s.text_en,
             narr_zh=s.narration_zh, narr_en=s.narration_en,
             img_desc=f"{s.text_en}, {base_scene}", progress=(k, total),
             fallback=lambda p, ss=s, kk=k: render.render_training_step(ss, kk, total, p))

    for t in module.practice_trials:
        emit(f"trial{t.index}_prompt", disp_zh=t.prompt_zh, disp_en=t.prompt_en,
             narr_zh=t.prompt_zh, narr_en=t.prompt_en,
             img_desc=(f"a young child with a friend and a toy, thoughtful and calm, {base_scene}"
                       if peer_cast else
                       f"a single young child alone, thoughtful and calm, thinking about what to do, {base_scene}"),
             note="⏳ 轮到你,试试看 · Your turn", tail=float(t.pause_seconds),
             fallback=lambda p, tt=t: render.render_practice_prompt(tt, p))
        emit(f"trial{t.index}_answer", disp_zh=t.answer_zh, disp_en=t.answer_en,
             narr_zh=f"可以这样说:{t.answer_zh}", narr_en=t.answer_en,
             img_desc=(f"a young child kindly responding to a friend, sharing a toy, {base_scene}"
                       if peer_cast else
                       f"a single young child calmly doing the step by themselves, {base_scene}"),
             fallback=lambda p, tt=t: render.render_practice_answer(tt, p))
        emit(f"trial{t.index}_reinforce", disp_zh=t.reinforce_zh, disp_en=t.reinforce_en,
             narr_zh=t.reinforce_zh, narr_en=t.reinforce_en,
             img_desc="a happy proud young child smiling, gentle warm encouragement",
             solo=True,   # 单人鼓励特写:只出主角
             fallback=lambda p, tt=t: render.render_practice_reinforce(tt, p))

    if module.social_choice is not None:
        sc = module.social_choice
        opt_note = "   ".join(f"{'ABCD'[k]}. {o.label_zh}" for k, o in enumerate(sc.options))
        emit("choice", disp_zh=sc.scenario_zh, disp_en=sc.scenario_en,
             narr_zh=sc.scenario_zh + " 你会怎么做呢?", narr_en=sc.scenario_en,
             img_desc=(f"{sc.scenario_en}, a young child and a friend, deciding"
                       if peer_cast else
                       f"{sc.scenario_en}, a single young child deciding what to do"),
             note=opt_note,
             fallback=lambda p, s2=sc: render.render_choice_scenario(s2, p))
        for k, o in enumerate(sc.options):
            letter = "ABCD"[k]
            emit(f"choice_{letter}", disp_zh=o.outcome_zh, disp_en=o.outcome_en,
                 narr_zh=f"如果{o.label_zh},{o.outcome_zh}", narr_en=o.outcome_en,
                 img_desc=f"{o.outcome_en}, {base_scene}", note=f"{letter}. {o.label_zh}",
                 fallback=lambda p, L=letter, oo=o: render.render_choice_outcome(L, oo, p))

    emit("review", disp_zh=module.review_zh, disp_en=module.review_en,
         narr_zh=module.review_zh, narr_en=module.review_en,
         img_desc=f"{module.review_en}, happy ending, warm and cozy",
         note="本内容为辅助/教育工具,不替代专业诊疗。",
         fallback=lambda p: render.render_training_review(module, p))

    # 3.5) 仅出场景插画:先给用户审图,满意后再用同一 slug 续跑合成视频。
    #      此时 scenes/ 与带角色锚点的 _illus/ 缓存都已生成好,续跑会命中缓存不重绘。
    if scenes_only:
        print(f"· 仅生成场景插画({len(beats)} 页)→ {scenes_dir}(未配音/未合成)。")
        return {
            "out_dir": out_dir,
            "scenes_dir": scenes_dir,
            "n_scenes": len(beats),
            "passed": report.passed,
            "review_required": True,
        }

    # 4) 逐屏:配音 → 合成片段(默认只读中文,英文仅作画面字幕)
    print("· 生成配音并合成片段…" + ("(中英双语)" if narrate_english else "(仅中文旁白,英文只做字幕)"))
    clips: list[Path] = []
    for j, (png, nz, ne, tail) in enumerate(beats):
        zh_mp3 = tts.synth(nz, "zh", work_dir / f"a_{j:02d}_zh.mp3")
        en_mp3 = tts.synth(ne, "en", work_dir / f"a_{j:02d}_en.mp3") if (narrate_english and ne) else None
        scene_audio = video.make_scene_audio(zh_mp3, en_mp3, work_dir / f"audio_{j:02d}.m4a", tail=tail)
        clip = video.make_scene_clip(png, scene_audio, work_dir / f"clip_{j:02d}.mp4")
        clips.append(clip)
        print(f"    片段 {j + 1}/{len(beats)} 完成")

    # 5) 拼接成片
    final_name = "final.mp4" if report.passed else "final_DRAFT_needs_fix.mp4"
    final_mp4 = video.concat_clips(clips, out_dir / final_name, work_dir)
    print(f"· 成片:{final_mp4}")

    # 5.5) 汇总:把成片额外复制一份到集中视频库(便于统一查看/分发)
    collected = collect_video(final_mp4, slug, report.passed, out_root)
    print(f"· 已汇总到视频库:{collected}")

    # 6) 导出可打印视觉卡片(图片)
    print("· 导出配套视觉卡片(images/)…")
    card_paths: list[Path] = []
    for k, c in enumerate(module.visual_cards, 1):
        cp = render.render_card(c, images_dir / f"card_{k:02d}_{c.kind}.png")
        card_paths.append(cp)

    # 7) 打包:模块 JSON / 可读脚本 / 引用 / 训练指南+记录表 / 免责
    print("· 打包模块、引用、训练指南、免责声明…")
    artifacts = package.write_all_training(module, report, out_dir)

    # 8) 清理临时文件
    if not keep_temp:
        shutil.rmtree(work_dir, ignore_errors=True)

    return {
        "out_dir": out_dir,
        "final_mp4": final_mp4,
        "passed": report.passed,
        "blocked": report.blocked,
        "review_required": report.review_required,
        "scenes_dir": scenes_dir,
        "images_dir": images_dir,
        "cards": card_paths,
        "n_cards": len(card_paths),
        **{k: v for k, v in artifacts.items()},
    }


# =====================================================================
# 互动小游戏(HTML5)端到端编排:训练模块 → 可点击网页游戏 + 图片卡 + 产物包
# 与视频管线并列;读同一份模块,不需 TTS/ffmpeg。
# =====================================================================
def run_game_pipeline(spec: TrainingSpec | None = None, module: TrainingModule | None = None,
                      out_root: Path = Path("output"), no_ai: bool = False,
                      keep_temp: bool = False, model: str | None = None,
                      slug: str | None = None, game_type: str = "pack") -> dict:
    # 1) 取得训练模块(与训练管线同源)
    if module is not None:
        print("· 使用已提供的训练模块(--script)")
    elif no_ai:
        print("· 使用内置训练模块样例(--no-ai,不调用 Claude)")
        module = sample_training()
    else:
        if spec is None:
            raise ValueError("需要提供 spec(或 --script / --no-ai)。")
        print(f"· 调用 Claude 生成训练模块(model={model or '默认'})…")
        module = generate_training(spec, model=model)
    print(f"  标题:{module.title_zh} / {module.title_en}")

    if slug:
        slug = _slugify(slug)
    elif spec is not None:
        slug = spec.resolved_slug()
    else:
        slug = _slugify(module.title_zh) or "game"
    out_dir = ensure_dir(Path(out_root) / slug)
    images_dir = ensure_dir(out_dir / "images")

    # 2) 校验 + 安全门禁
    report = validate_training(module)
    if report.errors:
        print("  ⚠️ 校验发现问题(将标记为草稿):")
        for e in report.errors:
            print("    -", e)
    for w in report.warnings:
        print("    · 提醒:", w)

    # 3) 渲染 HTML5 小游戏
    print("· 渲染 HTML5 小游戏…")
    game_name = "game.html" if report.passed else "game_DRAFT_needs_fix.html"
    game_html = game.render_game(module, out_dir / game_name, game_type=game_type)
    print(f"· 小游戏(玩法:{game_type}):{game_html}")

    # 4) 导出配套视觉卡片(图片)
    card_paths: list[Path] = []
    for k, c in enumerate(module.visual_cards, 1):
        card_paths.append(render.render_card(c, images_dir / f"card_{k:02d}_{c.kind}.png"))

    # 5) 打包:模块 JSON / 可读脚本 / 引用 / 训练指南+记录表 / 免责
    print("· 打包模块、引用、训练指南、免责声明…")
    artifacts = package.write_all_training(module, report, out_dir)

    return {
        "out_dir": out_dir,
        "game_html": game_html,
        "passed": report.passed,
        "blocked": report.blocked,
        "review_required": report.review_required,
        "images_dir": images_dir,
        "cards": card_paths,
        "n_cards": len(card_paths),
        **{k: v for k, v in artifacts.items()},
    }
