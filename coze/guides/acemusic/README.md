# ACE Music in Coze

Import three HTTP tools into your Coze workspace to create songs, write lyrics, and recover an existing task. Use the MCP configuration if your client supports remote MCP.

## Import the HTTP tools

1. Download the [Coze YAML](../../imports/acemusic.yaml) or [JSON](../../imports/acemusic.json). In your workspace, create an API plugin and import that file. The server is `https://api.acedata.cloud`.
2. Sign in to [Applications](https://platform.acedata.cloud/console/applications) and open **General Application**. Initialize it on your first visit if prompted, then copy the key shown in **API KEY**.

   ![General Application API KEY field and copy button](https://cdn.acedata.cloud/dvc3cg.jpg)

   Set a **private** variable called `adc_auth` to `Bearer YOUR_API_TOKEN` using the copied key. Bind each tool's required `Authorization` header by reference. Restrict key access to the intended APIs and check [your service balance and pricing](https://platform.acedata.cloud/services/acemusic). Keep the key out of prompts, shared defaults and exported workflows.
3. Add `getTaskResults` first. With `action=retrieve` and an existing `id`, it reads your original song or lyric task without submitting a new generation. For finished audio use `response.data[].audio_url`, and save `response.data[].id` separately for covers and mashups. For lyrics use `response.data[].text`.

| Tool | Inputs and result |
| --- | --- |
| `generateMusic` | `action=generate` takes a prompt, or `custom=true` plus `title`, `lyric` and `style`. Select `acemusic-v1.1` or `acemusic-v1`. A complete song yields two MP3 candidates. |
| `generateLyrics` | Submit `prompt` and optional `style` for a title and editable lyrics. This operation is charged separately. |
| `getTaskResults` | Use `retrieve` with `id`, `retrieve_batch` with `ids`, or `list` to recover your own tasks. Reads are free and authenticated. |

## Use references and recover results

For a reference import, choose `generateMusic` with `action=upload` and an authorized public HTTPS MP3 `audio_url`. This separately priced operation returns one track. A cover uses `action=cover` and one owned `audio_id`. A mashup uses `action=mashup` and exactly two different, compatible owned `mashup_audio_ids`. Supply `lyric` and `style` and select `acemusic-v1.1` for either action. Leave unrelated optional fields unset.

After one submission, keep the returned `task_id` and call `getTaskResults` with that ID. Continue polling while the task is active. At `partial_failed` show only finished tracks with playable URLs and stop. For `submission_unknown` retain the original ID and check history before any new submission. [Public API guide](https://platform.acedata.cloud/documents/acemusic-audios-integration?lang=en&utm_source=github&utm_medium=referral&utm_campaign=evergreen)

## Remote MCP

Use the [ACE Music configuration](../../mcp-plugins/acemusic.json) to configure `https://acemusic.mcp.acedata.cloud/mcp` with the caller's private credentials. The three HTTP tools map to API routes; the hosted MCP server advertises 11 named tools, including model discovery and separate cover, mashup and upload tools. After connecting, list tools and run `acemusic_list_models` before creating anything. [Public MCP server card](https://acemusic.mcp.acedata.cloud/.well-known/mcp/server-card.json)

[简体中文](README_zh-CN.md) · [Coze Studio component validation](../../validation/studio_import/README.md)
