# Unknown Extension preservation

**NON-NORMATIVE ILLUSTRATIVE EXAMPLE**

## Purpose

Show lossless carriage of an Extension that AI Context Profile does not
interpret.

## Source scope

The source contains one scientific sample host, an opaque Extension payload and
one descriptive Assertion.

## Selection context

The sample and its label are selected.

## Projection scope

The explicit two-record scope includes the Extension host and Assertion.

## Completeness

`complete` relative to that declared scope.

## Material context decision

The host is material, so its complete record body, host scope and opaque
Extension payload are carried unchanged.

## Key distinction

An unknown Extension can be preserved without being understood. An Extension
is not a plugin, command or executable capability.

## Files

- `source.json`: valid S2 sample with unknown Extension data.
- `projection.json`: complete lossless carriage of the Extension host.

## Validation

The example test compares the carried host body exactly with the source body.

## What this example does NOT mean

It does not promote payload members into Core or assign semantics to the
unknown payload.
