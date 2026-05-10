# Fish Voices Generation API Integration Guide

This article introduces the Fish Voices Generation API integration guide. This API allows you to create your own voice model by providing an audio URL.

## Application Process

To use the API, visit the [Fish Voices Generation API](https://platform.acedata.cloud/documents/55e61b64-ac7d-4710-a7f1-57a4ba786b17) page and click the "Acquire" button, as shown below:

![](https://cdn.acedata.cloud/q6ytrc.png)

If you are not logged in or registered, you will be automatically redirected to the login page. After logging in, you will automatically return to the current page.

Upon your first application, there will be a free quota provided, allowing you to use the API for free.

## Basic Usage

The basic usage involves providing a voice audio URL `voice_url` to obtain the processed result, as shown below:

<p><img src="https://cdn.acedata.cloud/278ikr.png" width="500" class="m-auto"></p>

The Request Headers include:

- `accept`: The response format you want to receive, set to `application/json` for JSON format.
- `authorization`: The API key, which can be selected after application.

The Request Body includes:

- `voice_url`: The URL of the audio sample for the voice model.
- `title`: The title of the voice model.
- `image_urls`: The cover image for the voice model.
- `description`: A description of the voice model.
- `callback_url`: The URL for the asynchronous callback result.

After configuration, the corresponding code is automatically generated on the right side, as shown below:

<p><img src="https://cdn.acedata.cloud/dkdfyj.png" width="500" class="m-auto"></p>

Click the "Try" button to test. The result looks like this:

```json
{
  "success": true,
  "task_id": "b01db503-dd9e-4f92-861a-344f14756217",
  "trace_id": "8731a2f1-7736-4a47-98e7-da942f9346a7",
  "data": {
    "_id": "d5d21261512b4852b9ccd709facf93f3",
    "type": "tts",
    "title": "test",
    "description": "test",
    "cover_image": "coverimage/d5d21261512b4852b9ccd709facf93f3",
    "train_mode": "fast",
    "state": "trained",
    "tags": [],
    "samples": [
      {
        "title": "Default Sample",
        "text": "Through long-term observation, it was found that fish in coral reef ecosystems exhibit complex group behavior patterns.",
        "task_id": "4ae961828fc94c07b2103dc039a8466b",
        "audio": "task/4ae961828fc94c07b2103dc039a8466b.mp3"
      }
    ],
    "created_at": "2025-09-21T07:29:41.058506Z",
    "updated_at": "2025-09-21T07:29:41.057917Z",
    "languages": [
      "zh"
    ],
    "visibility": "public",
    "lock_visibility": false,
    "default_text": "Through long-term observation, it was found that fish in coral reef ecosystems exhibit complex group behavior patterns.",
    "like_count": 0,
    "mark_count": 0,
    "shared_count": 0,
    "task_count": 0,
    "unliked": false,
    "liked": false,
    "marked": false,
    "author": {
      "_id": "7ecad23df62a4174acd6a2a6cb5201ee",
      "nickname": "Matthew Garcia",
      "avatar": "avatars/7ecad23df62a4174acd6a2a6cb5201ee.jpg"
    }
  }
}
```

The returned result contains multiple fields:

- `success`: The status of the current voice creation task.
- `data`: The result of the voice creation task.
  - `_id`: The ID of the created voice model, used for subsequent voice cloning with this ID.
  - `title`: The title of the voice model.
  - `cover_image`: The cover image information for the voice model.
  - `description`: The description of the voice model.
  - `train_mode`: The mode used for the voice training task.
  - `tags`: The style tags for the voice model.
  - `default_text`: The default sample text for the voice model.

Once you have the voice model `_id`, you can use it as the `voice_id` parameter in the Fish Audios Generation API to clone speech.

The corresponding CURL code example is as follows:

```shell
curl -X POST 'https://api.acedata.cloud/fish/voices' \
-H 'accept: application/json' \
-H 'authorization: Bearer {token}' \
-H 'content-type: application/json' \
-d '{
  "voice_url": "https://platform.r2.fish.audio/task/604133d7b3c7430385382470f67770e8.mp3",
  "title": "test",
  "description": "test"
}'
```

## Asynchronous Callback

Because Fish Voices Generation API generation can take relatively long (approximately 1–2 minutes), keeping an HTTP connection open throughout would consume extra system resources. This API supports asynchronous callbacks.

The flow is: the client includes an extra `callback_url` field in the request. After the client submits the API request, the API immediately returns a result containing a `task_id` field representing the current task ID. When the task is complete, the generation result is sent via POST JSON to the `callback_url` specified by the client, along with the `task_id` field, so the result can be correlated with the original task.

First, a webhook callback must be an HTTP service capable of receiving requests. Developers should replace the URL with their own HTTP server URL. For demonstration purposes, you can use the public webhook sample site https://webhook.site/ to get a webhook URL, as shown below:

![](https://cdn.acedata.cloud/tbcnai.png)

Copy this URL to use as a webhook. The sample URL is `https://webhook.site/4815f79f-a40f-4078-ac85-1cc126b6bb34`.

Next, set the `callback_url` field to the webhook URL above and fill in the other parameters, as shown below:

<p><img src="https://cdn.acedata.cloud/ecbq1s.png" width="500" class="m-auto"></p>

After clicking run, an immediate result is returned:

```json
{
  "task_id": "9f626a13-96ec-4dec-8846-dc5aab7362a8"
}
```

After a short wait, the generation result will appear at `https://webhook.site/4815f79f-a40f-4078-ac85-1cc126b6bb34`, as shown below:

![](https://cdn.acedata.cloud/dxlupe.png)

The content is as follows:

```json
{
  "success": true,
  "task_id": "9f626a13-96ec-4dec-8846-dc5aab7362a8",
  "trace_id": "3fcdea82-7c1c-4a0a-b8d8-f7616f722d8f",
  "data": {
    "_id": "fa75e7c3f02f42e79a6aa622b6cf075e",
    "type": "tts",
    "title": "test",
    "description": "test",
    "cover_image": "coverimage/fa75e7c3f02f42e79a6aa622b6cf075e",
    "train_mode": "fast",
    "state": "trained",
    "tags": [],
    "samples": [
      {
        "title": "Default Sample",
        "text": "Dolphins navigate the ocean using echolocation, a precise acoustic technology that allows them to detect their surroundings, find food, and avoid danger.",
        "task_id": "68cdda24d26e4794bae177e20da740db",
        "audio": "task/68cdda24d26e4794bae177e20da740db.mp3"
      }
    ],
    "created_at": "2025-09-21T07:36:20.200865Z",
    "updated_at": "2025-09-21T07:36:20.200353Z",
    "languages": [
      "zh"
    ],
    "visibility": "public",
    "lock_visibility": false,
    "default_text": "Dolphins navigate the ocean using echolocation, a precise acoustic technology that allows them to detect their surroundings, find food, and avoid danger.",
    "like_count": 0,
    "mark_count": 0,
    "shared_count": 0,
    "task_count": 0,
    "unliked": false,
    "liked": false,
    "marked": false,
    "author": {
      "_id": "7ecad23df62a4174acd6a2a6cb5201ee",
      "nickname": "Matthew Garcia",
      "avatar": "avatars/7ecad23df62a4174acd6a2a6cb5201ee.jpg"
    }
  }
}
```

The result contains a `task_id` field; the other fields are the same as described above. Use this field to correlate task results.

## Error Handling

When calling the API, if an error is encountered, the API will return the corresponding error code and message. For example:

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

Through this document, you have learned how to use the Fish Voices Generation API to create your own voice model by providing an audio URL. We hope this document helps you integrate and use the API more effectively. If you have any questions, please contact our technical support team.
