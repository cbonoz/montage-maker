# Harry Potter Montage Project

Place source clips (hook.mp4, scene clips) in `source/`.
Generated videos go in `output/`.

## Source clips needed

- `hook.mkv` — "Yer a wizard, Harry" clip (2.6s)
- Scene clips from Harry Potter and the Philosopher's Stone

## Build

```bash
python ../../build_montage.py source/diagon.webm \
    --hook 0-2.6 \
    --scenes 30-33 70-73 140-143 20-23 75-78 \
    --song ../../sounds/sb_snowfall.mp3 \
    --max-dur 20 \
    --output output/hp_montage.mp4
```
