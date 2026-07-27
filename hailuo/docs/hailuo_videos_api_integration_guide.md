# Hailuo Videos Generation API Integration Instructions

This article introduces the Hailuo Videos Generation API integration guide, which allows you to generate official Hailuo videos by inputting custom parameters.

## Application Process

To use the API, you first need to apply for the corresponding service on the [Hailuo Videos Generation API](https://platform.acedata.cloud/documents/ee06377b-9185-438f-ac84-3376bcb1275e) page. After entering the page, click the "Acquire" button, as shown in the image below:

![](https://cdn.acedata.cloud/q6ytrc.png)

If you are not logged in or registered, you will be automatically redirected to the login page inviting you to register and log in. After logging in or registering, you will automatically return to the current page.

Upon your first application, there will be a free quota available for you to use the API for free.

## Basic Usage

First, understand the basic usage method, which involves inputting the prompt `prompt`, the generation action `action`, the first frame reference image `first_image_url`, and the model `model` to obtain the processed result. You first need to simply pass a field `action` with the value `generate`, and then input the model. Currently, the main models are the image-to-video model `minimax-i2v` and the text-to-video model `minimax-t2v`, as detailed below:

<p><img src="https://cdn.acedata.cloud/7jyu0n.png" width="500" class="m-auto"></p>

Here, we can see that we have set the Request Headers, including:

- `accept`: the format of the response you want to receive, filled in as `application/json`, which means JSON format.
- `authorization`: the key to call the API, which can be selected directly after application.

Additionally, the Request Body is set, including:

- `model`: the model for generating the video, mainly the image-to-video model `minimax-i2v` and the text-to-video model `minimax-t2v`.
- `action`: the action for this video generation task.
- `first_image_url`: the first frame reference image link that must be uploaded when using the image-to-video model `minimax-i2v`. Base64 encoding is not supported.
- `prompt`: the prompt.
- `callback_url`: the URL for callback results.

After selection, you can see that the corresponding code is generated on the right side, as shown in the image below:

<p><img src="https://cdn.acedata.cloud/8psuxw.png" width="500" class="m-auto"></p>

Click the "Try" button to test, as shown in the image above, and we get the following result:

```json
{
  "success": true,
  "task_id": "baf1034c-684c-46be-ae6d-89ebb89b690d",
  "trace_id": "3221eb74-1a25-447a-ba69-7d9b310e306c",
  "data": [
    {
      "id": "0pv8yhe4fdrge0cmckpv23pd2g",
      "model": "minimax-t2v",
      "prompt": "Internal heat",
      "video_url": "https://platform.cdn.acedata.cloud/czjl/qoueLWBokF3ud6tdVD6VJTZuXTnK5HaMO2qAOS46Ef8VSBFUA/tmp9e3u11c1.output.mp4",
      "state": "succeeded"
    }
  ]
}
```

The returned result contains multiple fields, described as follows:

- `success`: the status of the current video generation task.
- `task_id`: the ID of the current video generation task.
- `trace_id`: the trace ID of the current video generation task.
- `data`: the result list of the current video generation task.
  - `id`: the video ID of the current video generation task.
  - `prompt`: the prompt of the current video generation task.
  - `model`: the model of the current video generation task.
  - `video_url`: the video link of the current video generation task.
  - `state`: the status of the current video generation task.

We can see that we have obtained satisfactory video information. We only need to obtain the generated Hailuo video using the video link address from `data`.

Additionally, if you want to generate the corresponding integration code, you can directly copy the generated code. For example, the CURL code is as follows:

```shell
curl -X POST 'https://api.acedata.cloud/hailuo/videos' \
-H 'accept: application/json' \
-H 'authorization: Bearer {token}' \
-H 'content-type: application/json' \
-d '{
  "action": "generate",
  "prompt": "Internal heat"
}'
```

## Asynchronous Callback

Since the generation time of the Hailuo Videos Generation API is relatively long, approximately 1-2 minutes, if the API does not respond for a long time, the HTTP request will keep the connection open, leading to additional system resource consumption. Therefore, this API also provides support for asynchronous callbacks.

The overall process is: when the client initiates a request, an additional `callback_url` field is specified. After the client initiates the API request, the API will immediately return a result containing a `task_id` field, representing the current task ID. When the task is completed, the generated video result will be sent to the client-specified `callback_url` in the form of a POST JSON, which also includes the `task_id` field, allowing the task result to be associated by ID.

Let's understand how to operate specifically through an example.

First, the Webhook callback is a service that can receive HTTP requests, and developers should replace it with the URL of their own HTTP server. For demonstration purposes, a public Webhook sample site https://webhook.site/ is used, and opening this site will provide a Webhook URL, as shown in the image:

![](https://cdn.acedata.cloud/cjjfly.png)

Copy this URL, and it can be used as a Webhook. The sample here is `https://webhook.site/580b81f5-596e-4321-b03f-606770b0bb83`.

Next, we can set the `callback_url` field to the above Webhook URL and fill in the corresponding parameters, as shown in the image:

<p><img src="https://cdn.acedata.cloud/odabh3.png" width="500" class="m-auto"></p>

Clicking run, we can find that an immediate result is obtained, as follows:

```
{
  "task_id": "05aff65c-5e84-442b-8e29-3a5d27130840"
}
```

After a moment, we can observe the generated video result at `https://webhook.site/580b81f5-596e-4321-b03f-606770b0bb83`, as shown in the image:

![](https://cdn.acedata.cloud/7jngb4.png)

The content is as follows:

```json
{
    "success": true,
    "task_id": "05aff65c-5e84-442b-8e29-3a5d27130840",
    "trace_id": "b9856b8a-725d-45c9-befe-e789d9fd9ffb",
    "data": [
        {
            "id": "t80jhsf96srg80cmcm6b0rk8gm",
            "model": "minimax-t2v",
            "prompt": "Internal heat",
            "video_url": "https://platform.cdn.acedata.cloud/czjl/YPaUz2DcwpJqItTXAG9XHAoEoj3dbF0XPU69LT5nefCMzBFUA/tmp8s_59jez.output.mp4",
            "state": "succeeded"
        }
    ]
}
```

As you can see, the result contains a `task_id` field, and the other fields are similar to the above text, allowing the task to be associated through this field.

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

Through this document, you have learned how to use the Hailuo Videos Generation API to generate videos by inputting prompt words and a first frame reference image. We hope this document helps you better integrate and use this API. If you have any questions, please feel free to contact our technical support team.
