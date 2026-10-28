# Contributing to GeesNO.Semantic

**Status:** Contribution policy for the GeesNO.Semantic source distribution. Public Preview `0.1.0-preview.1` remains
a release candidate and has not been finalized.

GeesNO.Semantic is pre-1.0 work. This policy defines the public
contribution route without changing the standard or creating a certification
program.

## Start Here

Before proposing a change, read:

1. [ARCHITECTURE.md](ARCHITECTURE.md) for the architectural baseline and
   project boundaries;
2. the [Documentation Map](docs/README.md) for authority and reading order;
3. the [Implementation Guide](docs/implementation-guide.md) and
   [Conformance Guide](docs/conformance-guide.md); and
4. [LICENSES.md](LICENSES.md) for the license applying to the target material.

Keep GeesNO.Semantic descriptive, domain-neutral, format-neutral,
software-neutral and independent from GeesNO.Core. Do not add product adapters,
execution semantics, automatic dereference or hidden runtime behavior.

## Contribution Routes

The prepared issue templates distinguish documentation/navigation problems,
implementation/tooling bugs, conformance discrepancies and
specification/architecture proposals.

Use an issue before substantial work when the change may affect normative
meaning, compatibility, licenses, security boundaries or multiple repository
layers. Small unambiguous editorial fixes may be proposed directly once public
intake is activated.

Security issue? Stop and follow [SECURITY.md](SECURITY.md). Do not disclose a
vulnerability through a public issue or pull request.

## Normative Changes

Normative work follows the applicable portion of this order:

```text
issue / discussion
-> ADR when an architectural decision is required
-> specification
-> schema or formal constraints
-> conformance fixtures
-> SDK / tooling
-> examples
-> CHANGELOG
```

Not every contribution needs every step. A normative change must never be
introduced silently through SDK-only, schema-only, example-only or README-only
behavior. Domain-specific meaning belongs in a Vocabulary, Profile, Extension
or qualified locator unless it survives the universal-core test.

## Tests And Review Information

Describe what changed, why it changed, whether normative meaning is affected
and which checks were run. The repository baseline includes:

```shell
python tools/validation/check_repository.py
python conformance/runner/run.py
python -m unittest discover -s tools/validation/tests -v
python -m unittest discover -s sdk/python/tests -v
```

Run the focused checks relevant to the change as well. Do not include private,
customer, security-sensitive or third-party data unless its use and license
have been explicitly approved.

## License And DCO Sign-Off

A contribution is offered under the license applying to its target material,
as mapped by [LICENSES.md](LICENSES.md). Human-readable
specification/documentation material is generally CC BY 4.0, while schemas,
code, tests and tooling are generally Apache-2.0. The map controls mixed
material.

Contributors retain copyright in their contributions and certify their right
to submit them using the unmodified
[Developer Certificate of Origin 1.1](https://developercertificate.org/).
Each contributed commit must include:

```text
Signed-off-by: Name <email>
```

Use `git commit --signoff` to add the line. This repository does not adopt a
CLA, copyright assignment, project-specific contributor license or relicensing
grant for the initial Public Preview. Any future relicensing capability
requires separate legal and governance review.

External contribution intake requires a maintainer-designated public endpoint and
remains subject to the review and acceptance boundary below. The DCO/no-CLA
model does not imply that the controlled Public Preview release is complete.

## Review And Acceptance

Maintainers decide whether a submission is accepted under the applicable
project governance and authority hierarchy. No voting body, committee or
quorum is created here.

```text
submission != acceptance
passing tests != normative approval
merged code != certification
```

Normative proposals still require the applicable human decision and ADR or
specification process. The established licensor, CC BY attribution identity and
copyright-holder statement are recorded in `LICENSES.md`. This policy does not
alter those statements or invent a separate legal entity.

## Conduct And Publication Boundary

Professional, respectful and technically focused interaction is expected. No
formal Code of Conduct is adopted by this policy; whether one is desired is a
deferred human governance decision.

```text
contribution workflow available when a public endpoint is designated
!= submission accepted

Public Preview 0.1.0-preview.1 - planned release; not yet finalized
Public contribution endpoint: not established by this distribution
```

