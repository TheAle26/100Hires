import json
import os
import re
from pathlib import Path
from typing import Any
from urllib.parse import parse_qs, urlparse

import requests
from dotenv import load_dotenv


VIDEO_URLS = [
    "https://www.youtube.com/watch?v=PqKXA9LvWUc&t=767s",
    "https://www.youtube.com/watch?v=SuYLRq-xK2U",
    "https://www.youtube.com/watch?v=RxwMMROFWPc&t=3s",
    "https://www.youtube.com/watch?v=KjK5-L-wDVg",
    "https://www.youtube.com/watch?v=83zPgIzYJAY",
    "https://www.youtube.com/watch?v=7KR3YiN6uYo",
]

SUPADATA_ENDPOINT = "https://api.supadata.ai/v1/youtube/transcript"
SUPADATA_METADATA_ENDPOINT = "https://api.supadata.ai/v1/youtube/video"
OUTPUT_DIR = Path("research/youtube-transcripts")


def _unwrap_data(payload: Any) -> dict[str, Any]:
    """Return the main object for API responses that may wrap data."""
    if isinstance(payload, dict) and isinstance(payload.get("data"), dict):
        return payload["data"]
    return payload if isinstance(payload, dict) else {}


def extract_video_id(url: str) -> str:
    parsed = urlparse(url)
    hostname = parsed.netloc.lower()

    if "youtu.be" in hostname:
        return parsed.path.strip("/").split("/")[0]

    if "youtube.com" in hostname:
        query = parse_qs(parsed.query)
        if "v" in query and query["v"]:
            return query["v"][0]
        if parsed.path.startswith("/shorts/"):
            return parsed.path.split("/shorts/")[1].split("/")[0]
        if parsed.path.startswith("/embed/"):
            return parsed.path.split("/embed/")[1].split("/")[0]

    return "unknown_video"


def sanitize_filename(name: str) -> str:
    cleaned = re.sub(r'[<>:"/\\|?*\x00-\x1F]', "", name)
    cleaned = re.sub(r"\s+", "_", cleaned).strip("._")
    return cleaned[:120] or "untitled_video"


def extract_transcript_text(payload: dict[str, Any]) -> str:
    for key in ("transcript", "content", "captions"):
        value = payload.get(key)
        if isinstance(value, str) and value.strip():
            return value.strip()
        if isinstance(value, list):
            pieces = []
            for item in value:
                if isinstance(item, str):
                    pieces.append(item)
                elif isinstance(item, dict):
                    text = item.get("text") or item.get("content")
                    if isinstance(text, str) and text.strip():
                        pieces.append(text.strip())
            if pieces:
                return "\n".join(pieces)
    return json.dumps(payload, ensure_ascii=True, indent=2)


def pick_metadata(payload: dict[str, Any]) -> tuple[str, str]:
    metadata = payload.get("metadata", {})
    author = (
        metadata.get("channelTitle")
        or metadata.get("author")
        or payload.get("author")
        or "Unknown_Author"
    )
    title = metadata.get("title") or payload.get("title") or "Unknown_Title"

    return str(title).strip(), str(author).strip()


def fetch_metadata(url: str, api_key: str) -> tuple[str, str]:
    video_id = extract_video_id(url)
    try:
        response = requests.get(
            SUPADATA_METADATA_ENDPOINT,
            headers={"x-api-key": api_key},
            params={"id": video_id},
            timeout=15,
        )

        response.raise_for_status()
        data = _unwrap_data(response.json())

        if not data:
            return "Unknown_Title", "Unknown_Author"

        author = (
            data.get("channelTitle")
            or data.get("channel_title")
            or data.get("author")
            or data.get("author_name")
            or data.get("channel", {}).get("name")
            or "Unknown_Author"
        )
        title = data.get("title") or data.get("videoTitle")

        if not title or not author:
            fallback_title, fallback_author = pick_metadata(data)
            title = title or fallback_title
            author = author or fallback_author

        return str(title).strip(), str(author).strip()

    except Exception:
        return "Unknown_Title", "Unknown_Author"


def fetch_transcript(url: str, api_key: str) -> str:
    """Fetch only transcript text for a single video URL."""
    response = requests.get(
        SUPADATA_ENDPOINT,
        headers={"x-api-key": api_key},
        params={"url": url},
        timeout=45,
    )
    response.raise_for_status()
    payload = _unwrap_data(response.json())
    return extract_transcript_text(payload)


def main() -> None:
    load_dotenv()
    api_key = os.getenv("SUPADATA_API_KEY")
    if not api_key:
        raise RuntimeError("Missing SUPADATA_API_KEY in your .env file.")

    if not VIDEO_URLS:
        print("No URLs found in VIDEO_URLS. Add at least one YouTube URL and run again.")
        return

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    for idx, url in enumerate(VIDEO_URLS, start=1):
        print(f"[{idx}/{len(VIDEO_URLS)}] Processing {url}...")
        try:
            title, author = fetch_metadata(url, api_key)
            transcript = fetch_transcript(url, api_key)

            author_dir = OUTPUT_DIR / sanitize_filename(author)
            author_dir.mkdir(parents=True, exist_ok=True)

            filename = sanitize_filename(title) + ".txt"
            output_path = author_dir / filename

            output_path.write_text(transcript, encoding="utf-8")
            print(f"   Success! Saved to: {output_path}")

        except Exception as err:
            print(f"   Failed for {url}: {err}")


if __name__ == "__main__":
    main()
