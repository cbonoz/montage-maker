# Montage Maker

Build short TikTok-style video montages from movie clips. Opening hook → music drop → rapid scene cuts (15-30s).

Reproducible CLI — always caps total duration under your target (default 25s).

## Quick Start

```bash
python build_montage.py movie.mp4 \
    --hook 1:30-1:38 \
    --scenes 5:10-5:14 12:20-12:24 25:00-25:04 \
    --song sounds/sb_snowfall.mp3 \
    --output montage.mp4
```

The script automatically:
- Cuts the hook to ~3s max
- Picks the right number of scenes to fit under 25s total
- Trims each scene clip to exact duration (re-encode, not keyframe-gated)
- Mixes dialogue (full volume) + background music (low under hook, fades up after)
- Rebuilds if result exceeds max duration

## CLI Options

| Flag | Default | Description |
|------|---------|-------------|
| `movie` | required | Path to source movie file |
| `--hook` | required | Hook range: `mm:ss-mm:ss` |
| `--scenes` | required | Scene ranges: `mm:ss-mm:ss ...` (space-separated) |
| `--song` | — | Background music path (try `sounds/sb_snowfall.mp3`) |
| `--output` | `montage.mp4` | Output file path |
| `--max-dur` | `25.0` | Target max duration in seconds |
| `--scene-dur` | `2.0` | Per-scene duration in seconds |
| `--hook-dur` | `3.0` | Max hook duration in seconds |
| `--keep` | — | Keep temp working files |

## Examples

**Harry Potter style — 13s with ambient piano:**
```bash
python build_montage.py source/diagon.webm \
    --hook 0-2.6 \
    --scenes 30-33 70-73 140-143 20-23 75-78 \
    --song sounds/sb_snowfall.mp3 \
    --max-dur 20 \
    --output output/hp_montage.mp4
```

**Tighter edit — 15s max, 1.5s per scene:**
```bash
python build_montage.py movie.mp4 \
    --hook 1:30-1:35 \
    --scenes 5:10-5:13 12:20-12:23 \
    --max-dur 15 --scene-dur 1.5 \
    --output tight.mp4
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

All tracks: `Scott Buckley — scottbuckley.com.au` (CC BY 4.0) — add credit in video description.

## Project Convention

```
montage-maker/
├── build_montage.py       # reproducible CLI
├── sounds/                # shared ambient sound library
├── README.md
└── projects/
    ├── hp-montage/        # demo
    │   ├── source/        # raw clips
    │   ├── output/        # generated videos
    │   └── notes.md
    └── <next-project>/
```

## Requirements

- `ffmpeg` (Homebrew)
- `yt-dlp` (optional — for downloading YouTube clips)
- Python 3 (stdlib only)

## Getting movie clips

- **Screen record** from streaming service (QuickTime → File → New Screen Recording)
- **YouTube clip downloads** via `yt-dlp`
- **Digital copy** from iTunes/Amazon

## To do

- [x] Reproducible CLI with duration enforcement
- [x] GitHub-connected
- [ ] Beat-synced cuts from music BPM (librosa)
- [ ] Vertical 9:16 crop for TikTok
- [ ] Hermes skill for one-command "make a montage with [clip]"
- [ ] Smooth audio transitions between scenes
- [ ] Auto-find scenes from movie by searching transcript/dialogue
