#!/usr/bin/env python3
"""Find dialogue timestamps in video clips.

Accepts a YouTube URL (fetches captions via youtube-transcript-api)
or a local file path (transcribes with Whisper). Searches for the
given dialogue text and outputs timestamps compatible with build_montage.py.

Usage:
  # YouTube URL with existing captions
  uv run find_dialogue.py "https://youtu.be/..." "I will have my vengeance"

  # Local file (transcribes with Whisper)
  uv run find_dialogue.py clip.mp4 "I will have my vengeance"

  # --hook format for build_montage.py
  TIMING=$(uv run find_dialogue.py "https://youtu.be/..." "vengeance" --output hook)
  python build_montage.py movie.mp4 --hook "$TIMING" ...
"""

import argparse, json, re, sys
from pathlib import Path
from urllib.parse import urlparse, parse_qs

CACHE_DIR = Path(__file__).resolve().parent / "transcripts"


def _cache_key(source: str) -> str:
    """Generate a cache key from a YouTube URL or local file path."""
    vid = extract_video_id(source)
    if vid:
        return vid
    return Path(source).stem


def _cache_path(key: str) -> Path:
    return CACHE_DIR / f"{key}-whisper.json"


def _load_cache(key: str) -> list[dict] | None:
    path = _cache_path(key)
    if path.exists():
        with open(path) as f:
            return json.load(f)
    return None


def _save_cache(key: str, segments: list[dict]) -> None:
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    with open(_cache_path(key), "w") as f:
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


def fetch_youtube_transcript(video_id: str, lang: str = "en") -> list[dict]:
    """Fetch transcript from YouTube via youtube-transcript-api."""
    from youtube_transcript_api import YouTubeTranscriptApi

    api = YouTubeTranscriptApi()
    transcript = api.fetch(video_id, languages=[lang])
    return transcript.to_raw_data()


def transcribe_local(path: str, model_name: str = "tiny") -> list[dict]:
    """Transcribe a local audio/video file with Whisper.
    Returns segments as [{text, start, duration}, ...].
    """
    import whisper

    model = whisper.load_model(model_name)
    result = model.transcribe(path, word_timestamps=False)
    segments = []
    for seg in result.get("segments", []):
        segments.append({
            "text": seg["text"].strip(),
            "start": seg["start"],
            "duration": seg["end"] - seg["start"],
        })
    return segments


def fetch_transcript(source: str, lang: str = "en", model: str = "tiny", refresh: bool = False) -> list[dict]:
    """Fetch transcript from YouTube URL (captions) or local file (Whisper)."""
    key = _cache_key(source)
    if not refresh:
        cached = _load_cache(key)
        if cached is not None:
            return cached

    video_id = extract_video_id(source)
    if video_id:
        segments = fetch_youtube_transcript(video_id, lang)
    else:
        segments = transcribe_local(source, model)

    _save_cache(key, segments)
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
    m = int(seconds // 60)
    s = seconds % 60
    return f"{m}:{s:05.2f}"


def main():
    parser = argparse.ArgumentParser(description="Find dialogue timestamps in video clips")
    parser.add_argument("source", help="YouTube URL or local video/audio file path")
    parser.add_argument("dialogue", help="Dialogue text to search for")
    parser.add_argument("--lang", default="en", help="Language code for YouTube captions (default: en)")
    parser.add_argument("--model", default="tiny",
                        help="Whisper model size for local files: tiny, base, small, medium, large (default: tiny)")
    parser.add_argument("--refresh", action="store_true", help="Bypass cache")
    parser.add_argument("--output", choices=["human", "json", "hook"], default="human",
                        help="Output format (default: human-readable timestamps)")
    args = parser.parse_args()

    # Check if local file exists
    is_local = Path(args.source).exists()
    if not is_local and not extract_video_id(args.source):
        print(f"Error: '{args.source}' is not a valid YouTube URL or existing file", file=sys.stderr)
        sys.exit(1)

    try:
        segments = fetch_transcript(
            args.source, lang=args.lang, model=args.model, refresh=args.refresh
        )
        source_type = "Whisper" if is_local else "YouTube captions"
        print(f"   Transcript: {len(segments)} segments ({source_type})", file=sys.stderr)
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
