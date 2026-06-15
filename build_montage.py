#!/usr/bin/env python3
"""
Movie montage maker: black → hook (dialogue audible) → beat-synced scene montage + music → fade out.

Structure:
  [0.5s black] → [hook with dialogue audible, music building] → [beat-synced scene cuts, music full] → [fade out]

Features:
  - Beat-synced cut timing (--bpm or auto-detect)
  - Dialogue auto-boost: quiet hooks get louder, loud hooks get normal
  - Multiple source movies for visual variety
  - Scenes interleaved across source files

Usage:
  python build_montage.py movie1.mp4 [movie2.mp4 ...] \
      --hook 0-2.6 --hook-movie hook.mkv \
      --scenes 30-33 55-58 70-73 \
      --song sounds/sb_snowfall.mp3 --bpm 80 \
      --max-dur 30 --output montage.mp4
"""
import argparse, subprocess, sys, tempfile, shutil, math, re
from pathlib import Path

TARGET_DUR = 25.0
SCENE_DUR = 2.0
HOOK_DUR = 3.0
BLACK_DUR = 0.5
MAX_SCENES = 20
DIALOGUE_LOUDNESS_TARGET = -10.0  # target dB for dialogue after boosting (loud enough to hear over music)


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
    val = r.stdout.strip()
    try:
        return float(val)
    except ValueError:
        return 0.0


def probe_max_volume(path):
    """Probe the peak volume (dB) of an audio file. Returns float, None on failure."""
    r = subprocess.run(
        ["ffmpeg", "-y", "-i", str(path), "-af", "volumedetect",
         "-f", "null", "-"],
        capture_output=True, text=True, timeout=15
    )
    m = re.search(r'max_volume:\s*([-\d.]+)\s*dB', r.stderr)
    if m:
        return float(m.group(1))
    return None


def detect_bpm(song_path):
    """Simple BPM detection via ffmpeg peak analysis. Falls back gracefully."""
    try:
        r = subprocess.run([
            "ffmpeg", "-y", "-t", "15", "-i", str(song_path),
            "-ac", "1", "-ar", "22050", "-f", "wav", "pipe:1"
        ], capture_output=True, timeout=30)
        if r.returncode != 0 or len(r.stdout) < 1000:
            return None
        samples = r.stdout[44:]  # skip WAV header
        sample_rate = 22050
        chunk_size = sample_rate // 10  # 100ms windows
        peaks = []
        for i in range(0, min(len(samples), sample_rate * 10), chunk_size):
            chunk = samples[i:i+chunk_size]
            if len(chunk) < 2:
                continue
            vals = [abs(int.from_bytes(chunk[j:j+2], 'little', signed=True))
                    for j in range(0, len(chunk)-1, 2)]
            peaks.append(max(vals))
        if len(peaks) < 3:
            return None
        threshold = sum(peaks) / len(peaks) * 1.5
        beat_positions = [i for i, p in enumerate(peaks) if p > threshold]
        if len(beat_positions) >= 3:
            intervals = [beat_positions[i+1] - beat_positions[i]
                        for i in range(len(beat_positions)-1)]
            avg_interval = sum(intervals) / len(intervals) * 0.1  # in seconds
            bpm = round(60.0 / avg_interval) if avg_interval > 0 else 120
            return max(60, min(200, bpm))
    except Exception:
        pass
    return None


def detect_beat_positions(song_path: str, max_dur: float = 30.0) -> list[float]:
    """Detect beat/transient positions in the first N seconds of audio.

    Analyzes audio for energy peaks (kick/snare hits, chord changes) that
    represent musical downbeats. Returns sorted timestamps (seconds) that
    scene cuts can snap to for rhythm-aligned editing.
    """
    try:
        dur = min(max_dur, 30.0)
        r = subprocess.run([
            "ffmpeg", "-y", "-t", str(dur), "-i", str(song_path),
            "-ac", "1", "-ar", "22050", "-f", "wav", "pipe:1"
        ], capture_output=True, timeout=30)
        if r.returncode != 0 or len(r.stdout) < 1000:
            return []
        samples = r.stdout[44:]  # skip WAV header
        sample_rate = 22050
        window = sample_rate // 20  # 50ms
        hop = window // 2           # 25ms overlap

        energy = []
        times = []
        for i in range(0, len(samples) - window, hop):
            chunk = samples[i:i+window]
            if len(chunk) < 2:
                continue
            vals = [abs(int.from_bytes(chunk[j:j+2], 'little', signed=True))
                    for j in range(0, len(chunk)-1, 2)]
            energy.append(sum(vals) / max(len(vals), 1))
            times.append(i / sample_rate)

        if not energy:
            return []

        # Adaptive threshold: median + 1.5 × interquartile range
        sorted_e = sorted(energy)
        n = len(sorted_e)
        q1 = sorted_e[n // 4]
        q3 = sorted_e[3 * n // 4]
        iqr = q3 - q1
        threshold = sorted_e[n // 2] + 1.5 * iqr

        # Find local maxima above threshold
        peaks = []
        for i in range(1, len(energy)-1):
            if (energy[i] > energy[i-1] and
                energy[i] >= energy[i+1] and
                energy[i] > threshold):
                peaks.append(times[i])

        if len(peaks) < 3:
            return []

        # Remove too-close peaks (min 80ms between distinct beats)
        filtered = [peaks[0]]
        for p in peaks[1:]:
            if p - filtered[-1] < 0.08:
                continue
            filtered.append(p)

        return filtered
    except Exception:
        return []


def scale_pad_filter(target_w=1280, target_h=720):
    """Return an ffmpeg filter string to scale + pad to exact target resolution."""
    return (
        f"scale={target_w}:{target_h}:force_original_aspect_ratio=decrease,"
        f"pad={target_w}:{target_h}:(ow-iw)/2:(oh-ih)/2:black"
    )


def extract_video_only(movie, start, end, out):
    """Extract video-only subclip, scaled/padded to uniform resolution."""
    dur = end - start
    subprocess.run([
        "ffmpeg", "-y",
        "-ss", str(start), "-i", str(movie),
        "-t", str(dur),
        "-filter_complex", f"[0:v]{scale_pad_filter()}",
        "-c:v", "libx264", "-preset", "fast", "-crf", "23",
        "-an",
        "-pix_fmt", "yuv420p",
        "-movflags", "+faststart",
        str(out)
    ], capture_output=True, check=True, timeout=120)
    return probe_dur(out)


def extract_with_audio(movie, start, end, out):
    """Extract subclip keeping audio, scaled/padded."""
    dur = end - start
    subprocess.run([
        "ffmpeg", "-y",
        "-ss", str(start), "-i", str(movie),
        "-t", str(dur),
        "-filter_complex", f"[0:v]{scale_pad_filter()}",
        "-c:v", "libx264", "-preset", "fast", "-crf", "23",
        "-c:a", "aac",
        "-pix_fmt", "yuv420p",
        "-movflags", "+faststart",
        str(out)
    ], capture_output=True, check=True, timeout=120)
    return probe_dur(out)


def build(args):
    movies = [Path(m) for m in args.movie]
    for m in movies:
        if not m.exists():
            print(f"❌ Movie not found: {m}")
            sys.exit(1)

    hook_movie = Path(args.hook_movie) if args.hook_movie else movies[0]
    if not hook_movie.exists():
        print(f"❌ Hook movie not found: {hook_movie}")
        sys.exit(1)

    max_dur = args.max_dur or TARGET_DUR
    hook_max = min(args.hook_dur or HOOK_DUR, max_dur * 0.3)

    # --- BPM ---
    bpm = args.bpm
    if bpm is None and args.song and Path(args.song).exists():
        print(f"\n🎵 Detecting BPM from {Path(args.song).name}...")
        detected = detect_bpm(args.song)
        if detected:
            bpm = detected
            print(f"   Detected: {bpm} BPM")
        else:
            bpm = 120
            print(f"   Detection failed, defaulting to {bpm} BPM")
    elif bpm is None:
        bpm = 120
    beat_sec = 60.0 / bpm

    work = Path(tempfile.mkdtemp(prefix="montage_"))
    out = Path(args.output)
    print(f"📁 Working in: {work}")
    print(f"🎵 BPM: {bpm} ({beat_sec:.3f}s per beat)")

    avail = max_dur - BLACK_DUR

    # --- Step 1: extract hook (with audio) ---
    hs, he = parse_ts(args.hook.split("-")[0]), parse_ts(args.hook.split("-")[1])
    raw_hook_dur = min(he - hs, hook_max)
    print(f"\n🎤 Hook: {fmt(hs)}–{fmt(hs + raw_hook_dur)} (from {hook_movie.name})")
    hook_path = work / "hook.mp4"
    hook_actual = extract_with_audio(str(hook_movie), hs, hs + raw_hook_dur, hook_path)

    # Snap hook duration to nearest beat
    hook_actual = max(beat_sec, round(hook_actual / beat_sec) * beat_sec)

    # --- Step 2: budget scenes ---
    remaining = avail - hook_actual
    raw_scene_dur = args.scene_dur or SCENE_DUR
    beat_scene_dur = max(beat_sec, round(raw_scene_dur / beat_sec) * beat_sec)
    beat_scene_dur = max(beat_sec * 2, min(beat_sec * 8, beat_scene_dur))

    n_scenes = min(len(args.scenes), MAX_SCENES, max(1, int(remaining // beat_scene_dur)))
    actual_scene_dur = max(beat_sec * 2, round((remaining / n_scenes) / beat_sec) * beat_sec)
    n_scenes = min(len(args.scenes), MAX_SCENES, max(1, int(remaining // actual_scene_dur)))

    print(f"📐 {fmt(max_dur)}s total → {fmt(BLACK_DUR)}s black + {fmt(hook_actual)} hook + {n_scenes}x{fmt(actual_scene_dur)}s scenes")
    print(f"   (beat: {beat_sec:.2f}s, {int(actual_scene_dur/beat_sec)} beats per scene)")

    # --- Beat alignment: snap scene boundaries to actual music downbeats ---
    beat_positions = []
    if args.song and Path(args.song).exists():
        beat_positions = detect_beat_positions(args.song, max_dur)
        if beat_positions:
            print(f"   Beat grid: {len(beat_positions)} transients detected in first {min(30.0, max_dur)}s")

    # Compute per-scene cut times, each snapped to nearest detectable beat
    scene_cut_times = []
    current = BLACK_DUR + hook_actual
    for i in range(n_scenes):
        target = current + actual_scene_dur
        nearest = target
        if beat_positions:
            window = beat_sec * 1.5  # search within ±1.5 beats
            candidates = [b for b in beat_positions
                          if abs(b - target) <= window and b > current]
            if candidates:
                nearest = min(candidates, key=lambda b: abs(b - target))
        scene_cut_times.append(nearest)
        current = nearest

    # Cap to max_dur: drop last scene if total overshoots
    if scene_cut_times and scene_cut_times[-1] > max_dur:
        n_scenes -= 1
        scene_cut_times = scene_cut_times[:n_scenes]
        scene_cut_times.append(BLACK_DUR + hook_actual + actual_scene_dur * n_scenes)
        # Re-snap
        current = BLACK_DUR + hook_actual
        for i in range(n_scenes):
            target = current + actual_scene_dur
            nearest = target
            if beat_positions:
                window = beat_sec * 1.0
                candidates = [b for b in beat_positions
                              if abs(b - target) <= window and b > current]
                if candidates:
                    nearest = min(candidates, key=lambda b: abs(b - target))
            scene_cut_times[i] = nearest
            current = nearest

    # Report alignment
    if beat_positions:
        on_beat = 0
        for ct in scene_cut_times:
            if any(abs(ct - b) < beat_sec * 0.3 for b in beat_positions):
                on_beat += 1
        print(f"   Beat-aligned: {on_beat}/{n_scenes} cuts on detected downbeats")

    # --- Step 3: extract scenes (video-only) with variable beat-aligned durations ---
    scene_paths = []
    for i in range(n_scenes):
        ss, se = parse_ts(args.scenes[i].split("-")[0]), parse_ts(args.scenes[i].split("-")[1])
        raw_dur = se - ss
        if scene_cut_times:
            if i == 0:
                clip_dur = scene_cut_times[i] - (BLACK_DUR + hook_actual)
            else:
                clip_dur = scene_cut_times[i] - scene_cut_times[i - 1]
            clip_dur = min(raw_dur, max(beat_sec * 1.5, clip_dur))
        else:
            clip_dur = min(raw_dur, actual_scene_dur)
        mid = (ss + se) / 2
        clip_start = mid - clip_dur / 2
        mid = (ss + se) / 2
        clip_start = mid - clip_dur / 2
        source_movie = movies[i % len(movies)]
        sp = work / f"scene_{i:02d}.mp4"
        actual = extract_video_only(str(source_movie), clip_start, clip_start + clip_dur, sp)
        scene_paths.append(sp)
        print(f"🎬 Scene {i+1}: {fmt(clip_start)}–{fmt(clip_start + actual)} ({fmt(actual)}) — {source_movie.name}")

    # --- Step 4: generate black lead-in ---
    black_path = work / "black.mp4"
    subprocess.run([
        "ffmpeg", "-y",
        "-f", "lavfi", "-i", f"color=c=black:s=1280x720:d={BLACK_DUR}",
        "-c:v", "libx264", "-preset", "fast", "-crf", "23",
        "-pix_fmt", "yuv420p",
        "-t", str(BLACK_DUR),
        str(black_path)
    ], capture_output=True, check=True, timeout=30)
    # --- Step 5: concat video ---
    all_clips = [black_path, hook_path] + scene_paths
    raw_vid = work / "raw_video.mp4"

    print(f"\n🔗 Concatenating {len(all_clips)} clips...")
    if args.transition == "crossfade" and len(all_clips) > 2:
        xfade_dur = min(beat_sec * 0.5, 0.4)  # half-beat crossfade, max 0.4s
        scene_label = f"[1:v]"
        durs = [probe_dur(p) for p in all_clips]
        inputs = []
        for p in all_clips:
            inputs.extend(["-i", str(p)])
        parts = []
        for i in range(2, len(all_clips)):
            offset = sum(durs[1:i]) - xfade_dur * (i - 1)
            next_label = f"x{i}"
            parts.append(
                f"{scene_label}[{i}:v]xfade=transition=fade:duration={xfade_dur}:offset={offset:.3f}[{next_label}]"
            )
            scene_label = f"[{next_label}]"
        filter_str = ";".join(parts)
        concat_filter = f"[0:v]{scene_label}concat=n=2:v=1:a=0[outv]"
        full_filter = filter_str + ";" + concat_filter if filter_str else concat_filter
        try:
            subprocess.run([
                "ffmpeg", "-y"] + inputs + [
                "-filter_complex", full_filter,
                "-map", "[outv]",
                "-c:v", "libx264", "-preset", "fast", "-crf", "23",
                "-pix_fmt", "yuv420p",
                "-movflags", "+faststart",
                str(raw_vid)
            ], capture_output=True, check=True, timeout=300)
            print(f"   Crossfade: {xfade_dur:.1f}s transitions between {len(all_clips)-2} scenes")
        except subprocess.CalledProcessError:
            print(f"   Crossfade failed, falling back to hard cuts")
            # Fall through to hard cut below
            args.transition = "cut"

    if args.transition != "crossfade":
        inputs = []
        labels = []
        for i, p in enumerate(all_clips):
            inputs.extend(["-i", str(p)])
            labels.append(f"[{i}:v]")
        filter_str = "".join(labels) + f"concat=n={len(all_clips)}:v=1:a=0[outv]"
        subprocess.run([
            "ffmpeg", "-y"] + inputs + [
            "-filter_complex", filter_str,
            "-map", "[outv]",
            "-c:v", "libx264", "-preset", "fast", "-crf", "23",
            "-pix_fmt", "yuv420p",
            "-movflags", "+faststart",
            str(raw_vid)
        ], capture_output=True, check=True, timeout=180)
    vid_dur = probe_dur(raw_vid)
    print(f"   -> {fmt(vid_dur)}")

    # --- Step 6: build audio track ---
    #
    # Audio envelope:
    #   0 - hook_start: silence (black lead-in)
    #   hook_start - hook_end: music at 20% volume (present but low, dialogue dominant)
    #   hook_end: music "drops" to 100% (dramatic release on first scene cut)
    #   hook_end - end: music full
    #   last 3s: music fade out
    #
    # Dialogue is boosted to ~-10dB to cut through the music.

    hook_start = BLACK_DUR
    hook_end = hook_start + hook_actual
    fade_out_dur = min(3.0, vid_dur * 0.12)
    music_drop_dur = 0.15  # how fast music goes from 20% -> 100% at hook end

    # These will be set during mixing, init to safe defaults for reporting
    hook_db = -999.0
    dialogue_boost = 4.0

    if args.song and Path(args.song).exists():
        print(f"\n🎵 Mixing: {args.song}")
        song_path = Path(args.song)
        final_audio = work / "mixed_audio.aac"

        # Extract hook dialogue
        hook_audio = work / "hook_audio.aac"
        subprocess.run([
            "ffmpeg", "-y", "-i", str(hook_path), "-vn",
            "-c:a", "aac", str(hook_audio)
        ], capture_output=True, check=True)

        # Auto-detect and calculate boost
        hook_db = probe_max_volume(hook_audio)
        if hook_db is not None:
            # Target: -10dB after boost (loud enough to be clear over music)
            boost_db = DIALOGUE_LOUDNESS_TARGET - hook_db
            # Clamp boost: between 2x (6dB) and 8x (18dB)
            boost_db = max(6.0, min(18.0, boost_db))
            dialogue_boost = 10 ** (boost_db / 20)  # convert dB to linear gain
            dialogue_boost = round(dialogue_boost, 1)
            print(f"   Hook audio at {hook_db:.1f} dB -> boosting {boost_db:.0f} dB (x{dialogue_boost})")
        else:
            dialogue_boost = 4.0
            print(f"   Could not probe volume, defaulting to x{dialogue_boost} boost")

        # Silence for black
        silence_audio = work / "silence.aac"
        subprocess.run([
            "ffmpeg", "-y",
            "-f", "lavfi", "-i", f"anullsrc=r=44100:cl=stereo:d={BLACK_DUR}",
            "-c:a", "aac", "-b:a", "192k",
            str(silence_audio)
        ], capture_output=True, check=True)

        # Concat: silence + hook -> dialogue track
        dialogue_track = work / "dialogue_track.aac"
        with open(work / "dialog_concat.txt", "w") as f:
            f.write(f"file '{silence_audio}'\n")
            f.write(f"file '{hook_audio}'\n")
        subprocess.run([
            "ffmpeg", "-y", "-f", "concat", "-safe", "0",
            "-i", str(work / "dialog_concat.txt"), "-c", "copy",
            str(dialogue_track)
        ], capture_output=True, check=True)

        # Mix dialogue + music
        # Music at 20% during hook, then drops to 100% at first scene cut
        filter_str = (
            f"[0:a]adelay=0|0[d];"
            f"[1:a]adelay=0|0,"
            f"volume=0:enable='lt(t,{hook_start})',"
            f"volume=0.20:enable='between(t,{hook_start},{hook_end})':eval=frame,"
            f"afade=t=in:st={hook_end}:d={music_drop_dur},"
            f"volume=1.0:enable='gte(t,{hook_end})':eval=frame,"
            f"afade=t=out:st={vid_dur-fade_out_dur}:d={fade_out_dur}[m];"
            f"[d]volume={dialogue_boost}[d_boosted];"
            f"[d_boosted][m]amix=inputs=2:duration=longest:dropout_transition=0,"
            f"volume=2.0[aout]"
        )

        subprocess.run([
            "ffmpeg", "-y",
            "-i", str(dialogue_track),
            "-i", str(song_path),
            "-filter_complex", filter_str,
            "-map", "[aout]",
            "-c:a", "aac", "-b:a", "192k",
            str(final_audio)
        ], capture_output=True, check=True, timeout=60)
    else:
        print("\n🎵 No song — hook audio only")
        hook_audio = work / "hook_audio.aac"
        subprocess.run([
            "ffmpeg", "-y", "-i", str(hook_path), "-vn",
            "-c:a", "aac", str(hook_audio)
        ], capture_output=True, check=True)
        silence_audio = work / "silence.aac"
        subprocess.run([
            "ffmpeg", "-y",
            "-f", "lavfi", "-i", f"anullsrc=r=44100:cl=stereo:d={BLACK_DUR}",
            "-c:a", "aac", "-b:a", "192k",
            str(silence_audio)
        ], capture_output=True, check=True)
        final_audio = work / "dialog_audio.aac"
        with open(work / "dialog_concat.txt", "w") as f:
            f.write(f"file '{silence_audio}'\n")
            f.write(f"file '{hook_audio}'\n")
        subprocess.run([
            "ffmpeg", "-y", "-f", "concat", "-safe", "0",
            "-i", str(work / "dialog_concat.txt"), "-c", "copy",
            str(final_audio)
        ], capture_output=True, check=True)

    # --- Step 7: trim & mux ---
    trimmed_audio = work / "trimmed_audio.aac"
    subprocess.run([
        "ffmpeg", "-y", "-i", str(final_audio), "-t", str(vid_dur),
        "-c:a", "aac", "-b:a", "192k", str(trimmed_audio)
    ], capture_output=True, check=True)

    print("\n🎬 Muxing final video...")
    subprocess.run([
        "ffmpeg", "-y",
        "-i", str(raw_vid), "-i", str(trimmed_audio),
        "-c:v", "copy",
        "-map", "0:v:0", "-map", "1:a:0",
        "-c:a", "aac", "-b:a", "192k",
        "-shortest",
        "-movflags", "+faststart",
        str(out)
    ], capture_output=True, check=True)

    # --- Step 8: cleanup ---
    actual_dur = probe_dur(out)
    size_mb = out.stat().st_size / 1024 / 1024
    print(f"\n✅ -> {out}")
    print(f"   Duration: {fmt(actual_dur)} (max: {fmt(max_dur)})")
    print(f"   Size: {size_mb:.1f} MB")
    print(f"   BPM: {bpm} | Beat: {beat_sec:.2f}s | Scene dur: {fmt(actual_scene_dur)} ({int(actual_scene_dur/beat_sec)} beats)")
    print(f"   Audio: {fmt(BLACK_DUR)}s silence -> {fmt(hook_actual)}s dialogue+music -> {(actual_dur - hook_end):.1f}s music only")
    if beat_positions:
        print(f"   Beat-aligned: scenes snapped to {len(beat_positions)} detected transients")
    print(f"   Transition: {args.transition}")
    if hook_db is not None:
        print(f"   Hook audio: {hook_db:.1f} dB -> boosted x{dialogue_boost}")

    if not args.keep:
        shutil.rmtree(work)

    return actual_dur <= max_dur + 0.5


def main():
    p = argparse.ArgumentParser(
        description="Montage Maker - build beat-synced video montages"
    )
    p.add_argument("movie", nargs="+",
                   help="Movie file(s) for scene clips (multiple = interleaved)")
    p.add_argument("--hook", required=True, help="Hook range (mm:ss-mm:ss)")
    p.add_argument("--hook-movie", help="Separate file for the hook clip")
    p.add_argument("--scenes", nargs="+", required=True,
                   help="Scene ranges: mm:ss-mm:ss ...")
    p.add_argument("--song", help="Background music file")
    p.add_argument("--bpm", type=float,
                   help="Beats per minute (auto-detected if omitted)")
    p.add_argument("--output", default="montage.mp4", help="Output file")
    p.add_argument("--max-dur", type=float, default=TARGET_DUR,
                   help=f"Max duration (default: {TARGET_DUR}s)")
    p.add_argument("--scene-dur", type=float, default=SCENE_DUR,
                   help=f"Per-scene duration (default: {SCENE_DUR}s)")
    p.add_argument("--hook-dur", type=float, default=HOOK_DUR,
                       help=f"Max hook duration (default: {HOOK_DUR}s)")
    p.add_argument("--transition", choices=["cut", "crossfade"], default="cut",
                       help="Scene transition style: cut or crossfade (default: cut)")
    p.add_argument("--keep", action="store_true", help="Keep temp files")

    ok = build(p.parse_args())
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
