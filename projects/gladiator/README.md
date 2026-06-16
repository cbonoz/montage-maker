# Gladiator — Montages

A collection of montages from Ridley Scott's epic drama about vengeance, honor, and the Roman Colosseum.

## Montages

### 1. gladiator_vengeance — "I will have my vengeance…" (Long Hook)

**Status:** ✅ Built

**Hook (monologue):**
> "My name is Maximus Decimus Meridius, commander of the Armies of the North, General of the Felix Legions, loyal servant to the true emperor, Marcus Aurelius. Father to a murdered son, husband to a murdered wife. And I will have my vengeance, in this life or the next."

**Music:** Moonlight @ 75 BPM

**Output:** `output/gladiator_montage.mp4`

**Source clips used:**
- `hook_maximus_reveal.mp4` — Maximus removes his helmet in the Colosseum (full speech)
- `scenes_compilation.mp4` — Gladiator best scenes compilation

**Hook timing:** 91-111s in `hook_maximus_reveal.mp4`

**Build Command:**

```bash
python build_montage.py \
    projects/gladiator/source/scenes_compilation.mp4 \
    --hook-movie projects/gladiator/source/hook_maximus_reveal.mp4 \
    --hook 91-111 --hook-dur 8 \
    --bpm 75 \
    --scenes 32-36 40-44 52-56 72-76 \
            120-124 130-134 140-144 160-164 \
            180-184 200-204 230-234 260-264 \
    --song sounds/Moonlight.mp3 \
    --max-dur 30 --scene-dur 1.5 \
    --output projects/gladiator/output/gladiator_montage.mp4
```

---

### 2. gladiator_vengeance_short — "I will have my vengeance…" (Short Hook)

**Status:** ✅ Built

**Hook:**
> "I will have my vengeance, in this life or the next."

**Music:** Moonlight @ 75 BPM

**Output:** `output/gladiator_vengeance_montage.mp4`

**Source clips used:**
- `scenes_compilation.mp4` — Gladiator best scenes compilation (hook + scenes from same file)

**Hook timing:** 303-307s in `scenes_compilation.mp4` (found via youtube-transcript-api)

**Built using:**

```bash
# Find the hook timing from the scenes compilation transcript
uv run find_dialogue.py \
    "https://www.youtube.com/watch?v=OgU1QOkFFT0" \
    "will have my" \
    --output hook
# → 300.0-307.3 (contains "wife, and I will have my vengeance in this life or the next")
# Start at 300.5 to drop "wife, and" preamble but keep "I will have my"

# Build
python build_montage.py \
    projects/gladiator/source/scenes_compilation.mp4 \
    --hook 300.5-306.5 --hook-dur 6 \
    --bpm 75 \
    --scenes 32-36 40-44 52-56 72-76 \
            120-124 130-134 140-144 160-164 \
            180-184 200-204 230-234 260-264 \
    --song sounds/Moonlight.mp3 \
    --max-dur 30 --scene-dur 1.5 \
    --output projects/gladiator/output/gladiator_vengeance_montage.mp4
```

---

### 3. gladiator_entertained — "Are you not entertained?"

**Status:** ✅ Built

**Hook:** "Are you not entertained?"

**Music:** Legacy @ 100 BPM (bold brass, soaring strings, heroic)

**Output:** `output/gladiator_entertained_montage_Legacy.mp4`

**Source clips used:**
- `mc_are_you_entertained.mp4` — "Are you not entertained?" scene (135s, 720p)
- `scenes_compilation.mp4` — Gladiator best scenes compilation (860s)
- `mc_germania.mp4` — Germania battle scenes (191s)

**Hook timing:** 90-96s in `mc_are_you_entertained.mp4` (found via Whisper)

**Build:**

```bash
python build_montage.py \
    projects/gladiator/source/scenes_compilation.mp4 \
    projects/gladiator/source/mc_germania.mp4 \
    --hook-movie projects/gladiator/source/mc_are_you_entertained.mp4 \
    --hook 90-96 --hook-dur 6 \
    --bpm 100 \
    --scenes \
        10-13 30-33 50-53 70-73 90-93 110-113 \
        130-133 150-153 170-173 190-193 210-213 30-33 \
        250-253 50-53 \
    --song sounds/Legacy.mp3 \
    --max-dur 35 --scene-dur 1.8 \
    --transition crossfade \
    --output projects/gladiator/output/gladiator_entertained_montage_Legacy.mp4
```

## Notes

- Both montages use the same scene clips with the same beat-sync (75 BPM, 3 beats per scene)
- The long hook version gives the full speech arc (helmet reveal + monologue)
- The short hook version punches straight to "vengeance" — tighter, more aggressive
- The scenes compilation (Binge Society, `OgU1QOkFFT0`) has auto-captions that `find_dialogue.py` used to find the exact "vengeance" timing
- The dedicated Movieclips hook clip (`lEM5nJ-AUiM`) has no captions, so the scenes compilation was used as the hook source instead
