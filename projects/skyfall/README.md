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

**Output:** `output/skyfall_loyalty_montage.mp4`

**Source clips used:**
- `hook_ms_apartment.mp4` — M's apartment scene (hook at 68-72s from silencedetect analysis)
- `scenes_compilation.mp4` — Skyfall best scenes compilation

**Scenes sampled:**
- Opening chase in Istanbul
- Bond falling from the bridge
- Silva's introduction
- Shanghai skyscraper fight
- Tube train fight
- Scottish manor finale

**Mood:** Defiance, loyalty, the spy game, power dynamics, Bond's return

**Build:**

```bash
python build_montage.py \
    projects/skyfall/source/scenes_compilation.mp4 \
    --hook-movie projects/skyfall/source/hook_ms_apartment.mp4 \
    --hook 68-72 --hook-dur 4 \
    --bpm 80 \
    --scenes \
        30-33 60-63 90-93 120-123 150-153 180-183 \
        210-213 240-243 270-273 300-303 330-333 360-363 \
    --song sounds/sb_snowfall.mp3 \
    --max-dur 30 --scene-dur 1.5 \
    --output projects/skyfall/output/skyfall_loyalty_montage.mp4
```

## Notes

- The "I need you back" / "I never left" exchange is the ideal two-party hook: three words each, no exposition, instant power dynamics
- M is stern, Bond is defiant — you know their relationship instantly
- sb_snowfall provides cinematic, brooding pacing appropriate for spy thriller aesthetics
- This montage works best with a mix of explosive action shots and quieter character moments
- Penumbra (70 BPM) could be used as an alternative for slower, more introspective pacing
