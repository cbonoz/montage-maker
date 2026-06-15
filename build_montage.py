#!/usr/bin/env python3
"""
Movie montage maker: opening hook → beat drop → rapid scene montage.

Reproducible builds, always under 30s total.
Auto-trims scene clips and reduces count to fit.

Usage:
  python build_montage.py movie.mp4 \
      --hook 1:30-1:38 \
      --scenes 5:10-5:14 12:20-12:24 25:00-25:04 \
      [--song sounds/sb_snowfall.mp3] [--output montage.mp4] [--max-dur 25]
"""
import argparse, subprocess, sys, tempfile, shutil, math
from pathlib import Path

TARGET_DUR = 25.0  # max total seconds (hook + scenes)
SCENE_DUR = 2.0    # seconds per scene clip
HOOK_DUR = 3.0     # max seconds for hook
MAX_SCENES = 6     # max scene count


def parse_ts(ts: str) -> float:
    ts = ts.strip()
    if ":" in ts:
        parts = ts.split(":")
        if len(parts) == 2:
            return int(parts[0]) * 60 + float(parts[1])
        return int(parts[0]) * 3600 + int(parts[1]) * 60 + float(parts[2])
    return float(ts)


def fmt(sec):
    return f"{int(sec//60)}:{sec%60:05.2f}"


def probe_dur(path):
    r = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "csv=p=0", str(path)],
        capture_output=True, text=True, timeout=10
    )
    return float(r.stdout.strip())


def extract(movie, start, end, out):
    """Extract subclip with precise duration (re-encode)."""
    dur = end - start
    subprocess.run([
        "ffmpeg", "-y",
        "-ss", str(start), "-i", str(movie),
        "-t", str(dur),
        "-c:v", "libx264", "-preset", "fast", "-crf", "23",
        "-c:a", "aac", "-pix_fmt", "yuv420p",
        "-movflags", "+faststart",
        str(out)
    ], capture_output=True, check=True, timeout=60)
    return probe_dur(out)


def build(args):
    movie = Path(args.movie)
    if not movie.exists():
        print(f"❌ Movie not found: {movie}")
        sys.exit(1)

    max_dur = args.max_dur or TARGET_DUR
    scene_dur = min(args.scene_dur or SCENE_DUR, max_dur / 3)  # at least 3 clips
    hook_max = min(args.hook_dur or HOOK_DUR, max_dur * 0.3)   # hook max 30% of total

    work = Path(tempfile.mkdtemp(prefix="montage_"))
    out = Path(args.output)
    print(f"📁 Working in: {work}")

    # -- Step 1: extract hook, cap to hook_max --
    hs, he = parse_ts(args.hook.split("-")[0]), parse_ts(args.hook.split("-")[1])
    raw_hook_dur = min(he - hs, hook_max)
    print(f"\n🎤 Hook: {fmt(hs)}–{fmt(hs + raw_hook_dur)} (capped at {fmt(hook_max)})")
    hook_path = work / "hook.mp4"
    hook_actual = extract(str(movie), hs, hs + raw_hook_dur, str(hook_path))

    # -- Step 2: figure out how many scenes fit --
    remaining = max_dur - hook_actual
    n_scenes = min(len(args.scenes), MAX_SCENES, int(remaining // scene_dur))
    if n_scenes < 1:
        print("⚠️  Not enough room for scenes — reducing hook duration")
        hook_actual = max_dur * 0.3
        # Re-extract hook shorter
        extract(str(movie), hs, hs + hook_actual, str(hook_path))
        hook_actual = probe_dur(hook_path)
        remaining = max_dur - hook_actual
        n_scenes = min(len(args.scenes), int(remaining // scene_dur))
        n_scenes = max(n_scenes, 1)

    actual_scene_dur = min(scene_dur, remaining / n_scenes)

    print(f"📐 Budget: {fmt(max_dur)} total, {fmt(hook_actual)} hook, {fmt(remaining)} for scenes")
    print(f"   → {n_scenes} scenes × {fmt(actual_scene_dur)} each = {fmt(n_scenes * actual_scene_dur)}")

    # -- Step 3: extract scenes with exact duration --
    scene_paths = []
    for i in range(n_scenes):
        ss, se = parse_ts(args.scenes[i].split("-")[0]), parse_ts(args.scenes[i].split("-")[1])
        raw_dur = se - ss
        clip_dur = min(raw_dur, actual_scene_dur)
        # Sample from the middle of the scene for best content
        mid = (ss + se) / 2
        clip_start = mid - clip_dur / 2
        sp = work / f"scene_{i:02d}.mp4"
        actual = extract(str(movie), clip_start, clip_start + clip_dur, str(sp))
        scene_paths.append(sp)
        print(f"🎬 Scene {i+1}: {fmt(clip_start)}–{fmt(clip_start + actual)} ({fmt(actual)})")

    # -- Step 4: concat video --
    concat_txt = work / "concat.txt"
    with open(concat_txt, "w") as f:
        f.write(f"file '{hook_path}'\n")
        for sp in scene_paths:
            f.write(f"file '{sp}'\n")

    raw_vid = work / "raw_video.mp4"
    print("\n🔗 Concatenating...")
    subprocess.run([
        "ffmpeg", "-y", "-f", "concat", "-safe", "0",
        "-i", str(concat_txt), "-c", "copy", str(raw_vid)
    ], capture_output=True, check=True)
    vid_dur = probe_dur(raw_vid)

    if vid_dur > max_dur + 1:
        print(f"⚠️  Result {fmt(vid_dur)} exceeds max {fmt(max_dur)} — retrying with shorter scenes")
        # Tighten scene durations
        overage = vid_dur - max_dur
        new_scene_dur = max(0.5, actual_scene_dur - overage / n_scenes)
        # Re-extract scenes shorter
        scene_paths = []
        for i in range(n_scenes):
            ss, se = parse_ts(args.scenes[i].split("-")[0]), parse_ts(args.scenes[i].split("-")[1])
            mid = (ss + se) / 2
            clip_start = mid - new_scene_dur / 2
            sp = work / f"scene_{i:02d}.mp4"
            actual = extract(str(movie), clip_start, clip_start + new_scene_dur, str(sp))
            scene_paths.append(sp)
        # Re-concat
        with open(concat_txt, "w") as f:
            f.write(f"file '{hook_path}'\n")
            for sp in scene_paths:
                f.write(f"file '{sp}'\n")
        subprocess.run([
            "ffmpeg", "-y", "-f", "concat", "-safe", "0",
            "-i", str(concat_txt), "-c", "copy", str(raw_vid)
        ], capture_output=True, check=True)
        vid_dur = probe_dur(raw_vid)

    # -- Step 5: extract hook audio --
    hook_audio = work / "hook_audio.aac"
    subprocess.run([
        "ffmpeg", "-y", "-i", str(hook_path), "-vn",
        "-c:a", "aac", str(hook_audio)
    ], capture_output=True, check=True)

    # -- Step 6: build audio mix --
    if args.song and Path(args.song).exists():
        print(f"\n🎵 Mixing: {args.song}")
        song_path = Path(args.song)
        final_audio = work / "mixed_audio.aac"
        fade_dur = min(0.3, hook_actual * 0.3)

        filter_str = (
            f"[0:a]adelay=0|0[a1];"
            f"[1:a]adelay=0|0[a2];"
            f"[a2]volume=0.12:enable='between(t,0,{hook_actual-fade_dur})'[song_low];"
            f"[song_low]volume=1:enable='gt(t,{hook_actual-fade_dur})',"
            f"afade=t=in:st={hook_actual-fade_dur}:d={fade_dur}[song_full];"
            f"[a1][song_full]amix=inputs=2:duration=longest:dropout_transition=0[aout]"
        )

        subprocess.run([
            "ffmpeg", "-y",
            "-i", str(hook_audio),
            "-i", str(song_path),
            "-filter_complex", filter_str,
            "-map", "[aout]",
            "-c:a", "aac", "-b:a", "192k",
            str(final_audio)
        ], capture_output=True, check=True, timeout=60)
    else:
        print("\n🎵 No song — hook audio only")
        final_audio = hook_audio

    # -- Step 7: trim audio to video duration & mux --
    trimmed_audio = work / "trimmed_audio.aac"
    subprocess.run([
        "ffmpeg", "-y", "-i", str(final_audio), "-t", str(vid_dur),
        "-c:a", "aac", "-b:a", "192k", str(trimmed_audio)
    ], capture_output=True, check=True)

    subprocess.run([
        "ffmpeg", "-y",
        "-i", str(raw_vid), "-i", str(trimmed_audio),
        "-c:v", "copy",
        "-c:a", "aac", "-b:a", "192k",
        "-shortest",
        "-movflags", "+faststart",
        str(out)
    ], capture_output=True, check=True)

    # -- Step 8: cleanup --
    if not args.keep:
        shutil.rmtree(work)

    actual_dur = probe_dur(out)
    size_mb = out.stat().st_size / 1024 / 1024
    print(f"\n✅ → {out}")
    print(f"   Duration: {fmt(actual_dur)} (max requested: {fmt(max_dur)})")
    print(f"   Size: {size_mb:.1f} MB")
    if actual_dur > max_dur + 1:
        print("⚠️  Over budget — consider fewer or shorter scenes with --scene-dur")

    return actual_dur <= max_dur + 1


def main():
    p = argparse.ArgumentParser(
        description="Montage Maker — build short video montages under 30s",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "Examples:\n"
            "  python build_montage.py movie.mp4 --hook 1:30-1:38 --scenes 5:10-5:14 12:20-12:24\n"
            "  python build_montage.py movie.mp4 --hook 1:30-1:38 --scenes 5:10-5:14 12:20-12:24 \\\n"
            "      --song sounds/sb_snowfall.mp3 --max-dur 20 --output out.mp4\n"
        )
    )
    p.add_argument("movie", help="Movie file path")
    p.add_argument("--hook", required=True, help="Hook range (mm:ss-mm:ss)")
    p.add_argument("--scenes", nargs="+", required=True,
                   help="Scene ranges: mm:ss-mm:ss ...")
    p.add_argument("--song", help="Background music (from sounds/ or elsewhere)")
    p.add_argument("--output", default="montage.mp4", help="Output file")
    p.add_argument("--max-dur", type=float, default=TARGET_DUR,
                   help=f"Target max duration in seconds (default: {TARGET_DUR})")
    p.add_argument("--scene-dur", type=float, default=SCENE_DUR,
                   help=f"Per-scene duration in seconds (default: {SCENE_DUR})")
    p.add_argument("--hook-dur", type=float, default=HOOK_DUR,
                   help=f"Max hook duration in seconds (default: {HOOK_DUR})")
    p.add_argument("--keep", action="store_true", help="Keep temp files")

    ok = build(p.parse_args())
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
