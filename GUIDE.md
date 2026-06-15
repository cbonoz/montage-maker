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

`build_montage.py` now **detects actual transient peaks** in the music (kick drums, snare hits, sharp chord changes) and snaps each scene boundary to the nearest detected downbeat. This means:

- Each scene cut lands on an **actual musical event**, not just an arithmetic position
- **Variable scene durations** create natural rhythmic variation instead of robotic uniformity
- Works best with percussive music (sb_snowfall, Penumbra)
- Ambient music (Moonlight, Meanwhile) gracefully falls back to fixed durations

```
# Scene boundaries before (fixed, may drift from beats):
[0.5s black] [6.4s hook] [1.60s] [1.60s] [1.60s] ...

# Scene boundaries after (snapped to actual music transients):
[0.5s black] [6.4s hook] [1.58s] [1.63s] [1.58s] ...
                              ^ each boundary snaps to nearest detected beat
```

---

## Music + Hook Dialogue Synchronization

### Audio Envelope Strategy

**Hook placement** sets the emotional tone (automated by `build_montage.py`):

| Time range | Video | Audio |
|------------|-------|-------|
| **0–0.5s** | Black lead-in | Silence |
| **0.5s–hook_end** | Hook dialogue clip | Dialogue only — **no music** (clean, isolated dialogue) |
| **hook_end** (the drop) | First scene cut begins | Music fades in over 0.15s |
| **hook_end–last 3s** | Scene montage | Music full volume |
| **Last 3s** | Final scenes | Music fades out |

### Music Drop Timing

The music is completely silent during the hook — only the native dialogue audio is heard. This creates two effects:

- **Clean focus on the quote** — no music competes with the words
- **Dramatic impact** — when the hook ends, the music enters fresh alongside the first scene cut, hitting like a new chapter

```
Audio Timeline:
  [silence 0.5s] → [dialogue only 6.4s] → [music fades in 0.15s] → [music full → fade out 3s]
                                          ↑ first scene cut lands here
```

### Fade Timing

- **Dialogue fade-out**: instantaneous at hook end (dialogue stops, music takes over)
- **Music drop**: 0.15s ramp from 20% → 100% at hook end (the "drop")
- **Scene audio**: Mute original scene audio entirely (use only music + hook dialogue)

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

**Limitations:**
- Only works for YouTube videos that have captions enabled
- Auto-generated captions may mangle words (e.g., "vengeance" → "venyards")
- Use broader search terms or adjacent text when exact phrases fail
- Verify the returned segment by checking adjacent segments for context

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

