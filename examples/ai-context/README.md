# AI Context examples

**NON-NORMATIVE ILLUSTRATIVE EXAMPLE COLLECTION**

These examples show how AI Context Profile edition `0.1.0` can describe compact
Projections using binding `ai-context-json/0.1.0`. They are explanatory, work
offline and are neutral to software, formats, domains, models and providers.
They do not define Profile requirements or conformance. If an example and a
normative artifact differ, the normative artifact wins.

`illustrative-record-set` and `illustrative-anchor` are readable values in
Profile-defined value slots for these examples. They do not define a public
scope grammar, query language or runtime API. Directory and file names are not
artifact or semantic identities.

| Example | Relative size | Context | Completeness | Main distinction |
| --- | --- | --- | --- | --- |
| [`01-small-complete/`](01-small-complete/) | small | generic asset description | `complete` | A narrow source subset can be complete relative to its declared Projection scope. |
| [`02-medium-traceable/`](02-medium-traceable/) | medium | scientific observation record | `complete` | Semantic content can retain material trust, Source and Binding context without making them truth. |
| [`03-bounded-partial/`](03-bounded-partial/) | larger | tabular observation series | `partial` | An explicit reached bound plus established truncation is partial; the bound is not priority. |
| [`04-projection-continuation/`](04-projection-continuation/) | medium | structured document sections | `partial` | Projection continuation describes known remaining same-scope content. |
| [`05-external-dependency/`](05-external-dependency/) | medium | digital module dependency | `partial` | Exact external reference, omission and dependency continuation remain distinct. |
| [`06-unknown-extension/`](06-unknown-extension/) | small | scientific sample | `complete` | An unknown inert Extension can be preserved losslessly with its host. |
| [`07-bounded-unknown/`](07-bounded-unknown/) | small | open-ended dataset view | `unknown` | Bounded does not mean truncated, and unknown does not mean partial. |

Each directory contains a valid S2 `source.json`, an I2-valid
`projection.json`, and a short explanation. The examples deliberately cover
all three completeness states and both continuation kinds without creating an
invalid-example corpus, benchmark, generator, SDK or runtime behavior.

Do not infer that every Source or Binding is material, every partial Projection
needs continuation, an external reference will be dereferenced, or any
illustrative bound is a normative size threshold.
