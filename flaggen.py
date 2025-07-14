"""
leetify_random.py – Randomly leetify text to CTF-style flag format.

Regex enforced:  ^ducactf{[\w_!@#?$%\.'"+:->]{5,50}}$
"""

import re
import sys
import random

# Leet substitution options per character
LEET_DICT = {
    "a": "4", "A": "4",
    "b": "8", "B": "8",
    "e": "3", "E": "3",
    "i": "1", "I": "1",
    "l": "1", "L": "1",
    "o": "0", "O": "0",
    "s": "5", "S": "5",
    "t": "7", "T": "7",
    "g": "9", "G": "9",
}

# Allowed characters in flag body
ALLOWED_PATTERN = re.compile(r"[\w_!@#?$%\.'\"+\:->]")

# Full flag format
FLAG_RE = re.compile(r"^ducactf{[\w_!@#?$%\.'\"+\:->]{5,50}}$")


def leetify_random(text: str, seed: int = None) -> str:
    """
    Randomly leetify a string to match CTF flag format.

    Optionally set a seed for reproducibility.
    """
    if seed is not None:
        random.seed(seed)

    result = []

    for char in text:
        # Space becomes underscore
        if char == " ":
            result.append("_")
            continue

        # 50% chance to replace if a leet alternative exists
        if char in LEET_DICT and random.choice([True, False]):
            result.append(LEET_DICT[char])
        else:
            result.append(char)

    # Filter to allowed characters only
    cleaned = "".join(c for c in result if ALLOWED_PATTERN.fullmatch(c))

    if not (5 <= len(cleaned) <= 50):
        raise ValueError(
            f"Flag body must be 5–50 allowed characters after cleaning; got {len(cleaned)}"
        )

    flag = f"ctf{{{cleaned}}}"

    if not FLAG_RE.fullmatch(flag):
        raise RuntimeError("Generated flag failed regex validation")

    return flag

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python leetify_random.py \"text to leetify\" [optional_seed]")
        sys.exit(1)

    text = " ".join(sys.argv[1:-1]) if len(sys.argv) > 2 else sys.argv[1]
    seed = int(sys.argv[-1]) if len(sys.argv) > 2 and sys.argv[-1].isdigit() else None

    try:
        flag = leetify_random(text, seed=seed)
        print(flag)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(2)
