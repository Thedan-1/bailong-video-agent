"""One-shot deterministic video demo.

The model supplies one brief and one JSON asset manifest.  This module turns
that plan into an FFmpeg render without opening a GUI editor.  The input media
stays local; the repository contains only the recipe and example manifest.
"""

from __future__ import annotations

import argparse
import json
import math
import shlex
import subprocess
from pathlib import Path


def _parse_brief(path: Path) -> dict[str, str]:
    values: dict[str, str] = {}
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or ":" not in line:
            continue
        key, value = line.split(":", 1)
        values[key.strip().lower()] = value.strip()
    return values


def _q(value: str) -> str:
    return value.replace("\\", "/").replace("'", "\\'").replace(":", "\\:")


def _run(cmd: list[str]) -> None:
    print("$", " ".join(shlex.quote(x) for x in cmd))
    subprocess.run(cmd, check=True)


def render(brief: Path, manifest_path: Path, output: Path) -> Path:
    brief_values = _parse_brief(brief)
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    canvas = manifest.get("canvas", {})
    width = int(canvas.get("width", brief_values.get("width", 1920)))
    height = int(canvas.get("height", brief_values.get("height", 1080)))
    fps = int(canvas.get("fps", brief_values.get("fps", 60)))
    background = manifest.get("background", "0b0d14")
    segments = manifest.get("segments", [])
    beats = [float(x) for x in manifest.get("beats", [])]
    if not segments:
        raise ValueError("manifest.segments 不能为空")

    output.parent.mkdir(parents=True, exist_ok=True)
    inputs: list[str] = []
    filters: list[str] = [
        f"color=c=0x{background}:s={width}x{height}:r={fps}:d={manifest.get('duration', 8)}[base]"
    ]
    last = "base"
    duration = float(manifest.get("duration", 0))

    for index, segment in enumerate(segments):
        source = Path(segment["path"])
        if not source.exists():
            raise FileNotFoundError(f"素材不存在: {source}")
        at = float(segment.get("at", 0))
        clip_duration = float(segment.get("duration", 1))
        start = float(segment.get("start", 0))
        x, y = int(segment.get("x", 0)), int(segment.get("y", 0))
        w, h = int(segment.get("w", width)), int(segment.get("h", height))
        rotation = float(segment.get("rotation", 0))
        inputs.extend(["-ss", str(start), "-t", str(clip_duration), "-i", str(source)])
        input_index = index
        rotate = ""
        if rotation:
            rotate = f",rotate={rotation * math.pi / 180}:fillcolor=black@0"
        filters.append(
            f"[{input_index}:v]setpts=PTS-STARTPTS,scale={w}:{h}:force_original_aspect_ratio=increase," 
            f"crop={w}:{h},setsar=1,fps={fps}{rotate}[clip{index}]"
        )
        next_name = f"layer{index}"
        filters.append(
            f"[{last}][clip{index}]overlay=x={x}:y={y}:eof_action=pass:enable='between(t,{at},{at + clip_duration})'[{next_name}]"
        )
        last = next_name
        duration = max(duration, at + clip_duration)

    for beat in beats:
        # A short full-frame flash marks a musical attack without introducing a
        # permanent white border or a GUI-style shake.
        next_name = f"flash{len(filters)}"
        filters.append(
            f"[{last}]drawbox=x=0:y=0:w={width}:h={height}:color=white@0.16:t=fill:"
            f"enable='between(t,{beat - 0.025},{beat + 0.045})'[{next_name}]"
        )
        last = next_name

    fontfile = manifest.get("fontfile")
    if fontfile and Path(fontfile).exists():
        for index, segment in enumerate(segments):
            label = segment.get("label")
            if not label:
                continue
            at = float(segment.get("at", 0))
            end = at + float(segment.get("duration", 1))
            next_name = f"text{index}"
            filters.append(
                f"[{last}]drawtext=fontfile='{_q(fontfile)}':text='{_q(str(label))}':"
                f"fontcolor=white:fontsize={int(segment.get('font_size', 54))}:"
                f"borderw=2:bordercolor=black@0.7:x={int(segment.get('text_x', 60))}:"
                f"y={int(segment.get('text_y', height - 130))}:enable='between(t,{at},{end})'[{next_name}]"
            )
            last = next_name

    filter_graph = ";".join(filters)
    cmd = ["ffmpeg", "-y", *inputs, "-filter_complex", filter_graph, "-map", f"[{last}]", "-an"]
    bgm = manifest.get("bgm")
    if bgm:
        cmd.extend(["-i", str(Path(bgm)), "-map", f"{len(segments) + 1}:a", "-shortest"])
    cmd.extend(
        [
            "-r", str(fps), "-c:v", "libx264", "-preset", "medium", "-crf", "18",
            "-pix_fmt", "yuv420p", "-movflags", "+faststart", str(output),
        ]
    )
    _run(cmd)
    output.with_suffix(".json").write_text(
        json.dumps({"brief": str(brief), "manifest": str(manifest_path), "width": width, "height": height, "fps": fps, "duration": duration}, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    return output


def main() -> None:
    parser = argparse.ArgumentParser(description="Bailong one-shot FFmpeg demo")
    parser.add_argument("--brief", type=Path, required=True)
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    render(args.brief, args.manifest, args.output)


if __name__ == "__main__":
    main()
