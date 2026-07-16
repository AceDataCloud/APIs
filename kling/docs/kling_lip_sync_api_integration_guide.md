# Kling Lip Sync API Integration Guide

This article introduces the Kling Lip Sync API integration instructions. By inputting a Kling-generated video and audio or text, you can generate a talking video where the character speaks in sync (lip sync).

## Application Process

To use the API, you need to first apply for the corresponding service on the [Kling Lip Sync API](https://platform.acedata.cloud/documents/kling-lip-sync) page. After entering the page, click the "Acquire" button, as shown in the image:

![](https://cdn.acedata.cloud/q6ytrc.png)

If you are not logged in or registered, you will be automatically redirected to the login page inviting you to register and log in. After logging in or registering, you will be automatically returned to the current page.

There will be a free quota offered for the first application, allowing you to use the API for free.

## Basic Usage

The Kling Lip Sync API drives an existing Kling video (5s or 10s) with audio or text so the character speaks in sync. You can pair it with `/kling/videos` `image2video` to build a complete talking-photo or digital-human narration pipeline.

- **Endpoint**: `POST https://api.acedata.cloud/kling/lip-sync`
- **Pricing**: 2.45 Credits per successful call

### Request Headers

- `accept`: the format of the response result you want to receive, filled in as `application/json`, which means JSON format.
- `authorization`: the key to call the API, which can be directly selected from the dropdown after application.
- `content-type`: `application/json`.

### Request Body Parameters

- `mode` (required): generation mode. Options: `audio2video` (drive lip sync with an audio clip), `text2video` (generate speech from text and drive lip sync).
- `video_id`: ID of a Kling-generated video (e.g., the `video_id` returned by `/kling/videos` image2video). Only 5s/10s videos generated within the last 30 days. Provide `video_id` OR `video_url`, not both.
- `video_url`: public URL of a video. Constraints: `.mp4`/`.mov`, ≤100MB, 2–10s, 720p/1080p only, dimensions 720–1920px. Provide `video_id` OR `video_url`.
- `audio_url`: download URL of the driving audio. Required when `mode=audio2video` and `audio_type=url`. Formats: `.mp3`/`.wav`/`.m4a`/`.aac`, ≤5MB.
- `audio_type`: how audio is supplied. Options: `url` (default), `file`.
- `audio_file`: base64 of the audio file. Required when `audio_type=file`. Same formats, ≤5MB.
- `text`: text to speak. Required when `mode=text2video`, max 120 characters.
- `voice_id`: voice ID. Required when `mode=text2video`.
- `voice_language`: voice language. Options: `zh` (default), `en`. Used when `text2video`.
- `voice_speed`: speech rate, range `0.8`–`2.0`, one decimal place. Default `1.0`. Used when `text2video`.
- `callback_url`: the URL to which the result will be sent upon completion. Providing this switches to async mode.
- `async`: async mode. When `true`, returns `task_id` immediately; poll via `/kling/tasks` or receive `callback_url`.

## Audio-Driven Example (audio2video)

The following example drives a Kling video with an audio file:

```shell
curl -X POST 'https://api.acedata.cloud/kling/lip-sync' \
-H 'accept: application/json' \
-H 'authorization: ******' \
-H 'content-type: application/json' \
-d '{
  "mode": "audio2video",
  "video_id": "895055164389466178",
  "audio_url": "https://cdn.acedata.cloud/6f7d62b18b.wav"
}'
```

The returned result looks like:

```json
{
  "success": true,
  "task_id": "07a3ec65-9f7e-4a09-b7b7-282684082527",
  "video_id": "895055968777281546",
  "video_url": "https://platform2.cdn.acedata.cloud/kling/07a3ec65-9f7e-4a09-b7b7-282684082527.mp4",
  "duration": "4.966",
  "state": "succeed"
}
```

The returned result contains multiple fields, described as follows:

- `success`: whether the call succeeded.
- `task_id`: the ID of the task (use with `/kling/tasks` to query).
- `video_id`: the Kling ID of the generated video (reusable for the next `extend` or `lip-sync`).
- `video_url`: the URL of the talking video.
- `duration`: the video duration in seconds.
- `state`: the task status: `succeed` or `failed`.

## Text-Driven Example (text2video)

The following example generates speech from text and drives lip sync:

```shell
curl -X POST 'https://api.acedata.cloud/kling/lip-sync' \
-H 'accept: application/json' \
-H 'authorization: ******' \
-H 'content-type: application/json' \
-d '{
  "mode": "text2video",
  "video_id": "895055164389466178",
  "text": "Hi, long time no see. I am doing well, take care of yourself.",
  "voice_id": "genshin_vindi2",
  "voice_language": "en",
  "voice_speed": 1.0
}'
```

## Full Pipeline: Talking Photo (image2video → lip-sync)

You can chain the `/kling/videos` image2video action with the lip-sync API to build a complete talking-photo pipeline:

```shell
# Step 1: animate the photo to get a video_id
curl -X POST 'https://api.acedata.cloud/kling/videos' \
-H 'accept: application/json' \
-H 'authorization: ******' \
-H 'content-type: application/json' \
-d '{
  "model": "kling-v2-1-master",
  "action": "image2video",
  "start_image_url": "https://cdn.acedata.cloud/4hfydw.jpg",
  "prompt": "look at camera, natural",
  "duration": 5,
  "mode": "pro"
}'
# → { "video_id": "895055164389466178", ... }

# Step 2: lip-sync the animated video with audio
curl -X POST 'https://api.acedata.cloud/kling/lip-sync' \
-H 'accept: application/json' \
-H 'authorization: ******' \
-H 'content-type: application/json' \
-d '{
  "mode": "audio2video",
  "video_id": "895055164389466178",
  "audio_url": "https://your.cdn/voice.mp3"
}'
```

## Asynchronous Callback

Since the Kling Lip Sync API may take some time to process, the API also supports asynchronous callbacks.

The overall flow is: the client specifies an additional `callback_url` field when making the request. The API immediately returns a result containing a `task_id` field representing the current task ID. When the task completes, the generated video result is sent via POST JSON to the specified `callback_url`, also including the `task_id` field.

You can also poll the status using `/kling/tasks` with body `{ "action": "retrieve", "id": "<task_id>" }`.

## Error Handling

When calling the API, if an error occurs, the API will return the corresponding error code and message. For example:

- `400 bad_request`: Bad request, possibly due to missing or invalid parameters (e.g., no mode, video/audio conflict, text over 120 characters).
- `401 authorization_missing`: Unauthorized, missing or invalid API key.
- `403 forbidden`: Blocked by content moderation.
- `429 too_many_requests`: Too many requests, you have exceeded the rate limit.
- `500 api_error`: Internal server error, something went wrong on the server.

### Error Response Example

```json
{
  "success": false,
  "error": {
    "code": "bad_request",
    "message": "one of video_id or video_url is required"
  },
  "trace_id": "f07cab09-3c18-4d74-9030-64ee840d9f16",
  "task_id": "f490537f-2e5c-4739-8149-6252fba2091c"
}
```

## Notes

- `video_id` must be a Kling video generated within 30 days and 5s or 10s; otherwise pass a constraint-compliant video via `video_url`.
- A clear, frontal, single-person video gives the best lip-sync results.
- Audio or text length should match the video length (audio no longer than the video).
- Billing happens on success (2.45 Credits/call); validation failures (4xx) are not billed.

## Conclusion

Through this document, you have learned how to use the Kling Lip Sync API to drive an existing video with audio or text to produce a talking video. We hope this document helps you integrate and use the API more effectively. If you have any questions, please feel free to contact our technical support team.
