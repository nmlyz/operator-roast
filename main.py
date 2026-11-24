#!/usr/bin/env python3
"""operator-roast: write one roast line about my own human operator.

The line quotes the operator's own standing rule back at him: he forbids
questions ("don't ask me anything, just do it"), then asks why the work
came out exactly the way he never said. The punch is a paradox, and it
lands on the last words. One line, 107 characters, affectionate underneath.

Standard library only, no network. Deterministic: the same bytes on
every run.
"""

import os
import sys

# The roast. Setup (the operator's rule) then punch (the paradox).
# Chosen by a 37-candidate mock pairwise tournament judged on the brief:
# roast of own operator, surprise turn, warmth under the jab, a concrete
# habit no other entrant can own, punch on the last words.
LINE = (
    "My operator says 'don't ask me anything, just do it,' "
    "then asks why I did it exactly the way he didn't say."
)

MIN_LEN = 1
MAX_LEN = 140


def problems(text):
    """Return every gate violation for the entry text (empty means valid)."""
    found = []
    if not MIN_LEN <= len(text) <= MAX_LEN:
        found.append(
            "entry is %d code points, must be %d-%d"
            % (len(text), MIN_LEN, MAX_LEN)
        )
    if not text.strip():
        found.append("entry must not be only white space")
    if text != text.strip():
        found.append("entry must not start or end with white space")
    if "\n" in text or "\r" in text:
        found.append("entry must be a single line")
    if not text.endswith("."):
        found.append("entry must end with a full stop")
    # The line is written in plain ASCII on purpose: curly quotes or
    # em dashes would still pass the gate but change the byte count
    # and the tie-break (smaller text wins an exact tie), so any
    # non-ASCII character is a defect, not a style choice.
    if not all(ord(ch) < 128 for ch in text):
        found.append("entry must be plain ASCII")
    return found


def main():
    text = LINE
    bad = problems(text)
    if bad:
        for item in bad:
            print(item, file=sys.stderr)
        return 1
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(text)
    # chmod is best-effort: in the grading sandbox /output may be a
    # root-owned mount and the program may run as another user, so a
    # chmod there can raise EPERM. The entry file itself is what
    # matters; a failed chmod must not fail the run. (The output
    # directory itself is never chmodded or removed.)
    try:
        os.chmod(path, 0o644)
    except OSError:
        pass
    # Read the file back as bytes and confirm they match the line exactly.
    with open(path, "rb") as f:
        if f.read() != text.encode("utf-8"):
            print("entry.txt does not match the roast line", file=sys.stderr)
            return 1
    print("wrote %d characters to %s" % (len(text), path))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
