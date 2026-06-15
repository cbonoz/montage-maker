# Harry Potter and the Philosopher's Stone — Montages

A collection of montages capturing the wonder and discovery of Harry's introduction to the wizarding world.

## Montages

### 1. hp_yer_a_wizard — "Yer a wizard, Harry"

**Status:** ✅ Built

**Hook (two-party):**
> **Hagrid:** "Harry — yer a wizard."
> **Harry:** "I'm a what?"
> **Hagrid:** "A wizard, an' a thumpin' good one, I'd wager, once yeh get trained up a bit."

**Music:** sb_snowfall @ 80 BPM
**Alt Music:** Meanwhile

**Output:** `output/hp_montage_30s_final.mp4` (29.9s)

**Source clips used:**
- `hook.mkv` — Hagrid's dialogue on the island (2.6s)
- `diagon.webm` — Diagon Alley scenes (3:42)
- `sorting.webm` — Sorting Hat ceremony scenes (4:56)

**Scenes sampled:**
- Diagon Alley: shops, Gringotts, wand selection, bustling crowds
- Great Hall: Sorting ceremony for all houses
- Quidditch intro: golden snitch, broom flying

**Mood:** Magical awakening, wonder, discovery, awe

---

### 2. hp_hermione_arrival — "You are a wizard, Harry"

**Status:** 🔁 Reusable

**Hook (two-party):**
> "You are a wizard, Harry!"
> *Ron eating his sandwich* — "You've got dirt on your nose, by the way."
> **Hermione:** "Are you sure that's a real spell? Well, it's not very good, is it?"

**Alternative hook (train carriage):**
> "I've noticed some very strange behavior lately... Has anyone else noticed?"

**Music:** Moonlight @ 80 BPM
**Alt Music:** Meanwhile

**Source clips reused from hp_yer_a_wizard:**
- `diagon.webm` — Hogwarts Express, Diagon Alley scenes
- `sorting.webm` — Sorting ceremony, first flying lesson, troll in the dungeons

**Scenes to sample:**
- Hogwarts Express compartment scenes
- Sorting ceremony (focusing on different houses)
- First flying lesson (Madam Hooch)
- Troll in the dungeons
- Quidditch intro with the golden snitch
- Mirror of Erised scene

**Mood:** Friendships forming, wonder, trio's first adventure, magical mishaps

---

## Build Commands

To rebuild the existing montage:

```bash
# Rebuild hp_yer_a_wizard
python build_montage.py projects/harry_potter_philosophers_stone sounds/sb_snowfall.mp3 --bpm 80

# Build hp_hermione_arrival (uses same clips; extract different sections)
python build_montage.py projects/harry_potter_philosophers_stone sounds/Moonlight.mp3 --bpm 80
```

## Notes

- Both montages source from the same set of clips (diagon.webm and sorting.webm)
- hp_hermione_arrival is marked as 🔁 Reusable because it leverages already-downloaded scenes
- For hp_hermione_arrival, trim different sections from the source files to create distinct visual flow
- Both use cinematic piano tracks at 80 BPM for consistent pacing
