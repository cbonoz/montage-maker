#!/usr/bin/env python3
"""
Movie montage maker: opening hook → beat drop → rapid scene montage.

Usage:
  python build_montage.py movie.mp4 \
      --hook 1:30-1:38 \
      --scenes 5:10-5:14 12:20-12:24 25:00-25:04 \
      [--song track.mp3] [--output montage.mp4]
"""
import argparse, json, os, subprocess, sys, tempfile, shutil
from pathlib import Path

def parse_ts(ts: str) -> float:
    """Convert mm:ss or ss to seconds."""
    ts = ts.strip()
    if ":" in ts:
        parts = ts.split(":")
        if len(parts) == 2:
            return int(parts[0]) * 60 + float(parts[1])
        return int(parts[0]) * 3600 + int(parts[1]) * 60 + float(parts[2])
    return float(ts)

def fmt(sec): return f"{int(sec//60)}:{sec%60:05.2f}"

def extract(movie, start, end, out):
    dur = end - start
    subprocess.run([
        "ffmpeg", "-y", "-ss", str(start), "-i", movie,
        "-t", str(dur), "-c:v", "libx264", "-preset", "fast",
        "-crf", "22", "-c:a", "aac", "-pix_fmt", "yuv420p", out
    ], capture_output=True, check=True)
    return dur

def build(args):
    movie = Path(args.movie)
    if not movie.exists():
        print(f"❌ Movie not found: {movie}"); sys.exit(1)

    work = Path(tempfile.mkdtemp(prefix="montage_"))
    out = Path(args.output)
    print(f"📁 Working in {work}")

    # Step 1: extract hook
    hs, he = parse_ts(args.hook.split("-")[0]), parse_ts(args.hook.split("-")[1])
    print(f"\n🎤 Extracting hook: {fmt(hs)}–{fmt(he)}")
    hook_path = work / "hook.mp4"
    hook_dur = extract(str(movie), hs, he, str(hook_path))

    # Step 2: extract scenes
    scene_paths = []
    for i, s in enumerate(args.scenes):
        ss, se = parse_ts(s.split("-")[0]), parse_ts(s.split("-")[1])
        print(f"🎬 Scene {i+1}: {fmt(ss)}–{fmt(se)}")
        sp = work / f"scene_{i:02d}.mp4"
        extract(str(movie), ss, se, str(sp))
        scene_paths.append(sp)

    # Step 3: concat video (hook + scenes, no audio)
    concat_txt = work / "concat.txt"
    with open(concat_txt, "w") as f:
        f.write(f"file '{hook_path}'\n")
        for sp in scene_paths:
            f.write(f"file '{sp}'\n")

    raw_vid = work / "raw_video.mp4"
    print("\n🔗 Concatenating video clips...")
    subprocess.run([
        "ffmpeg", "-y", "-f", "concat", "-safe", "0",
        "-i", str(concat_txt), "-c", "copy", str(raw_vid)
    ], capture_output=True, check=True)

    # Step 4: extract hook audio
    hook_audio = work / "hook_audio.aac"
    subprocess.run([
        "ffmpeg", "-y", "-i", str(hook_path), "-vn",
        "-c:a", "copy", str(hook_audio)
    ], capture_output=True, check=True)

    # Step 5: build final audio mix
    if args.song and Path(args.song).exists():
        print(f"\n🎵 Mixing with song: {args.song}")
        song_path = Path(args.song)
        final_audio = work / "mixed_audio.aac"

        # Complex filter:
        # [0:a] = hook audio (full volume for its duration)
        # [1:a] = song (low during hook, full after)
        fade_in_dur = min(0.3, hook_dur)  # start raising music before hook ends
        filter_str = (
            f"[0:a]adelay=0|0[a1];"
            f"[1:a]adelay=0|0[a2];"
            f"[a2]volume=0.12:enable='between(t,0,{hook_dur-fade_in_dur})'[song_low];"
            f"[song_low]volume=1:enable='gt(t,{hook_dur-fade_in_dur})',"
            f"afade=t=in:st={hook_dur-fade_in_dur}:d={fade_in_dur}[song_full];"
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
        print("\n🎵 No song provided — using hook audio only")
        final_audio = hook_audio

    # Step 6: final mux (video + mixed audio)
    print(f"\n📦 Muxing final video...")

    # Get raw_vid duration to trim audio to match
    probe = subprocess.run([
        "ffprobe", "-v", "error", "-show_entries",
        "format=duration", "-of", "csv=p=0", str(raw_vid)
    ], capture_output=True, text=True)
    vid_dur = float(probe.stdout.strip())

    # Trim audio to match video duration
    trimmed_audio = work / "trimmed_audio.aac"
    subprocess.run([
        "ffmpeg", "-y", "-i", str(final_audio), "-t", str(vid_dur),
        "-c:a", "aac", "-b:a", "192k", str(trimmed_audio)
    ], capture_output=True, check=True)

    # Final mux
    subprocess.run([
        "ffmpeg", "-y",
        "-i", str(raw_vid),
        "-i", str(trimmed_audio),
        "-c:v", "copy",
        "-c:a", "aac", "-b:a", "192k",
        "-shortest",
        "-movflags", "+faststart",
        str(out)
    ], capture_output=True, check=True)

    # Step 7: cleanup
    if not args.keep:
        shutil.rmtree(work)

    print(f"\n✅ Done! → {out}")
    dur_s = subprocess.run([
        "ffprobe", "-v", "error", "-show_entries",
        "format=duration", "-of", "csv=p=0", str(out)
    ], capture_output=True, text=True)
    print(f"   Duration: {fmt(float(dur_s.stdout.strip()))}")
    print(f"   File size: {out.stat().st_size / 1024 / 1024:.1f} MB")

def main():
    p = argparse.ArgumentParser(description="Movie montage maker")
    p.add_argument("movie", help="Movie file path")
    p.add_argument("--hook", required=True, help="Opening hook range (mm:ss-mm:ss)")
    p.add_argument("--scenes", nargs="+", required=True,
                   help="Scene ranges: mm:ss-mm:ss ...")
    p.add_argument("--song", help="Background music file")
    p.add_argument("--output", default="montage.mp4", help="Output file")
    p.add_argument("--keep", action="store_true", help="Keep temp files")
    p.add_argument("--vertical", action="store_true",
                   help="Crop to 9:16 vertical (default: keep original aspect)")
    build(p.parse_args())

if __name__ == "__main__":
    main()
