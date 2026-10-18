# Reproduce the keyless Coze Studio import checks

This runs the **unchanged official import validation and parameter-mapping
components**, pinned to Coze Studio commit
[`fefb05ff27be1da939612fbf9faf5db62583b8ae`](https://github.com/coze-dev/coze-studio/tree/fefb05ff27be1da939612fbf9faf5db62583b8ae).
It does not start the Coze UI, authenticate a workspace, install a market plugin
or make an Ace API request. Commercial Coze regions may differ from this
open-source version.

## Run

Obtain the official source tarball, then run with Go 1.24 and Python 3.9+:

```bash
gh api repos/coze-dev/coze-studio/tarball/fefb05ff27be1da939612fbf9faf5db62583b8ae > /tmp/coze-studio-fefb05f.tar.gz
python3 coze/validation/studio_import/run.py \
  --archive /tmp/coze-studio-fefb05f.tar.gz \
  --output /tmp/coze-studio-import-results.json
```

The runner verifies SHA-256 for every source file in `upstream-sources.json`,
copies them to a temporary module, downloads the dependencies pinned by
`go.mod`/`go.sum`, and runs the probe with module downloads disabled. Use
`--goproxy https://your-approved-go-proxy` if the default registry is unavailable.
The module is the smallest source closure needed for these official methods;
it is not a replacement Coze distribution. The upstream versions of
kin-openapi (`0.118.0`), Eino (`0.4.8`), Thrift (`0.13.0`, upstream replacement)
and Sonic (`1.15.0`) are preserved.

On the verified Intel macOS machine, upstream Sonic still triggered Go 1.24's
`invalid reference to runtime.lastmoduledatap` linker check. Only for this
isolated local verification, append `--intel-link-workaround`. It passes
`-ldflags=-checklinkname=0`; it does not change the source, product dependencies,
TLS, credentials or deployment. This workaround is recorded as an environment
limitation, not a portable Coze build result.

## What is exercised

For Seedance, HappyHorse and Nano Banana, both JSON and YAML pass through
kin-openapi parsing and official `Openapi3T.Validate`,
`Openapi3Operation.ToEinoSchemaParameterInfo`, `ToolInfo.ToReqAPIParameter`
and `ToolInfo.ToRespAPIParameter`.

- Two tools, same-task retrieval fields and media paths survive conversion.
- Single/batch task errors and the returned media fields stay visible.
- Authorization is required with no default/example credential.
- An in-memory `x-variable-ref=adc_auth` survives the official mapper. No token
  is stored, and this is not proof of private-variable access control in the UI.
- kin-openapi rejects a missing Authorization header and accepts valid request
  shapes. A deliberately invalid public marker is used **only in memory**;
  the probe blocks outgoing HTTP transport.

The 2026-10-19 run exposed numeric `format: double` values that pass ordinary
OpenAPI validation but fail Coze's response editor, which interprets formats
as file/media assist types. The projections omit only those numeric format
annotations; number types, fields and full canonical contracts remain.

## Limits and next host checks

This component execution is distinct from a full installed host test. Market
search, ordinary installation, workspace ownership/permissions, private Key
visibility, expired/revoked credentials, actual 401/403/429/500 rendering and
user cancellation still require the existing authenticated host session.
Canceling a Coze preview is not documented as canceling an already submitted
Ace task: retain its ID, do not resubmit generation, and query that same task
when appropriate. These plugins do not claim an upstream task-cancel API.

No model generation, live service authentication or task query is performed by
this check. Success fixtures, media placeholders and invalid-marker requests
are not runtime results, billing evidence or proof of store publication.
