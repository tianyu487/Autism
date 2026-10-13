# 视频课选题创意库(Idea Backlog · TrainingModule)

> 用途:积累**未来视频课选题(训练模块)**,只积累不产出成片。
> 现阶段遵循长期守则「**停止产出产品·完善生成器**」——本文件只登记选题,
> 不生成任何视频/图卡/成片,不撰写完整模块 JSON,日后再逐个用管线实现(`train --script`)。
> 每条选题锚定「技能域 + 循证方法(EBP)+ 真实引用」,做到「日后可直接开写」。
> 纪律:所有 skill_area / method_id / citation id **逐字取自知识库真实条目**;
> 拿不准是否存在的引用一律写 `TODO_CITATION: …`,**绝不臆造**引用、id 或疗效。
> 所有选题均为「**需专业审核草稿**」概念;语气正向、赋能、非恐吓。

**已完成(勿重复):**
1. 《当同伴想玩我的玩具时 / When a Friend Wants My Toy》——social_interaction → `sharing_requesting`,method `video_modeling`(见 `output/demo_training/module.json`)。
2. 《轮流与等待 / Waiting for My Turn》——social_interaction → `turn_taking`,method `video_modeling`。
> 下列新选题均避开这两个已做主题;涉及「等待/轮流」的新条目一律换到**不同技能域与情境**(如课堂举手、认知灵活性里的等待与接受"不行")。

---

## 领域:情绪认知与调节 emotional_regulation

### 深呼吸,让我平静下来 / Taking Deep Breaths to Calm Down
- **技能**:emotional_regulation → `regulation_strategies` · regulate 层(使用具体平复工具)
- **EBP**:`cognitive_behavioral`
- **cast**:solo_child
- **引用**:`kuypers_2011`(verify:true)、`buron_curtis_2003`(verify:true)、`wood_2009`(verify:false)
- **学习目标(种子)**:情绪升高时,孩子在提示下能用一次深呼吸,把自己从"黄区"带回"绿区"(触发情境 3 次中≥2 次)。
- **一句话梗概**:当我感觉快要生气或着急时,我先停下来,慢慢吸气、慢慢呼气,让身体和心情都松下来。

### 用语言说出我的大情绪 / Using Words for My Big Feelings
- **技能**:emotional_regulation → `emotion_expression` · regulate 层(用被接纳的方式表达强烈情绪)
- **EBP**:`video_modeling`
- **cast**:solo_child
- **引用**:`prizant_2006`(verify:true)、`gray_2015_newbook`(verify:false)、`nac_2015`(verify:false)
- **学习目标(种子)**:在触发情境中,孩子能用一句恰当的话表达强烈情绪(如"我很生气,我要先离开一下"),替代动手或退缩,提示下达成 1 次。
- **一句话梗概**:情绪很强的时候,我可以用语言把它说出来,让别人知道我需要什么,这样比发脾气更有用。

### 我的心情叫什么名字 / Naming My Feelings
- **技能**:emotional_regulation → `recognize_name` · recognize 层(辨识表情并命名基本情绪)
- **EBP**:`visual_supports`
- **cast**:solo_child
- **引用**:`ekman_1992`(verify:true)、`buron_curtis_2003`(verify:true)、`golan_2010`(verify:false)
- **学习目标(种子)**:看四种基本情绪(开心/难过/生气/害怕)的表情图,孩子能正确命名至少 3 种,并在日常情境中提示下说出自己当下的心情(连续 2 次达成)。
- **一句话梗概**:我看着表情图,能说出这是开心、难过、生气还是害怕;也能用情绪词把我现在的心情讲出来。
- *备注:与已做情绪课不同,本课落在"识别与命名"基础层,是后续调节策略的前置技能,不重复。*

### 做错了也没关系,再试一次 / When I Make a Mistake
- **技能**:emotional_regulation → `coping_specific` · regulate 层(应对愤怒/挫折:身体升温时先暂停再降温)
- **EBP**:`cognitive_behavioral`
- **cast**:solo_child
- **引用**:`kuypers_2011`(verify:true)、`buron_curtis_2003`(verify:true)、`wood_2009`(verify:false)
- **学习目标(种子)**:事情做不好、出错时,孩子能觉察挫折的身体信号并先暂停,用深呼吸或数数把强度从高降到可控,再说一句"再试一次",触发情境 3 次中≥2 次不升级为发脾气。
- **一句话梗概**:拼不上、写错了的时候,我先停一停、深呼吸,对自己说"做错了没关系,我再试一次",让着急的心情慢慢降下来。
- *备注:与《深呼吸,让我平静下来》(regulation_strategies 通用工具)不同,本课聚焦"针对挫折/犯错"的特定应对,情境与技能不重复。*

---

## 领域:社交互动 social_interaction

### 说"你好"和"再见" / Saying Hello and Goodbye
- **技能**:social_interaction → `initiating_responding` · sustain 层(完成问候与告别常规)
- **EBP**:`video_modeling`
- **cast**:peer_play
- **引用**:`krantz_mcclannahan_1993`(verify:true)、`chan_2009`(verify:true)、`nac_2015`(verify:false)
- **学习目标(种子)**:到达或离开时,孩子能主动完成问候或告别(说"你好"/"再见,明天见")3 次中≥2 次。
- **一句话梗概**:见到老师和小朋友,我可以先打招呼说"你好";要走的时候挥挥手说"再见",这样大家都觉得很友好。

### 我可以一起玩吗?加入同伴游戏 / Can I Play Too? Joining In
- **技能**:social_interaction → `friendship_group` · sustain 层(加入正在进行的集体游戏,并温和应对被拒)
- **EBP**:`social_skills_training`
- **cast**:peer_play
- **引用**:`gates_2017`(verify:false)、`steinbrenner_2020`(verify:false)、`nac_2015`(verify:false)
- **学习目标(种子)**:孩子能用恰当方式(先观察再问"我可以一起玩吗")请求加入正在进行的集体游戏,并在被拒时保持平和 1 次。
- **一句话梗概**:想加入小朋友的游戏时,我先在旁边看一看,再问"我可以一起玩吗";就算这次被拒绝,我也可以平静地去找别的活动。

### 一起搭、一起玩:分工合作的游戏 / Working Together in Play
- **技能**:social_interaction → `cooperative_play` · sustain 层(合作/协商游戏:分工、遵守规则、共同达成目标)
- **EBP**:`peer_based_intervention`
- **cast**:peer_play
- **引用**:`chan_2009`(verify:true)、`kasari_2006`(verify:false)、`nac_2015`(verify:false)
- **学习目标(种子)**:在一次合作游戏中(如一起搭一座塔或分角色过家家),孩子能与同伴分工、按约定规则行动并坚持到共同完成目标 1 次。
- **一句话梗概**:我和小朋友一起搭积木——你递、我接,说好谁做什么,一直合作到我们把塔搭好。
- *备注:与已做《轮流与等待》(轮流机制)及《我可以一起玩吗》(加入/被拒)不同,本课聚焦"分工协商、共达目标"的合作游戏,不重复。*

### 别人喜欢的和我不一样:社交小侦探 / The Social Detective
- **技能**:social_interaction → `perspective_taking` · initiate 层(愿望与情绪归因:考虑他人有不同喜好,读线索猜感受)
- **EBP**:`social_skills_training`
- **cast**:peer_play
- **引用**:`baron_cohen_1985`(verify:true)、`howlin_1999`(verify:true)、`fisher_happe_2005`(verify:true)
- **学习目标(种子)**:给同伴挑玩具或活动前,孩子能先问"你喜欢哪一个"并据表情/情境线索恰当推断对方的感受,3 次中≥2 次。
- **一句话梗概**:我像小侦探一样观察——别人喜欢的东西可能和我不一样;看看他的表情,我就能猜到他现在开心还是难过。

---

## 领域:沟通与语言 communication_language

### 需要帮忙时说"帮我" / Asking for Help
- **技能**:communication_language → `requesting` · request 层(请求帮助/休息,用沟通替代哭闹)
- **EBP**:`naturalistic_intervention`
- **cast**:solo_child
- **引用**:`koegel_odell_1987`(verify:true)、`bondy_frost_1994`(verify:false)、`steinbrenner_2020`(verify:false)
- **学习目标(种子)**:遇到困难时,孩子能用语言或图片主动发起一次"帮我"的请求,而不是哭闹或放弃。
- **一句话梗概**:东西打不开、事情太难的时候,我可以说"帮我一下"或递出求助卡,大人就会来帮我。

### 听懂两步指令:先……再…… / Following Two-Step Directions
- **技能**:communication_language → `labeling_receptive` · label 层(听懂并执行两步以上指令)
- **EBP**:`task_analysis`
- **cast**:solo_child
- **引用**:`sundberg_2008`(verify:true)、`steinbrenner_2020`(verify:false)、`cooper_2007`(verify:false)
- **学习目标(种子)**:孩子能独立听懂并按序完成常见的两步指令(如"先拿书,再坐下"),5 个中达成。
- **一句话梗概**:听到"先做这个,再做那个",我可以记住顺序,一步一步照着做完。

### 说说我今天做了什么 / Telling What I Did Today
- **技能**:communication_language → `narration_recount` · converse 层(复述刚发生的简单事件,说出 2–3 个要素)
- **EBP**:`video_modeling`
- **cast**:solo_child
- **引用**:`sundberg_2008`(verify:true)、`bellini_akullian_2007`(verify:true)、`steinbrenner_2020`(verify:false)
- **学习目标(种子)**:活动结束后,孩子能借图片顺序或提示说出刚发生事件的 2 个以上要素(谁、做了什么),5 次中≥3 次。
- **一句话梗概**:玩完或放学后,我可以说说刚才发生了什么——"我在公园荡秋千""我们搭了积木",把我做过的事讲给大人听。

### 你问我答:回答关于我的问题 / Answering Questions About Me
- **技能**:communication_language → `conversation` · converse 层(回答简单社交问题、你问我答)
- **EBP**:`video_modeling`
- **cast**:peer_play
- **引用**:`sundberg_2008`(verify:true)、`krantz_mcclannahan_1993`(verify:true)、`nac_2015`(verify:false)
- **学习目标(种子)**:被问到常见社交问题(叫什么名字、几岁、喜欢什么)时,孩子能恰当回答至少 3 类问题,并做一次简单的你问我答来回。
- **一句话梗概**:有人问"你叫什么名字""你喜欢什么"时,我能回答;我也可以反过来问对方,一来一回地聊上几句。

---

## 领域:生活自理与行为 daily_living_behavior

### 洗手六步 / Washing My Hands Step by Step
- **技能**:daily_living_behavior → `self_care` · prompted 层(按步骤完成洗手)
- **EBP**:`task_analysis`
- **cast**:solo_child
- **引用**:`bellini_akullian_2007`(verify:true)、`van_laarhoven_2010`(verify:true)、`cn_peizhi_2016`(verify:false)
- **学习目标(种子)**:孩子能在不超过 2 处提示下,按 卷袖→打湿→抹皂→搓洗→冲净→擦干 完成一次洗手。
- **一句话梗概**:洗手有六个小步骤,我照着流程卡一步一步做,就能把手洗得干干净净。

### 我会自己刷牙 / Brushing My Teeth
- **技能**:daily_living_behavior → `self_care` · prompted 层(按步骤完成刷牙)
- **EBP**:`video_modeling`
- **cast**:solo_child
- **引用**:`bellini_akullian_2007`(verify:true)、`van_laarhoven_2010`(verify:true)、`steinbrenner_2020`(verify:false)
- **学习目标(种子)**:孩子能在提示下,按 挤牙膏→上下刷→漱口→擦嘴 完成一次刷牙。
- **一句话梗概**:早晚我都自己刷牙:挤一点牙膏,上上下下刷一刷,再漱口、擦擦嘴,牙齿就变干净了。

### 上厕所的流程 / Using the Toilet
- **技能**:daily_living_behavior → `self_care` · prompted 层(按步骤完成如厕并事后洗手)
- **EBP**:`task_analysis`
- **cast**:solo_child
- **引用**:`bellini_akullian_2007`(verify:true)、`steinbrenner_2020`(verify:false)、`cn_peizhi_2016`(verify:false)
- **学习目标(种子)**:孩子能在提示下,按 进厕所→脱裤→如厕→冲水→提裤→洗手 完成一次如厕并事后洗手。
- **一句话梗概**:想上厕所时,我照着流程一步步来,最后别忘了冲水和洗手。
- *备注:如厕属敏感自理主题,成片前须专业人员与家长按孩子实际情况把关。*

### 尝一小口新食物 / Trying a New Food
- **技能**:daily_living_behavior → `mealtime_eating` · prompted 层(温和尝试一小口新食物,不强迫)
- **EBP**:`naturalistic_intervention`
- **cast**:solo_child
- **引用**:`bellini_akullian_2007`(verify:true)、`steinbrenner_2020`(verify:false)、`cn_peizhi_2016`(verify:false)
- **TODO_CITATION**:检索并核验"喂养/食物挑剔行为干预(如系统脱敏、SOS 喂养、行为喂养疗法)"的专项一手实证(citations.yaml 暂无对应 id),补齐后再回带到本选题。
- **学习目标(种子)**:在鼓励而非强迫下,孩子能按 看→闻→舔→尝一小口 逐级接近,并主动尝试一小口新食物 1 次。
- **一句话梗概**:遇到没吃过的食物,我先看一看、闻一闻、舔一舔,再勇敢尝一小口——不喜欢也没关系,我已经很棒了。
- *备注:需专业审核。喂养/食物挑剔属敏感专业主题,可能涉及口腔运动、感觉与医学因素,须喂养/作业治疗师与家长评估把关,严禁强迫喂食。*

### 收好玩具,物归原处 / Putting My Toys Away
- **技能**:daily_living_behavior → `chores_home` · prompted 层(收拾玩具、物归原处)
- **EBP**:`task_analysis`
- **cast**:solo_child
- **引用**:`steinbrenner_2020`(verify:false)、`cooper_2007`(verify:false)、`cn_peizhi_2016`(verify:false)
- **学习目标(种子)**:听到"收拾时间"提示后,孩子能在提示下把一组玩具按图卡放回对应的收纳盒/位置,1 次达成。
- **一句话梗概**:玩完以后,我把积木放回贴着图卡的盒子、把书放回架子上——每样东西都回到自己的家。

---

## 领域:游戏与休闲技能 play_leisure

### 假装喂娃娃:开始假装游戏 / Pretend Play: Feeding the Doll
- **技能**:play_leisure → `symbolic_play` · symbolic 层(把假装指向他人,以娃娃为承受者)
- **EBP**:`naturalistic_intervention`
- **cast**:solo_child
- **引用**:`westby_1980`(verify:true)、`lifter_1993`(verify:true)、`kasari_2006`(verify:false)
- **学习目标(种子)**:孩子能把≥2 个假装动作(用奶瓶喂饭、给娃娃盖被子)指向娃娃/玩偶,而不只是对自己做。
- **一句话梗概**:我可以假装照顾娃娃——喂它吃饭、哄它睡觉,像它是真的一样,这就是好玩的假装游戏。

### 输了也没关系:玩有规则的游戏 / Playing a Game and Coping with Losing
- **技能**:play_leisure → `games_with_rules` · social 层(参与有规则的游戏,遵守规则并接受输赢)
- **EBP**:`social_narratives`
- **cast**:peer_play
- **引用**:`chan_2009`(verify:true)、`nac_2015`(verify:false)、`steinbrenner_2020`(verify:false)
- **学习目标(种子)**:孩子能完整参与一局有规则的集体游戏(抢椅子/简单桌游),按回合行动,并在输一次时用应对语("下次再努力")保持平和,连续 3 局中≥2 局不升级为崩溃。
- **一句话梗概**:玩游戏时我按规则一轮一轮来;就算这局输了也没关系,我可以对自己说"下次再努力",继续开心地玩下一局。
- *备注:与已做《轮流与等待》不同,本课聚焦"有规则游戏中的输赢接纳";与认知灵活性域的"接受不行/等待"互为补充,不重复。*

### 自己安静玩一会儿:独立休闲 / Playing On My Own for a While
- **技能**:play_leisure → `independent_leisure` · independent 层(按活动清单/视觉日程独自恰当地玩一段时间)
- **EBP**:`visual_supports`
- **cast**:solo_child
- **引用**:`lee_2007`(verify:true)、`steinbrenner_2020`(verify:false)、`nac_2015`(verify:false)
- **学习目标(种子)**:在最少提示下,孩子能看活动清单从几项休闲活动中自选一项,独立进行≥10 分钟不需成人陪玩。
- **一句话梗概**:空下来的时候,我看看我的活动卡,自己选一样喜欢的事(看绘本、拼拼图),安安静静地玩一会儿。

---

## 领域:认知灵活性与问题解决 cognitive_flexibility

### 计划变了也没关系 / When Plans Change
- **技能**:cognitive_flexibility → `tolerating_change` · developing 层(应对未预告的意外,用应对语并转向替代方案)
- **EBP**:`cognitive_behavioral`
- **cast**:solo_child
- **引用**:`buron_curtis_2003`(verify:true)、`lee_2007`(verify:true)、`gray_garand_1993`(verify:false)、`nac_2015`(verify:false)
- **学习目标(种子)**:遇到未预告的变化时,孩子能说出一句应对语("没关系,换一个")并接受替代方案,3 次中≥2 次不升级为崩溃。
- **一句话梗概**:想做的事突然变了,我可以对自己说"没关系,还有别的办法",然后试试新的安排。

### 停一停,想一想 / Stop and Think
- **技能**:cognitive_flexibility → `self_monitoring` · developing 层(用"停一停—想一想—再行动"隔开冲动与反应)
- **EBP**:`cognitive_behavioral`
- **cast**:solo_child
- **引用**:`lee_2007`(verify:true)、`kuypers_2011`(verify:true)、`buron_curtis_2003`(verify:true)
- **学习目标(种子)**:在冲动情境中,孩子能自发使用"停一停—想一想—再行动",把冲动和反应隔开(每周记录≥3 次)。
- **一句话梗概**:想马上去做一件事之前,我先停一停、想一想再行动,这样更容易做出好的选择。

### 现在不行,等一下也没关系 / When the Answer Is "No" or "Wait"
- **技能**:cognitive_flexibility → `waiting_tolerating_no` · developing 层(接受"现在不行/等一下",自我平复并转向可做的事)
- **EBP**:`cognitive_behavioral`
- **cast**:solo_child
- **引用**:`lee_2007`(verify:true)、`wood_2009`(verify:false)、`nac_2015`(verify:false)
- **学习目标(种子)**:听到"现在不能/等一下"时,孩子能用一句自我对话("下次再买""等一下就好")平复自己并转向别的活动,3 次中≥2 次不升级为对抗或崩溃。
- **一句话梗概**:想要的东西现在还不能有,我可以对自己说"等一下就好、下次再说",先去做别的事,心里也不会那么难受。
- *备注:与已做《轮流与等待》(轮流机制)不同,本课落在认知灵活性域的"接受被拒与延迟",情境与技能均不同,不重复。*

---

## 领域:安全技能 safety_skills

### 过马路:停、等、看两边 / Crossing the Street Safely
- **技能**:safety_skills → `road_traffic` · guided 层(和大人一起过马路:等绿灯、看两边)
- **EBP**:`video_modeling`
- **cast**:solo_child
- **引用**:`bellini_akullian_2007`(verify:true)、`steinbrenner_2020`(verify:false)、`nac_2015`(verify:false)
- **学习目标(种子)**:在引导下,孩子过马路前能先在路缘停下、等绿灯、看两边后再随大人通过,连续 3 次达成。
- **一句话梗概**:过马路前,我先在路边停下来,等绿灯亮、看看左右两边都没车,再牵着大人一起走过去。
- *备注:安全技能是监护的补充而非替代;真实路口须成人严密监护,语气赋能、非恐吓。*

### 走失了怎么办:停在原地,找穿制服的人 / If I Get Lost
- **技能**:safety_skills → `getting_help_lost` · foundational→guided 层(走散时停在原地并找安全求助者)
- **EBP**:`video_modeling`
- **cast**:solo_child
- **引用**:`bergstrom_2012`(verify:true)、`bellini_akullian_2007`(verify:true)、`steinbrenner_2020`(verify:false)
- **学习目标(种子)**:与大人走散时,孩子能停在原地不乱跑,并走向一位穿制服的工作人员求助 1 次。
- **一句话梗概**:如果和大人走散了,我先停在原地不乱跑,再找穿制服的工作人员说"我找不到妈妈了"。

### 水边要小心 / Water Safety
- **技能**:safety_skills → `water_safety` · foundational 层(靠近水边会停下,没有大人不靠近、不下水)
- **EBP**:`video_modeling`
- **cast**:solo_child
- **引用**:`miltenberger_2008`(verify:true,安全技能 BST 通用框架,非水安全专项)、`steinbrenner_2020`(verify:false)、`nac_2015`(verify:false)
- **TODO_CITATION**:检索并核验"防溺水/泳池安全行为技能训练(BST)"的专项一手实证(citations.yaml 暂无对应 id),补齐后再回带到本选题。
- **学习目标(种子)**:靠近水边(泳池、河湖、浴缸)时,孩子能主动停下,没有大人不靠近、不下水,5 次中≥4 次。
- **一句话梗概**:到水边我先停下来,没有大人在身边就不靠近、不下水;要玩水一定先叫上大人。

### 火警响了怎么办:安全离开 / When the Fire Alarm Rings
- **技能**:safety_skills → `emergency_basics` · foundational→guided 层(识别火警/烟雾并配合逃生演练)
- **EBP**:`video_modeling`
- **cast**:solo_child
- **引用**:`bellini_akullian_2007`(verify:true)、`steinbrenner_2020`(verify:false)、`nac_2015`(verify:false)
- **学习目标(种子)**:听到火警铃声时,孩子能停下手上的事、跟随大人/队伍走安全出口到集合点、不躲藏,逃生演练中≤2 处提示完成全流程。
- **一句话梗概**:听到火警"叮铃铃",我先停下来,跟着老师和小朋友排好队,从安全出口走到外面集合,不害怕、不躲起来。
- *备注:需专业审核。紧急/安全主题须消防与专业人员把关;语气平静赋能、非恐吓,且安全技能是成人监护与真实演练的补充,不能替代。*

### 厨房和家里的安全 / Safe at Home
- **技能**:safety_skills → `home_safety` · foundational→guided 层(不碰灶台/热锅/刀具与药品清洁剂;陌生人敲门先找大人)
- **EBP**:`social_narratives`
- **cast**:solo_child
- **引用**:`miltenberger_2008`(verify:true)、`gray_garand_1993`(verify:false)、`steinbrenner_2020`(verify:false)、`nac_2015`(verify:false)
- **学习目标(种子)**:在情境演练中,孩子看到灶台/热锅/刀具或药品清洁剂时能后退不碰、想帮忙先叫大人;有人敲门时先去找大人,5 次中≥4 次。
- **一句话梗概**:厨房里的灶台、热锅和刀我不自己碰,想帮忙先叫大人;药品和清洁剂不乱开;有人敲门时,我先去找爸爸妈妈。
- *备注:需专业审核。居家安全须家长做好环境防护(炉具/药品/清洁剂上锁),本课是监护的补充而非替代;语气平静赋能、非恐吓。*

### 我信任的大人 / My Trusted Grown-Ups
- **技能**:safety_skills → `body_safety` · guided 层(认识 2–3 位可求助的信任的大人;"我的身体我做主")
- **EBP**:`social_narratives`
- **cast**:solo_child
- **引用**:`miltenberger_2008`(verify:true)、`gray_garand_1993`(verify:false)、`steinbrenner_2020`(verify:false)、`nac_2015`(verify:false)
- **学习目标(种子)**:孩子能说出或指出至少 2 位可以求助的"信任的大人";在角色扮演中,遇到让自己不舒服的接触能说"不,请停下"并去告诉一位信任的大人 1 次。
- **一句话梗概**:爸爸妈妈、老师是我信任的大人,有事我可以找他们;我的身体我做主,不舒服的时候我可以说"不",再去告诉信任的大人。
- *备注:需专业审核。身体安全属高敏感主题,须专业人员与家长按孩子理解水平,以平静、赋能、非恐吓的方式教授并个别化调整。*

---

## 领域:入学与课堂准备 school_readiness

### 举手等老师叫到我 / Raising My Hand and Waiting to Be Called
- **技能**:school_readiness → `waiting_turn_taking` · supported 层(举手并等待被叫到)
- **EBP**:`video_modeling`
- **cast**:peer_play
- **引用**:`steinbrenner_2020`(verify:false)、`nac_2015`(verify:false)、`cooper_2007`(verify:false)
- **学习目标(种子)**:想发言时,孩子能先举手并等待被老师叫到(≥5 秒)不喊出,提示≤1 次,5 次中≥4 次。
- **一句话梗概**:在课堂上想说话时,我先举手,安静地等老师叫到我的名字,再说出我的想法。

### 跟着全班一起做:听懂集体指令 / Following Group Directions
- **技能**:school_readiness → `following_group_instructions` · supported 层(借视觉提示或同伴示范跟随面向全班的 1–2 步指令)
- **EBP**:`visual_supports`
- **cast**:peer_play
- **引用**:`steinbrenner_2020`(verify:false)、`cooper_2007`(verify:false)、`nac_2015`(verify:false)
- **学习目标(种子)**:当老师对全班发出 1–2 步指令(如"把书翻到第 3 页并坐好")时,孩子仅需视觉提示或看同伴示范即完成,5 次中≥4 次。
- **一句话梗概**:老师对着全班说要做什么时,我看看墙上的步骤图卡、也看看旁边的小朋友,就能跟着大家一起照做。
- *备注:集体指令须在真实集体情境专门训练,1 对 1 会做不等于面向全班时会反应。*

### 我的工作篮:独立完成工作系统 / My Work Basket
- **技能**:school_readiness → `independent_work_system` · supported 层(依从左到右的视觉工作系统完成一组任务并转向下一活动)
- **EBP**:`task_analysis`
- **cast**:solo_child
- **引用**:`hume_odom_2007`(verify:true)、`steinbrenner_2020`(verify:false)、`cooper_2007`(verify:false)
- **学习目标(种子)**:借视觉工作系统("做什么/做多少/怎样算完成/接下来做什么"),孩子能独立完成一组(≥3 件)已掌握的任务并放入"完成"框,过程提示≤1 次。
- **一句话梗概**:我从左边拿任务,一件一件做完放到右边的"完成"框;看到"完成"标记,我就知道接下来该做什么。
- *备注:独立工作系统有直接实证(`hume_odom_2007`),但 TEACCH 整体疗效为小效应,勿夸大。*

---

## 领域:社区参与 community_participation

### 排队不插队 / Waiting in Line
- **技能**:community_participation → `public_behavior` · supported 层(排队跟着队伍等候、不插队)
- **EBP**:`video_modeling`
- **cast**:solo_child
- **引用**:`gray_garand_1993`(verify:false)、`steinbrenner_2020`(verify:false)、`nac_2015`(verify:false)
- **TODO_CITATION**:社区参与"特异性"一手实证(如超市/收银台排队、公共场所举止的行为干预研究)在 citations.yaml 尚无对应 id;现引用为通用循证锚点,商用前须补齐并核对原文。
- **学习目标(种子)**:在支持下,孩子能排队等候≥1 分钟、队伍前移时跟着走、轮到自己再上前,连续 3 次。
- **一句话梗概**:在收银台或洗手间前,我站在队伍后面慢慢等,队伍往前我就往前,轮到我了再上前。

### 自己买一样东西 / Buying One Thing Myself
- **技能**:community_participation → `shopping` · supported→independent 层(收银台付款流程→大人远处看护下独立完成小额购物)
- **EBP**:`video_modeling`
- **cast**:solo_child
- **引用**:`bellini_akullian_2007`(verify:true)、`steinbrenner_2020`(verify:false)、`nac_2015`(verify:false)
- **TODO_CITATION**:检索并核验"视频示范/视频提示教超市购物或自助结账"的社区参与特异性一手实证(citations.yaml 暂无对应 id,见 `skills/community_participation.yaml` 顶部 TODO_CITATIONS),补齐后再回带。
- **学习目标(种子)**:在大人远处看护下,孩子能拿一样常买商品到收银台、付款(或出示付款码)、等待并拿好东西离开,连续 2 次独立完成。
- **一句话梗概**:我可以自己拿一瓶水走到收银台,把它放上台、付钱、等一等,再拿好东西说"谢谢"走开。
- *备注:付钱的"进一元"数钱机制见 functional_academics `money_skills` 的《用"进一元"付钱》,本课聚焦"完整购物行为链",不重复;真实购物须成人在旁看护。*

### 谁能帮我?认识社区里的帮助者 / Who Can Help Me?
- **技能**:community_participation → `community_helpers_help` · emerging→supported 层(认识社区帮助者→需要时走向工作人员求助)
- **EBP**:`social_narratives`
- **cast**:solo_child
- **引用**:`bergstrom_2012`(verify:true)、`steinbrenner_2020`(verify:false)、`nac_2015`(verify:false)
- **学习目标(种子)**:孩子能在图片/实景中认出穿制服的工作人员(收银员、保安、服务员),并在需要时(找洗手间/找不到东西)走向一位工作人员表达需要,演练中≤2 次提示达成 1 次。
- **一句话梗概**:在商场或餐厅,穿制服的收银员、保安、服务员都是可以帮我的人;需要帮忙时,我可以走过去说"请帮帮我"。
- *备注:需专业审核。本课衔接安全域"走失求助"(见 safety_skills `getting_help_lost`),涉及走散/陌生人,须专业人员与家长按孩子理解水平把关,语气赋能非恐吓。*

### 去看医生/看牙医 / Going to the Doctor
- **技能**:community_participation → `appointments` · emerging→supported 层(预演流程→候诊安坐→配合检查关键步骤)
- **EBP**:`social_narratives`
- **cast**:solo_child
- **引用**:`bellini_akullian_2007`(verify:true)、`gray_garand_1993`(verify:false)、`steinbrenner_2020`(verify:false)、`nac_2015`(verify:false)
- **TODO_CITATION**:检索并核验"看诊/牙科脱敏与配合(社交叙事+视觉日程+分级暴露)"的社区参与特异性一手实证(见 `skills/community_participation.yaml` 顶部 TODO_CITATIONS,citations.yaml 暂无对应 id),补齐后再回带。
- **学习目标(种子)**:事前用社交故事预演后,孩子能进入诊室并在候诊区安坐等待≥5 分钟(可用等待包/计时器),并配合完成检查的≥2 个关键步骤(如张嘴、量身高)。
- **一句话梗概**:去看医生前,我先看"看医生"的小故事知道会发生什么;到了先安静地在候诊室等,轮到我时张开嘴、配合医生检查。
- *备注:需专业审核。就医/牙科属医疗敏感主题,须专业人员与家长按孩子情况把关,配合分级暴露与预演,语气赋能、非恐吓。*

---

## 领域:职业前与工作准备 prevocational

### 卡住时求助,并听取反馈 / Asking for Help and Taking Feedback at Work
- **技能**:prevocational → `help_and_feedback` · emerging→supported 层(卡住/缺料时求助;接受纠正并据反馈修改)
- **EBP**:`video_modeling`
- **cast**:none(题材面向大龄儿童/青少年的作业情境,与学前主角差异大,只保留风格串、场景另配)
- **引用**:`lee_2007`(verify:true)、`steinbrenner_2020`(verify:false)、`cooper_2007`(verify:false)
- **学习目标(种子)**:作业卡住或缺料时,孩子能用求助卡或语言发起"帮我一下",并在被纠正后据反馈修改,不逃避或发脾气(5 次中≥4 次)。
- **一句话梗概**:做作业遇到装不上、材料用完时,我可以举求助卡说"帮我一下";别人告诉我怎么改,我就照着改过来。

### 分类与配对:做我的第一份手上作业 / Sorting and Matching Work
- **技能**:prevocational → `functional_work_tasks` · emerging→supported 层(单维度分类/配对→依样板或视频提示完成多步装配/包装)
- **EBP**:`video_modeling`
- **cast**:none(面向大龄儿童/青少年的作业情境,与学前主角差异大,只保留风格串、场景另配)
- **引用**:`van_laarhoven_2010`(verify:true)、`allen_2010`(verify:true)、`steinbrenner_2020`(verify:false)
- **学习目标(种子)**:孩子能按单一维度(大小/颜色/类别)独立完成分类或配对(准确率≥80%),并依样板/视频提示完成一件多步装袋或装配,过程提示≤1 次。
- **一句话梗概**:我看着视频一步一步学,把螺丝按大小分进盒子、把文具装进袋子封好——这是我能独立做完的第一份小作业。

### 工具用完放回原位 / Putting My Tools Back
- **技能**:prevocational → `tool_material_care` · supported 层(用完把工具与材料整理归位,保持工位整洁)
- **EBP**:`video_modeling`
- **cast**:none(面向大龄儿童/青少年的作业情境,与学前主角差异大,只保留风格串、场景另配)
- **引用**:`bellini_akullian_2007`(verify:true)、`steinbrenner_2020`(verify:false)、`cooper_2007`(verify:false)
- **学习目标(种子)**:完成作业后,孩子能看视频示范把工具与材料放回对应轮廓位/收纳格、把废料丢进垃圾盒,仅需≤1 次提示,5 次中≥4 次。
- **一句话梗概**:活儿做完了,我看着示范把剪刀、胶水放回它们的位置,把桌面收拾干净——下次用起来又快又顺手。

---

## 领域:功能性学业·生活数学 functional_academics

### 用"进一元"付钱买东西 / Paying with the Next-Dollar Strategy
- **技能**:functional_academics → `money_skills` · developing 层("进一元"付钱策略)
- **EBP**:`video_modeling`
- **cast**:solo_child
- **引用**:`steinbrenner_2020`(verify:false)、`cooper_2007`(verify:false)、`cn_peizhi_2016`(verify:false)
- **学习目标(种子)**:面对几元几角的价格,孩子能用"进一元"策略数出上一个整元数付款(如标价 3 元 5 角付 4 元),3 个价格中≥2 次付对。
- **一句话梗概**:买东西时看价签,几元几角我就付上一个整元数——比如 3 块 5 就数出 4 块钱,不用心算找零也能付对。

### 看时钟,按作息做事 / Telling Time for My Routine
- **技能**:functional_academics → `time_clock` · developing 层(读整点/半点并与日常活动对应)
- **EBP**:`visual_supports`
- **cast**:solo_child
- **引用**:`steinbrenner_2020`(verify:false)、`cn_peizhi_2016`(verify:false)、`nac_2015`(verify:false)
- **学习目标(种子)**:孩子能读出指针钟的整点与半点,并把 3 个时间与对应的日常活动正确配对(如"12 点吃午饭、7 点半刷牙、9 点睡觉")。
- **一句话梗概**:我会看时钟——长针指到 12 是整点、指到 6 是半点;看到几点,我就知道该吃饭、该刷牙还是该睡觉了。

### 看懂我的视觉日程 / Reading My Visual Schedule
- **技能**:functional_academics → `schedule_reading` · functional 层(用日程/时间表自我管理一天并逐项勾掉)
- **EBP**:`visual_supports`
- **cast**:solo_child
- **引用**:`lee_2007`(verify:true)、`steinbrenner_2020`(verify:false)、`nac_2015`(verify:false)
- **学习目标(种子)**:孩子能看图片日程知道"现在/接下来",独立照日程完成 3 项活动并逐项勾掉。
- **一句话梗概**:我看着日程条,就知道现在做什么、接下来做什么;做完一项我就打个勾,一步步把今天的事做完。
- *备注:"先……再……"的过渡与情绪面见 cognitive_flexibility `transitions`;本课聚焦"读懂并自我管理日程"的功能性学业面,不重复。*

---

## 领域:运动与感觉调节 motor_sensory

### 我需要休息:请求感觉/运动休息 / I Need a Break
- **技能**:motor_sensory → `sensory_regulation_supports` · functional 层(主动请求休息或感觉工具并独立调节)
- **EBP**:`visual_supports`
- **cast**:solo_child
- **引用**:`steinbrenner_2020`(verify:false)、`nac_2015`(verify:false)、`schaaf_2014`(verify:true;感觉处理干预证据**新兴且混杂**,仅作背景,勿据此宣称改善核心症状)
- **学习目标(种子)**:感到过载(太吵/太挤/太亮)时,孩子能用语言或图卡主动请求"我需要休息",并到安静角或做一次运动休息后自我平复(每周记录≥3 次)。
- **一句话梗概**:当身体觉得太吵、太挤、受不了时,我可以出示"休息"卡,去安静角待一会儿或动一动,让自己缓过来。
- *备注:本选题定位为"以感觉为基础的自我调节支持",非"感觉统合治疗";涉及感觉处理的方案宜由作业治疗师参与,勿夸大疗效。*

### 扣扣子、拉拉链:我的能干小手 / Buttons and Zippers
- **技能**:motor_sensory → `fine_motor` · functional 层(扣扣子、拉拉链等自理相关精细动作)
- **EBP**:`video_modeling`
- **cast**:solo_child
- **引用**:`van_laarhoven_2010`(verify:true)、`steinbrenner_2020`(verify:false)、`cooper_2007`(verify:false)
- **学习目标(种子)**:孩子能独立扣好或解开 3 颗中等大小的纽扣、把外套拉链拉到顶端,5 次中≥4 次成功。
- **一句话梗概**:我的小手越来越能干——看着视频一步步学,我可以自己扣纽扣、拉拉链,把衣服穿整齐。

### 一起上体育课 / Joining PE with Everyone
- **技能**:motor_sensory → `daily_movement_participation` · developing→functional 层(参与结构化体育/律动:排队、听口令、遵守规则轮流)
- **EBP**:`video_modeling`
- **cast**:peer_play
- **引用**:`bellini_akullian_2007`(verify:true)、`steinbrenner_2020`(verify:false)、`nac_2015`(verify:false)
- **学习目标(种子)**:体育或律动课上,孩子能排队、听口令"开始/停"做动作并完成≥3 个环节;在有规则的运动游戏(传球/接力)中遵守规则参与到结束,3 次中≥2 次。
- **一句话梗概**:上体育课我和大家一起排队、听老师口令做动作;玩传球游戏时,我等到轮到自己再传,和小朋友一起玩到最后。

---

## 汇总(便于日后排期)

- **选题总数**:45 条(在原 32 条基础上新增 13 条;覆盖全部 12 个技能域,各≥3 条)。每条锚定一个**全新且未被复用**的 skill_area id。
- **本轮新增(13 条)分布**:优先加厚原先各仅 2 条的 5 个薄弱域,再补高价值缺口(居家/身体安全、就医、喂养、整理)——emotional_regulation ×2 · social_interaction ×2 · communication_language ×2 · daily_living_behavior ×2 · safety_skills ×2 · prevocational ×1 · motor_sensory ×1 · community_participation ×1。
  - 新锚定的全新 skill_area:emotional_regulation `recognize_name`/`coping_specific` · social_interaction `cooperative_play`/`perspective_taking` · communication_language `narration_recount`/`conversation` · daily_living_behavior `mealtime_eating`/`chores_home` · safety_skills `home_safety`/`body_safety` · prevocational `tool_material_care` · motor_sensory `daily_movement_participation` · community_participation `appointments`。
- **全库技能域分布(45 条)**:safety_skills ×6 · daily_living_behavior ×5 · emotional_regulation ×4 · social_interaction ×4 · communication_language ×4 · community_participation ×4 · play_leisure ×3 · cognitive_flexibility ×3 · school_readiness ×3 · functional_academics ×3 · prevocational ×3 · motor_sensory ×3。
- **method_id 分布(45 条,均为 `knowledge/methods/_registry.yaml` 真实 id)**:`video_modeling` ×18 · `visual_supports` ×6 · `cognitive_behavioral` ×5 · `task_analysis` ×5 · `social_narratives` ×5 · `naturalistic_intervention` ×3 · `social_skills_training` ×2 · `peer_based_intervention` ×1。
- **cast 分布(取自 `autismcare/cast.py`)**:solo_child ×32 · peer_play ×10 · none ×3。
- **TODO_CITATION(5 处,须联网核验后补库,严禁臆造)**:
  1. 防溺水/泳池安全行为技能训练(BST)专项实证 —— 支撑《水边要小心》(safety_skills `water_safety`)。
  2. 社区参与特异性一手实证(超市/排队/公共场所举止干预)—— 支撑《排队不插队》(community_participation `public_behavior`)。
  3. 视频示范/视频提示教超市购物或自助结账的社区参与特异性实证 —— 支撑《自己买一样东西》(community_participation `shopping`)。
  4. 喂养/食物挑剔行为干预(系统脱敏、SOS 喂养、行为喂养疗法)专项实证 —— 支撑《尝一小口新食物》(daily_living_behavior `mealtime_eating`)。
  5. 看诊/牙科脱敏与配合(社交叙事+视觉日程+分级暴露)社区参与特异性实证 —— 支撑《去看医生/看牙医》(community_participation `appointments`)。
- **敏感主题(须"需专业审核",已在条目内标注)**:本轮新增《厨房和家里的安全》(safety_skills `home_safety`)、《我信任的大人》(safety_skills `body_safety`)、《去看医生/看牙医》(community_participation `appointments`,医疗)、《尝一小口新食物》(daily_living_behavior `mealtime_eating`,喂养);连同原有《火警响了怎么办》《谁能帮我?》及如厕、走失、水边、身体安全等条目,正式成片前须专业人员与家长把关。
- **纪律确认**:本轮每个 skill_area id、method_id、citation id 均逐字核对自 `knowledge/skills/*.yaml`、`knowledge/methods/_registry.yaml`、`knowledge/citations.yaml`;verify 状态与 `citations.yaml` 一致;13 个新 skill_area 均未与原 32 条及 2 条已完成课(`sharing_requesting`/`turn_taking`)重复;所有选题均为「需专业审核草稿」概念,只积累选题、不产出成片。
