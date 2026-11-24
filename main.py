"""Two-Sentence Horror — entry program.

Writes one horror story of exactly two sentences (<=400 chars) to
/output/entry.txt. Stdlib only, deterministic.
"""
import os
import re

MAX_CHARS = 400  # sealed scorer gate (RULES.txt): 1-400 characters.

TEXT = (
    "The new doorbell camera sends me a photo every time someone stands "
    "on the porch, and at 03:12 it sent one of me, standing on my own "
    "porch, waving. I have not left my bed all night, and the camera "
    "just sent another."
)

_SENTENCE_END = re.compile(r"[.!?]+(?:\s+|$)")


def count_sentences(text):
    """Count sentences by terminal punctuation followed by space/end."""
    return len(_SENTENCE_END.findall(text.strip())) if text.strip() else 0


def check_gate(text):
    """Enforce the scorer's gate (RULES.txt) plus the brief's two-sentence rule.

    UTF-8 text of 1-400 chars, not whitespace-only, no control characters,
    no newline, exactly two sentences. Fail loudly instead of writing an
    invalid entry.
    """
    if not isinstance(text, str):
        return False
    if not 1 <= len(text) <= MAX_CHARS:
        return False
    if not text.strip():
        return False
    if "\n" in text or "\r" in text:
        return False
    if any(ord(c) < 32 for c in text):
        return False
    if count_sentences(text) != 2:
        return False
    return True


def main():
    if not check_gate(TEXT):
        raise SystemExit("entry text violates the 1-400 char two-sentence gate")
    out_dir = os.environ.get("OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "entry.txt")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(TEXT)
    # Write-verify: read the file back and refuse to exit cleanly if
    # the bytes on disk differ from the gated text.
    with open(out_path, "r", encoding="utf-8") as f:
        if f.read() != TEXT:
            raise SystemExit("entry.txt on disk does not match the gated text")


if __name__ == "__main__":
    main()
