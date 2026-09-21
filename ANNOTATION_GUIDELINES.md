# Annotation Guidelines

Rules for the genre annotation of ancient testamentary literature. They
describe the procedure by which the 33 texts of this corpus were annotated,
and they serve as the instruction for any extension of the collection.

---

## 1. Object of annotation

What is annotated is the **generic status of a passage** — not its style, not
its syntax, not its content **as such**. The question put to every passage is:
*which element of the testamentary speech is present here?*

This rests on a **family-resemblance concept of genre**. There is no feature
that every testament must exhibit, and none whose presence alone would
constitute one. The genre consists in a **repertoire** of possible elements
from which individual texts draw differently. The tagset maps this repertoire —
it is not a schema of necessary and sufficient criteria, and it is not to be
read as a checklist.

From this it follows directly that a text lacking an element is not therefore a
lesser representative of the genre. The annotation records what is there and
remains silent about what is not.

---

## 2. The tagset

32 codes on four levels under three roots. The roots do not distinguish by
importance but by kind of feature.

### N — Narrative Setting

The narrative surrounding the speech: who speaks, when, under what
circumstances, and what happens after the speech.

| Code | Label |
|---|---|
| `N` | Narrative Setting |
| `N1` | narrative opening |
| `N1a` | age of death |
| `N1b` | gathering |
| `N1c` | Introduction formula |
| `N2` | narrative closing |
| `N2a` | Closing formula |
| `N2b` | burial details |

### T — Testament (the speech)

The testamentary speech itself and its constituent parts.

| Code | Label |
|---|---|
| `T` | Testament |
| `T1` | retrospection |
| `T2` | eschatological perspective |
| `T2a` | threat/curse/judgement |
| `T2b` | blessing |
| `T2c` | conditioned promise |
| `T3` | Ethical exhortations |
| `T3a` | burial order |
| `T3b` | Great Commandment |
| `T3bα` | Love to God |
| `T3bβ` | Love to men |
| `T3c` | love/hatred |
| `T3d` | marriage/divorce |
| `T3e` | works of mercy |
| `T3f` | purity/impurity |
| `T3g` | Law/tora |
| `T3h` | Own Words/Commandments |
| `T4` | salvatory assertion |

### I — Independent traits

Features not tied to a position in the structure, occurring in the narrative
frame as well as within the speech.

| Code | Label |
|---|---|
| `I` | Independent traits |
| `I1` | (proximity of) death |
| `I2` | addressee(s) |
| `I2a` | inauguration of a successor |
| `I3` | family (relations) |
| `I4` | Speaker |

The three roots `N`, `T` and `I` are both organising categories and usable
codes. In practice `I` is hardly ever applied as a label — the independent
traits are marked directly as `I1` to `I4`.

---

## 3. Exhaustive annotation — and genuine gaps

**The whole text is considered.** What stands out is not selected; the text is
worked through from beginning to end and classified. In the present corpus an
average of 96 % of each text carries an annotation.

**Gaps are permitted and indeed intended** — but only genuine ones. A passage
is left unannotated where the repertoire does not cover it and is not meant to
cover it: material that belongs to the text but is not an element of the
testamentary speech.

---

## 4. Multiple assignment

**A passage may carry several codes.** This is the normal case rather than the
exception, and follows from the structure of the tagset: the independent traits
lie by their nature within the narrative frame or the speech, and one passage
can name an addressee and a family relation at once.

---

## 5. Nesting

**A subtag does not presuppose its super-tag.** `T3g` may be applied without
the same passage additionally carrying `T3` and `T`.

**Where the additional marking carries meaning, it is applied.** It does so
above all where the parent tag establishes a connection that the child tag
alone does not show: the speech as a whole as `T`, the opening section as `N1`,
a continuous exhortation as `T3` within which individual themes are marked
separately.

What is not meaningful is the mechanical addition of every super-tag above
every single annotation. It inflates the annotation without showing anything.

*Note for analysis:* since nesting is not enforced, quantitative analyses must
not assume that every `T3g` passage is also marked as `T3`. Anyone computing on
the superordinate categories should close the hierarchy beforehand.

---

## 6. Procedure

1. **Scheme.** The feature repertoire was developed jointly in advance and
   refined in the course of the work.
2. **First annotation.** The texts were distributed to at least two annotators
   each.
3. **Adjudication.** The annotations were discussed in joint sessions and
   merged into a supra-individual version.
4. **Gold standard.** The published corpus is this unified version. It rests on
   consensus, not on an averaged agreement coefficient.

The tool was CATMA 7.3.1; the citation is given in the README.

---

## 7. Extending the corpus

Anyone annotating further texts according to these rules should follow sections
3 to 6. The tagset is open: a feature missing from the repertoire is a finding,
not a defect of the source.
