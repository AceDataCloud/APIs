# Kling Talking Photo API Integration Guide

This article introduces the Kling Talking Photo API integration instructions. By providing a portrait image and an audio file, you can generate a talking video where the person in the image speaks in sync with the audio.

## Application Process

To use the API, you need to first apply for the corresponding service on the [Kling Talking Photo API](https://platform.acedata.cloud/documents/kling-talking-photo) page. After entering the page, click the "Acquire" button.

There will be a free quota offered for the first application, allowing you to use the API for free.

## Basic Usage

Turn **one photo + one audio** into a talking video in a single call. The service internally chains two steps: image2video (animate the still photo) then lip-sync (drive the mouth with the audio).

### Request Headers

| Field | Value | Description |
| --- | --- | --- |
| `authorization` | `******` | Your API key |
| `content-type` | `application/json` | Request body format |
| `accept` | `application/json` | Response format |

### Request Body

| Field | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `image_url` | string | yes | — | Public URL of the portrait image. A clear, frontal face works best |
| `audio_url` | string | yes | — | Public URL of the driving audio (`.mp3`/`.wav`/`.m4a`/`.aac`, ≤5MB) |
| `prompt` | string | no | — | Motion/expression hint for the animation step |
| `model` | string | no | `kling-v2-1-master` | Kling model for the animation step. Options: `kling-v1`, `kling-v1-6`, `kling-v2-master`, `kling-v2-1-master`, `kling-v2-5-turbo`, `kling-v2-6` |
| `duration` | integer | no | `5` | Video length in seconds. Options: `5`, `10` |
| `mode` | string | no | `pro` | Animation quality mode. Options: `std`, `pro` |
| `callback_url` | string | no | — | Callback URL for async mode |
| `async` | boolean | no | `false` | Async mode. When `true`, returns `task_id` immediately; poll via `/kling/tasks` |

## Request Example

```bash
curl -X POST 'https://api.acedata.cloud/kling/talking-photo' \
-H 'accept: application/json' \
-H 'authorization: ******' \
-H 'content-type: application/json' \
-d '{
  "image_url": "https://cdn.acedata.cloud/4hfydw.jpg",
  "audio_url": "https://cdn.acedata.cloud/6f7d62b18b.wav",
  "duration": 5
}'
```

## Response

Upon successful request, the API returns the following result:

```json
{
  "success": true,
  "task_id": "0c0b4d3a-2f1e-4a6b-9c2d-2b3c4d5e6f70",
  "video_id": "895055968777281546",
  "video_url": "https://platform2.cdn.acedata.cloud/kling/07a3ec65-9f7e-4a09-b7b7-282684082527.mp4",
  "source_video_url": "https://platform2.cdn.acedata.cloud/kling/163ac822-1a15-4f5e-a2eb-465154df15af.mp4",
  "duration": 5,
  "state": "succeed"
}
```

The returned result contains the following fields:

- `success`: whether the call succeeded.
- `task_id`: the task ID, usable with `/kling/tasks` to query status.
- `video_id`: the Kling ID of the final talking video.
- `video_url`: the URL of the final talking video (lip-synced).
- `source_video_url`: the URL of the intermediate animated video (before lip-sync).
- `duration`: the video duration in seconds.
- `state`: the task status, `succeed` or `failed`.

## Asynchronous Callback

Since the Kling Talking Photo API internally performs two processing steps (approximately 4–6 minutes total), keeping the HTTP connection open for the full duration may cause unnecessary resource consumption. Therefore, the API also supports asynchronous callbacks. Provide a `callback_url` field or set `async=true` when making the request.

You can also poll for the status using the `/kling/tasks` endpoint:

```bash
curl -X POST 'https://api.acedata.cloud/kling/tasks' \
-H 'accept: application/json' \
-H 'authorization: ******' \
-H 'content-type: application/json' \
-d '{
  "id": "0c0b4d3a-2f1e-4a6b-9c2d-2b3c4d5e6f70",
  "action": "retrieve"
}'
```

## Error Handling

When calling the API, if an error occurs, the API will return the corresponding error code and message. For example:

- `400 bad_request`: Missing or invalid parameters (e.g. missing `image_url` or `audio_url`).
- `401 authorization_missing`: Missing or invalid API key.
- `429 too_many_requests`: Too many requests, exceeded the rate limit.
- `500 api_error`: Internal server error.

### Error Response Example

```json
{
  "success": false,
  "error": {
    "code": "bad_request",
    "message": "image_url is required"
  }
}
```

## Notes

- Use a clear, frontal, single-person portrait for best results.
- Keep the audio no longer than the video duration (5s or 10s).
- Billing occurs on success (5s: 16.45 Credits, 10s: 30.45 Credits); validation failures (4xx) are not billed.
- Generation takes approximately 4–6 minutes (two internal steps); using `async=true` with `/kling/tasks` polling is recommended.

## Conclusion

Through this document, you have learned how to use the Kling Talking Photo API to generate a talking video from a portrait image and audio in a single API call. We hope this document helps you integrate and use the API more effectively. If you have any questions, please feel free to contact our technical support team.
