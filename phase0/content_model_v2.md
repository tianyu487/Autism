# 内容模型 v2 —— beat 契约(Phase 0 · 草案)

> 目的:把当前扁平的 `module.json` 升级成**未来所有 agent 共享的中央契约**:稳定 beat ID +
> 语言键值容器(区分字幕/旁白)+ 时间轴无关 + 预留粤语与互动分支。
> **零风险落地**:v2 作为新真源,`to_legacy()` 能**精确复原**当前 `module.json`,现有管线原样能跑。
>
> 状态:已在 2 门成片(calm_breathing / handwashing)+ 5 门新课上做**往返无损**校验通过,
> 且派生的 beat 序列与各课 `page_visuals` 的键**完全一致**。

---

## 1. 为什么要它

三个演化方向(可切字幕 中/粤/英、同步配音、付费互动)最终都收敛到同一句话:

> **"每个 beat(稳定 ID)× 每种语言 ×(字幕 + 旁白 + 音频 + 时长/留白 + 分支)"** 这张清单。

把这张清单定下来,免费的"逐语言 MP4 装配器"和付费的"事件驱动互动播放器"都只是它的**消费者**;
粤语只是"给某个键填值",互动只是"给某个选项填 `goto`"。这就是 Phase 0 的全部意义。

---

## 2. 三个关键改动

### 2.1 稳定 beat ID(与现有 page_visuals 键对齐)
每个产生画面的元素都有稳定 `id`;整门课的**规范 beat 序列**由结构派生,和 `pipeline.emit` 一致:

```
title · intro · step1..stepN · trial{k}_prompt/answer/reinforce · choice · choice_A/B · review
```

好处:① 插入/重排某页不再因"序号错位"打乱缓存与审查;② 互动分支必须指向**稳定目标**,没有 ID 就做不了。
现有 `page_visuals` 本就用这些名字当键 —— 所以这一步只是把隐含约定**正式确立**,不动数据。

### 2.2 语言键值容器 i18n(区分"字幕"与"旁白")
每个可本地化文本从 `X_zh / X_en` 两个扁平字段,收拢成一个容器:

```json
"text":      { "zh": "嘴角弯弯往上翘,这是开心。", "en": "When the mouth curves up, that is happy.", "yue": null },
"narration": { "zh": "嘴角弯弯地往上翘,眼睛亮亮的,这是开心。", "en": "...", "yue": null }
```

- **字幕(text/label/caption/scenario…)** 与 **旁白(narration)** 分开存 —— 这是为决策二配置2 预留的:
  粤语的**旁白脚本(粵口語)** 会和**字幕(書面中文)** 不一样,靠这个分离一次容纳。
- `yue` 先留 `null`,二期填入,**不改结构**。

### 2.3 时间轴无关
`duration_hint` 降级为 `min_seconds`(建议下限),练习页保留 `pause_seconds`(留白下限)。
**真实每页时长在装配时由该语言音频长度决定** —— 这样同一份内容能出任意语言、任意节奏,
免费 MP4 逐语言精确配速,付费播放器"音频放完即进"。

### 2.4 互动分支预留
每个选择项加 `"goto": null`(目标 beat-id,null=线性继续)。二期做互动时只填值,不改模型。

---

## 3. 顶层结构

```
schema_version: 2
id                     课程 slug
languages: ["zh","en"]  已填充语言(粤语二期加 "yue")
method_id / cast        循证方法 / 视觉阵容(不变)
learning_objective      i18n(付费版多语言家长/教师指南要用,故本地化;先只填 zh)
title / intro / review  i18n
steps[]                 {id, index, text(i18n), narration(i18n), visual_keyword, icon, min_seconds}
practice_trials[]       {id, index, prompt/answer/reinforce(i18n), pause_seconds, icon}
social_choice           {id:"choice", scenario(i18n), icon, options[]:{id, label/outcome(i18n), icon, goto}}
visual_cards[]          {kind, title/caption(i18n), icon}
citations_used          引用 id 列表(语言中性,不本地化)
review_flags[]          i18n(草稿/复核提示会写进多语言指南,故本地化;先只填 zh)
page_visuals            按 beat-id 的逐页画面(英文,不本地化)
```

机器可校验的完整定义见 `content_schema_v2.json`(JSON Schema draft-07)。

---

## 4. 兼容策略(为什么零风险)

- v2 是**新真源**(独立文件 `*.v2.json`),**不喂给当前管线**;当前 `train --script module.json` 继续吃原文件,照跑。
- `convert_module.py` 提供两向:
  - `upgrade(module.json) -> v2`:把现有课程升级成 v2(供后续新代码消费);
  - `to_legacy(v2) -> module.json`:从 v2**精确复原**当前扁平格式(供现有管线继续用)。
- 已验证 `to_legacy(upgrade(x)) == x`(逐字段深比)在全部 7 门课上**无损**。
  这意味着:即便我们把所有课迁到 v2,也能随时一键生成"当前管线认识的" module.json —— **不破坏任何现有能力**。

### 用法
```bash
python convert_module.py selftest  output/*/module.json     # 往返无损校验(应全 OK)
python convert_module.py upgrade   module.json  module.v2.json
python convert_module.py downgrade module.v2.json  module.json
python convert_module.py batch     scripts/                 # 批量升级为 *.v2.json
```

---

## 5. 它如何对接后续

- **渲染层**(Base-Frame / 字幕轨):底帧只画插画;字幕文本从 `i18n[lang]` 取,按语言出软字幕或烧录。
- **配音**(Dubbing):旁白从 `narration[lang]`(粤语用其专属脚本)取,逐 beat 合成各语言音频。
- **装配**:免费=逐语言 MP4(按该语言音频定时长);付费=事件驱动播放器(读 beat 序列 + `goto` 分支)。
- **多语言家长/教师指南**(付费):`guide.md` 的可本地化内容来自本模型的 `learning_objective` + `review_flags`;
  其余(方法名、免责声明、章节模板)来自 `knowledge/`(methods 的 name_zh/en、safety_rules 的 disclaimer zh/en)与打包模板,
  在**打包层**按语言拼装,不进本 schema。引用条目(作者/年份/DOI)语言中性,直接复用。
- **agent 拆分**:这份 schema 就是各 agent 之间的 I/O 契约 —— 之后"升格 agent"只是给模块套上它,不再返工。

---

## 6. 下一步(接 Phase 0 剩余)

1. 把 `models.py` 增加 v2 读取(pydantic 模型),让新代码直接吃 v2;
2. `render.py` 拆出"底帧(无字) / 烧字幕"两模式;
3. `tts.py` 从 `narration[lang]` 取词,`video.py` 按语言循环出 MP4(Phase 1:中/英)。

本步只交付**契约 + 无损转换器**,不动任何现有课程与管线。你在此定稿后,我再往下接。
