# Kling Lip Sync API Integration Guide

This article introduces the Kling Lip Sync API integration instructions. By inputting a video and an audio source or text, you can generate a lip-synced video where the character's mouth movements match the provided audio.

## Application Process

To use the API, you need to first apply for the corresponding service on the [Kling Lip Sync API](https://platform.acedata.cloud/documents/kling-lip-sync) page. After entering the page, click the "Acquire" button, as shown in the image:

![](https://cdn.acedata.cloud/q6ytrc.png)

If you are not logged in or registered, you will be automatically redirected to the login page inviting you to register and log in. After logging in or registering, you will be automatically returned to the current page.

There will be a free quota offered for the first application, allowing you to use the API for free.

## Basic Usage

The Kling Lip Sync API supports two modes:

- `audio2video`: Drive lip sync using an existing audio file or audio URL.
- `text2video`: Drive lip sync using synthesized speech generated from provided text.

You must provide either a `video_id` (from a previously generated Kling video) or a `video_url` pointing to the source video to be lip-synced.

### Request Headers

- `accept`: the format of the response result you want to receive, filled in as `application/json`.
- `authorization`: the key to call the API, which can be directly selected from the dropdown after application.

### Request Body

- `mode` (required): the lip sync mode. Options: `audio2video` or `text2video`.
- `video_id`: the Kling video ID to apply lip sync to. Either `video_id` or `video_url` is required.
- `video_url`: the URL of the source video to apply lip sync to. Either `video_id` or `video_url` is required.
- `audio_url`: the URL of the audio file for lip sync. Required when `mode` is `audio2video` and `audio_type` is `url`.
- `audio_type`: the type of audio input. Options: `url` (default) or `file`.
- `audio_file`: base64-encoded audio file content. Used when `audio_type` is `file`.
- `text`: the text to synthesize into speech for lip sync. Maximum 120 characters. Required when `mode` is `text2video`.
- `voice_id`: the voice ID to use for text-to-speech synthesis.
- `voice_language`: the language of the synthesized voice. Options: `zh` (Chinese, default) or `en` (English).
- `voice_speed`: the speed of the synthesized voice. Range: 0.8–2.0. Default: `1.0`.
- `callback_url`: optional URL to receive the result via POST when the task completes.
- `async`: whether to run the task asynchronously. Default: `false`.

### Code Example

#### CURL (audio2video)

```bash
curl -X POST 'https://api.acedata.cloud/kling/lip-sync' \
-H 'accept: application/json' \
-H 'authorization: ******' \
-H 'content-type: application/json' \
-d '{
  "mode": "audio2video",
  "video_url": "https://cdn.acedata.cloud/sample-video.mp4",
  "audio_url": "https://cdn.acedata.cloud/sample-audio.mp3"
}'
```

#### CURL (text2video)

```bash
curl -X POST 'https://api.acedata.cloud/kling/lip-sync' \
-H 'accept: application/json' \
-H 'authorization: ******' \
-H 'content-type: application/json' \
-d '{
  "mode": "text2video",
  "video_url": "https://cdn.acedata.cloud/sample-video.mp4",
  "text": "Hello, welcome to Ace Data Cloud.",
  "voice_language": "en"
}'
```

#### Python

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
    "video_url": "https://cdn.acedata.cloud/sample-video.mp4",
    "audio_url": "https://cdn.acedata.cloud/sample-audio.mp3"
}

response = requests.post(url, json=payload, headers=headers)
print(response.text)
```

### Response Example

A successful response looks like:

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

The response fields are:

- `success`: whether the lip sync task succeeded.
- `task_id`: the ID of the lip sync task.
- `video_id`: the video ID of the generated lip-synced video.
- `video_url`: the URL of the generated lip-synced video.
- `duration`: the duration of the generated video in seconds.
- `state`: the current state of the task.

## Asynchronous Callback

Since the Kling Lip Sync API may take some time to process, the API supports asynchronous callbacks.

Set `async` to `true` and provide a `callback_url`. The API will immediately return a `task_id`, and when the task completes, it will POST the result to the specified `callback_url`.

```bash
curl -X POST 'https://api.acedata.cloud/kling/lip-sync' \
-H 'accept: application/json' \
-H 'authorization: ******' \
-H 'content-type: application/json' \
-d '{
  "mode": "audio2video",
  "video_url": "https://cdn.acedata.cloud/sample-video.mp4",
  "audio_url": "https://cdn.acedata.cloud/sample-audio.mp3",
  "async": true,
  "callback_url": "https://webhook.site/your-webhook-id"
}'
```

The immediate response will be:

```json
{
  "task_id": "0c0b4d3a-2f1e-4a6b-9c2d-2b3c4d5e6f70"
}
```

Once the task completes, the full result will be POSTed to your `callback_url`.

## Error Handling

When calling the API, if an error occurs, the API will return the corresponding error code and message. For example:

- `400 bad_request`: Bad request, possibly due to missing or invalid parameters (e.g., neither `video_id` nor `video_url` provided).
- `401 authorization_missing`: Unauthorized, invalid or missing authorization token.
- `500 api_error`: Internal server error, something went wrong on the server.

### Error Response Example

```json
{
  "code": "bad_request",
  "detail": "one of video_id or video_url is required"
}
```

## Conclusion

Through this document, you have learned how to use the Kling Lip Sync API to implement AI-driven lip sync on videos. We hope this document helps you integrate and use the API more effectively. If you have any questions, please feel free to contact our technical support team.
