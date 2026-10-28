"""Offline public-distribution guards; no private history or Git metadata required."""
from __future__ import annotations

import ast
import hashlib
import json
import re
import sys
from pathlib import Path
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[2]
VALIDATION_DIR = ROOT / "tools" / "validation"
if str(VALIDATION_DIR) not in sys.path:
    sys.path.insert(0, str(VALIDATION_DIR))
import publication_hygiene

PUBLIC_ARTIFACT_MANIFEST = ROOT / "tools/validation/public-artifacts.json"


AI_CONTEXT_SCHEMA = "profiles/ai-context/schema/v0.1/ai-context.schema.json"

AI_CONTEXT_ASSESSMENT_SCHEMA = (
    "profiles/ai-context/schema/v0.1/ai-context-assessment.schema.json"
)

PUBLIC_ARCHITECTURE = "ARCHITECTURE.md"

AI_CONTEXT_ASSESSMENT_CATALOG = "conformance/ai-context-assessment-corpus.md"

S5_CORPUS_INVENTORY = "spec/s5-assessment-corpus-inventory.md"

S7_P9_RECORD = "spec/s7-p9-publication-record.md"

RELEASE_NOTES = "RELEASE_NOTES.md"

CONTRIBUTING_POLICY = "CONTRIBUTING.md"

SECURITY_POLICY = "SECURITY.md"

PULL_REQUEST_TEMPLATE = ".github/PULL_REQUEST_TEMPLATE.md"

ISSUE_TEMPLATES = (
    ".github/ISSUE_TEMPLATE/documentation.md",
    ".github/ISSUE_TEMPLATE/tooling-bug.md",
    ".github/ISSUE_TEMPLATE/conformance-discrepancy.md",
    ".github/ISSUE_TEMPLATE/specification-proposal.md",
)

DOCUMENTATION_MAP = "docs/README.md"

IMPLEMENTATION_GUIDE = "docs/implementation-guide.md"

CONFORMANCE_GUIDE = "docs/conformance-guide.md"

PUBLIC_PREVIEW = "PUBLIC_PREVIEW.md"

OFFICIAL_LICENSE_SHA256 = {
    "LICENSE-SPECIFICATION": (
        "9ba9550ad48438d0836ddab3da480b3b69ffa0aac7b7878b5a0039e7ab429411"
    ),
    "LICENSE-CODE": (
        "cfc7749b96f63bd31c3c42b5c471bf756814053e847c10f3eb003417bc523d30"
    ),
}

SDK_I1_REQUIRED_FILES = (
    "sdk/README.md",
    "sdk/python/README.md",
    "sdk/python/geesno_semantic/__init__.py",
    "sdk/python/geesno_semantic/_s2.py",
    "sdk/python/geesno_semantic/document.py",
    "sdk/python/geesno_semantic/io.py",
    "sdk/python/geesno_semantic/validation.py",
    "sdk/python/tests/test_sdk_io_validation.py",
)

SDK_I2_REQUIRED_FILES = (
    "sdk/python/geesno_semantic/entities.py",
    "sdk/python/geesno_semantic/ids.py",
    "sdk/python/tests/test_sdk_document_entities.py",
)

SDK_I3_REQUIRED_FILES = (
    "sdk/python/geesno_semantic/assertions.py",
    "sdk/python/geesno_semantic/references.py",
    "sdk/python/geesno_semantic/sources.py",
    "sdk/python/geesno_semantic/values.py",
    "sdk/python/tests/test_sdk_sources_assertions_values.py",
)

SDK_I4_REQUIRED_FILES = (
    "sdk/python/geesno_semantic/trust.py",
    "sdk/python/tests/test_sdk_trust.py",
)

SDK_I5_REQUIRED_FILES = (
    "sdk/python/geesno_semantic/lifecycle.py",
    "sdk/python/tests/test_sdk_lifecycle.py",
)

SDK_I6_REQUIRED_FILES = (
    "sdk/python/geesno_semantic/extensions.py",
    "sdk/python/geesno_semantic/terms.py",
    "sdk/python/tests/test_sdk_extensions_vocabulary.py",
)

SDK_I7_REQUIRED_FILES = (
    "sdk/python/geesno_semantic/projection.py",
    "sdk/python/tests/test_sdk_projection.py",
)

SDK_I8_REQUIRED_FILES = (
    "sdk/python/tests/test_sdk_exit_audit.py",
)

AI_CONTEXT_PROFILE = "profiles/ai-context/v0.1/profile.json"

AI_CONTEXT_CORPUS = "profiles/ai-context/conformance/v0.1"

AI_CONTEXT_ASSESSMENT_CORPUS = (
    "profiles/ai-context/assessment-conformance/v0.1"
)

EXPECTED_AI_CONTEXT_REQUIREMENTS = (
    {
        "requirement_id": "projection-baseline",
        "requirement_kind": "projection",
        "requirement_mode": "required",
        "applicability": {
            "subject_category": "projection_artifact",
            "basis_kind": "always",
        },
        "requirement_body": {
            "scope_descriptor": "explicit_deterministic_scope",
            "completeness_policy": "partial_projection_allowed",
            "boundedness_policy": "optional_explicit_finite_bound",
            "truncation_policy": "declare_established_truncation",
        },
    },
    {
        "requirement_id": "projection-unknown",
        "requirement_kind": "projection",
        "requirement_mode": "required",
        "applicability": {
            "subject_category": "projection_artifact",
            "basis_kind": "always",
        },
        "requirement_body": {
            "completeness_policy": "unknown_completeness_allowed",
        },
    },
    {
        "requirement_id": "material-context-carry",
        "requirement_kind": "preservation",
        "requirement_mode": "required",
        "applicability": {
            "subject_category": "material_context",
            "basis_kind": "material_context_condition",
            "expected_value": "carry_required",
        },
        "requirement_body": {
            "preservation_target": "material_context",
            "material_context_policy": "carry",
        },
    },
    {
        "requirement_id": "material-context-reference",
        "requirement_kind": "preservation",
        "requirement_mode": "required",
        "applicability": {
            "subject_category": "material_context",
            "basis_kind": "material_context_condition",
            "expected_value": "exact_reference_sufficient",
        },
        "requirement_body": {
            "preservation_target": "material_context",
            "material_context_policy": "exact_reference_sufficient",
        },
    },
    {
        "requirement_id": "material-context-omission",
        "requirement_kind": "preservation",
        "requirement_mode": "required",
        "applicability": {
            "subject_category": "material_context",
            "basis_kind": "material_context_condition",
            "expected_value": "explicit_omission_required",
        },
        "requirement_body": {
            "preservation_target": "material_context",
            "material_context_policy": "omission_allowed",
        },
    },
    {
        "requirement_id": "material-context-dependency",
        "requirement_kind": "preservation",
        "requirement_mode": "required",
        "applicability": {
            "subject_category": "material_context",
            "basis_kind": "material_context_condition",
            "expected_value": "dependency_continuation_required",
        },
        "requirement_body": {
            "preservation_target": "material_context",
            "material_context_policy": "dependency_continuation",
        },
    },
    {
        "requirement_id": "source-record-traceability",
        "requirement_kind": "source_binding",
        "requirement_mode": "required",
        "applicability": {
            "subject_category": "source_record",
            "basis_kind": "material_to_projection",
            "expected_value": True,
        },
        "requirement_body": {
            "source_participation": "source_record",
            "target_category": "material_origin_context",
        },
    },
    {
        "requirement_id": "binding-record-traceability",
        "requirement_kind": "source_binding",
        "requirement_mode": "required",
        "applicability": {
            "subject_category": "binding_record",
            "basis_kind": "material_to_projection",
            "expected_value": True,
        },
        "requirement_body": {
            "source_participation": "binding_record",
            "target_category": "material_source_correlation",
        },
    },
    {
        "requirement_id": "external-reference-closure",
        "requirement_kind": "closure",
        "requirement_mode": "required",
        "applicability": {
            "subject_category": "projection_artifact",
            "basis_kind": "always",
        },
        "requirement_body": {
            "closure_scope": "projection_artifact_references",
            "closure_policy": "external_references_allowed",
        },
    },
)

EXPECTED_AI_CONTEXT_PROFILE = {
    "artifact_kind": "profile_requirement_artifact",
    "binding": {
        "family": "https://geesno.com/binding/ai-context-json",
        "version": "0.1.0",
    },
    "profile_edition": {
        "profile_family": "https://geesno.com/profile/ai-context",
        "profile_version": "0.1.0",
    },
    "vocabulary_dependencies": [],
    "requirements": list(EXPECTED_AI_CONTEXT_REQUIREMENTS),
}

EXPECTED_S5_CORPUS_CASE_IDS = (
    tuple(f"V{index:02d}" for index in range(1, 13))
    + tuple(f"I{index:02d}" for index in range(1, 23))
    + tuple(f"S{index:02d}" for index in range(1, 25))
)

MARKDOWN_LINK = re.compile(r"(?<!!)\[[^\]]*\]\(([^)]+)\)")

LOCAL_ABSOLUTE_PATH = re.compile(
    r"(?im)(?:\b[A-Za-z]:[\\/]|file://|/(?:home|Users)/[^/\s]+/)"
)

FENCED_JSON = re.compile(
    r"^```json[ \t]*\r?\n(.*?)^```[ \t]*$",
    re.MULTILINE | re.DOTALL,
)

ACCEPTED_ARCHITECTURE_ADRS = (
    "adr/0001-project-scope.md",
    "adr/0002-semantic-vs-execution.md",
    "adr/0003-serialization.md",
    "adr/0004-licensing.md",
    "adr/0005-assertion-model.md",
    "adr/0006-source-binding-model.md",
    "adr/0007-lifecycle-model.md",
    "adr/0008-concept-representation-cardinality.md",
    "adr/0009-identifier-reference-model.md",
    "adr/0010-qualified-term-namespace-model.md",
    "adr/0011-canonical-json-assertion-placement.md",
    "adr/0012-value-measured-quantity-model.md",
    "adr/0013-source-binding-serialization.md",
    "adr/0014-lifecycle-serialization.md",
    "adr/0015-version-extension-strictness.md",
    "adr/0016-json-processing-canonicalization.md",
    "adr/0017-vocabulary-identity-version-model.md",
    "adr/0018-vocabulary-publication-artifact.md",
    "adr/0019-vocabulary-term-lifecycle.md",
    "adr/0020-extension-vocabulary-authoring-payload-compatibility.md",
    "adr/0021-optional-vocabulary-discovery-authority-governance.md",
    "adr/0022-geesno-base-vocabulary.md",
    "adr/0023-cross-vocabulary-profile-compatibility-model.md",
    "adr/0024-profile-identity-version-conformance-boundary.md",
    "adr/0025-ai-context-selection-projection-semantics.md",
    "adr/0026-projection-omission-boundedness-continuation-semantics.md",
    "adr/0027-projection-preservation-material-context-semantics.md",
    "adr/0028-profile-requirement-expression-semantics.md",
    "adr/0029-ai-context-profile-projection-serialization-binding.md",
    "adr/0030-ai-context-profile-conformance-result-diagnostics.md",
    "adr/0031-ai-context-profile-composition-conflict-policy.md",
)

PROCESSING_ACCEPTANCE_MARKERS = (
    "## Context",
    "## Requirements",
    "## Processing pipeline",
    "## UTF-8/Unicode policy",
    "## Parser-level rules",
    "## Duplicate-member policy",
    "## Version dispatch",
    "## JSON number handling",
    "## Extension preservation",
    "## Object/array ordering semantics",
    "## Validation-layer model",
    "## JSON Schema role",
    "## Draft selection",
    "## Schema identifier and versioning",
    "## Closed-core schema strategy",
    "## Cross-record semantic validation",
    "## Lexical freeze audit",
    "## Member-name/token freeze audit",
    "## Omission/empty/null rules",
    "## Canonicality levels",
    "## Byte-canonicalization decision",
    "## Diagnostics",
    "## Resource/security model",
    "## Streaming/large-document processing",
    "## Cross-language evidence",
    "## Cross-domain evidence",
    "## Adversarial cases",
    "## READY TO WRITE SCHEMA?",
    "## Accepted decision",
    "## Consequences",
    "## Remains open",
    "## Acceptance record",
    "Decision status: Accepted",
    "exact lexical token",
    "schema-valid != fully GeesNO.Semantic-conformant",
    "resource refusal",
)

ACCEPTED_VOCABULARY_IDENTITY_MARKERS = (
    "## Decision",
    "## Acceptance record",
    "Decision status: Accepted",
    "Vocabulary edition identity",
    "stable and immutable",
    "MUST NOT be repointed",
    "A new Vocabulary version does not by itself require new term IRIs",
    "An incompatible change to one term's denoted meaning requires a new term",
)

S5_I2_SCHEMA_SHA256 = "aec4f4e42267e8486b3420e0590f976aac1a3a07c61c2ba8d7a5776e57c5346a"

ADR_INDEX_ARCHITECTURE_MARKERS = (
    "The public architectural baseline is defined in [ARCHITECTURE.md]",
    "ADR-0001 through ADR-0008 establish",
    "ADR-0009 through ADR-0016 define",
    "ADR-0017 through ADR-0023 define",
    "ADR-0024 through ADR-0031 define Profile identity",
    "Profile requirement != execution instruction",
    "conformance result != semantic truth",
    "IRI != retrieval instruction",
    "An Accepted ADR remains authoritative until an explicit later architectural decision supersedes it",
)

ADR_INDEX_FORBIDDEN_OPERATIONAL_MARKERS = (
    "The S4 milestone remains In\nProgress",
    "S4 milestone remains In Progress",
    "human-approved",
    "Human closure approved",
)

RELEASE_NOTES_MARKERS = (
    "# Draft Release Notes",
    "0.1.0-preview.1",
    "planned first pre-1.0 Public Preview",
    "The preview has not yet been released",
    "AI Context Profile `0.1.0`",
    "non-normative Python reference SDK",
    "does not establish a certification program",
    "No package-registry release is planned for this preview",
    "[SECURITY.md](SECURITY.md)",
)

CONTRIBUTING_POLICY_MARKERS = (
    "External contribution intake requires a maintainer-designated public endpoint",
    "## Start Here",
    "## Contribution Routes",
    "Security issue? Stop and follow [SECURITY.md](SECURITY.md)",
    "## Normative Changes",
    "SDK-only, schema-only, example-only or README-only",
    "## License And DCO Sign-Off",
    "[LICENSES.md](LICENSES.md)",
    "Developer Certificate of Origin 1.1",
    "Signed-off-by: Name <email>",
    "does not adopt a\nCLA",
    "Contributors retain copyright",
    "submission != acceptance",
    "passing tests != normative approval",
    "merged code != certification",
    "No\nformal Code of Conduct is adopted",
    "Public contribution endpoint: not established by this distribution",
    "Public Preview 0.1.0-preview.1 - planned release; not yet finalized",
)

SECURITY_POLICY_MARKERS = (
    "preparing its first public preview, `0.1.0-preview.1`",
    "## Supported Versions",
    "No public GeesNO.Semantic release is currently designated as a supported security release",
    "## Reporting a Vulnerability",
    "Do not disclose suspected vulnerabilities through a public issue",
    "A private vulnerability-reporting route is not verified by this source distribution",
    "## Security Scope",
    "The semantic standard itself is descriptive and does not authorize execution",
    "Extensions are inert semantic data, not executable plugins",
    "External references and IRIs must not be interpreted as automatic retrieval or execution instructions",
    "syntactic validity\n!= semantic truth",
    "## Information to Include",
    "## Response Process",
    "No response-time SLA is currently promised",
    "semantic interpretation does not require",
    "Extension\n!= executable plugin",
)

DOCUMENTATION_MAP_MARKERS = (
    "non-normative navigation index",
    "## Authority and document roles",
    "ARCHITECTURE.md\n+ Accepted ADRs",
    "## Documentation taxonomy",
    "## Normative-source map",
    "Core != Vocabulary != Profile",
    "IRI\n!= retrieval instruction",
    "## AI Context Profile navigation",
    "AI Context assessment corpus catalogue",
    "[Implementation Guide](implementation-guide.md)",
    "[Conformance Guide](conformance-guide.md)",
    "validation/conformance != certification",
    "This documentation map does not itself establish release status",
)

IMPLEMENTATION_GUIDE_MARKERS = (
    "NON-NORMATIVE implementation guidance",
    "License:** [CC BY 4.0]",
    "Start with [ARCHITECTURE.md]",
    "[Accepted ADR index]",
    "You do not need the Python reference SDK",
    "## 2. Producer Route",
    "## 3. Consumer Route",
    "## 4. Minimal SemanticDocument",
    "## 5. Identity and References",
    "## 6. Concept and Representation",
    "## 7. Source and Binding",
    "## 8. Assertions, Values and Relations",
    "## 9. Namespaces and Vocabularies",
    "## 10. Provenance, Confidence and Review",
    "## 11. Lifecycle",
    "## 12. Extensions and Explicit Conditions",
    "## 13. Serialization and Validation Boundary",
    "## 14. How to Validate What You Produced",
    "[Conformance Guide](conformance-guide.md)",
    "## 15. Optional: Producing an AI Context Projection",
    "## 16. Language-Neutral Pseudocode",
    "## 18. Common Anti-Patterns",
    "## 19. Reference SDK Relationship",
    "## 20. Traceability Matrix",
    "## 21. Learn From Examples",
    "examples/cross-domain/public-preview/README.md",
    "## 22. Documentation Boundaries",
    "reference != resolution",
    "stable identity != required dereference",
    "schema validation != complete Layers 0-3 conformance",
    "No official certification or endorsement workflow is defined by this guide",
)

IMPLEMENTATION_GUIDE_TRACE_TARGETS = (
    PUBLIC_ARCHITECTURE,
    "adr/README.md",
    "spec/semantic-core.md",
    "spec/identity.md",
    "spec/entities.md",
    "spec/source-bindings.md",
    "spec/assertions.md",
    "spec/values-and-units.md",
    "spec/json-values-and-units.md",
    "spec/relations.md",
    "spec/provenance.md",
    "spec/revisions.md",
    "spec/extensions.md",
    "spec/json-qualified-terms.md",
    "spec/json-serialization.md",
    "schema/v0.1/geesno-semantic.schema.json",
    "vocab/README.md",
    "spec/conformance.md",
    "conformance/README.md",
    "spec/ai-context-profile.md",
    "profiles/ai-context/v0.1/profile.json",
    "spec/ai-context-json-binding.md",
    "profiles/ai-context/schema/v0.1/ai-context.schema.json",
)

IMPLEMENTATION_GUIDE_FORBIDDEN_TOKENS = (
    "geesno_semantic.",
    "RawNumber",
    "__all__",
    "dataclass",
    "dict subclass",
    "property decorator",
    "Python Decimal",
)

CONFORMANCE_GUIDE_MARKERS = (
    "NON-NORMATIVE conformance guidance",
    "License:** [CC BY 4.0]",
    "It creates no requirement, outcome, diagnostic, certification program",
    "[ARCHITECTURE.md]",
    "[Accepted ADRs]",
    "## 3. Bare-Core Layers 0-3",
    "Layer 0 - raw input",
    "Layer 1 - version dispatch",
    "Layer 2 - schema",
    "Layer 3 - semantic/integrity",
    "load or parse success",
    "!= schema validity",
    "17 documents expected",
    "84 inputs expected",
    "101 same-stem",
    "bare-Core conformance",
    "!= Profile conformance",
    "12 valid",
    "4 structural-invalid",
    "18 semantic-invalid",
    "satisfied",
    "violated",
    "not_applicable",
    "unsupported",
    "unavailable",
    "conformant",
    "nonconformant",
    "indeterminate",
    "diagnostic\n!= semantic Assertion",
    "AI Context assessment corpus catalogue",
    "## 12. Independent Validator Criterion",
    "## 13. Making a Bounded Factual Conformance Statement",
    "## 15. Traceability Matrix",
    "No badge, certificate, signed attestation, submission service, hosted",
    "must run without network, cloud service",
)

CONFORMANCE_GUIDE_TRACE_TARGETS = (
    PUBLIC_ARCHITECTURE,
    "adr/README.md",
    "PUBLIC_PREVIEW.md",
    "requirements-conformance.txt",
    "spec/conformance.md",
    "schema/v0.1/geesno-semantic.schema.json",
    "conformance/README.md",
    "conformance/valid/README.md",
    "conformance/invalid/README.md",
    "conformance/expected/README.md",
    "conformance/runner/README.md",
    "spec/ai-context-profile.md",
    "spec/ai-context-json-binding.md",
    "profiles/ai-context/v0.1/profile.json",
    "profiles/ai-context/schema/v0.1/ai-context.schema.json",
    "profiles/ai-context/conformance/v0.1/README.md",
    "spec/ai-context-assessment-json-binding.md",
    "profiles/ai-context/schema/v0.1/ai-context-assessment.schema.json",
    "profiles/ai-context/assessment-conformance/v0.1/README.md",
    AI_CONTEXT_ASSESSMENT_CATALOG,
    "tools/validation/ai_context_acceptance.py",
    "tools/validation/ai_context_requirement_assessment.py",
    "tools/validation/ai_context_result_construction.py",
    "tools/validation/integrated_conformance.py",
    "tools/validation/reference_cli.py",
)

CONFORMANCE_GUIDE_FORBIDDEN_TOKENS = (
    "GeesNO-certified implementation",
    "officially certified implementation",
    "SDK defines conformance",
    "requires the Python SDK",
    "latest Profile",
    "automatic Profile substitution",
)

PUBLIC_NAVIGATION_TARGETS = (
    PUBLIC_ARCHITECTURE,
    "adr/README.md",
    "spec/semantic-core.md",
    "spec/json-serialization.md",
    "schema/v0.1/geesno-semantic.schema.json",
    "vocab/README.md",
    "spec/extensions.md",
    "profiles/ai-context/README.md",
    "profiles/ai-context/v0.1/profile.json",
    "profiles/ai-context/schema/v0.1/ai-context.schema.json",
    "conformance/README.md",
    "profiles/ai-context/conformance/v0.1/README.md",
    "profiles/ai-context/assessment-conformance/v0.1/README.md",
    AI_CONTEXT_ASSESSMENT_CATALOG,
    "sdk/README.md",
    "LICENSES.md",
    "LICENSE-SPECIFICATION",
    "LICENSE-CODE",
    "PUBLIC_PREVIEW.md",
    RELEASE_NOTES,
)

PUBLIC_ENTRY_DOCS = (
    "README.md",
    DOCUMENTATION_MAP,
    IMPLEMENTATION_GUIDE,
    "spec/README.md",
)

PUBLIC_PREVIEW_MARKERS = (
    "preparing its first public preview",
    "0.1.0-preview.1",
    "does not itself publish a release",
    "public preview\n!= stable 1.0",
    "Until the corresponding versioned release is published",
    "this identifier describes the planned preview rather than an already released distribution",
    "exact assessed subject and the exact applicable contract",
    "conformance\n!= certification",
    "passing repository conformance tests\n!= official certification",
    "reference SDK behavior\n!= certification",
    "No certification program is established by this preview",
    "semantic identity URL\n!= required network resource\n!= retrieval instruction",
    "reference implementation\n!= normative authority",
    "Adapters, execution systems and product integrations",
)

PUBLIC_DOCUMENT_MARKERS = {
    RELEASE_NOTES: RELEASE_NOTES_MARKERS,
    SECURITY_POLICY: SECURITY_POLICY_MARKERS,
    DOCUMENTATION_MAP: DOCUMENTATION_MAP_MARKERS,
    IMPLEMENTATION_GUIDE: IMPLEMENTATION_GUIDE_MARKERS,
    CONFORMANCE_GUIDE: CONFORMANCE_GUIDE_MARKERS,
    PUBLIC_PREVIEW: PUBLIC_PREVIEW_MARKERS,
}

PUBLIC_AUTHORITY_DOCS = (
    DOCUMENTATION_MAP,
    IMPLEMENTATION_GUIDE,
    CONFORMANCE_GUIDE,
)

PUBLIC_INTERNAL_AUTHORITY_TARGETS = (
    "PROJECT_FOUNDATION.md",
    S7_P9_RECORD,
)

PUBLIC_RELEASE_STATUS_DOCS = (
    "README.md",
    DOCUMENTATION_MAP,
    IMPLEMENTATION_GUIDE,
    CONFORMANCE_GUIDE,
    PUBLIC_PREVIEW,
    RELEASE_NOTES,
    SECURITY_POLICY,
    "ROADMAP.md",
)

MISLEADING_PUBLICATION_PATTERNS = (
    re.compile(
        r"\b`?0\.1\.0-preview\.1`?\s+(?:is|was|has been)\s+"
        r"(?:published|released|finalized)\b",
        re.IGNORECASE,
    ),
    re.compile(
        r"\b(?:the\s+)?public preview"
        r"(?:\s+`?0\.1\.0-preview\.1`?)?"
        r"(?:\s*[-:]\s*|\s+(?:is|was|has been)\s+)"
        r"(?:published|released|finalized)\b",
        re.IGNORECASE,
    ),
    re.compile(
        r"\bthe\s+(?:public\s+)?(?:preview|release)\s+"
        r"(?:is|was|has been)\s+(?:published|released|finalized)\b",
        re.IGNORECASE,
    ),
    re.compile(
        r"\b(?:we|the\s+(?:project|repository|maintainers?))\s+"
        r"(?:(?:have|has)\s+)?(?:published|released|finalized)\s+"
        r"(?:the\s+)?(?:public\s+preview|preview|release)"
        r"(?:\s+`?0\.1\.0-preview\.1`?)?\b",
        re.IGNORECASE,
    ),
    re.compile(r"\brelease tag:\s*v0\.1\.0-preview\.1\b", re.IGNORECASE),
    re.compile(r"\bGitHub Release:\s*https://", re.IGNORECASE),
)

PUBLICATION_CLAIM_PREFIX_EXEMPTIONS = (
    re.compile(
        r"\b(?:if|when|whether|unless|until|before|assuming|suppose(?:\s+that)?)\b"
        r"[^.!?\n]{0,160}$",
        re.IGNORECASE,
    ),
    re.compile(
        r"\b(?:do|must|should)\s+not\s+(?:claim|state|say|describe)\b.*$",
        re.IGNORECASE,
    ),
    re.compile(
        r"\b(?:historical\s+(?:record|records|text)|marked\s+historical\s+quote)"
        r"\b.*\b(?:quote|claim|statement)\b.*$",
        re.IGNORECASE,
    ),
    re.compile(
        r"\b(?:forbidden|prohibited|incorrect|false)\s+"
        r"(?:claim|statement|example)\b.*$",
        re.IGNORECASE,
    ),
    re.compile(r"\bexamples?(?:\s+of\b|\s*:)\s*.*$", re.IGNORECASE),
)

PUBLICATION_CLAIM_EXPLANATION_PREFIX = re.compile(
    r"\b(?:claim|statement|assertion|wording|text|phrase)\s+"
    r"(?:that|saying)\b",
    re.IGNORECASE,
)

PUBLICATION_CLAIM_EXPLANATION_SUFFIX = re.compile(
    r"\bwould\s+be\s+(?:misleading|false|incorrect)\b",
    re.IGNORECASE,
)

PUBLICATION_SENTENCE_BOUNDARY = re.compile(r"[.!?](?:[\"')\]]+)?\s+|;\s*")

MISLEADING_CERTIFICATION_PATTERNS = (
    re.compile(r"\bGeesNO-certified implementation\b", re.IGNORECASE),
    re.compile(r"\bofficially certified implementation\b", re.IGNORECASE),
    re.compile(
        r"\bofficial certification program\s+(?:is|has been)\s+"
        r"(?:available|established|launched)\b",
        re.IGNORECASE,
    ),
)

README_PUBLIC_ENTRY_MARKERS = (
    "[Documentation Map](docs/README.md)",
    "GeesNO.Semantic is an open, universal and descriptive semantic standard",
    "preparing its first pre-1.0 Public Preview,\n`0.1.0-preview.1`",
    "reference SDK](sdk/README.md); it does not define the\n   standard",
    "Concept != Representation",
    "Profile != Core != Vocabulary",
    "IRI != retrieval instruction",
    "validation/conformance != certification",
    "[LICENSES.md](LICENSES.md)",
    "[Public Preview Status](PUBLIC_PREVIEW.md)",
    "Until the corresponding release tag and GitHub Release exist",
    "this distribution remains development state",
    "draft\n[release notes](RELEASE_NOTES.md)",
    "The licensor and copyright holder is `GENARO ESCUDERO NOGALES`",
)

README_FORBIDDEN_PUBLIC_CLAIMS = (
    "Status: Stable 1.0",
    "GeesNO-certified implementation",
    "officially approved implementation",
    "endorsed by GeesNO",
    "Public release authorized",
)

ASSESSMENT_CASE_ROW = re.compile(
    r"^\| `([VIS][0-9]{2})` \|.*$",
    re.MULTILINE,
)

def check_ai_context_profile(profile: object) -> list[str]:
    errors: list[str] = []
    if not isinstance(profile, dict):
        return ["AI Context Profile 0.1 artifact root must be an object"]
    if set(profile) != set(EXPECTED_AI_CONTEXT_PROFILE):
        errors.append("AI Context Profile 0.1 root members changed")
    if profile.get("artifact_kind") != "profile_requirement_artifact":
        errors.append("AI Context Profile 0.1 artifact_kind changed")
    if profile.get("binding") != EXPECTED_AI_CONTEXT_PROFILE["binding"]:
        errors.append("AI Context Profile 0.1 binding family/version changed")
    if profile.get("profile_edition") != EXPECTED_AI_CONTEXT_PROFILE["profile_edition"]:
        errors.append("AI Context Profile 0.1 exact edition changed")
    if profile.get("vocabulary_dependencies") != []:
        errors.append("AI Context Profile 0.1 must have no Vocabulary dependencies")

    requirements = profile.get("requirements")
    if not isinstance(requirements, list):
        errors.append("AI Context Profile 0.1 requirements must be an array")
    else:
        requirement_ids = [
            requirement.get("requirement_id")
            for requirement in requirements
            if isinstance(requirement, dict)
            and isinstance(requirement.get("requirement_id"), str)
        ]
        expected_by_id = {
            requirement["requirement_id"]: requirement
            for requirement in EXPECTED_AI_CONTEXT_REQUIREMENTS
        }
        if len(requirements) != 9:
            errors.append("AI Context Profile 0.1 must contain exactly 9 requirements")
        if len(requirement_ids) != len(requirements):
            errors.append("AI Context Profile 0.1 requirements need string IDs")
        elif len(requirement_ids) != len(set(requirement_ids)):
            errors.append("AI Context Profile 0.1 requirement IDs must be unique")
        if set(requirement_ids) != set(expected_by_id):
            errors.append("AI Context Profile 0.1 exact requirement ID inventory changed")
        kinds = {
            requirement.get("requirement_kind")
            for requirement in requirements
            if isinstance(requirement, dict)
            and isinstance(requirement.get("requirement_kind"), str)
        }
        if kinds != {"projection", "preservation", "source_binding", "closure"}:
            errors.append("AI Context Profile 0.1 exact requirement kinds changed")
        actual_by_id = {
            requirement["requirement_id"]: requirement
            for requirement in requirements
            if isinstance(requirement, dict)
            and isinstance(requirement.get("requirement_id"), str)
        }
        for requirement_id, expected in expected_by_id.items():
            if actual_by_id.get(requirement_id) != expected:
                errors.append(
                    "AI Context Profile 0.1 requirement differs from the "
                    f"accepted requirement inventory: {requirement_id}"
                )
    return errors

def local_markdown_targets(path: Path) -> list[Path]:
    """Return resolved local targets found in a Markdown document."""

    targets: list[Path] = []
    text = path.read_text(encoding="utf-8")
    for raw in MARKDOWN_LINK.findall(text):
        target = raw.strip()
        if target.startswith("<") and target.endswith(">"):
            target = target[1:-1]
        target = target.split(maxsplit=1)[0]
        if target.startswith(("#", "http://", "https://", "mailto:")):
            continue
        file_part = unquote(target.split("#", 1)[0])
        if not file_part:
            continue
        targets.append((path.parent / file_part).resolve())
    return targets

def normalized_contract_text(text: str) -> str:
    """Normalize presentation-only whitespace and case for prose contracts."""

    return re.sub(r"\s+", " ", text).strip().casefold()

def missing_contract_markers(text: str, markers: tuple[str, ...]) -> list[str]:
    normalized = normalized_contract_text(text)
    return [
        marker
        for marker in markers
        if normalized_contract_text(marker) not in normalized
    ]

def publication_claim_is_exempt(line: str, match: re.Match[str]) -> bool:
    """Return whether one matched claim has bounded non-affirmative context."""

    prefix = line[: match.start()]
    suffix = line[match.end() :]
    boundaries = list(PUBLICATION_SENTENCE_BOUNDARY.finditer(prefix))
    local_prefix = prefix[boundaries[-1].end() :] if boundaries else prefix
    next_boundary = PUBLICATION_SENTENCE_BOUNDARY.search(suffix)
    local_suffix = suffix[: next_boundary.start()] if next_boundary else suffix

    if any(
        exemption.search(local_prefix)
        for exemption in PUBLICATION_CLAIM_PREFIX_EXEMPTIONS
    ):
        return True
    return bool(
        PUBLICATION_CLAIM_EXPLANATION_PREFIX.search(local_prefix)
        and PUBLICATION_CLAIM_EXPLANATION_SUFFIX.search(local_suffix)
    )

def misleading_publication_claims(text: str) -> list[str]:
    """Return affirmative publication claims outside bounded quoted contexts."""

    claims: list[str] = []
    in_fenced_block = False
    for line in text.splitlines():
        stripped = line.lstrip()
        if stripped.startswith(("```", "~~~")):
            in_fenced_block = not in_fenced_block
            continue
        if in_fenced_block or stripped.startswith(">"):
            continue
        line_claim: str | None = None
        for pattern in MISLEADING_PUBLICATION_PATTERNS:
            for match in pattern.finditer(line):
                if publication_claim_is_exempt(line, match):
                    continue
                line_claim = match.group(0)
                break
            if line_claim is not None:
                claims.append(line_claim)
                break
    return claims

def public_document_contract_errors(relative: str, text: str) -> list[str]:
    errors: list[str] = []
    markers = PUBLIC_DOCUMENT_MARKERS.get(relative, ())
    for marker in missing_contract_markers(text, markers):
        errors.append(f"public contract marker is missing from {relative}: {marker}")

    if relative in PUBLIC_AUTHORITY_DOCS:
        for internal_target in PUBLIC_INTERNAL_AUTHORITY_TARGETS:
            if internal_target in text:
                errors.append(
                    f"public authority route must not expose internal record in "
                    f"{relative}: {internal_target}"
                )

    if relative in PUBLIC_RELEASE_STATUS_DOCS:
        for claim in misleading_publication_claims(text):
            errors.append(
                f"public document makes an unverified publication claim in "
                f"{relative}: {claim}"
            )
        for pattern in MISLEADING_CERTIFICATION_PATTERNS:
            if pattern.search(text):
                errors.append(
                    f"public document makes an improper certification claim in "
                    f"{relative}: {pattern.pattern}"
                )

    if relative == SECURITY_POLICY:
        for forbidden in (
            "security@geesno.com",
            "Private reporting channel active: yes",
            "github.com/GeesNO/GeesNO.Semantic/security/advisories/new",
        ):
            if forbidden in text:
                errors.append(
                    f"security policy claims an unverified private channel: {forbidden}"
                )
    return errors

def markdown_link_errors(root: Path) -> list[str]:
    errors: list[str] = []
    resolved_root = root.resolve()
    for markdown in root.rglob("*.md"):
        for target in local_markdown_targets(markdown):
            if not target.is_relative_to(resolved_root):
                errors.append(
                    f"local link escapes repository in "
                    f"{markdown.relative_to(root)}: {target}"
                )
            elif not target.exists():
                errors.append(
                    f"broken local link in {markdown.relative_to(root)}: {target}"
                )
    return errors

def repository_link_targets(path: Path, root: Path) -> set[str]:
    resolved_root = root.resolve()
    return {
        target.relative_to(resolved_root).as_posix()
        for target in local_markdown_targets(path)
        if target.is_relative_to(resolved_root)
    }

def assessment_case_rows(text: str) -> tuple[tuple[str, str], ...]:
    return tuple((match.group(1), match.group(0)) for match in ASSESSMENT_CASE_ROW.finditer(text))

def assessment_catalog_contract_errors(
    catalog_text: str,
    inventory_text: str,
) -> list[str]:
    catalog_rows = assessment_case_rows(catalog_text)
    catalog_ids = tuple(case_id for case_id, _ in catalog_rows)
    errors: list[str] = []
    if catalog_ids != EXPECTED_S5_CORPUS_CASE_IDS:
        errors.append(
            "public AI Context assessment catalogue must contain exactly ordered "
            "cases V01-V12, I01-I22 and S01-S24"
        )

    historical_rows: dict[str, str] = {}
    for case_id, row in assessment_case_rows(inventory_text):
        historical_rows.setdefault(case_id, row)
    expected_rows = tuple(
        (case_id, historical_rows.get(case_id, ""))
        for case_id in EXPECTED_S5_CORPUS_CASE_IDS
    )
    if catalog_rows != expected_rows:
        errors.append(
            "public AI Context assessment catalogue rows must remain literal copies "
            "of the approved historical inventory"
        )
    return errors

def assessment_catalog_errors(root: Path) -> list[str]:
    catalog_path = root / AI_CONTEXT_ASSESSMENT_CATALOG
    inventory_path = root / S5_CORPUS_INVENTORY
    if not catalog_path.is_file() or not inventory_path.is_file():
        return []
    return assessment_catalog_contract_errors(
        catalog_path.read_text(encoding="utf-8"),
        inventory_path.read_text(encoding="utf-8"),
    )


def artifact_digest_errors(root: Path, expected: dict[str, str]) -> list[str]:
    errors = []
    for relative, digest in expected.items():
        path = root / relative
        if not path.is_file():
            errors.append(f"missing public artifact: {relative}")
        elif hashlib.sha256(path.read_bytes()).hexdigest() != digest:
            errors.append(f"public artifact digest mismatch: {relative}")
    return errors


def snapshot_manifest_errors(root: Path) -> list[str]:
    path = root / "MANIFEST.sha256"
    if not path.is_file():
        return ["missing complete distribution manifest"]
    expected = {}
    for row in path.read_text(encoding="utf-8").splitlines():
        fields = row.split("  ", 1)
        if len(fields) != 2 or not re.fullmatch(r"[0-9a-f]{64}", fields[0]):
            return ["malformed complete distribution manifest"]
        digest, relative = fields
        target = root / relative
        if not target.resolve().is_relative_to(root.resolve()) or relative in expected:
            return ["unsafe or duplicate complete distribution manifest entry"]
        expected[relative] = digest
    actual = set(publication_hygiene.tracked_paths()) if root == ROOT else {
        p.relative_to(root).as_posix() for p in root.rglob("*") if p.is_file()}
    actual.discard("MANIFEST.sha256")
    if actual != set(expected):
        return ["complete distribution file inventory mismatch"]
    return artifact_digest_errors(root, expected)


def check_repository() -> list[str]:
    errors = []
    for relative in REQUIRED_FILES:
        path = ROOT / relative
        if not path.is_file() or not path.stat().st_size:
            errors.append(f"missing or empty distribution file: {relative}")
    errors.extend(artifact_digest_errors(ROOT, PUBLIC_ARTIFACTS["artifacts"]))
    errors.extend(snapshot_manifest_errors(ROOT))
    errors.extend(markdown_link_errors(ROOT))
    errors.extend(assessment_catalog_errors(ROOT))
    try:
        profile = json.loads((ROOT / AI_CONTEXT_PROFILE).read_text(encoding="utf-8"))
        errors.extend(check_ai_context_profile(profile))
    except (OSError, ValueError):
        errors.append("AI Context Profile cannot be read")
    for relative in PUBLIC_DOCUMENT_MARKERS:
        path = ROOT / relative
        if path.is_file():
            errors.extend(public_document_contract_errors(
                relative, path.read_text(encoding="utf-8")))
    for relative in ACCEPTED_ARCHITECTURE_ADRS:
        if "- **Status:** Accepted" not in (ROOT / relative).read_text(encoding="utf-8"):
            errors.append(f"accepted ADR status changed: {relative}")
    for relative, expected in OFFICIAL_LICENSE_SHA256.items():
        errors.extend(artifact_digest_errors(ROOT, {relative: expected}))
    if (ROOT / "adapters").exists():
        errors.append("product adapters are outside the public Core distribution")
    for path in ROOT.rglob("*"):
        if not path.is_file() or "__pycache__" in path.parts or ".git" in path.parts:
            continue
        if path.suffix not in {".md", ".py", ".json", ".yml", ".txt"}:
            continue
        data = path.read_bytes()
        try:
            content = data.decode("utf-8")
        except UnicodeDecodeError:
            errors.append(f"non-UTF8 public text: {path.relative_to(ROOT)}")
            continue
        if data.startswith(b"\xef\xbb\xbf") or not data.endswith(b"\n"):
            errors.append(f"invalid public text encoding/termination: {path.relative_to(ROOT)}")
        if path.suffix == ".py":
            try:
                ast.parse(content)
            except SyntaxError:
                errors.append(f"invalid Python syntax: {path.relative_to(ROOT)}")
        if path.suffix == ".json":
            try:
                json.loads(content)
            except ValueError:
                errors.append(f"invalid JSON syntax: {path.relative_to(ROOT)}")
        if path.suffix == ".md":
            for block in FENCED_JSON.findall(content):
                try:
                    json.loads(block)
                except ValueError:
                    errors.append(f"invalid documentation JSON: {path.relative_to(ROOT)}")
    try:
        errors.extend(publication_hygiene.audit_current_tree().errors)
    except OSError:
        errors.append("public distribution hygiene audit could not read files")
    return errors


def main() -> int:
    errors = check_repository()
    for error in errors:
        print("ERROR:", error)
    if not errors:
        print("Public distribution guard PASS: artifacts, authority, links, syntax and hygiene; no Git metadata required.")
    return bool(errors)


PUBLIC_ARTIFACTS = json.loads(PUBLIC_ARTIFACT_MANIFEST.read_text(encoding="utf-8"))
REQUIRED_FILES = tuple(PUBLIC_ARTIFACTS["required_files"])
FOUNDATION_SHA256 = PUBLIC_ARTIFACTS["artifacts"]["PROJECT_FOUNDATION.md"]

if __name__ == "__main__":
    raise SystemExit(main())
