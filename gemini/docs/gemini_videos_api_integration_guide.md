# Gemini Videos Generation API Integration Guide

This document will introduce the integration instructions for the Gemini Videos Generation API, which can generate Google Gemini (omni-flash) videos by inputting text prompts (and optional reference images).

## Application Process

To use the Gemini Videos Generation API, apply for the corresponding service on the [Gemini Videos Generation API](https://platform.acedata.cloud/documents/gemini-videos) page. After entering the page, click the "Acquire" button.

If you are not logged in or registered, you will be automatically redirected to the login page. Upon the first application, there will be a free quota provided.

## Basic Usage

The request body fields:

- `prompt`: the text prompt describing the content you want to generate in the video, **required**.
- `model`: the model for generating the video, currently only supports `omni-flash`, which is the default.
- `aspect_ratio`: the aspect ratio of the generated video, optional `16:9` (landscape) or `9:16` (portrait), default is `16:9`.
- `resolution`: optional output resolution, can be `720p` or `1080p`, default is `720p`.
- `image_urls`: an optional array of reference image links used to guide video generation; empty items will be ignored. This parameter is required when using `video_urls` for video editing (at least one image).
- `video_urls`: an optional array of reference video links (up to 1), used for **video editing / video reference**; when provided, at least one `image_urls` must also be provided.
- `callback_url`: asynchronous callback address; after setting, the API will immediately return `task_id`, and when the task is completed, it will POST the result to this address.
- `async`: optional, when set to `true`, the interface immediately returns `task_id`, no need to provide `callback_url`, and then the result can be polled through the corresponding task query interface.

### Request Example

```bash
curl -X POST 'https://api.acedata.cloud/gemini/videos' -H 'authorization: ******' -H 'accept: application/json' -H 'content-type: application/json' -d '{
  "prompt": "A cinematic shot of a kitten chasing a butterfly in a sunlit garden",
  "model": "omni-flash",
  "aspect_ratio": "16:9"
}'
```

### Response Example

```json
{
  "success": true,
  "task_id": "b8976e18-32dc-4718-9ed8-1ea090fcb6ea",
  "trace_id": "fb751e1e-4705-49ea-9fd4-5024b7865ea2",
  "data": [
    {
      "id": "omni-flash:job_01k777hjrbfrgs2060q5zvf2a5",
      "video_url": "https://cdn.acedata.cloud/gemini/example-video.mp4",
      "state": "succeeded"
    }
  ]
}
```

Response fields:

- `success`: whether the video generation request was successful.
- `task_id`: the ID of the video generation task.
- `trace_id`: the tracking ID of this request, used for troubleshooting.
- `data`: the list of generated video results.
  - `id`: the unique identifier of the generated video.
  - `video_url`: the link address of the generated video.
  - `state`: the status of the video generation task, optional `pending` / `succeeded` / `failed`.

## Image to Video

If you want to generate a video based on reference images, you can pass one or more image links in `image_urls`:

```json
{
  "prompt": "The character slowly turns around and smiles at the camera",
  "model": "omni-flash",
  "aspect_ratio": "9:16",
  "image_urls": [
    "https://cdn.acedata.cloud/example-reference.png"
  ]
}
```

## Video Editing / Reference Video

Pass a reference video link (up to 1) in `video_urls`, and **simultaneously** provide at least one reference image in `image_urls`. Use `prompt` to describe the editing effect:

```json
{
  "prompt": "Restyle the video into cinematic anime, keep the motion",
  "model": "omni-flash",
  "aspect_ratio": "16:9",
  "resolution": "720p",
  "image_urls": [
    "https://cdn.acedata.cloud/example-reference.png"
  ],
  "video_urls": [
    "https://cdn.acedata.cloud/example-source.mp4"
  ]
}
```

> Note: A maximum of 1 reference video; when providing `video_urls`, at least one `image_urls` must be provided.

## Asynchronous Callback

Video generation requires some processing time. Pass in `callback_url` to get the result via webhook:

```json
{
  "prompt": "A cinematic shot of a kitten chasing a butterfly in a sunlit garden",
  "model": "omni-flash",
  "aspect_ratio": "16:9",
  "callback_url": "https://your-domain.com/callback/gemini"
}
```

The immediately returned result:

```json
{
  "task_id": "b8976e18-32dc-4718-9ed8-1ea090fcb6ea"
}
```

## Query Task Results

Query task status via the [Gemini Tasks API](https://platform.acedata.cloud/documents/gemini-tasks) (`POST https://api.acedata.cloud/gemini/tasks`) using `task_id`.

## Error Handling

- `400`: The request parameters are incorrect, such as missing `prompt` or invalid `aspect_ratio`.
- `401`: Authentication failed, the token is invalid or does not match the API.
- `403`: Insufficient balance, or the prompt has been rejected by content review.
- `500`: Internal server error or upstream generation failure.
