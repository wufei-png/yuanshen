"""Rebuild the public PV audio against the approved, separately recorded voice files."""

from __future__ import annotations

import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VIDEO = ROOT / "output/nadia_character/assets/video"
AUDIO = ROOT / "output/nadia_character/assets/audio"
OUT = VIDEO / "nadia_video_pv_between_two_weights_v1.mp4"
CLIPS = (
    ("nadia_video_v01_intro_720p_a01.mp4", 6.080),
    ("nadia_video_v07_wind_720p_a01.mp4", 8.096),
    ("nadia_video_v08_hug_720p_a01.mp4", 6.080),
    ("nadia_video_v03_skill_720p_a01.mp4", 6.080),
    ("nadia_video_v04_light_720p_a01.mp4", 5.088),
    ("nadia_video_v05_heavy_720p_a01.mp4", 5.088),
)
VOICES = (
    ("nadia_voice_01_greeting.mp3", 350),
    ("nadia_voice_03_wind.mp3", 6430),
    ("nadia_voice_05_heavy_hug.mp3", 15676),
    ("nadia_voice_06_skill.mp3", 21806),
    ("nadia_voice_07_light_phase.mp3", 29916),
    ("nadia_voice_08_heavy_phase.mp3", 34604),
)
DUCK_WINDOWS = (
    (0.35, 5.53), (6.43, 11.48), (15.68, 20.31),
    (21.81, 25.10), (29.92, 32.85), (34.60, 36.55),
)


def main() -> None:
    inputs = [OUT, *(VIDEO / name for name, _ in CLIPS), *(AUDIO / name for name, _ in VOICES)]
    for path in inputs:
        if not path.is_file():
            raise FileNotFoundError(path)
    filters: list[str] = []
    for index, (_, duration) in enumerate(CLIPS, 1):
        filters.append(
            f"[{index}:a]aresample=48000,aformat=channel_layouts=stereo,"
            f"atrim=0:{duration},asetpts=PTS-STARTPTS[clip{index}]"
        )
    filters.append("".join(f"[clip{i}]" for i in range(1, 7)) + "concat=n=6:v=0:a=1[bed0]")
    duck = ",".join(
        f"volume=0.316:enable='between(t,{start},{end})'" for start, end in DUCK_WINDOWS
    )
    filters.append(f"[bed0]apad=pad_dur=6,atrim=0:42,{duck}[bed]")
    filters.append(
        "[1:a]aresample=48000,aformat=channel_layouts=stereo,"
        "atrim=start=0.9:end=6.08,asetpts=PTS-STARTPTS,"
        "afade=t=in:st=0:d=0.6,adelay=36544:all=1[tail]"
    )
    for index, (_, delay_ms) in enumerate(VOICES, 7):
        filters.append(
            f"[{index}:a]aresample=48000,aformat=channel_layouts=stereo,"
            f"adelay={delay_ms}:all=1[voice{index}]"
        )
    voice_inputs = "".join(f"[voice{i}]" for i in range(7, 13))
    filters.append(
        f"[bed][tail]{voice_inputs}amix=inputs=8:duration=longest:"
        "dropout_transition=0:normalize=0,"
        "loudnorm=I=-16:TP=-0.95:LRA=11,afade=t=out:st=40.5:d=1.5[mix]"
    )
    temporary = OUT.with_name(".nadia_pv_v3_1.tmp.mp4")
    command = ["ffmpeg", "-hide_banner", "-loglevel", "error", "-y"]
    for path in inputs:
        command += ["-i", str(path)]
    command += [
        "-filter_complex", ";".join(filters), "-map", "0:v:0", "-map", "[mix]",
        "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-ac", "2",
        "-t", "42", "-movflags", "+faststart", str(temporary),
    ]
    try:
        subprocess.run(command, check=True)
        temporary.replace(OUT)
    finally:
        temporary.unlink(missing_ok=True)
    print(OUT)


if __name__ == "__main__":
    main()
