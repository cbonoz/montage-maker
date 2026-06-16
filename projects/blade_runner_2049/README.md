# Blade Runner 2049 — Montages

Montages from Blade Runner 2049, exploring themes of loneliness, humanity, and connection.

## Montages

### 1. br2049_stranger — "Sometimes to love someone..."

**Status:** ✅ Built

**Hook (monologue):**
> "Sometimes to love someone, you gotta be a stranger." — Joi

**Music:** Penumbra @ 70 BPM (dark, longing, glacial)

**Output:** `output/br2049_stranger_montage.mp4`

**Source clips used:**
- `hook_stranger.mkv` — "Sometimes to love someone, you gotta be a stranger." (14s YouTube clip)
- `scenes_compilation.webm` — "4 Minutes of Blade Runner 2049 in 4K" (241s)

**Hook timing (found via Whisper):**
```
"Sometimes to love someone, you gotta be a stranger." → 0.0-7.0s
Uses the entire clip as hook source
```

**Build:**

```bash
# Find hook timestamps (Whisper transcribes local files)
uv run find_dialogue.py projects/blade_runner_2049/source/hook_stranger.mkv "stranger"

# Build montage
python build_montage.py \
    projects/blade_runner_2049/source/scenes_compilation.webm \
    --hook-movie projects/blade_runner_2049/source/hook_stranger.mkv \
    --hook 0-7 --hook-dur 7 \
    --bpm 70 \
    --scenes \
        10-13 30-33 50-53 70-73 90-93 110-113 \
        130-133 150-153 170-173 190-193 210-213 230-233 \
    --song sounds/Penumbra.mp3 \
    --max-dur 30 --scene-dur 1.5 \
    --output projects/blade_runner_2049/output/br2049_stranger_montage.mp4
```
