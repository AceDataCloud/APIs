# Maestro AI Video Production API

Maestro turns a natural-language brief and optional reference media into a finished video. Its AI director handles planning, scripting, visual assets, voiceover, music, editing, captions, quality checks, rendering, and multilingual variants.

![Platform](https://img.shields.io/badge/platform-Ace%20Data%20Cloud-0f766e?style=flat-square) ![API](https://img.shields.io/badge/type-AI%20API-2563eb?style=flat-square) ![Docs](https://img.shields.io/badge/docs-online-16a34a?style=flat-square)

API home page: [Ace Data Cloud - Maestro](https://platform.acedata.cloud/services/maestro)

Keywords: maestro-api, ai-video, video-production, prompt-to-video, article-to-video, multilingual-video, video-editing, rest-api, ai-api, developer-api, Ace Data Cloud

## Why Use Maestro on Ace Data Cloud

- Produce a complete video instead of a single model-generated shot
- Create scripts, visuals, narration, music, captions, and edits in one asynchronous workflow
- Attach public image, video, and audio references
- Render localized variants from one production
- Remix, edit, or extend an earlier Maestro task
- Use one Ace Data Cloud API token, billing system, and task history

## Quick Start

Create an API token in the [Ace Data Cloud console](https://platform.acedata.cloud/console/applications), then submit a video brief:

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
| [Maestro Videos API](https://platform.acedata.cloud/documents/maestro-videos) | `POST /maestro/videos` | [Video production guide](docs/maestro_videos_api_integration_guide.md) |
| [Maestro Tasks API](https://platform.acedata.cloud/documents/maestro-tasks) | `POST /maestro/tasks` | [Task retrieval guide](docs/maestro_tasks_api_integration_guide.md) |

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

Task polling and history retrieval do not consume credits. Video jobs are settled after production from the output actually delivered; failed jobs are not charged. See [live Maestro pricing](https://platform.acedata.cloud/services/maestro?tab=pricing) for current rates.

## Related Resources

- [Maestro in Ace Data Cloud Studio](https://studio.acedata.cloud/maestro)
- [Ace Data Cloud Developer Platform](https://platform.acedata.cloud)
- [Ace Data Cloud documentation](https://docs.acedata.cloud)
- [Service status](https://status.acedata.cloud)
- [Ace Data Cloud GitHub organization](https://github.com/AceDataCloud)

## Support

For integration help, use the [support page](https://platform.acedata.cloud/support) and include the response `trace_id` when available.