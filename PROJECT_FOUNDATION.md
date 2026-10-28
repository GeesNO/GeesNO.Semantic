# GeesNO.Semantic — Foundational Design Background

**Role:** Historical design background; not the current conformance contract.

The public architectural baseline is [ARCHITECTURE.md](ARCHITECTURE.md).
[Accepted ADRs](adr/README.md), the [specification index](spec/README.md)
and exact versioned artifacts define the applicable public contracts.

The design material below preserves the initial architectural rationale and
exploratory proposals. Later accepted decisions govern wherever they refine
or replace an initial proposal. Examples and provisional ideas below do not
create alternate serialization or conformance requirements.

# 1. Executive definition

## 1.1 What GeesNO.Semantic is

**GeesNO.Semantic is an open, software-agnostic, AI-oriented semantic standard for describing what data, objects, concepts and relationships exist in a file, document, model or software-produced dataset, and what they mean.**

Its primary purpose is to let an AI system understand technical or general-purpose digital information **faster, with less ambiguity, with less repeated interpretation and with a smaller context/token cost** than if the AI had to reverse-engineer the native format every time.

The standard must be usable by:

- any software vendor;
- any open-source project;
- any individual developer;
- any company;
- any user;
- any AI provider;
- any LLM or future AI architecture;
- any file format or application domain.

GeesNO.Semantic is not tied to CAD, BIM, architecture, construction or engineering. Those are important use cases and useful validation domains, but **they must not shape the universal core in a way that prevents use elsewhere**.

---

## 1.2 Core question answered by the standard

GeesNO.Semantic answers:

> **What exists in this information, what does it mean, how is it related, where did it come from, and how confidently can that meaning be trusted?**

It does **not** answer:

> What action should be executed on software?

Execution belongs outside GeesNO.Semantic.

---

# 2. Fundamental project boundary

## 2.1 GeesNO.Semantic is descriptive, not executable

The standard describes information. It does not command applications.

It may describe:

- identity;
- concepts;
- representations;
- types/classifications;
- properties;
- units;
- relationships;
- source bindings;
- provenance;
- confidence;
- human review state;
- revisions;
- changes;
- extensions;
- compact AI context.

It must not define a runtime that:

- creates objects in software;
- moves objects;
- deletes objects;
- edits native documents;
- invokes application commands;
- controls GUIs;
- executes tools;
- manages permissions for software execution;
- performs transaction orchestration.

---

## 2.2 Relationship with GeesNO.Core

**GeesNO.Semantic and GeesNO.Core are independent projects.**

They may be complementary, but neither is required by the other.

The conceptual boundary is:

```text
GeesNO.Semantic
    = understanding / meaning / context

GeesNO.Core
    = operations / capabilities / validation / execution / traceability
```

Hard rules:

1. GeesNO.Semantic MUST NOT import, depend on or require GeesNO.Core.
2. GeesNO.Core does not need to know that GeesNO.Semantic exists.
3. A product may implement only GeesNO.Semantic.
4. A product may implement only GeesNO.Core.
5. A product may independently use both.
6. Integration between them, if ever demonstrated, belongs in examples/integration projects, not in either universal core.

The former idea of a separate **SCA / Semantic CAD Actions** standard is discontinued as part of GeesNO.Semantic. Executable actions are outside this project and must not be recreated here.

---

# 3. Non-goals

GeesNO.Semantic is deliberately **not**:

- an AI agent;
- an LLM;
- an AI provider API;
- a universal file parser;
- a universal file converter;
- a CAD system;
- a BIM system;
- an IFC replacement;
- a DWG replacement;
- a PDF replacement;
- a database engine;
- an execution runtime;
- a workflow engine;
- an MCP server requirement;
- a plugin framework;
- an adapter marketplace;
- a product-specific ontology;
- a mandatory cloud service;
- a proprietary file format intended to replace native formats.

The project must resist scope creep toward any of these.

---

# 4. Design principles

The following principles are foundational.

## 4.1 Universal core, domain-neutral by construction

The core model MUST NOT contain mandatory concepts such as:

- wall;
- beam;
- column;
- room;
- invoice;
- spreadsheet cell;
- medical record;
- image layer;
- code function.

Those may exist in vocabularies or profiles outside the universal core.

The universal core provides the mechanisms to express them.

---

## 4.2 Meaning is separate from representation

A real or logical concept may have one or more digital representations.

Example:

```text
Concept: Structural Column P-12

Representations:
- object in a DWG
- object in an IFC
- object in a Revit model
- row in a quantity table
- symbol in a PDF
```

The project preserves the useful predecessor distinction:

- **Concept** — the logical, semantic or real-world thing.
- **Representation** — a particular digital manifestation of that concept.

A representation can exist before its semantic meaning is known and can be enriched later.

---

## 4.3 Identity, geometry/representation, semantics and source remain separable

The predecessor SCC architecture identified four useful concerns:

- identity;
- representation/geometry;
- semantics;
- source.

GeesNO.Semantic generalizes this beyond CAD.

Geometry becomes only one possible representation payload/reference. A representation may instead be text, a table row, a raster region, a database record, a time series, a code symbol or another digital form.

---

## 4.4 Incremental semantics

A dataset MUST be allowed to be partially semantic.

An entity may be:

- identified but unclassified;
- classified but missing properties;
- automatically classified with low confidence;
- human-reviewed;
- related to other entities later;
- enriched across revisions.

The standard must never require perfect semantic completeness as a condition for usefulness.

---

## 4.5 Provenance is first-class

Every important semantic assertion should be able to state how it was obtained.

Possible origins include:

- authored by source software;
- imported from a native property;
- inferred by deterministic rule;
- inferred by AI;
- provided by user;
- mapped from another standard;
- externally curated.

This lets AI distinguish facts from inference.

---

## 4.6 Confidence and review are first-class

An AI-oriented semantic standard must distinguish certainty from interpretation.

Assertions may include:

- confidence score;
- review state;
- reviewer or process identifier;
- timestamp;
- evidence/reference;
- provenance.

A source-authoritative property does not need to be treated the same as a weak AI guess.

---

## 4.7 Non-destructive adoption

GeesNO.Semantic MUST NOT require rewriting a native file.

Three implementation patterns are valid:

### Embedded
The native software or format stores GeesNO.Semantic information internally.

### Sidecar
A semantic document exists next to the source file.

Example:

```text
building.ifc
building.ifc.geesno-semantic.json
```

### External
Semantic data is stored in an external database, service or knowledge store and linked to the native source.

All three are valid implementations of the same semantic model.

---

## 4.8 AI-provider neutrality

No normative structure may depend on:

- OpenAI;
- Anthropic;
- Google;
- Microsoft;
- Meta;
- a specific model family;
- a proprietary embedding system;
- a specific prompt syntax.

The standard describes meaning; AI providers consume it.

---

## 4.9 Human readability without sacrificing machine rigor

The canonical representation must be:

- deterministic enough to validate;
- easy to inspect;
- compact enough for AI tooling;
- explicit about units and identifiers;
- usable without a specialized binary decoder.

The initial reference serialization should therefore be JSON + JSON Schema, while the abstract semantic model remains serialization-independent.

JSON-LD/RDF mappings may be explored later, but MUST NOT be mandatory in the first stable core if they materially increase implementation complexity.

---

## 4.10 Specification-first development

The normative order is:

```text
conceptual model
    ↓
specification
    ↓
schema / formal constraints
    ↓
conformance tests
    ↓
reference SDK / tooling
```

The SDK is never allowed to silently become the specification.

If schema, SDK and normative specification disagree, the conflict must be resolved explicitly with an ADR/change record.

---

# 5. Universal information model

GeesNO.Semantic must evolve around a small set of universal primitives.

The initial model should contain the following concepts.

## 5.1 SemanticDocument

Container for one semantic dataset.

Minimum responsibilities:

- standard/version declaration;
- document identity;
- source references;
- entity collection or index;
- namespaces/vocabularies;
- revision information;
- extensions;
- optional conformance profile declaration.

---

## 5.2 Entity

Universal identifiable semantic unit.

An entity should support at least:

- stable semantic ID;
- entity kind;
- label/name when available;
- type/classification assertions;
- properties;
- relations;
- provenance;
- confidence/review metadata;
- source bindings;
- extensions.

Initial entity kinds:

- `concept`
- `representation`

Additional kinds must not be introduced casually. Prefer semantic typing/extensions over growing the universal enum.

---

## 5.3 Concept

A logical, semantic or real-world thing independent of a particular file representation.

Examples are intentionally cross-domain:

- a structural element;
- a customer;
- a contractual requirement;
- a machine component;
- a room;
- a product;
- a software module;
- a measured quantity.

The core does not define those domain types; vocabularies do.

---

## 5.4 Representation

A digital occurrence or representation of a concept.

A representation should be able to reference:

- source document/application;
- native object ID;
- location/range/record;
- optional geometry reference;
- optional content fingerprint;
- concept it represents;
- representation-specific properties.

---

## 5.5 Source and Binding

A binding connects semantic identity to native information.

Possible bindings include:

- file + native object ID;
- file + page + bounding region;
- database + table + primary key;
- workbook + sheet + cell/range;
- source repository + file + symbol;
- application + document + object ID;
- URI/resource identifier.

The core must support extensible binding types without requiring one universal parser.

---

## 5.6 Type / Classification Assertion

Entities can have one or more semantic types.

Types should use qualified identifiers/namespaces so that multiple vocabularies can coexist.

Example:

```text
type: example.structures/column
```

The project must not attempt to create one giant mandatory ontology covering all industries.

Instead:

- the core defines how types are referenced;
- vocabularies define domain meaning;
- profiles define interoperable subsets when needed.

---

## 5.7 Property Assertion

Properties must support:

- property identifier;
- value;
- datatype;
- unit when applicable;
- provenance;
- confidence/review when applicable;
- validity/revision metadata when needed.

Values should allow common universal forms:

- string;
- boolean;
- integer;
- decimal;
- date/time;
- identifier/reference;
- measured quantity;
- list/set;
- structured value.

---

## 5.8 Relation

Relations connect entities.

Minimum model:

```text
subject --predicate--> object
```

Relations may carry:

- provenance;
- confidence;
- review;
- validity/revision information;
- extensions.

The core defines relation mechanics, not an exhaustive list of domain predicates.

---

## 5.9 Provenance

Provenance should allow an assertion to state:

- origin mechanism;
- source reference;
- actor/process/tool;
- timestamp;
- method;
- evidence reference;
- optional model/tool version.

The standard must distinguish authored/native data from derived/inferred data.

---

## 5.10 Confidence

Confidence is optional where information is authoritative, but available wherever information is inferred.

Recommended normalized range:

```text
0.0 .. 1.0
```

A confidence score MUST NOT substitute provenance or review state.

---

## 5.11 Review

Review represents validation/approval state independently from confidence.

Example states may include:

- `unreviewed`
- `accepted`
- `rejected`
- `corrected`

Exact normative vocabulary will be fixed during specification design.

---

## 5.12 Revision and Change

The model must support semantic evolution without losing identity.

It should eventually represent:

- document revision;
- entity added;
- entity modified;
- entity removed/tombstoned;
- semantic assertion changed;
- source binding changed;
- superseded assertion.

The initial SCC work on revisions, changes and tombstones should be reused where it remains domain-neutral.

---

## 5.13 Extensions

Extensibility is mandatory.

Rules:

1. Extensions must be namespaced.
2. Unknown extensions must not invalidate otherwise conforming core content unless a declared profile requires them.
3. Core identifiers must not be reused with incompatible meaning.
4. Experimental extensions should be clearly identifiable.
5. Extension data must not silently redefine normative core semantics.

---

# 6. Vocabularies and profiles

## 6.1 Do not build one universal ontology

Attempting to define every concept from every industry inside the GeesNO.Semantic core would make the standard impossible to stabilize.

Instead use three layers:

```text
GeesNO.Semantic Core
    universal mechanics

Vocabularies
    domain or organization concepts

Profiles
    interoperable subsets / rules for a use case
```

---

## 6.2 Base vocabulary

A very small base vocabulary may cover universally useful metadata such as:

- label;
- description;
- category/type;
- containment;
- part-of;
- derived-from;
- represents;
- same-as/equivalent when safely defined.

The base vocabulary must remain deliberately small.

---

## 6.3 Domain vocabularies

Domain vocabularies may be created by:

- GeesNO;
- standards bodies;
- software vendors;
- industry groups;
- companies;
- users;
- community projects.

GeesNO.Semantic does not require GeesNO itself to maintain CAD, BIM, construction, spreadsheet, image or other domain vocabularies.

The standard only needs a robust mechanism for registering/referencing them.

---

# 7. AI Context Profile

## 7.1 Why it exists

A complete semantic dataset can itself become too large for efficient AI use.

Therefore GeesNO.Semantic should define an **AI Context Profile**: a standardized compact projection of a larger semantic dataset optimized for language-model consumption.

This is a major project feature, but it remains descriptive rather than executable.

---

## 7.2 Core purpose

The AI Context Profile should allow a system to provide only the information relevant to a request while preserving:

- stable identity;
- semantic type;
- relevant properties;
- relevant relations;
- provenance/confidence when material;
- source bindings needed for traceability;
- omitted/continuation metadata so the AI knows the context is partial.

---

## 7.3 Example conceptual context

```text
GEESNO-SEMANTIC-CONTEXT/0.1

scope:
  source: model-A
  selection: [P12]

entity P12:
  type: structures/column
  level: level/02
  material: materials/concrete-C30
  dimensions: 300 mm x 400 mm

relations:
  supports -> B24, B25
  connected_to -> F07

provenance:
  classification: source-authored
  dimensions: source-authored

context_status:
  partial: true
  omitted_entities: 12427
```

This example is illustrative, not yet normative syntax.

---

## 7.4 Important boundary

The AI Context Profile defines the **shape and semantics of contextual information**.

It does not define:

- prompting strategies;
- model routing;
- retrieval algorithms;
- vector databases;
- RAG implementation;
- agent execution;
- tool calling.

Those are implementation concerns outside the standard.

---

# 8. Conformance levels

The predecessor SCC used L0/L1/L2 profiles. GeesNO.Semantic should retain the idea of progressive conformance, but the exact requirements must be revalidated for the universal scope before 1.0.

Provisional model:

## L0 — Identity / Binding

Minimum semantic envelope:

- document/version;
- entity identity;
- entity kind;
- source/binding sufficient to locate the represented native information.

Useful when meaning is not yet enriched.

## L1 — Semantic

L0 plus:

- semantic type/classification;
- properties;
- relations where applicable;
- namespaces/vocabulary references.

## L2 — Trusted / Lifecycle

L1 plus advanced integrity and lifecycle information such as:

- provenance;
- confidence;
- review;
- revision/change semantics;
- tombstones/supersession where applicable.

The project may later define separate profile names if clearer. Do not freeze these requirements until conformance tests prove that they work across unrelated domains.

---

# 9. Serialization strategy

## 9.1 Abstract model first

The normative semantic model must be independent of serialization.

## 9.2 Initial reference serialization

The first reference serialization should be:

- UTF-8 JSON;
- formally validated with JSON Schema;
- deterministic canonicalization rules where signatures/hashes require them;
- explicit versioning;
- explicit units;
- stable IDs;
- extension namespaces.

## 9.3 Future serializations

Potential future mappings may include:

- JSON-LD;
- RDF;
- CBOR or another compact binary representation;
- database mappings;
- streaming representations.

These should be added only when there is a demonstrated interoperability/performance need.

They must represent the same abstract model rather than creating incompatible semantic dialects.

---

# 10. Source-file implementation patterns

A conforming producer may expose GeesNO.Semantic through:

## 10.1 Embedded semantic data

Native application/file stores the semantic model internally.

## 10.2 Sidecar semantic data

Native file remains untouched and semantic data is adjacent.

Recommended provisional naming convention:

```text
<source-filename>.geesno-semantic.json
```

This is a project convention until formally standardized.

## 10.3 External semantic store

Semantic data lives elsewhere and references the source through stable bindings.

## 10.4 Live software endpoint

A software vendor may expose a semantic document/context dynamically through its own API.

This does not turn that API into part of the GeesNO.Semantic standard. Only the semantic payload/conformance is relevant.

---

# 11. Adapters: explicit project policy

**The GeesNO.Semantic project does not have the objective of building or maintaining application-specific adapters.**

Do not create mandatory adapters for:

- AutoCAD;
- BricsCAD;
- Revit;
- CYPE;
- IFC;
- PDF;
- Excel;
- Blender;
- proprietary software;
- any other application or format.

Any vendor, user, company or open-source developer may independently build a producer/consumer/adapter that maps native data to GeesNO.Semantic.

Reference examples may use small synthetic data generators to test the standard, but they must not evolve into product integrations inside the core repository.

If existing SCC CAD Adapter code exists elsewhere, treat it as an **external reference implementation/prototype**, not as part of the GeesNO.Semantic universal core.

---

# 12. What a software implementation should need to do

A software vendor wishing to support GeesNO.Semantic should be able to:

1. assign or expose stable semantic identities;
2. declare source/native bindings;
3. classify entities using one or more vocabularies;
4. expose semantic properties with datatypes and units;
5. expose relations;
6. expose provenance/review when needed;
7. serialize or serve a conforming GeesNO.Semantic document;
8. optionally produce an AI Context Profile projection.

A vendor does **not** need to expose its internal implementation details or proprietary file structure beyond the bindings it chooses to publish.

---

# 13. Security, privacy and trust

Even though GeesNO.Semantic is descriptive, the standard can expose sensitive information.

The specification must therefore state:

- semantic data inherits the sensitivity of the source information;
- producers should be able to omit/redact entities and properties;
- context profiles should declare that they are partial when redacted or filtered;
- provenance must not require personal data when a pseudonymous process/tool identity is sufficient;
- external references must not be automatically dereferenced by conforming consumers;
- semantic content must be treated as untrusted input by parsers;
- schemas and SDKs must defend against malformed/deeply nested/oversized input;
- embedded executable code is forbidden in the core format;
- extensions are data, not executable plugins.

The standard must never imply that semantic classification is automatically true simply because it is syntactically valid.

---

# 14. Versioning and compatibility

Use Semantic Versioning principles for released specifications and reference packages where practical.

Recommended lifecycle:

```text
0.x   design may evolve; migration allowed
1.0   first stable interoperability contract
1.x   backwards-compatible additions/clarifications
2.0   breaking semantic changes only when unavoidable
```

Rules:

- `spec_version` must be explicit in documents.
- Parsers should fail clearly on unsupported major versions.
- Unknown extensions should be preserved/ignored according to extension rules.
- Deprecated fields require a documented migration path.
- Breaking changes require an ADR and migration guide.
- The project must maintain a CHANGELOG.

The old SCC 1.0 label does not automatically make GeesNO.Semantic 1.0 stable. The universalized project begins at `0.1.0-dev`.

---

# 15. Licensing and openness strategy

## 15.1 Licensing objective

The licensing model must maximize adoption as an open sector standard while preserving:

- attribution;
- legal clarity;
- commercial implementation rights;
- vendor neutrality;
- the GeesNO name/brand;
- the integrity of official conformance claims.

The license must not force implementers to make their own applications open source merely because they implement the standard.

---

## 15.2 Recommended public licensing split

### A. Specification and explanatory documentation

Recommended license:

**Creative Commons Attribution 4.0 International (CC BY 4.0).**

Purpose:

- permits copying, redistribution and adaptation;
- permits commercial use;
- requires attribution;
- is suitable for openly reusable specification/documentation material.

Applies to, once public:

```text
/spec
/docs
/examples intended as documentation
published specification PDFs/HTML/Markdown
```

### B. Schemas, SDKs, conformance tooling and reference code

Recommended license:

**Apache License 2.0.**

Purpose:

- permissive commercial and non-commercial implementation;
- modification and redistribution allowed under its terms;
- no copyleft requirement on software that merely uses the implementation;
- includes an explicit patent-license framework for code contributions covered by the license.

Applies to, once public:

```text
/schema
/sdk
/conformance
/tools
reference source code
machine-readable vocabularies when treated as implementation artifacts
```

### C. Name, logos and official certification/conformance marks

The open licenses above **do not grant trademark rights**.

Reserve:

- `GeesNO`;
- `GeesNO.Semantic`;
- logos;
- visual identity;
- future official conformance/certification marks.

Create a separate `TRADEMARKS.md` before public 1.0.

Third parties may accurately state factual compatibility, for example:

> “Implements GeesNO.Semantic 1.0”

subject to the future trademark/conformance policy, but may not imply that their product is made, certified or endorsed by GeesNO unless formally authorized.

---

## 15.3 Phase-based licensing policy

### Phase S0–S4 — private/bootstrap development

Until the repository is intentionally published:

- copyright remains with the project owner/contributors;
- no external distribution is required;
- draft documents should be marked `DRAFT`;
- do not accidentally promise stable compatibility;
- license files may already be prepared so publication is deliberate rather than improvised.

### Phase S5–S7 — public preview / 0.x

When the project becomes publicly reusable:

- specification/docs: CC BY 4.0;
- code/schemas/tests/SDK: Apache-2.0;
- trademark rights reserved;
- versions clearly marked pre-1.0;
- conformance claims must identify exact spec/profile version;
- no party may claim official certification unless an official certification program exists.

### Phase S8–S9 — candidate and 1.0 standard

Maintain the same open licenses unless a legal review identifies a concrete problem.

Before final 1.0:

- publish `LICENSE-SPECIFICATION`;
- publish `LICENSE-CODE`;
- publish `NOTICE` where required;
- publish `TRADEMARKS.md`;
- publish `CONTRIBUTING.md`;
- publish `GOVERNANCE.md`;
- publish `SECURITY.md`;
- decide contributor sign-off policy;
- assess whether a formal royalty-free patent policy for essential specification claims is necessary.

---

## 15.4 Contributions

Before accepting substantial third-party contributions, define contributor terms explicitly.

Recommended initial low-friction model:

- contribution under the license applying to the target material;
- Developer Certificate of Origin (DCO) sign-off or equivalent contributor attestation;
- contributors retain their copyright;
- project maintainers retain governance over what enters the normative standard.

If future governance requires the ability to relicense specification material, obtain legal advice before adopting a CLA. Do not silently assume relicensing rights.

---

## 15.5 Patents

The project should aim for implementability without patent royalties.

Apache-2.0 provides patent provisions for covered code contributions, but specification-essential patent claims are a separate governance question.

Before a formal industry-standard 1.0 process involving external organizations, evaluate and document a **royalty-free essential-claims policy** if necessary.

This is a legal/governance task, not a reason to delay the technical 0.x prototype.

---

## 15.6 No forced commercialization model

GeesNO.Semantic itself should remain usable in open and commercial products under the applicable public licenses.

Commercial value may exist around it without restricting the standard, for example:

- proprietary applications implementing it;
- hosted services;
- semantic authoring tools;
- validation services;
- enterprise support;
- domain vocabularies;
- private extensions;
- certification services;
- integration/adapters maintained by third parties.

The universal standard should not require any of those services.

---

# 16. Governance principles

The long-term goal is credible sector adoption, therefore governance should eventually be more important than any one implementation.

Principles:

1. Public normative specification.
2. Versioned change history.
3. Architecture decisions recorded.
4. Backwards compatibility treated seriously after 1.0.
5. Vendor-neutral terminology.
6. No privileged AI provider.
7. No privileged software vendor.
8. Transparent conformance criteria.
9. Extensions allowed without fragmenting the core.
10. The official GeesNO.Semantic name remains governed so incompatible forks cannot present themselves as the official standard.

---

# 17. Repository architecture

Recommended initial repository:

```text
GeesNO.Semantic/
│
├─ README.md
├─ PROJECT_FOUNDATION.md
├─ CHANGELOG.md
├─ ROADMAP.md
├─ CONTRIBUTING.md                 # before public contributions
├─ SECURITY.md                     # before public preview
├─ GOVERNANCE.md                   # before 1.0
├─ TRADEMARKS.md                   # before public 1.0
├─ LICENSE-SPECIFICATION           # CC BY 4.0 when public
├─ LICENSE-CODE                    # Apache-2.0 when public
├─ NOTICE                          # as required
│
├─ spec/
│  ├─ semantic-core.md
│  ├─ identity.md
│  ├─ entities.md
│  ├─ properties.md
│  ├─ relations.md
│  ├─ provenance.md
│  ├─ revisions.md
│  ├─ extensions.md
│  └─ conformance.md
│
├─ schema/
│  ├─ v0.1/
│  │  └─ geesno-semantic.schema.json
│  └─ README.md
│
├─ vocab/
│  ├─ base/
│  └─ README.md
│
├─ profiles/
│  └─ ai-context/
│     ├─ README.md
│     └─ schema/
│
├─ conformance/
│  ├─ valid/
│  ├─ invalid/
│  ├─ expected/
│  └─ runner/
│
├─ sdk/
│  ├─ python/                       # first reference SDK, non-normative
│  └─ README.md
│
├─ examples/
│  ├─ generic/
│  ├─ cross-domain/
│  └─ ai-context/
│
├─ adr/
│  ├─ 0001-project-scope.md
│  ├─ 0002-semantic-vs-execution.md
│  ├─ 0003-serialization.md
│  └─ 0004-licensing.md
│
└─ tools/
   └─ validation/
```

**Do not create `/adapters` in the universal core repository.**

---

# 18. Development principles

These principles guide specification and implementation work.

## 18.1 Preserve scope

Never add execution semantics, software control or product-specific APIs to the universal core.

## 18.2 No hidden domain bias

Every required field must be defensible using at least three unrelated domains.

A useful review question for every mandatory concept is:

> Would this still make sense for a CAD model, a spreadsheet, a legal document, a software repository and a scientific dataset?

If not, it probably belongs in a vocabulary/profile/extension rather than the core.

## 18.3 No adapter creep

Do not add AutoCAD/Revit/IFC/PDF/etc. adapters to prove the architecture.

Use synthetic or generic examples for conformance.

## 18.4 Spec before implementation

For a normative change:

1. update/create ADR;
2. update specification;
3. update schema;
4. add valid/invalid conformance fixtures;
5. update SDK;
6. update examples;
7. update CHANGELOG.

## 18.5 Stable IDs

Do not use array position or transient runtime memory address as semantic identity.

## 18.6 Explicit units

Never infer units silently when a numeric value is a measured quantity unless a profile explicitly defines a default.

## 18.7 Unknown data

Distinguish:

- absent;
- unknown;
- not applicable;
- intentionally redacted.

Do not collapse these into the same value if the distinction matters semantically.

## 18.8 Derived data

AI/rule-derived semantic data must be capable of carrying provenance and confidence.

## 18.9 Deterministic validation

Conformance validation must not require an LLM.

LLMs may help create semantic content, but syntactic/profile conformance must be testable deterministically.

## 18.10 Backwards compatibility

Before 1.0, changes are allowed but migration must be documented.

After 1.0, breaking changes require a new major version.

## 18.11 Keep reference SDK non-normative

The SDK must implement the spec; the spec must not depend on quirks of the SDK.

## 18.12 Preserve source data

Tools in this repository must not modify original user documents unless a separate explicit tool outside the standard is designed for that purpose.

---

# 19. Initial technical choices

These are starting decisions, not all permanently frozen.

```text
Project name:            GeesNO.Semantic
Initial version:         0.1.0-dev
Normative model:         serialization-independent
Reference serialization: JSON / UTF-8
Validation:              JSON Schema
Reference SDK:           Python first
AI dependency:           none
Cloud dependency:        none
GeesNO.Core dependency:  none
Adapters in core repo:   none
Domain-specific core:    none
```

Python is recommended only as the first reference SDK because it is accessible for tooling and AI workflows. A conforming implementation in any language is equally valid.

---

# 20. Migration of useful SCC concepts

The following SCC concepts are strong candidates to preserve after universal review:

- Document;
- Entity;
- concept / representation split;
- persistent UUID/stable IDs;
- Source / native ID bindings;
- semantic assertions;
- property assertions;
- relations;
- provenance;
- confidence;
- review;
- binding;
- revisions / changes;
- extensions;
- progressive conformance levels;
- compact context generation for LLMs.

The following SCC-specific direction should **not** be part of the GeesNO.Semantic core:

- CAD-only assumptions;
- geometry as a mandatory universal property;
- AutoCAD/BricsCAD adapter ownership;
- CAD Capability Manifest as a core concept;
- SCA executable actions;
- MCP as a required runtime;
- a roadmap centered on IFC/PDF/Revit/CYPE adapters.

Existing SCC code should be reused only after checking that each part satisfies the domain-neutrality rules in this document.

---

# 21. Roadmap

## S0 — Repository bootstrap

Goal: create a clean universal project skeleton.

Deliverables:

- root documents;
- initial licenses prepared;
- ADR system;
- CI skeleton;
- formatting/linting rules;
- no product/domain adapters.

Exit criteria:

- project builds/tests in CI;
- project purpose is understandable from README + PROJECT_FOUNDATION;
- no CAD-specific dependency exists.

---

## S1 — Universal Core Model 0.1

Goal: define the abstract information model.

Deliverables:

- SemanticDocument;
- Entity;
- Concept;
- Representation;
- Source/Binding;
- Type assertions;
- Properties;
- Relations;
- Provenance;
- Confidence;
- Review;
- Revision/change;
- Extensions.

Exit criteria:

- model tested conceptually against at least five unrelated data domains;
- no mandatory domain-specific field remains.

---

## S2 — JSON Serialization + Schema 0.1

Goal: make the model mechanically representable and validatable.

Deliverables:

- JSON serialization rules;
- JSON Schema;
- identifier rules;
- datatype rules;
- unit representation rules;
- namespace rules;
- valid/invalid fixtures.

Exit criteria:

- deterministic validation;
- schema passes its own conformance suite;
- malformed cases are rejected with useful errors.

---

## S3 — Base Vocabulary + Extension Rules

Goal: provide minimal universal semantics without building a giant ontology.

Deliverables:

- tiny base vocabulary;
- vocabulary namespace mechanism;
- extension rules;
- collision/versioning rules;
- examples using third-party/custom vocabularies.

Exit criteria:

- two independent vocabularies can coexist in one document without ambiguity.

---

## S4 — AI Context Profile 0.1

Goal: define compact, traceable AI-readable context.

Deliverables:

- context profile model;
- projection rules;
- partial-context declaration;
- source/provenance retention rules;
- examples at different context sizes;
- token/size benchmark methodology.

Exit criteria:

- a large synthetic semantic dataset can produce a compact context without losing entity identity or material provenance;
- the output is model-provider neutral.

---

## S5 — Conformance Suite

Goal: make compatibility objectively testable.

Deliverables:

- core conformance tests;
- profile conformance tests;
- invalid edge cases;
- extension compatibility tests;
- version compatibility tests;
- command-line validation tool.

Exit criteria:

- a third party can determine whether its generated semantic document conforms without using any GeesNO cloud service.

---

## S6 — Reference SDK

Goal: make implementation easy without making the SDK normative.

First SDK: Python.

Minimum API areas:

- create/load/save document;
- validate;
- create concept/representation;
- bind source IDs;
- add types/properties/relations;
- add provenance/confidence/review;
- revision/change support;
- extension access;
- create/query AI context projection.

Exit criteria:

- SDK passes the same conformance fixtures as the schema;
- no SDK-only semantics exist.

---

## S7 — Public Preview 0.x

Goal: make the standard usable by external implementers.

Deliverables:

- public repository/release;
- CC BY 4.0 specification license;
- Apache-2.0 code license;
- implementation guide;
- conformance documentation;
- cross-domain examples;
- issue templates;
- contribution policy.

Exit criteria:

- an external developer can implement a producer/consumer using only public documentation.

---

## S8 — Interoperability Hardening

Goal: find hidden assumptions before 1.0.

Test with unrelated domains, for example:

- CAD/engineering-like object graph;
- spreadsheet/table data;
- technical PDF/document structure;
- source-code/project structure;
- generic product/asset dataset.

These are test datasets, not adapters.

Exit criteria:

- no core breaking issue discovered across test domains;
- ambiguities resolved in spec and conformance tests.

---

## S9 — GeesNO.Semantic 1.0

Goal: first stable universal standard.

Required before release:

- stable core specification;
- stable JSON serialization;
- stable extension mechanism;
- stable AI Context Profile or clearly versioned companion profile;
- conformance suite;
- reference SDK;
- licensing files;
- governance;
- trademarks policy;
- security policy;
- migration notes from 0.x;
- no unresolved critical architecture issue.

After 1.0, backward compatibility becomes a primary constraint.

---

## S10 — Ecosystem / governance expansion

Possible later work:

- additional reference SDK languages;
- community vocabularies;
- formal vocabulary registry mechanism;
- conformance badges/certification;
- performance profiles;
- streaming/compact serialization;
- standardized discovery metadata;
- formal standards-body collaboration if adoption warrants it.

None of these are prerequisites for proving the core idea.

---

# 22. Success metrics

GeesNO.Semantic should be evaluated on measurable interoperability and AI efficiency rather than only code volume.

Useful metrics:

## Semantic interoperability

- same concept can be represented from multiple source systems;
- stable identity survives representation changes;
- vocabularies can coexist;
- provenance survives transformation;
- third-party implementation passes conformance independently.

## AI efficiency

Benchmark against raw/native extracted data where feasible:

- context bytes/tokens required;
- time to locate relevant information;
- number of parsing/reasoning steps;
- factual extraction accuracy;
- relation-resolution accuracy;
- ambiguity/error rate;
- ability to cite native source bindings;
- context reduction ratio.

Do not claim a fixed percentage improvement until measured with repeatable benchmarks.

---

# 23. Key risks and defenses

## Risk: becoming a giant ontology
Defense: keep core mechanics small; move domain semantics to vocabularies/profiles.

## Risk: duplicating GeesNO.Core
Defense: no executable actions or runtime in GeesNO.Semantic.

## Risk: becoming another proprietary file format
Defense: support embedded, sidecar and external models; keep abstract model independent of transport.

## Risk: requiring GeesNO adapters for adoption
Defense: publish specification, schemas, SDK and conformance tests so anyone can implement it.

## Risk: being optimized for only CAD/BIM
Defense: cross-domain conformance examples required before 1.0.

## Risk: AI hallucinations becoming semantic facts
Defense: provenance + confidence + review + authoritative-source distinction.

## Risk: context packets hiding important omissions
Defense: partial/omitted/continuation metadata in AI Context Profile.

## Risk: fragmentation through extensions
Defense: namespaces, profiles, conformance rules and stable core IDs.

## Risk: open license diluting the official standard name
Defense: open specification/code licenses plus separate trademark and conformance policy.

---

# 24. Decisions currently considered CLOSED unless an ADR reopens them

1. Project name is **GeesNO.Semantic**.
2. Scope is universal, not CAD/BIM-specific.
3. Project is descriptive, not executable.
4. GeesNO.Core and GeesNO.Semantic are independent.
5. SCA is not part of GeesNO.Semantic.
6. No mandatory application-specific adapters belong in the core project.
7. Any third party may implement producers/consumers/adapters under the public standard licensing terms.
8. The semantic model supports Concept and Representation separately.
9. Provenance, confidence and review remain first-class capabilities.
10. Embedded, Sidecar and External storage are valid.
11. AI Context Profile is a first-class project objective.
12. The core is AI-provider neutral.
13. The abstract model is serialization-independent.
14. JSON + JSON Schema is the initial reference serialization/validation route.
15. Existing SCC work is input/prototype material, not automatically frozen GeesNO.Semantic 1.0.
16. GeesNO.Semantic begins as `0.1.0-dev`.
17. Conformance must be deterministic and not require an LLM.
18. The core must not define a giant universal domain ontology.
19. Specification/docs are intended for CC BY 4.0 at public release.
20. Schemas/SDK/tests/reference code are intended for Apache-2.0 at public release.
21. GeesNO/GeesNO.Semantic trademarks and official conformance marks remain reserved.

---

# 25. Questions intentionally left OPEN for implementation work

These must be resolved through ADRs rather than assumptions:

1. Exact stable-ID syntax: UUID, URI/IRI-capable ID, or both.
2. Exact namespace syntax and vocabulary versioning.
3. Exact measured-quantity/unit representation.
4. Exact shape of source bindings.
5. Whether assertions are represented inline or as first-class assertion objects in all cases.
6. Exact revision/change model.
7. Exact L0/L1/L2 requirements and naming.
8. Canonical JSON ordering/canonicalization requirements.
9. Exact AI Context Profile serialization.
10. Rules for chunking/continuation of very large semantic datasets.
11. Digital signature/integrity model, if required.
12. Registry/discovery mechanism for vocabularies, if any.
13. Formal patent/contributor policy before mature public governance.

Important architectural choices require explicit ADRs; exploratory proposals do not establish accepted contracts.

---

# 27. Definition of the long-term vision

The project succeeds when a software vendor, user or independent developer can expose semantic information from any digital source in a common open representation so that an AI does not need to rediscover the meaning of that source from scratch on every interaction.

The target architecture is therefore simple:

```text
ANY SOFTWARE / FILE / DATASET
            │
            │ produces or exposes
            ▼
    GEESNO.SEMANTIC
            │
            │ standard meaning/context
            ▼
        ANY AI SYSTEM
```

Optional implementations may create the semantic data through native support, sidecars, external stores or third-party tooling.

GeesNO.Semantic itself remains the **common semantic contract**, not the product-specific implementation.

---

# 28. One-sentence project rule

> **GeesNO.Semantic standardizes how meaning is represented for AI; it does not standardize how software is controlled.**
