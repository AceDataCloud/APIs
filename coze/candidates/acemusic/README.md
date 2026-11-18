# ACE Music Coze import candidate

Import `openapi.json` or `openapi.yaml` after the ACE Music service is deployed. This candidate follows the source contract in the companion Backend/API PR; it is not part of the historical live service snapshot, a submitted listing, or a verified Coze installation.

Privately bind Authorization to `Bearer YOUR_API_TOKEN` using your own AceDataCloud credential. Do not put credentials in the workflow prompt or shared defaults.

Tools cover music generation, one-track reference import, covers, two-reference mashups, lyrics and retrieval of the same original task. Song creation is asynchronous: save `task_id`, wait, then query it. Do not resubmit generation from a polling loop. A full generation/cover/mashup two-track group is charged once; final failed/partial groups are free. A successful one-track import has its own upload price. Lyrics are a separate paid operation; queries are free and authenticated.

Before store submission, import in the target Coze host, verify JSON-only tool schemas, choose exact model and required fields, run controlled generation/query/billing validation, and record the actual listing/version. The new reference actions depend on Backend #2351 and companion runtime deployment. Extension, instrumental controls, style-strength controls, stems and voice parameters remain outside this contract. This candidate has not been installed or submitted to a Coze store.
