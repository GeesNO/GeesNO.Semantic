# GeesNO.Semantic Conformance Guide

**Status:** NON-NORMATIVE conformance guidance for GeesNO.Semantic.
**License:** [CC BY 4.0](../LICENSE-SPECIFICATION), as assigned by the
[repository license map](../LICENSES.md).

This guide explains existing conformance contracts and repository workflows.
It creates no requirement, outcome, diagnostic, certification program or
normative API. If it conflicts with an authoritative specification or artifact,
the authoritative source wins.

[ARCHITECTURE.md](../ARCHITECTURE.md) defines the public architectural
baseline. The [Accepted ADRs](../adr/README.md) refine that baseline, followed
by the exact normative contracts linked below.

The route is language-neutral, SDK-independent and offline-capable. Python is
needed only to run the repository's reference tooling. An independent
implementation may use any language and equivalent local processing.

## 1. Start With an Exact Assessment

Before running a check, identify all four parts:

```text
assessment subject
exact contract
exact version or Profile edition
applicable validation path
```

Do not replace them with a broad statement such as "the product is compliant."
An artifact result establishes only what was assessed against the named exact
contract. Passing fixture corpora with an implementation is useful compatibility
evidence, but it does not prove that every future product output conforms.

Keep these claim scopes distinct:

```text
artifact conformance
!= test-suite compatibility
!= implementation-wide behavior
!= product certification
```

The [Public Preview boundary](../PUBLIC_PREVIEW.md) controls factual claim
wording. Conformance always remains separate from truth and authority:

```text
conformance
!= semantic truth
!= human Review
!= permission
!= endorsement
!= certification

diagnostic
!= Assertion
```

## 2. Select the Applicable Route

| Subject and question | Exact route | Primary authority |
| --- | --- | --- |
| Is one SemanticDocument valid under exact Core JSON `spec_version` `0.1.0`? | Bare-Core Layers 0-3 | [Core conformance specification](../spec/conformance.md) |
| Does one AI Context artifact satisfy the exact JSON binding and accepted Profile semantics? | AI Context structural and semantic Profile acceptance | [AI Context Profile](../spec/ai-context-profile.md), [JSON binding](../spec/ai-context-json-binding.md) |
| How is one subject assessed requirement-by-requirement against exact AI Context Profile edition `0.1.0`? | AI Context deterministic assessment and result construction | [Assessment binding](../spec/ai-context-assessment-json-binding.md) |
| Are all repository baselines mutually consistent? | Integrated repository workflow | [Integrated checker](../tools/validation/integrated_conformance.py) |

```text
bare-Core conformance
!= Profile conformance
```

Profile conformance does not replace bare-Core conformance unless an exact
accepted Profile contract explicitly defines that relationship. The current
AI Context material keeps the paths separate. Do not infer composition,
inheritance, precedence or automatic aggregation between contracts.

## 3. Bare-Core Layers 0-3

The [normative Core conformance contract](../spec/conformance.md) composes these
four deterministic layers in this order and under these official names:

1. **Layer 0 - raw input:** size/resource policy, BOM-free UTF-8, Unicode scalar
   validity, strict JSON, one object root, duplicate decoded member rejection
   and exact retention of JSON numeric tokens.
2. **Layer 1 - version dispatch:** canonical SemVer and exact supported
   `spec_version` `0.1.0`. A well-formed unsupported version produces the
   distinct `unsupported-version` result; it never selects a nearby schema.
3. **Layer 2 - schema:** local Draft 2020-12 validation against the closed
   [Core schema](../schema/v0.1/geesno-semantic.schema.json), without network
   access.
4. **Layer 3 - semantic/integrity:** the deterministic identity, reference,
   namespace, numeric/trust, set, calendar, interval, lifecycle graph and
   related checks enumerated by the Core conformance specification.

```text
load or parse success
!= schema validity
!= complete Core conformance
```

A library constructing an object does not prove conformance. Layer 2 proves
only the formal structural constraints represented by the schema. Layers 0, 1
and 3 remain required by the normative Core conformance process.

Resource refusal is separate from semantic invalidity. Concrete byte, depth,
collection or numeric limits used by one processor are safety controls unless
the authoritative contract makes a particular bound normative.

## 4. Core Corpus and Expected Outcomes

The [Core suite](../conformance/README.md) contains:

- [`conformance/valid/`](../conformance/valid/README.md): 17 documents expected
  to pass exact bare-Core Layers 0-3;
- [`conformance/invalid/`](../conformance/invalid/README.md): 84 inputs expected
  to be rejected, reported unsupported or refused at their documented layer;
- [`conformance/expected/`](../conformance/expected/README.md): 101 same-stem
  expected result records; and
- [`conformance/runner/`](../conformance/runner/README.md): the non-normative
  reference implementation of the approved process.

These counts describe the current finite corpus, not the conceptual limit of
the standard. Valid fixtures are accepted conformance fixtures, not tutorial
authority and not an exhaustive enumeration of valid documents. Invalid
filenames and Python implementation details do not create normative rules.
Expected records are formal evidence for their paired corpus inputs; they do
not make human-readable diagnostic wording normative.

An independent validator demonstrates compatible Core behavior by producing
the same expected outcome for every applicable fixture, without needing the
same code or language.

## 5. Run the Core Reference Workflow

The reference tools use the pinned packages listed in
[`requirements-conformance.txt`](../requirements-conformance.txt). Installing
those packages is a tooling setup step, not a dependency of the semantic
standard:

```shell
python -m pip install -r requirements-conformance.txt
```

From the repository root, run the complete Core corpus:

```shell
python conformance/runner/run.py
```

Validate one external or repository-local SemanticDocument through the same
Layers 0-3 path:

```shell
python tools/validation/reference_cli.py validate-document conformance/valid/minimal-document.json
```

These are reference repository workflows, not normative APIs.
The reference runner is Python; the conformance contract is not.

For `validate-document PATH`, the input is the named file, output is a concise
tool report, and the accepted repository CLI uses exit status `0` for valid,
`1` for conformance failure and `2` for invocation/read/configuration failure.
Those codes are tool behavior, not semantic outcome vocabulary and not a
promise of a separately published stable CLI.

## 6. Core Result Boundaries

Keep route-specific states distinct:

| State | Meaning in the current Core workflow |
| --- | --- |
| Parse/load success | Raw data was read; no schema or full-conformance claim follows. |
| `unsupported-version` | The declared version is well formed but not the exact supported contract. No fallback occurs. |
| Resource refusal | Local safety policy declined processing; this is not semantic invalidity. |
| Layer 0 failure | Raw byte/JSON processing contract failed. |
| Layer 1 failure | Version declaration/dispatch contract failed or is unsupported. |
| Layer 2 failure | Draft 2020-12 structural validation failed. |
| Layer 3 failure | A deterministic semantic/integrity constraint failed. |
| `valid` | The exact subject passed all applicable Core Layers 0-3. |

This table explains existing classifications. It is not a new unified error
taxonomy. Python exceptions and exact diagnostic messages remain
non-normative.

## 7. AI Context Profile 0.1 Path

The exact Profile path uses these identities:

```text
profile family  = https://geesno.com/profile/ai-context
profile edition = 0.1.0

binding family  = https://geesno.com/binding/ai-context-json
binding version = 0.1.0

Projection artifact_kind = projection_artifact
```

Read the [Profile semantics](../spec/ai-context-profile.md), exact
[Profile requirement artifact](../profiles/ai-context/v0.1/profile.json),
[JSON binding](../spec/ai-context-json-binding.md) and
[Profile schema](../profiles/ai-context/schema/v0.1/ai-context.schema.json).

One assessment uses one exact Profile edition. Do not select `latest`, a
similar edition, a registry result or an automatic substitution. Binding
declaration and Profile declaration do not prove Profile conformance.

```text
Projection != SemanticDocument
Projection != new semantic truth
```

Assessment does not mutate the source SemanticDocument, resolve references,
follow continuation metadata or retrieve missing content.

## 8. Structural and Semantic Profile Acceptance

The [AI Context acceptance corpus](../profiles/ai-context/conformance/v0.1/README.md)
has three separate expected classes:

```text
12 valid
4 structural-invalid
18 semantic-invalid
```

Structural validation applies the exact binding grammar and Profile schema.
Semantic validation applies the additional deterministic accepted invariants
implemented by the repository-local checker. The
[binding validation matrix](../spec/ai-context-json-binding.md#structural-versus-semantic-validation-matrix)
states which responsibility belongs where; the schema is not the complete
Profile definition.

Run the current reference acceptance check:

```shell
python tools/validation/ai_context_acceptance.py
```

The checker and fixture index are evidence for the exact finite corpus. They do
not create a general Profile evaluator, stable public diagnostics or result
artifact grammar.

## 9. AI Context Assessment and Result Model

The normative
[AI Context Assessment JSON binding](../spec/ai-context-assessment-json-binding.md)
represents assessment of exactly one subject against exactly one Profile
edition. Its binding identity and artifact kind are:

```text
binding family  = https://geesno.com/binding/ai-context-assessment-json
binding version = 0.1.0
artifact_kind   = conformance_result_artifact
```

The assessment model preserves these separate responsibilities:

```text
assessment subject
exact Profile edition
requirement-level assessment
aggregate result
diagnostics
result artifact
```

Requirement outcomes are exactly:

```text
satisfied
violated
not_applicable
unsupported
unavailable
```

Overall outcomes are exactly:

```text
conformant
nonconformant
indeterminate
```

`not_applicable`, `unsupported` and `unavailable` are not aliases for `false`,
`missing` or `error`. `indeterminate` is neither `conformant` nor
`nonconformant`. In the absence of a decisive violation, unsupported or
unavailable applicable requirements and structural/interpretation blockers
lead to `indeterminate` under the accepted aggregation rules. A decisive
applicable violation retains precedence. Severity and array order never choose
the outcome.

## 10. Diagnostics and Result Artifacts

Diagnostics report assessment context using only the exact code/category and
severity vocabulary defined by the assessment binding:

```text
diagnostic
!= semantic Assertion
!= human Review
!= permission
!= conformance outcome by itself
```

Diagnostic severity (`info`, `warning`, `error`) does not redefine requirement
or aggregate outcomes. A message, locator or related reference is reporting
data, not semantic identity or a new graph edge.

The [assessment-result schema](../profiles/ai-context/schema/v0.1/ai-context-assessment.schema.json)
validates the closed representation. The
[assessment corpus](../profiles/ai-context/assessment-conformance/v0.1/README.md)
separates 12 valid artifacts, 18 Layer A schema rejections, one reused Core
Layer 3 temporal rejection and three Layer B binding-local integrity
rejections. These representation checks do not themselves implement general
requirement evaluation or aggregation.

The human-readable
[AI Context assessment corpus catalogue](../conformance/ai-context-assessment-corpus.md)
records the complete `V01-V12`, `I01-I22` and `S01-S24` inventory and its fixed
expectations without replacing the normative binding or executable fixtures.

## 11. AI Context Reference Workflows

Run the materialized result-artifact corpus:

```shell
python tools/validation/ai_context_assessment_corpus.py
```

Run the focused requirement-assessment and result-construction tests:

```shell
python -m unittest tools.validation.tests.test_ai_context_requirement_assessment -v
python -m unittest tools.validation.tests.test_ai_context_result_construction -v
```

Run the complete offline repository integration directly or through the
repository CLI:

```shell
python tools/validation/integrated_conformance.py
python tools/validation/reference_cli.py validate-repository
```

The integrated workflow runs eight repository components: repository guard,
Core conformance, Core/Profile/Extension/version boundaries, AI Context
acceptance, the reproducibility benchmark, assessment-result corpus,
requirement assessment and result construction. `PASS (8 components)` proves that repository state reproduced
those checks. It is not certification of every future implementation.

For `validate-repository`, the accepted repository CLI uses exit status `0`
when all components pass, `1` when a component fails and `2` for an invocation
or configuration failure. The CLI observes existing checks; it is not semantic
authority and defines no new result artifact.

## 12. Independent Validator Criterion

An independent implementation can reproduce conformance without importing
`sdk/python`, `geesno_semantic`, `SemanticDocument`, `Projection` or any SDK
class. Its conceptual route is:

1. Read the exact authoritative specifications and formal artifacts.
2. Implement safe raw-input processing.
3. Dispatch by exact supported version or Profile edition.
4. Apply the exact local schema.
5. Implement the specified deterministic additional constraints.
6. Run every applicable fixture.
7. Compare results with the expected outcomes.

```text
independent implementation
+ same applicable fixture outcomes
= evidence of compatible conformance behavior
```

This is evidence, not certification, endorsement or proof about all possible
product outputs. The Python SDK reuses the process but neither defines nor is
required by it.

## 13. Making a Bounded Factual Conformance Statement

A factual statement identifies:

- the exact assessed artifact or subject;
- exact GeesNO.Semantic `spec_version`;
- exact Profile family and edition when applicable; and
- the actual result produced by the applicable deterministic process.

Examples within the scope defined by [PUBLIC_PREVIEW.md](../PUBLIC_PREVIEW.md) are:

```text
Conforms to GeesNO.Semantic spec_version 0.1.0 under Core Layers 0-3

Conforms to AI Context Profile https://geesno.com/profile/ai-context
exact edition 0.1.0
```

Use them only for the exact subject that actually produced the stated result.
Do not claim `GeesNO-certified`, `officially certified`, `officially approved
implementation`, `endorsed by GeesNO`, `1.0 compatible`, future-version
compatibility or whole-product conformance without separate explicit authority.

No badge, certificate, signed attestation, submission service, hosted
validator or certification database exists in this repository.

## 14. Offline and Security Boundary

Every reference validation path above uses local artifacts and must run without
network, cloud service, `geesno.com` dereference, registry, resolver, LLM or AI
provider. IRIs identify resources; they are not retrieval commands.

Treat inputs, Extensions, messages, locators and context values as untrusted.
Safe processing covers invalid UTF-8, duplicate members, oversized input, deep
nesting, large collections and numeric abuse as assigned by the exact contract
and local resource policy. Do not expose redacted data through diagnostics or
turn an implementation limit into universal semantic invalidity.

## 15. Traceability Matrix

| Guide topic | Normative authority | Formal/reference artifact |
| --- | --- | --- |
| Core processing and Layers 0-3 | [spec/conformance.md](../spec/conformance.md) | [Core schema](../schema/v0.1/geesno-semantic.schema.json), [Core suite](../conformance/README.md) |
| Core exact version and JSON contract | [JSON serialization](../spec/json-serialization.md) | Core schema and same-stem expected records |
| AI Context Profile semantics | [spec/ai-context-profile.md](../spec/ai-context-profile.md) | [Profile `0.1.0`](../profiles/ai-context/v0.1/profile.json) |
| AI Context representation | [spec/ai-context-json-binding.md](../spec/ai-context-json-binding.md) | [Profile schema](../profiles/ai-context/schema/v0.1/ai-context.schema.json) |
| AI Context structural/semantic acceptance | Profile and binding specifications | [AI Context corpus](../profiles/ai-context/conformance/v0.1/README.md), [reference checker](../tools/validation/ai_context_acceptance.py) |
| Assessment outcomes, aggregation and diagnostics | [Assessment binding](../spec/ai-context-assessment-json-binding.md), Accepted ADR-0030 | [Assessment schema](../profiles/ai-context/schema/v0.1/ai-context-assessment.schema.json) |
| Assessment evidence | [Assessment binding](../spec/ai-context-assessment-json-binding.md) | [Assessment corpus](../profiles/ai-context/assessment-conformance/v0.1/README.md), [58-case catalogue](../conformance/ai-context-assessment-corpus.md), [requirement assessment](../tools/validation/ai_context_requirement_assessment.py), [result construction](../tools/validation/ai_context_result_construction.py) |
| Integrated repository workflow | Existing exact contracts above | [integrated checker](../tools/validation/integrated_conformance.py), [reference CLI](../tools/validation/reference_cli.py) |
| Public claim boundary | [PUBLIC_PREVIEW.md](../PUBLIC_PREVIEW.md) | No certification artifact |

## 16. Preview and Claim Boundaries

The
[cross-domain learning examples](../examples/cross-domain/public-preview/README.md)
are validated through the same Core Layers 0-3, but remain tutorials:

```text
learning example != conformance fixture
```

This guide defines no general Profile evaluator, Profile composition runtime,
registry, resolver, network service, SDK API, badge or certification program.

For release scope and bounded public claims, see
[PUBLIC_PREVIEW.md](../PUBLIC_PREVIEW.md).

This guide remains non-normative and does not override accepted architecture,
specification, schema or conformance material.
