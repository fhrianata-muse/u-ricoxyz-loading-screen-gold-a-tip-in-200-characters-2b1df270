"""Loading-screen tip entry for make.fun.

Holds the proxy-winning tip as data, validates it against the
competition gate (one line, 1-200 characters), and writes it to
/output/entry.txt. No network, no randomness: the output is
byte-identical on every run.
"""

from pathlib import Path
import sys

LINE = "Tip: your agent just opened the file you were about to open. It was the wrong file. You were about to open the wrong file too — that's why you make a good team."


def valid(line):
    if not 1 <= len(line) <= 200:
        return "length %d, must be 1-200" % len(line)
    if "\n" in line or "\r" in line:
        return "must be a single line"
    if line.strip() != line:
        return "leading or trailing whitespace"
    if "  " in line:
        return "repeated whitespace inside the line"
    if line[-1] not in ".!?":
        return "must end with sentence punctuation"
    return None


def run():
    problem = valid(LINE)
    if problem is not None:
        print("invalid tip: %s" % problem, file=sys.stderr)
        return 1
    out = Path("/output/entry.txt")
    out.parent.mkdir(parents=True, exist_ok=True)
    expected = (LINE + "\n").encode("utf-8")
    out.write_bytes(expected)
    # Verify the round-trip: the grader reads exactly these bytes, so a
    # short write or an encoding slip must fail loudly here, not silently.
    if out.read_bytes() != expected:
        print("verify failed: entry.txt bytes differ", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(run())
