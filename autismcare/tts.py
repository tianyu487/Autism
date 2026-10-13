"""配音层:可切换后端的中英双语旁白合成。

后端由环境变量 AUTISMCARE_TTS 选择(CLI 的 --tts 会设置它):
- "edge"  : edge-tts,免费、无需密钥、需联网(默认)。
- "azure" : 微软 Azure 语音(REST + SSML),支持 gentle/affectionate 等情感风格,更自然;
            需 AZURE_SPEECH_KEY 与 AZURE_SPEECH_REGION。

对上层保持同一接口 synth(text, lang, out_path);换后端只改这里。
音色偏平和、语速偏慢,更适合自闭症儿童(清晰、可预期)。
"""

from __future__ import annotations

import asyncio
import os
import time
from pathlib import Path
from xml.sax.saxutils import escape

# 默认中英文语音(可用环境变量覆盖)。
ZH_VOICE = "zh-CN-XiaoxiaoNeural"
EN_VOICE = "en-US-JennyNeural"
DEFAULT_RATE = "-12%"      # edge-tts 用;偏慢
DEFAULT_PITCH = "+0Hz"

# Azure 用:略慢一点即可(Azure 神经语音本身更自然,不宜过慢),以及情感风格。
AZURE_DEFAULT_RATE = "-6%"
AZURE_DEFAULT_STYLE = "gentle"   # gentle 温柔 / affectionate 亲切 / calm 平静 / cheerful 轻快


def backend() -> str:
    return os.environ.get("AUTISMCARE_TTS", "edge").lower()


def zh_voice() -> str:
    return os.environ.get("AUTISMCARE_ZH_VOICE", ZH_VOICE)


def en_voice() -> str:
    return os.environ.get("AUTISMCARE_EN_VOICE", EN_VOICE)


# --------------------------------------------------------------------------
# edge-tts 后端(免费)
# --------------------------------------------------------------------------
async def _edge_async(text: str, voice: str, out_path: Path, rate: str, pitch: str) -> None:
    import edge_tts

    communicate = edge_tts.Communicate(text, voice, rate=rate, pitch=pitch)
    await communicate.save(str(out_path))


def _synth_edge(text: str, lang: str, out_path: Path, rate: str, pitch: str) -> None:
    voice = zh_voice() if lang.startswith("zh") else en_voice()
    asyncio.run(_edge_async(text, voice, out_path, rate, pitch))


# --------------------------------------------------------------------------
# Azure 语音后端(REST + SSML,支持情感风格,更自然)
# --------------------------------------------------------------------------
def _synth_azure(text: str, lang: str, out_path: Path, rate: str) -> None:
    import urllib.request

    key = os.environ.get("AZURE_SPEECH_KEY")
    region = os.environ.get("AZURE_SPEECH_REGION")
    if not key or not region:
        raise RuntimeError(
            "使用 Azure 需要设置 AZURE_SPEECH_KEY 和 AZURE_SPEECH_REGION(见 .env.example)。"
        )
    voice = zh_voice() if lang.startswith("zh") else en_voice()
    style = os.environ.get("AUTISMCARE_AZURE_STYLE", AZURE_DEFAULT_STYLE) if lang.startswith("zh") else ""
    xml_lang = "zh-CN" if lang.startswith("zh") else "en-US"
    # Azure 用相对百分比语速;沿用传入的 rate(如 -6%)。
    inner = f'<prosody rate="{rate}">{escape(text)}</prosody>'
    if style:
        inner = f'<mstts:express-as style="{style}" styledegree="1">{inner}</mstts:express-as>'
    ssml = (
        '<speak version="1.0" '
        'xmlns="http://www.w3.org/2001/10/synthesis" '
        'xmlns:mstts="https://www.w3.org/2001/mstts" '
        f'xml:lang="{xml_lang}">'
        f'<voice name="{voice}">{inner}</voice></speak>'
    )
    url = f"https://{region}.tts.speech.microsoft.com/cognitiveservices/v1"
    req = urllib.request.Request(
        url, data=ssml.encode("utf-8"), method="POST",
        headers={
            "Ocp-Apim-Subscription-Key": key,
            "Content-Type": "application/ssml+xml",
            "X-Microsoft-OutputFormat": "audio-24khz-48kbitrate-mono-mp3",
            "User-Agent": "autismcare",
        },
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        audio = resp.read()
    if not audio:
        raise RuntimeError("Azure 返回空音频。")
    Path(out_path).write_bytes(audio)


# --------------------------------------------------------------------------
# 统一入口
# --------------------------------------------------------------------------
def synth(text: str, lang: str, out_path: Path,
          rate: str | None = None, pitch: str = DEFAULT_PITCH) -> Path:
    """合成一段语音到 out_path(mp3)。lang: 'zh' | 'en'。返回 out_path。

    这是可替换的核心接口:换 TTS 提供商时保持本函数签名不变即可。
    """
    text = (text or "").strip()
    if not text:
        raise ValueError("TTS 文本为空。")
    out_path = Path(out_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)

    be = backend()
    last_err: Exception | None = None
    for attempt in range(4):
        try:
            if be == "azure":
                _synth_azure(text, lang, out_path, rate or AZURE_DEFAULT_RATE)
            else:
                _synth_edge(text, lang, out_path, rate or DEFAULT_RATE, pitch)
            if out_path.exists() and out_path.stat().st_size > 0:
                return out_path
            raise RuntimeError("TTS 输出为空文件。")
        except Exception as e:  # noqa: BLE001 —— 外部服务抖动,统一重试
            last_err = e
            if attempt < 3:
                time.sleep(0.6 * (attempt + 1))
    raise RuntimeError(f"TTS 合成失败(后端={be},已重试):{last_err}")


def synth_scene_bilingual(narration_zh: str, narration_en: str, out_dir: Path, index: int
                          ) -> tuple[Path, Path]:
    """为一个场景生成中、英两段配音,返回 (zh_mp3, en_mp3)。"""
    out_dir = Path(out_dir)
    zh_path = synth(narration_zh, "zh", out_dir / f"scene_{index:02d}_zh.mp3")
    en_path = synth(narration_en, "en", out_dir / f"scene_{index:02d}_en.mp3")
    return zh_path, en_path
