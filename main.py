#!/usr/bin/env python3
"""Write one alien one-star review of Earth to /output/entry.txt.

Deterministic: no network, no clock, no randomness. The review is a fixed
string. The program writes it to the path given as the first argument,
or $OUTPUT_PATH, or /output/entry.txt by default, and enforces the
competition gate: one sentence, 1 to 200 characters, not only white space.
"""

import os
import sys
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

ENTRY = "One star: your gravity broke my luggage, your weather changed its mind twice, and the locals kept asking about my probe, but the tacos were worth the abduction."

MIN_CHARS = 1
MAX_CHARS = 200
DEFAULT_PATH = "/output/entry.txt"


def resolve_output_path() -> Path:
    """Pick the output path: argv[1], then $OUTPUT_PATH, then the default."""
    if len(sys.argv) > 1:
        return Path(sys.argv[1])
    env_path = os.environ.get("OUTPUT_PATH")
    if env_path:
        return Path(env_path)
    return Path(DEFAULT_PATH)


def validate(text: str) -> int:
    """Enforce the competition gate: one sentence, 1 to 200 chars.

    Returns the character count. Raises ValueError when the gate fails.
    """
    chars = len(text)
    if not (MIN_CHARS <= chars <= MAX_CHARS):
        raise ValueError(f"entry is {chars} characters, outside 1-200")
    if not text.strip():
        raise ValueError("entry is only white space")
    if text.strip().count(".") != 1 or not text.strip().endswith("."):
        raise ValueError("entry is not exactly one sentence")
    return chars


def write_entry(path: Path, text: str) -> int:
    """Validate the text, write it to path, and return its length.

    Creates any missing parent directories first.
    """
    chars = validate(text)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    return chars


def main() -> int:
    path = resolve_output_path()
    try:
        chars = write_entry(path, ENTRY)
    except ValueError as exc:
        print(exc, file=sys.stderr)
        return 1
    print(f"wrote {chars} characters to {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
