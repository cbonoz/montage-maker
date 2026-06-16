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

**Build:**

```bash
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
    --transition crossfade \
    --output projects/blade_runner_2049/output/br2049_stranger_montage.mp4
```

---

### 2. br2049_freysa — "Dying for the right cause"

**Status:** ✅ Built

**Hook (monologue):**
> "Dying for the right cause. It's the most human thing we can do." — Freysa

**Music:** Penumbra @ 70 BPM (dark, glacial)

**Output:** `output/br2049_freysa_montage_Penumbra.mp4`

**Source clips used:**
- `hook_freysa.mp4` — "Dying for the right cause..." (8s, 1080p)
- `scenes_compilation.webm` — "4 Minutes of Blade Runner 2049 in 4K" (241s)
- `scene_freysa_K.mp4` — "Blade Runner 2049 - Freysa and K" (118s)

**Build:**

```bash
python build_montage.py \
    projects/blade_runner_2049/source/scenes_compilation.webm \
    projects/blade_runner_2049/source/scene_freysa_K.mp4 \
    --hook-movie projects/blade_runner_2049/source/hook_freysa.mp4 \
    --hook 0-7.7 --hook-dur 7.7 \
    --bpm 70 \
    --scenes \
        10-13 30-33 50-53 70-73 90-93 110-113 \
        130-133 30-33 170-173 50-53 210-213 70-73 \
        10-13 90-93 \
    --song sounds/Penumbra.mp3 \
    --max-dur 35 --scene-dur 1.5 \
    --transition crossfade \
    --output projects/blade_runner_2049/output/br2049_freysa_montage_Penumbra.mp4
```
