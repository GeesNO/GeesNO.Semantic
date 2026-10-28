# Six-domain adversarial review of Universal Core Model 0.1

**Status: NON-NORMATIVE S1 ANALYSIS — synthetic concepts, not adapters**

This review tries to break the model rather than demonstrate only happy paths.
It tests whether every core primitive is universally meaningful, whether its
presence must be mandatory, whether it inherits a domain shape, and whether it
supports partial enrichment.

## Primitive challenge matrix

| Primitive | Meaningful in all six? | Universally available? | Mandatory presence in each document/entity? | Bias / move-out test | Partial-enrichment result |
| --- | --- | --- | --- | --- | --- |
| SemanticDocument | Yes, as dataset boundary. | Yes. | One document envelope; only identity/spec version are intrinsically required. Collections may be empty. | Storage/collection shape cannot be borrowed from files or databases. | Metadata-only or fully redacted document remains possible. |
| Entity | Yes, as identifiable subject. | Yes. | Entity occurrences optional; each occurrence requires identity and kind. | Domain labels/types move to vocabularies. | Identified-but-unclassified Entity is valid. |
| Concept | Yes, logical subject independent of occurrence. | Yes. | No; a dataset may expose only Representations. | Domain categories move to vocabularies. | Can exist with no Representation or Binding. |
| Representation | Yes, digital occurrence. | Yes. | No; a purely conceptual dataset may have none. | Geometry/page/row/path/segment are not core fields. | Can exist with no known Concept or complete Binding. |
| Source | Yes, when traceability exists. | Yes. | No; purely semantic or redacted data may omit it. | Application/format fields are optional descriptions. | Source identity can exist with partial metadata. |
| Binding | Yes as correlation mechanism. | Yes. | No for any Entity class. | Locator families move to qualified vocabulary/profile/extension payloads. | Can be added/corrected later; entity remains valid before it. |
| Type Assertion | Yes. | Yes. | No. | Type terms live in vocabularies. | Zero, multiple or conflicting types are valid. |
| Property Assertion | Yes. | Yes. | No. | Domain properties/datatypes move outside core. | Missing properties are valid; explicit unknown/N/A/redacted remain distinguishable. |
| Relation | Yes. | Yes. | No. | Domain predicates move to vocabularies. | Relations can be added after endpoints exist. |
| Provenance | Yes for traceable/derived claims. | Yes. | Optional content, but important assertions must be able to carry it. | Actor/tool vocabularies cannot privilege one provider. | Can be appended without changing subject identity. |
| Confidence | Yes for inference/uncertainty. | Yes. | No for authoritative content. | Calibration/threshold belongs to profiles/methods. | Low-confidence claims remain representable. |
| Review | Yes where validation occurs. | Yes. | No. | Workflow-specific states/authority move to profiles. | Unreviewed and later-reviewed states coexist through lifecycle. |
| Revision / Change | Yes when data evolves. | Yes. | No history is required for a static occurrence; capability is universal. | Commit/page/drawing revision models cannot define core lifecycle. | Enrichment can occur while stable identity continues. |
| Extensions | Yes as controlled escape hatch. | Yes. | No Extension content is required for bare core. | Domain data belongs here only when vocabulary/profile is insufficient. | Unknown Extensions do not block core use. |

No primitive fails the universal-availability test, but most fail the
mandatory-presence test. This distinction drove the S1 cardinality model.

## 1. Engineering-like object graph

**Counterexamples/problems:** a composite digital object can represent several
logical components; a logical assembly may have no geometry; geometry changes
without changing the Concept; one connection may require n-ary semantics.
Native handles can be recycled or scoped to one source revision.

**Assumptions detected:** one Representation → one Concept, mandatory geometry,
mandatory Binding, native handle as identity and binary Relations sufficient
for every engineering relationship.

**Changes made:** Concept–Representation association became optional `0..*` in
both directions; Binding became optional/plural; geometry stayed outside core;
n-ary semantics remains an explicit open edge case rather than a new primitive.

**Result:** the core describes identity, claims and traceability without a CAD
field. Complex relation patterns need vocabulary/profile testing, not a core
engineering predicate.

## 2. Spreadsheet / table dataset

**Counterexamples/problems:** row numbers move under sorting; blank cells do not
say whether a value is unknown or inapplicable; one row may aggregate multiple
Concepts; a formula value has a derivation chain and can change independently.

**Assumptions detected:** array/row position as identity, every record as exactly
one Concept, generic `null`, and one provenance record per Entity.

**Changes made:** identity explicitly excludes position; one Representation may
associate with several Concepts; value conditions were separated; assertion-
scoped plural provenance/lifecycle was specified.

**Result:** rows/ranges are qualified locator details, not core fields. Partial
tables and formulas fit without a spreadsheet-specific primitive.

## 3. Technical or legal document

**Counterexamples/problems:** pagination changes across renderings; one passage
can state multiple requirements; interpretations can conflict; an accepted
review is not the same as high statistical confidence; redaction must preserve
the fact of withholding without exposing content.

**Assumptions detected:** page as stable ID, single Concept per passage, a
single winning classification, confidence/review collapse and absence equals
redaction.

**Changes made:** Source-scoped qualified locators, many-to-many association,
coexisting assertions, independent Confidence/Review and explicit redacted
condition.

**Result:** document structure is expressible without mandatory page, paragraph,
party or legal-status fields. Review authority remains profile/governance work.

## 4. Software repository / source-code structure

**Counterexamples/problems:** paths and symbol names change; generated code has
several provenance stages; one source symbol can implement several API
Concepts; branching revisions are not a single integer sequence.

**Assumptions detected:** path/native symbol as semantic identity, single-step
provenance, one Concept per Representation and linear lifecycle.

**Changes made:** locators cannot confer identity; provenance chains/plural
records are allowed; association is `0..*`; lifecycle ADR now flags branch,
merge and causality as blockers.

**Result:** source paths/symbols/commits remain locator or lifecycle vocabulary
details. The accepted state-first hybrid adds no Git, branch or merge behavior.

## 5. Scientific dataset

**Counterexamples/problems:** measured values without units are ambiguous;
uncertainty and calibration vary by discipline; a time-series segment may
support several observations; the same sample has records from multiple
instruments; source data can be incomplete.

**Assumptions detected:** global/default units without a declared profile,
sensor/time fields in core, one confidence score as uncertainty and complete
Bindings.

**Changes made:** measured magnitude requires explicit unit semantics or an
applicable profile default; Confidence is not measurement uncertainty;
temporal/instrument details stay in qualified Bindings/vocabularies; partial
sources/Bindings remain valid.

**Result:** universal values and provenance suffice. Uncertainty/tolerance is an
open value/profile concern, not a mandatory primitive.

## 6. Generic product / asset dataset

**Counterexamples/problems:** SKU differs by market/source and can be reassigned;
one catalog record can describe a family plus variants; sensitive commercial
properties may be redacted; the logical product survives listing changes.

**Assumptions detected:** SKU as semantic ID, product-specific core fields, one
record → one Concept and missing value equals unknown.

**Changes made:** SKU-like identifiers are qualified properties or Bindings;
many-to-many association remains available; redacted/unknown/absent/N/A are
distinct; listing lifecycle does not replace Concept identity.

**Result:** no mandatory SKU, customer, price, asset class or catalog field was
added. Product vocabularies/profiles carry those meanings.

## Lifecycle stress tests

### Engineering-like model lifecycle

**Case:** Representation `R-A` disappears from Source `S-A`, while Concept `C`
remains represented by `R-B` in Source `S-B`.

**Failure exposed:** treating a missing source object as Concept deletion or
coupling Binding lifecycle to Entity identity.

**State-first result:** a current snapshot can tombstone/remove `R-A` or mark
its Binding stale while retaining `C`, `R-B` and their association. Mere absence
from a partial export is not enough. Source and semantic Revision can advance
independently.

**Residual open point:** exact tombstone and stale-Binding encoding.

### Spreadsheet/table lifecycle

**Case:** a row moves after sorting, its locator is corrected, and the semantic
record is later deleted from a declared complete dataset.

**Failure exposed:** row index as identity and absence-as-deletion in filtered
views.

**State-first result:** the Entity ID survives locator correction; Binding
history can supersede the old range. Later deletion needs an explicit tombstone
or profile completeness semantics. No event replay is needed to read the final
state.

**Residual open point:** completeness declarations and Binding addressability.

### Technical/legal document lifecycle

**Case:** clause `C1` is replaced by `C2`; the prior Representation remains
historically citable, and an interpretation assertion is later rejected while
another is accepted.

**Failure exposed:** latest revision as truth, correction as destructive update,
and Review conflated with validity.

**State-first result:** the current snapshot exposes current clause semantics;
directed supersession retains `C1`/its Representation when history is present.
Interpretation assertions require addressability for rejection/correction.
Validity, Review and Revision membership remain distinct.

**Residual open point:** whether supersession is lifecycle metadata, Relation or
canonical specialized form.

### Software repository lifecycle

**Case:** two branches derive semantic revisions `R-left` and `R-right`; a later
revision `R-combined` references both without claiming an automatic merge.

**Failure exposed:** a single revision counter/parent, total ordering and
implicit conflict resolution.

**State-first result:** parent cardinality `0..*` expresses non-linear lineage.
Each state is independently consumable; no branch names, merge algorithm,
working tree or replay semantics enter the core.

**Residual open point:** external parents, partial lineage graphs and cycle
validation.

### Scientific dataset lifecycle

**Case:** an original measurement remains historically valid as observed, but a
derived property is corrected after recalibration and has a different valid-time
interval.

**Failure exposed:** revision order equated with scientific validity and one
lifecycle for Entity plus every assertion.

**State-first result:** measurement and corrected derived assertion coexist;
assertion supersession/validity changes independently. Provenance explains
recalibration and is not itself a Revision. Latest does not mean truest.

**Residual open point:** validity encoding, uncertainty and recorded/observed
timestamp vocabularies.

### Product/asset lifecycle

**Case:** a market SKU changes and two catalog records are federated while the
same commercial Concept remains.

**Failure exposed:** SKU/Source revision as semantic identity and multiple
parents interpreted as a merge procedure.

**State-first result:** old Binding is superseded, Concept identity remains and
the federated Revision may cite multiple parents as lineage only. Conflicting
catalog assertions may remain syntactically valid with separate trust metadata.

**Residual open point:** Binding supersession identity and cross-document
lineage references.

## Lifecycle stress conclusion

Snapshot-only loses portable fine-grained correction/audit. Event-only requires
replay and violates standalone interchange. A state-first hybrid survives all
six cases if history is optional, Changes cannot override state, absence is not
deletion, and multiple parents express lineage without merge behavior. Those
constraints are the basis of accepted ADR-0007; exact encoding remains open.

## Findings across domains

1. No new universal primitive was necessary.
2. Source/Binding is universally necessary as a mechanism but never mandatory
   on every Entity.
3. Assertion metadata needs the accepted common abstract contract; its exact
   storage architecture remains open.
4. Concept–Representation must not be universally one-to-one.
5. Absence and explicit value conditions must remain distinct.
6. Binary Relation mechanics are sufficient for S1, but n-ary patterns require
   later adversarial testing.
7. The accepted lifecycle is state-first and history-optional; authority is
   limited to the document's declared scope and Revision, and replay is never
   required.
8. Every domain-specific locator/type/property/predicate found can move to a
   vocabulary, profile or Extension.

The six domains remain coherent under accepted ADRs 0005–0008. This closes the
S1 abstract model but does not freeze a schema or choose concrete lifecycle
representation.
