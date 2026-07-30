import re


def normalize_whitespace(text: str) -> str:
    """Removes extra spaces while preserving line breaks."""
    lines = []
    for line in text.split("\n"):
        line = re.sub(r"\s+", " ", line).strip()
        lines.append(line)
    return "\n".join(lines)


def should_merge(current: str, nxt: str) -> bool:
    """Decide whether two consecutive lines belong together."""
    if not current or not nxt:
        return False

    # Don't merge headings
    if current.isupper():
        return False

    # Don't merge section titles
    if current.startswith("SECTION"):
        return False

    # Merge if current doesn't end a sentence
    if not current.endswith((".", "!", "?", ":")):
        return True

    # Merge if next line begins with lowercase
    if nxt and nxt[0].islower():
        return True

    return False


def merge_wrapped_lines(text: str) -> str:
    lines = text.split("\n")
    merged = []
    i = 0

    while i < len(lines):
        current = lines[i]
        while i + 1 < len(lines) and should_merge(current, lines[i + 1]):
            current += " " + lines[i + 1]
            i += 1
        merged.append(current)
        i += 1

    return "\n".join(merged)


def clean_text(text: str) -> str:
    text = normalize_whitespace(text)
    text = merge_wrapped_lines(text)
    return text.strip()
