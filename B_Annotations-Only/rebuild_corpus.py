#!/usr/bin/env python3
"""
rebuild_corpus.py — reassembling the annotated texts from your own text files.

PURPOSE
    For 17 text versions of this corpus the base text cannot be published
    alongside — not for reasons of copyright, but because of the source. What is
    published are the annotations (TEI standoff with character offsets). This
    script joins the two again: you provide your own copy of the text, and the
    script produces the annotated version from it.

WHAT YOU NEED
    For each text a .txt file containing the text of the relevant critical
    edition, UTF-8, NFC-normalised. Place it beside the corresponding
    annotationcollections/ folder, under the file name given in manifest.json.

    The underlying editions are de Jonge, PVTG I/2, Brill 1978 for the twelve
    testaments and Harrington, SC 229, 1976 for Ps.-Philo). If you obtain a text
    from a licensed database, please observe its terms of use.

USAGE
    python3 rebuild_corpus.py .            # verify and build
    python3 rebuild_corpus.py . --check    # verify only, write nothing

DIVERGING TEXT VERSIONS
    The offsets hold for exactly the version of the text on which the annotation
    was made (its length and SHA-256 are given in manifest.json). If your version
    differs, the offsets do not fit, and this script stops with a message rather
    than annotating the wrong places.

    To find the divergence, use normalise.py: it brings the file onto the same
    character basis, checks the SHA-256 sum, and where it differs uses the layout
    mask in layout/ to show you which line is at fault. The instructions are in
    README.md, section "Producing the texts without a base text yourself".
"""

import sys
import re
import json
import hashlib
import unicodedata
from pathlib import Path
import xml.etree.ElementTree as ET

TEI = "{http://www.tei-c.org/ns/1.0}"
XI = "{http://www.w3.org/XML/1998/namespace}"
CHAR_RE = re.compile(r"char=(\d+),(\d+)")
CODE_RE = re.compile(r"^\[(.*?)\]\s*(.*)$")


def read_exact(p):
    with open(p, encoding="utf-8", newline="") as f:
        return f.read()


def write_exact(p, s):
    with open(p, "w", encoding="utf-8", newline="") as f:
        f.write(s)


def parse_annotations(xml_path):
    """(segments, instance_labels) from the CATMA TEI standoff file."""
    root = ET.parse(xml_path).getroot()
    tagdefs = {}
    for fd in root.iter(TEI + "fsDecl"):
        de = fd.find(TEI + "fsDescr")
        descr = (de.text or "").strip() if de is not None else ""
        m = CODE_RE.match(descr)
        tagdefs[fd.get(XI + "id")] = (m.group(1), m.group(2)) if m else (fd.get(XI + "id"), descr)
    labels = {fs.get(XI + "id"): tagdefs.get(fs.get("type"), (fs.get("type"), "?"))
              for fs in root.iter(TEI + "fs")}
    segments = []
    for ch in root.find(f".//{TEI}body/{TEI}ab"):
        p = ch if ch.tag == TEI + "ptr" else ch.find(TEI + "ptr")
        if p is None:
            continue
        m = CHAR_RE.search(p.get("target", ""))
        ids = frozenset(a.lstrip("#") for a in (ch.get("ana", "") or "").split() if a.strip())
        segments.append((int(m.group(1)), int(m.group(2)), ids))
    segments.sort(key=lambda s: s[0])
    return segments, labels


def derive_spans(segments):
    """Derive one contiguous span per instance from the sequence of segments.
    Every iteration over a set is sorted — the result is reproducible."""
    open_, last, spans = {}, {}, []
    prev = frozenset()
    for start, end, ids in segments:
        for i in sorted(ids - prev):
            open_[i] = start
        for i in sorted(prev - ids):
            spans.append((i, open_.pop(i), last[i]))
        for i in ids:
            last[i] = end
        prev = ids
    for i, s in sorted(open_.items()):
        spans.append((i, s, last[i]))
    return spans


def build_merged(text, spans, labels):
    """Insert the markers into the text. The ordering at any one position is
    fully determined: closes before opens, longer spans outside, instance id as
    the tiebreaker."""
    events = {}
    for inst, s, e in spans:
        code, label = labels.get(inst, (inst, "?"))
        events.setdefault(s, []).append(((1, -(e - s), str(inst)), f"[[{code}::{label}]]"))
        events.setdefault(e, []).append(((0, -s, str(inst)), f"[[/{code}]]"))
    out, last = [], 0
    for pos in sorted(events):
        out.append(text[last:pos])
        for _, marker in sorted(events[pos], key=lambda x: x[0]):
            out.append(marker)
        last = pos
    out.append(text[last:])
    return "".join(out)


def process(folder, entry, mode):
    name = folder.name
    txt = folder / entry["txt_expected"]
    xml = folder / "annotationcollections" / entry["xml"]

    if not txt.exists():
        return ("MISSING", name, f"text file not found: {entry['txt_expected']}")

    text = read_exact(txt)
    nfc = unicodedata.normalize("NFC", text)
    hint = ""
    if nfc != text:
        hint = "  (note: your file is not NFC-normalised)"

    digest = hashlib.sha256(text.encode()).hexdigest()
    exact = (digest == entry["sha256"])

    if not exact:
        detail = (f"length {len(text)}, {entry['characters']} expected"
                  f"{'' if len(text) != entry['characters'] else '; length matches, content differs'}{hint}")
        return ("DIVERGES", name,
                detail + "  -> see normalise.py and layout/")

    segments, labels = parse_annotations(xml)
    status = "OK"

    max_end = max((e for _, e, _ in segments), default=0)
    if max_end != len(text):
        return ("ERROR", name, f"last annotation offset {max_end} != text length {len(text)}")

    spans = derive_spans(segments)
    merged = build_merged(text, spans, labels)

    stripped = re.sub(r"\[\[/?[^\]]*?\]\]", "", merged)
    if stripped != text:
        return ("ERROR", name, "self-test failed: the markers alter the text")

    if mode != "check":
        write_exact(folder / f"{txt.stem}_merged.txt", merged)
    return (status, name, f"{len(spans)} annotations")


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    root = Path(sys.argv[1])
    mode = "check" if "--check" in sys.argv else "build"

    mf = root / "manifest.json"
    if not mf.exists():
        mf = root / "B_Annotations-Only" / "manifest.json"
    if not mf.exists():
        print("manifest.json not found.")
        sys.exit(1)
    base = mf.parent
    manifest = json.loads(mf.read_text(encoding="utf-8"))

    results = []
    for name, entry in sorted(manifest.items()):
        folder = base / name
        if not folder.exists():
            results.append(("MISSING", name, "folder not found"))
            continue
        results.append(process(folder, entry, mode))

    w = max(len(r[1]) for r in results)
    for status, name, detail in results:
        print(f"  {status:14} {name[:w]:{w}}  {detail}")

    ok = sum(1 for r in results if r[0].startswith("OK"))
    print(f"\n{ok}/{len(results)} texts reassembled"
          + ("  (check mode — nothing written)" if mode == "check" else ""))
    if ok < len(results):
        print("\nWhere versions diverge: your text must correspond exactly to the")
        print("version on which the annotation was made (UTF-8, NFC, length as")
        print("given in manifest.json).")


if __name__ == "__main__":
    main()
