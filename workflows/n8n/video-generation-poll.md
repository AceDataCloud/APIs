# Async video generation with bounded polling

[`video-generation-poll.json`](video-generation-poll.json) submits one asynchronous video-generation request to `POST https://api.acedata.cloud/wan/videos`, polls `POST https://api.acedata.cloud/wan/tasks`, and returns a structured video result. It uses only built-in n8n nodes and caps polling at 20 attempts separated by 15 seconds.

Last contract verification: **2026-09-10**.

## Import and setup

1. Download `video-generation-poll.json`.
2. In n8n, choose **Import from File**. For CLI validation, run `n8n import:workflow --input=video-generation-poll.json` against an isolated n8n user folder/database first.
3. The stable template ID is `acedata-video-generation-poll-v1`. An n8n CLI import can overwrite an existing workflow with the same ID; change or remove the ID before importing if you need a separate copy.
4. [Create an Ace Data Cloud API token](https://platform.acedata.cloud/?utm_source=n8n&utm_medium=workflow&utm_campaign=n8n-video-generation-poll).
5. Create one **Header Auth** credential:
   - Name: `Authorization`
   - Value: `Bearer <YOUR_API_TOKEN>`
6. Select that credential separately in **Submit video with Ace Data Cloud** and **Poll video task**.
7. Edit `prompt`, `image_url`, or `ratio` in **Set video input**, then run the workflow.

The exported workflow contains no credential ID, token, pinned response, or user data. n8n stores credential data separately from the workflow JSON.

## Inputs and request selection

| Field | Default | Contract |
| --- | --- | --- |
| `prompt` | Paper-boat cinematic shot | Generation prompt |
| `image_url` | Empty | Optional public source-image URL |
| `ratio` | `16:9` | Output aspect ratio |

The workflow selects a request contract from `image_url`:

- empty `image_url`: `action=text2video`, `model=wan2.6-t2v`;
- non-empty `image_url`: `action=image2video`, `model=wan2.6-i2v`.

Both branches set `async=true`. Keep the fixed actions and models paired as exported unless you have checked the current endpoint schema. When using image-to-video, the source image URL must be reachable by the API.

## Polling and failure behavior

The submit response must have HTTP 200 and a non-empty `task_id`. The workflow then creates exactly 20 poll items. For each item it waits 15 seconds and requests the task record with:

```json
{
  "action": "retrieve",
  "id": "<task_id>"
}
```

The workflow does not infer undocumented status strings:

- no numeric `finished_at`: continue to the next bounded attempt;
- numeric `finished_at` plus `response.success=true` and a non-empty `response.video_url`: return success;
- numeric `finished_at` without that result contract: stop as a terminal failure;
- all 20 attempts consumed: stop with a timeout error.

Submit and poll HTTP responses must be exactly 200. Transport/API failures, a missing task ID, a terminal task failure, and polling timeout all stop explicitly with useful response context. The submit and poll request timeouts are each 60 seconds; the scheduled polling window is approximately five minutes, excluding request latency.

A successful run returns:

```json
{
  "status": "success",
  "task_id": "...",
  "model": "wan2.6-t2v",
  "prompt": "...",
  "video_url": "https://...",
  "thumbnail_url": "https://...",
  "elapsed_seconds": 42
}
```

## Cost and data boundary

- Each execution submits **one billable video-generation request** and makes up to 20 task-retrieval requests. Failed, timed-out, or manually retried executions can add requests. Check current generation pricing before activation.
- The prompt, selected action/model, ratio, and optional source-image URL are sent to Ace Data Cloud. The task ID, task records, and returned media URLs are present in n8n execution data.
- n8n executions can remain stored according to the instance's retention settings. Configure retention before processing sensitive material.
- Do not send secrets, personal data, or content you are not authorized to process. Review generated videos for accuracy, rights, and policy compliance before publication.
