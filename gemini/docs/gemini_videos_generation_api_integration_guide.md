# Gemini Videos Generation API Integration Instructions

This document introduces the integration instructions for the Gemini Videos Generation API, which can generate Google Gemini (omni-flash) videos by inputting text prompts and optional reference images.

## Application Process

To use the Gemini Videos Generation API, you can first visit the [Gemini Videos Generation API](https://platform.acedata.cloud/documents/gemini-videos) page and click the "Acquire" button to obtain the credentials needed for the request.

If you are not logged in or registered, you will be automatically redirected to the login page inviting you to register and log in. After logging in or registering, you will be automatically returned to the current page.

During the first application, there will be a free quota provided, allowing you to use the API for free.

## Basic Usage

First, understand the basic usage method by inputting the prompt `prompt`, model `model`, and aspect ratio `aspect_ratio`, which will generate the corresponding video.

Here we set the Request Headers, including:

- `accept`: the format of the response result you want to receive, here filled in as `application/json`, which is JSON format.
- `authorization`: the key to call the API, which can be selected directly after application.

Additionally, we set the Request Body, including:

- `prompt`: the text prompt describing the content of the video to be generated, **required**.
- `model`: the model for generating the video, currently only supports `omni-flash`, which is the default.
- `aspect_ratio`: the aspect ratio of the generated video, optional `16:9` (landscape) or `9:16` (portrait), default is `16:9`.
- `resolution`: optional output resolution, can be `720p` or `1080p`, default is `720p`.
- `image_urls`: an optional array of reference image links used to guide video generation; empty items will be ignored. This parameter is required when using `video_urls` for video editing (at least one image).
- `video_urls`: an optional array of reference video links (up to 1), used for video editing / video reference; when provided, at least one `image_urls` must also be provided.
- `callback_url`: asynchronous callback address; after setting, the API will immediately return `task_id`, and when the task is completed, it will POST the result to this address.
- `async`: optional, when set to `true`, the interface immediately returns `task_id` without needing to provide `callback_url`, and then polls the corresponding task query interface to obtain results.

Click the "Try" button to test, and the result will be similar to the following:

```json
{
  "success": true,
  "task_id": "9258c45f-bed9-4dde-81c2-a70a710a6904",
  "trace_id": "862d6aae-cec0-407f-9524-bc1be2291bcb",
  "data": [
    {
      "id": "dc4b7292-070c-49a8-8183-919bdf8ad59e",
      "video_url": "https://platform2.cdn.acedata.cloud/gemini/9258c45f-bed9-4dde-81c2-a70a710a6904.mp4",
      "state": "succeeded",
      "aspect_ratio": "16:9",
      "prompt": "A cinematic shot of a kitten chasing a butterfly in a sunlit garden"
    }
  ],
  "started_at": 1784112953.856,
  "finished_at": 1784113021.328,
  "elapsed": 67.472,
  "cost": {
    "amount": 1.932,
    "currency": "credit",
    "list_amount": 2.1
  }
}
```

The returned result contains multiple fields, described as follows:

- `success`: whether the video generation request was successful.
- `task_id`: the ID of the video generation task.
- `trace_id`: the tracking ID of this request, used for troubleshooting.
- `data`: the list of generated video results.
  - `id`: the unique identifier of the generated video.
  - `video_url`: the link address of the generated video (`null` when `state` is `pending`).
  - `state`: the status of the video generation task, optional `pending` / `succeeded` / `failed`.
  - `aspect_ratio`: the aspect ratio of the video, consistent with the request parameters.
  - `prompt`: the prompt used to generate the video.

When returned synchronously, the top level will also include fields such as `started_at`, `finished_at`, `elapsed` (time taken, in seconds), and `cost` (the charge for this request, in Credits).

We only need to obtain the generated video from the `video_url` link address in the `data` result.

The corresponding CURL code is as follows:

```shell
curl -X POST 'https://api.acedata.cloud/gemini/videos' \
-H 'authorization: ******' \
-H 'accept: application/json' \
-H 'content-type: application/json' \
-d '{
  "prompt": "A cinematic shot of a kitten chasing a butterfly in a sunlit garden",
  "model": "omni-flash",
  "aspect_ratio": "16:9"
}'
```

The corresponding Python code is as follows:

```python
import requests

url = "https://api.acedata.cloud/gemini/videos"

headers = {
    "accept": "application/json",
    "authorization": "******",
    "content-type": "application/json"
}

payload = {
    "prompt": "A cinematic shot of a kitten chasing a butterfly in a sunlit garden",
    "model": "omni-flash",
    "aspect_ratio": "16:9"
}

response = requests.post(url, json=payload, headers=headers)
print(response.text)
```

## Image to Video

If you want to generate a video based on reference images, you can pass one or more image links in `image_urls` to guide video generation:

```json
{
  "prompt": "The woman slowly turns around and smiles at the camera, gentle breeze",
  "model": "omni-flash",
  "aspect_ratio": "9:16",
  "image_urls": [
    "https://platform2.cdn.acedata.cloud/nanobanana/e44bfceb-1458-4b4b-9d10-21024678f1a3.png"
  ]
}
```

## Video Editing / Reference Video

This API also supports directly inputting a video to generate a new video: pass a reference video link (up to 1) in `video_urls`, and simultaneously provide at least one reference image in `image_urls` (a strict requirement from upstream), then use `prompt` to describe the desired editing effect (changing style, changing scenes, adding or removing elements, etc.).

Video editing takes longer, so it is recommended to submit the task asynchronously with `async: true`:

```json
{
  "prompt": "Turn this sunny tropical beach into a snowy winter scene with heavy snowfall and overcast sky; keep the same beach, palm trees and boat layout.",
  "model": "omni-flash",
  "aspect_ratio": "9:16",
  "resolution": "720p",
  "image_urls": [
    "https://cdn.acedata.cloud/99289603bd.png"
  ],
  "video_urls": [
    "https://platform2.cdn.acedata.cloud/seedance/dd3dc063-3383-4f29-bedc-e771a096758c.mp4"
  ],
  "async": true
}
```

After submission, the API immediately returns the `task_id`:

```json
{
  "task_id": "cd68b4ee-de70-4c94-ac69-997a3fed0284"
}
```

Then use this `task_id` as `id` to poll the [Gemini Tasks API](gemini_tasks_api_integration_guide.md). After the task is completed, you can obtain the newly generated video:

```json
{
  "success": true,
  "task_id": "cd68b4ee-de70-4c94-ac69-997a3fed0284",
  "trace_id": "5b22104b-5a6d-4a4f-8063-69acae1dc1c6",
  "data": [
    {
      "id": "e125d316-3d26-4c65-9413-55baf6be46b8",
      "video_url": "https://platform2.cdn.acedata.cloud/sora/cd68b4ee-de70-4c94-ac69-997a3fed0284.mp4",
      "state": "succeeded",
      "aspect_ratio": "9:16",
      "prompt": "Turn this sunny tropical beach into a snowy winter scene with heavy snowfall and overcast sky; keep the same beach, palm trees and boat layout."
    }
  ],
  "started_at": 1784084482.914,
  "finished_at": 1784084877.09,
  "elapsed": 394.176,
  "cost": {
    "amount": 1.932,
    "currency": "credit",
    "list_amount": 2.1
  }
}
```

If you need higher-definition results, you can set `resolution` to `1080p` (other parameters remain unchanged).

> Note: the generated video and image links have a retention period and will expire, so please download and save the results to your own storage in time.

> Note: at most 1 reference video is allowed; and when `video_urls` is provided, at least one `image_urls` must also be provided, otherwise the following parameter error will be returned:

```json
{
  "success": false,
  "error": {
    "code": "bad_request",
    "message": "image_urls (at least one reference image) is required when video_urls is provided."
  }
}
```

## Asynchronous Callback

Video generation takes some time to process. If you do not want to keep a long connection waiting, you can pass in `callback_url`. In this case, the API will immediately return `task_id`, and will POST the final result to this address after the task is completed:

```json
{
  "prompt": "A cinematic shot of a kitten chasing a butterfly in a sunlit garden",
  "model": "omni-flash",
  "aspect_ratio": "16:9",
  "callback_url": "https://your-domain.com/callback/gemini"
}
```

The result returned immediately is as follows:

```json
{
  "task_id": "04a043bd-6b23-4b4e-945c-ce48158c3eee"
}
```

## Querying Task Results

If you use an asynchronous callback or want to actively query the task status, you can use the [Gemini Tasks API](gemini_tasks_api_integration_guide.md) (`POST https://api.acedata.cloud/gemini/tasks`) to query the latest status and result of the task by `task_id`. Pass the `task_id` returned when creating the video as `id` in the request body:

```json
{
  "id": "04a043bd-6b23-4b4e-945c-ce48158c3eee"
}
```

After the task is completed, the returned result is similar to the following. The structure of `response.data` is consistent with the synchronous generation (when generating, `state` is `pending` and `video_url` is `null`):

```json
{
  "id": "04a043bd-6b23-4b4e-945c-ce48158c3eee",
  "type": "videos",
  "request": {
    "model": "omni-flash",
    "prompt": "Time-lapse photography of clouds over snowy mountains at sunrise",
    "aspect_ratio": "16:9",
    "async": true
  },
  "response": {
    "success": true,
    "task_id": "04a043bd-6b23-4b4e-945c-ce48158c3eee",
    "data": [
      {
        "id": "486ebd5a-6a4b-406c-84ae-33835de4fe19",
        "video_url": "https://platform2.cdn.acedata.cloud/gemini/04a043bd-6b23-4b4e-945c-ce48158c3eee.mp4",
        "state": "succeeded",
        "aspect_ratio": "16:9",
        "prompt": "Time-lapse photography of clouds over snowy mountains at sunrise"
      }
    ],
    "elapsed": 96.716,
    "cost": {
      "amount": 1.932,
      "currency": "credit",
      "list_amount": 2.1
    }
  }
}
```

## Error Handling

When there is a problem with the request, the API will return the corresponding error code and description. Common ones are as follows:

- `400`: the request parameters are incorrect, for example `prompt` is missing or the value of `aspect_ratio` is illegal.
- `401`: authentication failed, the token is invalid or does not match the API.
- `403`: insufficient balance, or the prompt was rejected by content moderation.
- `500`: internal server error or upstream generation failure.
