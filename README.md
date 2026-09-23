# Annotated Corpus of Ancient Testamentary Literature

Manual genre annotation of 33 ancient testamentary texts (Greek, Latin).
Annotated with CATMA; the annotations record features typical of the genre —
narrative framing, speaker, addressees, proximity of death, ethical exhortation,
eschatological perspective, and others.

The rules, the complete tagset and the procedure are given in
**`ANNOTATION_GUIDELINES.md`**.

**Extent:** 33 texts in 38 text versions, 3,451 annotation instances.
The five Ps.-Philo texts are present in two versions (see below).

---

## Why this package is divided in two

The **annotations** throughout are the scholarly work of the authors named in
`CITATION.cff` and are released under CC BY 4.0.

**21 text versions** are included here in full, **17** without their base text:

- the **twelve Testaments of the Twelve Patriarchs**, annotated on de Jonge's
  edition (PVTG I/2, Brill 1978);
- the **five Ps.-Philo texts**, annotated on Harrington's edition (SC 229,
  Cerf 1976). For these five the base text has additionally been produced from
  a public-domain edition — see *Ps.-Philo in two versions*.

To the best of our understanding the underlying editions are in both cases no
longer protected under § 70 UrhG, the German copyright provision covering
scholarly editions (de Jonge 1978 since 2003, Harrington 1976 since 2001).
Neither publisher has permitted publication of the text, however, and we
therefore refrain from it for the time being.

For all 17 texts without a base text, instructions are provided for
reassembling them in a few steps. The result is verifiable through SHA-256
checksums: anyone following the instructions demonstrably holds exactly the text
version to which the offsets refer.

A third folder, `C_CATMA-Import`, carries no material of its own: it is the
twenty-one full text versions once more, in the form CATMA reads on import.

This is a **preliminary version**. The concept DOI remains unchanged across
future versions, and citations of this version remain valid.

---

## A_Full-Text — 21 text versions, complete

Base text, annotation XML and merged version.

| File | Content |
|---|---|
| `<Name>.txt` | base text, UTF-8, NFC |
| `<Name>_merged.txt` | text with inserted annotation markers `[[CODE::Label]] … [[/CODE]]` |
| `annotationcollections/<Name>.xml` | TEI standoff annotations (CATMA export) |

Included are:

**Septuagint** (A. Rahlfs, *Septuaginta*, Stuttgart 1935) — Gen 47–50,
Deut 31–34, Josh 23f., 1 Kgs 2, 1 Macc 2:49–70, 2 Macc 6, 2 Macc 7, Tob 14.

**New Testament** (SBL Greek New Testament, CC BY 4.0) — Luke 22:14–39,
John 13–17, Acts 20:17–38

**Ps.-Philo, Liber Antiquitatum Biblicarum** after the printing by Johannes
Sichardus, Basel 1527 (public domain) — LAB 19, LAB 23f., LAB 28, LAB 29,
LAB 33. Folders carry the suffix `_Sichardus`.

> This file is not a critical edition. It was produced for digital text
> analysis and rests on the public-domain Sichardus printing. Obvious
> printing and transcription errors have been corrected, and individual
> readings have been checked against modern scholarly literature. The file
> makes no claim to reproduce the text of a modern critical edition; for
> philological work the authoritative critical editions must be consulted.

**Online Critical Pseudepigrapha** (CC BY 4.0) — four texts, each in the version
of the electronic edition published there:

| Text | OCP file, column | Basis |
|---|---|---|
| Testamentum Abrahae, rec. A | `TAbA.xml`, «Evans» | M. R. James, TS II.2, 1892; reprinted in M. E. Stone (ed.), SBLTT 2, Missoula 1972, 2–84 |
| Testamentum Abrahae, rec. B | `TAbB.xml`, «Evans» | ibid. |
| Testamentum Iobi | `TJob.xml`, **column «P»** | diplomatic transcription of the manuscript Paris, BN gr. 2658 |
| Testamentum Mosis / Assumptio Mosis | `Mois.xml`, «Ceriani» | A. M. Ceriani, *Fragmenta Assumptionis Mosis*, Monumenta sacra et profana 1, Milan 1861, 55–64 |

For the Testamentum Iobi the column matters: this is the manuscript
transcription, **not** Brock's eclectic text (PVTG 2, 1967) and not that of
James (1897).

## B_Annotations-Only — 17 text versions

Here the annotations are published, the base text is not. The XML files contain
**no text**, only character offsets, tag definitions and metadata. Two groups:

| Group | Texts | Reason |
|---|---:|---|
| `TestXII*` | 12 | de Jonge's edition (PVTG I/2, Brill 1978); permission to redistribute not granted. |
| `LAB_*_Harrington` | 5 | Harrington's edition (SC 229, Cerf 1976); permission to redistribute not granted. `A_Full-Text` offers the public-domain Sichardus printing instead. |

| File | Content |
|---|---|
| `<Name>/annotationcollections/<Name>.xml` | TEI standoff annotations |
| `manifest.json` | per text: expected character count, SHA-256, layout file |
| `layout/<Name>.txt` | layout mask (see below) |
| `normalise.py` | character normalisation and verification |
| `rebuild_corpus.py` | produces the merged version |

## C_CATMA-Import — the same 21 text versions, ready for CATMA

The twenty-one text versions of `A_Full-Text` once more, in the folder form
that CATMA expects on import, and without the merged files:

```
<Name>/<Name>.txt
<Name>/annotationcollections/<Name>.xml
```

CATMA has no import for entire projects: the archive it produces on export
cannot be read back in. Each text is added on its own, in two steps, in the
Project module:

1. Plus icon on the *Documents & Annotations* tile, then *Add Document*, and
   upload `<Name>/<Name>.txt`.

   In step 2 of the wizard, **set the character set to UTF-8**. CATMA guesses
   the encoding and settles on ISO-8859-1 for these files. The annotations are
   anchored to character offsets, so a wrong encoding shifts every one of them
   in the Greek texts.

2. Select the document, then *Import a Collection* from the three-dot menu of
   the same tile, and upload `<Name>/annotationcollections/<Name>.xml`.

   CATMA asks whether to import the tagset *Generic traits* alongside. Confirm;
   without it the annotations have no tags to refer to.

Adding the document creates an empty collection of its own, named
"… Default Annotations". It can be deleted; the imported collection is the one
that carries the annotations.

The layout above is the one CATMA's own export produces, so the files are
already in the shape the import expects.

The seventeen versions of `B_Annotations-Only` are **not** part of this folder,
since their base text is not distributed. To view those in CATMA, first
reconstruct the text as described in the next section; the result then has the
same shape as a folder here.

---

## Producing the texts without a base text yourself

**1. Obtain the text.**

*For the twelve Testaments of the Twelve Patriarchs* — from the edition:

> M. de Jonge (ed.), *The Testaments of the Twelve Patriarchs: A Critical Edition
> of the Greek Text* (Pseudepigrapha Veteris Testamenti Graece I/2),
> Leiden: Brill 1978, 1–180.

*For the five Ps.-Philo texts* — from the edition:

> D. J. Harrington et al. (eds.), *Pseudo-Philon, Les Antiquités Bibliques*
> (Sources chrétiennes 229), Paris: Cerf 1976.

Take each of the seventeen texts as a plain Unicode file, one per work. How you
obtain the text from the edition is your own affair; if you draw on a licensed
database, please observe its terms.

**2. Place the files** under the name given in `manifest.json`:

```
B_Annotations-Only/TestXIIRub/TestXIIRub.txt
B_Annotations-Only/LAB_19_[Ps.-Philon LAB 19_1–16_(Testament_of_Mose)]/LAB_19_….txt
…
```

**3. Establish the layout.** One line per chapter containing the chapter number,
below it one line per verse beginning with the verse number, a period and a
space. For the Testaments of the Twelve Patriarchs a title line comes first, and
between two chapters there is **exactly one** empty line — not before the first.
No indentation, no trailing whitespace, line endings LF, the file ending in a
single newline.

```
ΔΙΑΘΗΚΗ ΡΟΥΒΗΜ ΠΕΡΙ ΕΝΝΟΙΩΝ
I
1. Ἀντίγραφον διαθήκης Ῥουβὴμ ὅσα ἐνετείλατο …
2. Μετὰ ἔτη δύο τῆς τελευτῆς Ἰωσήφ, …

II
1. Καὶ νῦν ἀκούσατέ μου, τέκνα, …
```

This can be checked character by character against the **layout mask** in
`layout/<Name>.txt`. There every text character is replaced by `·`; whitespace,
line structure and chapter/verse numbers stand exactly as they must:

```
······· ······ ···· ·······
I
1. ·········· ········ ······ ··· ·········· ···· ····· ······ ···· ·········
```

**4. Normalise and verify.**

```
python3 normalise.py . --apply
```

The script converts NBSP to space, OXIA to TONOS, ano teleia to middle dot, and
normalises to NFC — pure character substitutions, no intervention in the text.
It then compares the SHA-256 checksum against `manifest.json`. If it matches,
you have exactly the version to which the offsets refer. If it does not, the
script uses the layout mask to show where the problem lies:

```
   -> DIVERGES. Expected: 2c062266a62735e6…
      difference in length: 12 characters.
      layout comparison against TestXIIRub.txt: 75 lines, 81 expected
      line    5: indentation 4 instead of 0 spaces
      line    9: marker «» instead of «7.»
      line   24: missing        «»  (reference line 24)
```

**5. Merge.**

```
python3 rebuild_corpus.py .            # verify and build
python3 rebuild_corpus.py . --check    # verify only
```

This produces the `_merged.txt` for each text with the annotation markers
inserted. The `.txt` and the `.xml` can also be imported directly into CATMA.

---

## Ps.-Philo in two versions

Annotation was originally carried out on Harrington's edition (SC 229, 1976).
**As a text file, only the Sichardus printing of 1527 is published here**, with
the annotations transferred onto it. Harrington's base text is not contained in
this package; where it is quoted below, this is done as a citation of variant
readings.

In addition, the **annotations on Harrington's text** are supplied, in
`B_Annotations-Only/LAB_*_Harrington`. They are the original record and thus the
actual scholarly contribution; anyone working with SC 229 should be able to use
them without having to fall back on the Sichardus version. They consist solely
of character offsets and tag definitions and disclose nothing of the text
itself.

That the transfer onto Sichardus is philologically sound has been verified:
Sichardus and Harrington offer the same text in differing orthography, not
different recensions. Word agreement stands at **96.1 %**; all 238 annotations
could be transferred.
One substantive divergence is to be noted: LAB 23:1 reads `Eleazar uero filius
Naue` in Sichardus where Harrington offers `Ihesus autem filius Nave`.

---

## Why no public-domain substitute was used for the TestXII

For the twelve testaments a public-domain edition exists in R. H. Charles, *The
Greek Versions of the Testaments of the Twelve Patriarchs* (Oxford: Clarendon
1908), which would circumvent the licensing obstacle. It was examined and
rejected.

Charles places the **α recension** in the main text; de Jonge offers the **β
version**, on which the annotation here was carried out. These are not two
editions of the same text but two textual forms. The gain in licensing terms would be bought
with a scholarly loss that cannot be justified. The annotations of these twelve
texts are therefore published without a base text.

---

## On the textual basis

The base texts are **not critical editions** and make no claim to replace one.
They have been prepared for digital text analysis. For philological work the authoritative critical editions are to be consulted.

---

## Software used

Annotation was carried out with CATMA version 7.3.1 (app.catma.de).

> Gius, Evelyn, Meister, Jan Christoph, Meister, Malte, von Detten, Immanuel,
> Petris, Marco, & Messner, Stefanie (2026). *CATMA* (Version 7.3.0)
> [Software]. Zenodo. https://doi.org/10.5281/zenodo.1470118

The Python scripts in this package (`normalise.py`, `rebuild_corpus.py`) were
drafted with the assistance of Claude Code (Anthropic) and reviewed and tested
by the authors. The annotations themselves were made by hand; no language model
was involved in assigning, revising or checking them.

---

## Licence

- **Annotations** (all `.xml`, the tagsets, `manifest.json`, `layout/`): CC BY 4.0
  — full text in `LICENSE`
- **Scripts**: MIT — full text in `LICENSE-scripts`
- **Base texts in `A_Full-Text`**: public domain or CC BY 4.0. The editions are
  named above; their term of protection under § 70 UrhG has expired in every
  case — Rahlfs 1935 (since 1960), Sichardus 1527, Ceriani 1861,
  James 1892/1897.

When redistributing, the attributions of the incorporated texts must be retained:

- **SBL Greek New Testament** (CC BY 4.0) for the three New Testament texts.
- **Online Critical Pseudepigrapha** (CC BY 4.0) for Testamentum Abrahae A and B,
  Testamentum Iobi and Testamentum Mosis:
  > Ian W. Scott and Ken M. Penner (eds.), *The Online Critical Pseudepigrapha*,
  > Atlanta: Society of Biblical Literature / pseudepigrapha.org. Testamentum
  > Abrahae A and B in the transcription of Craig A. Evans.

## Citation

> Joel Klenk, Charlott Buschatz, Arne Käfer, Timotheus Chang-whae Kim,
> Adele-Nike Nehlsen, Anne Maria Rath and Stefanie Steichele, *Annotated Corpus
> of Ancient Testamentary Literature*, version 1 (preliminary),
> University of Tübingen, 2026. DOI: [to be added on publication]

`CITATION.txt` holds the same reference as plain text, with BibTeX and RIS
for reference managers. `CITATION.cff` holds it in machine-readable form;
Zenodo and GitHub read that file automatically.

## Contact

Joel Klenk, University of Tübingen — joel.klenk@uni-tuebingen.de
(corresponding author; for the full list of authors see `CITATION.cff`)
