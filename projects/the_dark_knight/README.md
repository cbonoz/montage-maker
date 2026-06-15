# The Dark Knight Trilogy — Montages

A collection of montages from Christopher Nolan's The Dark Knight trilogy, featuring themes of duality, tragedy, and moral decay.

## Montages

### 1. dk_hero_villain — "You either die a hero…"

**Status:** ✅ Built

**Hook (two-party):**
> **Batman:** *grab* "Why do you wanna kill me?"
> **Joker:** *laughs* "I don't wanna kill you! What would I do without you?… You… you complete me."

**Alternative hook (monologue):**
> "You either die a hero, or you live long enough to see yourself become the villain."

**Music:** Penumbra @ 70 BPM
**Alt Music:** Unraveling

**Output:** `output/dark_knight_montage.mp4`

**Source clips used:**
- `hook_die_a_hero.mp4` — Batman delivering the final line
- `scenes_compilation.mp4` — Top 10 Moments compilation (all 3 movies)

**Scenes sampled (timestamps from scenes_compilation.mp4):**
- 36-39s: Batman's first appearance (docks)
- 42-45s: Training with Ra's al Ghul
- 50-53s: Batman Begins flight
- 107-110s: Joker interrogation ("Why so serious?")
- 132-135s: Joker truck flip
- 158-161s: Two-Face reveal at hospital
- 242-245s: Bane breaks the Bat

**Mood:** Tragic fall, duality, moral decay

---

### 2. dk_joker_interrogation — "Why do you wanna kill me?…"

**Status:** ✅ Built

**Hook (two-party):**
> **Batman:** "Why do you wanna kill me?"
> **Joker:** "I don't wanna kill you! What would I do without you?… You… you complete me."

**Music:** Penumbra @ 70 BPM

**Source clips used:**
- `scenes_compilation.mp4` — Batman/Joker interrogation scene and related moments

**Mood:** Conflict, obsession, psychological duality

---

### 3. dk_bane_strength — "Peace has cost you your strength"

**Status:** 📝 Planned

**Hook (two-party):**
> **Bane:** "Peace has cost you your strength. Victory has defeated you."
> **Batman:** "No. I came back to stop you."

**Music:** Penumbra @ 75 BPM

**Source clips needed:**
- `scenes_compilation.mp4` (timestamps 242-282s) — Bane breaking Batman scenes

**Note:** Reuses existing clips from the trilogy compilation already sourced for other montages.

**Mood:** Power loss, tragic vulnerability, class conflict

---

## Build Commands

To rebuild the existing montages:

```bash
# Rebuild dk_hero_villain montage
python build_montage.py projects/the_dark_knight sounds/Penumbra.mp3 --bpm 70

# Build dk_bane_strength (when clips are ready)
python build_montage.py projects/the_dark_knight sounds/Penumbra.mp3 --bpm 75
```

## Notes

- All three montages use the `scenes_compilation.mp4` as the primary visual source
- The compilation is from: https://www.youtube.com/watch?v=K5rsrd3P0dg (Top 10 Moments, all 3 movies)
- Bane montage is planned but not yet built; it reuses scenes already downloaded for dk_hero_villain
