# Repository validation

Install the pinned dependencies and run the integrated suite from the
repository root:

```shell
python -m pip install -r requirements-conformance.txt
python tools/validation/reference_cli.py validate-repository
python tools/validation/reference_cli.py validate-document path/to/document.json
```

The reference CLI is repository-local tooling, not a stable public API or a
semantic authority. `validate-repository` runs these mandatory components:

- repository structure, documentation, scope and frozen-baseline guards;
- S2 Core Layers 0-3 conformance;
- Core/Profile/Extension/exact-version integration boundaries;
- S4 AI Context acceptance and frozen benchmark reproduction;
- S5 assessment-result corpus validation;
- focused I5 deterministic requirement-assessment tests; and
- focused I6 aggregation/result-construction tests.

The suite blocks socket creation and name resolution while it runs. It performs
no IRI dereference, registry lookup, model invocation or cloud call, and it does
not mutate the checked artifacts. Exit code `0` means every mandatory component
passed; exit code `1` means at least one conformance component failed; command
invocation/configuration errors use a nonzero code. The human-readable output
is not a normative GeesNO.Semantic artifact format.

`validate-document` reads one supplied SemanticDocument and reuses the exact S2
Layers 0-3 parser, version dispatch, Draft 2020-12 schema validation and
semantic checker. It never repairs, normalizes, rewrites, fetches or
dereferences the input. A valid document returns `0`; invalid, unsupported or
otherwise nonconforming input returns `1`; and an unreadable/missing path or
invocation/configuration error returns `2`.

Individual checks remain available for focused development:

```shell
python tools/validation/check_repository.py
python conformance/runner/run.py
python tools/benchmark/ai_context_s4_exit.py
python -m unittest discover -s tools/validation/tests -v
```

`check_repository.py` protects repository structure and scope; it is not the
integrated suite. The S2, S4 and S5 modules retain ownership of their existing
validation behavior, while `integrated_conformance.py` only orchestrates them.
