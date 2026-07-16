# Kling Talking Photo API Integration Guide

This article introduces the Kling Talking Photo API integration instructions. By inputting a portrait image and an audio clip, you can generate a talking video in a single call — the service internally chains image-to-video animation and lip sync.

## Application Process

To use the API, you need to first apply for the corresponding service on the [Kling Talking Photo API](https://platform.acedata.cloud/documents/kling-talking-photo) page. After entering the page, click the "Acquire" button, as shown in the image:

![](https://cdn.acedata.cloud/q6ytrc.png)

If you are not logged in or registered, you will be automatically redirected to the login page inviting you to register and log in. After logging in or registering, you will be automatically returned to the current page.

There will be a free quota offered for the first application, allowing you to use the API for free.

## Basic Usage

The Kling Talking Photo API turns one photo and one audio clip into a talking video in a single API call. It internally chains two steps: image2video (animating the still photo) and lip-sync (driving the mouth with the audio). This is ideal for creating digital human narration, talking avatars, or portrait animations.

- **Endpoint**: `POST https://api.acedata.cloud/kling/talking-photo`
- **Pricing**: 5s — 16.45 Credits, 10s — 30.45 Credits (image2video + lip-sync bundle)

### Request Headers

- `accept`: the format of the response result you want to receive, filled in as `application/json`, which means JSON format.
- `authorization`: the key to call the API, which can be directly selected from the dropdown after application.
- `content-type`: `application/json`.

### Request Body Parameters

- `image_url` (required): public URL of the portrait image. A clear, frontal, single-person face works best.
- `audio_url` (required): public URL of the driving audio. Formats: `.mp3`/`.wav`/`.m4a`/`.aac`, ≤5MB.
- `prompt`: motion or expression hint for the animation step.
- `model`: Kling model for the animation step. Options: `kling-v1`, `kling-v1-6`, `kling-v2-master`, `kling-v2-1-master` (default), `kling-v2-5-turbo`, `kling-v2-6`.
- `duration`: video length in seconds. Options: `5` (default) or `10`.
- `mode`: animation quality. Options: `std` (standard), `pro` (high quality, default).
- `callback_url`: the URL to which the result will be sent upon completion. Providing this switches to async mode.
- `async`: async mode. When `true`, returns `task_id` immediately; poll via `/kling/tasks` or receive `callback_url`.

## Request Example

```shell
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

The returned result looks like:

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

The returned result contains multiple fields, described as follows:

- `success`: whether the call succeeded.
- `task_id`: the ID of the task (use with `/kling/tasks` to query status).
- `video_id`: the Kling ID of the generated talking video.
- `video_url`: the URL of the final talking video (after lip sync).
- `source_video_url`: the URL of the intermediate animated video (before lip sync).
- `duration`: the video duration in seconds.
- `state`: the task status: `succeed` or `failed`.

## Asynchronous Callback

Since the Kling Talking Photo API internally runs two steps (animation and lip sync), it takes approximately 4–6 minutes to complete. The API supports asynchronous callbacks to avoid keeping the HTTP connection open.

The overall flow is: the client specifies an additional `callback_url` field when making the request. The API immediately returns a result containing a `task_id` field representing the current task ID. When the task completes, the generated video result is sent via POST JSON to the specified `callback_url`, also including the `task_id` field.

You can also poll the status using `/kling/tasks` with body `{ "action": "retrieve", "id": "<task_id>" }`.

## Error Handling

When calling the API, if an error occurs, the API will return the corresponding error code and message. For example:

- `400 bad_request`: Bad request, possibly due to missing or invalid parameters.
- `401 authorization_missing`: Unauthorized, missing or invalid API key.
- `403 forbidden`: Blocked by content moderation.
- `429 too_many_requests`: Too many requests, you have exceeded the rate limit.
- `500 api_error`: Internal server error, something went wrong on the server.

### Error Response Example

```json
{
  "success": false,
  "error": {
    "code": "api_error",
    "message": "fetch failed"
  },
  "trace_id": "2cf86e86-22a4-46e1-ac2f-032c0f2a4e89"
}
```

## Notes

- Use a clear, frontal, single-person photo for best results.
- Keep the audio no longer than the video duration (5s or 10s).
- Generation takes approximately 4–6 minutes (two internal steps); prefer `async=true` with `/kling/tasks` polling.
- Billing happens on success; validation failures (4xx) are not billed.

## Conclusion

Through this document, you have learned how to use the Kling Talking Photo API to generate a talking video from a portrait image and audio in a single call. We hope this document helps you integrate and use the API more effectively. If you have any questions, please feel free to contact our technical support team.
