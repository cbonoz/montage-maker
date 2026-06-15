# Skyfall — Montages

A collection of montages from the James Bond film Skyfall, exploring themes of loyalty, defiance, and the spy game.

## Montages

### 1. skyfall_loyalty — "I need you back"

**Status:** 📝 Planned

**Hook (two-party):**
> **M:** "I need you back."
> **Bond:** "I never left."

**Alternative hook (power dynamic exchange):**
> **M:** "If you fail, it's my head."
> **Bond:** "If I fail, you'll be dead before I am."

**Music:** sb_snowfall @ 80 BPM
**Alt Music:** Penumbra

**Source clips needed:**
- `hook_loyalty.mp4` — M summoning Bond after the botched mission
- `scenes_compilation.mp4` — Skyfall best scenes compilation

**Scenes to sample:**
- The opening chase in Istanbul (high-octane, Bond in action)
- Bond falling from the bridge (vulnerability)
- The title sequence (stylized, iconic)
- Silva's introduction (menace and mystery)
- The island lair (exotic scale)
- Shanghai skyscraper fight (neon-lit, vertical action)
- The tube train fight (intimate conflict)
- The Scottish manor finale (personal stakes)

**Mood:** Defiance, loyalty, the spy game, power dynamics, Bond's return

**Build Command (when ready):**

```bash
# Build skyfall_loyalty montage
python build_montage.py projects/skyfall sounds/sb_snowfall.mp3 --bpm 80
```

## Notes

- The "I need you back" / "I never left" exchange is the ideal two-party hook: three words each, no exposition, instant power dynamics
- M is stern, Bond is defiant — you know their relationship instantly
- sb_snowfall provides cinematic, brooding pacing appropriate for spy thriller aesthetics
- This montage works best with a mix of explosive action shots and quieter character moments
- Penumbra (70 BPM) could be used as an alternative for slower, more introspective pacing
