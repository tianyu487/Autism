"""合成层:用 ffmpeg 把 幻灯 PNG + 双语配音 合成为成品 mp4。

- ffmpeg 二进制优先用系统的;没有则回退到 imageio-ffmpeg 自带的静态二进制,
  因此无需用户手动安装系统 ffmpeg。
- 每屏:中文配音 → 短停顿 → 英文配音 → 结尾停顿;画面停留时长跟随配音(-shortest)。
- 各屏片段编码参数一致,最后用 concat демuxer 无损拼接。
字幕即画面上的双语句子本身(社交故事的核心就是“图+字”),无需额外烧字幕。
"""

from __future__ import annotations

import shutil
import subprocess
from pathlib import Path

FPS = 25
AUDIO_RATE = 24000          # edge-tts 输出约 24kHz 单声道
SCENE_GAP = 0.6             # 中英之间的停顿(秒)
SCENE_TAIL = 0.9            # 每屏结尾的停顿(秒)
CANVAS_W, CANVAS_H = 1280, 720   # 标准幻灯尺寸(与 render 一致)。任何尺寸的手改图都
                                 # 归一到此:等比缩放贴合 + 白边填充 + 偶数边,保证各屏
                                 # 分辨率一致(concat 无损拼接要求)且 libx264 可编码。


def ffmpeg_exe() -> str:
    """返回可用的 ffmpeg 可执行文件路径。"""
    sys_ff = shutil.which("ffmpeg")
    if sys_ff:
        return sys_ff
    try:
        import imageio_ffmpeg
        return imageio_ffmpeg.get_ffmpeg_exe()
    except Exception as e:  # pragma: no cover
        raise RuntimeError(
            "未找到 ffmpeg。请安装系统 ffmpeg,或 `pip install imageio-ffmpeg`。"
        ) from e


def _run(cmd: list[str]) -> None:
    proc = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")
    if proc.returncode != 0:
        tail = (proc.stderr or "")[-1500:]
        raise RuntimeError(f"ffmpeg 失败(exit {proc.returncode}):\n{tail}")


def make_scene_audio(zh_mp3: Path, en_mp3: Path | None, out_audio: Path,
                     gap: float = SCENE_GAP, tail: float = SCENE_TAIL) -> Path:
    """拼接场景音频 → 单个音频(m4a/aac)。

    - en_mp3 提供时:中文 + 停顿 + 英文 + 结尾停顿(双语配音);
    - en_mp3 为 None 时:中文 + 结尾停顿(只读中文,英文仅作画面字幕)。
    """
    ff = ffmpeg_exe()
    out_audio = Path(out_audio)
    silence = f"anullsrc=channel_layout=mono:sample_rate={AUDIO_RATE}"
    fmt = f"aformat=sample_rates={AUDIO_RATE}:channel_layouts=mono"

    inputs = ["-i", str(zh_mp3)]
    if en_mp3 is not None:
        inputs += ["-f", "lavfi", "-t", str(gap), "-i", silence,
                   "-i", str(en_mp3)]
    inputs += ["-f", "lavfi", "-t", str(tail), "-i", silence]

    n = 4 if en_mp3 is not None else 2
    fmt_stages = "".join(f"[{i}:a]{fmt}[a{i}];" for i in range(n))
    concat_ins = "".join(f"[a{i}]" for i in range(n))
    filt = f"{fmt_stages}{concat_ins}concat=n={n}:v=0:a=1[out]"

    cmd = [ff, "-y", *inputs,
           "-filter_complex", filt, "-map", "[out]",
           "-c:a", "aac", "-b:a", "160k", str(out_audio)]
    _run(cmd)
    return out_audio


def make_scene_clip(image_png: Path, audio: Path, out_mp4: Path) -> Path:
    """静态图 + 音频 → 一屏视频片段(时长=音频时长)。"""
    ff = ffmpeg_exe()
    out_mp4 = Path(out_mp4)
    # 归一到标准画布:等比缩放到不超过 1280x720,再白边补齐到精确 1280x720,SAR=1。
    # 标准页本就是 1280x720(此滤镜对其为恒等);手改的异尺寸图会被安全归一,不再让 libx264
    # 因奇数边/尺寸不一而报错,也保证与其它片段同分辨率以便 concat 无损拼接。
    vf = (f"scale={CANVAS_W}:{CANVAS_H}:force_original_aspect_ratio=decrease,"
          f"pad={CANVAS_W}:{CANVAS_H}:(ow-iw)/2:(oh-ih)/2:color=white,setsar=1")
    cmd = [
        ff, "-y",
        "-loop", "1", "-i", str(image_png),
        "-i", str(audio),
        "-vf", vf,
        "-c:v", "libx264", "-tune", "stillimage", "-pix_fmt", "yuv420p",
        "-r", str(FPS),
        "-c:a", "aac", "-b:a", "160k", "-ar", str(AUDIO_RATE),
        "-shortest", "-movflags", "+faststart",
        str(out_mp4),
    ]
    _run(cmd)
    return out_mp4


def concat_clips(clips: list[Path], out_mp4: Path, work_dir: Path) -> Path:
    """把多屏片段无损拼接为最终视频。"""
    ff = ffmpeg_exe()
    out_mp4 = Path(out_mp4)
    work_dir = Path(work_dir)
    work_dir.mkdir(parents=True, exist_ok=True)
    list_file = work_dir / "concat_list.txt"
    lines = []
    for c in clips:
        p = str(Path(c).resolve()).replace("\\", "/")
        lines.append(f"file '{p}'")
    list_file.write_text("\n".join(lines), encoding="utf-8")

    cmd = [
        ff, "-y", "-f", "concat", "-safe", "0",
        "-i", str(list_file),
        "-c", "copy", "-movflags", "+faststart",
        str(out_mp4),
    ]
    _run(cmd)
    return out_mp4
