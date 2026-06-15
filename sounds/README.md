# Sound Library — Ambient Tracks

Download required tracks manually. All are CC BY 4.0 by Scott Buckley (scottbuckley.com.au).

## Tracks

| File | Track Name | Source URL | Size |
|------|-----------|------------|------|
| `sb_snowfall.mp3` | Snowfall | https://www.scottbuckley.com.au/library/snowfall/ | 9.5 MB |
| `FirstSnow.mp3` | First Snow | https://www.scottbuckley.com.au/library/first-snow/ | 8.1 MB |
| `Penumbra.mp3` | Penumbra | https://www.scottbuckley.com.au/library/penumbra/ | 17 MB |
| `Unraveling.mp3` | Unraveling | https://www.scottbuckley.com.au/library/unraveling/ | 17 MB |
| `Meanwhile.mp3` | Meanwhile | https://www.scottbuckley.com.au/library/meanwhile/ | 12 MB |
| `Moonlight.mp3` | Moonlight | https://www.scottbuckley.com.au/library/moonlight/ | 9.7 MB |

## Download all

```bash
cd sounds
for url in \
  "https://www.scottbuckley.com.au/library/wp-content/uploads/2018/12/sb_snowfall.mp3" \
  "https://www.scottbuckley.com.au/library/wp-content/uploads/2022/12/FirstSnow.mp3" \
  "https://www.scottbuckley.com.au/library/wp-content/uploads/2025/07/Penumbra.mp3" \
  "https://www.scottbuckley.com.au/library/wp-content/uploads/2026/05/Unraveling.mp3" \
  "https://www.scottbuckley.com.au/library/wp-content/uploads/2025/01/Meanwhile.mp3" \
  "https://www.scottbuckley.com.au/library/wp-content/uploads/2022/07/Moonlight.mp3"; do
  curl -sL -o "$(basename "$url")" "$url"
done
```

## Credit

All tracks by Scott Buckley — https://scottbuckley.com.au — CC BY 4.0
