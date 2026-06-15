#!/usr/bin/env python3
"""Find dialogue timestamps in YouTube clips via their captions.

Extracts the video ID from a YouTube URL, fetches the transcript via
youtube-transcript-api, and searches for the given dialogue text.
Outputs timestamps in a format compatible with build_montage.py --hook.

Usage:
  # Human-readable output
  uv run find_dialogue.py "https://youtu.be/..." "I will have my vengeance"

  # --hook format for build_montage.py
  TIMING=$(uv run find_dialogue.py "https://youtu.be/..." "vengeance" --output hook)
  python build_montage.py movie.mp4 --hook "$TIMING" ...

  # JSON for scripting
  uv run find_dialogue.py "https://youtu.be/..." "vengeance" --output json
"""

import argparse, json, re, sys
from pathlib import Path
from urllib.parse import urlparse, parse_qs

CACHE_DIR = Path(__file__).resolve().parent / "transcripts"


def _cache_path(video_id: str, lang: str) -> Path:
    return CACHE_DIR / f"{video_id}-{lang}.json"


def _load_cache(video_id: str, lang: str) -> list[dict] | None:
    path = _cache_path(video_id, lang)
    if path.exists():
        with open(path) as f:
            return json.load(f)
    return None


def _save_cache(video_id: str, lang: str, segments: list[dict]) -> None:
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    with open(_cache_path(video_id, lang), "w") as f:
        json.dump(segments, f, indent=2)


def extract_video_id(url: str) -> str | None:
    """Parse video ID from common YouTube URL formats."""
    parsed = urlparse(url)
    host = parsed.hostname or ""
    if host in ("youtu.be",):
        return parsed.path.lstrip("/").split("?")[0]
    if host.endswith("youtube.com"):
        return parse_qs(parsed.query).get("v", [None])[0]
    return None


def fetch_transcript(video_id: str, lang: str = "en", refresh: bool = False) -> list[dict]:
    """Fetch transcript segments as raw dicts: {text, start, duration}.

    Caches transcripts locally to avoid re-fetching. Pass refresh=True to
    bypass the cache and re-download from YouTube.
    """
    if not refresh:
        cached = _load_cache(video_id, lang)
        if cached is not None:
            return cached

    from youtube_transcript_api import YouTubeTranscriptApi

    api = YouTubeTranscriptApi()
    transcript = api.fetch(video_id, languages=[lang])
    segments = transcript.to_raw_data()
    _save_cache(video_id, lang, segments)
    return segments


def search(segments: list[dict], query: str) -> list[dict]:
    """Find transcript segments whose text contains the query (case-insensitive)."""
    q = query.lower()
    results = []
    for seg in segments:
        if q in seg["text"].lower():
            results.append({
                "text": seg["text"].strip(),
                "start": seg["start"],
                "end": seg["start"] + seg["duration"],
            })
    return results


def format_ts(seconds: float) -> str:
    """Format seconds as mm:ss with two-decimal precision."""
    m = int(seconds // 60)
    s = seconds % 60
    return f"{m}:{s:05.2f}"


def main():
    parser = argparse.ArgumentParser(description="Find dialogue timestamps in YouTube clips")
    parser.add_argument("url", help="YouTube URL")
    parser.add_argument("dialogue", help="Dialogue text to search for")
    parser.add_argument("--lang", default="en", help="Language code (default: en)")
    parser.add_argument("--refresh", action="store_true", help="Bypass cache and re-fetch transcript")
    parser.add_argument(
        "--output", choices=["human", "json", "hook"], default="human",
        help="Output format (default: human-readable timestamps)",
    )
    args = parser.parse_args()

    video_id = extract_video_id(args.url)
    if not video_id:
        print(f"Error: could not extract video ID from: {args.url}", file=sys.stderr)
        sys.exit(1)

    try:
        segments = fetch_transcript(video_id, args.lang, refresh=args.refresh)
    except Exception as e:
        print(f"Error fetching transcript: {e}", file=sys.stderr)
        sys.exit(1)

    matches = search(segments, args.dialogue)
    if not matches:
        print(f'No match found for "{args.dialogue}"', file=sys.stderr)
        sys.exit(1)

    if args.output == "json":
        print(json.dumps(matches))

    elif args.output == "hook":
        m = matches[0]
        print(f"{m['start']:.1f}-{m['end']:.1f}")

    else:
        for m in matches:
            start_ts = format_ts(m["start"])
            end_ts = format_ts(m["end"])
            print(f"  {start_ts} \u2192 {end_ts}  ({m['start']:.1f}s\u2013{m['end']:.1f}s)  {m['text']}")


if __name__ == "__main__":
    main()
