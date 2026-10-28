# ADR-0026: Projection omission, boundedness and continuation semantics

- **Status:** Accepted
- **Accepted by:** Explicit human architecture decision on 2026-09-20
- **Date:** 2026-09-20
- **Decision order:** Third S4 architecture decision after ADR-0024 and ADR-0025 acceptance

## Context

ADR-0024 accepts exact AI Context Profile identity and the bare-core/Profile
conformance boundary. ADR-0025 accepts Projection as a finite derived semantic
view of an identified source SemanticDocument state under an exact Profile
edition and explicit selection context. ADR-0025 also establishes that
Projection is descriptive, identity-preserving, non-executable and separate
from AI/runtime/retrieval behavior.

D3 asks how a Projection can be explicitly finite, partial or bounded without
collapsing omission into deletion, without inventing source state, without
requiring AI-model limits, and without defining retrieval, APIs, cursors or
execution behavior.

This ADR proposes abstract omission, boundedness and continuation semantics
only. It does not define concrete JSON members, profile artifacts, schemas,
fixtures, SDK APIs, diagnostics, query languages, retrieval protocols, cursor
formats, artifact packaging, network behavior or executable continuation.

## Prerequisite review

No unresolved prerequisite blocks D3 readiness:

1. The Foundation defines AI Context as compact descriptive context with
   explicit partial/omitted/continuation metadata, not prompting, model routing,
   RAG, tools, agents or execution.
2. ADR-0009 separates semantic identifiers from references and locators and
   rejects automatic dereference.
3. ADR-0011 keeps Assertion identity distinct from Entity identity.
4. ADR-0013 separates Source, Binding and source-relative Locator semantics.
5. ADR-0014 establishes state-first lifecycle, scoped completeness and the
   distinction between omission, deletion and Tombstone.
6. ADR-0015 separates lossless preservation from lossy projection and keeps
   unknown Extensions inert.
7. ADR-0016 freezes S2 Layers 0-3 and leaves Profile validation to later
   layers.
8. ADR-0024 accepts exact Profile edition identity and the Profile conformance
   boundary.
9. ADR-0025 accepts Projection, selection semantics, source-state traceability,
   identity preservation and the D3/D4 boundary.

## Controlling distinctions

```text
source content
!= selection scope
!= projection scope
!= included content
!= unselected content
!= omitted content
!= continuation

source scope
!= selection scope
!= Projection scope

outside selection scope
!= omitted inside Projection scope

subset of source
!= automatically partial relative to Projection scope

unselected
!= omitted

omitted
!= deleted
!= false
!= invalid
!= Tombstone

bounded
!= semantically important
!= true
!= priority
!= model context window

bound reached / bounded
!= truncation established

truncated
=> known incomplete relative to declared Projection scope
=> partial

truncated
!= unknown completeness

continuation
!= retrieval instruction
!= URL fetch
!= API call
!= tool call
!= resolver requirement
!= prompt instruction
```

## Definitions

**Source content** is the semantic content available in the identified source
SemanticDocument state. Its meaning and lifecycle remain governed by the source
SemanticDocument's declared scope, Revision and accepted core rules.

**Selection scope** is the explicit boundary of source content considered for a
particular Projection decision. Content outside the selection scope is
unselected. It is not omitted merely because it exists in the source.

**Projection scope** is the explicit abstract scope for what the Projection
claims to cover for this projected view under the exact Profile edition and
selection context. Projection scope is separate from source scope and selection
scope. Completeness is assessed only relative to this declared Projection scope,
not relative to the entire source unless the Projection scope explicitly says
so.

**Included content** is source semantic content actually carried in the
Projection while preserving identity and meaning under ADR-0025.

**Unselected content** is source content outside the explicit selection scope.
Generic processing MUST NOT treat unselected content as omitted, false, deleted,
invalid, Tombstoned or less true.

**Omitted content** is content that belongs to, or is material to satisfying,
the declared Projection scope but is not included in the Projection. Omission is
descriptive only. It does not alter source state or carried semantic identity.

**Continuation** is a descriptive claim that additional content related to the
same projected context exists or may exist outside the current Projection
segment. Continuation is inert semantic metadata, not an executable retrieval
mechanism.

## Alternatives

### Alternative A - Treat every source subset as partial

Every Projection smaller than its source could be considered partial. This is
rejected. A source with 100 Entities may yield a Projection whose explicit
selection and Projection scope are only Entity A. If Entity A and the required
scope around Entity A are fully included, the Projection can be complete
relative to that declared selection/projection scope even though it is a tiny
subset of the source.

### Alternative B - Treat absence of omission metadata as completeness

A consumer could infer that no omission record means the Projection is complete.
This is rejected. Absence of omission information does not establish
completeness. Completeness must be explicit or otherwise established by an
accepted Profile rule.

### Alternative C - Model boundedness with AI token budgets

AI Context could define universal token, tokenizer, model window or prompt-size
limits. This is rejected. Implementations may use those limits internally, but
universal GeesNO.Semantic semantics must remain AI-provider-neutral and usable
without an LLM.

### Alternative D - Treat continuation as executable pagination

Continuation could be a URL, API cursor, resolver command or tool-call
instruction. This is rejected. Future bindings may carry inert descriptors such
as references, tokens, handles or locators, but such representation is not
semantic authority; generic semantics do not fetch, execute, resolve or trust
them automatically.

### Alternative E - Explicit scope-relative omission, boundedness and inert continuation

Projection completeness is evaluated only relative to declared Projection scope.
Unselected content is separate from omitted content. Boundedness is an explicit
finite limiting policy. Continuation is inert descriptive metadata preserving
source-state and Profile-edition traceability. This is proposed.

## Proposed decision

### Projection scope and completeness

Projection completeness is always relative to an explicit declared Projection
scope. There is no universal completeness claim for a Projection unless a future
accepted Profile rule defines one for an exact scope.

The accepted ADR-0014 tri-state completeness concepts are reused at the
Projection level:

```text
complete = complete only relative to declared Projection scope
partial = known incomplete relative to declared Projection scope
unknown = completeness relative to declared Projection scope is not established
```

A Projection MUST NOT copy source completeness into a broader or different
Projection scope. A Projection that is complete for a narrow scope does not
claim source-wide completeness.

A subset of source content is not automatically partial. If the source contains
100 Entities, the selection scope is only Entity A, the declared Projection
scope is Entity A and all content required by that scope is included, then the
Projection may be complete relative to that scope. Conversely, if the Projection
scope asks for 20 relevant Entities and only 10 are included, completeness is
partial when the incompleteness is known, or unknown when it is not established.

```text
subset of source != automatically partial relative to Projection scope
complete relative to narrow Projection scope != complete for source scope
```

### Selection scope versus Projection scope

Selection scope identifies which source content is considered for this projected
view. Projection scope identifies what the Projection claims to cover and what
completeness is assessed against. They may align, but generic processing MUST
keep them conceptually separate.

Content outside selection scope is unselected. It is not omitted inside the
Projection scope unless the Projection scope also declares that content as
material to the projected view.

```text
outside selection scope != omitted inside Projection scope
```

A future binding may represent selection and Projection scope together or
separately, but representation must preserve the distinction and does not
collapse it.

### Unselected content and omitted content

Unselected content is outside the explicit selection scope. Omitted content is
inside, or material to, the declared Projection scope but not included.

Generic consumers MUST NOT infer:

```text
unselected = omitted
omitted = deleted
omitted = false
omitted = invalid
omitted = Tombstone
omission = lifecycle transition
omission = Source mutation
```

A Projection does not need to enumerate all unselected source content. In large
sources, such enumeration would defeat the purpose of projection.

### Omission declarations

Omission declarations are descriptive metadata about the projected view. They
MUST NOT:

- delete source content;
- create Tombstones;
- alter semantic identity;
- invalidate omitted assertions;
- make omitted assertions false;
- invent replacement state;
- authorize retrieval;
- imply network availability;
- execute continuation;
- retarget references.

Omitted content remains separate from deletion and from lifecycle Tombstones.
Deletion or retirement requires the accepted lifecycle mechanism.

### Known and unknown omission

A Projection may distinguish known omitted content from unknown or unassessed
additional content.

Known omitted content is content whose omission is known at the level defined
by a future accepted semantic rule or exact Profile requirement and represented
by a future binding: for example, a known Entity ID, known Assertion ID, known
category of dependency, known count or known scope area. D3 does not define the
normative granularity or concrete expression of those details.

Unknown omission means additional material content may exist, but its identity,
count, category or relevance is not established by the Projection.

Generic processing MUST NOT infer:

```text
not listed = known omitted
no omission record = complete
absence of omission information = no omission
unknown omitted content = deleted content
```

Completeness must be explicitly declared or established by a future accepted
Profile rule. Absence of omission metadata does not establish completeness.

### Boundedness

A bounded Projection is intentionally limited by an explicit finite bound
policy. A future exact Profile edition or accepted semantic rule may define the
normative meaning of such a policy. A future serialization binding may
represent, encode or transport that policy, but the binding is not independent
semantic authority. D3 does not define the concrete syntax.

Boundedness is provider-neutral and model-neutral. Generic semantics MUST NOT
use any of the following as universal bound semantics:

```text
token budget
tokenizer
model context window
prompt packing limit
embedding store page size
retrieval batch size
```

A quantitative bound needs an explicit dimension, unit and rule before it has
portable meaning. A future exact Profile edition or accepted semantic rule may
define byte count, item count, assertion count, source-range span or other
bounded dimensions. A future binding may represent those requirements, but does
not originate them. No universal metric is created here.

```text
bound != semantic importance
bound != truth
bound != priority
bound != relevance
bound != completeness
```

A bounded Projection can be complete when the declared Projection scope fits
within the bound. A bounded Projection can be partial when the bound prevents
including all content required by the declared Projection scope and that
incompleteness is known. A bounded Projection can also have unknown
completeness when a bound exists but completeness relative to the declared
Projection scope is not established; bounded + unknown does not mean truncation
is known.

### Truncation

Truncation is the established condition where Projection generation stopped
before including all content required by the declared Projection scope because
a bound or other finite stopping rule prevented further inclusion. Because
truncation establishes that required in-scope content is not included,
truncation implies known incompleteness relative to the declared Projection
scope and therefore `partial` completeness.

Truncation is a cause or explanation for omission/partiality; it is not a
lifecycle event, deletion, Tombstone, invalidity, source mutation or semantic
priority claim. Bound reached or boundedness alone is not truncation unless the
Projection also establishes that required in-scope content was left out.

```text
bounded + complete is possible when the scope fits
bounded + partial is possible when the bound prevents full inclusion and this is known
bounded + unknown is possible when completeness is not established
bounded + unknown does not mean truncation is known
bound reached / bounded != truncation established
truncated => known incomplete relative to declared Projection scope
truncated => partial
truncated != unknown completeness
truncated != deleted
truncated != lower priority
```

A future exact Profile edition or accepted semantic rule may define when
truncation must be declared, how omitted content must be summarized and whether
continuation descriptors are required. A future binding may encode those
requirements. D3 only fixes the abstract relationship.

### Continuation

Continuation means additional content related to the same projected context
exists or may exist outside the current Projection segment. Continuation can be
used for more of the same declared Projection scope, later segments or related
projected content, subject to future exact Profile requirements or accepted
semantic rules that a future binding may represent.

A continuation declaration MUST NOT be interpreted as:

```text
URL fetch instruction
API call
cursor execution
resolver requirement
tool invocation
network availability
trust claim
prompt text
priority order
```

Future bindings may represent continuation using an inert descriptor, handle,
reference, token or locator. Such descriptors are data. They do not originate
semantic requirements, execute anything or authorize execution.

A continuation descriptor may be unavailable, stale, unreachable, unresolved,
untrusted, maliciously worded or not supplied. The Projection remains a
descriptive artifact; consumers decide separately whether and how to use any
implementation-specific retrieval system outside GeesNO.Semantic.

### Continuation traceability

Continuation must preserve enough context to prevent silent drift across source
states or Profile editions. At the abstract level, continuation traceability
requires preserving:

- source SemanticDocument identity;
- source state context, including exact Revision when available;
- exact Profile edition;
- selection context;
- declared Projection scope;
- segment or continuation relationship when a future exact Profile requirement
  or accepted semantic rule defines it and a future binding represents it.

If a Projection segment is derived from source state R1, a continuation of that
segment MUST NOT silently resolve against R2 after the source changes. A future
exact Profile requirement or accepted semantic rule may allow a new Projection
or updated derivation to be declared, and a future binding may encode that
declaration, but it must not pretend that R2 is the same continuation context
as R1.

```text
continuation of R1 != silent continuation against R2
```

Continuation declaration does not mean additional content is currently
available, network-reachable, retrievable, trustworthy or still valid.

### Ordering and segment semantics

A continuation segment, next segment or serialized order carries structural
relationship only unless a later accepted ADR explicitly defines additional
semantics.

Generic processing MUST NOT infer:

```text
next segment = more important
next segment = less important
later segment = later truth
first segment = highest priority
last segment = universal source completeness
```

If a future accepted semantic rule defines deterministic structural order for
serialization or diagnostics, a future binding may encode that order; it remains
structural and non-priority by default.

### Projection continuation and dependency continuation

Projection continuation means more content related to the same projected context
may exist outside the current segment.

Dependency continuation means content needed to resolve, interpret or inspect a
carried reference is not included in the current Projection. For example, a
selected Assertion may reference an Entity not included in the current segment.

These are distinct. Generic processing MUST NOT fabricate the dependency,
retarget the reference, fetch it automatically or treat the carried reference as
invalid solely because its target is outside the segment.

```text
projection continuation != dependency continuation
missing referenced target != fabricated local target
```

### Self-containment boundary

A valid Projection need not include every referenced semantic object when
accepted rules, a future exact Profile edition or another accepted semantic rule
allows references outside the current view. D3 makes this explicit through
partiality, omission and continuation semantics, without retargeting references
or requiring universal self-containment.

If a Profile requires a self-contained Projection for a particular use case,
that requirement belongs to a future exact Profile edition or accepted semantic
rule. A future binding may represent the requirement, but representation is not
semantic authority. Self-containment is not a generic D3 rule.

### AI/runtime/security boundary

Omission, boundedness and continuation semantics MUST work without AI. Generic
processing MUST NOT depend on:

```text
LLM
RAG
embeddings
vector database
model ID
tokenizer
token budget
context-window size
prompt packing
agent planning
tool calling
```

External implementations may use AI or local deterministic processes to choose
what to include or omit, but the normative result is the explicit Projection
metadata, not the method that produced it.

Continuation and omission metadata are inert semantic data. Malicious text in a
continuation descriptor is not a prompt instruction, command, permission,
resolver directive or tool-call authorization.

```text
continuation descriptor != prompt
continuation descriptor != command
```

### Offline behavior

A Projection and its omission/continuation metadata can be interpreted from
locally supplied data. Generic semantics do not require a network, registry,
resolver, Profile fetch, geesno.com endpoint, model API, cloud service or
remote continuation service.

Unavailable network resources, failed dereference, 404 responses or absent
continuation services do not by themselves invalidate semantic identity,
Profile identity or the descriptive Projection state.

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

D3 does not decide which trust, validity, source or binding records are material
in every Projection. It only establishes that omission/continuation cannot
change their meaning, silently delete them, fabricate replacements or erase the
need for later preservation rules.

### D5/D6 boundary

D5 remains responsible for Profile requirement expression, Vocabulary/Profile
policy and the normative requirements applicable to an exact Profile edition.
D6 remains responsible for representing, encoding or transporting those
requirements and metadata in a concrete AI Context/Profile serialization
binding.

A serialization binding is not independent semantic authority. It MUST NOT
originate self-containment requirements, bound-policy semantics, required
continuation presence, Projection completeness requirements or other Profile
requirements. Those semantics must come from an exact Profile edition or another
accepted semantic rule before a binding represents them.

D3 does not define:

- JSON field names;
- omission-record syntax;
- bound-policy syntax;
- continuation descriptor syntax;
- artifact identity;
- profile schema;
- conformance fixtures;
- validation diagnostics;
- SDK APIs;
- query languages;
- retrieval protocols.

## Cross-domain validation

| Domain | Stress case | Result under the proposed decision |
| --- | --- | --- |
| Engineering-like objects | Select one component from a larger object graph with omitted connected components. | The Projection can be complete for the selected component scope; omitted supports are not deleted or Tombstoned. |
| Spreadsheet/table data | Select one sheet range or computed column from a workbook with many unselected cells. | Cells outside selection are unselected, not omitted; known omitted formula dependencies can be declared separately. |
| Technical/legal documents | Select clauses relevant to one review while leaving other clauses outside selection. | Narrow-scope completeness is possible; continuation is not a legal retrieval instruction or priority claim. |
| Software/source repositories | Select symbols from one revision while the repository later changes. | Continuation must preserve the source Revision context and cannot silently resolve R1 against R2. |
| Scientific datasets | Select observations under a finite item-count bound. | Bounded and complete is possible if the declared scope fits; bounded + unknown remains possible when completeness is not established, but established truncation means known partiality rather than negative results. |
| Generic product/asset data | Select attributes for one product from a catalog. | Unselected products need not be enumerated; omitted known dependencies remain descriptive only. |

The proposal remains universal, software-neutral, format-neutral,
domain-neutral, AI-provider-neutral, offline-capable and non-executable.

## Adversarial cases

| # | Case | Generic processing may infer | Generic processing MUST NOT infer |
| --- | --- | --- | --- |
| 1 | Source has 100 Entities; selection only Entity A; Entity A's declared Projection scope is fully included. | The Projection may be complete relative to Entity A's declared Projection scope. | Source-wide completeness or partiality solely because 99 Entities are unselected. |
| 2 | Source has 100 Entities; Projection scope asks for 20; only 10 are included. | The Projection is partial when that incompleteness is known. | That omitted 10 are deleted, false, invalid or Tombstoned. |
| 3 | Content is outside selection scope. | It is unselected. | It is omitted inside Projection scope. |
| 4 | Content is inside Projection scope but omitted by a bound. | The Projection is partial when the in-scope omission is known; if truncation is established, it is known partial. | Lifecycle deletion or lower semantic truth. |
| 5 | Omission is interpreted as deletion. | That interpretation is a semantic error. | Deletion from omission. |
| 6 | Omission is interpreted as Tombstone. | That interpretation is a semantic error. | Tombstone from omission. |
| 7 | No omission metadata is present. | Completeness is not established unless separately declared. | Complete by default. |
| 8 | Source completeness is copied onto the Projection. | It applies only if the Projection scope is exactly supported. | Automatic completeness transfer across scopes. |
| 9 | Projection is complete relative to a narrow scope. | It is complete for that declared scope. | Complete for the full source. |
| 10 | Projection is partial relative to a narrow scope. | Known in-scope content is missing. | The source is partial or invalid. |
| 11 | Projection completeness is unknown. | Completeness is not established. | Complete, partial, false or deleted. |
| 12 | A bounded Projection fits completely within its declared scope. | It can be bounded and complete. | Bounds always imply truncation. |
| 13 | A bounded Projection is truncated. | The Projection is known incomplete relative to the declared Projection scope and therefore partial. | Truncated content is less true, deleted or unknown-completeness content. |
| 14 | Token limit is used as a universal bound. | An implementation used an external AI-specific limit. | Portable GeesNO.Semantic boundedness. |
| 15 | Byte limit is explicitly declared by a future accepted policy. | The byte dimension may have portable meaning under that policy. | Any undeclared byte-count semantics in D3. |
| 16 | Item-count limit is explicitly declared by a future accepted policy. | The item dimension may have portable meaning under that policy. | Semantic importance or priority from item order. |
| 17 | A bound is supplied without unit or semantics. | It is not portable as a quantitative bound. | Valid universal limit semantics. |
| 18 | Continuation is present but unavailable. | Additional content exists or may exist, but is not currently available through that descriptor. | Invalid Projection or guaranteed retrievability. |
| 19 | Continuation IRI or locator returns 404. | Dereference failed or no artifact is available there. | Invalid semantic identity or automatic source deletion. |
| 20 | Continuation is treated as auto-fetch. | That is implementation behavior outside generic semantics. | Required GeesNO.Semantic processing. |
| 21 | Continuation is treated as a tool call. | That is outside GeesNO.Semantic. | Execution authority. |
| 22 | Source changes from R1 to R2 after Projection. | The Projection traces to its derivation context. | It automatically tracks R2. |
| 23 | Continuation of R1 silently resolves against R2. | This violates traceability. | Valid continuation of the same context. |
| 24 | Two continuation segments share the same source state. | They may be related segments of one projected context. | Priority, truth ordering or completeness beyond their declared scope. |
| 25 | Segment order is interpreted as importance. | That is consumer-specific behavior. | Normative priority. |
| 26 | Selected Assertion references an Entity not included. | The target may be outside the current Projection segment. | Fabricated local target or invalid carried Assertion solely for that reason. |
| 27 | Dependency continuation is present. | Additional dependency content may be needed to resolve a reference. | More of the same Projection scope or automatic fetch. |
| 28 | Content is omitted but identity is known. | Known omitted content may be identified at that granularity. | Deletion, falsity or invalidity. |
| 29 | Additional content may exist but identities are unknown. | Omission/completeness may remain unknown. | Known omitted IDs or counts. |
| 30 | Third-party Vocabulary content is omitted. | Vocabulary details may be outside the view. | Invalid term identity or automatic vocabulary dereference. |
| 31 | AI decides truncation. | An external process chose where to stop. | AI choice as normative truth or priority. |
| 32 | Local deterministic process decides truncation. | The process may be reproducible if described. | Selected content is more true. |
| 33 | Malicious text appears in continuation metadata. | It is inert data. | Prompt instruction, command or permission. |
| 34 | Continuation descriptor is interpreted as a prompt. | That interpretation is outside GeesNO.Semantic. | Normative prompt semantics. |
| 35 | Consumer assumes final segment means universal source completeness. | It may indicate no further segment for the declared Projection scope only if a future accepted semantic rule says so and a future binding represents that claim. | Universal completeness of the source. |

## Consequences

- Projection completeness becomes explicitly scope-relative.
- Unselected content and omitted content remain separate.
- Known omitted content and unknown/unassessed additional content remain
  separate.
- Omission remains descriptive and cannot cause deletion, Tombstone, invalidity,
  falsity, source mutation or execution.
- Boundedness becomes an explicit finite limiting policy, not AI token budget or
  semantic priority.
- Truncation entails known partiality relative to declared Projection scope
  without implying deletion, unknown completeness or lower truth.
- Continuation is inert descriptive metadata, not retrieval, API, cursor,
  resolver, tool call or prompt.
- Continuation must preserve source-state, exact Profile edition,
  selection-context and Projection-scope traceability.
- Dependency continuation and projection continuation remain distinct.
- D4 preservation requirements remain open; D5 Profile requirement semantics
  and D6 serialization binding remain separate and open.

## Remains open

- D4 detailed preservation requirements for Provenance, Confidence, Review,
  Validity, Source and Binding;
- Profile requirement expression and Vocabulary/Profile policy;
- concrete omission, bound and continuation syntax;
- concrete AI Context/Profile serialization binding;
- Profile artifact identity and packaging;
- validation diagnostics and conformance result;
- S4 examples after the required abstract decisions are accepted;
- S5 fixtures and mature diagnostic governance; and
- SDK/tooling behavior.

## Acceptance record

**Decision status: Accepted**

Accepted by explicit human architecture decision on 2026-09-20. Acceptance
closes S4 D3 only. It does not implement JSON serialization, schema, fixtures,
Profile artifacts, SDK behavior, registry, resolver, network service,
retrieval protocol, AI integration, prompt format, tool call, execution
behavior or any later S4 decision.
