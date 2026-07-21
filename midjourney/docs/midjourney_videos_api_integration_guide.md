# Midjourney Videos API Integration Guide

The Midjourney Videos API generates videos from existing Midjourney images or extends previously generated Midjourney videos.

This document provides detailed integration instructions for the Midjourney Videos API, helping you easily integrate and fully utilize its video generation capabilities.

## Application Process

To use the Midjourney Videos API, you first need to apply for the corresponding service on the [Midjourney Videos API](https://platform.acedata.cloud/documents/midjourney-videos) page. After entering the page, click the "Acquire" button, as shown in the image:

![Application Page](https://cdn.acedata.cloud/q6ytrc.png)

If you have not logged in or registered, you will be automatically redirected to the [login page](https://platform.acedata.cloud) inviting you to register and log in. After logging in or registering, you will be automatically returned to the current page.

There is a free quota available for first-time applicants, allowing you to use this API for free.

## Basic Usage

The basic usage involves setting the `action` to `generate` and providing an `image_url` or a reference to an existing Midjourney image to generate a short video.

**Request Headers** include:

- `accept`: Specifies that the response should be in JSON format, set to `application/json`.
- `authorization`: The key to call the API, which can be selected directly from the dropdown after application.

**Request Body** includes:

- `action`: The video generation action. Options: `generate` (create a new video from an image), `extend` (extend an existing video). Required.
- `prompt`: The text prompt describing the desired video content. Example: `A cat sitting on a table`.
- `mode`: The generation mode. Options: `fast`, `turbo`.
- `resolution`: The video resolution. Options: `480p`, `720p`.
- `image_url`: The URL of the source image to animate (used when `action` is `generate`).
- `end_image_url`: The URL of an optional end-frame image for the video.
- `video_id`: The ID of the existing video to extend (used when `action` is `extend`).
- `video_index`: The index of the video to use when multiple videos were generated.
- `loop`: Whether to loop the generated video. Default is `false`.
- `callback_url`: The URL to which the result will be sent upon completion (for async mode).
- `async`: Whether to use asynchronous mode. When `true`, the API returns a `task_id` immediately.

### Generate a Video from an Image

#### CURL

```bash
curl -X POST 'https://api.acedata.cloud/midjourney/videos' \
-H 'accept: application/json' \
-H 'authorization: ******' \
-H 'content-type: application/json' \
-d '{
  "action": "generate",
  "prompt": "A cat sitting on a table, slowly turning its head",
  "image_url": "https://example.com/cat-image.png",
  "resolution": "720p"
}'
```

#### Python

```python
import requests

url = "https://api.acedata.cloud/midjourney/videos"

headers = {
    "accept": "application/json",
    "authorization": "******",
    "content-type": "application/json"
}

payload = {
    "action": "generate",
    "prompt": "A cat sitting on a table, slowly turning its head",
    "image_url": "https://example.com/cat-image.png",
    "resolution": "720p"
}

response = requests.post(url, json=payload, headers=headers)
print(response.text)
```

### Response Example

Upon successful request, the API will return the generated video information. For example:

```json
{
  "success": true,
  "task_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
  "image_id": "1234567890abcdef",
  "progress": 100,
  "image_url": "https://cdn.acedata.cloud/midjourney/video-result.mp4",
  "image_width": "1280",
  "image_height": "720",
  "raw_image_url": "https://cdn.acedata.cloud/midjourney/video-result-raw.mp4",
  "raw_image_width": "1280",
  "raw_image_height": "720",
  "actions": ["extend"]
}
```

The returned result contains multiple fields. The field descriptions are as follows:

- `success`: Whether the video generation task succeeded.
- `task_id`: The ID of the task, used to query the task status via the Tasks API.
- `image_id`: The ID of the generated video asset.
- `progress`: The progress of the task (0–100).
- `image_url`: The URL of the generated video.
- `image_width`: The width of the generated video.
- `image_height`: The height of the generated video.
- `raw_image_url`: The URL of the original full-resolution video.
- `raw_image_width`: The width of the original video.
- `raw_image_height`: The height of the original video.
- `actions`: A list of follow-up actions available for the generated video (e.g., `extend`).

## Video Extension

To extend an existing Midjourney video, set the `action` to `extend` and provide the `video_id` of the video to continue.

```bash
curl -X POST 'https://api.acedata.cloud/midjourney/videos' \
-H 'accept: application/json' \
-H 'authorization: ******' \
-H 'content-type: application/json' \
-d '{
  "action": "extend",
  "video_id": "1234567890abcdef",
  "prompt": "The cat continues to look around the room"
}'
```

## Asynchronous Callback

Since video generation may take a significant amount of time, the API supports asynchronous callbacks to avoid holding the HTTP connection open.

The overall flow is: the client specifies an additional `callback_url` field and sets `async` to `true` when making the request. The API immediately returns a result containing a `task_id` field. When the task completes, the generated video result is sent via POST JSON to the specified `callback_url`.

### Code Example

```bash
curl -X POST 'https://api.acedata.cloud/midjourney/videos' \
-H 'accept: application/json' \
-H 'authorization: ******' \
-H 'content-type: application/json' \
-d '{
  "action": "generate",
  "image_url": "https://example.com/cat-image.png",
  "prompt": "A cat sitting on a table, slowly turning its head",
  "async": true,
  "callback_url": "https://webhook.site/your-webhook-id"
}'
```

The API immediately returns:

```json
{
  "task_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890"
}
```

When the task completes, the full result is posted to your `callback_url`.

## Error Handling

When calling the API, if an error occurs, the API will return the corresponding error code and message. For example:

- `400 token_mismatched`: Bad request, possibly due to missing or invalid parameters.
- `400 api_not_implemented`: Bad request, possibly due to missing or invalid parameters.
- `401 invalid_token`: Unauthorized, invalid or missing authorization token.
- `403 forbidden`: Forbidden, you do not have permission to access this resource.
- `429 too_many_requests`: Too many requests, you have exceeded the rate limit.
- `500 api_error`: Internal server error, something went wrong on the server.
- `504 gateway_timeout`: Gateway timeout, the upstream service did not respond in time.

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

Through this document, you have learned how to use the Midjourney Videos API to generate and extend videos from Midjourney images. We hope this document helps you integrate and use the API more effectively. If you have any questions, please feel free to contact our technical support team.
