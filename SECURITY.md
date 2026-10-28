# Security Policy

This document describes the security scope and vulnerability-reporting expectations for GeesNO.Semantic.

GeesNO.Semantic is currently preparing its first public preview, `0.1.0-preview.1`.

## Supported Versions

No public GeesNO.Semantic release is currently designated as a supported security release.

The planned first public preview is:

`0.1.0-preview.1`

Support expectations for that preview will apply only after the corresponding release is published.

Stable `1.0` does not yet exist.

## Reporting a Vulnerability

Do not disclose suspected vulnerabilities through a public issue, discussion, pull request, example or other public repository content.

A private vulnerability-reporting route is not verified by this source distribution. It must be identified and verified before the first public preview is finalized.

When a private reporting interface is provided by the repository, use that interface and include sensitive technical details only through that private channel.

If no private reporting route is available, do not publish exploit details or sensitive information publicly.

## Security Scope

Security reports may concern concrete security impact involving:

- parsing malformed, deeply nested, oversized or otherwise hostile semantic data;
- denial of service or resource exhaustion;
- unsafe error handling;
- schema, conformance, benchmark or assessment tooling;
- the non-normative reference SDK;
- repository command-line or validation tooling;
- unexpected network or filesystem access;
- unsafe automatic dereferencing;
- unexpected execution or interpretation of Extension data;
- dependency or supply-chain risks in reference tooling.

The semantic standard itself is descriptive and does not authorize execution.

```text
semantic data
!= executable instruction
```

Extensions are inert semantic data, not executable plugins.

External references and IRIs must not be interpreted as automatic retrieval or execution instructions.

## Data Sensitivity

Semantic material may inherit the sensitivity of its source.

Producers, processors and consumers are responsible for applying appropriate:

- access control;
- filtering;
- redaction;
- retention;
- disclosure controls;
- transport security;
- storage security.

These operational controls remain outside the semantic contract unless an explicit specification states otherwise.

GeesNO.Semantic does not make sensitive source material safe merely by representing it semantically.

## Semantic Correctness and Security

Syntactic or structural validity does not establish truth.

```text
syntactic validity
!= semantic truth
```

A factually incorrect Assertion, disputed classification, low-confidence inference or incorrect semantic statement is not automatically a security vulnerability.

Such behavior may become security-relevant when it causes a concrete security impact, such as:

- authorization bypass;
- unintended disclosure;
- unsafe execution by a consuming system;
- integrity loss;
- denial of service;
- exploitation of repository tooling.

## Information to Include

When reporting privately, include where safely possible:

- a concise description of the issue;
- the expected security impact;
- affected component;
- exact repository, specification, binding or Profile version where relevant;
- reproduction steps;
- a minimal safe input or proof of concept;
- environmental details needed to reproduce the issue;
- suggested remediation, if known.

Do not include unnecessary third-party or personal data.

## Testing Boundaries

Security research must not:

- access data without authorization;
- perform destructive testing against third-party systems;
- violate privacy;
- intentionally disrupt services;
- disclose an unresolved vulnerability publicly before reasonable coordination.

This policy does not itself create a legal safe-harbor program.

## Response Process

The intended vulnerability-handling process is:

```text
private report
-> triage
-> request additional information when needed
-> technical assessment
-> remediation
-> coordinated disclosure where appropriate
```

No response-time SLA is currently promised.

## Architectural Security Boundaries

GeesNO.Semantic is designed so that semantic interpretation does not require:

- automatic network access;
- registry lookup;
- remote resolution;
- automatic Profile download;
- automatic Vocabulary download;
- model invocation;
- tool execution.

```text
IRI
!= retrieval instruction

Profile requirement
!= execution authorization

Extension
!= executable plugin
```

Software that consumes GeesNO.Semantic may introduce its own execution, networking or integration behavior. Those behaviors remain the responsibility of that software and do not become part of the universal semantic standard merely because it consumes semantic data.

## Security of Reference Implementations

Schemas, conformance tooling and the reference SDK are implementation artifacts.

They may contain ordinary software defects and should be treated with the same dependency, input-validation and supply-chain precautions as other software.

The reference SDK remains non-normative:

```text
reference SDK behavior
!= semantic authority
```

A security defect in reference tooling does not by itself redefine the GeesNO.Semantic specification.
