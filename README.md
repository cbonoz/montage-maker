# Montage Maker

Build short video montages from movie clips. 0.5s black lead-in → hook (dialogue audible, music low) → beat-synced muted scene cuts with music full → 3s fade out. Typically 15–30s.

Reproducible CLI — always caps total duration, supports multiple source movies, and snaps scene durations to the music's beat for rhythmic edits.

## Quick Start

```bash
# Single movie source for both hook and scenes
python build_montage.py movie.mp4 \
    --hook 1:30-1:38 \
    --scenes 5:10-5:14 12:20-12:24 25:00-25:04 \
    --song sounds/sb_snowfall.mp3 --bpm 80 \
    --output montage.mp4

# Multiple movie sources interleaved for visual variety
python build_montage.py scene_movie1.mp4 scene_movie2.mp4 \
    --hook-movie hook_clip.mkv \
    --hook 0-2.6 \
    --scenes 30-33 60-63 90-93 120-123 150-153 180-183 \
    --song sounds/sb_snowfall.mp3 --bpm 80 \
    --max-dur 30 --scene-dur 2.25 \
    --output montage.mp4
```

The script automatically:
- Cuts the hook to ~3s max (≤30% of total duration)
- Picks the right number of scenes to fit under total duration
- Snaps scene durations to the nearest beat multiple based on BPM (rhythmic cuts)
- Scales/pads all clips to uniform 1280x720 (supports mixed-resolution source files)
- Mutes all scene audio (scenes play with background music only)
- Mixes hook dialogue (full volume) + background music (low under hook, fades up after)
- Opens with 0.5s black lead-in for cinematic feel
- Fades music out over 3s at the end (no abrupt climax cut-off)
- Interleaves scene sources for visual variety when multiple movies provided

## CLI Options

| Flag | Default | Description |
|------|---------|-------------|
| `movie` | required | One or more source movie files for scene clips (interleaved) |
| `--hook` | required | Hook range: `mm:ss-mm:ss` |
| `--hook-movie` | same as movie[0] | Separate file for the hook clip (e.g. a short dialogue clip) |
| `--scenes` | required | Scene ranges: `mm:ss-mm:ss ...` (space-separated) |
| `--song` | — | Background music path (try `sounds/sb_snowfall.mp3`) |
| `--bpm` | auto-detect | Beats per minute of the song (scene dur snaps to beat multiples) |
| `--transition` | `cut` | Scene transition: `cut` or `crossfade` |
| `--output` | `montage.mp4` | Output file path |
| `--max-dur` | `25.0` | Target max duration in seconds |
| `--scene-dur` | `2.0` | Per-scene duration in seconds (snapped to nearest beat) |
| `--hook-dur` | `3.0` | Max hook duration in seconds |
| `--keep` | — | Keep temp working files |

## Examples

**Harry Potter — 30s beat-synced, dual source movies:**
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

This builds a 30s montage with the "Yer a wizard, Harry" hook (from hook.mkv), then 12 scene cuts alternating between Diagon Alley and Sorting Hat footage, each 3 beats long at 80 BPM.

**Tighter edit — 15s, 2 beats per scene:**
```bash
python build_montage.py movie.mp4 \
    --hook 1:30-1:35 \
    --scenes 5:10-5:13 12:20-12:23 \
    --bpm 80 \
    --max-dur 15 --scene-dur 1.5 \
    --output tight.mp4
```

## Audio Structure

All montages follow the same audio envelope across the video timeline:

| Time | Video | Audio |
|------|-------|-------|
| 0.0–0.5s | Black screen | Silence |
| 0.5–3.1s | Hook clip | Dialogue at full volume + music at 15% volume underneath |
| 3.1s–end | Muted scene cuts | Music at 100% volume |
| Last 3s | Final scenes | Music fades out |

- Scene clips are **always extracted without audio** (`-an` flag)
- Music volume transitions are smooth: silence → fade in → low during hook → ramp up → full → fade out
- Fade-out is 3s to avoid cutting off at a music climax

## Beat-Synced Editing

When `--bpm` is provided (or auto-detected), scene durations snap to the nearest beat boundary:

```
scene_duration = round(requested_duration / beat_length) * beat_length
min = 2 beats, max = 8 beats
```

This ensures each scene cut lands on a musical downbeat rather than mid-beat. For 80 BPM (sb_snowfall.mp3), `beat_length = 60/80 = 0.75s`.

**Known BPMs in the sound library:**
- `sb_snowfall.mp3` — 80 BPM
- `FirstSnow.mp3`, `Penumbra.mp3`, `Unraveling.mp3`, `Meanwhile.mp3`, `Moonlight.mp3` — auto-detect or specify manually

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
- [x] Beat-synced cuts from music BPM
- [x] Multiple source movies (interleaved scenes)
- [x] Mixed-resolution source support (auto-pad to 1280x720)
- [x] GitHub-connected
- [ ] Vertical 9:16 crop for TikTok
- [ ] Hermes skill for one-command "make a montage with [clip]"
- [ ] Smooth crossfade transitions between scenes
- [ ] Auto-find scenes from movie by searching transcript/dialogue
- [ ] Energy progression (reorder scenes by intensity)
- [ ] Download sound tracks as part of first build
