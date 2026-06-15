# Montage Maker

Build short TikTok-style video montages from movie clips. Opening hook → music drop → rapid scene cuts (15-30s).

## Status

**Working prototype** — hp-montage demo built (13s). Core pipeline works:
- Extract hook clip + scene clips from source
- Concat in sequence
- Mix dialogue + ambient background track with volume fade
- Export as MP4

**Limitations / next iteration needed:**
- `build_montage.py` CLI script needs rework to handle the full flow (currently the demo was built with a one-off bash script)
- No beat-synced cuts yet — clips are sequential, not timed to music
- No vertical/crop to 9:16 for TikTok
- Hook audio mix could use smoother crossfade
- Need a Hermes skill for one-command generation

## How it works

1. **Hook** — 2-3s opening clip (iconic line from a movie)
2. **Music** — introspective ambient track from `sounds/` plays low under hook, rises after
3. **Montage** — 3-6 scene clips (2s each) cut together, total 15-25s

## Usage (bash, for now)

Each project lives in its own folder:
```
projects/your-project/
├── source/    # hook + scene clips
├── output/    # generated montages
└── notes.md
```

Build script approach (from project root):
```bash
# 1. Put hook clip and scene clips in source/
# 2. Run a build script that:
#    - Takes hook as first clip
#    - Extracts 2s subclips from scene files
#    - Mixes with background audio from sounds/
#    - Exports to output/
```

## Sound Library

Introspective ambient tracks in `sounds/` — all CC BY 4.0 by Scott Buckley (credit required):

| File | BPM | Vibe | Duration |
|------|-----|------|----------|
| `sb_snowfall.mp3` | 80 | Cinematic piano, wintery | 4:08 |
| `FirstSnow.mp3` | — | Gentle, calm, piano + strings | 3:32 |
| `Penumbra.mp3` | — | Tender, glacial, longing | 7:00 |
| `Unraveling.mp3` | — | Introspective, bittersweet | 6:55 |
| `Meanwhile.mp3` | — | Dreamy, ethereal piano | 5:14 |
| `Moonlight.mp3` | — | Simple, nostalgic piano + strings | 4:05 |

All tracks credit: `Scott Buckley — scottbuckley.com.au` (CC BY 4.0)

Add more by dropping mp3s into `sounds/`.

## Project Folder Convention

```
montage-maker/
├── build_montage.py      # (needs rework)
├── sounds/               # shared ambient sound library
├── README.md
└── projects/
    ├── hp-montage/       # demo: Harry Potter
    │   ├── source/       # raw clips
    │   ├── output/       # hp_montage.mp4 (13s)
    │   └── notes.md
    └── <next-project>/
```

## Getting movie clips

- **Screen record** from streaming service (QuickTime → File → New Screen Recording)
- **YouTube clip downloads** via `yt-dlp`
- **Digital copy** purchased from iTunes/Amazon

## Requirements

- `ffmpeg` (Homebrew)
- `yt-dlp` (for YouTube clip downloads)
- Python 3

## To do

- [ ] Beat-synced cuts from music BPM (librosa beat detection)
- [ ] `build_montage.py` — full pipeline from one CLI command
- [ ] Vertical 9:16 crop for TikTok
- [ ] Hermes skill for "make a montage with [clip] about [topic]"
- [ ] Smooth audio transitions between hook and montage (fade-in/fade-out per clip)
- [ ] Configurable total duration (target 15-30s)
- [ ] Multiple scene clips from one movie file (extract by timestamp)
