# S2 invalid-case coverage catalogue

**Status: ACCEPTED S2 BEHAVIOR CATALOGUE; EXECUTABLE BARE-CORE COVERAGE LIVES UNDER `conformance/`**

These cases describe what accepted ADR-0009–0016 require rejecting or
classifying separately. The paired machine-readable fixtures under
`conformance/invalid/` and `conformance/expected/` are loaded by the runner and
provide the executable baseline coverage for cases deterministically decidable
from one bare-core document. Processor-contract and future vocabulary/profile
cases remain labelled behavior requirements rather than fabricated input
invalidity.

| Case | Normative reason for rejection | Governing decision/proposal |
| --- | --- | --- |
| UTF-8 BOM | Normative 0.1 input has one BOM-free UTF-8 envelope. | ADR-0016 |
| Malformed UTF-8 or non-scalar decoded content | Whole-document Unicode interoperability fails. | ADR-0012/0016 |
| Lone/reversed escaped surrogate | The decoded string is not a Unicode scalar sequence. | ADR-0012/0016 |
| Non-object JSON root | A SemanticDocument must be exactly one JSON object. | ADR-0016 |
| Missing `spec_version` | Document contract/version is unknown. | ADR-0015 |
| Malformed `spec_version` | No valid exact contract identifier is declared. | ADR-0015 |
| Well-formed but unsupported `spec_version` | Unsupported-version outcome; another version's schema must not be substituted. | ADR-0015 |
| Missing document ID | SemanticDocument lacks stable identity. | ADR-0009 |
| Duplicate ID anywhere in document | Document-wide reference equality is ambiguous. | ADR-0009 |
| Array index/JSON Pointer used as semantic ID | Position is not stable identity. | ADR-0009 |
| Broken `in-document` reference | A target expected in a closed current graph fails to resolve exactly once. | ADR-0009 |
| Omitted target marked `in-document` | The target required by the local expectation does not resolve exactly once. Local availability never makes `out-of-document` invalid. | ADR-0009/0014 |
| Reference object containing conflicting location expectations | Target-location expectation is ambiguous. | ADR-0009 |
| Undeclared namespace prefix | Qualified term cannot expand. | ADR-0010 |
| Prefix rebound or duplicate namespace alias | Canonical expansion is ambiguous. | ADR-0010 |
| Malformed qualified term | Vocabulary identity/local term cannot be separated. | ADR-0010 |
| Assertion embedded in Entity | Violates canonical placement. | ADR-0011 |
| Same assertion inline and global | Two normative forms claim one meaning. | ADR-0011 |
| Assertion without ID | Stable review/lifecycle target is unavailable. | ADR-0011 |
| Same assertion ID assigned different claim bodies | One stable record identity denotes incompatible claims. | ADR-0009/0011 |
| Type/Property/Relation without required Entity subject | The claim has no explicit subject after global placement. | ADR-0011 |
| `in-document` assertion subject unresolved or duplicated | The required local Entity target does not resolve exactly once. | ADR-0009/0011 |
| Property with both `value` and `condition`, or with neither | The category claim body is ambiguous or missing. | ADR-0011/0012 |
| Relation duplicated in reverse endpoint placement | Duplicate/ambiguous claim. | ADR-0011 |
| Singular `concept_id` shortcut | Violates many-to-many association model. | ADR-0011 |
| Association encoded as both Relation and dedicated category | Competing canonical representations. | ADR-0011 |
| Trust record independently referenced, reviewed or lifecycle-targeted without ID | Stable semantic addressability is required for the independent target; purely scoped nested trust metadata may remain anonymous. | ADR-0011/0014 |
| Property containing raw JSON number/array/object | Canonical hybrid value contract is bypassed; only native string/boolean are direct values. | ADR-0012 |
| Property containing JSON `null` as unknown/redacted | Semantic conditions are collapsed. | ADR-0012 |
| Redacted condition accompanied by source/display spelling or an equivalent raw value | Auxiliary metadata reconstructs content that the condition says is hidden. | ADR-0012 |
| Decimal coefficient/exponent or integer with non-canonical string | Cross-language exactness or unique numeric form is lost. | ADR-0012 |
| Canonical measured quantity without unit | Exchange would depend on silently inferred profile/source context. | ADR-0012 |
| Set containing duplicate semantic values | Set semantics are violated. | ADR-0012 |
| Structured value with unqualified structure/field | Domain meaning can collide. | ADR-0010/0012 |
| Source without ID | Separately referenceable origin context lacks ADR-0009 identity. | ADR-0013 |
| Binding without ID | Correlation cannot retain stable correction/review/lifecycle identity. | ADR-0013 |
| Binding without Entity reference | Accepted Binding cardinality is violated. | ADR-0013 |
| Binding without Source reference | Locator lacks Source context. | ADR-0013 |
| Binding locator value without qualified kind, or kind without value | Consumer cannot identify and interpret one complete locator. | ADR-0013 |
| Binding locator encoded as raw arbitrary JSON | Canonical ADR-0012 value boundary is bypassed. | ADR-0012/0013 |
| Source location/revision descriptor with undeclared kind | Qualified descriptor cannot be expanded. | ADR-0010/0013 |
| Fingerprint without separate algorithm and value | Digest semantics and lexical content are conflated. | ADR-0013 |
| Duplicate Binding ID | Document-wide correlation identity is ambiguous. | ADR-0009/0013 |
| Same Binding ID reused for a different occurrence | One ID no longer denotes continuity of one specific correlation, even if Entity/Source/locator values match. | ADR-0013/0014 |
| Product-specific field required by core Binding | Universal serialization acquires domain bias. | ADR-0013 |
| `complete` scope without qualified definition | The boundary over which absence is claimed is not explicitly declared. | ADR-0014 |
| Revision descriptor without ID | An explicit lineage node is not addressable. | ADR-0009/0014 |
| Repeated target in Revision `parents`, Provenance `sources`, Change `targets` or `supersedes` | ADR-0016 defines target uniqueness for each of these specific unordered Reference-array roles. | ADR-0016 |
| Revision parent cycle in declared closed graph | Lineage is structurally incoherent. | ADR-0014 |
| Change target marked `in-document` but absent from a closed graph | History target integrity fails; `unresolved` remains a processing observation. | ADR-0014 |
| Change contains executable command/JSON Patch | Lifecycle becomes execution/replay. | ADR-0014 |
| Change placed outside `history` | A second lifecycle placement/dialect is introduced. | ADR-0014 |
| Cited, reviewed, ordered, deduplicated, corrected or superseded Change without ID | Portable Change addressability/continuity is unavailable. | ADR-0007/0009/0014 |
| Change silently contradicts same scope/Revision state | Invalid only when an applicable known vocabulary/profile makes the Change effect locally decidable; unknown qualified Change meaning is not inferred by bare core. | ADR-0014/0016 |
| Missing record treated as tombstoned in partial/unknown scope | Absence is incorrectly treated as deletion. | ADR-0014 |
| Tombstone without its own ID, target or target category | Standalone withdrawal identity or preserved target meaning is missing. | ADR-0009/0014 |
| Live current target and Tombstone for that target in the same scope/Revision | Current state makes contradictory lifecycle claims. | ADR-0014 |
| Tombstoned ID assigned to a different subject | Historical identity is corrupted when continuity is locally evidenced; cross-document continuity remains externally unverifiable. | ADR-0014 |
| Self/cyclic supersession in declared closed graph | Directed lifecycle graph is incoherent. | ADR-0014 |
| Locally comparable validity end before start | The declared interval is incoherent. | ADR-0012/0014 |
| Unknown member inside closed core object | Likely typo/hidden dialect. | ADR-0015 |
| Qualified-looking member placed outside `extensions` | The explicit Extension boundary is bypassed. | ADR-0015 |
| `extensions` on a helper object outside the accepted host matrix | Extensibility is not ubiquitous across every JSON object. | ADR-0015 |
| Extension key not qualified | Collision-safe Extension identity is absent. | ADR-0010/0015 |
| Extension key with undeclared prefix | Absolute Extension term identity cannot be expanded. | ADR-0010/0015 |
| Duplicate Extension term on one host after expansion | One Extension identity has ambiguous payload. | ADR-0010/0015 |
| Extension attempts to override core `id` or cardinality | Extension redefines core semantics. | ADR-0015 |
| Executable Extension semantics | Foundation security boundary is violated. | ADR-0015/0016 |
| Lossless processor rewrites `1`, `1.0`, `1e0` or `1E+0` inside an unknown Extension | Unknown-contract numeric information is lost. | ADR-0015/0016 |
| Lossless processor rewrites Extension `-0` as `0` | Unknown-contract sign information is lost. | ADR-0015/0016 |
| Extension number rounded, truncated, overflowed or converted to infinity | Host-language numeric loss violates the preservation contract. | ADR-0015/0016 |
| Empty optional core collection, namespace map or `extensions` map | Optional zero-entry containers must be omitted. | ADR-0016 |
| Optional core member serialized as `null` | Absence uses omission; core `null` is not a shorthand. | ADR-0012/0016 |
| Reordered `list.items` treated as the same value | List order is semantic. | ADR-0012/0016 |
| Reordered Extension payload array treated as the same payload | Opaque array order is preserved. | ADR-0015/0016 |
| Duplicate JSON object member name | Parser interpretation is non-deterministic. | ADR-0016 |
| Duplicate member inside arbitrary Extension payload | Opacity does not legalize duplicate members. | ADR-0015/0016 |
| Validator requires schema/vocabulary network access | Offline deterministic processing is violated. | Foundation/ADR-0016 |
| Well-formed input exceeds a defensive implementation limit | Resource refusal must not be reported as semantic invalidity where distinguishable. | ADR-0016 |

## Semantically contentious but not structurally invalid

The baseline must not reject data merely because it contains competing
assertions, several Revision parents, conflicting Reviews, low Confidence,
multiple directed replacements or claims from different authorities. Syntax and
reference integrity do not decide truth.

Two assertions with different IDs and identical claim bodies are likewise not
a structural error. They may be independent claims with different Provenance or
a semantic duplicate; canonical processing does not merge them by content.

Likewise, an ID-only Source, an unreachable Source, a Binding without locator,
multiple locations and distinct Binding IDs with the same Entity/Source/locator
are not structural errors under accepted ADR-0013. Stale locator, Source
unavailability and processor resolution diagnostics are separate lifecycle or
processing concerns.

Under accepted ADR-0014, current Revision without history, zero or
multiple Revision parents, partial history, restoration of the same subject,
multiple superseders and a simple nested Review without ID are likewise
valid. A `complete` claim with an uninterpretable qualified scope remains
structurally preservable but permits no portable bare-core absence inference.
Complete history need not embed prior bodies/snapshots and never enables
replay. An out-of-document parent can be structurally valid while its
existence or remote cycles remain externally unverifiable. If the same target
identity is materialized locally, that availability permits locally decidable
category, kind, self-edge, Tombstone and closed-cycle checks; it does not change
the reference's location expectation or make the reference invalid by itself.

Under accepted ADR-0015, arbitrary JSON—including raw numbers and `null`—is
valid inside a well-placed qualified Extension but not in an ADR-0012 core
value slot. A semantically unknown Extension is valid
for bare core unless an applicable profile requires understanding. A lossless
tool dropping it violates the tool's preservation contract; an explicitly
lossy projection may report the omission without making the input invalid.

Under accepted ADR-0016, a lossless unknown-Extension round trip also
retains each exact numeric token, while object ordering and string escape
spelling need not be preserved. Root record collections, Revision parents,
trust arrays and supersession targets are unordered; list and Extension-array
order is semantic, and set order is not. Unordered Reference arrays are not
implicitly duplicate-free: target uniqueness is enforced only where ADR-0016
expressly specifies it—Revision `parents`, Provenance `sources`, Change
`targets` and `supersedes`. Recursive set duplicate equality is a deterministic
semantic-integrity check rather than a schema-only check.

## Fixture status

All governing ADRs are Accepted and the deterministic suite implements the
approved S2 bare-core baseline across Layers 0–3. Same-stem expected JSON files, not prose
wording, define the runner's expected outcome/layer classifications. Lossless
processor behavior is additionally exercised by focused unit tests. Cases that
require remote evidence or future qualified vocabulary/profile meaning remain
externally unverifiable or profile-dependent, not generic invalid fixtures.
Explicit human closure approval on 2026-09-10 completes S2. Public `0.1.0`
remains unreleased.
