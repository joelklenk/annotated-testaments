#!/usr/bin/env python3
"""
normalise.py — character normalisation of your own copy of a text.

PURPOSE
    The annotations in this package point to character offsets in one
    particular version of the text. If you obtain the base text yourself (see
    README.md, section "Producing the texts without a base text yourself"),
    this script brings it onto the same character basis and then tells you,
    through the SHA-256 checksum, whether you hold the right version.

WHAT IT DOES — character substitutions only, no intervention in the text:
    U+00A0 NO-BREAK SPACE        -> U+0020 SPACE
    U+2022 BULLET (as a colon)   -> U+00B7 MIDDLE DOT
    NFC normalisation, and with it:
      U+1F71 OXIA etc.           -> U+03AC TONOS etc.
      U+0387 GREEK ANO TELEIA    -> U+00B7 MIDDLE DOT
      U+037E GREEK QUESTION MARK -> U+003B SEMICOLON
      decomposed characters (NFD) -> composed

WHAT IT LEAVES ALONE
    Editorial signs { } [ ] < > *, question marks, exclamation marks, dashes,
    every letter, every word, every word order, every line break. The script
    changes nothing that concerns the text itself.

USAGE
    python3 normalise.py <file.txt|folder>            # report only
    python3 normalise.py <file.txt|folder> --apply    # write

    If manifest.json sits alongside, the SHA-256 checksum is checked against
    the expected value automatically.
"""

import sys
import re
import json
import difflib
import hashlib
import unicodedata
from pathlib import Path


def read_exact(p):
    """Read character-exactly — no newline translation."""
    with open(p, encoding="utf-8", newline="") as f:
        return f.read()


def write_exact(p, s):
    """Write character-exactly — CRLF stays CRLF."""
    with open(p, "w", encoding="utf-8", newline="") as f:
        f.write(s)


def normalise(text):
    """(new_text, [(what, how_many)])"""
    changes, out = [], text

    n = out.replace(" ", " ")
    if n != out:
        changes.append(("U+00A0 NO-BREAK SPACE -> SPACE", out.count(" ")))
        out = n

    # BULLET only where it stands as punctuation (before whitespace/end of line)
    cnt = len(re.findall(r"•(?=\s|$)", out))
    if cnt:
        out = re.sub(r"•(?=\s|$)", "·", out)
        changes.append(("U+2022 BULLET -> U+00B7 MIDDLE DOT", cnt))

    before = out
    out = unicodedata.normalize("NFC", out)
    if out != before:
        oxia = sum(1 for a, b in zip(before, out) if a != b and len(before) == len(out))
        changes.append(("NFC (OXIA -> TONOS, Ano Teleia, decompositions)",
                        oxia or abs(len(before) - len(out)) or 1))
    return out, changes


def mask(text):
    """Everything textual becomes '·'. Whitespace, line structure and the
    chapter/verse numbers at the start of a line are kept. Length-preserving."""
    out = []
    for line in text.split("\n"):
        m = re.match(r"^(\s*)((?:[IVXLC]+|\d+\.)(?=\s|$))?(.*)$", line, flags=re.S)
        out.append(m.group(1) + (m.group(2) or "") + re.sub(r"\S", "·", m.group(3)))
    return "\n".join(out)


def layout_diff(new, layout_file, limit=10):
    """Shows where the layout of your version departs from the reference.
    Line-by-line alignment, so that one missing line does not make everything
    after it look like a divergence."""
    expected = read_exact(layout_file).split("\n")
    actual = mask(new).split("\n")
    print(f"      layout comparison against {layout_file.name}: "
          f"{len(actual)} lines, {len(expected)} expected")

    def shape(line):
        """Reduce a line to its form: indentation, marker, length."""
        m = re.match(r"^(\s*)((?:[IVXLC]+|\d+\.)(?=\s|$))?(.*)$", line, flags=re.S)
        return (m.group(1), m.group(2) or "", len(m.group(3)))

    sm = difflib.SequenceMatcher(None, [shape(x) for x in expected],
                                 [shape(x) for x in actual], autojunk=False)
    shown = 0
    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        if tag == "equal":
            continue
        for k in range(max(i2 - i1, j2 - j1)):
            shown += 1
            if shown > limit:
                print("      … further divergences")
                return
            a = expected[i1 + k] if i1 + k < i2 else None
            b = actual[j1 + k] if j1 + k < j2 else None
            z = f"      line {(j1 + k) + 1:>4}: "
            if a is None:
                print(z + f"surplus        «{b[:50]}»")
            elif b is None:
                print(z + f"missing        «{a[:50]}»  (reference line {i1 + k + 1})")
            else:
                ka, kb = shape(a), shape(b)
                if ka[0] != kb[0]:
                    print(z + f"indentation {len(kb[0])} instead of {len(ka[0])} spaces")
                elif ka[1] != kb[1]:
                    print(z + f"marker «{kb[1]}» instead of «{ka[1]}»")
                else:
                    print(z + f"line length {kb[2]} instead of {ka[2]} characters")
    if not shown:
        print("      layout matches — the divergence lies in individual characters.")


def manifest_for(path):
    for folder in (path.parent, path.parent.parent):
        mf = folder / "manifest.json"
        if mf.exists():
            d = json.loads(mf.read_text(encoding="utf-8"))
            d["__base__"] = folder
            return d
    return {}


def process(path, apply, mf):
    text = read_exact(path)
    new, changes = normalise(text)
    sha = hashlib.sha256(new.encode()).hexdigest()

    print(f"\n{path.name}")
    if changes:
        for what, n in changes:
            print(f"   {n:>6}x  {what}")
    else:
        print("          no change needed")

    # Write first, report afterwards — otherwise writing would hang on the check.
    if apply and new != text:
        write_exact(path, new)
        print("          written")

    expected = None
    for name, e in mf.items():
        if name == "__base__":
            continue
        if e.get("txt_expected") == path.name or name == path.stem:
            expected = e
            break

    print(f"   {len(new):>6}   characters"
          + (f"   ({expected['characters']} expected)" if expected else ""))
    print(f"   SHA-256  {sha}")

    if expected is None:
        # Name unknown — does the content match an entry all the same?
        match = [n for n, e in mf.items()
                 if n != "__base__" and e.get("sha256") == sha]
        if match:
            print(f"   -> identical in content with «{match[0]}». The offsets fit.")
            return True
        print("   -> no manifest entry for this file name.")
        return False

    if sha == expected["sha256"]:
        print("   -> matches the manifest. The offsets fit.")
        return True

    print(f"   -> DIVERGES. Expected: {expected['sha256']}")
    if len(new) != expected["characters"]:
        print(f"      difference in length: {len(new) - expected['characters']} characters.")
    lay = expected.get("layout")
    if lay:
        lay_path = mf["__base__"] / lay
        if lay_path.exists():
            layout_diff(new, lay_path)
    return False


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    target = Path(sys.argv[1])
    apply = "--apply" in sys.argv
    # layout/ holds the masks, not the texts — do not process those.
    files = (sorted(p for p in target.rglob("*.txt")
                    if "merged" not in p.name and "layout" not in p.parts)
             if target.is_dir() else [target])
    if not files:
        print("No .txt files found.")
        sys.exit(1)
    mf = manifest_for(files[0])
    ok = sum(process(p, apply, mf) for p in files)
    print(f"\n{ok}/{len(files)} files match the manifest."
          + ("" if apply else "  (report mode — nothing written)"))


if __name__ == "__main__":
    main()
