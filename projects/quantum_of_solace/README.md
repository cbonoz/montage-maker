# Quantum of Solace — Montages

A collection of montages from the James Bond film Quantum of Solace, focusing on moody, dramatic moments rather than action.

## Montages

### 1. qos_loyalty — "I need you back"

**Status:** ✅ Built

**Hook (two-party):**
> **M:** "I need you back."
> **Bond:** "I never left."

**Music:** Penumbra @ 70 BPM (dark, longing, glacial)
**Alt Music:** sb_snowfall @ 80 BPM

**Outputs:**
- `output/qos_loyalty_montage_Penumbra.mp4` (recommended — dark/moody)
- `output/qos_loyalty_montage_sb_snowfall.mp4` (cinematic/wintery)

**Source clips used:**
- `hook_i_never_left.mkv` — "Quantum of Solace - 'I never left.' (1080p)" from YouTube
- `scenes_compilation.webm` — QUANTUM OF SOLACE CLIP COMPILATION #2 (347s) — general scenes compilation

**Hook timing (found via find_dialogue.py):**
```
"I need you back" → 64.2-69.7s
"I never left"    → 66.3-69.7s
Combined hook     → 64-70s (6s)
```

**Build:**

```bash
# Step 1: Download the hook clip
yt-dlp -f "bestvideo[height<=720]+bestaudio/best[height<=720]" \
    -o "projects/quantum_of_solace/source/hook_i_never_left.%(ext)s" \
    "https://www.youtube.com/watch?v=WFwmDq-MKaE"

# Step 2: Download the scenes compilation
yt-dlp -f "bestvideo[height<=720]+bestaudio/best[height<=720]" \
    -o "projects/quantum_of_solace/source/scenes_compilation.%(ext)s" \
    "https://www.youtube.com/watch?v=c_7A_mw2eCE"

# Step 3: Find hook timestamps
uv run find_dialogue.py \
    "https://www.youtube.com/watch?v=WFwmDq-MKaE" \
    "I need you back" --output hook

# Step 4: Build montage (dark/moody version)
python build_montage.py \
    projects/quantum_of_solace/source/scenes_compilation.webm \
    --hook-movie projects/quantum_of_solace/source/hook_i_never_left.mkv \
    --hook 64-70 --hook-dur 6 \
    --bpm 70 \
    --scenes \
        10-13 40-43 70-73 100-103 130-133 160-163 \
        190-193 220-223 250-253 280-283 310-313 340-343 \
    --song sounds/Penumbra.mp3 \
    --max-dur 30 --scene-dur 1.5 \
    --output projects/quantum_of_solace/output/qos_loyalty_montage_Penumbra.mp4
```

## Vibe

Moody, dramatic, dark — not an action montage. Penumbra's glacial piano creates space for the dialogue to breathe. The scenes compilation was chosen for general scene variety rather than action-only highlights.

## Notes

- The hook clip was originally in projects/skyfall/ (misidentified). Now lives here.
- Two music versions available: Penumbra (dark, recommended) and sb_snowfall (cinematic)
