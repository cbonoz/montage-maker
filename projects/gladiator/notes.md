# Gladiator — "My name is Maximus Decimus Meridius"

Montage of Maximus's arc — from general to gladiator to avenger.

## Build

```bash
python build_montage.py \
    projects/gladiator/source/scenes_compilation.mp4 \
    --hook-movie projects/gladiator/source/hook_maximus_reveal.mp4 \
    --hook 91-111 --hook-dur 8 \
    --bpm 75 \
    --scenes \
        32-36 40-44 52-56 72-76 \
        120-124 130-134 140-144 160-164 \
        180-184 200-204 230-234 260-264 \
    --song sounds/Penumbra.mp3 \
    --max-dur 30 --scene-dur 1.5 \
    --output projects/gladiator/output/gladiator_montage.mp4
```

## Source Clips

| Clip | Source URL | Duration |
|------|-----------|----------|
| `hook_maximus_reveal.mp4` | https://www.youtube.com/watch?v=lEM5nJ-AUiM | 2:52 (Movieclips, clean) |
| `scenes_compilation.mp4` | https://www.youtube.com/watch?v=OgU1QOkFFT0 | 14:20 (Binge Society) |

**Note:** Scenes compilation is from Binge Society — check for watermark. The hook clip is a classic Movieclips upload (clean).

## Structure

- 0.5s black
- 8s hook: Maximus helmet reveal + full speech (music low, dialogue dominant)
- ~19s: 12 muted scene cuts + Penumbra full
- 3s fade out
