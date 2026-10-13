"""命令行入口。

用法示例:
  python -m autismcare generate --config config/example_story.yaml
  python -m autismcare generate --config config/example_story.yaml --no-ai   # 免密钥,验证媒体管线
  python -m autismcare generate --situation "第一天上幼儿园" --name 乐乐 --age 5
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

import yaml

try:
    from dotenv import load_dotenv
    load_dotenv()  # 读取 .env 中的 ANTHROPIC_API_KEY 等
except Exception:
    pass

from .models import StorySpec, TrainingSpec
from .pipeline import (
    load_script_json, load_training_json, run_game_pipeline, run_pipeline,
    run_training_pipeline,
)


def _load_spec_optional(args) -> StorySpec | None:
    """尽力构造 StorySpec;缺少 situation 时返回 None(留给 --script / --no-ai 模式)。"""
    data: dict = {}
    if args.config:
        with open(args.config, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f) or {}
    if args.situation:
        data["situation"] = args.situation
    if args.name:
        data["child_name"] = args.name
    if args.age is not None:
        data["age"] = args.age
    if args.goal:
        data["goal"] = args.goal
    if args.slug:
        data["project_slug"] = args.slug
    if not data.get("situation"):
        return None
    return StorySpec(**data)


def cmd_generate(args) -> int:
    import os
    if args.tts:
        os.environ["AUTISMCARE_TTS"] = args.tts
    if args.zh_voice:
        os.environ["AUTISMCARE_ZH_VOICE"] = args.zh_voice
    if args.zh_style:
        os.environ["AUTISMCARE_AZURE_STYLE"] = args.zh_style

    spec = _load_spec_optional(args)
    script = load_script_json(args.script) if args.script else None

    if script is None and not args.no_ai and spec is None:
        raise SystemExit(
            "错误:请提供以下之一 —— situation(--config/--situation)、"
            "--script <script.json>、或 --no-ai。"
        )

    result = run_pipeline(
        spec=spec,
        script=script,
        out_root=Path(args.out),
        no_ai=args.no_ai,
        keep_temp=args.keep_temp,
        model=args.model,
        slug=args.slug,
        narrate_english=args.en_audio,
    )
    print("\n=== 完成 ===")
    print(f"输出目录:{result['out_dir']}")
    print(f"成品视频:{result['final_mp4']}")
    print(f"通过校验:{result['passed']} | 需专业审核:{result['review_required']}")
    if not result["passed"]:
        print("⚠️ 未通过基础校验:视频已标记为草稿,请查看 guide.md 修正后再使用。")
    print("产物包含:script.json / script.md / citations.md / guide.md / DISCLAIMER.txt / scenes/")
    return 0


def _apply_tts_env(args) -> None:
    import os
    if getattr(args, "tts", None):
        os.environ["AUTISMCARE_TTS"] = args.tts
    if getattr(args, "zh_voice", None):
        os.environ["AUTISMCARE_ZH_VOICE"] = args.zh_voice
    if getattr(args, "zh_style", None):
        os.environ["AUTISMCARE_AZURE_STYLE"] = args.zh_style


def _print_skills() -> None:
    from . import knowledge as K
    print("可用技能领域与技能区(用 --skill-area <id>):\n")
    for d in K.list_skill_domains():
        dom = K.load_skill_domain(d)
        print(f"# 领域 {d}:{dom.get('name_zh','')} / {dom.get('name_en','')}")
        for a in dom.get("skill_areas", []) or []:
            print(f"    {a.get('id'):24s} {a.get('name_zh','')}")
        print()


def _load_training_spec_optional(args) -> TrainingSpec | None:
    """尽力构造 TrainingSpec;缺少 skill_target 时返回 None(留给 --script / --no-ai)。"""
    data: dict = {}
    if args.config:
        with open(args.config, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f) or {}
    if args.skill:
        data["skill_target"] = args.skill
    if getattr(args, "method", None):
        data["method_id"] = args.method
    if getattr(args, "domain", None):
        data["skill_domain"] = args.domain
    if getattr(args, "skill_area", None):
        data["skill_area"] = args.skill_area
    if args.name:
        data["child_name"] = args.name
    if args.age is not None:
        data["age"] = args.age
    if args.goal:
        data["goal"] = args.goal
    if args.interests:
        data["interests"] = [x for x in re.split(r"[,、,\s]+", args.interests) if x]
    if args.slug:
        data["project_slug"] = args.slug
    if not (data.get("skill_target") or data.get("skill_area")):
        return None
    return TrainingSpec(**data)


def cmd_train(args) -> int:
    if getattr(args, "list_skills", False):
        _print_skills()
        print("示例:python -m autismcare train --skill-area regulation_strategies --name 乐乐 --age 6")
        return 0

    _apply_tts_env(args)

    spec = _load_training_spec_optional(args)
    module = load_training_json(args.script) if args.script else None

    if module is None and not args.no_ai and spec is None:
        raise SystemExit(
            "错误:请提供以下之一 —— 训练技能(--config/--skill)、"
            "--script <module.json>、或 --no-ai。"
        )

    result = run_training_pipeline(
        spec=spec,
        module=module,
        out_root=Path(args.out),
        no_ai=args.no_ai,
        keep_temp=args.keep_temp,
        model=args.model,
        slug=args.slug,
        narrate_english=args.en_audio,
        scenes_only=getattr(args, "scenes_only", False),
        reuse_scenes=getattr(args, "reuse_scenes", False),
    )
    print("\n=== 完成 ===")
    print(f"输出目录:{result['out_dir']}")
    if getattr(args, "scenes_only", False):
        print(f"场景插画:{result['n_scenes']} 页 → {result['scenes_dir']}(仅出图,未配音/未合成)")
        print(f"通过校验:{result['passed']} | 需专业审核:{result['review_required']}")
        print("审图满意后,用相同 --slug 再跑一次(去掉 --scenes-only)即可续做配音+合成,不重复出图。")
        return 0
    print(f"训练视频:{result['final_mp4']}")
    print(f"配套图片:{result['n_cards']} 张 → {result['images_dir']}")
    print(f"通过校验:{result['passed']} | 需专业审核:{result['review_required']}")
    if not result["passed"]:
        print("⚠️ 未通过基础校验:视频已标记为草稿,请查看 guide.md 修正后再使用。")
    print("产物包含:module.json / script.md / citations.md / guide.md / DISCLAIMER.txt / scenes/ / images/")
    return 0


def cmd_game(args) -> int:
    if getattr(args, "list_skills", False):
        _print_skills()
        print("示例:python -m autismcare game --skill-area regulation_strategies --name 乐乐 --age 6")
        return 0

    spec = _load_training_spec_optional(args)
    module = load_training_json(args.script) if args.script else None

    if module is None and not args.no_ai and spec is None:
        raise SystemExit(
            "错误:请提供以下之一 —— 训练技能(--config/--skill 或 --skill-area)、"
            "--script <module.json>、或 --no-ai。"
        )

    result = run_game_pipeline(
        spec=spec,
        module=module,
        out_root=Path(args.out),
        no_ai=args.no_ai,
        keep_temp=args.keep_temp,
        model=args.model,
        slug=args.slug,
        game_type=args.game_type,
    )
    print("\n=== 完成 ===")
    print(f"输出目录:{result['out_dir']}")
    print(f"小游戏:{result['game_html']}(用浏览器打开)")
    print(f"配套图片:{result['n_cards']} 张 → {result['images_dir']}")
    print(f"通过校验:{result['passed']} | 需专业审核:{result['review_required']}")
    if not result["passed"]:
        print("⚠️ 未通过基础校验:游戏已标记为草稿,请查看 guide.md 修正后再使用。")
    print("产物包含:game.html / module.json / script.md / citations.md / guide.md / DISCLAIMER.txt / images/")
    return 0


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="autismcare",
        description="面向自闭症儿童的循证疗愈内容生成器(社交故事 → 中英双语成品视频)。",
    )
    sub = p.add_subparsers(dest="command", required=True)

    g = sub.add_parser("generate", help="生成一份社交故事的双语成品视频与产物包")
    g.add_argument("--config", help="输入 YAML(如 config/example_story.yaml)")
    g.add_argument("--script", help="直接用已生成的 script.json(跳过 API;Claude Code 现场生成用)")
    g.add_argument("--situation", help="目标场景/情境(覆盖配置)")
    g.add_argument("--name", help="孩子名字(覆盖配置)")
    g.add_argument("--age", type=int, help="年龄(覆盖配置)")
    g.add_argument("--goal", help="学习目标(覆盖配置)")
    g.add_argument("--slug", help="输出文件夹名(覆盖配置)")
    g.add_argument("--out", default="output", help="输出根目录(默认 output)")
    g.add_argument("--model", help="覆盖生成用的 Claude 模型(默认 claude-opus-4-8)")
    g.add_argument("--no-ai", action="store_true",
                   help="不调用 Claude,用内置样例脚本跑通媒体管线(免密钥/离线)")
    g.add_argument("--keep-temp", action="store_true", help="保留 _work 临时音频/片段")
    g.add_argument("--en-audio", action="store_true",
                   help="同时朗读英文旁白(默认只读中文,英文仅作画面字幕)")
    g.add_argument("--zh-voice", help="中文配音语音(如 zh-CN-XiaoyiNeural);默认 zh-CN-XiaoxiaoNeural")
    g.add_argument("--tts", choices=["edge", "azure"], help="配音后端(默认 edge;azure 更自然,需密钥)")
    g.add_argument("--zh-style", help="Azure 情感风格(gentle 温柔 / affectionate 亲切 / calm / cheerful)")
    g.set_defaults(func=cmd_generate)

    # ---- 训练模块:视频即康复训练(视频示范 + 练习回合 + 社交选择 + 图片卡)----
    t = sub.add_parser("train", help="生成一个「训练模块」:能练到技能的双语视频课程 + 可打印图片卡")
    t.add_argument("--config", help="输入 YAML(含 skill_target 等)")
    t.add_argument("--script", help="直接用已生成的 module.json(跳过 API)")
    t.add_argument("--skill", help="要训练的具体、可观察的目标行为/技能")
    t.add_argument("--method", help="循证方法 id(默认 video_modeling;可选 cognitive_behavioral / social_skills_training,见 methods/_registry.yaml)")
    t.add_argument("--domain", help="技能领域库 id(如 emotional_regulation / social_interaction)")
    t.add_argument("--skill-area", help="技能区 id(如 regulation_strategies);据此自动带出发展序列目标 + 推荐方法 + 引用")
    t.add_argument("--list-skills", action="store_true", help="列出可用的技能领域与技能区后退出")
    t.add_argument("--scenes-only", action="store_true",
                   help="只渲染场景插画后停下(先审图);满意后用相同 --slug 再跑即续做配音+合成,不重复出图")
    t.add_argument("--reuse-scenes", action="store_true",
                   help="已存在的 scenes/NN 页原样复用、绝不重绘(保留人工手改的成品页),只对缺失页出图,再合成视频")
    t.add_argument("--name", help="孩子名字")
    t.add_argument("--age", type=int, help="年龄")
    t.add_argument("--goal", help="可测量的训练目标(可留空由 AI 拟定)")
    t.add_argument("--interests", help="孩子兴趣,逗号分隔(如 恐龙,小汽车)")
    t.add_argument("--slug", help="输出文件夹名(覆盖配置)")
    t.add_argument("--out", default="output", help="输出根目录(默认 output)")
    t.add_argument("--model", help="覆盖生成用的 Claude 模型(默认 claude-opus-4-8)")
    t.add_argument("--no-ai", action="store_true",
                   help="不调用 Claude,用内置训练样例跑通媒体管线(免密钥/离线)")
    t.add_argument("--keep-temp", action="store_true", help="保留 _work 临时音频/片段")
    t.add_argument("--en-audio", action="store_true",
                   help="同时朗读英文旁白(默认只读中文,英文仅作画面字幕)")
    t.add_argument("--zh-voice", help="中文配音语音(如 zh-CN-XiaoyiNeural)")
    t.add_argument("--tts", choices=["edge", "azure"], help="配音后端(默认 edge;azure 更自然,需密钥)")
    t.add_argument("--zh-style", help="Azure 情感风格(gentle / affectionate / calm / cheerful)")
    t.set_defaults(func=cmd_train)

    # ---- 互动小游戏:读同一份训练模块,输出可点击的 HTML5 网页游戏 ----
    gm = sub.add_parser("game", help="生成一个「互动小游戏」:可点击的 HTML5 网页游戏(读同一份训练模块)")
    gm.add_argument("--config", help="输入 YAML(含 skill_target 等)")
    gm.add_argument("--script", help="直接用已生成的 module.json(跳过 API)")
    gm.add_argument("--skill", help="要训练的具体、可观察的目标行为/技能")
    gm.add_argument("--method", help="循证方法 id(见 methods/_registry.yaml)")
    gm.add_argument("--domain", help="技能领域库 id(如 emotional_regulation / social_interaction)")
    gm.add_argument("--skill-area", help="技能区 id;据此自动带出发展序列目标 + 推荐方法")
    gm.add_argument("--game-type", choices=["pack", "story", "sequence", "match"], default="pack",
                    help="玩法:pack 首页选(默认)/ story 听故事 / sequence 排顺序 / match 配一配")
    gm.add_argument("--list-skills", action="store_true", help="列出可用的技能领域与技能区后退出")
    gm.add_argument("--name", help="孩子名字")
    gm.add_argument("--age", type=int, help="年龄")
    gm.add_argument("--goal", help="可测量的训练目标(可留空由 AI 拟定)")
    gm.add_argument("--interests", help="孩子兴趣,逗号分隔(如 恐龙,小汽车)")
    gm.add_argument("--slug", help="输出文件夹名")
    gm.add_argument("--out", default="output", help="输出根目录(默认 output)")
    gm.add_argument("--model", help="覆盖生成用的 Claude 模型(默认 claude-opus-4-8)")
    gm.add_argument("--no-ai", action="store_true",
                    help="不调用 Claude,用内置训练样例跑通(免密钥/离线)")
    gm.add_argument("--keep-temp", action="store_true", help="保留临时文件")
    gm.set_defaults(func=cmd_game)

    return p


def main(argv=None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
