# JSON qualified-term and namespace analysis

**Scope:** Core 0.1 JSON qualified-term and namespace representation.
**Architectural authority:** [ARCHITECTURE.md](../ARCHITECTURE.md), accepted ADR-0010 and ADR-0016.

Qualified terms identify semantic vocabulary meanings, not ADR-0009 records or
external-resource locators.

```text
record ID != qualified term
```

## Accepted compact model

Every qualified-term slot has one `prefix:local` serialized form. An absolute
IRI is not a second occurrence form. The document namespace map expands the
term deterministically:

```text
prefix -> expansion base IRI
expansion base IRI + local -> absolute term IRI
```

Direct concatenation inserts no delimiter or normalization and requires no
network access. The expanded absolute term IRI is semantic identity; prefix
spelling and labels are not.

## Expansion base, vocabulary identity and version

These are three distinct concepts:

- **expansion base:** required mechanical IRI stem for term expansion;
- **vocabulary identity:** optional identity of an associated vocabulary,
  which need not equal its term stem;
- **vocabulary version:** optional edition/interpretation metadata.

The minimum universal Core 0.1 JSON namespace declaration needs only prefix
and absolute expansion base. Vocabulary identity, version, labels,
fingerprints and discovery metadata are separate optional roles governed
by applicable Vocabulary contracts. They never replace the expansion base
or silently alter an expanded term's identity.

Conceptual, non-normative sketch:

```json
{
  "namespaces": {
    "structures": "https://example.org/terms/structures/"
  },
  "term": "structures:column"
}
```

The term expands to `https://example.org/terms/structures/column`, not to
an optional vocabulary resource plus the local. Accepted ADR-0016 defines
the Core 0.1 JSON map as direct `prefix -> expansion-base string`.
Vocabulary identity/version metadata is governed separately.

## Equality and prefixes

`str:column` in one document and `s:column` in another are the same semantic
term if and only if they expand to the same canonical absolute term IRI.
Cross-document comparison expands first.

Within one document:

- every used prefix must be declared once;
- a prefix cannot be rebound;
- one expansion base cannot have multiple prefix aliases;
- duplicate declaration members are invalid.

Across documents, different prefix choices are valid. No central prefix
registry or global prefix-renaming/canonical-selection algorithm is required.
Byte-for-byte JSON canonicalization is not imposed by the Core 0.1 JSON
contract. Semantic equivalence across independently prefixed documents
requires comparison of expanded term IRIs rather than byte equality.

## Namespace-map responsibility

The map is required and non-empty when compact terms occur and can be absent or
empty otherwise. Unused declarations are mechanically valid for reusable
contexts; compact producers should omit them and profiles may be stricter.

Accepted ADR-0016 defines the Core 0.1 JSON ASCII-safe prefix/local grammar,
non-empty components and case-sensitive comparison, with no normative maximum
length. Any broader Unicode internationalization requires an applicable
later-version contract.

## Unknown vocabularies

Unknown vocabulary plus a declared expansion base produces mechanically
processable terms. Consumers can parse, preserve, expand and compare them
without understanding domain meaning. Vocabulary/namespace IRIs are not
automatically dereferenced and no registry is a parsing or conformance
dependency.

Different version metadata for the same expanded term does not create different
term identities. It may be a vocabulary semantic conflict or profile issue;
the parser preserves/reports metadata rather than resolving dependencies.

## Extensions, locators, units and datatypes

Extension keys and locator kinds use the same qualified-term mechanism.
Unknown declared Extensions remain mechanically valid and inert. Non-normative
locator examples include `pdf:region`, `sheet:range` and `code:symbol`.

Accepted ADR-0012 uses qualified terms for unit identity while retaining closed core
tokens for fundamental serialization datatypes. Domain structured datatypes may
also be qualified. ADR-0010 itself does not own unit vocabularies.

## Adversarial classification

| Case | Accepted classification |
| --- | --- |
| Same local term under different bases | Valid, different terms. |
| Same base under two prefixes in one document | Invalid alias. |
| Same base under different prefixes across documents | Valid; expanded terms compare equal. |
| Undeclared/rebound prefix | Invalid. |
| Full absolute IRI in term slot | Invalid alternate spelling. |
| Unknown declared vocabulary | Mechanically valid; meaning may be profile-dependent. |
| Non-dereferenceable namespace | Valid. |
| Same expanded term, different version metadata | Same term identity; possible semantic/profile conflict. |
| Raw Unicode local spelling | Invalid under the accepted Core 0.1 JSON ASCII-safe local grammar. |

## Vocabulary and future-edition boundaries

- Unicode/escaping/internationalization beyond the accepted Core 0.1 JSON
  ASCII-safe grammar requires an applicable later-version contract.
- Accepted ADR-0017 governs Vocabulary identity/version; ADR-0018 covers
  publication; ADR-0019 covers lifecycle; ADR-0020 covers Extension Vocabulary
  authoring/payload compatibility; ADR-0021 covers optional discovery,
  authority and governance.
- Cross-edition compatibility and concrete Vocabulary metadata bindings
  remain distinct from Core namespace expansion and term identity.
- Any base-vocabulary namespace or preferred prefix follows its applicable
  Vocabulary contract; Core does not impose a universal preferred prefix.
- Accepted ADR-0015 and ADR-0016 govern Extension preservation and exact
  raw-token processing. Byte-for-byte JSON canonicalization is not required
  by the Core 0.1 JSON contract.

The accepted qualified-term architecture is recorded in
[ADR-0010](../adr/0010-qualified-term-namespace-model.md).
