"""插画层:为每一页生成"精美且符合内容"的感官友好绘本插画。

默认后端 Pollinations(免费、无需 key、基于 Flux),按画面描述生成柔和扁平的绘本插画。
可用环境变量 AUTISMCARE_IMAGE 切换:
  - "pollinations"(默认):调用免费图像服务生成插画;
  - "none":关闭插画,回退到极简图标页(离线/无网时也可用)。
所有请求只发送画面英文描述(不含个人信息);结果按文件名缓存,重复运行不重复请求。

这是可替换接口:将来接入付费图像模型(更高质量/角色一致)时,只改本文件。

说明(2026-07-13):在原始风格基础上只做一处最小修改——生成前把提示词里
的引号对白/句子剥掉(见 visual_prompt),从根源避免 Flux 把字幕文字"照着写"
成背景乱码;风格与 seed 保持原样,人物表情/画风与最初一致。

说明(2026-07-14):illustration() 新增 anchors 参数——在清洗之后追加"固定角色
关键词块 + 场景锚点"(由 cast.py 提供、pipeline 自动注入),让同一角色跨页/跨视频
复现。风格一致由三根支柱共同保证:统一 STYLE 串 + 固定 seed 4242 + cast 角色锚点。
详见 design/visual_style_bible.md。
"""

from __future__ import annotations

import os
import re
import time
import urllib.parse
import urllib.request
from pathlib import Path

# 统一的感官友好绘本风格(柔和、扁平、低刺激)——注入每个提示词。
# 眼睛执行标准(2026‑07‑15):全局强调"清晰黑色瞳孔 + 眼白、正常人物外貌",
# 与 cast.EYES(逐角色)双保险,避免 Flux 画出无神/异常/无眼白的眼睛。
STYLE = ("children's picture book illustration, soft flat vector art, "
         "gentle muted pastel palette, simple clean rounded shapes, "
         "minimal calm background, warm cozy soft lighting, cute friendly characters, "
         "characters with clear well-defined eyes, round dark-black pupils and visible white sclera, "
         "natural human-like eyes, expressive friendly faces, "
         "sensory-friendly, wholesome, high quality, no text, no words, no letters")

# 固定 seed → 全片风格更一致(不同页仍是不同画面)。
SEED = int(os.environ.get("AUTISMCARE_IMAGE_SEED", "4242"))

# 引号里的对白会被 Flux "照着写"进画面(变成背景乱码文字);对白引导词同理。
# 生成前删掉所有引号/撇号字符 + 对白动词 + 问句,只留纯视觉场景,从根源消字。
# (只清洗提示词、不改风格与 seed,人物表情/画风保持原样。)
_QUOTES = re.compile(r"[\"'`“”‘’『』「」《》]")
_SPEECH = re.compile(r"\b(I can say|you can say|we can say|I say|say|says|said|"
                     r"tell|tells|told|ask|asks|asked|speak|talk|talking|reads?)\b", re.I)


def visual_prompt(desc: str) -> str:
    """把一段可能含对白/句子的描述,清洗成纯视觉场景描述(避免 Flux 画出文字)。"""
    s = _QUOTES.sub("", desc)           # 删除所有引号/撇号字符
    s = _SPEECH.sub(" ", s)             # 去掉"说/问/念"等会触发文字的动词
    s = re.split(r"[?？]", s)[0]         # 丢掉问句部分(常触发"标语"式文字)
    s = re.sub(r"\s+", " ", s).strip(" ,.;:!?，。;:")
    if len(s.split()) < 3:              # 清洗后信息过少 → 退回安全的通用儿童场景
        return "a warm gentle scene of friendly young children"
    return s


def backend() -> str:
    return os.environ.get("AUTISMCARE_IMAGE", "pollinations").lower()


def _pollinations(prompt: str, out_path: Path, seed: int) -> None:
    q = urllib.parse.quote(f"{prompt}, {STYLE}", safe="")
    url = (f"https://image.pollinations.ai/prompt/{q}"
           f"?width=1024&height=768&model=flux&nologo=true&seed={seed}")
    req = urllib.request.Request(url, headers={"User-Agent": "autismcare"})
    with urllib.request.urlopen(req, timeout=120) as resp:
        data = resp.read()
    if not data or len(data) < 2000:
        raise RuntimeError("插画返回内容异常(过小)。")
    Path(out_path).write_bytes(data)


def illustration(prompt_en: str, out_path: Path, seed: int | None = None,
                 anchors: str | None = None) -> Path | None:
    """为一段画面描述生成插画;失败或关闭时返回 None(调用方回退到图标页)。

    anchors:固定角色关键词块 + 场景锚点(见 cast.py),在清洗之后追加,
    保证角色描述不被清洗器的问句/对白剪裁掉——从而跨页/跨视频复现同一角色。
    带缓存:out_path 已存在且非空则直接复用,便于反复调试不重复请求。
    """
    if backend() == "none":
        return None
    out_path = Path(out_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    if out_path.exists() and out_path.stat().st_size > 2000:
        return out_path

    prompt_en = visual_prompt(prompt_en)          # 先清洗掉对白/句子,防止画面出现文字
    if anchors:                                   # 再追加固定角色/场景锚点(不参与清洗,确保存活)
        prompt_en = f"{prompt_en}, {anchors}"
    seed = SEED if seed is None else seed
    # 抗抖动:图像服务偶发超时/抖动会导致回退到“图标页”(与绘本画风不一致)。
    # 多次重试 + 退避,尽量让每页都拿到真正的插画;次数可用环境变量覆盖。
    attempts = int(os.environ.get("AUTISMCARE_IMAGE_RETRIES", "8"))
    last: Exception | None = None
    for attempt in range(attempts):
        try:
            _pollinations(prompt_en, out_path, seed)
            return out_path
        except Exception as e:  # noqa: BLE001 —— 外部服务抖动,多次重试后才回退
            last = e
            time.sleep(min(3.0 * (attempt + 1), 20))
    print(f"    · 插画生成失败(重试 {attempts} 次仍失败,回退到图标页):{last}")
    return None
