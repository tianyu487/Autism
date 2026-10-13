# 互动游戏创意库(Idea Backlog)

> 用途:积累**新颖、有互动性**的小游戏创意,供生成器日后逐个实现。
> 现阶段**只积累创意,不生成产品**(遵循"停止产出产品·完善生成器")。
> 每个创意都锚定循证方法(EBP)与技能领域,并标注它消费哪些内容模型字段——
> 这样实现时"加一个游戏 = 加一个 JS 活动函数",不动知识层与生成层(三层架构继续生效)。

已实现(基线,见 `autismcare/game.py`):**听故事 story** · **排顺序 sequence** · **配一配 match**。
下面是候选新游戏。

> **当前累计:75 个创意(批次 1–6,#1–#75)**;详见各批次小结与文末统计。本库只积累创意、不生成产品。

---

## 0. 自闭症友好设计原则(所有新游戏硬性遵守)

1. **无惩罚 / 无计分 / 无计时 / 无竞争**——错了只给温和提示与重试,不扣分、不"游戏结束"。
2. **可预期、结构一致**——每个游戏布局、反馈方式固定;先示范("我先做")再邀请("轮到你")。
3. **低感官负荷**——柔和配色、少动画、无突兀音效;一屏一焦点。
4. **即时、具体、正向反馈**——针对刚才的行为("你把'先'放对了!"),非泛泛表扬。
5. **给选择与掌控感**——首页自选活动;可随时重来;节奏由孩子掌握。
6. **泛化钩子**——每个游戏结尾给一句"生活里可以这样用"的迁移提示(接 `visual_cards`/`review`)。
7. **循证可溯源**——每个游戏标注所训练技能 + EBP 方法 + 引用;产出仍是"需专业审核草稿"。
8. **内容驱动、优雅降级**——玩法出现与否由模块内容自动决定;内容不足则该玩法不出现,不报错。

---

## 1. 情绪认知与调节(emotional_regulation)

### 1.1 情绪温度计 Emotion Thermometer
- **训练**:情绪强度分级(情绪不是"有/无"而是有程度)· CBT/CBIS · 视觉支持(5分量表)
- **机制**:给一个情境卡,孩子拖动"温度计/滑块"把情绪强度调到匹配位置;不同强度对应不同应对建议(1-2 平静、3 提醒、4-5 用平静策略)。
- **消费字段**:需新增轻量内容——`emotion_scale`(情绪词×强度×身体信号×策略)。可由 `emotion_library.yaml` 供给。
- **新颖/互动**:连续滑动而非点选;"量表"本身是循证工具(Incredible 5-Point Scale / Zones of Regulation)。
- **渲染工作量**:中(滑块组件 + 分级反馈)。
- **依赖**:`emotion_library.yaml`(子agent正在建)。

### 1.2 平静工具箱 Calm-Down Toolbox
- **训练**:情绪调节策略 · CBT/CBIS · 自我管理
- **机制**:孩子从"工具箱"里挑一个策略卡(深呼吸/数到十/挤压/喝水/找大人),点开后**动画演示并带孩子做一遍**(如呼吸球随节奏胀缩 4-7-8)。
- **消费字段**:`visual_cards(kind=strategy/reminder)`;呼吸动画为内置组件。
- **新颖/互动**:呼吸引导动画=真正"边玩边练"的调节练习,不只是看。
- **渲染工作量**:中(呼吸动画 SVG/CSS 循环 + 策略卡网格)。

### 1.3 看脸识情绪 Read the Face
- **训练**:表情/情绪识别 · DTT/社交技能训练 · 视觉支持
- **机制**:出示一张人脸插画(或情境),孩子从 2-4 个情绪词里点匹配的;逐步加难度(基础4情绪→复合情绪)。
- **消费字段**:`visual_cards(kind=emotion)` + `emotion_library` 分级词表。
- **新颖/互动**:比 match 更聚焦——单目标、带渐进难度与"为什么"(点开看身体线索)。
- **渲染工作量**:低(复用 match 的点选骨架 + 人脸插画)。

### 1.4 身体侦探 Body Detective(内感受 Interoception)
- **训练**:识别情绪的身体信号(心跳快、脸发烫→可能是生气/紧张)· CBT · 自我管理
- **机制**:三段连线——**身体信号 → 情绪 → 该用的策略**;孩子依次点亮一条链。
- **消费字段**:`emotion_library`(body_signals + emotion + strategy 三元组)。
- **新颖/互动**:教"早期预警信号",是自我调节的关键前技能,市面少见。
- **渲染工作量**:中(三列连线交互)。

### 1.5 心情签到 Mood Check-In
- **训练**:情绪自我监控 · 自我管理 · CBT
- **机制**:孩子每天点"我现在感觉…"(表情阵列),可选再点一个"我可以做…"的策略;无对错,纯自我觉察,可重复。
- **消费字段**:`emotion_library` 表情阵列 + 策略;可选记录到 localStorage。
- **新颖/互动**:**可重复、个人化**的日常小工具(不是一次性关卡);培养情绪词汇与自我觉察。
- **渲染工作量**:低-中。

---

## 2. 社交互动(social_interaction)

### 2.1 社交侦探 Social Detective
- **训练**:观点采择 / 心理理论("他在想什么?")· 社交技能训练 · CBT
- **机制**:四格连环画情境,问"他现在**感觉/想**什么?",孩子选;选后**思维泡泡揭晓**并解释线索。
- **消费字段**:`social_choice`(把 options 复用为"他的想法"猜测 + outcome 作揭晓解释)。
- **新颖/互动**:思维泡泡揭晓动画;直击自闭症核心难点(推测他人心理)。
- **渲染工作量**:中(连环画 + 泡泡揭晓)。

### 2.2 对话搭桥 Conversation Bridge
- **训练**:对话轮流、回应、开启/维持话题 · 社交技能训练 · 脚本教学
- **机制**:一段对话逐句展开,轮到孩子时从 2-3 个回应里选合适的一句,选后对话继续"搭桥"往前;搭到终点=一段完整对话。
- **消费字段**:需新增 `dialogue_turns`(speaker + 候选回应 + 各自走向);或用多个 `social_choice` 串接。
- **新颖/互动**:对话像搭积木一样"长出来",可视化"我的一句让对话继续"。
- **渲染工作量**:中-高(对话状态机)。

### 2.3 轮到谁 Whose Turn?
- **训练**:轮流与等待 · 视频示范 · 社交叙事
- **机制**:简单来回互动(滚球/搭一块/你一句我一句),清晰的"轮次指示灯"在"你/我"间切换;等待时有温和的"等一等"视觉提示。
- **消费字段**:复用 `steps` 或轻量轮流脚本。
- **新颖/互动**:把抽象的"等待/轮流"变成可见的灯与节奏;等待被正向框架化。
- **渲染工作量**:低-中。

### 2.4 一起搭 Build Together
- **训练**:合作游戏(平行→联合→合作)· 同伴中介 · 视频示范
- **机制**:一个共同目标(搭塔/拼图),"我先放一块→轮到你放一块",合力完成后一起庆祝;强调分工与共同目标。
- **消费字段**:`steps`(拆成"你一块我一块"的合作序列)。
- **新颖/互动**:合作而非单人闯关;示范"一起达成"的正向社交体验。
- **渲染工作量**:中。

### 2.5 找一找·跟着指 Find & Point
- **训练**:共同注意、跟随他人指向/视线 · 自然情境干预
- **机制**:插画场景里"看,那边有…",顺着一个大手指/箭头找到并点亮目标物;找到后可"指给大人看"。
- **消费字段**:场景插画 + 目标物(可用 `visual_keyword`/新增 targets 列表)。
- **新颖/互动**:找物+跟随指向,训练最早、最难的共同注意;轻扫视交互。
- **渲染工作量**:中(场景热区)。

---

## 3. 沟通语言(communication_language)

### 3.1 我想要 I Want(图片组句)
- **训练**:功能性请求、图片交换沟通(PECS)· AAC/PECS
- **机制**:底部"句条","我要"固定 + 孩子从图片库拖一张需求图拼成"我要 ___",完成后播报整句并给出被理解的正向结果。
- **消费字段**:`aac_pecs` 内容 + 图片库(icon/visual_cards);需新增 `sentence_strip` 轻模型。
- **新颖/互动**:数字版 PECS 句条,直接对应真实沟通板;"表达→被理解"的即时正反馈。
- **渲染工作量**:中(拖拽组句 + 播报)。

---

## 4. 生活自理与行为(daily_living_behavior)

### 4.1 我的一天 My Day(视觉日程)
- **训练**:日常流程、过渡转换、"先—然后" · 视觉支持(TEACCH 日程)· 任务分析
- **机制**:把活动卡拖到时间轴/"先→然后→最后"格子里排好一天;做完一项打勾;支持"下一个是什么"预告。
- **消费字段**:`steps`(作为日程项)+ `visual_cards(kind=schedule)`。
- **新颖/互动**:真实 TEACCH 视觉日程的互动版;打勾+预告降低过渡焦虑。
- **渲染工作量**:中(时间轴拖放 + 勾选状态)。

### 4.2 如果…怎么办 What If?(问题解决)
- **训练**:灵活思维、应对意外、问题解决 · CBT · 社交叙事
- **机制**:抛一个小问题(玩具坏了/朋友说不行/计划变了),孩子从几种应对里选,选后看到**平和的结果**与"还可以怎么办";强调"办法不止一个"。
- **消费字段**:`social_choice`(options=应对方式,outcome=平和结果)。
- **新颖/互动**:训练灵活性与情绪应对;"多种解法"对抗刻板。
- **渲染工作量**:低(复用 story 的选择分支)。

---

## 5. 通用 / 注意力

### 5.1 记忆翻翻乐 Memory Flip
- **训练**:注意、视觉记忆、情绪/词汇配对 · 视觉支持
- **机制**:经典翻牌配对,但**无计时、无步数惩罚、无限翻**;可选 图↔图 / 图↔词 / 情绪↔情境 配对。
- **消费字段**:`visual_cards` / `steps` / `emotion_library` 生成成对卡。
- **新颖/互动**:熟悉的翻牌机制 + 感官友好改造;翻牌动画有掌控感。
- **渲染工作量**:低-中(复用 match 数据 + 翻牌动画)。

---

## 6. 内容模型影响一览(实现时需要的新字段/资源)

| 游戏 | 复用现有字段 | 需新增 |
|---|---|---|
| 情绪温度计 / 身体侦探 / 心情签到 / 平静工具箱 / 看脸识情绪 | visual_cards | `emotion_library.yaml`(情绪×强度×身体信号×策略);可选 `EmotionScale` 轻模型 |
| 社交侦探 / 如果…怎么办 | social_choice | 无(直接复用) |
| 对话搭桥 | social_choice(串接) | `DialogueTurn` 轻模型(更佳) |
| 轮到谁 / 一起搭 / 我的一天 | steps | `kind=schedule` 卡 / 轮流脚本(可选) |
| 找一找 | visual_keyword | 场景目标物列表(轻) |
| 我想要 | aac_pecs 内容、icon | `SentenceStrip` 轻模型 + 图片库 |
| 记忆翻翻乐 | visual_cards / steps | 无 |

**结论**:一半以上创意**零内容-模型改动**即可实现(纯新增 JS 活动函数);情绪类若干共享一个 `emotion_library` 知识资源(子agent正在建),一次投入多个游戏受益。

---

## 7. 建议优先级(实现时参考)

**第一批(高价值 · 低改动 · 复用现有内容)**
1. 如果…怎么办 What If?(复用 social_choice,补灵活性训练空白)
2. 社交侦探 Social Detective(复用 social_choice,直击心理理论)
3. 记忆翻翻乐 Memory Flip(复用 match 数据,加翻牌)
4. 我的一天 My Day 视觉日程(复用 steps,TEACCH 高实用)

**第二批(需 `emotion_library`,一次投入多游戏受益)**
5. 看脸识情绪 → 情绪温度计 → 平静工具箱 → 心情签到 → 身体侦探

**第三批(需新轻模型)**
6. 对话搭桥(DialogueTurn) · 我想要(SentenceStrip) · 轮到谁/一起搭/找一找

---

## 8. 第二批创意(2026-07-13,结合新增技能域)

知识库已扩到 12 技能域,解锁一批新玩法。仍**只积累不生成**。

### 安全 · 社区(safety_skills / community_participation)
- **15. 安全过马路 Safe Crossing** — 交通安全。等红灯变绿→点"看左看右"→再点过街;抢步只给温和"再等一等",不惩罚。消费 `safety_skills.road_traffic` 步骤。真实预演的低风险版本。
- **16. 这样安全吗?Safe or Not?** — 安全判断。出示情境图,点"安全/要小心",点开看原因。消费 safety 各区(social_choice 式)。
- **17. 走失了怎么办 Lost & Found** — 走失求助。分支:停在原地→找穿制服的人/带孩子的家长→说出名字电话。消费 `getting_help_lost`。喂 `bergstrom_2012` 证据。
- **18. 小小购物 Little Shopper** — 购物+钱币。照图片清单取货→到收银台→用"进一元"付款。跨 `community.shopping` + `functional_academics.money`。
- **19. 点餐吧 Order Please** — 外出就餐。指认点餐→等待→结账。消费 `dining_out`。
- **20. 谁能帮我 Who Can Help?** — 识别帮助者。需求↔合适的人(医生/警察/店员)配对。消费 `community_helpers_help`。

### 生活数学(functional_academics)
- **21. 数一数买几个 Count & Buy** — 功能性数数。按要求数出 N 个。消费 `functional_counting`。
- **22. 几点做什么 What Time?** — 认时钟+日程。时钟↔活动配对。消费 `time_clock`/`schedule_reading`。
- **23. 凑钱付款 Pay It** — 钱币。拖硬币凑到价格("进一元"策略)。消费 `money_skills`。

### 认知灵活(cognitive_flexibility)
- **24. 换个办法 Another Way** — 灵活生成。一个问题,尽量想出多个办法("还有别的吗?"),每个都被肯定。消费 `flexible_thinking`+`problem_solving`。比"如果…怎么办"更聚焦"多解"。
- **25. 换规则分一分 Switch & Sort** — 定势转换(set-shifting)。先按颜色分,中途"现在改成按形状分"。消费新的 set-shifting 目标。新颖点:规则中途切换,直击刻板。

### 运动 · 感觉调节(motor_sensory)
- **26. 跟我做 Copy Me** — 动作模仿/律动。看一个动作→镜像动画带做→点"我做到了"(无需摄像头)。消费 `motor_imitation`。
- **27. 呼吸小星球 Breathing Planet** — 感觉性自我调节。呼吸引导动画(4-7-8),星球随呼吸胀缩。与"平静工具箱"同源、可独立成小工具。

### 职业前(prevocational)
- **28. 小小分拣员 Sorter** — 功能性作业+任务完成。把物品按类别拖进对应箱,做完出现"完成✓"。消费 `functional_work_tasks`+`task_completion`。喂 `van_laarhoven_2010`/`allen_2010` 的视频提示思路。
- **29. 工作板 Work Board** — TEACCH 工作系统。"做什么→做多少→怎样算完成→接下来"的可视化流程走一遍。消费 `work_routines`;呼应 `hume_odom_2007`。

### 观点采择(social_interaction.perspective_taking)
- **30. 他想的和我一样吗?Same Mind?** — 心理理论/错误信念。经典 Sally-Anne 式:东西被移动了,"他会去哪里找?"思维泡泡揭晓。消费 `perspective_taking`。喂 `baron_cohen_1985`/`howlin_1999`。是"社交侦探"的错误信念专项版。

### 第二批内容模型影响
| 玩法 | 复用字段 | 需新增 |
|---|---|---|
| Safe Crossing / Sorter / Copy Me / Switch&Sort | steps | 无(排序/点选类可复用) |
| Safe or Not? / Lost&Found / Another Way / Same Mind? | social_choice | 无 |
| Little Shopper / Pay It / Count&Buy / What Time? | — | 轻量 `MoneyItem`/`ClockItem`(生活数学专用) |
| Order Please / Who Can Help? | steps / social_choice | 无 |
| Breathing Planet | — | 内置呼吸动画组件(与平静工具箱共用) |
| Work Board | steps | `kind=schedule` 卡 |

**再次印证**:绝大多数新玩法仍是"加一个 JS 活动函数"即可;生活数学四款共享一个轻量数字组件,一次投入多游戏受益(与情绪类共享 `emotion_library` 同理)。

---

## 9. 第三批创意(生活自理 · 运动 · 沟通)

配合 daily_living / motor_sensory 深化,补一批"分步照做型"与"沟通型"玩法。仍只积累不生成。

### 生活自理(daily_living_behavior)—— 任务分析步骤类
- **31. 穿衣顺序 Get Dressed** — 穿衣。把衣物按"先内后外、先上后下"拖到小人身上;顺序对才穿上,错了温和提示。消费 `self_care` 步骤。呼应 `van_laarhoven_2010` 视频提示。
- **32. 刷牙泡泡 Brush Time** — 刷牙。跟着分步动画刷(上/下/内/外),无计时压力,刷到每区亮一下。消费 `self_care` 卫生步骤。
- **33. 洗手七步 Wash Hands** — 洗手。七步顺序排/照做,泡泡动画反馈。消费 `self_care`。分步序列(复用 sequence 骨架)。

### 运动(motor_sensory)
- **34. 平衡小径 Balance Path** — 大肌肉/身体觉知。跟着屏幕节奏点"左脚/右脚/跳",镜像动画带做,点"我做到了"。消费 `gross_motor`/`body_awareness`。无摄像头、无计分。
- **35. 描一描 Trace It** — 精细动作。用手指沿虚线描出形状/字;偏离给柔和引导回正轨。消费 `fine_motor`。触屏描画,天然互动。

### 沟通(communication_language)
- **36. 打招呼 Say Hi** — 问候/告别。不同情境(见老师/见同学/离开)选合适的一句;选后对方微笑回应。消费 `conversation` 问候目标。
- **37. 问一问 Ask Me** — 提问。看图选合适的问题(这是什么/在哪里/是谁),问对了揭晓答案。消费 `conversation` 提问目标。

### 情绪表达(emotional_regulation)
- **38. 表情镜子 Feelings Mirror** — 情绪表达/模仿。屏幕给一个情绪,孩子"做出这个表情"(镜像卡通同步),做完点确认;把命名情绪与表情联系起来。消费 `emotion_expression` + `emotion_library`。新颖:做表情而非只识别。

### 第三批内容模型影响
| 玩法 | 复用字段 | 需新增 |
|---|---|---|
| Get Dressed / Wash Hands / Brush Time / Balance Path | steps(任务分析) | 无(sequence/照做骨架复用) |
| Say Hi / Ask Me | social_choice / conversation 目标 | 无 |
| Trace It | — | 轻量描画组件(触屏路径) |
| Feelings Mirror | emotion_library | 镜像表情动画组件 |

**累计**:游戏创意已达 **38 个**,覆盖全部 12 技能域。多数仍"加一个 JS 活动函数"即可;"分步照做型"(穿衣/洗手/刷牙/平衡)全部复用 sequence 骨架,是**投入产出比最高的一类**。

---

## 10. 第四批创意(2026-07-14,补齐两块零覆盖域 + 深化浅覆盖 skill_area)

前三批已触及 12 个技能域,但校对发现**两个域尚无任何玩法**——入学与课堂准备(school_readiness)、游戏与休闲(play_leisure);另有若干 skill_area 仅浅覆盖。本批 12 款专攻这些缺口,仍**只积累不生成**,全部硬性遵守第 0 节 8 条原则(无惩罚/可预期/低感官/具体正反馈/给选择/泛化钩子/循证可溯源/优雅降级)。

### 入学与课堂准备(school_readiness)—— 此前零覆盖

#### 39 举手等一等 Raise Hand & Wait
- **训练**:集体中的等待与轮流(先举手、等被叫到再说)· 自我管理 · 视觉支持
- **机制**:圆圈时间老师问全班一个问题,孩子心里冒出"想说"的泡泡;点"举手"→手举起、旁边亮起柔和的"等待中"灯→老师叫到名字再点"说出答案"揭晓。若先点"喊出来",温和提示"先举手,老师就能看到你"并可重来(无惩罚)。
- **消费字段**:`steps`(waiting_turn_taking 目标拆成 举手→等待→被叫→回答)+ `visual_cards`;可选把"举手成功"记入 localStorage 供自我觉察(不计分)。
- **新颖/互动**:把"举手—等待"这条看不见的课堂规则做成可见的灯与节奏,并把冲动暂停和轮流合在一起练;区别于"轮到谁"(那是双人来回,这是面向全班的举手等待)。
- **渲染工作量**:低-中(等待灯 + 举手动画,复用点选骨架)。
- **依赖**:`skills/school_readiness.yaml → skill_area: waiting_turn_taking`;方法 `visual_supports` / `self_management` / `reinforcement`;引用 `steinbrenner_2020`、`nac_2015`。

#### 40 一起做·听全班口令 Follow-the-Class Cue
- **训练**:遵循面向全班的集体指令(非 1 对 1)· 同伴中介 · 视觉支持
- **机制**:一屏卡通同学(2-3 个)坐成一排,老师发出 1-2 步集体指令("拿出书、坐好");孩子点着做每一步,做对时**同学们也跟着一起做**(同伴示范揭晓),出现"你和大家一起做到了"。做错温和重放指令。
- **消费字段**:`steps`(following_group_instructions 目标)+ `visual_cards`;同伴示范为内置轻动画。
- **新颖/互动**:专门训练"面向全班"的指令响应(1 对 1 会做 ≠ 全班会做),并用同伴一起做的画面把集体感可视化;同伴中介以动画替代真人。
- **渲染工作量**:中(同伴同步动画)。
- **依赖**:`skills/school_readiness.yaml → skill_area: following_group_instructions`;方法 `visual_supports` / `peer_based_intervention` / `modeling`;引用 `steinbrenner_2020`、`nac_2015`。

### 游戏与休闲(play_leisure)—— 此前零覆盖

#### 41 假装小厨房 Pretend Kitchen
- **训练**:象征/假装游戏——串联假装动作 + 物品替代 · 示范 / 自然情境干预
- **机制**:一个假装厨房场景;先示范"我先假装倒水→搅拌→喝",再"轮到你",孩子按顺序拖动作卡串成一小段假装情节;进阶给"物品替代"——把积木拖来"当"电话/勺子,系统认可"这个可以当作…"。
- **消费字段**:`steps`(假装动作序列)+ `visual_cards`(可替代物品);无需新字段。
- **新颖/互动**:市面少见把"象征游戏"游戏化——教串联假装与物品替代(自闭症自发象征游戏偏少的核心难点),而非又一个配对;"我先假装/轮到你"的示范-邀请结构天然合规。
- **渲染工作量**:中(拖放 + 物品替代确认)。
- **依赖**:`skills/play_leisure.yaml → skill_area: symbolic_play`;方法 `modeling` / `video_modeling` / `naturalistic_intervention`(如需可提 `jasper`);引用 `westby_1980`、`piaget_1962`、`lifter_1993`。

#### 42 加入一起玩 Can I Play?
- **训练**:加入正在进行的集体游戏,并温和应对被拒绝 · 社交技能训练 / 同伴中介
- **机制**:同伴在玩的场景;孩子按"先观察→问'我可以一起玩吗?'"分步选择;分支揭晓——被欢迎加入,或温和的"这次不行",此时再从"找别的同伴/换个游戏/先看一会儿"里选一个平和的备选。全程无惩罚,强调"被拒绝也没关系"。
- **消费字段**:`social_choice`(options=加入方式与被拒后的备选,outcome=平和结果)+ `scenarios`;无需新字段。
- **新颖/互动**:把"加入游戏 + 接受被拒"这条又难又真实的完整链条做成分支选择,补齐灵活性与社交的交叉空白;区别于"社交侦探"(猜想法)与"一起搭"(已在一起)。
- **渲染工作量**:低-中(复用 story/social_choice 分支)。
- **依赖**:`skills/play_leisure.yaml → skill_area: play_flexibility`,并接 `skills/social_interaction.yaml → friendship_group`;方法 `social_skills_training` / `peer_based_intervention` / `cognitive_behavioral`;引用 `gates_2017`、`nac_2015`。

### 安全技能(safety_skills)—— 深化 water/body/emergency

#### 43 泳池边先停一停 Stop at the Water's Edge
- **训练**:水与泳池安全——靠近水先停、穿好浮具、听"上来"就离水 · 视频示范 / 视觉支持
- **机制**:泳池/河边场景;孩子须先点"停下、等大人"→给小人"穿好救生衣/浮圈"→大人点头后才"靠近";若先点水面,温和提示"先等大人、先穿好救生衣"。再练"大人说'上来'→立刻点'离水'"。
- **消费字段**:`steps`(water_safety 目标序列)+ `visual_cards`;无需新字段。
- **新颖/互动**:把高风险的水边规则做成零风险预演;明确这是监护的补充、绝不替代大人在场。
- **渲染工作量**:中(场景 + 穿浮具/离水动画)。
- **依赖**:`skills/safety_skills.yaml → skill_area: water_safety`;方法 `video_modeling` / `visual_supports` / `social_narratives`;通用框架引用 `miltenberger_2008`(安全技能 BST)。**TODO_CITATION**:泳池/防溺水安全技能的专项实证(citations.yaml 暂无对应条目,与 water_safety 域内既有标注一致,勿臆造)。

#### 44 身体安全:可以吗? Body Safety: Is This Okay?
- **训练**:身体界限与自我保护——分辨舒服/不舒服的接触、会说"不"并告诉信任的大人 · 社交叙事 / 视频示范
- **机制**:出示接触/亲近的情境卡,孩子拖到"可以(如击掌、家人拥抱)"或"我可以说不(不舒服的接触)"两个筐;点开揭晓该怎么做——"说不→走开→告诉信任的大人",并复习"我的信任大人"是谁。语气平静、赋能、非恐吓。
- **消费字段**:`social_choice` 或 `scenarios`(接触情境 + 恰当反应)+ `visual_cards`;无需新字段。
- **新颖/互动**:少见而关键的身体自主/同意主题,用"可以/说不"的温和分类替代恐吓式教育;揭晓的是可执行的三步反应。
- **渲染工作量**:低-中(拖放分类 + 揭晓)。
- **依赖**:`skills/safety_skills.yaml → skill_area: body_safety`;方法 `social_narratives` / `video_modeling` / `modeling`;引用 `miltenberger_2008`、`gray_garand_1993`。此敏感主题须专业人员与家长把关。

#### 45 火警疏散小路 Fire-Drill Path
- **训练**:紧急情况基础——识别警报、跟随疏散、"停—趴—滚" · 视频示范 / 任务分析
- **机制**:警报以**柔和闪烁的视觉提示 + 文字**呈现(不用突兀巨响,守低感官原则),孩子按序走完:停下→跟着大人/排队→走绿色安全出口→到集合点;附一段"身上着火:停—趴—滚"的动作序列。"绝不躲柜子/床下"由揭晓强化。
- **消费字段**:`steps`(emergency_basics 目标)+ `visual_cards`(出口/集合点标志);无需新字段。
- **新颖/互动**:把逃生流程与"停趴滚"做成有序小路径演练;特意用视觉警报替代刺耳音效,兼顾安全教育与低感官原则。
- **渲染工作量**:中(路径 + 序列动画)。
- **依赖**:`skills/safety_skills.yaml → skill_area: emergency_basics`;方法 `video_modeling` / `task_analysis` / `visual_supports`;引用 `steinbrenner_2020`、`nac_2015`。

### 职业前(prevocational)—— 深化 tool_material_care/help_and_feedback

#### 46 物归原位 Everything Home
- **训练**:工具与材料管理——取用→归位→清整的闭环 · 任务分析 / 视频示范
- **机制**:完成一件作业后,把每件工具拖回它的**轮廓/影子位**(形状配位),全部归位后出现"桌面整洁 ✓";可先看一步一停的视频提示示范。
- **消费字段**:`steps`(tool_material_care 目标)+ `visual_cards`(工具轮廓位);无需新字段。
- **新颖/互动**:用"影子配位"把 TEACCH 的物理结构游戏化,教常被忽视的"用完归位"工作习惯;是可迁移的独立工作行为。
- **渲染工作量**:低-中(轮廓拖放配位)。
- **依赖**:`skills/prevocational.yaml → skill_area: tool_material_care`;方法 `task_analysis` / `video_modeling` / `visual_supports`;引用 `van_laarhoven_2010`、`hume_odom_2007`。

#### 47 卡住了就求助 Stuck? Ask for Help
- **训练**:寻求帮助与接受反馈——卡住时求助、据反馈修改 · 时间延迟 / 示范
- **机制**:做一件多步作业,到"卡住"点弹出选择:发脾气/放弃 · 举"我需要帮助"卡 · 自己再试一次;选求助→看一次示范→改好继续。再练"接受温和纠正('这里再对齐一点')→修改"。全程无惩罚,把求助正向框架化。
- **消费字段**:`social_choice`(卡住时的选择 + 结果)+ `steps`;无需新字段。
- **新颖/互动**:在"困难当下"给出功能性沟通替代(求助代替挫败),并练"接受反馈"这一就业关键软技能;区别于"如果…怎么办"(泛化问题解决)。
- **渲染工作量**:低-中(复用 social_choice + 示范回放)。
- **依赖**:`skills/prevocational.yaml → skill_area: help_and_feedback`;方法 `time_delay` / `modeling` / `video_modeling` / `reinforcement`;引用 `steinbrenner_2020`、`lee_2007`。

### 功能性学业 · 生活数学(functional_academics)—— 深化 measurement/number

#### 48 倒到这条线 Fill to the Line
- **训练**:功能性测量——按刻度线取量、比较多/少 · 视频示范 / 视觉支持
- **机制**:拖动/倾斜把水或米倒进量杯到标好的线("倒到 1 杯");倒够即停并给"正好到线了"的具体反馈;另有"点更多的那一杯"比较小关。无计时。
- **消费字段**:复用第二批已提出的"生活数学轻量数字组件",扩一个极小的 `measure_item`(容器 + 目标刻度线);其余复用 `visual_cards`。
- **新颖/互动**:把抽象测量换成"倒到线"的生活化连续交互,直接对应做饭/取药量;与"凑钱付款/认时钟"共享同一套生活数学轻组件,一次投入多游戏受益。
- **渲染工作量**:中(倾倒/液面动画 + 刻度判定)。
- **依赖**:`skills/functional_academics.yaml → skill_area: measurement_basics`;方法 `video_modeling` / `visual_supports` / `task_analysis`;引用 `steinbrenner_2020`、`cn_peizhi_2016`。

#### 49 生活里的数字 Numbers Around Me
- **训练**:生活数字认读——在真实场景中找到并认读数字 · 自然情境 / 视觉支持
- **机制**:给一个生活场景(电梯按钮墙/公交车/门牌/价签),"找到写着 5 的按钮"——在场景里点中目标数字;进阶到数字串(找"302 路"、认自家门牌)。找到即放大揭晓并读出。
- **消费字段**:`scenarios`/`visual_cards`(生活场景)+ 轻量"场景数字目标"列表(与"找一找·跟着指"的 targets 同构,可复用其结构)。
- **新颖/互动**:把认数字从闪卡搬进真实情境热区,直击"日常用得上"的功能取向;点中即读、场景化泛化。
- **渲染工作量**:中(场景热区 + 目标数字)。
- **依赖**:`skills/functional_academics.yaml → skill_area: number_recognition`;方法 `naturalistic_intervention` / `visual_supports` / `discrete_trial_training`;引用 `steinbrenner_2020`、`nac_2015`。

### 认知灵活(cognitive_flexibility)—— 深化 self_monitoring

#### 50 停一停,想一想 Pause & Think
- **训练**:冲动暂停——停一停→想一想→再行动,并自我监控 · 自我管理 / 认知行为策略
- **机制**:遇到冲动情境(想抢玩具/想冲出去)时先出现大大的"停",孩子点"停"暂停;再展开"想一想"的 2-3 个办法,选一个,才"行动";结束给一个"今天我停下来了 __ 次"的自我觉察小勾(纯记录、不计分)。
- **消费字段**:`social_choice`(想一想的选项)+ `scenarios`;可选把"停下来"次数记 localStorage 供自我觉察。
- **新颖/互动**:把"停—想—做"这条抽象自控链做成看得见、可自我记录的按钮流程,分开冲动与反应;可重复的个人化小工具,而非一次性关卡。
- **渲染工作量**:低-中(停止按钮 + 选项 + 自记小勾)。
- **依赖**:`skills/cognitive_flexibility.yaml → skill_area: self_monitoring`;方法 `self_management` / `cognitive_behavioral` / `visual_supports`;引用 `lee_2007`、`wood_2009`。

### 第四批内容模型影响
| 玩法 | 复用字段 | 需新增 |
|---|---|---|
| 举手等一等 / 一起做 / 假装小厨房 / 泳池边 / 火警疏散 / 物归原位 | steps + visual_cards | 无(排序/照做/拖放骨架复用) |
| 加入一起玩 / 身体安全 / 卡住了就求助 / 停一停想一想 | social_choice / scenarios | 无 |
| 生活里的数字 | scenarios / visual_cards | 轻量"场景数字目标"列表(与"找一找"targets 同构) |
| 倒到这条线 | 生活数学轻组件(与凑钱/认时钟共用) | 极小 `measure_item`(容器 + 目标刻度线) |

**累计**:游戏创意达 **50 个**;本批补齐先前**零覆盖的两个技能域**(school_readiness、play_leisure),并深化 safety_skills(水/身体/紧急)、prevocational(工具管理/求助反馈)、functional_academics(测量/生活数字)、cognitive_flexibility(自我监控)。绝大多数仍"加一个 JS 活动函数"即可;仅"倒到这条线"需给生活数学轻组件加一个极小刻度扩展,与已有生活数学玩法共享。**校对留意**:泳池安全缺"水安全专项实证"(见 #43 的 TODO_CITATION),其余均锚定 citations.yaml 现有真实引用。

---

## 11. 第五批创意(2026-07-14)

**仍只积累创意,不生成产品**(遵循"停止产出产品·完善生成器")。本批分两组共 14 款(#51–#64),全部硬性遵守第 0 节 8 条原则。经**逐条点数** #1–#50,最薄的 5 个域为:play_leisure(2)、school_readiness(2)、communication_language(3)、community_participation(3)、cognitive_flexibility(3)(注:任务提示所猜的 emotional_regulation/social_interaction 实为最厚,各 6;community_participation 实为 3 而非 ≈1——已按实读修正)。
- **Group A(#51–57)**:深化上述最薄的 5 个域,每款锚定一个此前**未被玩法覆盖的 skill_area**。
- **Group B(#58–64)**:机制主导——每款主打一个**此前全库未出现的交互机制**,仍锚定真实 skill_area + method_id。

### Group A — 深化最薄的域

#### 51 一起玩有规则的游戏 Play by the Rules
- **训练**:遵守规则的简单游戏、接受输赢 · `social_skills_training`/`video_modeling` · 视觉支持
- **机制**:一局极简的有规则小游戏(骰子走 3–5 格 / 简版"抢座位");先"我先玩一轮"示范规则,再"轮到你";结束时无论输赢都出现温和的"这一局 __ 赢了,我们再玩一局好吗?",把"输"正向框架化——不闪红、不"游戏结束"、可立即再来。
- **消费字段**:复用 `steps`(把规则拆成"投骰→数格→停")+ 轻量"规则局"脚本;无需新字段。
- **新颖/互动**:补齐 play_leisure 里"有规则的游戏/接受输赢"这一 skill_area(此前 41/42 只覆盖象征游戏与游戏灵活性);把"遵守规则 + 接受输"这条真实又难的社交游戏能力做成零惩罚的一局。
- **渲染工作量**:中(走格/回合状态机 + 温和结算)。
- **依赖**:`skills/play_leisure.yaml → skill_area: games_with_rules`;方法 `social_narratives`/`video_modeling`/`social_skills_training`/`peer_based_intervention`;引用 `chan_2009`、`nac_2015`。

#### 52 我的休闲我来选 My Leisure, My Choice
- **训练**:独立休闲——从选项中自选并恰当玩一段 · `self_management`/`visual_supports` · 视觉支持
- **机制**:一块"休闲选择板"列 3–5 个已会的活动(听音乐/看绘本/拼插/涂色),孩子自选一项,配一个柔和的可视时长条(沙漏式,非倒计时压力);玩完可打个"我玩过了"的勾或再选一项。纯自主、无对错。
- **消费字段**:`visual_cards`(活动卡)+ 可选 localStorage 记录"我选过什么"(自我觉察,不计分);无需新字段。
- **新颖/互动**:补齐 play_leisure 的"独立休闲"skill_area;把第 0 节"给选择与掌控"原则做成一个**可重复的日常自主工具**,而非一次性关卡;训练自闭症儿童常缺的"空闲时间自我安排"。
- **渲染工作量**:低-中(选择板 + 可视时长条)。
- **依赖**:`skills/play_leisure.yaml → skill_area: independent_leisure`;方法 `self_management`/`visual_supports`/`task_analysis`/`video_modeling`;引用 `steinbrenner_2020`、`lee_2007`。

#### 53 小助手发一发 Class Helper
- **训练**:集体常规角色——当"小助手"分发/收取材料 · `visual_supports`/`peer_based_intervention` · 同伴示范
- **机制**:圆圈里坐着 3–4 个卡通同学,孩子当"小助手",按"一人一张"把纸/贴纸拖给每个同学(发完即止,不多不少);发对一个,那位同学就微笑点头。做完出现"你帮全班发好了"。
- **消费字段**:`steps`(把常规拆成"取一张→走到同学→给出→下一位")+ `visual_cards`;同学微笑为内置轻动画;无需新字段。
- **新颖/互动**:补齐 school_readiness 的"集体参与与常规"skill_area(此前 39/40 只覆盖等待轮流与集体指令);"一人一张、发完即止"的**一对多分发**是全新交互,练承担集体角色与一一对应。
- **渲染工作量**:中(一对多分发动画)。
- **依赖**:`skills/school_readiness.yaml → skill_area: group_participation_routines`;方法 `visual_supports`/`peer_based_intervention`/`modeling`/`task_analysis`;引用 `steinbrenner_2020`、`cn_gbt_47041_2026`、`cn_peizhi_2016`。

#### 54 我发现了就说 I Spy & Tell
- **训练**:主动评论/分享观察(而非仅被问才命名)· `naturalistic_intervention`/`modeling` · 时间延迟
- **机制**:一幅安静的生活场景里"发生"一点小变化(一只鸟飞进来、灯亮了),孩子点他注意到的东西,系统弹出"我看到了…/好大的…"的句式起头带他把观察说出来(可配语音),并给"你主动发现并说出来了!"的具体反馈;不问"这是什么",重在自发。
- **消费字段**:`scenarios`/`visual_cards`(场景 + 可评论热点)+ 轻量"评论句式起头";与"找一找"targets 结构同构;无需新字段。
- **新颖/互动**:补齐 communication_language"命名与听者反应"里最难的**自发评论/分享**;区别于 3.1(请求)、36/37(问候/提问)——这里练无提问触发的自发表达,用"注意→评论"的自然情境时间延迟。
- **渲染工作量**:中(场景 + 可点评论热点)。
- **依赖**:`skills/communication_language.yaml → skill_area: labeling_receptive`(主动评论/分享观察目标);方法 `naturalistic_intervention`/`modeling`/`time_delay`;引用 `sundberg_2008`、`schreibman_2015`、`steinbrenner_2020`。

#### 55 说说刚才 Tell What Just Happened
- **训练**:复述刚发生的简单事件(说出谁·做了什么 2–3 要素)· `scripting`/`visual_supports`/`video_modeling` · 视觉支持
- **机制**:先让孩子看/做一小段 3 步的事(如"倒水→搅拌→喝"),随即出现一条空白"复述条",孩子把"谁"+"做了什么"的图卡按先—然后—最后填上,拼好后系统把它连读成一句复述("刚才,小熊倒水、搅拌、喝了")并给具体肯定。
- **消费字段**:`steps`(刚发生事件的要素)+ `visual_cards`;复用"排顺序 sequence"骨架但对象是"已发生事件",可选极小 `recount_strip`;无必需新字段。
- **新颖/互动**:补齐 communication_language 的"叙述与复述"skill_area(此前无);区别于基线 sequence(排任意故事)——这里锚定"刚经历的事"做**即时复述装配 + 连读**,练叙事与工作记忆。
- **渲染工作量**:中(事件回放 + 复述条装配 + 连读)。
- **依赖**:`skills/communication_language.yaml → skill_area: narration_recount`;方法 `scripting`/`visual_supports`/`video_modeling`/`task_analysis`;引用 `prizant_2006`、`sundberg_2008`、`bellini_akullian_2007`。

#### 56 坐车去 Let's Ride
- **训练**:社区出行——候车不越线、刷卡坐稳、识别到站下车 · `task_analysis`/`video_modeling`/`social_narratives` · 视觉支持
- **机制**:一条简化路线图,孩子分步照做:在黄线后候车→上车刷卡→找座坐稳/扶好→"听到/看到报站"时判断该不该下车(**到站信号识别**小关)→到站点"下车"。抢步或越线只给温和"先等在黄线后",可重来。
- **消费字段**:`steps`(transportation 目标序列)+ `visual_cards`(黄线/刷卡/到站牌);无需新字段。
- **新颖/互动**:补齐 community_participation 的"社区出行"skill_area(此前 18/19/20 只覆盖购物/就餐/求助);"到站信号识别"这一判断子关是新交互;高风险出行的零风险预演,明确须成人全程监护、不替代真实陪同。
- **渲染工作量**:中(路线图 + 到站信号判定)。
- **依赖**:`skills/community_participation.yaml → skill_area: transportation`;方法 `task_analysis`/`video_modeling`/`social_narratives`/`visual_supports`/`self_management`;引用(通用锚点)`steinbrenner_2020`、`nac_2015`、`bellini_akullian_2007`、`cn_peizhi_2016`。**TODO_CITATION**:公共交通出行技能(乘公交/地铁的行为链/自我管理)专项实证——citations.yaml 暂无对应条目,与 community_participation.yaml 顶部登记的"社区出行特异性证据待补"一致,勿臆造。

#### 57 换了也没关系 It Changed, and That's Okay
- **训练**:容忍变化——接受一个小的、未预告的改变并转向替代 · `cognitive_behavioral`/`social_narratives` · 视觉支持
- **机制**:一个熟悉小场景里突然出现一点变化(红杯子没了只剩蓝杯子 / 想要的贴纸卖光了),先出现一句可点的应对语("没关系,换一个"),点了之后从 2–3 个平和替代里选一个,揭晓平稳的结果;强调变化会发生、也有办法。
- **消费字段**:`social_choice`/`scenarios`(变化情境 + 应对语 + 替代选项与平和结果);可复用 emotion_library 的 `plan_changed` 等情境;无需新字段。
- **新颖/互动**:补齐 cognitive_flexibility 的"容忍变化与应对意外"skill_area(此前 24/25 是灵活生成/定势转换,50 是冲动暂停);区别于 4.2/24——这里变化是"**发生在孩子身上的未预告改变**",练的是接受 + 应对语 + 替代,而非主动多解。
- **渲染工作量**:低-中(复用 social_choice + 应对语按钮)。
- **依赖**:`skills/cognitive_flexibility.yaml → skill_area: tolerating_change`;方法 `cognitive_behavioral`/`social_narratives`/`video_modeling`/`self_management`;引用 `nac_2015`、`buron_curtis_2003`、`gray_garand_1993`、`steinbrenner_2020`、`lee_2007`。

### Group B — 新颖交互机制专攻

#### 58 分岔小路 Fork in the Path
- **训练**:问题解决序列——找问题→想办法→选一个→试试→检查,且不同选择走不同路径 · `task_analysis`/`cognitive_behavioral` · 视频示范
- **机制**:一条从"遇到问题"到"解决"的路,孩子把"办法卡"拖到分岔口;拖不同的卡,路径就分到不同(但都平和、都可行)的后续,最后都能到达"解决了"。可回到分岔换另一条走,看"另一条路也能到"。
- **消费字段**:`steps` + `social_choice`(分岔点的可选办法与各自后续);需新增轻量 `branch_map`(哪张卡通向哪段)。
- **新颖/互动**:机制=**分支拖放序列(branching drag-sequence,choices change the path)**;不同于基线 sequence 的固定单一顺序,拖动的选择**实时改变接下来的路径**,把"办法不止一条"变成看得见的分岔。低感官:静态路径图 + 柔和高亮,无音效轰炸、无失败态。
- **渲染工作量**:中-高(分支状态机 + 路径图)。
- **依赖**:`skills/cognitive_flexibility.yaml → skill_area: problem_solving`;方法 `task_analysis`/`cognitive_behavioral`/`video_modeling`/`self_management`;引用 `steinbrenner_2020`、`nac_2015`、`wood_2009`、`kenworthy_2014`、`cannon_2011`。

#### 59 静一静·雪花落定 Hold the Calm
- **训练**:自我调节——维持平静/安静一小会儿 · `visual_supports`/`self_management` · 认知行为策略
- **机制**:屏幕是一个雪花球/柔光球,孩子**按住**时雪花缓缓落定、光晕渐柔;松手只是暂停(雪花轻轻浮起),随时可再按住继续。没有倒计时、没有目标秒数、没有"失败"——只有"你让它静下来了"的温和反馈。
- **消费字段**:内置"静止维持"组件(与呼吸动画同源但机制不同);可挂 emotion_library 的 `quiet_corner`/`calm` 作策略泛化;无需新字段。
- **新颖/互动**:机制=**按住维持(tap-and-hold sustain)**,把"保持平静/安静"这件抽象事变成手指持续参与的连续动作;区别于 1.2/27 的**呼吸节律引导**(随节拍胀缩),这里是"按住让画面静下来"的持续性调节。低感官,且**显式遵守无计时/无惩罚**:无秒数、无进度条竞争、松手不罚。
- **渲染工作量**:中(按压驱动的落定动画)。
- **依赖**:`skills/emotional_regulation.yaml → skill_area: regulation_strategies`;方法 `visual_supports`/`self_management`/`cognitive_behavioral`;引用 `wood_2009`、`kuypers_2011`、`lee_2007`。

#### 60 先看看会怎样 Peek the Outcome
- **训练**:用被接纳的方式表达强烈情绪(替代发脾气/退缩)· `social_narratives`/`video_modeling`/`cognitive_behavioral` · 强化
- **机制**:一个情绪触发情境给 2–3 个反应选项(大喊 / 用语言说"我很生气" / 先离开一下);孩子点任一选项**先看到一小段平和的"会怎样"预览**(不是最终提交),看完可返回比较别的,想好再"就这么做"确认。把"三思而后行"具体化。
- **消费字段**:`social_choice` + `scenarios`;把 outcome 拆成"可预览的软结果";可复用 emotion_library 触发情境;无需新字段。
- **新颖/互动**:机制=**结果预览后再决定(choice-with-consequence-preview)**;不同于既有 social_choice"选了才揭晓结果",这里**提交前**就能温和预览每条路的后果并来回比较,真正把后果前置。低感官:预览为静态小画面 + 一句话,无惊吓式负面演示。
- **渲染工作量**:中(预览态 vs 提交态两层)。
- **依赖**:`skills/emotional_regulation.yaml → skill_area: emotion_expression`;方法 `social_narratives`/`video_modeling`/`cognitive_behavioral`/`reinforcement`;引用 `prizant_2006`、`gray_2015_newbook`、`nac_2015`。

#### 61 拼出这个表情 Build the Feeling Face
- **训练**:辨识面部表情、命名情绪(哪些五官线索对应哪种情绪)· `visual_supports`/`video_modeling`/`discrete_trial_training` · 视觉支持
- **机制**:给一个目标情绪词(开心/难过/生气/害怕…),孩子从眉、眼、嘴的几种部件里挑选拼到一张脸上,拼出符合该情绪的表情;拼对关键线索(如"生气=眉毛向下 + 嘴巴紧")就点亮并解释线索,拼得不同也温和提示"再看看眉毛"。
- **消费字段**:`emotion_library`(emotions + 身体/表情线索);**需新增 `face_parts`**(每种情绪的眉/眼/嘴部件与关键线索)——emotion_library 的轻量扩展。
- **新颖/互动**:机制=**表情构造器(build-a-face emotion constructor)**;不同于 1.3 的**识别**(点选已画好的脸)与 38 的**镜像模仿**(自己做表情),这里是**从部件构造**表情,主动学"五官→情绪"的映射。低感官:拼贴式、无动画轰炸,一次一张脸一个焦点。
- **渲染工作量**:中(部件拖拼 + 线索判定)。
- **依赖**:`skills/emotional_regulation.yaml → skill_area: recognize_name`;方法 `visual_supports`/`video_modeling`/`discrete_trial_training`;引用 `golan_2010`、`buron_curtis_2003`、`ekman_1992`。

#### 62 一拍一答 Tap Back
- **训练**:轮流——从物件/游戏轮流到"我一下·你一下"的来回 · `video_modeling`/`social_narratives`/`modeling` · 强化
- **机制**:屏幕一边是"我(卡通伙伴)"、一边是"你";伙伴先轻拍出一个简单节奏(1–2 下),轮到你时你在自己这侧照拍,拍完轮次灯柔和地切回伙伴,如此来回。节奏极简、软音、可自定慢速;重在"轮到我—轮到你"的可感体验,不比准、不打分。
- **消费字段**:轻量"轮流节奏脚本"(谁先、几拍);复用轮次指示的视觉;无需新字段。
- **新颖/互动**:机制=**轮流节奏拍打(turn-taking rhythm tapping)**;不同于 2.3"轮到谁"(滚球/轮次灯)——这里用**一来一回的拍击节奏**让轮流成为身体可感的时间体验。低感官:柔和短音、慢节奏可调、无突兀音效,一次一拍一焦点。
- **渲染工作量**:中(节奏回放 + 轮次切换)。
- **依赖**:`skills/social_interaction.yaml → skill_area: turn_taking`;方法 `video_modeling`/`social_narratives`/`modeling`/`reinforcement`;引用 `nac_2015`、`sundberg_2008`。

#### 63 我的选择小故事 My Choose-a-Path Story
- **训练**:友谊与维持关系——在社交小故事的决策点做选择、看故事如何走向 · `social_narratives`/`social_skills_training` · 认知行为策略
- **机制**:一则第一人称社交故事(如"约朋友来家里玩")逐段展开,读到关键处停下问"这时我可以…",孩子选一个,故事据此**分支续写**成不同(都友好)的走向;可回到决策点走另一条,读到"两种做法故事都能继续"。
- **消费字段**:`scenarios` + `social_choice`(每个决策点的选项与后续段落);复用社交故事结构;可选新增 `story_branch` 轻结构标注段落走向。
- **新颖/互动**:机制=**带决策点的互动社交故事(interactive branching social story)**;不同于 2.2"对话搭桥"(实时你问我答的对话状态机)——这里是**被讲述的故事**在决策点分叉,把静态社交故事变成可探索的多结局叙事。低感官:图文慢节奏阅读、无时限、无音效压力。
- **渲染工作量**:中-高(分支叙事状态机)。
- **依赖**:`skills/social_interaction.yaml → skill_area: friendship_group`;方法 `social_narratives`/`social_skills_training`/`cognitive_behavioral`;引用 `gray_garand_1993`、`gray_2015_newbook`、`nac_2015`、`gates_2017`。

#### 64 找找友好的信号 Spot the Friendly Signal
- **训练**:回应同伴的发起——在场景里找出"友好邀请"的社交信号并回应 · `video_modeling`/`social_skills_training`/`prompting` · 提示
- **机制**:一幅有几个卡通同伴的场景,其中一个正发出**友好信号**(挥手/微笑/让出位置/看向你);孩子在场景里找到并点它,系统放大揭晓"他在邀请你一起玩",再给一个温和的"我可以回应…"的小选择。找错只温和提示"再看看谁在看你/向你招手"。
- **消费字段**:`scenarios`/`visual_cards`(场景 + 社交信号热点)+ 轻量"社交线索目标"(与"找一找"targets 同构);无需新字段。
- **新颖/互动**:机制=**搜寻社交线索(spot-the-social-cue)**;把场景热区扫视**专用于转瞬即逝的社交信号**(挥手/微笑/身体朝向),区别于 2.5/49 找"物品/数字"——目标是社交线索且带"为什么友好"的揭晓与回应。低感官:静态场景 + 柔和高亮被点中项,无闪烁无音效。
- **渲染工作量**:中(场景热区 + 社交信号揭晓)。
- **依赖**:`skills/social_interaction.yaml → skill_area: initiating_responding`(回应同伴的发起);方法 `video_modeling`/`social_skills_training`/`prompting`;引用 `gates_2017`、`nac_2015`、`steinbrenner_2020`。

### 第五批内容模型影响
| 玩法 | 复用字段 | 需新增 |
|---|---|---|
| 一起玩有规则的游戏 / 小助手发一发 / 坐车去 | steps + visual_cards | 无 |
| 我的休闲我来选 | visual_cards | 无(可选 localStorage 自我记录) |
| 我发现了就说 / 找找友好的信号 | scenarios / visual_cards | 无(复用"找一找"targets 结构) |
| 说说刚才 | steps + visual_cards | 可选极小 `recount_strip` |
| 换了也没关系 / 先看看会怎样 | social_choice / scenarios / emotion_library | 无 |
| 静一静·雪花落定 | emotion_library(策略泛化) | 内置"按住维持"组件(与呼吸动画同源) |
| 分岔小路 | steps + social_choice | 轻量 `branch_map`(卡→后续段) |
| 拼出这个表情 | emotion_library | `face_parts`(眉/眼/嘴部件 + 关键线索) |
| 一拍一答 | 轮次视觉 | 轻量"轮流节奏脚本" |
| 我的选择小故事 | scenarios / social_choice | 可选 `story_branch` 段落走向标注 |

**累计**:游戏创意达 **64 个**(批次 1–5)。Group A(#51–57)深化经核对最薄的 5 个域:play_leisure(批前 2→4)、school_readiness(2→3)、communication_language(3→5)、community_participation(3→4)、cognitive_flexibility(3→4,另 Group B #58 再落此域→5)。Group B(#58–64)主打 7 个此前全库未出现的交互机制:**分支拖放序列 / 按住维持 / 结果预览后再决定 / 表情构造器 / 轮流节奏拍打 / 带决策点的互动社交故事 / 搜寻社交线索**,分别落在 cognitive_flexibility / emotional_regulation / social_interaction 的未覆盖 skill_area。绝大多数仍"加一个 JS 活动函数"即可;仅 `branch_map`、`face_parts` 与可选 `recount_strip`/`story_branch` 为轻量新增。**校对留意**:公共交通出行专项实证仍缺(见 #56 TODO_CITATION),其余均锚定 citations.yaml 现有真实引用与 skills/*.yaml 现有 skill_area。

---

## 12. 第六批创意(2026-07-14)

**仍只积累创意,不生成产品**(遵循"停止产出产品·完善生成器")。本批 11 款(#65–#75)专为**拉平技能库**:经逐条点数 #1–#64,最薄的 5 个域为 **school_readiness(3)、play_leisure(4)、motor_sensory(4)、prevocational(4)、community_participation(4)**(其余 12 域校核:emotional_regulation 9、social_interaction 9、safety_skills 6、communication_language/daily_living_behavior/functional_academics/cognitive_flexibility 各 5,另通用注意力"记忆翻翻乐"#14 计 1,合计 64)。本批把这 5 个薄域各补到 **6**,每款锚定该域一个**此前全库未被任何玩法覆盖的 skill_area**,全部硬性遵守第 0 节 8 条原则,交互限于低感官(拖动/配对/连线/分类/点亮揭晓/先—然后/带温和反馈的选择)。

### 入学与课堂准备(school_readiness)—— 补 attending_sitting / transitions / independent_work_system

#### 65 找座位·看这里 Find My Spot & Look Here
- **训练**:注意与入座——走到指定座位坐下、面向老师/材料保持注意 · 视觉支持 / 自我管理
- **机制**:一屏教室里几张空椅子,只有一张贴着孩子的名字/照片/脚印标记;孩子把小人拖到**标记匹配**的那张椅子坐下(名字—座位配对);坐好后进入圆圈时间,卡通老师一开口就柔和地提示"看这里",孩子点一下"看老师"让"在看"的柔光灯亮起;点错座位只温和提示"找找你的名字",可重来。无计时。
- **消费字段**:`visual_cards`(座位标记/名字卡,与"找一找"targets 结构同构)+ `steps`(就座→面向老师);无需新字段。
- **新颖/互动**:把"找到自己的座位 + 循线索朝向老师"这条最基础的课堂前技能做成"标记配位 + 朝向点亮";区别于 39/40/53(举手等待/集体指令/发材料)——这里锚定更早的**入座与注意定向**。
- **渲染工作量**:低-中(座位配位 + 朝向柔光灯,复用点选骨架)。
- **依赖**:`skills/school_readiness.yaml → skill_area: attending_sitting`;方法 `visual_supports`/`prompting`/`reinforcement`/`self_management`;引用 `steinbrenner_2020`、`odom_2010`、`cooper_2007`。

#### 66 换个活动啦 Time to Switch(现在—接下来)
- **训练**:校园过渡——收拾→排队→转到下一活动,并预知"接下来" · 视觉支持 / 社交叙事
- **机制**:活动进行中,角落出现**柔和闪动的过渡提示(视觉,不用刺耳铃声)**;孩子先点"接下来是什么"**揭晓下一张活动卡**(降低不确定),再把桌上的东西拖进"收纳筐"(收拾),最后点"到门口排队";抢先跳步只温和提示"先收好、再排队",可重来。
- **消费字段**:`steps`(收拾→排队→过渡)+ `visual_cards(kind=schedule)`("现在—接下来"卡);无需新字段。
- **新颖/互动**:专攻**过渡这一时刻**(而非 #12"我的一天"排整天日程)——用"先揭晓接下来 + 收拾—排队"把最易引发焦虑/抗拒的转换点做成可预期的小演练;揭晓"接下来"是降低过渡焦虑的循证要点。
- **渲染工作量**:中(过渡提示 + 揭晓 + 收拾拖放)。
- **依赖**:`skills/school_readiness.yaml → skill_area: transitions`;方法 `visual_supports`/`social_narratives`/`video_modeling`/`time_delay`/`self_management`;引用 `steinbrenner_2020`、`odom_2010`、`nac_2015`。

#### 67 从左做到右 Left-to-Right Work System
- **训练**:独立工作系统——从左边取任务、做完放入右边"完成"框、再取下一件,直到整组做完转下一活动 · 视觉支持 / 任务分析
- **机制**:一条从左到右的工作台:左侧篮里 2–3 张按**数字/颜色标记**的任务卡,孩子按标记取出一张→完成一件已掌握的小操作(配对/分类)→拖入右侧"完成✓"框→再取下一张;整组清空后出现"都做完了",翻出"接下来"活动卡。全程无计时、无催促。
- **消费字段**:`steps`(左取→做→右放的循环)+ `visual_cards`(任务卡/完成框标记);无需新字段。
- **新颖/互动**:机制=**从左到右的实体化任务队列 + "完成"框**(TEACCH 独立工作系统的直接互动化);区别于 #29"工作板"(那是"做什么/做多少/怎样算完成/接下来"的信息面板走一遍)——这里是**逐件取—做—归位**的执行流,由 [[hume_odom_2007]] 独立工作系统实证直接支撑。
- **渲染工作量**:中(左右台面 + 取放循环 + 完成框计数)。
- **依赖**:`skills/school_readiness.yaml → skill_area: independent_work_system`;方法 `visual_supports`/`task_analysis`/`time_delay`/`self_management`;引用 `hume_odom_2007`、`odom_2010`、`steinbrenner_2020`、`cooper_2007`。

### 游戏与休闲(play_leisure)—— 补 play_prerequisites / functional_play

#### 68 按一按·会怎样 Cause & Play(探索玩具)
- **训练**:游戏基础前技能——探索因果关系、模仿玩玩具的动作、与人共同注意同一玩具 · 自然情境 / 示范
- **机制**:一屏 2–3 件简单玩具(按钮灯/摇铃/小车);孩子**点/按**一件就**柔和揭晓它的反应**(按按钮→灯轻轻亮、摇→出现柔和的响铃图标、推小车→车滚一小段);随后"我先这样玩→轮到你",跟着做一个简单玩法动作;卡通伙伴会看向被玩的玩具,建立共同注意。无音效轰炸,反应皆为轻缓视觉。
- **消费字段**:`steps`(动作→反应/示范→轮到你)+ `visual_cards`(玩具及其反应);可选极小 `cause_effect`(动作↔反应对),非必需。
- **新颖/互动**:机制=**因果探索点按 + 玩法模仿**,补齐 play_leisure 最早的游戏前技能(此前 41/42/51/52 均在象征/规则/独立休闲层);区别于配对——这里是"按一按看会怎样"的因果发现 + 模仿,是后续一切游戏的地基。
- **渲染工作量**:中(因果反应轻动画 + 模仿提示)。
- **依赖**:`skills/play_leisure.yaml → skill_area: play_prerequisites`;方法 `naturalistic_intervention`/`modeling`/`jasper`/`prompting`/`reinforcement`;引用 `kasari_2006`、`sundberg_2008`。

#### 69 照着搭·串一串 Build & Thread(功能性/建构游戏)
- **训练**:功能性/建构游戏——按范例搭建、拼插、串珠,独立完成一项 3–5 步建构 · 任务分析 / 示范
- **机制**:先出示一个**范例**(一座三块塔 / 一串"红蓝红"珠子);"我先搭一块给你看",再"轮到你",孩子把积木/珠子按范例**拖到对位**搭起来或**依序串**上;搭对/串对即稳稳落位,放偏温和回弹并提示"再看看范例"。可自选搭塔或串珠。
- **消费字段**:`steps`(建构/串接的分步序列)+ `visual_cards`(范例图 + 可拖部件);无需新字段。
- **新颖/互动**:机制=**照范例单人建构 + 顺序串接**;区别于 #4"一起搭"(双人"你一块我一块"合作)与基线 match(配对)——这里是独自**按模型复现**的功能性/建构游戏,是象征游戏之前的关键一层。
- **渲染工作量**:中(对位拖放 + 串接顺序判定)。
- **依赖**:`skills/play_leisure.yaml → skill_area: functional_play`;方法 `task_analysis`/`modeling`/`naturalistic_intervention`/`prompting`/`reinforcement`;引用 `sundberg_2008`、`schreibman_2015`。

### 运动与感觉调节(motor_sensory)—— 补 body_awareness / daily_movement_participation

#### 70 指一指·摆一摆 Point & Place(身体与空间)
- **训练**:身体觉知——指认命名身体部位、理解上/下/前/后/里/外的空间位置 · 回合式教学 / 视觉支持
- **机制**:一个卡通小人;先"指出你的鼻子/手/脚"——孩子在小人身上点中被叫到的部位并亮起命名;进阶到空间概念:把一个物件**拖到指定位置**("把球放到头**上**""把小熊放到椅子**后面**""放进**里**面");做对即到位并读出方位词,放错温和提示"再听听是上还是下"。
- **消费字段**:`visual_cards`(身体部位 + 物件)+ `steps`(点部位→摆位置);可选轻量"空间目标"(方位词↔目标位,与"找一找"targets 同构),非必需。
- **新颖/互动**:机制=**身体部位点认 + 空间方位拖放**;补齐 motor_sensory 里最基础的身体图式/空间概念(此前 26/34/35 是动作模仿/律动平衡/描画,均非身体—空间认知);为动作计划打底。
- **渲染工作量**:中(部位热区 + 方位拖放判定)。
- **依赖**:`skills/motor_sensory.yaml → skill_area: body_awareness`;方法 `discrete_trial_training`/`visual_supports`/`naturalistic_intervention`/`modeling`/`prompting`;引用 `steinbrenner_2020`、`cooper_2007`。

#### 71 加入律动圈·开始和停 Join the Circle: Go & Stop
- **训练**:参与体育/律动集体活动——走进活动区加入圆圈、听"开始/停"口令跟做热身 · 视觉支持 / 视频示范
- **机制**:先"走进圈里坐下/排好"(把小人拖进圆圈的一步);律动开始,屏幕给柔和的"**开始**"信号时点着跟做一个示范动作(拍手/踏步),给"**停**"信号时点"停住"定格;信号切换柔和、节奏可调慢,抢拍只温和提示"等'开始'再动"。无比准、无计分。
- **消费字段**:`steps`(进圈→就位→开始/停跟做)+ `visual_cards`(开始/停信号、动作卡);开始/停信号为内置轻组件;无需新字段。
- **新颖/互动**:机制=**加入集体 + "开始/停"口令响应**;区别于 #15"安全过马路"(红绿灯用于路口)——这里的开始/停用于**体育/律动的集体参与与冲动控制**,也区别于 26/34(动作模仿/节奏)——重在"进入集体并听集体口令起停"。
- **渲染工作量**:中(进圈动画 + 开始/停信号切换)。
- **依赖**:`skills/motor_sensory.yaml → skill_area: daily_movement_participation`;方法 `visual_supports`/`video_modeling`/`modeling`/`naturalistic_intervention`/`self_management`/`reinforcement`;引用 `steinbrenner_2020`、`nac_2015`。

### 职业前(prevocational)—— 补 work_behaviors / task_completion

#### 72 上工准备·专心打卡 Ready to Work & Stay Focused
- **训练**:工作行为——守时到岗、遵守工位规则、维持专注(自我监控) · 视觉支持 / 自我管理
- **机制**:三步一屏:①"上工时间到"的柔和提示出现→点"到岗就位";②把 2–3 张**工位规则卡**(手放桌上/说话先举手/东西放整齐)与"这样做/不这样做"的图例**配对**,认得规则;③开始作业后,每隔一会儿温和弹出"我在专心工作吗?"让孩子自己点"在专心/我调整一下"——纯自我觉察打勾,**不计分、不排名**。
- **消费字段**:`steps`(到岗→守规→自查)+ `visual_cards`(规则卡)+ `social_choice`(规则的"该/不该");可选把"专心打勾"记 localStorage 供自我觉察;无需新字段。
- **新颖/互动**:补齐 prevocational 全新的 **work_behaviors**(守时/守规/专注,此前 28/29/46/47 是分拣/工作板/归位/求助);机制=**到岗提示响应 + 规则配对 + 周期性自我监控打勾**,把"工作行为"这类看不见的软技能做成可自察的流程。
- **渲染工作量**:低-中(提示 + 规则配对 + 自查小勾)。
- **依赖**:`skills/prevocational.yaml → skill_area: work_behaviors`;方法 `visual_supports`/`self_management`/`video_modeling`/`reinforcement`;引用 `steinbrenner_2020`、`lee_2007`、`allen_2010`、`cooper_2007`。

#### 73 做完了·自己检查 Finished? Check It Yourself
- **训练**:任务坚持与完成——做完全部后**对照样板自查**有无遗漏/错误并改正 · 视觉支持 / 自我管理
- **机制**:一件"刚做完"的多步作业(如装好三件文具的袋 / 排好的一组零件)旁给出**标准样板**;孩子把"完成品"与样板**逐处比对**,点出**缺的一件或放错的一处**并拖来补上/换正(找不同+补正);改好后在"开始—做完—已检查"三格里给"已检查"打勾。无惩罚,发现错误被正向框架化为"好眼力"。
- **消费字段**:`steps`(比对→找出→改正)+ `visual_cards`(样板 vs 完成品);"已检查"三格可记 localStorage(自我监控,不计分);无需新字段。
- **新颖/互动**:机制=**对照样板自查纠错(spot-and-fix against a standard)**;区别于 #28"小小分拣员"(把物品分箱、仅以"完成✓"收尾)——这里锚定 task_completion 的**独立层"自查遗漏/错误"**维度(#28 未触及),练就业关键的质量自检与坚持到底。
- **渲染工作量**:中(样板比对 + 找出/补正)。
- **依赖**:`skills/prevocational.yaml → skill_area: task_completion`;方法 `visual_supports`/`task_analysis`/`time_delay`/`self_management`/`reinforcement`;引用 `hume_odom_2007`、`steinbrenner_2020`、`lattimore_2006`、`cooper_2007`。

### 社区参与(community_participation)—— 补 public_behavior / appointments

#### 74 室内小声·排好队 Inside Voice & Wait in Line
- **训练**:公共场所举止——按场所用"室内声音"、排队不插队、不乱碰商品且跟紧大人 · 社交叙事 / 视觉支持
- **机制**:给一个场所卡(图书馆/超市/公园),孩子在一个**三档音量表**(悄悄话 / 平常说话 / 户外大声)上调到**与该场所相称**的一档("图书馆=悄悄话");再走一小步"排队"——队伍前移时点"跟着往前",轮到自己再上前;另有"手放好、跟在大人身边"的温和选择。选得不合适只温和提示"这里要小一点声",可重调。
- **消费字段**:`scenarios`/`visual_cards`(场所卡 + 队伍)+ `social_choice`(跟紧/不乱碰);三档音量表复用 #1.1"情绪温度计"的分级滑块组件;可选极小 `voice_level`(场所↔相称音量档),非必需。
- **新颖/互动**:机制=**场所→相称音量档匹配(voice-level meter)+ 排队小步**;全库首个"音量到场所"的调节玩法(区别于 #1.1 调情绪强度),补齐 community_participation 的 public_behavior(此前 18/19/20/56 是购物/就餐/求助/出行)。
- **渲染工作量**:中(音量表 + 场所匹配 + 排队小步)。
- **依赖**:`skills/community_participation.yaml → skill_area: public_behavior`;方法 `social_narratives`/`visual_supports`/`modeling`/`task_analysis`/`time_delay`/`reinforcement`;引用 `steinbrenner_2020`、`nac_2015`、`gray_garand_1993`、`cn_peizhi_2016`。

#### 75 看医生·理发预演 At the Doctor / Haircut(预告与配合)
- **训练**:社区常规(看诊/理发)——事前预告流程、候诊安坐、配合检查/理发的关键步骤 · 社交叙事 / 视觉支持
- **机制**:先用"现在—接下来"的**图片日程预演(priming)**走一遍流程(进门→候诊坐等→配合→结束);到关键处出现"**配合小步**":医生检查时点"张嘴让医生看一看"、理发时点"围上围布、低头"——配合即揭晓平和的下一步;候诊段给一个"看绘本/玩安静小物"的等待选择。语气平静、赋能,强调"预先知道会发生什么就不紧张"。
- **消费字段**:`steps`(看诊/理发流程)+ `visual_cards(kind=schedule)`("现在—接下来"卡);社交叙事文本复用 social_narratives 内容;无需新字段。
- **新颖/互动**:机制=**图片日程预告 + 配合关键步骤点按**;补齐 community_participation 的 appointments(此前无),把看诊/理发这类高焦虑就诊做成零压力预演;区别于 #56"坐车去"/#15"安全过马路"(出行/路口序列)——这里是**就诊脱敏与身体配合**。此敏感主题须专业人员与家长把关。
- **渲染工作量**:中(流程图 + 配合步骤揭晓)。
- **依赖**:`skills/community_participation.yaml → skill_area: appointments`;方法 `social_narratives`/`visual_supports`/`video_modeling`/`task_analysis`/`time_delay`/`prompting`/`reinforcement`;引用 `steinbrenner_2020`、`nac_2015`、`gray_garand_1993`、`bellini_akullian_2007`。**TODO_CITATION**:看诊/牙科/理发的脱敏与配合专项实证——citations.yaml 暂无对应条目(与 community_participation.yaml 顶部 TODO_CITATIONS 登记一致),现复用社交叙事/视觉支持的通用循证锚点,勿臆造。

### 第六批内容模型影响
| 玩法 | 复用字段 | 需新增 |
|---|---|---|
| 找座位·看这里 / 换个活动啦 / 从左做到右 / 照着搭·串一串 / 加入律动圈 / 看医生·理发预演 | steps + visual_cards(含 kind=schedule) | 无(配位/排序/照做/拖放骨架复用) |
| 按一按·会怎样 | steps + visual_cards | 可选极小 `cause_effect`(动作↔反应对) |
| 指一指·摆一摆 | visual_cards + steps | 可选轻量"空间目标"(与"找一找"targets 同构) |
| 上工准备·专心打卡 / 做完了·自己检查 | steps + visual_cards + social_choice | 无(自我监控可选 localStorage,不计分) |
| 室内小声·排好队 | scenarios / visual_cards / social_choice | 三档音量表复用 #1.1 滑块;可选极小 `voice_level` |

### 批次 6 领域拉平小结(逐条核对 #1–#75)
| 领域 domain | 批前(#1–64) | 本批 +N | 批后(#1–75) |
|---|---|---|---|
| emotional_regulation | 9 | 0 | 9 |
| social_interaction | 9 | 0 | 9 |
| safety_skills | 6 | 0 | 6 |
| **school_readiness** | 3 | **+3**(#65,66,67) | **6** |
| **play_leisure** | 4 | **+2**(#68,69) | **6** |
| **motor_sensory** | 4 | **+2**(#70,71) | **6** |
| **prevocational** | 4 | **+2**(#72,73) | **6** |
| **community_participation** | 4 | **+2**(#74,75) | **6** |
| communication_language | 5 | 0 | 5 |
| daily_living_behavior | 5 | 0 | 5 |
| functional_academics | 5 | 0 | 5 |
| cognitive_flexibility | 5 | 0 | 5 |
| 通用/注意力(记忆翻翻乐 #14) | 1 | 0 | 1 |
| **合计** | **64** | **+11** | **75** |

**累计**:游戏创意达 **75 个**(批次 1–6)。本批把此前最薄的 5 个域(school_readiness 3、其余 4)**各补至 6**,分布从批前的 3–9 收窄到 **5–9**,库已明显拉平(五个目标域现与 safety_skills 齐平在 6,仅低于最厚的 emotional_regulation/social_interaction 各 9)。11 款各锚定一个**此前未被玩法覆盖的真实 skill_area**:attending_sitting / transitions / independent_work_system(校准)· play_prerequisites / functional_play(游戏)· body_awareness / daily_movement_participation(运动)· work_behaviors / task_completion(职业前)· public_behavior / appointments(社区)。绝大多数仍"加一个 JS 活动函数"即可,仅 `cause_effect`、`voice_level`、"空间目标"为**可选**极小新增,音量表复用 #1.1 分级滑块。**校对留意**:看诊/理发脱敏专项实证仍缺(见 #75 TODO_CITATION,与 community_participation.yaml 顶部登记一致),其余全部锚定 citations.yaml 现有真实引用与 skills/*.yaml 现有 skill_area。

---

*所有游戏均为循证辅助/教育工具,不替代专业评估与治疗;产出默认标记"需专业人员审核草稿"。*
