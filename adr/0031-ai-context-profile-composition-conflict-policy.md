# ADR-0031: AI Context Profile composition and conflict policy

- **Status:** Accepted
- **Accepted by:** Explicit human architecture decision on 2026-09-27
- **Date:** 2026-09-27
- **Decision order:** Eighth S4 architecture decision after ADR-0030 acceptance

## Context

ADR-0024 defines a Profile edition as `profile_family + exact profile_version`
and makes that pair the identity of one immutable normative requirement set.
ADR-0025 through ADR-0027 define Projection, omission, boundedness,
continuation, preservation and material-context semantics. ADR-0028 defines
inert Profile requirements, explicit deterministic applicability, exact
Vocabulary dependencies, requirement modes and the boundary for future
composition. ADR-0029 accepts one concrete Profile/Projection binding version.
ADR-0030 accepts a conformance result for exactly one subject against exactly one
exact Profile edition.

Some use cases need policies originating in more than one exact Profile edition.
D8 must decide whether that need creates a normative composition, remains
multiple independent assessments or is coordinated externally. It must not
retroactively reinterpret multiple Profile references as a merged Profile or
change the accepted D7 assessment binding.

D8 is architecture only. It does not create a composition schema, Profile
artifact, fixture suite, composition engine, evaluator, SDK, CLI, runtime,
registry, resolver, package, publication or release artifact.

## Prerequisite review

1. The Foundation keeps GeesNO.Semantic universal, descriptive,
   software-neutral, format-neutral, domain-neutral, AI-provider-neutral and
   independent from GeesNO.Core.
2. The Foundation requires AI Context to remain inert semantic context rather
   than prompting, model arbitration, tools, agents, workflow or execution.
3. ADR-0009 separates identity, reference and locator and rejects automatic
   dereference.
4. ADR-0017 and ADR-0024 require exact edition identity without `latest`,
   version ranges, inferred compatibility or automatic upgrade.
5. ADR-0023 keeps compatibility claims inert and prevents them from becoming
   automatic substitution or conformance.
6. ADR-0028 makes a requirement authoritative only within its exact Profile
   edition, makes requirement order non-semantic and leaves merge, inheritance,
   override, precedence and conflict resolution to D8.
7. ADR-0029 fixes binding grammar ownership and forbids a Profile from inventing
   new normative slots under binding version `0.1.0`.
8. ADR-0030 fixes one D7 assessment as one subject plus one exact Profile
   edition and leaves multi-Profile aggregation and conflict outside D7.

No unresolved prerequisite blocks the D8 decision.

## Controlling distinctions

```text
multiple Profiles referenced
!= merged Profile

multiple assessments
!= composite conformance

Profile composition
!= requirement concatenation

Profile composition
!= array order precedence

Profile A + Profile B
!= automatically a new Profile edition

component Profile edition
!= composite Profile edition

component requirement identity
!= composite requirement identity

same requirement_id spelling
!= same requirement

conflict
!= difference
!= duplicate requirement
!= unsupported
!= unavailable

requirement mode
!= priority

required
!= higher priority

optional
!= weak

prohibited
!= override

composition declaration
!= execution order

composition artifact location
!= composition identity

exact edition reference
!= retrieval instruction

composition validity
!= subject conformance

conformance to a composite Profile edition
!= conformance to every component Profile edition
```

The accepted D7 invariant remains:

```text
one D7 assessment
=
one subject
+ one exact Profile edition
```

## Definitions

**Profile composition** means an explicit normative act that defines one exact
composite Profile edition from identified exact component Profile editions,
while providing a complete reproducible requirement set and traceability from
that set to component requirements.

**Composite Profile edition** means a Profile edition with its own
`profile_family + exact profile_version` identity whose normative definition
includes exact component-edition provenance and a complete resolved requirement
set. It is a normal exact Profile edition for D7 assessment, but its composition
provenance requires additional representation beyond D6 binding version `0.1.0`.

**Component Profile edition** means one exact Profile edition, identified by
`profile_family + exact profile_version`, that a composition declares as a
normative and provenance source. Every requirement occurrence in that edition's
exact requirement set must receive one explicit composition disposition. The
component declaration preserves origin and lineage; it does not establish
inheritance, precedence or conformance to the component and is not an
instruction to fetch, execute or dynamically import requirements.

**Independent assessment** means a D7 assessment of one subject against one exact
Profile edition. Two or more independent assessments do not create a composite
Profile or composite outcome.

**Coordination metadata** means descriptive information that associates multiple
Profile editions or assessment results without merging their requirement sets or
outcomes.

**Requirement origin** means the exact Profile edition and stable requirement
reference, or exact artifact-coupled occurrence reference when no stable
requirement identity exists, from which an adopted or resolved composite
requirement derives.

**Composition conflict** means a deterministic incompatibility among jointly
applicable requirements or composition constraints such that no subject state
can satisfy all of them under the same explicit assessment context and exact
semantics.

## Alternatives

### Candidate A - No normative composition in 0.1

Profiles are assessed independently. A consumer may retain several D7 result
artifacts, but no merged Profile, composite identity or aggregate conformance
result exists.

Advantages:

- preserves D7 without any new Profile representation;
- minimizes architecture and implementation;
- makes requirement ownership and outcome interpretation unambiguous.

Disadvantages:

- cannot express a reusable exact policy that intentionally combines multiple
  Profile editions;
- leaves every multi-policy use case to external coordination;
- cannot provide one reproducible combined requirement set.

Candidate A remains valid behavior when no composite Profile is authored, but it
is insufficient as the only D8 policy.

### Candidate B - Explicit composite Profile edition

Composition creates a new exact Profile edition with its own identity, exact
version, complete resolved requirement set and requirement-origin traceability.
The composite can then be assessed by D7 as one exact Profile edition.

Advantages:

- preserves D7 singular assessment;
- gives the composed policy immutable identity and reproducible semantics;
- permits deterministic conflict resolution at authoring time;
- preserves component and requirement provenance;
- supports offline assessment from finite exact artifacts.

Disadvantages:

- requires explicit publication authority and a new Profile binding version for
  composition metadata;
- requires authors to resolve conflicts and materialize a final requirement set;
- creates a new edition whenever components or resolutions change.

Candidate B is accepted.

### Candidate C - Coordination artifact over independent exact Profiles

A separate artifact may list several exact Profile editions and their independent
D7 assessments without creating a merged Profile.

Advantages:

- preserves component identities and original results;
- supports reporting bundles and external governance;
- avoids inventing a composite requirement set.

Disadvantages:

- does not answer whether one combined policy is conformant;
- cannot resolve requirement conflicts as Profile semantics;
- needs separate coordination semantics if standardized later.

Candidate C remains a possible future reporting mechanism, but it is not
normative Profile composition and is not selected as the D8 composition model.

### Candidate D - Declarative dynamic merge of component Profiles

A composition declaration could import component requirement arrays and apply
union, override, intersection or precedence dynamically during assessment.

This is rejected. It would make assessment depend on graph traversal and
availability, encourage order-based precedence, blur source requirement
authority, complicate offline reproducibility and risk changing results when a
component artifact or resolver changes.

## Comparison

| Criterion | A: independent only | B: explicit composite edition | C: coordination artifact | D: dynamic merge |
| --- | --- | --- | --- | --- |
| Exact identity for combined policy | None | Own exact Profile edition | None | Often derived or unstable |
| D7 binding remains singular | Yes | Yes | Yes for each result | At risk |
| Requirement origin traceability | Per independent Profile | Required per composite requirement | Per independent result | Easy to lose |
| Conflict resolution | External only | Explicit at authoring time | Not composition semantics | Runtime/dynamic |
| Offline reproducibility | Strong | Strong with exact local artifacts | Strong for supplied results | Dependency-sensitive |
| Deterministic assessment | Per Profile | One complete resolved set | Per Profile only | Complex and resolver-prone |
| Implicit precedence risk | None | Prohibited | None | High |
| Selected for D8 | Retained as default non-composition | Accepted | Deferred as coordination only | Rejected |

## Decision

Normative Profile composition is optional. The existence of several Profile
references, several independent assessments or coordination metadata does not
create composition.

When a use case needs one combined normative policy, D8 accepts exactly one
composition model: an explicitly authored composite Profile edition under
Candidate B.

```text
no explicit composite edition
=> no normative composition

explicit composite edition
=> one new exact Profile edition
   + exact component provenance
   + complete resolved requirement set
   + requirement-origin traceability
```

A composite Profile is not synthesized by a consumer, assessor, schema,
registry, resolver, model or array operation. It is authored and versioned under
the same Profile authority and immutability rules as every other exact Profile
edition.

## Composition versus reference and coordination

The following remain separate:

1. an artifact that mentions several Profiles;
2. several independent D7 assessments;
3. an external policy that asks a workflow to inspect several results;
4. one exact composite Profile edition;
5. informative metadata about related Profiles.

Only item 4 is normative Profile composition under this decision.

A document that lists P1 and P2 does not declare P1+P2. Two conformant D7 results
do not create composite conformance. A coordination artifact may preserve result
relationships, but it cannot create a merged Profile or invent an aggregate
outcome without a later accepted decision.

## Composite Profile identity

A composite Profile edition has exactly the identity accepted by ADR-0024:

```text
Profile edition
=
profile_family + exact profile_version
```

The publisher or governance authority defining the composite assigns
`profile_family` and `profile_version` under the ordinary Profile authority
model. D8 requires no central registry and grants no implementation authority to
invent the identity.

A composite may use a new Profile family or an edition under an existing family
only when the authority for that family explicitly authors it. Generic
processing never derives identity from:

- concatenated Profile IRIs;
- sorted component lists;
- array order;
- a content hash;
- a filename;
- a package path;
- an artifact URL;
- a registry key;
- the highest component version.

```text
Profile A + Profile B
!= automatically a new Profile edition
```

Changing any exact component edition, requirement disposition, conflict
resolution or normative resolved requirement requires a new composite Profile
version. Component provenance is part of the immutable composite edition.

## Component references and dependency graph

Every component reference identifies exactly one Profile edition using
`profile_family + exact profile_version`. A component reference must not use
`latest`, version ranges, implicit compatibility, automatic upgrade or registry
resolution.

The component dependency graph must be finite and acyclic. A composite Profile
may name another composite Profile as an exact component only when the resulting
graph remains finite and acyclic.

```text
self dependency
=> invalid composition

direct cycle
=> invalid composition

transitive or nested cycle
=> invalid composition
```

D8 defines no recursive runtime import. The composite edition contains a
complete resolved requirement set, so ordinary subject assessment does not need
to traverse the component graph. Component artifacts are needed to independently
verify composition provenance and conflict resolution, not to execute a dynamic
merge. When an exact component is itself composite, disposition accounting
applies to that component edition's exact resolved requirement set; an assessor
does not recursively import its component graph.

## Requirement ownership and origin

A requirement remains authoritative in the exact Profile edition that defines
it. Composition does not mutate, rename or reinterpret the source requirement.

Each requirement in the composite resolved set must have one of these explicit
origins:

- adopted unchanged from one exact component requirement;
- defined by the composite edition itself;
- defined by the composite as an explicit resolution of identified component
  requirements.

The composition also records exactly one explicit disposition for every
requirement occurrence in the exact requirement set of every exact component
edition. The three dispositions are conceptually equivalent to:

- `adopted_unchanged`;
- `replaced` by a distinct composite requirement;
- `excluded` by the composite rule.

No requirement is implicitly irrelevant, silently dropped, copied without
origin or changed in place. Absence of a disposition is incomplete composition
provenance; omission is not exclusion. An explicit exclusion retains the source
requirement's identity and meaning and does not delete or invalidate it. It only
states that the source requirement is not part of the composite resolved
normative requirement set.

For a component that is itself a composite Profile edition, this exhaustive
rule applies to the requirements in that exact component edition's resolved
requirement set. It does not require recursive runtime import or separate
disposition accounting over transitive source artifacts.

If a resolving requirement changes meaning, it is a new requirement owned by
the composite edition. Its lineage identifies every source requirement it
resolves. The original requirements retain their original meanings and
identities.

```text
source requirement
!= rewritten composite requirement

requirement origin
!= requirement identity

composition lineage
!= precedence

no disposition
!= implicitly irrelevant

omitted requirement
!= excluded requirement
```

## Requirement references and collisions

A stable `requirement_id` remains scoped to its exact Profile edition. Therefore
these are distinct even when the text token is identical:

```text
(P1 exact edition, requirement_id = R)
!=
(P2 exact edition, requirement_id = R)
```

The qualified source requirement reference is the exact source Profile edition
plus its stable requirement identity. If the source requirement has no stable
identity, composition may use an exact artifact-coupled occurrence reference
consistent with ADR-0030; array position, JSON Pointer, file line and display
order remain locators rather than semantic requirement identity.

Composite requirements may have composite-scoped stable requirement identities.
A composite must not collapse source requirements merely because their IDs or
bodies are textually equal. When a composite adopts colliding source IDs, its
own addressable requirement references must remain unambiguous and preserve the
qualified source origins.

Array index is never a collision solution.

## Composition models

### Union

Union means every requirement occurrence from every component's exact
requirement set is adopted unchanged. Each adopted requirement retains its own
applicability descriptor and may or may not apply in a particular subject
assessment. Union is permitted only as an explicit authoring rule and only when
the complete resulting requirement set is conflict-free. Union is never inferred
from a list of component Profiles.

### Override

Implicit override is rejected. No Profile wins because it is first, last,
newer, lexically greater, more specific in name or preferred by an
implementation.

A composite may explicitly replace identified component requirements with a new
composite-owned resolving requirement. That is an authored requirement and
lineage decision, not precedence or mutation of the source requirements.

### Intersection

Implicit intersection is rejected. Shared spelling, similar meaning or
duplicate bodies do not establish a common requirement. A composite may
explicitly select or define requirements, but it must record source dispositions
and cannot infer semantic intersection.

### Explicit composed requirement set

The composite edition contains the complete normative requirement set to be used
for assessment. This is the selected model.

### Independent conformance

Independent conformance remains valid and is the default when no composite
edition exists. Each exact Profile edition receives its own D7 assessment and
outcome. No merged outcome is inferred.

## Conflict definition

A composition conflict exists only when exact, deterministically understood
requirements or composition constraints:

1. are jointly applicable under at least one same explicit assessable context;
2. constrain the same or interacting semantic target, scope or policy dimension;
3. cannot all be satisfied by any subject state in that context.

Examples include:

- one requirement requires material that another prohibits in the same scope;
- `max_count = 1` and `min_count = 2` over the same target and count scope;
- mutually exclusive closure policies for the same Projection scope;
- exact Vocabulary requirements that target one exclusive slot and allow no
  common exact edition or explicit alternative;
- required materialization combined with a prohibition on carrying or
  referencing the same required context;
- Projection scope constraints whose simultaneous satisfaction is impossible.

These are not conflicts by themselves:

- two different requirements;
- two Profiles addressing different semantic dimensions;
- different requirement IDs;
- duplicate requirements;
- different serialization order;
- disjoint applicability contexts;
- unsupported requirement semantics;
- unavailable component artifacts;
- different but jointly satisfiable exact Vocabulary requirements.

```text
conflict
!= difference

conflict
!= duplicate requirement

conflict
!= unsupported

conflict
!= unavailable
```

Conflict determination uses only explicit assessable information and exact
locally supplied or exactly supported semantics. Hidden ambient state, GUI state,
network responses, model judgment or implementation preference cannot determine
whether requirements conflict.

## Conflict handling

A valid composite Profile edition must expose a complete conflict-free resolved
requirement set.

A known unresolved conflict prevents the composition declaration from
establishing a valid composite Profile edition. It is a defect in the composed
policy, not a violation by the assessed subject.

If conflict analysis cannot be completed because a component artifact is
unavailable or an exact requirement semantics is unsupported, composition
verification is unavailable or indeterminate. That condition is not itself a
conflict and is not subject non-conformance.

D8 does not encode composition conflict as any D7 requirement outcome:

```text
Profile/Profile conflict
!= violated
!= unsupported
!= unavailable
```

Those D7 outcomes describe assessment of one subject against one already
identified exact Profile edition. Composition validation and its diagnostics are
a separate architectural dimension. A future binding may define
composition-specific diagnostics, but D8 does not define their serialized
taxonomy.

Conflict resolution occurs at composite authoring time. Any resolution must be
explicit in the final requirement set and lineage and therefore changes the
composite edition when changed.

## No implicit precedence

D8 prohibits composition semantics based on:

- first wins;
- last wins;
- array order;
- lexical order;
- higher or newer version wins;
- more specific name wins;
- registry priority;
- implementation priority;
- source artifact location;
- confidence score;
- AI judgment.

If a future composite policy needs a replacement, it expresses a new explicit
composite requirement and source dispositions. D8 defines no general precedence
operator for Profile binding 0.1.

## Requirement applicability

Profile composition and requirement applicability remain separate.

A composite requirement retains an explicit applicability descriptor that is
deterministically assessable under ADR-0028. Two requirements with disjoint
applicability do not conflict merely because their bodies would be incompatible
if applied together.

Composition must not introduce executable selectors or hidden Profile-selection
rules. It cannot choose a winning Profile from ambient state.

## Requirement modes

Composition preserves D5/D7 semantics for `required`, `optional` and
`prohibited`.

```text
optional
!= weak

required
!= high priority

prohibited
!= override
```

A mode difference may contribute to a real incompatibility, such as one
requirement mandating material that another prohibits under the same
applicability. It is not resolved by priority.

## Vocabulary policy

Component and composite Vocabulary requirements retain exact Vocabulary family,
exact version, exact term and explicitly allowed alternative semantics.

Composition never infers:

- newer edition wins;
- compatible edition substitutes automatically;
- similar term satisfies the requirement;
- namespace prefix equality proves Vocabulary identity;
- an ADR-0023 compatibility claim resolves conflict automatically.

Two exact Vocabulary requirements conflict only when their jointly applicable
constraints cannot both be satisfied. Requiring two Vocabulary editions is not
automatically a conflict when both can coexist.

A composite author may define an explicit resolving requirement with exact
allowed alternatives, but that is a new composite requirement with lineage and
requires a new composite edition when changed.

## Relationship with D7

ADR-0030 remains unchanged:

```text
one D7 assessment
=
one subject
+ one exact Profile edition
```

A valid composite Profile edition satisfies the singular Profile side of that
equation. D7 assesses the subject against the composite edition as one exact
Profile edition.

D8 does not add `profile_editions[]`, merged requirement results, aggregate
outcomes or Profile/Profile conflict diagnostics to
`ai-context-assessment-json/0.1.0`.

Independent assessments remain independent. Two conformant results do not imply
composite conformance. One conformant and one indeterminate result do not
authorize an invented merged result.

Conformance to a composite Profile edition does not imply conformance to any or
every component Profile edition. Component provenance does not inherit component
conformance, including when every component requirement was adopted unchanged.
A conformance result against a component requires a separate D7 assessment of
the same subject against that exact component Profile edition.

```text
component provenance
!= inherited component conformance

all component requirements adopted unchanged
!= automatic D7 result for the component
```

## Subject assessment versus composition verification

Ordinary D7 subject assessment against a composite Profile edition uses that
edition's complete resolved requirement set. It does not traverse component
artifacts and does not verify that the composite was validly authored.

Independent composition verification is a separate operation. Exact component
artifacts may be required to verify component provenance, exhaustive
dispositions, lineage, conflict resolution and overall composition validity.
When an exact component artifact is missing, composition provenance or validity
may remain unverified or verification may be incomplete. Missing component
artifacts do not create a subject requirement outcome of `unavailable`, do not
make the subject nonconformant and do not trigger a fetch.

D8 defines no composition-verification result artifact or diagnostic taxonomy.
Those remain future work separate from the D7 subject-assessment result.

## Binding and version consequence

ADR-0029 `ai-context-json/0.1.0` has closed grammar and does not contain
normative component, lineage, disposition or conflict-resolution slots. A
Profile must not add those slots under the same binding version.

A normative serialized composite Profile therefore requires a future exact
version of the `https://geesno.com/binding/ai-context-json` binding family whose
grammar represents:

- composite Profile identity;
- exact component Profile editions;
- complete resolved requirement set;
- requirement origins and dispositions;
- explicit conflict resolutions;
- finite acyclic component provenance.

D8 selects a later Profile requirement binding version rather than changing the
accepted D7 assessment binding. The exact future version token, member names,
schema and media type remain downstream binding work.

A coordination artifact over independent results, if standardized later, would
be a different artifact role and would not create composite conformance.

```text
representation
!= semantic authority

new normative composition slots
=> new accepted binding version

new composition slots
!= silent extension of 0.1.0
```

## Composite completeness and reproducibility

A composite edition carries a complete resolved requirement set. Component
references alone are insufficient because they would make semantics depend on
dynamic import, artifact availability or resolver behavior.

Changing a component edition without changing the composite edition is invalid.
Changing only the component list while retaining the same resolved set is also a
normative composition change because provenance and dispositions changed.

A composition is independently reproducible when the exact composite artifact
and exact component artifacts are locally supplied and their exact semantics are
understood. Missing component artifacts prevent or leave incomplete independent
verification of composition provenance or validity; they do not trigger network
fetch and do not become subject `unavailable`, subject nonconformance or a
subject requirement violation.

## Offline behavior

Composition must be interpretable and verifiable from finite locally supplied
exact artifacts and exact locally supported semantics.

D8 requires no:

- registry;
- remote resolver;
- automatic Profile fetch;
- network access;
- moving alias;
- latest edition lookup;
- model invocation;
- external arbitration service.

An IRI is identity, not a retrieval command. A missing component is unavailable
evidence, not permission to substitute another edition.

## AI and execution boundary

Composition artifacts and requirements are inert data. Conflicts must not be
resolved through:

- LLM judgment;
- semantic similarity;
- embedding ranking;
- confidence scoring;
- natural-language preference;
- model-provider policy;
- tool execution;
- source mutation;
- workflow order.

A composition declaration does not define execution order, validation pipeline
order, retrieval order or tool-call order.

## Cross-domain validation

| Domain | Composition stress case | Result under the decision |
| --- | --- | --- |
| Engineering object graph | One Profile requires source bindings for selected objects and another requires self-contained material context. | An explicit composite can adopt both when satisfiable; no CAD-specific primitive is introduced. |
| Spreadsheet/table | One Profile constrains column Vocabulary terms and another constrains row cardinality. | Different dimensions compose without being mislabeled as conflict. |
| Technical/legal document | One Profile requires Review context while another prohibits carrying a protected source excerpt. | The composite must express a conflict-free explicit materialization/reference policy. |
| Software repository | One Profile requires exact Revision context and another requires module relationship closure. | Exact source semantics remain descriptive and do not introduce Git execution. |
| Scientific dataset | Profiles require incompatible exact unit Vocabularies for one exclusive field. | This is a Vocabulary conflict unless an explicit exact alternative resolves it. |
| Generic product/asset | Supplier and catalog Profiles reuse the same requirement_id token. | Source-edition qualification prevents collision and accidental deduplication. |

The decision requires no IFC, PDF, Git, Excel, SQL, vendor, model or runtime
primitive.

## Adversarial cases

| # | Case | D8 handling | Incorrect interpretation rejected |
| --- | --- | --- | --- |
| 1 | P1 and P2 appear in an array | They remain multiple references. | Array means merged Profile. |
| 2 | P1 appears before P2 | Order has no priority. | First Profile wins. |
| 3 | P2 has a newer-looking version | Exact editions remain unordered opaque tokens. | Newer Profile overrides. |
| 4 | P1 requires X and P2 prohibits X in the same context | Known unresolved conflict blocks a valid composite. | Assessor chooses one. |
| 5 | P1 sets max_count 1 and P2 sets min_count 2 for the same target/scope | Known unresolved cardinality conflict. | Both are applied optimistically. |
| 6 | Profiles require incompatible exact Vocabulary editions for one exclusive slot | Conflict unless an explicit exact resolving requirement exists. | Newer or similar Vocabulary wins. |
| 7 | Same requirement_id text occurs in two Profile editions | Qualify by exact source Profile edition. | Text token is globally unique. |
| 8 | Two independent assessments are conformant | Keep two independent conformant results. | Composite conformant result exists. |
| 9 | One assessment is conformant and one is indeterminate | Keep both outcomes. | Invented merged outcome. |
| 10 | One component Profile is unavailable locally | Independent composition verification is incomplete or unverified; no fetch or subject outcome occurs. | Network retrieval, conflict or subject unavailability. |
| 11 | Component reference uses latest | Not an exact component edition. | Moving alias is reproducible. |
| 12 | Profile A depends on B and B depends on A | Invalid cyclic composition. | Runtime recursion resolves it. |
| 13 | A nested composite depends transitively on itself | Invalid transitive cycle. | Nested cycle is harmless. |
| 14 | Profile conflict is represented as subject violated | Use composition-specific validation, not D7 violation. | Subject caused Profile conflict. |
| 15 | Profile conflict is represented as requirement unsupported | Conflict and assessor capability remain distinct. | Conflict equals unsupported. |
| 16 | Schema adds profile_editions[] to D7 binding 0.1.0 | Schema is ahead of accepted grammar and invalid. | D8 silently changes D7. |
| 17 | Implementation chooses the most specific Profile name | No implicit precedence exists. | Naming determines authority. |
| 18 | An LLM chooses the conflict winner | No deterministic composition was established. | Model judgment is normative. |
| 19 | Exact source requirement is copied without origin traceability | Invalid composite provenance. | Copy loses source authority. |
| 20 | Composition artifact location is treated as identity | Identity remains profile_family plus exact profile_version. | URL or path is Profile identity. |
| 21 | A component version changes but composite identity remains unchanged | Invalid edition immutability. | Component updates are transparent. |
| 22 | Requirement order is used as override | Order remains non-semantic. | Last requirement wins. |
| 23 | Compatibility claim is used to resolve Vocabulary conflict automatically | Claim is inert unless an explicit composite requirement uses exact alternatives. | Compatibility implies substitution. |
| 24 | One component is omitted from a new composition | Explicit disposition or new composition is required; omission is not deletion. | Component Profile was deleted. |
| 25 | Composition declaration is read as execution order | It is inert policy/provenance data. | Components execute sequentially. |
| 26 | Colliding requirement IDs are deduplicated | Preserve edition-qualified origins and distinct requirements. | Same token means same requirement. |
| 27 | Missing component artifact is labeled conflict | Composition verification remains incomplete or unverified. | Missing evidence equals conflict or a subject outcome. |
| 28 | A finite acyclic nested composite supplies a complete resolved set | It may be a valid exact component. | All nesting is forbidden or unlimited recursion is required. |
| 29 | Incompatible bodies have disjoint applicability contexts | They need not conflict because they are not jointly applicable. | Difference always means conflict. |
| 30 | Composite silently changes an adopted requirement body | Create a distinct composite requirement with explicit lineage and new edition. | Composition rewrites source meaning. |
| 31 | Component P has R1, R2 and R3, but the composition mentions only R1 and R2 | Composition provenance is incomplete until R3 is explicitly adopted, replaced or excluded. | Unmentioned R3 is implicitly irrelevant. |
| 32 | A component requirement disappears because the author calls it not relevant | Explicit exclusion is required. | Relevance silently removes a requirement. |
| 33 | Composite excludes one P1 requirement and the subject conforms to the composite | No P1 conformance follows; P1 needs a separate D7 assessment. | Composite conformance implies P1 conformance. |
| 34 | Composite adopts every P1 requirement unchanged | Component provenance is preserved, but no automatic D7 result against P1 exists. | Full adoption inherits P1 conformance. |
| 35 | A component artifact is missing during ordinary D7 assessment against a complete composite | Assess the composite resolved set; no composite requirement becomes unavailable automatically. | D7 traverses or fetches the component. |
| 36 | A component artifact is missing during independent composition verification | Verification is incomplete or composition provenance remains unverified, not subject nonconformance. | Missing evidence is a subject violation. |

## Consequences

- S4 gains an accepted optional composition model without making composition
  mandatory.
- Normative composition creates one explicit composite Profile edition with its
  own exact identity and complete reproducible requirement set.
- Multiple Profile references and independent assessments remain non-composite.
- Requirement authority and identity remain scoped to exact source editions;
  composite lineage preserves origins and resolves ID collisions without array
  positions.
- Every requirement occurrence in every exact component requirement set has
  exactly one explicit adopted, replaced or excluded disposition; no implicit
  irrelevance or silent omission exists.
- Composite conformance does not imply component conformance, even when all
  component requirements are adopted unchanged; each component result requires
  a separate D7 assessment.
- Ordinary D7 assessment uses only the complete composite resolved set, while
  independent composition verification may require exact component artifacts.
- Known unresolved conflicts prevent a valid composite edition and remain
  separate from D7 subject conformance outcomes.
- Implicit precedence, dynamic import, automatic merge and AI arbitration are
  rejected.
- Composite dependency graphs are finite, exact-edition and acyclic.
- D7 assessment binding `0.1.0` remains unchanged and singular.
- Normative composition representation requires a future new exact
  `ai-context-json` binding version; no schema or version token is created here.
- No schema, fixture, evaluator, SDK, CLI, runtime, registry, resolver,
  packaging, publication, tag, release or execution behavior is introduced.

## Remains open

- exact future Profile binding version token and closed composition grammar;
- concrete composition artifact schema and media type;
- composition-specific diagnostic/result serialization;
- normative fixtures for composite Profile validity and conformance;
- authority/publication governance for concrete composite editions;
- integrity, signatures and canonical bytes if later required;
- coordination artifacts over independent D7 results;
- S5 mature conformance and diagnostic governance;
- SDK/tooling behavior.

## Acceptance record

**Decision status: Accepted**

Accepted by explicit human architecture decision on 2026-09-27. Acceptance
closes S4 D8 Profile composition and conflict policy and completes the planned
S4 architecture decisions D1-D8. It does not complete the S4 milestone or
implement or accept a new binding version, schema, fixtures, evaluator, SDK,
CLI, runtime, registry, resolver, packaging, publication, tag, release or
execution behavior.
