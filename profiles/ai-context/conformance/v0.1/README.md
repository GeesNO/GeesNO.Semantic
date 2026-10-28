# AI Context Profile 0.1 S4 acceptance corpus

**Status: S4 I4 NORMATIVE ACCEPTANCE FIXTURES / REPOSITORY-LOCAL NON-NORMATIVE CHECKER.**

This finite corpus demonstrates critical accepted D2-D6 invariants for exact AI
Context Profile edition `0.1.0` and `ai-context-json/0.1.0`. It is separate from
the S2 Layers 0-3 corpus and is not the mature S5 conformance suite.

```text
fixture index
!= normative artifact grammar

test pass/fail
!= D7 conformance-result serialization
```

Fixture expectations and the one case-specific continuation expectation live in
`tools/validation/ai_context_acceptance.py`, outside every artifact. The
`fixture-record-set` and `fixture-anchor` values are deliberately small,
explicit Profile-defined values used only by this corpus. They are not a query
language, public API or general scope grammar.

All fixtures use the source companion
`sources/source-context.json`. That companion is a valid synthetic S2
SemanticDocument and contains no product-, format- or provider-specific data.

## Valid fixtures

| Fixture | Layer | Invariant demonstrated | Source |
| --- | --- | --- | --- |
| `valid/v01-complete-narrow.json` | structural + semantic | Complete relative to a narrow declared scope; source subset does not imply partial. | `sources/source-context.json` |
| `valid/v02-bounded-partial-truncation.json` | structural + semantic | Explicit finite bound plus established truncation requires partial. | `sources/source-context.json` |
| `valid/v03-bounded-unknown.json` | structural + semantic | Bounded plus unknown is valid when truncation and known omission are not established. | `sources/source-context.json` |
| `valid/v04-material-context-carried.json` | structural + semantic | Material Provenance, Confidence, Review, Validity and host scope are carried exactly. | `sources/source-context.json` |
| `valid/v05-exact-external-reference.json` | structural + semantic | Exact external reference may be sufficient without target materialization or network access. | `sources/source-context.json` |
| `valid/v06-explicit-omission-partial.json` | structural + semantic | Known material omission is explicit and partial; omission is not deletion or preservation. | `sources/source-context.json` |
| `valid/v07-omission-dependency-continuation.json` | structural + semantic | Explicit omission and dependency continuation may coexist for one material dependency. | `sources/source-context.json` |
| `valid/v08-projection-continuation.json` | structural + semantic | Remaining same-scope content uses Projection continuation, distinct from dependency continuation. | `sources/source-context.json` |
| `valid/v09-material-source.json` | structural + semantic | A material Source retains exact origin context without becoming truth or Entity identity. | `sources/source-context.json` |
| `valid/v10-material-binding.json` | structural + semantic | A material Binding retains exact Entity/Source anchors, locator and method. | `sources/source-context.json` |
| `valid/v11-external-reference-closure.json` | structural + semantic | External references are allowed but not required; V1 supplies the self-contained counterpart. | `sources/source-context.json` |
| `valid/v12-unknown-extension-carried.json` | structural + semantic | A material unknown Extension remains inert and is preserved exactly on its host. | `sources/source-context.json` |

## Invalid fixtures

| Fixture | Expected rejection | Exact invariant |
| --- | --- | --- |
| `invalid/i01-wrong-binding.json` | structural | Binding family/version must be exact. |
| `invalid/i02-unknown-grammar-member.json` | structural | D6 binding-defined objects are closed. |
| `invalid/i03-missing-projection-group.json` | structural | Every Projection requires the root Projection-scope group. |
| `invalid/i04-missing-namespace-context.json` | semantic | Every compact carried term must expand offline through the preserved namespace map. |
| `invalid/i05-identity-rewritten.json` | semantic | Projection must not assign a local replacement identity to carried source content. |
| `invalid/i06-reference-retargeted.json` | semantic | A carried S2 reference target must remain exact. |
| `invalid/i07-truncation-without-partial.json` | structural | Established truncation requires `projection_completeness = partial`. |
| `invalid/i08-omission-marked-complete.json` | semantic | Known required in-scope omission is inconsistent with complete. |
| `invalid/i09-unknown-hides-known-partial.json` | semantic | Unknown cannot hide a known required omission. |
| `invalid/i10-bound-misreported-as-truncation.json` | semantic | A reached bound does not establish truncation when the declared fixture scope is fully carried. |
| `invalid/i11-projection-continuation-for-dependency.json` | semantic | Projection continuation cannot satisfy a dependency-continuation requirement. |
| `invalid/i12-dependency-continuation-for-projection.json` | semantic | Dependency continuation cannot satisfy explicit known remaining same-scope continuation context. |
| `invalid/i13-material-carry-dropped.json` | semantic | `carry_required` cannot be replaced by reference-only handling. |
| `invalid/i14-fabricated-reference-sufficiency.json` | semantic | Exact-reference sufficiency requires an exact carried reference and consistent availability. |
| `invalid/i15-missing-material-source.json` | semantic | Material Source participation requires the exact Source record to be carried. |
| `invalid/i16-missing-material-binding.json` | semantic | Material Binding participation requires the exact Binding record to be carried. |
| `invalid/i17-locator-promoted-to-identity.json` | semantic | Locator value is not Entity identity. |
| `invalid/i18-unresolved-descriptor-reference.json` | semantic | Every local descriptor reference must resolve. |
| `invalid/i19-descriptor-reference-wrong-group.json` | semantic | Descriptor reference group and target occurrence must agree. |
| `invalid/i20-duplicate-descriptor-identity.json` | semantic | A descriptor token is unique across one Projection artifact. |
| `invalid/i21-reference-availability-inconsistent.json` | semantic | `carried` availability requires the target body to be carried. |
| `invalid/i22-unknown-extension-altered.json` | semantic | Losslessly carried unknown Extension payload and host scope must not change. |

The checker validates only existing artifacts. It does not generate
Projections, retrieve references, execute continuation metadata, access the
network or define stable public diagnostics.
