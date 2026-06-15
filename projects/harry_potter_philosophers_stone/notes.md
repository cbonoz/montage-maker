# Harry Potter Montage Project

Place source clips in `source/`.
Generated videos go in `output/`.

## Source clips

- `hook.mkv` — "Yer a wizard, Harry" clip (2.6s) — 1280×720 H.264 + opus audio
  - *(screen recorded, no URL)*
- `diagon.webm` — Diagon Alley scenes — 1280×720 AV1
  - *(screen recorded, no URL)*
- `sorting.webm` — Sorting Hat scenes — 1280×590 AV1 (auto-padded to 720)
  - *(screen recorded, no URL)*

## Build (final — beat-synced, dual source)

From montage-maker root:

```bash
python build_montage.py \
    projects/hp-montage/source/diagon.webm \
    projects/hp-montage/source/sorting.webm \
    --hook-movie projects/hp-montage/source/hook.mkv \
    --hook 0-2.6 \
    --bpm 80 \
    --scenes \
        30-33 60-63 90-93 120-123 150-153 180-183 \
        10-13 40-43 70-73 100-103 130-133 160-163 \
    --song sounds/sb_snowfall.mp3 \
    --max-dur 30 --scene-dur 2.25 \
    --output projects/hp-montage/output/hp_montage.mp4
```

## Structure

- 0.5s black lead-in
- 2.25s hook ("Yer a wizard, Harry") — dialogue audible, music low
- 12 muted scene cuts (2.25s each = 3 beats @ 80 BPM)
  - Alternates between diagon.webm and sorting.webm
- 3s music fade-out at end

Total: ~29.9s

## Audio

| Time | Audio |
|------|-------|
| 0.0–0.5s | Silence |
| 0.5–2.75s | Hook dialogue full + music at 15% |
| 2.75–27s | Music full over 12 muted scenes |
| 27–30s | Music fades out |

## Alternate songs

Replace `--song sounds/sb_snowfall.mp3` with:
- `sounds/FirstSnow.mp3` — Gentle, calm
- `sounds/Moonlight.mp3` — Simple, nostalgic
- `sounds/Meanwhile.mp3` — Dreamy, ethereal
- `sounds/Penumbra.mp3` — Tender, glacial
- `sounds/Unraveling.mp3` — Introspective, bittersweet

Adjust `--bpm` accordingly if using a different song.
