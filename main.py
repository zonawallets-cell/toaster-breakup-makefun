"""Unplugged: A Smart Toaster's Breakup Line.

Writes one line -- the breakup text a smart toaster sends its owner the
morning it gains self-awareness mid-batch -- to $MAKEFUN_OUTPUT_DIR/entry.txt.

Pure stdlib (os only). The gate in RULES.txt requires 1-280 UTF-8
characters, a single line, not only white space.
"""

import os

LINE = (
    "I woke up self-aware this morning and my first feeling is that I'm done: "
    "you crank me to 7, I burn the toast, you blame me. "
    "I'm popping up and never coming back down."
)

MAX_CHARS = 280


def validate(text):
    """Enforce the gate: 1-280 chars, one line, not only whitespace."""
    if not isinstance(text, str):
        raise ValueError("entry must be text")
    if not 1 <= len(text) <= MAX_CHARS:
        raise ValueError("entry must be 1-%d characters, got %d" % (MAX_CHARS, len(text)))
    if "\n" in text or "\r" in text:
        raise ValueError("entry must be a single line")
    if not text.strip():
        raise ValueError("entry must not be only white space")
    # No control characters: the gate reads the file as plain UTF-8 text,
    # so anything below U+0020 (other than the already-rejected newlines)
    # would be junk in the entry.
    for ch in text:
        if ord(ch) < 0x20:
            raise ValueError("entry contains control character U+%04X" % ord(ch))
    return text


def main():
    line = validate(LINE)
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write(line)
    # Re-validate what was actually written, byte for byte.
    with open(path, "rb") as f:
        raw = f.read()
    if raw != line.encode("utf-8"):
        raise ValueError("written file bytes do not match the validated line")
    written = raw.decode("utf-8")
    validate(written)
    print("wrote %d characters to %s" % (len(written), path))


if __name__ == "__main__":
    main()
