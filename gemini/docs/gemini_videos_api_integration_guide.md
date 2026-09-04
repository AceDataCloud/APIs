# Gemini Videos Generation API Integration and Usage

The Gemini Videos Generation API generates Google Gemini `omni-flash` videos from text prompts and optional reference media.

## Authentication

Obtain an API token from the [Ace Data Cloud Console](https://platform.acedata.cloud/console/applications) and send it in the `Authorization` header. One API token can call all services on the platform.

## Request

Send a POST request to `/gemini/videos`.

| Parameter | Required | Description |
| --- | --- | --- |
| `prompt` | Yes | Text description of the video to generate. |
| `model` | No | `omni-flash` (default). |
| `aspect_ratio` | No | `16:9` (default) or `9:16`. |
| `resolution` | No | `720p` (default) or `1080p`. |
| `image_urls` | No | Reference image URL array. Required with `video_urls`. |
| `video_urls` | No | Reference video URL array with at most one item. |
| `callback_url` | No | URL that receives the completed result. |
| `async` | No | Return a task ID immediately when `true`. |

```bash
curl -X POST "https://api.acedata.cloud/gemini/videos" \
  -H "Authorization: ******" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "A cinematic shot of a kitten chasing a butterfly in a sunlit garden",
    "model": "omni-flash",
    "aspect_ratio": "16:9",
    "resolution": "720p"
  }'
```

## Response

Synchronous requests return the generated results in `data`, including each video's `id`, `video_url`, `state`, `aspect_ratio`, and `prompt`. The response also includes `task_id`, `trace_id`, timing fields, and a `cost` object.

For asynchronous requests, save the returned `task_id` and query it with the [Gemini Tasks API](gemini_tasks_api_integration_guide.md).

When `video_urls` is provided for video editing, it accepts at most one video and requires at least one `image_urls` item.
