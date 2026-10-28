# SCC legacy review and retirement record

**Status: NON-NORMATIVE HISTORICAL REVIEW — COMPLETE**  
**Review date:** 2026-08-30  
**Input retired:** `SCC-CAD-Adapter-1.0.zip`

## Controlled inspection

S1 inspected only the archived README/architecture, the SDK README and document
model, the core/L0/L1/L2 schemas, and the small CAD snapshot model. The review
looked for domain-neutral conceptual lessons; no code was copied and no
compatibility target was created.

The archive implemented a Windows CAD adapter around source-native handles,
geometry/locator extraction, SCC UUIDs, inline classification/property
assertions, first-class relations, a revision counter/change log, tombstones and
a compact-context SDK method.

## Classification

| Legacy element | Classification | Problem it addressed | Still relevant? | Domain bias / S1 conclusion |
| --- | --- | --- | --- | --- |
| Concept / Representation split | `PRESERVE` | Separate logical meaning from a digital occurrence. | Yes, in all six domains. | The distinction is universal and already closed by the Foundation; no SCC implementation detail is preserved. |
| Non-destructive sidecar exposure | `PRESERVE` | Add semantics without rewriting native data. | Yes. | Sidecar is one of three equal exposure patterns; SCC naming/format is not preserved. |
| SCC UUID separate from CAD Handle | `GENERALIZE` | Keep semantic identity stable when native correlation differs. | Yes. | The separation survives; UUID-only syntax and handle-based matching do not. Stable-ID syntax remains OPEN. |
| Source, locator and binding | `GENERALIZE` | Correlate a Representation to native information. | Yes. | SCC required a source on every Representation and used document/application/native-ID plus CAD/document locator fields. S1 replaces this with optional plural Bindings and qualified locator families. |
| Classification and property assertions | `GENERALIZE` | Carry semantic claims with confidence/provenance/review. | Yes. | SCC inline records are evidence for an assertion contract, not a chosen architecture; qualified terms, values, conflict and lifecycle need redesign. |
| First-class relations | `GENERALIZE` | Connect identified entities and attach trust metadata. | Yes. | Universal subject–predicate–object survives; fixed relation types, mandatory relation IDs and placement do not automatically survive. |
| Provenance / confidence / review | `GENERALIZE` | Distinguish origin, certainty and validation. | Yes. | SCC had shallow single records/fixed enums. S1 keeps independent plural scoped capabilities and leaves vocabulary/identity open. |
| Revision counter, change events and tombstones | `GENERALIZE` | Track created/updated/deleted entities and relations. | Yes. | A single integer/event enum is insufficient for cross-domain lineage, assertion changes, validity and partial datasets. ADR-0007 later accepted state-first, history-optional semantics; concrete representation remains OPEN. |
| URN-keyed extension object | `GENERALIZE` | Permit non-core data. | Yes. | Namespaced inert data survives; URN-only syntax and one object shape do not. |
| L0/L1/L2 schemas | `GENERALIZE` | Offer progressive conformance. | Concept remains useful. | SCC L1 accepted geometry as semantic completeness and L2 merely required entities/relations; exact levels are rejected and remain OPEN. |
| Compact-context SDK method | `MOVE_OUTSIDE_CORE` | Reduce data for an LLM consumer. | Yes, as a later project objective. | Projection belongs to the AI Context Profile (S4), not the universal core or S1 implementation. |
| CAD snapshots, COM backend, extractors and native entity catalog | `MOVE_OUTSIDE_CORE` | Read particular applications and geometries. | Not as core mechanics. | Product adapters may exist independently; none belongs in this repository. |
| Geometry, layer, bounding box and native CAD type fields | `REJECT` | Describe CAD occurrences and support matching. | Only in certain domains. | They are never mandatory core content; qualified Representation/Binding data may express equivalents when relevant. |
| Command/classification CLI, synchronization and future action/plugin direction | `REJECT` | Operate the adapter and synchronize software-derived content. | No, for the semantic standard. | Execution, GUI/product control, transactions and adapter runtime are outside GeesNO.Semantic. |
| SCC SDK API, Python classes, schemas and package layout | `NOT_NEEDED` | Implement the former SCC 1.0 contract. | No. | S1 is specification-first, has no SCC compatibility objective and must not let an SDK define semantics. |
| Capability-manifest/action-layer concepts | `NOT_NEEDED` | Describe/control CAD capabilities in the wider predecessor direction. | No. | They are not needed to answer the semantic core question and remain outside the project. |

## General conclusion

SCC contributed no unique concept required by GeesNO.Semantic beyond ideas
already independently mandated by `PROJECT_FOUNDATION.md`. The inspection helped
identify failure modes—mandatory source on Representation, domain-shaped
locators, geometry as L1 evidence, shallow trust records and a simplistic
revision counter—but no archived schema, API, code or compatibility rule should
be reused.

The archive's historical-input function ended with this review. It was removed
from the workspace after the review and remains named in `.gitignore` only to
prevent accidental reintroduction.

> Future GeesNO.Semantic work no longer depends on SCC legacy material.
