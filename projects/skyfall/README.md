# Skyfall — Montages

A collection of montages from the James Bond film Skyfall, exploring themes of loyalty, defiance, and the spy game.

## Montages

### 1. skyfall_loyalty — "I need you back"

**Status:** ✅ Built

**Hook (two-party):**
> **M:** "I need you back."
> **Bond:** "I never left."

**Alternative hook (power dynamic exchange):**
> **M:** "If you fail, it's my head."
> **Bond:** "If I fail, you'll be dead before I am."

**Music:** sb_snowfall @ 80 BPM
**Alt Music:** Penumbra

**Output:** `output/skyfall_loyalty_montage_sb_snowfall.mp4`

**Source clips used:**
- `hook_ms_apartment.mp4` — M's apartment scene (hook at 64-70s, sourced from YouTube)
- `scenes_compilation.mp4` — Skyfall best scenes compilation

**Hook timing (found via find_dialogue.py):**
```
"I need you back" → 64.2-69.7s
"I never left"    → 66.3-69.7s
Combined hook     → 64-70s
```

**Build:**

```bash
# Find dialogue timestamps automatically
uv run find_dialogue.py \
    "https://www.youtube.com/watch?v=WFwmDq-MKaE" \
    "I need you back" --output hook
# → 64.2-69.7

# Build montage
python build_montage.py \
    projects/skyfall/source/scenes_compilation.mp4 \
    --hook-movie projects/skyfall/source/hook_ms_apartment.mp4 \
    --hook 64-70 --hook-dur 6 \
    --bpm 80 \
    --scenes \
        30-33 60-63 90-93 120-123 150-153 180-183 \
        210-213 240-243 270-273 300-303 330-333 360-363 \
    --song sounds/sb_snowfall.mp3 \
    --max-dur 30 --scene-dur 1.5 \
    --output projects/skyfall/output/skyfall_loyalty_montage_sb_snowfall.mp4
```

## Notes

- The "I need you back" / "I never left" exchange is the ideal two-party hook: three words each, no exposition, instant power dynamics
- M is stern, Bond is defiant — you know their relationship instantly
- sb_snowfall provides cinematic, brooding pacing appropriate for spy thriller aesthetics
- This montage works best with a mix of explosive action shots and quieter character moments
- Penumbra (70 BPM) could be used as an alternative for slower, more introspective pacing
