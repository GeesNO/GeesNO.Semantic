# ADR-0010: Qualified-term and namespace model

- **Status:** Accepted
- **Date:** 2026-09-01
- **Accepted by:** Explicit human architecture decision on 2026-09-01
- **Decision order:** After accepted ADR-0009

## Context

GeesNO.Semantic needs collision-free identifiers for type/classification terms,
properties, relation predicates, locator kinds, Extension keys, provenance
mechanisms and other vocabulary-defined meanings. These terms identify semantic
vocabulary meaning, not ADR-0009 records:

```text
semantic record ID != qualified semantic term
```

The mechanism must remain compact, deterministic offline, domain- and
vendor-neutral, and usable without registry lookup, dereference, ontology
download or dependency resolution.

## Alternatives considered

1. **Full absolute term IRIs at every occurrence.** Unambiguous, but verbose
   and expensive when repeated.
2. **Compact terms without canonical expansion semantics.** Readable, but
   makes aliases and cross-document equality ambiguous.
3. **One compact serialized form with deterministic absolute expansion.**
   Compact spelling remains document-local while expanded identity controls
   semantic comparison.
4. **Both compact and absolute occurrence forms.** Convenient, but creates two
   normative spellings for one term.

## Decision

Adopt Alternative 3.

Every qualified-term slot uses exactly one compact `prefix:local` serialized
form. An absolute IRI is not admitted as a second equivalent spelling in such a
slot. Every used prefix is declared by the SemanticDocument, and direct
deterministic expansion produces one absolute term IRI.

The prefix is a document-local alias and never participates in term identity.
Consumers compare the expanded absolute term IRIs using the accepted exact
identifier comparison rules. Labels, vocabulary versions and availability of
vocabulary definitions do not alter equality.

The same mechanism applies to types, properties, predicates, locator kinds,
Extension keys and other qualified semantic terms. ADR-0012 separately decides
whether unit and domain-datatype identities use it.

## Three concepts that must remain separate

### Namespace / term-expansion base

The expansion base is the absolute IRI stem used by the mechanical operation:

```text
prefix
  -> declared expansion base IRI
  + local
  -> absolute term IRI
```

Expansion is direct concatenation. No `/`, `#`, case conversion, Unicode
normalization, percent-decoding or other separator/normalization is inserted.
The owner chooses a base whose final delimiter, if any, produces the intended
term IRI. No network access is required.

### Vocabulary identity

Vocabulary identity identifies a vocabulary resource or conceptual vocabulary.
It is optional S2 metadata and is not necessarily the term-expansion base. A
vocabulary may use one IRI for itself and another IRI stem for its terms.

Term identity is never computed as `vocabulary identity + local` unless the
vocabulary itself deliberately chose that IRI design and exposed the same value
as its expansion base.

### Vocabulary version

Vocabulary version is separate optional metadata. It describes an edition or
interpretation context and never silently modifies an already expanded term
IRI. A vocabulary owner can make versions identity-significant by assigning
different term IRIs or expansion bases, not by relying on hidden parser logic.

## Minimal S2 namespace declaration

The universal S2 responsibility is only unambiguous term expansion. Therefore
the minimum namespace-map entry associates:

```text
prefix -> absolute expansion base IRI
```

Vocabulary identity, vocabulary version, labels, fingerprints and discovery
metadata are optional and may be developed further in S3. If present, they do
not replace the expansion base and do not participate silently in term
identity.

The namespace map is required and non-empty when any compact term occurs. It
may be absent or empty when none occurs. Unused declarations are mechanically
valid for reusable contexts, although compact producers should omit them and a
profile may impose a stricter rule.

## Canonical term identity

```text
serialized spelling != semantic term identity
```

For example, `str:column` in one document and `s:column` in another denote the
same term if and only if their declarations expand them to the same canonical
absolute term IRI. Prefix selection and human labels are irrelevant to
equality.

Within one SemanticDocument, a single expansion base cannot be assigned to
multiple prefixes. Such aliases are invalid because they create unnecessary
equivalent spellings, internal dialects and validation complexity. A prefix
also cannot be rebound or left undeclared.

Different documents may choose different prefixes for the same expansion base.
There is no mandatory global prefix registry or canonical-prefix selection
algorithm. Byte-level canonicalization of one document and semantic equivalence
between independently prefixed documents are distinct ADR-0016 concerns.

## Lexical direction

S2 0.1 should use an ASCII-safe, non-empty and deterministically parseable
prefix/local spelling. Prefix comparison is case-sensitive, and a producer must
emit the one spelling declared by its document. This ADR does not freeze an
unjustified regular expression, maximum lengths or a future Unicode escaping
and internationalization mechanism.

The final lexical grammar must prevent an absolute IRI from being mistaken for
a compact term and must make the structural colon unambiguous. Raw Unicode
local spellings are not assumed valid until that subordinate policy is
approved.

## Unknown vocabularies and offline behavior

```text
unknown vocabulary + declared expansion base = processable qualified terms
```

A consumer can parse, preserve, expand and compare such terms without knowing
their domain meaning. Unknown meaning may affect profile-level interpretation,
but not the core mechanics. Namespace, vocabulary and term IRIs are never
automatically dereferenced, and no registry determines core validity.

## Vocabulary-version conflicts

If two documents expand a term to the same absolute IRI while reporting
different vocabulary identity/version metadata, they still carry the same term
identity. The metadata can represent a vocabulary, profile or semantic conflict
but is not necessarily a syntax error. S2 parsers report/preserve it and do not
act as dependency resolvers. S3 may add vocabulary-specific rules.

## Extension and locator interaction

Extension keys use the same qualified-term expansion rules. An unknown
Extension vocabulary is mechanically valid when its prefix and expansion base
are declared; its payload remains inert and cannot redefine core semantics.
Nested Extension preservation and placement remain ADR-0015 work.

Locator kinds also use the mechanism without a universal domain enum.
`pdf:region`, `sheet:range` and `code:symbol` are non-normative examples only;
they create no mandatory base-vocabulary terms.

## Unit and datatype compatibility

Fundamental serialization datatypes may use closed core tokens. External or
domain datatype identities may use qualified terms. ADR-0012 decides the unit
and datatype boundary; ADR-0010 supplies compatibility without forcing every
datatype through a vocabulary.

## Cross-domain evidence

Engineering, spreadsheet/business, legal/document, software, scientific and
product vocabularies can all declare a local term such as `status` under
different expansion bases without collision. Third-party Extension keys and
locator kinds use the same rule. No domain concept or adapter enters the core.

## Adversarial results

| Case | Accepted result |
| --- | --- |
| Same local spelling under different expansion bases | Valid; different terms. |
| Same expansion base under two prefixes in one document | Invalid alias. |
| Different prefixes for the same expansion base across documents | Valid; compare expanded term IRIs. |
| Undeclared prefix | Invalid. |
| Prefix duplicated or rebound | Invalid. |
| Full absolute IRI in a qualified-term slot | Invalid alternate spelling. |
| Unknown vocabulary with declared expansion base | Mechanically valid; meaning may be profile-dependent. |
| Vocabulary definition cannot be dereferenced | Valid; dereference is irrelevant. |
| Same expanded term with different vocabulary-version metadata | Same term identity; possible semantic/profile conflict. |
| Raw Unicode local spelling | Not assumed valid; lexical/escaping policy remains open. |
| Prefixes differing only by case | Compared case-sensitively; same-base aliases remain invalid and exact admission awaits the lexical grammar. |

## Consequences

- Terms are compact in JSON while retaining globally comparable absolute
  semantic identity.
- S2 namespace declarations stay minimal and do not become vocabulary records.
- Consumers must expand before semantic comparison.
- Prefix spelling can differ between documents but cannot alias one base within
  a document.
- Vocabulary identity and version metadata never become hidden inputs to term
  equality.
- Unknown vocabularies remain processable offline.
- ADR-0016 must distinguish byte canonicalization from cross-document semantic
  equivalence.

## Remains open

- exact ASCII-safe prefix/local grammar and maximum lengths;
- future Unicode escaping/admission and internationalization policy;
- exact JSON names/shape for namespace declarations and optional vocabulary
  metadata;
- vocabulary-identity and version lexical forms and profile compatibility rules;
- optional labels, fingerprints and discovery metadata, primarily S3 work;
- any future GeesNO base-vocabulary namespace/preferred prefix;
- ADR-0012 unit and domain-datatype choices;
- ADR-0015 Extension placement/preservation;
- ADR-0016 byte-level canonical JSON processing.
