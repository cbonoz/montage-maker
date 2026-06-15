# Montage Maker

Build short TikTok-style video montages from a movie file. Opening hook dialogue → beat drop → rapid scene cuts synced to music.

## How it works

1. Pick an opening scene from a movie (the hook — an iconic line or moment)
2. Pick 3-6 more scenes from the same movie
3. Optionally add a background song
4. The script extracts all clips, splices them together, and mixes the audio

The hook plays at full volume. If a song is provided, it plays quietly underneath the hook, then rises to full volume once the hook ends.

## Usage

```bash
python build_montage.py /path/to/movie.mp4 \
    --hook 1:30-1:38 \
    --scenes 5:10-5:14 12:20-12:24 25:00-25:04 \
    --song background.mp3 \
    --output montage.mp4
```

Timestamps use `mm:ss` format. Scene clips play in sequence order after the hook.

## Getting movie clips

The script needs a local movie file. Options:

- **Screen record** from a streaming service you subscribe to (QuickTime → File → New Screen Recording, scrub directly to each scene)
- **Digital copy** purchased from iTunes/Amazon (some have DRM-free downloads)
- The movie doesn't need to be the full file — you can record just the scenes you want and concatenate them manually, then point the script at the combined file with just `--hook` and leave `--scenes` empty

## Requirements

- `ffmpeg` (installed via Homebrew)
- Python 3 (standard lib only — no pip deps needed)

## Coming next

- Beat-synced cuts (auto-detect beat from the song and trim scenes to match)
- Vertical/crop to 9:16 for TikTok
- Generate a background track programmatically (MusicGen / Audiocraft)
- Save as a reusable Hermes skill
