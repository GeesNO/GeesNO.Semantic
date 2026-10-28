# GeesNO.Semantic Architecture



GeesNO.Semantic is an open, universal and descriptive semantic standard for representing meaning, context, relationships, provenance, confidence, review and lifecycle information independently of any specific software product, file format, domain or AI provider.



This document defines the public architectural baseline of GeesNO.Semantic.



Detailed normative semantics are defined by the specifications and accepted Architecture Decision Records in this repository. JSON Schema and reference implementations validate or implement accepted semantics; they do not originate them.



## 1. Scope



GeesNO.Semantic describes information.



It does not execute applications, invoke tools, control workflows, define agent behavior or provide an application runtime.



```text

GeesNO.Semantic = meaning / context / semantic description

execution systems = operations / capabilities / runtime behavior

```



GeesNO.Semantic is independent of GeesNO.Core and of any other execution framework.



## 2. Universal design



The universal layer must remain:



- software-neutral;

- format-neutral;

- domain-neutral;

- AI-provider-neutral;

- implementation-language-neutral;

- usable without network access;

- deterministically interpretable from explicit data and exact local semantics.



No universal primitive may exist only because one application, file format, industry, model provider or runtime needs it.



Domain-specific meaning belongs in vocabularies, profiles or external application layers rather than in the universal Core.



## 3. Descriptive, not executable



Semantic information is inert data.



A semantic assertion, profile declaration, binding, provenance record, confidence value, review record or extension must not become an instruction to execute software.



Semantic meaning must not depend on:



- tool execution;

- workflow order;

- model invocation;

- hidden application state;

- ambient runtime state;

- automatic remote resolution;

- proprietary application behavior.



## 4. Core architectural distinctions



These distinctions are fundamental:



```text

Concept != Representation



semantic identity

!= representation

!= source locator



Source != Entity



Binding != semantic truth



Profile != Core != Vocabulary



schema validation != complete semantic conformance



SDK behavior != normative authority



IRI != retrieval instruction

```



A representation may describe or encode a concept without becoming that concept.



A locator may help find data without becoming semantic identity.



A Source identifies origin or source material; it is not automatically the Entity described by that material.



A Binding correlates exactly one Entity with exactly one Source. The existence of a Binding does not itself establish semantic truth.



## 5. Identity and namespaces



Published GeesNO.Semantic namespace identifiers use:



```text

https://geesno.com/

```



as the stable public identity authority.



GitHub, package registries, websites and files may host representations of the standard, but they are not the semantic identity authority.



An identifier under `geesno.com` does not require runtime dereferencing.



Conforming implementations must be able to operate with locally supplied artifacts and exact locally supported semantics.



Network access may be useful for discovery or documentation, but it is not a semantic requirement.



## 6. Universal information model



The Core model provides universal semantic building blocks such as:



- SemanticDocument;

- Entity;

- Concept;

- Representation;

- Source;

- Binding;

- assertions;

- properties;

- relations;

- Provenance;

- Confidence;

- Review;

- Revision and Change;

- Extension.



Exact structure and semantics are defined by the corresponding specifications and accepted ADRs.



The Core must not become a universal ontology containing every possible domain concept.



## 7. Vocabularies



Domain and application meaning should normally be expressed through explicit vocabularies rather than by expanding the universal Core.



A Vocabulary defines terms and their intended meaning within an identified vocabulary family and edition.



Vocabulary identity, term identity and compatibility must remain explicit.



Similarity, newer versions, matching labels or matching namespace prefixes do not automatically establish semantic equivalence.



## 8. Profiles



A Profile defines an explicit semantic contract for a particular usage context while preserving the universal Core.



Profiles are not execution policies.



A Profile may constrain or require semantic material, but it must not define tool calls, runtime workflows, hidden model behavior or application control.



Profile editions are exact. Implementations must not silently substitute `latest`, compatible-looking or newer editions.



The AI Context Profile is one optional Profile. It does not make the Core AI-specific.



## 9. Representations and serialization



Meaning is defined independently from any single serialization.



JSON is the initial reference serialization, not the definition of the semantic model itself.



Future serializations may represent the same accepted semantics without changing the Core merely because their syntax differs.



```text

semantic model

!= JSON

!= JSON Schema

!= storage format

```



Schemas validate accepted representational structure. They do not create semantic meaning absent from the specification.



## 10. Embedded, sidecar and external adoption



GeesNO.Semantic supports non-destructive adoption.



Semantic material may be:



- embedded in a source format where appropriate;

- stored as a sidecar;

- stored externally;

- exposed through a software interface.



These deployment patterns do not change the semantic model.



A source application or file format does not gain authority over universal Semantic meaning merely because it stores or transports it.



## 11. Adapters and integrations



The universal GeesNO.Semantic repository does not define product-, vendor-, format- or domain-specific adapters.



Adapters may exist in external projects.



An adapter translates between an external system and GeesNO.Semantic. It must not redefine the universal semantic model.



```text

adapter behavior != Core semantics

```



Execution and product integration remain outside the universal standard unless explicitly standardized by a future architectural decision.



## 12. Extensions



Extensions provide a controlled mechanism for carrying additional semantic material without modifying the universal Core.



Extensions are inert.



An Extension must not become a mechanism for hidden execution semantics, application commands, model-provider instructions or undeclared Core replacement.



Unknown Extension content must remain distinguishable from accepted Core semantics.



## 13. Provenance, confidence and review



Provenance, Confidence and Review are first-class semantic context.



They remain distinct concepts.



```text

provenance != confidence

confidence != review

review != semantic truth

```



A confidence value does not make an assertion true.



A review record does not automatically establish universal authority.



Provenance describes origin and derivation rather than execution history.



## 14. Offline and deterministic behavior



Core interpretation and conformance must be possible without network access.



A missing remote artifact must not trigger automatic retrieval merely because an identifier is an IRI.



Conforming processing must not require:



- network access;

- registry lookup;

- automatic dependency download;

- model invocation;

- semantic-similarity inference;

- embedding search;

- external arbitration.



Where exact external semantic material is required, its absence is handled explicitly rather than silently substituted.



## 15. Conformance



Conformance is determined by the normative specifications, accepted bindings, exact Profile editions where applicable, and the corresponding conformance rules.



JSON Schema validation is only one layer of validation.



```text

schema-valid

!= automatically semantically conformant

```



Reference conformance tooling must be deterministic and usable offline.



Conformance tooling does not constitute certification and does not grant authority to an implementation.



## 16. Reference SDK



The reference SDK exists to demonstrate and test implementation of accepted semantics.



It is non-normative.



```text

specification / accepted ADR

> schema

> conformance fixtures and rules

> reference SDK convenience behavior

```



An SDK must not introduce semantic rules absent from accepted architecture and specification.



Other languages and implementations may implement the standard independently.



## 17. Versioning



Normative editions and bindings use explicit versions.



Implementations must not infer compatibility from:



- version ordering alone;

- similar structures;

- matching labels;

- newer editions;

- implementation convenience.



Changes to accepted normative grammar or semantics require an explicit versioned architectural and specification change.



## 18. Security and privacy



Semantic documents may contain sensitive information.



The standard must support explicit, minimal and non-destructive representation without requiring unnecessary disclosure.



Semantic metadata must not silently authorize execution, access or trust.



Security policy for the repository is documented separately in `SECURITY.md`.



## 19. Architectural authority



The public architecture is expressed through:



1. this architectural baseline;

2. normative specifications under `spec/`;

3. accepted Architecture Decision Records under `adr/`;

4. exact schemas and binding artifacts where a specification assigns them normative representational status;

5. deterministic conformance artifacts.



Where explanatory documentation conflicts with normative specification, the normative specification governs.



Where a schema appears to introduce semantics absent from accepted specification or architecture, the schema does not create those semantics.



## 20. Project rule



GeesNO.Semantic must remain a universal semantic layer for expressing meaning and context without becoming a file format, application runtime, execution framework, proprietary integration layer or domain-specific ontology.
