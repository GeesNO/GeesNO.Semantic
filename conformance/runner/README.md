# S2 reference conformance runner

Run from the repository root:

```shell
python conformance/runner/run.py
```

Install `requirements-conformance.txt` first. The runner performs strict
BOM-free UTF-8/duplicate-aware parsing, exact `spec_version` dispatch, local
Draft 2020-12 validation and deterministic semantic/integrity checks. With no
arguments it discovers all valid/invalid fixtures and compares each result with
its same-stem expected JSON file. Paths may also be supplied for focused JSON
diagnostic output.

Resource refusal is reported separately from invalidity. Profile-specific
Layer 4 checks, stable public diagnostic wording and SDK behavior are outside
the approved S2 baseline.

`jsonschema` supplies standards-compliant Draft 2020-12 validation and
`rfc3987-syntax2` supplies syntax-only RFC 3987 IRI validation. Both are pinned
reference-tooling dependencies; neither library, Python nor this runner is part
of the normative abstract model. Runtime validation uses only local artifacts
and performs no network access.
