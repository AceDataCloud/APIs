# Kling Lip Sync API Integration Guide

This article introduces the Kling Lip Sync API integration instructions. By inputting custom parameters, you can drive an existing Kling video with audio or text so the character speaks in sync (对口型).

## Application Process

To use the API, you need to first apply for the corresponding service on the [Kling Videos Generation API](https://platform.acedata.cloud/documents/3b921a16-a411-4557-8335-53f21d3f9e46) page. After entering the page, click the "Acquire" button, as shown in the image:

![](https://cdn.acedata.cloud/q6ytrc.png)

If you are not logged in or registered, you will be automatically redirected to the login page inviting you to register and log in. After logging in or registering, you will be automatically returned to the current page.

There will be a free quota offered for the first application, allowing you to use the API for free.

## Basic Usage

The Kling Lip Sync API drives an existing Kling video (5s or 10s) with audio or text so the character speaks in sync. It can be paired with the `/kling/videos` image2video action for a full talking-photo pipeline.

You need to provide a source video (via `video_id` or `video_url`) and a driving mode (`mode`):

- `audio2video`: drive the video with an audio clip (`audio_url` required)
- `text2video`: drive the video with text and a voice (`text` and `voice_id` required)

The request parameters are as follows:

- `mode`: the driving mode. Options: `audio2video` or `text2video`.
- `video_id`: ID of a Kling-generated video (e.g. from `/kling/videos` image2video), generated within the last 30 days. Provide this OR `video_url`.
- `video_url`: public URL of a 5s/10s video to lip-sync. Provide this OR `video_id`.
- `audio_url`: public URL of the driving audio (required when `mode` is `audio2video`).
- `audio_type`: how the audio is supplied for `audio2video`. Options: `url` (default) or `file`.
- `text`: text to speak (required when `mode` is `text2video`, max 120 characters).
- `voice_id`: voice to use (required when `mode` is `text2video`).
- `voice_language`: voice language for `text2video`. Default is `zh`.
- `callback_url`: if provided, returns a `task_id` immediately and delivers the result via callback.

### Example: Audio-to-Video

The following CURL example drives an existing video with an audio file:

```shell
curl -X POST 'https://api.acedata.cloud/kling/lip-sync' \
-H 'accept: application/json' \
-H 'authorization: ******' \
-H 'content-type: application/json' \
-d '{
  "mode": "audio2video",
  "video_id": "895047463190134880",
  "audio_url": "https://cdn.acedata.cloud/sample_audio.mp3"
}'
```

### Example: Text-to-Video

The following CURL example drives an existing video with text and a specified voice:

```shell
curl -X POST 'https://api.acedata.cloud/kling/lip-sync' \
-H 'accept: application/json' \
-H 'authorization: ******' \
-H 'content-type: application/json' \
-d '{
  "mode": "text2video",
  "video_id": "895047463190134880",
  "text": "Hello, welcome to Ace Data Cloud.",
  "voice_id": "en_female_1",
  "voice_language": "en"
}'
```

Upon success, the API returns a result like:

```json
{
  "success": true,
  "task_id": "0c0b4d3a-2f1e-4a6b-9c2d-2b3c4d5e6f70",
  "video_id": "895047463190134880",
  "video_url": "https://cdn.acedata.cloud/bafb400e8a.mp4",
  "duration": 5,
  "state": "succeed"
}
```

The returned result contains multiple fields, described as follows:

- `success`: the status of the lip sync task.
- `task_id`: the ID of the lip sync task.
- `video_id`: the video ID of the generated lip sync video.
- `video_url`: the video link of the generated lip sync video.
- `duration`: the duration of the generated video in seconds.
- `state`: the current state of the task.

### Python Example

```python
import requests

url = "https://api.acedata.cloud/kling/lip-sync"

headers = {
    "accept": "application/json",
    "authorization": "******",
    "content-type": "application/json"
}

payload = {
    "mode": "audio2video",
    "video_id": "895047463190134880",
    "audio_url": "https://cdn.acedata.cloud/sample_audio.mp3"
}

response = requests.post(url, json=payload, headers=headers)
print(response.text)
```

## Asynchronous Callback

Since the Kling Lip Sync API may take some time to complete, the API also supports asynchronous callbacks. The overall flow is: the client specifies an additional `callback_url` field when making the request. The API immediately returns a result containing a `task_id` field representing the current task ID. When the task completes, the generated video result is sent via POST JSON to the specified `callback_url`, also including the `task_id` field, so the task result can be associated by ID.

Below is an example of how to use this feature.

First, a Webhook callback is an HTTP service that can receive requests. Developers should replace it with the URL of their own HTTP server. For demonstration purposes, we use the public Webhook sample site https://webhook.site/. Opening this site gives you a Webhook URL, as shown:

![](https://cdn.acedata.cloud/tbcnai.png)

Copy this URL to use as the Webhook. The sample URL here is `https://webhook.site/624b2c78-6dbd-4618-9d2b-b32eade6d8c3`.

Next, set the `callback_url` field to the above Webhook URL and fill in the corresponding parameters:

```shell
curl -X POST 'https://api.acedata.cloud/kling/lip-sync' \
-H 'accept: application/json' \
-H 'authorization: ******' \
-H 'content-type: application/json' \
-d '{
  "mode": "audio2video",
  "video_id": "895047463190134880",
  "audio_url": "https://cdn.acedata.cloud/sample_audio.mp3",
  "callback_url": "https://webhook.site/624b2c78-6dbd-4618-9d2b-b32eade6d8c3"
}'
```

After running, you will immediately get a result like:

```json
{
  "task_id": "0c0b4d3a-2f1e-4a6b-9c2d-2b3c4d5e6f70"
}
```

After a short wait, you can observe the generated video result at the callback URL. The content is as follows:

```json
{
  "success": true,
  "task_id": "0c0b4d3a-2f1e-4a6b-9c2d-2b3c4d5e6f70",
  "video_id": "895047463190134880",
  "video_url": "https://cdn.acedata.cloud/bafb400e8a.mp4",
  "duration": 5,
  "state": "succeed"
}
```

The result includes a `task_id` field. All other fields are similar to those described above, and through this field, task results can be correlated by ID.

## Error Handling

When calling the API, if an error occurs, the API will return the corresponding error code and message. For example:

- `400 token_mismatched`: Bad request, possibly due to missing or invalid parameters.
- `400 api_not_implemented`: Bad request, possibly due to missing or invalid parameters.
- `401 invalid_token`: Unauthorized, invalid or missing authorization token.
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

## Conclusion

Through this document, you have learned how to use the Kling Lip Sync API to drive an existing video with audio or text, making characters speak in sync. We hope this document helps you integrate and use the API more effectively. If you have any questions, please feel free to contact our technical support team.
