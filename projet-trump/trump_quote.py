#!/usr/bin/env python3
"""
Fetch a random Trump quote from WhatDoesTrumpThink API.
Endpoint: https://api.whatdoestrumpthink.com/api/v1/quotes/random
"""

from __future__ import annotations

import json
import sys
import urllib.request
import urllib.error


API_URL = "https://api.whatdoestrumpthink.com/api/v1/quotes/random"


def fetch_random_quote(url: str = API_URL, timeout: int = 10) -> str:
    req = urllib.request.Request(
        url,
        headers={
            "Accept": "application/json",
            "User-Agent": "trump-quote-cli/1.0 (+https://github.com/your-repo)",
        },
        method="GET",
    )

    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            charset = resp.headers.get_content_charset() or "utf-8"
            data = resp.read().decode(charset)
    except urllib.error.HTTPError as e:
        raise RuntimeError(f"HTTP error {e.code}: {e.reason}") from e
    except urllib.error.URLError as e:
        raise RuntimeError(f"Network error: {e.reason}") from e

    try:
        payload = json.loads(data)
    except json.JSONDecodeError as e:
        raise RuntimeError("Invalid JSON response") from e

    # According to the API docs, the quote text is in payload["message"]
    # :contentReference[oaicite:1]{index=1}
    msg = payload.get("message")
    if not isinstance(msg, str) or not msg.strip():
        raise RuntimeError("Unexpected API response: missing 'message' field")

    return msg.strip()


def main() -> int:
    try:
        quote = fetch_random_quote()
        print(quote)
        return 0
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())