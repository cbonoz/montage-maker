# Quantum of Solace — Montages

A collection of montages from the James Bond film Quantum of Solace.

## Montages

### 1. qos_loyalty — "I need you back"

**Status:** ✅ Built

**Hook (two-party):**
> **M:** "I need you back."
> **Bond:** "I never left."

**Music:** sb_snowfall @ 80 BPM

**Output:** `output/qos_loyalty_montage_sb_snowfall.mp4`

**Source clips used:**
- `hook_ms_apartment.mp4` — M's apartment scene (sourced from YouTube)
- `scenes_compilation.webm` — "Bond Goes Rogue: Best of Quantum of Solace Action" (607s)

**Hook timing (found via find_dialogue.py):**
```
"I need you back" → 64.2-69.7s
"I never left"    → 66.3-69.7s
Combined hook     → 64-70s
```

**Build:**

```bash
# Find hook timestamps
uv run find_dialogue.py \
    "https://www.youtube.com/watch?v=WFwmDq-MKaE" \
    "I need you back" --output hook

# Build montage
python build_montage.py \
    projects/quantum_of_solace/source/scenes_compilation.webm \
    --hook-movie projects/quantum_of_solace/source/hook_ms_apartment.mp4 \
    --hook 64-70 --hook-dur 6 \
    --bpm 80 \
    --scenes \
        30-33 70-73 110-113 150-153 190-193 230-233 \
        270-273 310-313 350-353 390-393 430-433 470-473 \
    --song sounds/sb_snowfall.mp3 \
    --max-dur 30 --scene-dur 1.5 \
    --output projects/quantum_of_solace/output/qos_loyalty_montage_sb_snowfall.mp4
```

## Notes

- The hook clip was originally in projects/skyfall/ (misidentified). Now lives here.
- Scene compilation from "Bond Goes Rogue: Best of Quantum of Solace Action" — great visual variety
