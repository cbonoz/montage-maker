# Quantum of Solace — Montages

A collection of montages from the James Bond film Quantum of Solace, focusing on moody, dramatic moments rather than action.

## Montages

### 1. qos_loyalty — "I need you back"

**Status:** ✅ Built

**Hook (two-party):**
> **M:** "I need you back."
> **Bond:** "I never left."

**Music:** The Long Dark @ 75 BPM (ambient neoclassical piano — Scott Buckley)

**Output:** `output/qos_loyalty_montage_TheLongDark.mp4`

**Source clips used:**
- `hook_i_never_left.mkv` — "Quantum of Solace - 'I never left.' (1080p)" from YouTube (hook at 64-68s)
- `scenes_betrayed.mp4` — "Betrayed Within - Quantum of Solace" (363s) — introspective, dark character scenes

**Build:**

```bash
# Download music
yt-dlp -x --audio-format mp3 -o "sounds/TheLongDark.%(ext)s" \
    "https://www.youtube.com/watch?v=8i_6R2zr9H8"

# Build montage
python build_montage.py \
    projects/quantum_of_solace/source/scenes_betrayed.mp4 \
    --hook-movie projects/quantum_of_solace/source/hook_i_never_left.mkv \
    --hook 64-68 \
    --bpm 75 \
    --scenes \
        5-7 30-33 55-58 80-83 105-108 130-133 \
        155-158 180-183 205-208 230-233 255-258 280-283 \
    --song sounds/TheLongDark.mp3 \
    --max-dur 30 --scene-dur 1.5 \
    --transition crossfade \
    --output projects/quantum_of_solace/output/qos_loyalty_montage_TheLongDark.mp4

# (No --hook-dur needed — automatically uses full range)
```

## Vibe

Introspective, dark, intimate — no action. The Long Dark's ambient neoclassical piano with strings and atmospheric synth creates a cold, suspended feel for Bond's isolation. Crossfade transitions between character-driven scenes.
