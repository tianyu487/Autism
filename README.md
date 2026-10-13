# 循证疗愈内容生成器 · autismcare

面向自闭症儿童的**循证**心理疗愈内容生成器(MVP)。
第一条竖线已打通:**一个目标场景 → Claude 依据「社交故事(Social Stories™)」循证规则生成中英双语脚本 → edge-tts 双语配音 → 程序化生成低刺激幻灯 → ffmpeg 合成中英双语成品 mp4 → 打包(脚本 / 引用 / 使用指南 / 免责声明)**。

> ⚠️ **重要免责**:本工具产出为**辅助 / 教育工具**,不构成医疗建议,**不替代专业评估、诊断或治疗**,不做任何“治愈 / 疗效”承诺。所有产物默认标记为**需专业人员审核的草稿**;面向家庭售卖前必须经特教老师 / 康复师审核并按孩子实际情况调整。

---

## 特性

- **循证骨架 + AI 填充**:方法规则、句型基本比、引用来源在 `knowledge/` 中结构化管理,注入 Claude 作为硬约束。
- **中英双语**:屏幕文字中英双语;**默认只朗读中文旁白,英文仅作画面字幕**(加 `--en-audio` 可同时朗读英文)。
- **感官友好画面**:程序化生成的低刺激、柔和配色、大字清晰、布局一致、带进度指示的幻灯(比 AI 花哨插图更循证、更稳定)。
- **免密钥兜底**:配音用免费 edge-tts;视频用 `imageio-ffmpeg` 自带二进制;`--no-ai` 可在无 Claude 密钥时跑通整条媒体管线。
- **安全门禁**:自动校验句型配比、第一人称、正向 / 字面表达,拦截恐吓 / 负面用语;每份产物附中英免责声明与引用。

## 安装

```bash
pip install -r requirements.txt
```

- Python 3.10+;Windows 已内置中文字体(微软雅黑)与彩色 emoji 字体(Segoe UI Emoji)。
- 跨平台建议额外安装 **Noto Sans SC** 放到 `assets/fonts/`,保证中文渲染。
- **无需**手动安装系统 ffmpeg(`imageio-ffmpeg` 自带静态二进制);若已装系统 ffmpeg 会优先使用。

## 配置密钥

复制 `.env.example` 为 `.env`,填入 Anthropic API 密钥:

```
ANTHROPIC_API_KEY=sk-ant-xxxx
# 可选:AUTISMCARE_MODEL=claude-opus-4-8   # 默认 claude-opus-4-8
```

## 用法

```bash
# 用配置文件(推荐)
python -m autismcare generate --config config/example_story.yaml

# 免密钥 / 离线,用内置样例脚本跑通媒体管线(验证画面+配音+合成)
python -m autismcare generate --config config/example_story.yaml --no-ai

# 直接用命令行参数
python -m autismcare generate --situation "第一天上幼儿园" --name 乐乐 --age 5
```

常用参数:`--out`(输出根目录,默认 `output`)、`--model`、`--slug`、`--keep-temp`、`--en-audio`(同时朗读英文)。

### 无 API 的用法(推荐:Claude Code 现场生成 → `--script`)

不想用付费 API 时,让 Claude(如本 Claude Code 会话)按 `knowledge/` 的循证规则直接生成一份脚本 `scripts/xxx.json`,再喂给管线,**全程免费、离线合成**:

```bash
python -m autismcare generate --script scripts/lele_dentist.json --slug lele_dentist
```

- `script.json` 的结构见 `autismcare/models.py` 的 `StoryScript`(标题、学习目标、场景数组、引用、复核标记)。
- 生成前建议先过一遍安全门禁:`validate_script()` 会校验句型基本比、第一人称、正向/字面表达。
- 也可手动编辑 `scripts/xxx.json` 里的任意句子,重跑同一命令即可更新视频。

### 输入(config/example_story.yaml)

```yaml
child_name: 乐乐
age: 6
situation: 第一次去看牙医        # 必填:目标场景 / 情境
goal: 帮助孩子理解看牙医的流程,减少焦虑
interests: [恐龙, 小汽车]
sensory_notes: 对强光和尖锐声音敏感
reading_level: simple            # simple | medium
project_slug: dentist_visit      # 输出文件夹名(留空自动生成)
```

### 输出(output/&lt;slug&gt;/)

```
final.mp4          # 成品视频(1280x720,中英双语字幕 + 中文旁白;若未过校验则名为 final_DRAFT_needs_fix.mp4)
script.json        # 结构化脚本(含句型标注、引用、复核标记)
script.md          # 人类可读的双语脚本
citations.md       # 引用来源
guide.md           # 家长 / 老师使用指南 + 校验结果 + 售卖前复核清单
DISCLAIMER.txt     # 中英免责声明
scenes/            # 每屏幻灯 PNG(可用于二次剪辑)
```

## 项目结构

```
autismcare/          # Python 包
  models.py          # 数据模型(pydantic)
  knowledge.py       # 加载循证方法库 / 引用 / 安全规则
  generate.py        # 构造受约束 Prompt + 调 Claude 结构化输出;含 --no-ai 样例脚本
  validate.py        # 社交故事 lint + 安全门禁
  tts.py             # edge-tts 双语配音(可替换接口)
  render.py          # Pillow 渲染低刺激双语幻灯
  video.py           # ffmpeg 合成 / 拼接成片
  package.py         # 输出打包(脚本 / 引用 / 指南 / 免责)
  pipeline.py        # 端到端编排
  cli.py             # 命令行入口
knowledge/           # 循证方法库(数据,可编辑 / 补充)
  methods/social_stories.yaml
  citations.yaml
  safety_rules.yaml
config/example_story.yaml
```

## 循证依据

第一版方法库聚焦 **Social Stories™(Carol Gray)**,规则(第一人称、正向、字面、句型基本比等)与引用见 `knowledge/`。
社交叙事 / 视觉支持被多项综述与标准(如 Wong et al. 2015;National Standards Project, 2015)列为循证实践。
**引用条目在商用前请核对原文卷期 / 页码 / DOI**(见 `knowledge/citations.yaml` 中 `verify: true` 的条目)。

## 路线图(后续)

- 泛化到「个性化干预活动方案」「情绪 / 社交技能」等更多内容类型(先复用文本层)。
- 「课程 = 多视频系列」的批量合辑与售卖包装。
- 可替换 TTS 接口接入更自然的商用中文语音;可选简笔插画素材库。
- Web / 桌面界面。
