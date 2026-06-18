# Kling Talking Photo API Integration Guide

This article introduces the Kling Talking Photo API integration instructions. By inputting a portrait image and an audio track, you can generate an animated talking-head video where the character's lip movements are synchronized to the audio.

## Application Process

To use the API, you need to first apply for the corresponding service on the [Kling Talking Photo API](https://platform.acedata.cloud/documents/kling-talking-photo) page. After entering the page, click the "Acquire" button, as shown in the image:

![](https://cdn.acedata.cloud/q6ytrc.png)

If you are not logged in or registered, you will be automatically redirected to the login page inviting you to register and log in. After logging in or registering, you will be automatically returned to the current page.

There will be a free quota offered for the first application, allowing you to use the API for free.

## Basic Usage

First, understand the basic usage method: provide a portrait image URL (`image_url`) and an audio URL (`audio_url`). The API animates the face in the image so that the character's lip movements match the provided audio.

### Request Body Parameters

- `image_url`: **(required)** URL of the portrait image. The face in this image will be animated to match the audio.
- `audio_url`: **(required)** URL of the audio file to drive the talking animation.
- `prompt`: optional text prompt to guide the generation.
- `model`: the model to use for generation. Supported models: `kling-v1`, `kling-v1-6`, `kling-v2-master`, `kling-v2-1-master`, `kling-v2-5-turbo`, `kling-v2-6`. Default: `kling-v2-1-master`.
- `duration`: video duration in seconds. Options: `5` or `10`. Default: `5`.
- `mode`: the generation mode. Options: standard mode `std` or high-quality mode `pro`. Default: `pro`.
- `callback_url`: the URL to which the result will be sent upon completion.
- `async`: whether to return immediately with a `task_id` instead of waiting for the result. Default: `false`.

## Example

The following example generates a talking photo video from a portrait image and an audio file:

```shell
curl -X POST 'https://api.acedata.cloud/kling/talking-photo' \
-H 'accept: application/json' \
-H 'authorization: ******' \
-H 'content-type: application/json' \
-d '{
  "image_url": "https://cdn.acedata.cloud/sample-portrait.jpg",
  "audio_url": "https://cdn.acedata.cloud/sample-audio.mp3",
  "model": "kling-v2-1-master",
  "mode": "pro",
  "duration": 5
}'
```

Upon success, the API returns:

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

- `success`: the status of the video generation task.
- `task_id`: the ID of the video generation task.
- `video_id`: the video ID of the generated talking photo video.
- `video_url`: the URL of the final generated video with the face animated to match the audio.
- `source_video_url`: the URL of the intermediate source video produced during generation.
- `duration`: the duration of the generated video in seconds.
- `state`: the current state of the task.

## Python Example

```python
import requests

url = "https://api.acedata.cloud/kling/talking-photo"

headers = {
    "accept": "application/json",
    "authorization": "******",
    "content-type": "application/json"
}

payload = {
    "image_url": "https://cdn.acedata.cloud/sample-portrait.jpg",
    "audio_url": "https://cdn.acedata.cloud/sample-audio.mp3",
    "model": "kling-v2-1-master",
    "mode": "pro",
    "duration": 5
}

response = requests.post(url, json=payload, headers=headers)
print(response.text)
```

## Asynchronous Callback

Since the Kling Talking Photo API may take some time to process, the API supports asynchronous callbacks. Set `async` to `true` and provide a `callback_url` to receive the result when the task completes.

The overall flow is: the client specifies an additional `callback_url` field when making the request. The API immediately returns a result containing a `task_id` field representing the current task ID. When the task completes, the generated video result is sent via POST JSON to the specified `callback_url`, also including the `task_id` field, so the task result can be associated by ID.

Below is an example of how to use this feature.

First, a Webhook callback is an HTTP service that can receive requests. Developers should replace it with the URL of their own HTTP server. For demonstration purposes, we use the public Webhook sample site https://webhook.site/. Opening this site gives you a Webhook URL, as shown:

![](https://cdn.acedata.cloud/tbcnai.png)

Copy this URL to use as the Webhook. The sample URL here is `https://webhook.site/624b2c78-6dbd-4618-9d2b-b32eade6d8c3`.

Next, set the `callback_url` field to the above Webhook URL and fill in the corresponding parameters:

```shell
curl -X POST 'https://api.acedata.cloud/kling/talking-photo' \
-H 'accept: application/json' \
-H 'authorization: ******' \
-H 'content-type: application/json' \
-d '{
  "image_url": "https://cdn.acedata.cloud/sample-portrait.jpg",
  "audio_url": "https://cdn.acedata.cloud/sample-audio.mp3",
  "async": true,
  "callback_url": "https://webhook.site/624b2c78-6dbd-4618-9d2b-b32eade6d8c3"
}'
```

After running, you will immediately get a result like:

```json
{
  "task_id": "0c0b4d3a-2f1e-4a6b-9c2d-2b3c4d5e6f70"
}
```

When the task completes, the full result is POSTed to the specified `callback_url`. The result includes a `task_id` field so that task results can be correlated by ID.

## Error Handling

When calling the API, if an error occurs, the API will return the corresponding error code and message. For example:

- `400 bad_request`: Bad request, possibly due to missing or invalid parameters (e.g., `image_url` or `audio_url` not provided).
- `401 authorization_missing`: Unauthorized, invalid or missing authorization token.
- `500 api_error`: Internal server error, something went wrong on the server.

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

## Conclusion

Through this document, you have learned how to use the Kling Talking Photo API to generate animated talking-head videos by providing a portrait image and an audio track. We hope this document helps you integrate and use the API more effectively. If you have any questions, please feel free to contact our technical support team.
