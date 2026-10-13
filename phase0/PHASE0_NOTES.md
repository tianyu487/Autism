# Phase 0 · 后两步落地说明

本次交付 Phase 0 剩下的两步,均**只新增能力、不改现有行为**,并已单元验证。

## ① models 层加 v2 读取 —— `autismcare/content_v2.py`(新文件)

- 完整的 v2 pydantic 模型(`I18N` / `StepV2` / `TrialV2` / `OptionV2` / `SocialChoiceV2` /
  `VisualCardV2` / `PageVisualV2` / `ContentModuleV2`),`extra=ignore`(转换器写的 `_present` 记账键自动忽略)。
- 桥接:`ContentModuleV2.to_legacy_dict(lang="zh")` / `.to_training_module()` 把 v2 摊平回当前 `TrainingModule`。
  出粤语片时传 `lang="yue"`,中文槽即取粤语文本(英文槽固定取 en)。
- **管线单一接入点**:`load_training_any(path, lang="zh")` —— v1 扁平 `module.json` 直通、v2 自动降级,都返回 `TrainingModule`。
- 未改 `models.py`,零风险。

**如何接入(下一步的一行改动)**:把 `pipeline.load_training_json` 或 `cli.cmd_train` 里的
`load_training_json(args.script)` 换成 `content_v2.load_training_any(args.script)`,
`train --script X.v2.json` 就能直接跑;对现有 v1 文件行为完全不变。这行我先没动,留给你确认后再接。

## ② render 拆“底帧 / 烧字幕”两模式 —— `autismcare/render.py`(改)

- 新增 `_illustration_base(image_png)`:载入插画 → cover 铺满 1280×720 → 顶部品牌色条,返回**不含任何文字**的底图。
- 新增 `render_base_frame(image_png, out_path)`:**底帧模式**,只出插画本体、不烧字幕。
  供付费互动播放器 / 软字幕(可切中/粤/英)路复用——同一张底帧配任意语言,不必逐语言各烧一版画面。
- `render_illustrated(...)`:签名与行为**完全不变**(仍是“烧字幕”模式,供逐语言 MP4 用),内部改为复用 `_illustration_base`。

## 验证(本次容器内实跑)

- `render_illustrated` 重构前后输出**逐字节一致**(14546 bytes 完全相同)→ 现有出图零行为变化。
- `render_base_frame` 产出合法 1280×720 底帧,且与烧字幕版不同(确无字幕带)。
- 全部 7 门课:`TrainingModule(v1 原始) == TrainingModule(经 v2 读取降级)` → 管线读 v2 得到与原来**完全相同**的模块。

## 没有动的东西

`models.py`、`pipeline.py` 行为、现有课程与成片、STYLE/seed/画风。均不受影响。

## 建议的下一步

1. 一行接入 `load_training_any`,让 `train` 同时吃 v1/v2(可选,随时可做)。
2. Phase 1:`tts.py` 从 `narration[lang]` 取词补上英文配音;`video.py` 按语言循环出**逐语言 MP4**;
   出图改用 `render_base_frame` 出无字底帧、字幕走软轨/按语言烧。到这一步就能看到“中/英可切”的实物。
