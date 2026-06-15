# Sound Library — Ambient Tracks

Download required tracks manually. All are CC BY 4.0 by Scott Buckley (scottbuckley.com.au).

## Reflective / Chill / Introspective (these work for montages)

| File | Track Name | Source URL | Size | Vibe |
|------|-----------|------------|------|------|
| `sb_snowfall.mp3` | Snowfall | https://www.scottbuckley.com.au/library/snowfall/ | 9.5 MB | Hopeful, wintery, cinematic (80 BPM) |
| `Moonlight.mp3` | Moonlight | https://www.scottbuckley.com.au/library/moonlight/ | 9.7 MB | Nostalgic, simple piano+strings (80 BPM) |
| `Meanwhile.mp3` | Meanwhile | https://www.scottbuckley.com.au/library/meanwhile/ | 12 MB | Dreamy, ethereal piano + synth (78 BPM) |
| `Unraveling.mp3` | Unraveling | https://www.scottbuckley.com.au/library/unraveling/ | 17 MB | Introspective, bittersweet strings+synth (75 BPM) |
| `FirstSnow.mp3` | First Snow | https://www.scottbuckley.com.au/library/first-snow/ | 8.1 MB | Gentle, calm, wintery |
| **`ChasingDaylight.mp3`** | Chasing Daylight | https://www.scottbuckley.com.au/library/chasing-daylight/ | 10 MB | Contemplative neoclassical piano+strings — journey to find meaning |
| **`Undertow.mp3`** | Undertow | https://www.scottbuckley.com.au/library/undertow/ | 9.5 MB | Sombre, ebbing piano/string/synth — reflective |
| **`Amberlight.mp3`** | Amberlight | https://www.scottbuckley.com.au/library/amberlight/ | 11 MB | Soft, nostalgic piano — Thomas Newman meets Ghibli |
| **`Incredulity.mp3`** | Incredulity | https://www.scottbuckley.com.au/library/incredulity/ | 14 MB | Introspective piano, strings, synth — suspended |

## Dark / Atmospheric (use sparingly)

| File | Track Name | Vibe |
|------|-----------|------|
| `Penumbra.mp3` | Penumbra | Dark, glacial, tender — strings + field recordings (70 BPM) |

## Epic / Horns (avoid for chill montages — too bold)

| File | Track Name | Vibe |
|------|-----------|------|
| `Legacy.mp3` | Legacy | Bold brass, soaring strings, heroic (110 BPM) |
| `Aphelion.mp3` | Aphelion | Slow build → epic climax (~85 BPM) |
| `IntoTheUnknown.mp3` | Into The Unknown | Driving, uplifting |

## Best song for each mood

| You want... | Use |
|------------|-----|
| Hopeful wonder | sb_snowfall, ChasingDaylight |
| Introspective / sad | Unraveling, Undertow |
| Dreamy / floating | Meanwhile |
| Nostalgic / warm | Amberlight, Moonlight |
| Dark / tense | Penumbra, Incredulity |
| Epic battle | Legacy, Aphelion ❌ (not for montages) |

## Download all

```bash
cd sounds
for url in \
  "https://www.scottbuckley.com.au/library/wp-content/uploads/2018/12/sb_snowfall.mp3" \
  "https://www.scottbuckley.com.au/library/wp-content/uploads/2022/12/FirstSnow.mp3" \
  "https://www.scottbuckley.com.au/library/wp-content/uploads/2025/07/Penumbra.mp3" \
  "https://www.scottbuckley.com.au/library/wp-content/uploads/2026/05/Unraveling.mp3" \
  "https://www.scottbuckley.com.au/library/wp-content/uploads/2025/01/Meanwhile.mp3" \
  "https://www.scottbuckley.com.au/library/wp-content/uploads/2022/07/Moonlight.mp3" \
  "https://www.scottbuckley.com.au/library/wp-content/uploads/2021/03/sb_chasingdaylight.mp3" \
  "https://www.scottbuckley.com.au/library/wp-content/uploads/2019/12/sb_undertow.mp3" \
  "https://www.scottbuckley.com.au/library/wp-content/uploads/2025/03/Amberlight.mp3" \
  "https://www.scottbuckley.com.au/library/wp-content/uploads/2025/04/Incredulity.mp3"; do
  curl -sL -o "$(basename "$url")" "$url"
done
```

## Credit

All tracks by Scott Buckley — https://scottbuckley.com.au — CC BY 4.0
