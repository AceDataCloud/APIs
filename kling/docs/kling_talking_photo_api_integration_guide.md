# Kling Talking Photo API Integration Guide

This article introduces the Kling Talking Photo API integration instructions. By inputting a portrait image and an audio file, you can generate a talking-head video where the character in the photo speaks in sync with the provided audio.

## Application Process

To use the API, you need to first apply for the corresponding service on the [Kling Talking Photo API](https://platform.acedata.cloud/documents/kling-talking-photo) page. After entering the page, click the "Acquire" button, as shown in the image:

![](https://cdn.acedata.cloud/q6ytrc.png)

If you are not logged in or registered, you will be automatically redirected to the login page inviting you to register and log in. After logging in or registering, you will be automatically returned to the current page.

There will be a free quota offered for the first application, allowing you to use the API for free.

## Basic Usage

The Kling Talking Photo API takes a portrait image and an audio file and generates a video where the person in the image appears to be speaking the audio. You can optionally provide a text prompt and choose a model, duration, and quality mode.

### Request Headers

- `accept`: the format of the response result you want to receive, filled in as `application/json`.
- `authorization`: the key to call the API, which can be directly selected from the dropdown after application.

### Request Body

- `image_url` (required): the URL of the portrait image. The face in this image will be animated.
- `audio_url` (required): the URL of the audio file that the character will lip-sync to.
- `prompt`: an optional text prompt to guide the video generation style.
- `model`: the model to use for generation. Options: `kling-v1`, `kling-v1-6`, `kling-v2-master`, `kling-v2-1-master` (default), `kling-v2-5-turbo`, `kling-v2-6`.
- `duration`: the duration of the generated video in seconds. Options: `5` (default) or `10`.
- `mode`: the quality mode. Options: `std` (standard) or `pro` (high quality, default).
- `callback_url`: optional URL to receive the result via POST when the task completes.
- `async`: whether to run the task asynchronously. Default: `false`.

### Code Example

#### CURL

```bash
curl -X POST 'https://api.acedata.cloud/kling/talking-photo' \
-H 'accept: application/json' \
-H 'authorization: ******' \
-H 'content-type: application/json' \
-d '{
  "image_url": "https://cdn.acedata.cloud/portrait-sample.jpg",
  "audio_url": "https://cdn.acedata.cloud/speech-sample.mp3",
  "model": "kling-v2-1-master",
  "duration": 5,
  "mode": "pro"
}'
```

#### Python

```python
import requests

url = "https://api.acedata.cloud/kling/talking-photo"

headers = {
    "accept": "application/json",
    "authorization": "******",
    "content-type": "application/json"
}

payload = {
    "image_url": "https://cdn.acedata.cloud/portrait-sample.jpg",
    "audio_url": "https://cdn.acedata.cloud/speech-sample.mp3",
    "model": "kling-v2-1-master",
    "duration": 5,
    "mode": "pro"
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
  "video_id": "895055968777281546",
  "video_url": "https://platform2.cdn.acedata.cloud/kling/07a3ec65-9f7e-4a09-b7b7-282684082527.mp4",
  "source_video_url": "https://platform2.cdn.acedata.cloud/kling/163ac822-1a15-4f5e-a2eb-465154df15af.mp4",
  "duration": 5,
  "state": "succeed"
}
```

The response fields are:

- `success`: whether the talking photo task succeeded.
- `task_id`: the ID of the talking photo task.
- `video_id`: the video ID of the generated talking-head video.
- `video_url`: the URL of the final generated video.
- `source_video_url`: the URL of the intermediate source video.
- `duration`: the duration of the generated video in seconds.
- `state`: the current state of the task.

## Asynchronous Callback

Since the Kling Talking Photo API may take some time to process, the API supports asynchronous callbacks.

Set `async` to `true` and provide a `callback_url`. The API will immediately return a `task_id`, and when the task completes, it will POST the result to the specified `callback_url`.

```bash
curl -X POST 'https://api.acedata.cloud/kling/talking-photo' \
-H 'accept: application/json' \
-H 'authorization: ******' \
-H 'content-type: application/json' \
-d '{
  "image_url": "https://cdn.acedata.cloud/portrait-sample.jpg",
  "audio_url": "https://cdn.acedata.cloud/speech-sample.mp3",
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

- `400 bad_request`: Bad request, possibly due to missing or invalid parameters (e.g., missing `image_url` or `audio_url`).
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

Through this document, you have learned how to use the Kling Talking Photo API to create talking-head videos from portrait images and audio. We hope this document helps you integrate and use the API more effectively. If you have any questions, please feel free to contact our technical support team.
