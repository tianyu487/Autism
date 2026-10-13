# 角色素材库 · Character Asset Library

同一批系列角色（小明 + 同伴女孩）的**不同表情、动作、服装**原始插画，作为后续视频/图卡/情绪卡的可复用素材。
风格与身份见 `design/visual_style_bible.md`（§3 角色设定、§3.4 变体与素材库）。

## 目录
- `xiaoming/` — 小明（男孩）：`boy_expr_<表情>.png`（8 表情）+ `boy_outfit_<装>.png`（3 换装）
- `friend/`   — 同伴女孩：`girl_expr_<表情>.png`（8 表情）+ `girl_outfit_<装>.png`（3 换装）
- `together/` — 同框互动：`pair_<动作>.png`（wave/play/comfort/share/think/laugh）
- `_sheet_*.png` — 三张带文件名标注的速览拼图（QA/挑选用）

**表情**：happy · calm · sad · surprised · thinking · proud · shy · excited
**服装**：boy = default/stripe/hoodie/overalls；girl = default/dress/cardigan/overalls

## 生成参数
- 免费 Pollinations（Flux）；尺寸 1024×768；风格串 = `illustrate.STYLE`；seed = 4242 + 序号。
- 提示词由 `cast.portrait_prompt()` / `cast.together_prompt()` 组装（身份 + 表情 + 服装 + 简洁中性背景）。
- 纯视觉、无台词（避免背景乱码文字）。

## 重生成 / 扩充
```
python scratchpad/gen_assets.py            # 全量重生成
python scratchpad/gen_assets.py 3 7 12     # 只重跑这几号（失败重试）
python scratchpad/montage_assets.py        # 重建三张速览拼图
```
新增表情/服装/动作 → 改 `autismcare/cast.py` 的 `EXPRESSIONS/OUTFITS/TOGETHER_ACTIONS`，再跑上面脚本。

## 局限
Flux + seed 只锁"同一角色家族/画风",不锁逐张同脸——这是一批**供挑选**的素材,表情与身份都足够识别,
但非像素级一致。要严格同脸复现,需升级 `illustrate.py` 后端(角色参考图 / LoRA / img2img)。

> 草稿素材:正式对外使用前需专业人员按用途审核。本工具为辅助/教育用途,不替代专业诊疗。
