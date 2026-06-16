# Montage Construction Guide

A technical reference for building montages with beat-aligned scenes, dialogue synchronization, and clip sourcing strategies.

## Status Legend

| Badge | Meaning |
|-------|---------|
| ✅ **Built** | Montage has been generated and output exists |
| 🎬 **Clips sourced** | Source clips downloaded, ready to build |
| 📝 **Planned** | Idea documented, needs sourcing |
| 🔁 **Reusable** | Uses clips already downloaded for another idea |
| ⚠️ **Light dialogue** | Hook is a punchline — needs strong visuals or short edit to work |

---

## Beat-Aligned Scene Transitions

### Why Beats Matter

Every montage lives or dies on **visual rhythm alignment with music**. A scene cut that lands *between* a musical beat feels jarring; a cut that lands *on* a beat feels inevitable. This is the foundation of montage craft.

### BPM Calculations

**BPM (Beats Per Minute)** determines scene cut frequency:

- **60 BPM**: 1 beat per second → 1 scene cut per second
- **70 BPM**: ~1.17 beats per second → 1 scene cut per 0.86s
- **80 BPM**: 1.33 beats per second → 1 scene cut per 0.75s

For a **30-second montage**, aim for:
- **12–16 scene cuts** (one cut every 2–2.5 seconds)
- This paces at roughly **80 BPM** naturally

### Beat Sync Workflow

1. **Identify the song's downbeat** — listen for the strongest pulse or drum hit
2. **Mark beats in your editor** — count from the hook's start to identify every 4th beat (musical measure)
3. **Cut scenes to land on measures, not individual beats** — scenes last 2–4 musical beats (0.5–2 seconds per scene)
4. **Offset hook strategically** — let the hook dialog sit for 1–2 beats before the first scene cut, so the audio draws focus

Example: At 80 BPM, a 4-beat measure = 3 seconds. Cut scenes to land at 0s, 3s, 6s, 9s, etc.

### Automatic Beat Alignment

`build_montage.py` **places scene cuts directly at detected transient peaks** in the music
(kick drums, snare hits, sharp chord changes) rather than computing fixed intervals and
snapping. This means:

- Each scene cut lands on an **actual musical event**, not just an arithmetic position
- **Variable scene durations** (typically 1.5–3.0s) create natural rhythmic variation
- Works best with percussive music (sb_snowfall, Penumbra, TheLongDark)
- Ambient music gracefully falls back to fixed beat-snapped durations

```
# Before (fixed intervals + snap):
[0.5s black] [10.0s hook] [1.71s] [1.71s] [1.71s] ...

# After (transient-aligned walk):
[0.5s black] [10.0s hook] [1.60s] [1.70s] [1.53s] ...
                            ^ each cut lands on a real musical downbeat
```

### Dynamic Post-Hook Buffer

Instead of a fixed silence gap after the hook, `build_montage.py` analyzes the hook clip's
audio to find the last moment where volume exceeds a silence threshold (2% of max energy).
The buffer adjusts dynamically:

```
trailing_silence = hook_actual - last_audio_moment
actual_buffer = max(0.3s, 2.0s - trailing_silence)
```

- Clips with natural trailing silence get less artificial pause
- Clips that cut off abruptly get the full 2.0s buffer
- The hook video's last frame lingers during the buffer for a natural pause

---

## Music + Hook Dialogue Synchronization

### Audio Envelope Strategy

**Hook placement** sets the emotional tone (automated by `build_montage.py`):

| Time range | Video | Audio |
|------------|-------|-------|
| **0–0.5s** | Black lead-in | Silence |
| **0.5s–hook_end** | Hook dialogue clip | Dialogue full volume + **music at 2%** (barely audible bed) |
| **hook_end-0.3s–hook_end** | Final dialogue words | Music swells from 2% → **~17%** (still low, dialogue dominant) |
| **hook_end–hook_end+1.7s** | First scene cuts | Music continues rising from 17% → 100% |
| **hook_end+1.7s–last 3s** | Scene montage | Music full volume |
| **Last 3s** | Final scenes | Music fades out |

### Audio Envelope Details

The music never fully cuts out — it stays as a low bed during the hook, then transitions smoothly:

```
Volume level:
  100% │                         ╱──────────────────
       │                        ╱
   50% │                       ╱
       │                      ╱
   17% │ ╱───────────────────╱
    2% │╱
    0% │
       └─────────────────────────────────────────────
       0s 0.5s   hook_start    hook_end          time
             │black│──── dialogue ────│── ramp ──│─ full ─│
                                  └─↗ 0.3s overlap
```

The 2% music bed during dialogue gives a sense of the song without competing with the words. In the last 0.3s of dialogue, the music starts swelling to ~17% — you feel it coming but the dialogue stays clear. After dialogue ends, the music takes over fully over 1.7s.

**Hook clip audio** is processed to **remove original background music/SFX**, replacing it with the montage song:
1. `pan=mono|c0=FL+FR` — extract center channel (dialogue is center-panned, music/SFX are wider)
2. `highpass=f=150,lowpass=f=5000` — keep only speech frequencies
3. `afftdn=nr=15:nf=-30` — FFT noise reduction to clean residual background

The montage song becomes the **sole background audio** — it plays at 2% during the hook (barely audible), then swells to full volume when scenes begin.

### Song Intro Detection

Many songs have quiet intros (ambient pads, fading in) that don't fit a montage. `build_montage.py` **detects the first musical onset** and skips any silent/quiet intro before it:

```python
# Analyzes first 15s of the song
# Finds first sustained energy peak
# Skips anything before it
# Backs up 1s for context
```

This means the song starts at the first meaningful moment — not awkward silence or a 10-second ambient fade-in.

### Fade Timing

- **Hook audio**: center-channel extracted (`pan=mono|c0=FL+FR`) + high/low pass + noise reduction
- **Dialogue**: automatically boosted to ~-10dB to be clear over the music bed
- **Music bed**: 2% volume during early hook (barely audible)
- **Pre-overlap**: music swells from 2% → ~17% in last 0.3s of dialogue (dialogue still dominant)
- **Post-overlap**: music continues from 17% → 100% over 1.7s after dialogue ends
- **Song intro**: automatically detected and skipped (starts at first musical onset)
- **Scene audio**: Mute original scene audio entirely (use only music + hook dialogue)

### Hook Duration & the `--hook-dur` Fix

`--hook-dur` is no longer required for most use cases. The script now uses the full range
of `--hook` by default. The old 3-second cap (`HOOK_DUR = 3.0`) only applies when no
`--hook` range is given at all. If you want to truncate a hook shorter than its range,
use `--hook-dur` explicitly.

**What changed:**
- `--hook-dur` default is now `None` (not `HOOK_DUR`)
- The 30%-of-max-duration cap only applies when the range is auto-derived
- Explicit `--hook-dur` values are used without any percentage cap

### Transient Detection Threshold

The beat detection threshold was changed from `median + 1.5 × IQR` to `max_energy × 0.5`.
The IQR-based threshold often exceeded the maximum energy of dynamic orchestral tracks
(sb_snowfall, Legazy, Penumbra), resulting in zero beats detected. The 50%-of-max threshold
reliably finds 500–600 transients in the first 30s of any soundtrack.

### Crossfade Transitions

Use `--transition crossfade` to enable smooth dissolves between scenes instead of hard cuts:

```bash
python build_montage.py movie.mp4 \
    --hook 1:30-1:35 \
    --scenes 5:10-5:14 12:20-12:24 25:00-25:04 \
    --song sounds/sb_snowfall.mp3 --bpm 80 \
    --transition crossfade \
    --output montage.mp4
```

- Crossfade duration = half a beat (0.4s at 80 BPM)
- Black → hook is always a hard cut (cinematic lead-in)
- Hook → scenes use crossfade for smooth visual flow
- Best for: emotional/melancholic montages where hard cuts feel too jarring
- Best for: music with clear dynamic shifts where dissolves match the ebb and flow
- Falls back to hard cuts automatically if ffmpeg's xfade filter fails

**Known pitfall (fixed):** The crossfade implementation previously had a bug where the
hook clip was silently dropped from the output (only black + 1 scene rendered) and the
offset calculation used absolute timeline positions instead of tracking accumulated
chain duration. Both issues were fixed in the Deckard & Rachael montage build.

### When to Mute

Always mute:
- Original film dialogue during scenes (conflicts with hook)
- Background music from original scenes (use only the montage track)
- Ambient noise/foley (keep it clean)

Keep (subtle):
- Rare action moments where the original sound effect is iconic (e.g., light saber hum, specific sword clash)

---

## Clip Sourcing Strategy

### Hook Selection Tips

**Strong hooks are:**
- **Specific** — "I will have my vengeance" not "I'm angry"
- **Universal** — works outside the film's context
- **Brief** — 2–3 seconds of clean dialogue
- **Two-party** — question + response, not a solo speech (more dynamic)

**Weak hooks are:**
- **Punchlines** — "No capes!" works only with visual comedy setup (⚠️ Light dialogue)
- **Exposition** — "I'm the villain because..." is too heavy-handed
- **Mumbled/noisy** — original audio has dialogue overlap or music underneath

**Verify clips first.** Many short YouTube clips titled with a quote are fan-made text
overlays, not actual movie footage. Before downloading:
1. Check the video description for source details
2. Use `--dump-json` to inspect resolution (1080p suggests real footage)
3. Run `find_dialogue.py` on the clip — 0 segments or garbled audio (only "You" every 30s)
   means it's a fake
4. Prefer longer scene clips (60s+) over short quote clips when possible
5. When in doubt, use a full scene file as both hook source and scenes source

### Scene Variety

Extract clips from **different parts of the film** to maximize visual contrast:

- Opening scenes (establishing)
- Action sequences (energy)
- Character moments (intimacy)
- Wide shots (scope)
- Close-ups (emotion)

Interleave them: avoid two action scenes back-to-back unless the montage theme demands it.

### Multi-Source Interleaving

When sourcing from multiple YouTube videos or recordings:

1. **Download separately** (e.g., `hook.mkv`, `scenes_part1.mp4`, `scenes_part2.webm`)
2. **Trim in editing software** before concatenating
3. **Stitch with ffmpeg** or your editor's timeline
4. **Verify color grading consistency** — if sources vary (one is crushed blacks, another is blown out), grade them to match

Example command to concat:
```bash
ffmpeg -f concat -safe 0 -i filelist.txt -c copy output.mp4
```

Where `filelist.txt` lists:
```
file 'hook.mkv'
file 'scenes_part1.mp4'
file 'scenes_part2.webm'
```

---

## Finding Dialogue Timestamps Automatically

Use `find_dialogue.py` to locate exact hook timestamps in YouTube-sourced clips:

```bash
# Search for a line in a YouTube clip
uv run find_dialogue.py "https://www.youtube.com/watch?v=OgU1QOkFFT0" "vengeance"

# Output -> hook format for build_montage.py
TIMING=$(uv run find_dialogue.py "https://youtu.be/..." "dialogue" --output hook)
python build_montage.py movie.mp4 --hook "$TIMING" ...
```

**How it works:** Fetches YouTube's existing captions (auto-generated or manual) via `youtube-transcript-api`, then searches for the dialogue text. Transcripts are cached locally in `transcripts/` for reuse.

**When to use transcripts:**
- **Hook dialogue** — always use `find_dialogue.py` to get exact timestamps (the dialogue needs to be word-perfect and cleanly extracted)
- **Scene clips** — transcripts are not needed. Scene audio is muted entirely (replaced by music). Just pick timestamps that give visual variety — different locations, lighting, action levels
- The beat alignment (`detect_beat_positions`) and crossfade transitions handle the rest

### When Whisper Can't Transcribe Dialogue

Some clips have challenging audio (music underneath, low dialogue volume) that even the
`small` Whisper model can't cleanly transcribe. Strategies for finding dialogue timestamps
in difficult clips:

1. **Search for fan edits** — a short fan edit that explicitly titles itself with the
   dialogue text (e.g. "do you love me, do you trust me | Blade Runner") is often easier
   to work with than a raw scene clip
2. **Extract sections** — use ffmpeg to extract 20-second audio chunks around the
   expected dialogue, then run Whisper on just those sections for more reliable results
3. **Search adjacent text** — if the exact line isn't found, search for the line before
   or after it in the transcript
4. **Use a larger model** — `--model medium` or `--model large` improves accuracy on
   music-heavy clips (at the cost of speed)

---

## Common Pitfalls & Solutions

### Pitfall: "Hook dialogue and music clash"
**Solution:** Reduce music volume to -20dB during hook (leave room for dialogue), crossfade back up after.

### Pitfall: "Scene cuts feel random, not rhythmic"
**Solution:** Use a metronome in your DAW or editor to mark every beat. Cut only on multiples of 2–4 beats.

### Pitfall: "Montage is too fast / too slow"
**Solution:** Adjust scene duration, not BPM. Longer scenes = slower pacing; shorter scenes = faster pacing. Aim for 12–16 cuts in 30s.

### Pitfall: "Hook audio is noisy or echoes"
**Solution:** Normalize to -3dB, apply gentle high-pass filter (remove rumble), use noise gate if needed. Clean audio before building the montage.

### Pitfall: "Montage feels flat despite good clips"
**Solution:** Add 1–2 dB of gentle compression to the final mix (bring up quiet moments, prevent peaks), add a subtle reverb tail to the hook dialogue fade (0.5s decay).

### Pitfall: "Reusable clips don't feel fresh in a new montage"
**Solution:** Use different trim points from the same scene (earlier/later frames), change the playback speed slightly (98% vs 102%), or flip horizontally if it doesn't break continuity.

---

## CSV Usage Examples

### Bash Query: List all Built montages
```bash
grep "✅ Built" MONTAGE_IDEAS.csv | cut -d',' -f1,2,4
```

Output:
```
dk_hero_villain,The Dark Knight,output/dark_knight_montage.mp4
hp_yer_a_wizard,Harry Potter and the Philosopher's Stone,output/hp_montage_30s_final.mp4
...
```

### Bash Query: Find all Reusable clips
```bash
grep "🔁 Reusable" MONTAGE_IDEAS.csv | cut -d',' -f1,2,3
```

Output:
```
hp_hermione_arrival,Harry Potter and the Philosopher's Stone,You are a wizard...
dk_bane_strength,The Dark Knight Rises,Peace has cost you your strength
...
```

### Python Query: Load CSV and filter by mood
```python
import csv

with open('MONTAGE_IDEAS.csv', 'r') as f:
    reader = csv.DictReader(f)
    for row in reader:
        if row['mood'] == 'vengeance':
            print(f"{row['project_id']}: {row['dialogue_hook']}")
            print(f"  Music: {row['music_primary']} @ {row['bpm']} BPM")
            print()
```

### Python Query: Build montage from CSV specs
```python
import csv
import subprocess

def build_from_csv(project_id):
    with open('MONTAGE_IDEAS.csv', 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row['project_id'] == project_id:
                cmd = [
                    'python', 'build_montage.py',
                    f"projects/{project_id}",
                    f"sounds/{row['music_primary']}",
                    '--bpm', row['bpm']
                ]
                subprocess.run(cmd)
                break

build_from_csv('dk_hero_villain')
```

---

## Reference: Song BPM & Pacing

| Song | BPM | Best for |
|------|-----|----------|
| sb_snowfall.mp3 | 80 | Epic, cinematic, wintery |
| FirstSnow.mp3 | 75 | Gentle, emotional |
| Penumbra.mp3 | 70 | Dark, longing |
| Unraveling.mp3 | 75 | Bittersweet |
| Meanwhile.mp3 | 80 | Dreamy, wonder |
| Moonlight.mp3 | 75 | Simple, nostalgic |

