# Harry Potter and the Deathly Hallows — Montages

Montages from the final Harry Potter installment, exploring memory, sacrifice, and love.

## Montages

### 1. hp_always — "Always"

**Status:** ✅ Built

**Hook (two-party):**
> **Dumbledore:** "After all this time?"
> **Snape:** "Always."

**Music:** FirstSnow @ 75 BPM

**Output:** `output/hp_always_montage.mp4`

**Source clips used:**
- `hook_always.webm` — "After all this time? Always." scene (YouTube, 82s)
- `mc_snapes_death.mp4` — Snape's death scene
- `hook_snape_memories.mp4` — Snape's memories of Lily

**Hook timing (found via find_dialogue.py):**
```
"Always" → 78.7-82.7s in hook_always.webm
Full exchange → 72-82s
```

**Build:**

```bash
# Find hook timestamps
uv run find_dialogue.py "https://www.youtube.com/watch?v=LeG_judrcOA" "Always"

# Build montage
python build_montage.py \
    projects/harry_potter_deathly_hallows/source/mc_snapes_death.mp4 \
    projects/harry_potter_deathly_hallows/source/hook_snape_memories.mp4 \
    --hook-movie projects/harry_potter_deathly_hallows/source/hook_always.webm \
    --hook 72-82 --hook-dur 10 \
    --bpm 75 \
    --scenes \
        10-13 20-23 40-43 60-63 90-93 120-123 \
        140-143 30-33 50-53 80-83 110-113 150-153 \
    --song sounds/FirstSnow.mp3 \
    --hook-text "After all this time?|Always" \
    --max-dur 30 --scene-dur 1.5 \
    --output projects/harry_potter_deathly_hallows/output/hp_always_montage.mp4
```
