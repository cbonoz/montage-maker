# The Dark Knight — Montage Projects

This project uses clean official Movieclips footage (no watermarks, no edits) downloaded from the Rotten Tomatoes Movieclips YouTube channel.

## Source Clips

All sourced from official YouTube channel uploads. **Movieclips uploads from 2023+ ("4K" labeled) have the RT watermark — BLACKLISTED.** Prefer older uploads (2008-2015) from the original Movieclips channel, which were uploaded before the Rotten Tomatoes rebranding.

| Clip | Source URL | Version | Clean? | Key scenes |
|------|-----------|---------|--------|-----------|
| `mc_pencil_trick.mp4` | https://www.youtube.com/watch?v=2RXZj-OUAtI | 4K (2025) | ❌ RT watermark | Joker's pencil trick, mob meeting |
| `mc_why_so_serious.mp4` | https://www.youtube.com/watch?v=zeUsI-duhgc | 4K (2025) | ❌ RT watermark | Joker threatens Gambol |
| `mc_interrogation.mp4` | https://www.youtube.com/watch?v=zJP03SgePDA | 4K (2025) | ❌ RT watermark | Batman interrogates Joker |
| `mc_car_chase.mp4` | https://www.youtube.com/watch?v=cFdDCTumLks | 4K (2025) | ❌ RT watermark | Joker car chase, truck flip |
| `mc_two_face.mp4` | https://www.youtube.com/watch?v=vmG4azhi90M | HD clip | ❌ RT watermark | Two-Face kills Maroni |
| `mc_batman_vs_joker.mp4` | https://www.youtube.com/watch?v=54oDA3ufmj8 | 4K (2025) | ❌ RT watermark | Final showdown |
| `hook_ending_scene.mp4` | https://www.youtube.com/watch?v=yuOLDMjCrRI | HD (2016) | ✅ Likely clean | Full ending scene (Gordon + Batman) |
| `mc_interrogation_clean.mp4` | https://www.youtube.com/watch?v=dBqdU7mat84 | HD (2009) | ✅ Clean (pre-RT) | Batman interrogates Joker |
| `mc_pencil_clean.mp4` | https://www.youtube.com/watch?v=votcOf5cYCM | HD (TopMovieClips) | ✅ Clean | Joker pencil trick |

## Audio Lessons Learned

- **Music should not start at the same time as dialogue.** Dialogue needs 0.5s to establish itself before music comes in.
- **Scene ambient noise is baked into hook audio.** The interrogation has echoes, chains, room tone. This is unavoidable for non-studio clips.
- **Song choice matters for mood fit.** sb_snowfall (hopeful, wintery) clashed with gritty interrogation scenes. Penumbra (dark, glacial) might work better if the music volume is high enough — 40% during hook, not 15%.

**Legacy clips (watermarked, not used in final builds):**
| `hook_die_a_hero.mp4` | https://www.youtube.com/watch?v=dAmimbL8l38 | 6s | Low quality audio |
| `scenes_compilation.mp4` | https://www.youtube.com/watch?v=K5rsrd3P0dg | 15min | Fan-made, watermarked |

## Montages Built

### v5 — Joker Interrogation Hook (latest)
**Build date:** June 14, 2026

```bash
python build_montage.py \
    projects/dark-knight/source/mc_pencil_trick.mp4 \
    projects/dark-knight/source/mc_why_so_serious.mp4 \
    projects/dark-knight/source/mc_interrogation.mp4 \
    projects/dark-knight/source/mc_car_chase.mp4 \
    projects/dark-knight/source/mc_two_face.mp4 \
    projects/dark-knight/source/mc_batman_vs_joker.mp4 \
    --hook-movie projects/dark-knight/source/mc_interrogation.mp4 \
    --hook 6-11 \
    --bpm 80 \
    --scenes \
        5-8 10-13 15-18 20-23 25-28 30-33 35-38 40-43 45-48 50-53 55-58 60-63 \
    --song sounds/sb_snowfall.mp3 \
    --max-dur 30 --scene-dur 2.0 \
    --output projects/dark-knight/output/dark_knight_montage.mp4
```

**Hook (two-party):**
- Batman: "Why do you wanna kill me?"
- Joker: "I don't wanna kill you! What would I do without you? You complete me."

**Song:** sb_snowfall.mp3 at 80 BPM

### v4 — Clean Movieclips, "die a hero" hook
Same as v5 but hook from `hook_ending_scene.mp4` at 196-203s.

### v3 — Fixed audio curve (music at 40% during hook)
Music comes in sooner, reaches full earlier.

### v1-v2 — Watermarked source (deprecated)
Used scenes_compilation.mp4 (fan-made, watermarked). Not recommended.

## Re-download All Clips

```bash
cd source
yt-dlp -f "136+140" -o "mc_pencil_trick.mp4" "https://www.youtube.com/watch?v=2RXZj-OUAtI"
yt-dlp -f "136+140" -o "mc_why_so_serious.mp4" "https://www.youtube.com/watch?v=zeUsI-duhgc"
yt-dlp -f "136+140" -o "mc_interrogation.mp4" "https://www.youtube.com/watch?v=zJP03SgePDA"
yt-dlp -f "136+140" -o "mc_car_chase.mp4" "https://www.youtube.com/watch?v=cFdDCTumLks"
yt-dlp -f "136+140" -o "mc_two_face.mp4" "https://www.youtube.com/watch?v=vmG4azhi90M"
yt-dlp -f "136+140" -o "mc_batman_vs_joker.mp4" "https://www.youtube.com/watch?v=54oDA3ufmj8"
yt-dlp -f "136+140" -o "hook_ending_scene.mp4" "https://www.youtube.com/watch?v=yuOLDMjCrRI"
```
