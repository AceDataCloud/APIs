# Fish Voices Generation API Integration Instructions

This article will introduce the integration instructions for the Fish Voices Generation API, which allows you to create your own voice by inputting an audio link.

## Application Process

To use Fish Voices Generation API, first open the [Ace Data Cloud Console](https://platform.acedata.cloud/console/applications) and copy your API Token.

![](https://cdn.acedata.cloud/5hmkdg.jpg)

If you are not logged in, you will be redirected to sign in and brought back to this page automatically.

**A single API Token works across every service on the platform — no need to subscribe per service.** New accounts receive free starter credit; when it runs low you can top up your shared balance in the [console](https://platform.acedata.cloud/console/coin).

> 📘 Full documentation: [Fish Voices Generation API →](https://platform.acedata.cloud/documents/fish-voices)

## Basic Usage

The basic usage involves inputting the audio link of the voice `voice_url` to obtain the processed result.

The Request Headers include:

- `accept`: the format of the response you want to receive, filled in as `application/json`, which means JSON format.
- `authorization`: the key to call the API, which can be selected directly after application.

The Request Body includes:

- `voice_url`: the uploaded audio link of the voice.
- `title`: the title information of the voice.
- `image_urls`: the cover image of the voice.
- `description`: the description information of the voice.
- `callback_url`: the URL to receive the callback result.

### Code Example

```shell
curl -X POST 'https://api.acedata.cloud/fish/voices' \
-H 'accept: application/json' \
-H 'authorization: ******' \
-H 'content-type: application/json' \
-d '{
  "voice_url": "https://platform.r2.fish.audio/task/604133d7b3c7430385382470f67770e8.mp3",
  "title": "test",
  "description": "test"
}'
```

### Response Example

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
        "text": "Through long-term observation, it has been found that fish in coral reef ecosystems exhibit complex group behavior patterns.",
        "task_id": "4ae961828fc94c07b2103dc039a8466b",
        "audio": "task/4ae961828fc94c07b2103dc039a8466b.mp3"
      }
    ],
    "created_at": "2025-09-21T07:29:41.058506Z",
    "updated_at": "2025-09-21T07:29:41.057917Z",
    "languages": ["zh"],
    "visibility": "public",
    "lock_visibility": false,
    "like_count": 0,
    "mark_count": 0,
    "shared_count": 0,
    "task_count": 0,
    "author": {
      "_id": "7ecad23df62a4174acd6a2a6cb5201ee",
      "nickname": "Matthew Garcia",
      "avatar": "avatars/7ecad23df62a4174acd6a2a6cb5201ee.jpg"
    }
  }
}
```

The returned result contains multiple fields, described as follows:

- `success`: the status of the voice creation task at this time.
- `data`: the result of the music task
  - `_id`: the ID of the voice generation task at this time, which will be used for cloning the voice in the future.
  - `title`: the title of the voice.
  - `description`: the description information of the voice.
  - `train_mode`: the mode used for the voice generation task at this time.
  - `tags`: the style of the voice.
  - `default_text`: the voice text information of the voice generation task at this time.

The `data._id` can be used as the `reference_id` in the Fish TTS API to perform speech synthesis using the cloned voice.

## Asynchronous Callback

Since the time taken by the Fish Voices Generation API to generate is relatively long, approximately 1-2 minutes, if the API does not respond for a long time, the HTTP request will keep the connection open, leading to additional system resource consumption. Therefore, this API also provides support for asynchronous callbacks.

The overall process is: when the client initiates a request, an additional `callback_url` field is specified. After the client initiates the API request, the API will immediately return a result containing a `task_id` field, representing the current task ID. When the task is completed, the result of the generation task will be sent to the client-specified `callback_url` in the form of a POST JSON, which also includes the `task_id` field, allowing the task result to be associated by ID.

Example with callback URL:

```shell
curl -X POST 'https://api.acedata.cloud/fish/voices' \
-H 'accept: application/json' \
-H 'authorization: ******' \
-H 'content-type: application/json' \
-d '{
  "voice_url": "https://platform.r2.fish.audio/task/604133d7b3c7430385382470f67770e8.mp3",
  "title": "test",
  "description": "test",
  "callback_url": "https://webhook.site/4815f79f-a40f-4078-ac85-1cc126b6bb34"
}'
```

Immediate response:

```json
{
  "task_id": "9f626a13-96ec-4dec-8846-dc5aab7362a8"
}
```

After a moment, the callback URL will receive the completed result with a `task_id` field for association.

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

Through this document, you have learned how to use the Fish Voices Generation API to create your own voice by connecting to the audio of the input tone. We hope this document helps you better integrate and use the API. If you have any questions, please feel free to contact our technical support team.

## Support

If you meet any issue, please check [support info](https://platform.acedata.cloud/support) or browse the latest documentation on [docs.acedata.cloud](https://docs.acedata.cloud)
