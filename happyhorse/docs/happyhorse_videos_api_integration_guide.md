# HappyHorse Videos Generation API Integration Instructions

This article introduces the HappyHorse Videos Generation API integration guide, which allows you to generate videos by inputting custom parameters such as prompt, action, model, and optional reference images or videos.

## Application Process

To use the API, you first need to apply for the corresponding service on the [HappyHorse Videos Generation API](https://platform.acedata.cloud/documents/happyhorse-videos) page. After entering the page, click the "Acquire" button.

If you are not logged in or registered, you will be automatically redirected to the login page inviting you to register and log in. After logging in or registering, you will automatically return to the current page.

Upon your first application, there will be a free quota available for you to use the API for free.

## Basic Usage

To generate a video, pass an `action` of `generate` along with a `prompt` and the desired `model`. The default model is `happyhorse-1.1-t2v` for text-to-video generation.

The request headers include:

- `accept`: the format of the response you want to receive, filled in as `application/json`.
- `authorization`: the API key obtained after application.

The request body includes:

- `action`: the action for this video generation task. Supported values: `generate`, `image_to_video`, `reference_to_video`, `video_edit`.
- `model`: the video generation model. See supported models below.
- `prompt`: the text prompt describing the video to generate.
- `image_url`: a single reference image URL (used with `image_to_video`).
- `image_urls`: an array of image URLs (used with `reference_to_video`).
- `video_url`: a reference video URL (used with `video_edit`).
- `resolution`: output resolution, either `720P` or `1080P`. Default is `1080P`.
- `ratio`: output aspect ratio. Supported values: `16:9`, `9:16`, `1:1`, `4:3`, `3:4`. Default is `16:9`.
- `duration`: video duration in seconds (3–15). Default is `5`.
- `watermark`: whether to add a watermark. Default is `false`.
- `audio_setting`: audio generation mode. Use `auto` to generate AI audio or `origin` to preserve original audio. Default is `auto`.
- `seed`: random seed (0–2147483647) for reproducible results.
- `callback_url`: asynchronous callback URL.
- `async`: whether to use asynchronous mode.

### Supported Models

| Model | Type |
|-------|------|
| `happyhorse-1.0-t2v` | Text-to-video |
| `happyhorse-1.1-t2v` | Text-to-video (latest) |
| `happyhorse-1.0-i2v` | Image-to-video |
| `happyhorse-1.1-i2v` | Image-to-video (latest) |
| `happyhorse-1.0-r2v` | Reference-to-video |
| `happyhorse-1.1-r2v` | Reference-to-video (latest) |
| `happyhorse-1.0-video-edit` | Video editing |

## Text-to-Video

Use `action: generate` with a text `prompt` to generate a video from a description:

```shell
curl -X POST 'https://api.acedata.cloud/happyhorse/videos' \
-H 'accept: application/json' \
-H 'authorization: ******' \
-H 'content-type: application/json' \
-d '{
  "action": "generate",
  "model": "happyhorse-1.1-t2v",
  "prompt": "A cinematic white horse lifts its head, the mane moves gently in the sunrise wind, slow camera push in, warm film lighting"
}'
```

The returned result is as follows:

```json
{
  "success": true,
  "task_id": "27837f92-d1c1-4db4-ad9a-4e6e81d9f6c1",
  "trace_id": "6071ab5e-2f37-46f0-9e07-f1e378112e69",
  "data": [
    {
      "id": "9650580f-6d9e-4bc1-823a-29011790c5cb",
      "video_url": "https://platform2.cdn.acedata.cloud/happyhorse/27837f92-d1c1-4db4-ad9a-4e6e81d9f6c1.mp4",
      "state": "succeeded",
      "duration": 5,
      "resolution": "720P",
      "ratio": null
    }
  ]
}
```

The returned result contains multiple fields, described as follows:

- `success`: indicates whether the video generation task succeeded.
- `task_id`: the ID of the current video generation task.
- `trace_id`: the trace ID of the current video generation task.
- `data`: the result list of the current video generation task.
  - `id`: the unique ID of the generated video.
  - `video_url`: the URL of the generated video.
  - `state`: the status of the task (`pending`, `succeeded`, or `error`).
  - `duration`: the duration of the generated video in seconds.
  - `resolution`: the resolution of the generated video.
  - `ratio`: the aspect ratio of the generated video.

## Image-to-Video

Use `action: image_to_video` along with `image_url` to generate a video from a reference image:

```shell
curl -X POST 'https://api.acedata.cloud/happyhorse/videos' \
-H 'accept: application/json' \
-H 'authorization: ******' \
-H 'content-type: application/json' \
-d '{
  "action": "image_to_video",
  "model": "happyhorse-1.1-i2v",
  "prompt": "The horse slowly turns its head and walks forward",
  "image_url": "https://cdn.acedata.cloud/b1c82e4937.png"
}'
```

## Reference-to-Video

Use `action: reference_to_video` along with `image_urls` (an array of images) to generate a video that incorporates multiple reference images:

```shell
curl -X POST 'https://api.acedata.cloud/happyhorse/videos' \
-H 'accept: application/json' \
-H 'authorization: ******' \
-H 'content-type: application/json' \
-d '{
  "action": "reference_to_video",
  "model": "happyhorse-1.1-r2v",
  "prompt": "The horse gallops through the meadow at sunrise",
  "image_urls": [
    "https://cdn.acedata.cloud/b1c82e4937.png",
    "https://cdn.acedata.cloud/example2.png"
  ]
}'
```

## Video Editing

Use `action: video_edit` along with `video_url` and a `prompt` to edit an existing video:

```shell
curl -X POST 'https://api.acedata.cloud/happyhorse/videos' \
-H 'accept: application/json' \
-H 'authorization: ******' \
-H 'content-type: application/json' \
-d '{
  "action": "video_edit",
  "model": "happyhorse-1.0-video-edit",
  "prompt": "Add cinematic color grading and slow motion effect",
  "video_url": "https://platform2.cdn.acedata.cloud/happyhorse/27837f92-d1c1-4db4-ad9a-4e6e81d9f6c1.mp4"
}'
```

## Asynchronous Callback

Since video generation can take some time, the API supports asynchronous callbacks. When the client sends a request with a `callback_url` field, the API immediately returns a result containing a `task_id`. When the task is completed, the result is sent to the specified `callback_url` as a POST request in JSON format, including the same `task_id` for correlation.

Example request with callback:

```shell
curl -X POST 'https://api.acedata.cloud/happyhorse/videos' \
-H 'accept: application/json' \
-H 'authorization: ******' \
-H 'content-type: application/json' \
-d '{
  "action": "generate",
  "model": "happyhorse-1.1-t2v",
  "prompt": "A cinematic white horse lifts its head, the mane moves gently in the sunrise wind",
  "callback_url": "https://webhook.site/your-unique-id"
}'
```

The immediate response will be:

```json
{
  "task_id": "27837f92-d1c1-4db4-ad9a-4e6e81d9f6c1"
}
```

When the task is complete, the callback URL will receive the full result including the `video_url`.

## Error Handling

When calling the API, if an error occurs, the API will return the corresponding error code and message. For example:

- `400 bad_request`: Bad request, possibly due to missing or invalid parameters (e.g., prompt is required for text-to-video).
- `401 invalid_token`: Unauthorized, invalid or missing authorization token.
- `403 used_up`: Insufficient balance; please top up your account on Ace Data Cloud.
- `429 too_many_requests`: Too many requests; you have exceeded the rate limit.
- `500 api_error`: Internal server error.

### Error Response Example

```json
{
  "error": {
    "code": "bad_request",
    "message": "prompt is required for text-to-video."
  },
  "trace_id": "2efa9340-b21b-4e26-9e14-4aac95f343ab"
}
```

## Conclusion

Through this document, you have learned how to use the HappyHorse Videos Generation API to generate videos using text prompts, reference images, or existing videos. We hope this document helps you better integrate and use this API. If you have any questions, please feel free to contact our technical support team.
