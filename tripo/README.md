# Tripo 3D API

Create a 3D model from a prompt or reference images, then texture, convert, rig or animate it. All four endpoints accept JSON over HTTPS. Use your AceDataCloud service token in the `Authorization: Bearer` header. [Get a token](https://platform.acedata.cloud/console/applications) · [OpenAPI JSON](openapi.json)

| POST endpoint | Actions | Output |
| --- | --- | --- |
| `/tripo/generations` | `generate` (default) | GLB model, model ID and optional preview image |
| `/tripo/models` | `import`, `texture`, `convert` | Model ID and download URL |
| `/tripo/animations` | `rig_check`, `rig`, `retarget` | Riggability report, rigged model or animated file |
| `/tripo/tasks` | `retrieve` (default), `retrieve_batch` | One task record or an ordered list of records |

## Use with an AI agent

Install the [Tripo 3D Skill](https://github.com/AceDataCloud/Skills/tree/main/skills/tripo-3d) for request examples and task handling. For an MCP client, configure `uvx mcp-tripo` as a local stdio server and supply your service token in `ACEDATACLOUD_API_TOKEN`. [MCP package](https://pypi.org/project/mcp-tripo/)

## Try a free request

The following example checks whether the Khronos sample Box mesh can be rigged. It uses the same submit-and-poll flow as a paid generation. Set `ACEDATACLOUD_API_TOKEN` to your service token, and run from this directory with Node.js 18+ and jq installed. [Khronos glTF sample asset](https://github.com/KhronosGroup/glTF-Sample-Assets/tree/main/Models/Box)

```bash
REQUEST_KEY=$(node -p "crypto.randomUUID()")
RECEIPT=$(curl --fail-with-body --silent --show-error https://api.acedata.cloud/tripo/animations \
  -H "Authorization: Bearer ${ACEDATACLOUD_API_TOKEN:?Set your AceDataCloud token}" \
  -H 'Content-Type: application/json' \
  -H "Idempotency-Key: $REQUEST_KEY" \
  -d '{
    "action": "rig_check",
    "model_url": "https://raw.githubusercontent.com/KhronosGroup/glTF-Sample-Assets/main/Models/Box/glTF-Binary/Box.glb",
    "async": true
  }')
TASK_ID=$(jq -er '.task_id' <<<"$RECEIPT")
node poll.mjs "$TASK_ID"
```

The async receipt has the form `{"task_id":"<TASK_ID>"}`. The polling example posts `{"id":"<TASK_ID>"}` to `/tripo/tasks` and prints the final task record. For this Box mesh, the observed result had the following fields (identifiers abbreviated).

```json
{
  "progress": 100,
  "response": {
    "success": true,
    "task_id": "<TASK_ID>",
    "trace_id": "<TRACE_ID>",
    "data": [{"id": "<TASK_ID>", "riggable": false, "rig_type": "biped"}]
  }
}
```

`riggable: false` is a successful check. For file-producing tasks, read the download URL from `response.data[0].model_url` and retain `response.data[0].id` to reference the model in later operations. A synchronous request returns the result envelope directly, with the download at `data[0].model_url`. Supplying `async: true` or `callback_url` returns the receipt instead. A callback receives the terminal result.

## Generate a model

This request generates geometry from text for **2 Ace Credits** on the default H model. Use a fresh idempotency key for each new operation. If transmission fails, retain the original key, request body and task ID so the same submission can be recovered.

```bash
REQUEST_KEY=$(node -p "crypto.randomUUID()")
curl --fail-with-body --silent --show-error https://api.acedata.cloud/tripo/generations \
  -H "Authorization: Bearer ${ACEDATACLOUD_API_TOKEN:?Set your AceDataCloud token}" \
  -H 'Content-Type: application/json' \
  -H "Idempotency-Key: $REQUEST_KEY" \
  -d '{"prompt":"A wooden chair with four straight legs","texture":"none","async":true}'
```

Pass exactly one of `prompt`, `image_url`, or `image_urls`. Single images and multiview slots accept public HTTPS PNG or JPEG files up to 20 MiB each. Multiview accepts two to four slots in front, left, back, right order. The front and at least one other view are required. Use `null` to skip an intermediate view. The default `model` is `v3.1-20260211`, and the default `texture` is `standard`.

## Work with an existing model

The following bodies show the required inputs. Replace angle-bracket identifiers with IDs from successful tasks owned by your account.

| Path | Example JSON body |
| --- | --- |
| `/tripo/models` | `{"action":"import","model_url":"https://raw.githubusercontent.com/KhronosGroup/glTF-Sample-Assets/main/Models/Box/glTF-Binary/Box.glb","async":true}` |
| `/tripo/models` | `{"action":"texture","model_id":"<MODEL_ID>","prompt":"Matte blue ceramic","texture_quality":"standard","async":true}` |
| `/tripo/models` | `{"action":"convert","model_id":"<MODEL_ID>","format":"OBJ","async":true}` |
| `/tripo/animations` | `{"action":"rig","model_id":"<RIGGABLE_MODEL_ID>","rig_type":"biped","format":"GLB","async":true}` |
| `/tripo/animations` | `{"action":"retarget","model_id":"<RIGGED_MODEL_ID>","animations":["preset:walk","preset:idle"],"format":"GLB","async":true}` |
| `/tripo/tasks` | `{"action":"retrieve_batch","ids":["<FIRST_TASK_ID>","<SECOND_TASK_ID>"]}` |

Import accepts public HTTPS GLB, GLTF, OBJ, FBX and STL files up to 150 MiB. Texture, conversion, rig checks and rigging accept either an owned `model_id` or a `model_url`. Conversion accepts `GLTF`, `FBX`, `USDZ`, `OBJ`, `STL` or `3MF`. Read the returned `format` and optional `container` when saving the file. For example, an OBJ package is a ZIP containing its material assets. Retargeting takes the ID from a successful rig operation and one to five compatible presets. A single file can contain multiple clips.

For batch lookup use either `ids` or `trace_ids`, up to 100 entries. The response has `items` and `count`. It preserves input order and duplicates, with `null` for missing or inaccessible tasks. A missing single lookup returns `{}`.

## Pricing

Prices are in Ace Credits per successful operation.

| Generation | Geometry only | Standard texture |
| --- | ---: | ---: |
| H text | 2 | 4 |
| H single image or multiview | 4 | 6 |
| P1 text | 6 | 8 |
| P1 single image or multiview | 8 | 10 |
| P2 text, single image or multiview | 20 | 22 |

Texture processing costs 2 for `fast` or `standard`, 4 for `detailed` and 6 for `extreme`. Basic and advanced format conversion cost 1 and 2 respectively. Rigging costs 5, and retargeting costs 2 per preset. Import, rig checks and task queries are free. [Service pricing](https://platform.acedata.cloud/services/tripo)

## Trial account concurrency

Accounts with neither a successful paid top-up nor an administrator's manual credit addition may run **one billable request at a time across the entire account**, shared by all API keys and services. Rewards, redemption cards and transferred credits do not count as paid top-ups. A successful paid top-up or manual credit addition removes this trial restriction; balance and key usage-limit checks still apply. The read-only user flag `has_recharged` records this eligibility; it is not a request parameter.

A new billable request returns `429 too_many_requests` while another is running. Wait for the active request's final result before submitting the next one. Free task polling remains available.

For async APIs, acceptance or a task ID is not completion: keep querying the same task until its final result. A disconnect or proxy timeout does not mean execution stopped. If a task has no terminal result for a long time, contact support with `trace_id`.

This restriction changes neither trial API availability nor pricing; fees are settled after execution based on actual usage. Realtime connection authentication does not occupy this ordinary-request slot and retains its existing per-turn billing.
