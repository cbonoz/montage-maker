# Interstellar — Montages

Montages from Interstellar, exploring humanity, exploration, and sacrifice.

## Montages

### 1. interstellar_mankind — "Mankind was born on Earth..."

**Status:** ✅ Built

**Hook (monologue):**
> "Mankind was born on Earth. It was never meant to die here." — Brand

**Music:** Penumbra @ 70 BPM (dark, glacial, epic)

**Output:** `output/interstellar_mankind_montage_Penumbra.mp4`

**Source clips used:**
- `hook_mankind.mp4` — "Interstellar: 'Mankind was born on Earth...'" (62s, 1080p)
- `scenes_compilation.mp4` — "5 Minutes of Interstellar in 4K" (281s)

**Hook timing (found via Whisper):**
```
"Mankind was born on Earth..." → ~44–53s
Full exchange → 44-54s
```

**Build:**

```bash
python build_montage.py \
    projects/interstellar/source/scenes_compilation.mp4 \
    --hook-movie projects/interstellar/source/hook_mankind.mp4 \
    --hook 44-54 --hook-dur 10 \
    --bpm 70 \
    --scenes \
        10-13 30-33 50-53 70-73 90-93 110-113 \
        130-133 150-153 170-173 190-193 210-213 230-233 \
    --song sounds/Penumbra.mp3 \
    --max-dur 30 --scene-dur 1.5 \
    --transition crossfade \
    --output projects/interstellar/output/interstellar_mankind_montage_Penumbra.mp4
```

## Vibe

Epic, humanist, bittersweet — Brand's words frame humanity's journey among the stars. Penumbra's glacial strings match the vast emptiness of space and the urgency of survival.
