# 视觉风格与角色设定手册（Visual Style & Character Bible）

> 目的：锁定 `output/demo_training/scenes_clean/` 这一版**已获认可**的画风与人物，作为**以后所有新视频/图卡的统一基准**。
> 新内容生成时，照本手册注入相同的风格串、seed 与角色关键词，即可保持画风一致、人物尽量复现。
>
> **✅ 已接进生成器（2026‑07‑14）**：本手册的三根一致性支柱已经代码化、生成时自动注入，
> **无需人工贴提示词** ——
> - **STYLE 串 + seed 4242** → `autismcare/illustrate.py`（原就在此）；
> - **固定角色关键词块 + 场景锚点** → `autismcare/cast.py`（本手册 §3/§4 的代码化）；
> - **每个视频声明用哪套阵容** → `TrainingModule.cast` 字段（默认 `peer_play`）；
> - **逐页自动拼装** → `autismcare/pipeline.py`（互动页注入整套阵容、单人鼓励页只注入主角）。
>
> 基准样本：`D:\Claude\Autism\output\demo_training\scenes_clean\`（19 张，2026‑07‑14 用户"满意"确认）
> 参考总览图：`output\demo_training\_contact_sheet_clean.png`
> 生成代码：`autismcare/illustrate.py`（本手册 = 该文件当前行为的说明书）

---

## 0. 一句话风格

**柔和、温暖、低刺激的儿童绘本插画**：奶油暖调背景、柔光逆光、圆润可爱的学龄前小朋友、粉扑腮红、平和微笑；**画面里绝不出现任何文字**（文字只由渲染层叠加，不烧进插画）。

---

## 1. 技术配置（硬参数，必须逐字复现）

| 项 | 值 | 说明 |
|---|---|---|
| 后端 | Pollinations.ai（免费、无需 key） | `AUTISMCARE_IMAGE=pollinations`（默认） |
| 模型 | **Flux** | URL 参数 `model=flux` |
| 尺寸 | **1024 × 768**（4:3 出图，渲染时裁成 16:9 卡片） | `width=1024&height=768` |
| **seed** | **4242**（固定） | 环境变量 `AUTISMCARE_IMAGE_SEED`，默认 4242。**换 seed = 换脸，务必保持 4242** |
| 其他 | `nologo=true` | 无水印 |

**请求 URL 形态：**
```
https://image.pollinations.ai/prompt/{urlencode(f"{画面描述}, {STYLE}")}?width=1024&height=768&model=flux&nologo=true&seed=4242
```

### 1.1 风格串 STYLE（逐字，注入每一条提示词末尾）
```text
children's picture book illustration, soft flat vector art,
gentle muted pastel palette, simple clean rounded shapes,
minimal calm background, warm cozy soft lighting, cute friendly characters,
sensory-friendly, wholesome, high quality, no text, no words, no letters
```
> 注：Flux 把这串"soft flat vector"解读成**柔和、带笔触质感的绘本画**（并非硬边扁平矢量），成片是温暖的手绘绘本感。**不要改这串**——之前改成"flat vector / gentle cartoon"会把脸压成古怪的圆眼卡通脸（用户明确不喜欢）。

### 1.2 提示词清洗器 `visual_prompt()`（防背景乱码，务必保留）
生成前对画面描述做清洗，**从根源避免 Flux 把字幕"照着写"进背景变乱码**：
- 删除所有引号/撇号字符 `" ' ` " " ' ' 『』「」《》`；
- 去掉会触发文字的对白动词：say / says / said / tell / ask / speak / talk / reads …；
- 丢弃问句部分（`?` 之后）；
- 清洗后词太少 → 退回安全通用场景 `a warm gentle scene of friendly young children`。

**红线：任何进入图像提示词的文本都不得含带引号的对白/句子。** 字幕、台词一律走渲染层叠加，绝不进插画提示词。

---

## 2. 调色板（Palette）

| 角色 | 色感 | 参考 |
|---|---|---|
| 背景主色 | 暖奶油 / 米白 | `#F5ECD8` 附近 |
| 辅助暖色 | 柔和蜜桃 / 杏色腮红 | `#F3C9A6` / 腮红 `#E8A87C` |
| 点缀冷色 | 低饱和鼠尾草绿（植物、卡片描边） | `#A7BFA6` |
| 光 | 金色柔光、窗口逆光 | 高光偏暖白 |

整体**低饱和、低对比、柔光**，无强烈色块、无高频细节、无刺眼白——符合感官友好原则。

---

## 3. 角色设定（Character Bible）

> ⚠️ **关于"人物复现"的诚实说明**：Flux + 固定 seed 只能锁**整体画风、氛围、构图倾向**，**不能逐帧锁定同一张脸**——不同提示词下五官/发型/衣服会有轻微漂移（对照总览图可见）。要让人物尽量一致，必须**每次都注入下面完全相同的角色关键词块**（别改措辞）。若将来要"同一角色严格复现"，需升级到支持角色参考图 / LoRA / img2img 的付费模型（见 §7）。

### 3.1 小明 —— 主角男孩（"我"）
- **年龄**：约 4–5 岁，学龄前。
- **头发**：短栗棕色，柔软微蓬，侧分刘海。
- **脸**：圆脸；两颊**粉扑圆形腮红**；小圆鼻（偶有几点小雀斑）；**弯月形笑眼**（多为眯眼笑）。
- **肤色**：温暖象牙白。
- **衣服**：柔软短袖 T 恤，**奶油米色**或**浅鼠尾草绿**，偶带细横条纹。
- **神情**：平和、温暖、满足。

**英文提示词块（每次原样复用）：**
```text
a gentle young preschool boy, short soft chestnut-brown hair with side-swept bangs,
round face, rosy pink cheeks, small nose, warm ivory skin, calm crescent smiling eyes,
soft cream short-sleeve t-shirt
```

### 3.2 小朋友 —— 同伴女孩
- **年龄**：约 4–5 岁。
- **头发**：暖棕色，侧刘海，扎**低侧马尾 / 小发髻**（有发圈）。
- **脸**：圆脸，粉腮红，温柔小微笑，弯月眼。
- **肤色**：温暖浅色。
- **衣服**：浅绿 / 米色细条纹短袖 T 恤。
- **神情**：友善、温和。

**英文提示词块（每次原样复用）：**
```text
a friendly young preschool girl, warm brown hair in a low side ponytail with side bangs,
round face, rosy cheeks, gentle small smile, warm light skin,
light sage-green striped short-sleeve t-shirt
```

### 3.3 共享玩具（道具）
一个**简单圆润的软玩具**：小汽车 / 彩色小鸟毛绒 / 小狗毛绒 / 小火车（随剧情）。保持**简单、圆润、低细节**，颜色不抢画面。
```text
a small simple rounded plush toy, soft colors
```

### 3.4 表情 / 动作 / 服装变体 —— 角色素材库
课内画面**同一节课保持**默认微笑+默认装（§3.1/3.2 的整块）；但角色的**身份**（发型/脸/肤色）
与**表情、动作、服装**已在 `cast.py` 拆开，可自由组合出同一角色的不同表情/换装 —— 用于情绪卡、
角色立绘、跨课换装等。数据即真源：
- `cast.IDENTITY`：身份（不含表情/服装）。
- `cast.OUTFITS`：每角色多套柔和配色服装（boy：default/stripe/hoodie/overalls；girl：default/dress/cardigan/overalls）。
- `cast.EXPRESSIONS`：8 种基础表情+轻动作（happy/calm/sad/surprised/thinking/proud/shy/excited，纯视觉无台词）。
- `cast.TOGETHER_ACTIONS`：同框互动（wave/play/comfort/share/think/laugh）。
- 组装器：`cast.portrait_prompt(char, expression, outfit, full_body=)` / `cast.together_prompt(action, ...)`。

**已生成的素材库**：`assets/characters/`（2026‑07‑14，28 张，seed 4242+序号、清洁中性背景）
- `xiaoming/`（小明 8 表情 + 3 换装）、`friend/`（女孩 8 表情 + 3 换装）、`together/`（6 种同框动作）
- 速览：`assets/characters/_sheet_{xiaoming,friend,together}.png`（带文件名标注）
- 重生成/扩充：`scratchpad/gen_assets.py`（免费 Pollinations，`gen_assets.py <序号...>` 可只重跑某几张）。

> 诚实局限同 §7：Flux 只锁"同一角色家族/画风",不锁逐张同脸；素材库是**供挑选/curate**的一批，
> 表情与身份都足够识别，但非像素级一致。要严格同脸需升级后端（角色参考图/LoRA/img2img）。

---

## 4. 场景 / 构图约定

- **环境**：温暖舒适的室内游戏角；大窗 + 薄纱白窗帘 + 金色柔光逆光。
- **点缀**：角落小盆栽、柔和装饰叶片；背景大面积留白（暖奶油墙）。
- **构图**：人物居中偏上，**下方约 1/3 留空**给渲染层的字幕卡片；单人特写用于"强化/鼓励"页，双人互动用于"示范/选择"页。
- **氛围**：安静、温馨、被支持感；无杂乱、无强透视、无夸张动作。

**场景英文关键词块：**
```text
cozy warm indoor playroom, large window with sheer white curtains, soft golden backlight,
small potted plants and soft foliage in the corners, plain warm cream background,
lots of empty space in the lower third, calm and quiet mood
```

---

## 5. 一页提示词的拼装公式（现由生成器自动完成）

```
[场景/动作纯视觉描述]  →  visual_prompt() 清洗（去引号/对白/问句）
                        +  [§3 角色关键词块]（cast.anchor_blocks 追加，不参与清洗，确保存活）
                        +  [§4 场景锚点]
                        +  ", " + STYLE(§1.1)（illustrate 追加）
                        ↑ seed = 4242
```
> 代码路径：`pipeline.emit` 取 `module.cast` → `cast.anchor_blocks(cast_name, with_others=not solo)`
> → `illustrate.illustration(img_desc, path, seed=4242, anchors=...)`。
> **互动页** `with_others=True`（主角+同伴）；**单人鼓励页** `solo=True`（只主角）。
> 新增角色 / 新阵容只改 `cast.py`；新题材在模块里改 `cast` 字段(`peer_play`/`solo_child`/`none`)。
示例（"轮到你说'等我一下'"这类含台词的页 → 清洗后）：
```
two young children sitting together with a small plush toy, one child waiting patiently,
+ 小明块 + 小朋友块 + 场景块, + STYLE     [seed=4242]
```

---

## 6. 复现检查清单（新视频出图前逐条核对）

- [ ] `seed = 4242`（没被环境变量改掉）
- [ ] STYLE 串**逐字**未改（§1.1）
- [ ] 每页都注入了 §3 角色关键词块（同一措辞，不即兴改写）
- [ ] 提示词已过 `visual_prompt()` 清洗；**无引号对白/台词/问句**进图
- [ ] 尺寸 1024×768、model=flux
- [ ] 出图后目检：**背景无乱码文字**、**表情自然**（非圆眼扁平卡通）、腮红+暖光在
- [ ] 台词/字幕只在渲染层叠加，**未烧进插画**
- [ ] **新图写入新文件夹，不覆盖任何原件**（用户长期铁律）
- [ ] **场景忠实**：每页画面贴合**该页文字**所述的具体场景/动作与出场角色（见 §6.1）
- [ ] **眼睛**：所有睁眼角色都有**清晰黑色瞳孔 + 可见眼白**、正常外貌（见 §6.2）；逐张查眼

### 6.1 场景忠实标准（用户要求 2026‑07‑15）

插画必须**画出该页文字所描述的具体场景**,而不是笼统的"主角+全阵容站在场景里"。
- 例:"看**墙上的步骤图**" → 画**贴满图卡的墙 + 男孩面对墙仰头细看**;
  "看**旁边的小朋友**怎么做" → 画**两个孩子、主角在看另一个小朋友做**。
- 机制:在模块 JSON 的 `page_visuals` 里**按页名**给出精确的 `visual_en`(该页画面英文描述)
  与 `roles`(该页出场角色键列表):`[]` 纯场景 / `["boy_ming"]` 单人 /
  `["boy_ming","peer_child"]` 主角+同伴 / `["boy_ming","teacher"]` 等。管线 `emit()` 命中即覆盖。
- 角色词表(`cast.CHARACTERS`):`boy_ming` 主角、`girl_friend` 同伴女孩、
  `peer_child` 通用同学(深发,与前两者区分)、`doctor` 医生、`teacher` 老师。
- 撰写 `visual_en` 注意:**别带引号台词/问号**(会被清洗器裁掉),用陈述句;
  别用 `read/say/ask/tell` 等词(清洗器会删),改用 `looking at a picture book / listening / watching`。

### 6.2 眼睛标准（用户要求 2026‑07‑15）

**每次生成都重点检查眼睛**:所有**睁眼**角色须有**清晰的黑色瞳孔 + 可见眼白**,符合正常人物外貌;
不得无神、无眼白、异形或只有一条缝(闭眼/眯眼仅在明确需要时——如冥想/深呼吸——由 `page_visuals` 指定)。
- 机制:`cast.EYES` 串写进每个角色块 + `illustrate.STYLE` 再全局强调一遍(双保险);
  角色默认表情由"闭眼月牙笑"改为**睁眼、黑瞳+眼白**。
- 出图后**逐张查眼**,不合标准的页按 §6.1 的 `page_visuals` 或重绘修掉。

---

## 7. 已知局限与升级路径

- **角色不能严格逐帧一致**：Flux+seed 只锁风格，不锁身份。当前靠"固定 seed + 固定角色关键词"把一致性做到**足够好**，但会有轻微漂移。
- **想要严格同一角色**（跨视频复现同一张脸）：需升级 `illustrate.py` 后端到支持
  ① 角色参考图 / IP‑Adapter，② LoRA 微调专属角色，③ img2img 以基准帧为参考。
  接口已隔离在 `illustrate.py` 单文件，替换后端不影响其余管线。
- **单主体复制**：单人题材里,若画面描述带"和朋友一起 / 分享玩具"之类**双人措辞**,
  Flux 会据此把主角**复制成两个孩子**。已双管齐下修进生成器:
  ① `pipeline` 按 `cast.has_others()` 给单人阵容改用"a single young child alone / by themselves"
  措辞(不再硬编码"with a friend and a toy");② `cast.anchor_blocks` 在**最终仅一个角色**时
  追加 `only one single child alone in the scene, no other people` 提示。双人题材(peer/医生/老师)不受影响。

---

## 8. 反面清单（别再犯）

| 别做 | 后果 |
|---|---|
| 改 STYLE 为 "flat vector / gentle cartoon" | 脸变古怪圆眼扁平卡通（用户明确不喜欢） |
| 换 seed | 换脸、风格漂移 |
| 把带引号的台词/字幕塞进图像提示词 | Flux 在背景"写字" → 乱码 |
| 加 "storybook cover / poster / title" 等词 | 诱导 Flux 生成文字/标题 |
| 覆盖 `scenes/`、`final.mp4` 等原件 | 违反铁律、可能丢数据 |
| 在成品插画页右上角画 "k / N" 页码 | 用户不要该数字(已在 `render.render_illustrated` 移除) |

---

## 变更记录
- **2026‑07‑14**：建档。锁定 `scenes_clean/`（19 张，用户"满意"）为基准；记录 STYLE / seed 4242 / 清洗器 / 双角色设定。
- **2026‑07‑14**：**接进生成器**。新增 `autismcare/cast.py`（角色/场景/阵容库）；`illustration()` 加 `anchors` 参数（清洗后追加、确保角色描述存活）；`TrainingModule` 加 `cast` 字段；`pipeline` 逐页自动注入（互动页整套阵容、单人页仅主角）。经 3 页实拍验证：同一男孩/女孩跨页复现、背景无乱码、表情自然。
- **2026‑07‑14**：**第 2 节课「轮流与等待」**用同阵容出片（`output/turn_taking/`），并给 `pipeline`/`cli` 加 `--scenes-only`（先审图、满意再合成）。
- **2026‑07‑14**：**角色素材库**（见 §3.4）。`cast.py` 拆出 `IDENTITY/OUTFITS/EXPRESSIONS/TOGETHER_ACTIONS` + `portrait_prompt/together_prompt`；生成 28 张表情/换装/同框素材到 `assets/characters/`。既有 `CHARACTERS/anchor_blocks` 一致性路径未改。
- **2026‑07‑14**：素材修订。按反馈重修 5 张（sad 翻白眼→垂眼、stripe 瞳孔加深、excited 多手→**拍手两手**、pair_comfort/pair_play 瞳孔清晰明亮）。根因修进生成器：`EXPRESSIONS["excited"]` 由"举双臂"改"拍手"（避免 Flux 画出多余的手）。旧图备份在 `assets/characters/_fixes/_superseded/`。
- **2026‑07‑15**：**批量出 5 节高区分度课程**(先出图审)。`cast.py` 新增大人角色(`doctor`/`teacher`)与场景锚点(安静角/游乐场/诊室/教室/浴室)+ 5 个阵容;5 节分别用 单人/双娃/带医生/带老师/单人 × 5 种场景拉开区分度。各 19 页,`output/{calm_breathing,joining_play,doctor_visit,group_directions,handwashing}/`。
- **2026‑07‑15**：**修单主体复制**(见 §7)。`cast.py` 加 `has_others()` + `anchor_blocks` 单人提示;`pipeline` 的练习/选择页画面描述改为按阵容区分单人/双人措辞。据此**只重绘**受影响页(calm_breathing 3 张练习提示;handwashing 3 提示+3 示范),其余缓存命中不重绘;旧图备份在各课 `_illus_superseded_dupe/`。
- **2026‑07‑15**：**两条新执行标准**(见 §6.1 场景忠实 / §6.2 眼睛)。生成器新增**逐页画面/角色覆盖**能力:`models.PageVisual` + `TrainingModule.page_visuals`;`cast.py` 加 `peer_child` 角色、`EYES` 串(全角色睁眼黑瞳+眼白)、`scene_of()`/`anchor_from_roles()`;`illustrate.STYLE` 全局加眼睛描述;`pipeline.emit()` 命中 `page_visuals` 即用其 `visual_en`/`roles`。先在 `group_directions` 落地验证(步骤/练习页忠实文字:墙面图卡+仰头看、看同伴做、一起收拾;眼睛达标),旧图备份 `_illus_pre_scenefix/`。
- **2026‑07‑15**：**逐页 seed 覆盖**(修畸形页而不动别页)。`PageVisual.seed` + `pipeline` 传入 `illustration(seed=…)`:固定 seed 4242 会复现同一张坏图,某页被 Flux 画出畸形眼/多手/脸瑕疵时,换 seed 重掷、挑干净的填进该页。据此修 `group_directions` 4 页:step3(右侧同伴眼)→6060、trial2_prompt(脸颊瑕疵)→11、trial3_prompt(右侧男孩眼)→1337、trial3_answer(众人眼)→777;旧图备份 `_illus_superseded_dupe/`。挑 seed 用 `scratchpad/seed_candidates.py`(每页多 seed 出候选→拼图目检)。
