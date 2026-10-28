# License Applicability


This document maps repository material to the two license families established
by Accepted ADR-0004 and the repository license files. It is explanatory
licensing metadata, not a third license and not normative GeesNO.Semantic
semantics.

## License texts

- `LICENSE-SPECIFICATION` contains the official Creative Commons Attribution
  4.0 International legal code (CC BY 4.0).
- `LICENSE-CODE` contains the official Apache License, Version 2.0, January
  2004 (Apache-2.0).

The local files preserve the official texts without project-specific clauses.
Explanations in this file do not alter either license.

## Functional rule

Licensing follows the function of material, not merely its file extension or
directory name:

```text
human-readable specification, explanation or documentation example
=> CC BY 4.0

schema, source code, test, conformance fixture, tooling, configuration or
machine-readable implementation artifact
=> Apache-2.0
```

When a directory contains both functions, each item follows the applicable row
below. A file is not relicensed merely because it is adjacent to material under
the other license.

## Applicability map

| Material | Function | License |
| --- | --- | --- |
| `README.md`, `ARCHITECTURE.md`, `ROADMAP.md`, `CHANGELOG.md`, `GOVERNANCE.md`, `CONTRIBUTING.md`, `SECURITY.md`, `TRADEMARKS.md`, `PUBLIC_PREVIEW.md`, this map and other human-readable root governance/explanation | Specification, governance or explanation | CC BY 4.0 |
| `adr/**/*.md` | Human-readable architecture decisions | CC BY 4.0 |
| `spec/**/*.md` and `docs/**` human-readable material | Specification or explanation | CC BY 4.0 |
| `examples/**` | Current explanatory, synthetic documentation examples, including their JSON data | CC BY 4.0 |
| `schema/**/*.json` | Machine-readable schema | Apache-2.0 |
| `sdk/**` source and tests | Reference source code and tests; the SDK remains non-normative | Apache-2.0 |
| `conformance/**` | Runner, machine-readable fixtures and expected results | Apache-2.0 |
| `tools/**` | Validation, benchmark and repository tooling plus tests | Apache-2.0 |
| `.github/**`, `requirements-conformance.txt`, `.editorconfig`, `.gitattributes`, `.gitignore` and equivalent repository automation/configuration | Operational implementation material | Apache-2.0 |
| `benchmarks/**` machine-readable recipes, sources and expected artifacts | Reproducible implementation/conformance evidence | Apache-2.0 |
| `benchmarks/**/README.md` and other human-readable benchmark explanation | Explanatory documentation | CC BY 4.0 |

## Mixed directories

### Profiles

`profiles/**` is intentionally mixed:

- human-readable Profile READMEs and explanatory documentation are CC BY 4.0;
- machine-readable Profile artifacts, including
  `profiles/ai-context/v0.1/profile.json`, are Apache-2.0;
- Profile and assessment schemas are Apache-2.0;
- Profile/assessment conformance fixtures and expected artifacts are
  Apache-2.0; and
- Profile validation tooling remains Apache-2.0 under `tools/**`.

Profile binding specifications under `spec/**` are human-readable
specification material and therefore CC BY 4.0. This allocation changes no
Profile identity, authority or semantics.

### Vocabularies

Current `vocab/**` content is human-readable Vocabulary specification or
analysis and is CC BY 4.0. Any future machine-readable Vocabulary artifact
treated as an implementation artifact is Apache-2.0. This is an editorial
license boundary, not Vocabulary semantics.

### Examples and fixtures

An explanatory example under `examples/**` is CC BY 4.0. A fixture, test input
or expected result under a conformance or test corpus is Apache-2.0, even when
both happen to use JSON. The current S4 benchmark machine-readable evidence is
Apache-2.0; its explanatory README is CC BY 4.0.

## Files with a special role

- `LICENSE-SPECIFICATION` and `LICENSE-CODE` are the unmodified official legal
  texts and are not remapped by this document.
- `NOTICE` is informational. No third-party attribution or
  NOTICE obligation was identified in the distributed material; `NOTICE` does not create one.
- Git history and authorship metadata are not reassigned or rewritten by this
  map.

## Attribution boundary

Attribution for CC BY 4.0 material must follow section 3(a) of the official
license, including retained attribution information supplied with the material,
the CC BY 4.0 notice/link and an indication of modifications where applicable.
This document adds no separate attribution condition.

```text
Work: GeesNO.Semantic
Licensor / CC BY attribution: GENARO ESCUDERO NOGALES
Copyright: Copyright 2026 GENARO ESCUDERO NOGALES
```

These attribution statements do not alter the official license texts or imply a separate organization,
company or copyright transfer.

## Third-party material

The distributed material contains no vendored third-party source, copied schema,
external fixture, asset, retained third-party license, copyright header or SPDX
notice requiring propagation. `requirements-conformance.txt` names external
Python dependencies but does not vendor them. The retired SCC material is not
present and is not redistributed.

Any future material with unclear origin or license is a publication blocker;
it must not be assigned CC BY 4.0 or Apache-2.0 by assumption.

## Reserved rights and publication

Neither CC BY 4.0 nor Apache-2.0 grants rights in the `GeesNO` or
`GeesNO.Semantic` names, logos, visual identity, or future official
conformance/certification marks except as the applicable law or license may
otherwise require. See `PUBLIC_PREVIEW.md` for the minimum preview claim
boundary. A mature trademark policy remains deferred.

```text
Public Preview 0.1.0-preview.1 - planned release; not yet finalized
```
