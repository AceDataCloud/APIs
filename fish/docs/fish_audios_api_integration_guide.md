# Fish Audios Generation API Integration Guide

This article introduces the Fish Audios Generation API integration guide. This API allows you to clone a voice by providing a prompt and a voice ID.

## Application Process

To use the API, visit the [Fish Audios Generation API](https://platform.acedata.cloud/documents/e681b715-54fd-4464-a59a-d7f14500e095) page and click the "Acquire" button, as shown below:

![](https://cdn.acedata.cloud/q6ytrc.png)

If you are not logged in or registered, you will be automatically redirected to the login page. After logging in, you will automatically return to the current page.

Upon your first application, there will be a free quota provided, allowing you to use the API for free.

## Basic Usage

The basic usage involves providing a prompt `prompt`, a cloning action `action`, a voice ID `voice_id`, and a model `model` to obtain the processed result. You need to pass an `action` field with the value `generate`, specify the model — currently the main model is `fish-tts` — and set the other parameters as described below:

<p><img src="https://cdn.acedata.cloud/0jnfqb.png" width="500" class="m-auto"></p>

The Request Headers include:

- `accept`: The response format you want to receive, set to `application/json` for JSON format.
- `authorization`: The API key, which can be selected after application.

The Request Body includes:

- `model`: The voice cloning model, currently the main model is `fish-tts`.
- `action`: The action for this voice cloning task.
- `prompt`: The prompt text for the cloning.
- `voice_id`: Clone voice based on this voice ID.
- `callback_url`: The URL for the asynchronous callback result.

After configuration, the corresponding code is automatically generated on the right side, as shown below:

<p><img src="https://cdn.acedata.cloud/8uyos2.png" width="500" class="m-auto"></p>

Click the "Try" button to test. The result looks like this:

```json
{
  "success": true,
  "task_id": "5872ab00-3cf4-4040-a798-8510aaa16756",
  "trace_id": "5eda3694-448a-4b72-af33-2acb3851ffe1",
  "data": [
    {
      "audio_url": "https://platform.r2.fish.audio/task/8a72ff9840234006a9f74cb2fa04f978.mp3"
    }
  ]
}
```

The returned result contains multiple fields:

- `success`: The status of the current voice cloning task.
- `data`: The result of the voice cloning task.
  - `audio_url`: The audio URL of the cloned voice.

You can then use the `audio_url` from the `data` field to access the cloned voice audio.

The corresponding CURL code example is as follows:

```shell
curl -X POST 'https://api.acedata.cloud/fish/audios' \
-H 'accept: application/json' \
-H 'authorization: Bearer {token}' \
-H 'content-type: application/json' \
-d '{
  "action": "speech",
  "prompt": "a white siamese cat",
  "model": "fish-tts",
  "voice_id": "d7900c21663f485ab63ebdb7e5905036"
}'
```

## Asynchronous Callback

Because Fish Audios Generation API generation can take relatively long (approximately 1–2 minutes), keeping an HTTP connection open throughout would consume extra system resources. This API supports asynchronous callbacks.

The flow is: the client includes an extra `callback_url` field in the request. After the client submits the API request, the API immediately returns a result containing a `task_id` field representing the current task ID. When the task is complete, the generation result is sent via POST JSON to the `callback_url` specified by the client, along with the `task_id` field, so the result can be correlated with the original task.

First, a webhook callback must be an HTTP service capable of receiving requests. Developers should replace the URL with their own HTTP server URL. For demonstration purposes, you can use the public webhook sample site https://webhook.site/ to get a webhook URL, as shown below:

![](https://cdn.acedata.cloud/tbcnai.png)

Copy this URL to use as a webhook. The sample URL is `https://webhook.site/4815f79f-a40f-4078-ac85-1cc126b6bb34`.

Next, set the `callback_url` field to the webhook URL above and fill in the other parameters, as shown below:

<p><img src="https://cdn.acedata.cloud/8rv4te.png" width="500" class="m-auto"></p>

After clicking run, an immediate result is returned:

```json
{
  "task_id": "2725a2d3-f87e-4905-9c53-9988d5a7b2f5"
}
```

After a short wait, the generation result will appear at `https://webhook.site/4815f79f-a40f-4078-ac85-1cc126b6bb34`, as shown below:

![](https://cdn.acedata.cloud/9utzve.png)

The content is as follows:

```json
{
  "success": true,
  "task_id": "2725a2d3-f87e-4905-9c53-9988d5a7b2f5",
  "trace_id": "e2d308bc-4df8-4c69-9369-a60f3c54f2b3",
  "data": [
    {
      "audio_url": "https://platform.r2.fish.audio/task/b627c2f7d38a4083a837570ba6d0962f.mp3"
    }
  ]
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

Through this document, you have learned how to use the Fish Audios Generation API to clone a voice by providing a prompt. We hope this document helps you integrate and use the API more effectively. If you have any questions, please contact our technical support team.
