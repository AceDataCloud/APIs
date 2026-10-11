# Maestro AI Video Production API

Maestro turns a natural-language brief and optional reference media into a finished video. Its AI director handles planning, scripting, visual assets, voiceover, music, editing, captions, quality checks, and rendering. Each task delivers one video in one selected language.

![Platform](https://img.shields.io/badge/platform-Ace%20Data%20Cloud-0f766e?style=flat-square) ![API](https://img.shields.io/badge/type-AI%20API-2563eb?style=flat-square) ![Docs](https://img.shields.io/badge/docs-online-16a34a?style=flat-square)

API home page: [Ace Data Cloud - Maestro](https://platform.acedata.cloud/services/maestro?utm_source=github&utm_medium=referral&utm_campaign=evergreen&utm_content=maestro_api_readme_services_maestro)

Keywords: maestro-api, ai-video, video-production, prompt-to-video, article-to-video, multilingual-video, video-editing, rest-api, ai-api, developer-api, Ace Data Cloud

## Get your Ace Data Cloud API key

1. Open [Ace Data Cloud → Applications](https://platform.acedata.cloud/console/applications?utm_source=github&utm_medium=referral&utm_campaign=evergreen&utm_content=maestro_api_readme_api_key). Sign in, or register an account first.
2. Find **General application**. If it has not been created, choose **Initialize General Application**. A general key can use the services available to your account; a dedicated application's key is limited to its service. Check the required service/model access and [current pricing](https://platform.acedata.cloud/models?utm_source=github&utm_medium=referral&utm_campaign=evergreen&utm_content=maestro_api_readme_pricing).
3. Copy the **API Key** from the application card, or open **Keys / Manage Keys → Create** to create a separate key for this integration. Give it a recognizable name so you can revoke or rotate it independently.
4. When creating a key, review **Expiration Time**, **Set Usage Limitation**, and **Allowed APIs**. Enable only the restrictions you need, allow the operations you will call, then click **Create** and copy the token from the key list. Task lookup does not grant permission to submit a generation. Confirm the application's balance can cover your first request; any trial allowance is whatever your account currently displays.
5. Copy only the token value, without quotation marks, spaces, or `Bearer `. An API Key / API Token field expects this raw value; only a manually configured HTTP `Authorization` header needs the `Bearer ` prefix. A `platform-...` account-management token cannot replace a generation API key.

![Copy an application API key or open Manage Keys](https://raw.githubusercontent.com/AceDataCloud/NanoBananaDify/2522b2f57210597af2db866445319334a1677a23/_assets/tutorial/get-api-key-en.png)

![Create a separately named key with optional restrictions](https://raw.githubusercontent.com/AceDataCloud/NanoBananaDify/2522b2f57210597af2db866445319334a1677a23/_assets/tutorial/create-api-key-en.png)

Save the key in the client's credential store or the environment variable shown below. Never put it in a prompt, shared workflow, screenshot, or Git commit. If authentication fails, check the full copied value, application/service access, expiration, usage limit, and balance before creating another key.

## Why Use Maestro on Ace Data Cloud

- Produce a complete video instead of a single model-generated shot
- Create scripts, visuals, narration, music, captions, and edits in one asynchronous workflow
- Attach public image, video, and audio references
- Choose the output language; create separate tasks for different language versions
- Remix, edit, or extend an earlier Maestro task
- Use one Ace Data Cloud API token, billing system, and task history

## Quick Start

Create an API token in the [Ace Data Cloud console](https://platform.acedata.cloud/console/applications?utm_source=github&utm_medium=referral&utm_campaign=evergreen&utm_content=maestro_api_readme_api_key), then submit a video brief:

```bash
curl --request POST 'https://api.acedata.cloud/maestro/videos' \
  --header 'Authorization: Bearer YOUR_API_TOKEN' \
  --header 'Content-Type: application/json' \
  --data '{
    "prompt": "Create a 30-second beginner-friendly video explaining vector databases. End with one memorable takeaway.",
    "langs": ["en"],
    "aspect": "16:9",
    "duration": 30,
    "scenario": "narrated"
  }'
```

The API accepts the job immediately:

```json
{
  "success": true,
  "task_id": "f57e99c4-f60f-4373-a155-17742ce2357d",
  "trace_id": "70e1cb12-c619-4292-a416-90191205996b"
}
```

Query the task until its top-level `status` becomes `succeeded` or `failed`:

```bash
curl --request POST 'https://api.acedata.cloud/maestro/tasks' \
  --header 'Authorization: Bearer YOUR_API_TOKEN' \
  --header 'Content-Type: application/json' \
  --data '{"id": "f57e99c4-f60f-4373-a155-17742ce2357d", "action": "retrieve"}'
```

## APIs and Guides

| API | Path | Integration Guide |
|---|---|---|
| [Maestro Videos API](https://platform.acedata.cloud/documents/maestro-videos?utm_source=github&utm_medium=referral&utm_campaign=evergreen&utm_content=maestro_api_readme_documents_maestro_videos) | `POST /maestro/videos` | [Video production guide](docs/maestro_videos_api_integration_guide.md) |
| [Maestro Tasks API](https://platform.acedata.cloud/documents/maestro-tasks?utm_source=github&utm_medium=referral&utm_campaign=evergreen&utm_content=maestro_api_readme_documents_maestro_tasks) | `POST /maestro/tasks` | [Task retrieval guide](docs/maestro_tasks_api_integration_guide.md) |

## Asynchronous Workflow

```text
POST /maestro/videos
        |
        v
  task_id returned
        |
        v
POST /maestro/tasks  ->  pending/planning/producing  ->  succeeded or failed
        |                                                   |
        +---------------- progress -------------------------+
                                                            |
                                                            v
                                             response.data.variants
```

Task polling and history retrieval do not consume credits. Successful video jobs cost 0.7 Credits per actual delivered second for every action, scenario, and language, with no multipliers or language surcharges; failed jobs are not charged. Billed duration is measured in integer seconds, never exceeds the requested duration, and falls back to the requested duration if the output duration cannot be read. A 30-second billed video costs 21 Credits. See [live Maestro pricing](https://platform.acedata.cloud/services/maestro?tab=pricing&utm_source=github&utm_medium=referral&utm_campaign=evergreen&utm_content=maestro_api_readme_services_maestro) for current rates.

## Related Resources

- [Maestro in Ace Data Cloud Studio](https://studio.acedata.cloud/maestro?utm_source=github&utm_medium=referral&utm_campaign=evergreen&utm_content=maestro_api_readme_maestro)
- [Ace Data Cloud Developer Platform](https://platform.acedata.cloud?utm_source=github&utm_medium=referral&utm_campaign=evergreen&utm_content=maestro_api_readme_platform)
- [Ace Data Cloud documentation](https://platform.acedata.cloud/documents?utm_source=github&utm_medium=referral&utm_campaign=evergreen&utm_content=maestro_api_readme_documents)
- [Service status](https://status.acedata.cloud)
- [Ace Data Cloud GitHub organization](https://github.com/AceDataCloud)

## Support

For integration help, use the [support page](https://platform.acedata.cloud/support?utm_source=github&utm_medium=referral&utm_campaign=evergreen&utm_content=maestro_api_readme_support) and include the response `trace_id` when available.