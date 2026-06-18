# Kling Lip Sync API Integration Guide

This article introduces the Kling Lip Sync API integration instructions. By inputting custom parameters, you can generate official Kling AI lip sync videos that synchronize a character's lip movements to a provided audio track or synthesized speech.

## Application Process

To use the API, you need to first apply for the corresponding service on the [Kling Lip Sync API](https://platform.acedata.cloud/documents/kling-lip-sync) page. After entering the page, click the "Acquire" button, as shown in the image:

![](https://cdn.acedata.cloud/q6ytrc.png)

If you are not logged in or registered, you will be automatically redirected to the login page inviting you to register and log in. After logging in or registering, you will be automatically returned to the current page.

There will be a free quota offered for the first application, allowing you to use the API for free.

## Basic Usage

The Kling Lip Sync API supports two modes:

- `audio2video`: drive lip movements from an existing audio file or URL.
- `text2video`: synthesize speech from text and drive lip movements from the synthesized audio.

You must provide either `video_id` (from a previously generated Kling video) or `video_url` (a direct URL to a video file) as the source video.

### Request Body Parameters

- `mode`: **(required)** the lip sync mode. Options: `audio2video` or `text2video`.
- `video_id`: the ID of a previously generated Kling video to use as the source.
- `video_url`: a direct URL to the source video file. One of `video_id` or `video_url` is required.
- `audio_url`: URL of the audio file to use for lip sync. Required when `mode=audio2video` and `audio_type=url`.
- `audio_type`: how the audio is provided. Options: `url` (default) or `file`.
- `audio_file`: base64-encoded audio file content. Used when `audio_type=file`.
- `text`: the text to synthesize into speech. Required when `mode=text2video`. Maximum 120 characters.
- `voice_id`: the voice ID to use for text-to-speech synthesis.
- `voice_language`: the language for voice synthesis. Options: `zh` (Chinese, default) or `en` (English).
- `voice_speed`: the speed of the synthesized voice. Range: 0.8–2.0. Default: `1.0`.
- `callback_url`: the URL to which the result will be sent upon completion.
- `async`: whether to return immediately with a `task_id` instead of waiting for the result. Default: `false`.

## Audio-to-Video Example

To drive lip sync from an audio URL, set `mode` to `audio2video` and provide either `video_id` or `video_url` along with `audio_url`:

```shell
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

Upon success, the API returns:

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

## Text-to-Video Example

To synthesize speech from text and drive lip sync, set `mode` to `text2video` and provide `text`, `voice_id`, and optionally `voice_language` and `voice_speed`:

```shell
curl -X POST 'https://api.acedata.cloud/kling/lip-sync' \
-H 'accept: application/json' \
-H 'authorization: ******' \
-H 'content-type: application/json' \
-d '{
  "mode": "text2video",
  "video_url": "https://cdn.acedata.cloud/sample-video.mp4",
  "text": "Hello, welcome to Ace Data Cloud!",
  "voice_id": "en_female_01",
  "voice_language": "en",
  "voice_speed": 1.0
}'
```

The returned result contains multiple fields, described as follows:

- `success`: the status of the lip sync task.
- `task_id`: the ID of the lip sync task.
- `video_id`: the video ID of the generated lip sync video.
- `video_url`: the URL of the generated lip sync video.
- `duration`: the duration of the generated video in seconds.
- `state`: the current state of the task.

## Asynchronous Callback

Since the Kling Lip Sync API may take some time to process, the API supports asynchronous callbacks. Set `async` to `true` and provide a `callback_url` to receive the result when the task completes:

```shell
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

When `async` is `true`, the API immediately returns a result containing only the `task_id`:

```json
{
  "task_id": "0c0b4d3a-2f1e-4a6b-9c2d-2b3c4d5e6f70"
}
```

When the task completes, the full result is POSTed to the specified `callback_url`.

## Error Handling

When calling the API, if an error occurs, the API will return the corresponding error code and message. For example:

- `400 bad_request`: Bad request, possibly due to missing or invalid parameters (e.g., neither `video_id` nor `video_url` was provided).
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

Through this document, you have learned how to use the Kling Lip Sync API to generate lip sync videos by driving a source video with an audio track or synthesized speech. We hope this document helps you integrate and use the API more effectively. If you have any questions, please feel free to contact our technical support team.
