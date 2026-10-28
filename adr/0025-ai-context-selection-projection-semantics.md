# ADR-0025: AI Context selection and projection semantics

- **Status:** Accepted
- **Accepted by:** Explicit human architecture decision on 2026-09-19
- **Date:** 2026-09-18
- **Decision order:** Second S4 architecture decision after ADR-0024 acceptance

## Context

ADR-0024 accepts the Profile identity, exact edition and conformance boundary for
S4. The AI Context Profile family identity is
`https://geesno.com/profile/ai-context`, the initial Profile version is
`0.1.0`, and the exact Profile edition pair is the normative requirement-set
identity. ADR-0024 also keeps Profile conformance separate from bare-core/S2
conformance and excludes prompts, models, agents, runtimes, tools and execution.

D2 asks what it means to select and project content from a SemanticDocument for
AI Context Profile use without mutating the source, inventing semantic truth,
collapsing omission into deletion, re-identifying existing objects, or making AI
heuristics normative.

This ADR accepts only abstract selection and projection semantics. It does not
create a new JSON member, AI Context schema, Profile artifact, conformance
fixture, SDK API, query language, retrieval algorithm, continuation syntax,
omission representation or runtime behavior.

## Prerequisite review

No unresolved prerequisite blocks D2 acceptance:

1. The Foundation defines AI Context as compact descriptive context, not model
   routing, RAG, prompting, tool calling, agents or execution.
2. ADR-0009 gives stable exact semantic identity and separates identifier,
   reference and locator semantics.
3. ADR-0011 makes Assertion identity distinct from Entity identity and gives
   assertions one canonical top-level representation in S2.
4. ADR-0013 separates Source from Binding and keeps locators source-relative.
5. ADR-0014 establishes state-first lifecycle, scoped completeness, Revision,
   Tombstone and omission/deletion distinctions.
6. ADR-0015 keeps Extensions inert and separates lossless preservation from
   lossy projection.
7. ADR-0016 freezes S2 Layers 0-3 and leaves Profile validation as a later
   layer.
8. ADR-0023 defines compatibility claims but does not make compatibility,
   equivalence or profile-acceptability into inclusion, relevance or priority.
9. ADR-0024 accepts exact Profile edition identity and the bare-core/Profile
   conformance boundary.

## Controlling distinctions

```text
Projection
!= source SemanticDocument mutation
!= new semantic truth
!= Core primitive
!= Vocabulary
!= Profile
!= execution result
!= prompt
!= AI inference
!= generated LLM summary
!= runtime cache
!= model context window

projection identity
!= projected semantic object identity

selected
!= true

unselected
!= false
!= deleted
!= invalid
!= Tombstone

source completeness
!= projection completeness

serialization order
!= semantic importance

selection order
!= semantic priority

selected original semantic content
!= generated summary
```

## Alternatives

### Alternative A - Profile edition uniquely determines one projection

A Profile edition could define one canonical projection for each source. This is
rejected for D2. A Profile edition defines requirements and permitted
projection behavior. Different explicit selections, purposes or scopes may
produce different valid Projections from the same source under the same exact
Profile edition.

### Alternative B - Projection as model/runtime retrieval output

Projection could be the output of an embedding search, LLM relevance ranking,
RAG pipeline, prompt assembly process or model context-window packing step. This
is rejected. External implementations may use those mechanisms to help choose
content, but the normative Projection is the explicit semantic selection/view
that results, not the algorithm that suggested it.

### Alternative C - Projection as a new AIContextDocument core primitive

A new core document kind could be introduced for AI Context. This is rejected
for D2. The accepted Semantic model is sufficient for the abstract decision.
If a future serialized projection artifact needs its own envelope or artifact
identity, that belongs to a later binding decision and does not create a new
Core primitive here.

### Alternative D - Projection as a finite derived semantic view

A Projection is a finite derived semantic view of an identified source
SemanticDocument state under an exact Profile edition and explicit selection
context. It transports selected semantic content while preserving identity and
meaning. This is accepted.

## Accepted decision

### Projection definition

A **Projection** is:

```text
finite derived semantic view
of an identified source SemanticDocument state
under an exact Profile edition
and an explicit selection context
```

A Projection is derived from accepted Semantic model content. It is not a source
mutation, new semantic truth, Core primitive, Vocabulary, Profile, execution
result, prompt, AI inference or generated summary. It does not create an
`AIContextDocument` primitive.

A Projection may be assessed against the exact AI Context Profile edition only
when a future binding defines the concrete target and assessment process. D2
sets the abstract invariants that such a binding must preserve.

### Source-state traceability

A Projection must be traceable to the source state it was derived from. The
minimum abstract source-state context is:

```text
SemanticDocument identity
+ declared scope
+ current semantic Revision when available
+ other accepted provenance/state context when necessary
```

A SemanticDocument ID by itself does not identify every historical state of that
document. If the source state carries an identified current Revision, the
Projection may claim traceability to that declared Revision and scope. If no
Revision is identified, the Projection may claim traceability to the supplied or
observed source instance and its available provenance/scope context, but it
must not claim exact historical reproducibility of a revisioned state.

Traceability is the ability to relate the Projection to the source state and
selection context. Exact historical reproducibility additionally requires enough
accepted state identity, such as a Revision, and may later require integrity
evidence. D2 does not introduce hashing, canonical-byte identity or signatures.

### Identity preservation

When a Projection carries the same semantic object or claim from the source, the
source identity is preserved:

```text
Entity ID remains Entity ID
Assertion ID remains Assertion ID
Source ID remains Source ID
Binding ID remains Binding ID
Revision/reference identities remain exact when carried
term IRIs remain unchanged
```

Projection MUST NOT re-identify content merely because it appears in a reduced
context. It MUST NOT rewrite semantic IDs to make a subset locally convenient.

```text
projection identity
!= projected semantic object identity
```

If a future serialized projection artifact needs its own identity as an
artifact or view, that identity belongs to the future binding and does not
replace carried semantic IDs.

### Selection semantics

Selection is the explicit decision/context that determines which source content
is included in a Projection. D2 does not define a concrete query language,
selector syntax, ranking model or selection serialization.

A selection may be authored by a user, deterministic local rule, application,
service, AI system or another external process. Regardless of how it is
produced, normative semantics attach to the explicit selection result and its
traceability, not to the algorithm that proposed it.

Generic Projection semantics MUST NOT treat any of the following as normative
selection meaning:

```text
embedding similarity
LLM relevance
vector score
model ranking
automatic semantic importance
```

Selection has only inclusion/context meaning:

```text
selected != true
unselected != false
unselected != deleted
unselected != invalid
unselected != Tombstone
```

### Profile versus selection

A Profile edition defines requirements and permitted projection obligations. A
selection decides which content is included for one projected view.

```text
Profile requirements
!= selection decision/context
```

The same source SemanticDocument under the same exact Profile edition may yield
multiple valid Projections when different explicit selections are allowed by the
Profile. Generic processing MUST NOT infer:

```text
one Profile edition => one unique projection
```

### Projection must not change meaning

Transporting source content into a Projection cannot change its meaning. A
Projection MUST NOT:

- change semantic identity;
- change a term IRI;
- change Assertion meaning;
- convert Confidence into truth;
- convert Review into universal approval;
- alter Source or Binding semantics;
- reinterpret lifecycle state;
- change Concept-Representation association semantics.

If a transformation changes meaning, it is not a transparent Projection of the
same content. It may be future derived content with its own identity,
provenance and confidence, but D2 does not define that derived-content model.

### Reference boundary

Selected content may reference content that is not selected. D2 does not define
the concrete representation for omitted dependency, continuation, external
continuation or partial context mechanics; that belongs primarily to D3.

D2 establishes these invariants:

```text
Projection MUST NOT silently retarget references
Projection MUST NOT fabricate local targets
Projection MUST NOT rewrite semantic IDs merely to make the subset self-contained
```

Consumers must not assume every reference target is present merely because a
Projection is syntactically valid. Future D3 work must define how necessary but
not included content is represented explicitly.

### Scope and completeness boundary

A Projection cannot copy a source completeness claim in a way that becomes false
for the projected view.

```text
source completeness != projection completeness
complete in source scope != complete in projected scope automatically
```

If the source declares complete scope and the Projection is a subset, the
Projection must not imply that the subset is complete for the source scope or
for any broader projected scope unless a future accepted Profile rule explicitly
supports that claim.

Projection omission is not deletion and is never a Tombstone:

```text
omission != deletion
omitted != Tombstone
```

The concrete representation of omission, partiality, boundedness and
continuation remains D3.

### Ordering boundary

D2 does not define semantic priority. Generic processing MUST preserve:

```text
serialization order != semantic importance
selection order != semantic priority
```

A future binding may define a reproducible structural order for deterministic
serialization or diagnostics, but that order is not relevance, priority,
importance or truth unless a later accepted ADR explicitly defines such
semantics.

### Selection purpose

A selection may declare a purpose or external context when a future binding
needs that traceability. Such a purpose is descriptive context only:

```text
declared selection purpose
!= prompt
!= instruction
!= permission
!= execution intent
!= truth
```

D2 does not introduce a universal task taxonomy.

### No summarization substitution

D2 is selection/projection, not summarization. A Projection MUST NOT replace
selected original semantic content with a paraphrase or generated summary while
retaining the original Entity ID, Assertion ID or claim identity.

```text
selected original semantic content != generated summary
```

A summary could be represented in future work as new derived semantic content
with appropriate identity, provenance, confidence and review, but it is not a
transparent copy of the original selected content.

### AI/runtime/execution boundary

Projection semantics must work without AI and MUST NOT depend on:

```text
tokenizers
token counts
context-window size
model relevance
attention
temperature
embeddings
RAG retrieval
LLM summarization
prompt roles
system/user/developer messages
agent planning
tool calling
```

External implementations may use AI systems to suggest selections or generate
separate derived content, but those implementation choices do not become
normative Projection semantics.

### Offline behavior

Projection semantics can operate entirely from locally supplied source data,
Profile rules and selection context. Generic Projection semantics do not require:

```text
network
registry
resolver
geesno.com
model API
LLM
vector store
```

If a Profile IRI returns 404 or a network is unavailable, that does not
invalidate the Profile identity, source semantic IDs or Projection semantics.

### Relationship to ADR-0024

ADR-0024 remains controlling for Profile identity/version, requirement-set
identity and Profile conformance boundary. Projection evaluated as an AI Context
Profile projection must refer to an exact Profile edition:

```text
https://geesno.com/profile/ai-context + 0.1.0
```

No `latest`, moving alias, range or inferred upgrade is allowed by D2.

### Relationship to S2

D2 does not modify:

```text
schema/v0.1/geesno-semantic.schema.json
spec_version 0.1.0
Layers 0-3
```

It adds no JSON members and creates no S4 normative fixtures.

### Relationship to S3 / D7

D7 compatibility claims do not infer Projection inclusion, relevance or
priority.

```text
Compatibility != inclusion
Compatibility != relevance
Compatibility != priority
```

Equivalent or mapped terms may coexist with a Projection, but a Projection MUST
NOT substitute terms automatically because a D7 claim exists unless a future
exact Profile edition explicitly permits such behavior.

### D3 boundary

D3 remains responsible for concrete omission, boundedness and continuation
semantics, including:

```text
omission representation
boundedness
continuation
truncation
partial context mechanics
dependency continuation
size limits
```

D2 only fixes the invariants that omission is not deletion, omitted content is
not Tombstone, and partial Projection is not source mutation.

### D4 boundary

D4 remains responsible for detailed preservation requirements for:

```text
Provenance
Confidence
Review
Validity
Source
Binding
```

D2 requires that Projection not change their meaning or silently drop material
context needed to interpret selected claims, but it does not close every
materiality, preservation or diagnostic rule.

## Cross-domain validation

| Domain | Projection stress case | Result under the accepted decision |
| --- | --- | --- |
| Engineering-like objects | Select one component and its selected relations from a larger object graph. | IDs and term IRIs remain stable; omitted supports are not deleted or retargeted. |
| Spreadsheet/table data | Select a subset of columns, rows and computed-value assertions. | The view can be finite and traceable without treating unselected cells as false or invalid. |
| Technical/legal documents | Select clauses and cited source regions for review. | Clause identity, Source and Review meaning are preserved; no legal truth is inferred. |
| Software/source repositories | Select symbols and module relations for one analysis context. | Projection can reference a Revision when available without making Git a universal lifecycle model. |
| Scientific datasets | Select observations and measured quantities relevant to one question. | Units, uncertainty/provenance and assertion identity are preserved; omitted observations are not negative results. |
| Generic product/asset data | Select product attributes and source bindings for a compact context. | Base and third-party terms can be carried unchanged without automatic compatibility substitution. |

The same Projection semantics work across all six domains without adapters,
execution behavior, domain-specific core fields, provider-specific AI concepts,
network access or a new document primitive.

## Adversarial cases

| # | Case | Generic processing may infer | Generic processing MUST NOT infer |
| --- | --- | --- | --- |
| 1 | Projection selects one Entity and omits another. | One Entity is included in the view. | Omitted Entity is false, deleted, invalid or Tombstoned. |
| 2 | Selected Assertion references an omitted Entity. | A carried reference target may be outside the view. | Local fabricated target or retargeted reference. |
| 3 | Same Entity appears in source and Projection. | It is the same semantic Entity ID. | New identity because context is smaller. |
| 4 | Projection reassigns Entity ID. | It is not transparent carriage of the same Entity. | Valid identity preservation. |
| 5 | Projection changes a term IRI. | Meaning may have changed. | Same Vocabulary term. |
| 6 | Source document changes after Projection creation. | Projection traces to its derivation context. | It automatically tracks later source state. |
| 7 | Source has identified current Revision. | Projection can trace to that declared Revision. | Replay or full history availability. |
| 8 | Source has no identified Revision. | Projection can trace to supplied/observed source context. | Exact historical reproducibility. |
| 9 | Source declares complete scope but Projection is a subset. | Projection is partial unless separately declared otherwise. | Source completeness transfers automatically. |
| 10 | Projection omission treated as deletion. | This is a semantic error. | Deletion from omission. |
| 11 | Projection omission treated as Tombstone. | This is a semantic error. | Tombstone from omission. |
| 12 | Selection produced by an LLM. | An external process suggested selection. | LLM relevance is normative truth. |
| 13 | Selection produced by deterministic local rules. | Selection can be reproducible if rules/context are supplied. | Selected content is more true. |
| 14 | Two different selections under same Profile edition. | Both may be valid if the Profile permits them. | Profile edition uniquely determines one view. |
| 15 | Same source/profile produces two different valid Projections. | Selection context differs. | Conflict solely from non-identity. |
| 16 | Projection orders records differently. | Order may be serialization/view order. | Importance, priority or truth. |
| 17 | Consumer treats first record as most important. | That is consumer-specific behavior. | Normative priority. |
| 18 | Projection silently rewrites reference targets. | It violates D2 invariants. | Valid self-containment repair. |
| 19 | Projection copies only a summary but retains original Assertion ID. | It is not transparent Projection. | Same Assertion meaning. |
| 20 | Malicious text is selected. | It remains inert semantic data. | Prompt instruction or execution permission. |
| 21 | Network unavailable. | Local projection can still be meaningful. | Network requirement. |
| 22 | Profile IRI returns 404. | Retrieval failed or no artifact is available there. | Invalid Profile identity. |
| 23 | Third-party Vocabulary terms are selected. | Their exact term IRIs are carried. | Automatic Profile acceptance. |
| 24 | D7 equivalent term exists but Projection substitutes it automatically. | Substitution needs explicit future Profile policy. | Automatic replacement from compatibility. |
| 25 | Projection drops Provenance necessary to interpret a selected claim. | D4 must define preservation/diagnostic consequences. | Meaning remains fully preserved by default. |
| 26 | Projection includes Source/Binding references without referenced records. | References may point outside the view. | Fabricated local Source or Binding records. |
| 27 | Source revision changes while semantic IDs persist. | Identity can persist across revisions. | Projection identifies the newer revision. |
| 28 | Selected content is copied byte-differently but semantically unchanged. | D2 cares about semantic identity/meaning, not byte identity. | Byte canonicality or signature validity. |
| 29 | Selection purpose is present. | Purpose is descriptive context. | Prompt, task command or permission. |
| 30 | Selection purpose is interpreted as execution instruction. | That interpretation is outside GeesNO.Semantic. | Execution authority. |

## Consequences

- S4 D2 has an accepted abstract Projection model without creating a serialized
  AI Context artifact.
- Projection is a finite derived semantic view of an identified source state
  under an exact Profile edition and explicit selection context.
- Projection preserves semantic IDs, Assertion IDs, Source IDs, Binding IDs,
  Revision/reference identities when carried, and term IRIs.
- Selection is explicit and traceable, but selection algorithms are not
  normative.
- Profile requirements remain separate from selection decisions.
- Omission, boundedness, continuation and detailed preservation rules remain
  downstream work.
- No schema, fixture, SDK, runtime, AI integration, registry, resolver, query
  language or profile artifact follows from this Accepted ADR.

## Remains open

- D3 omission representation, boundedness, continuation and truncation rules;
- D4 detailed preservation requirements for Provenance, Confidence, Review,
  Validity, Source and Binding;
- ordering/priority policy beyond the D2 non-priority boundary, if needed;
- selection-context serialization and concrete selector syntax, if any;
- concrete AI Context/Profile serialization binding;
- Profile conformance result and diagnostics;
- Profile requirement expression and Vocabulary/Profile policy;
- Profile composition and conflict handling;
- S4 examples after the required abstract decisions are accepted;
- S5 fixtures and mature diagnostic governance; and
- SDK/tooling behavior.

## Acceptance record

**Decision status: Accepted**

Accepted by explicit human architecture decision on 2026-09-19. Acceptance closes
S4 D2 only. It does not implement Projection serialization, publish a Profile
artifact or schema, create omission/continuation mechanics, modify S2, accept D3,
open S5, implement an SDK or add execution behavior.
