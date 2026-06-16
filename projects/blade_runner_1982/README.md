# Blade Runner (1982) — Montages

Montages from the original Blade Runner, exploring themes of humanity, memory, and connection.

## Montages

### 1. br_deckard_rachael — "Do you love me? Do you trust me?"

**Status:** ✅ Built

**Hook (two-party dialogue):**
> Deckard: "Do you love me?"  
> Rachael: "I love you."  
> Deckard: "Do you trust me?"  
> Rachael: "I trust you."

**Music:** Penumbra @ 70 BPM (dark, glacial, longing)

**Output:** `output/br_deckard_rachael_montage.mp4`

**Source clips used:**
- `hook_excerpt_dialogue.mp4` — "Blade Runner - Rachael and Deckard (Excerpt)" trimmed to 20s scene (193–213s)
- `scenes_compilation.mp4` — "Amazing Shots of BLADE RUNNER" (324s)

**Hook timing:**
```
Do you love me? → ~2–5s
I love you.     → ~5–7s
Do you trust me? → ~12–14s
I trust you.    → ~14–16s
```

**Build:**
```bash
python build_montage.py \
    projects/blade_runner_1982/source/scenes_compilation.mp4 \
    --hook-movie projects/blade_runner_1982/source/hook_excerpt_dialogue.mp4 \
    --hook 0-20 \
    --bpm 70 \
    --scenes \
        5-7 22-24 42-44 60-62 80-82 \
        98-100 115-117 135-137 152-154 170-172 \
        190-192 210-212 230-232 250-252 270-272 \
    --song sounds/Penumbra.mp3 \
    --max-dur 40 --scene-dur 1.5 \
    --transition crossfade \
    --output projects/blade_runner_1982/output/br_deckard_rachael_montage.mp4
```
