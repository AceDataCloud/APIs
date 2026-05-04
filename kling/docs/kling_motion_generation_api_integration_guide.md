# Kling Motion Generation API Integration Instructions

This article will introduce the Kling Motion Generation API integration instructions, which can generate official Kling AI videos by inputting custom parameters for motion transfer.

## Application Process

To use the API, you need to first apply for the corresponding service on the [Kling Motion Generation API](https://platform.acedata.cloud/documents/d3f2c369-102d-4856-9565-702ac5f2df63) page. After entering the page, click the "Acquire" button, as shown in the image:

![](https://cdn.acedata.cloud/q6ytrc.png)

If you are not logged in or registered, you will be automatically redirected to the login page inviting you to register and log in. After logging in or registering, you will be automatically returned to the current page.

There will be a free quota offered for the first application, allowing you to use the API for free.

## Basic Usage

First, understand the basic usage method, which involves inputting the prompt `prompt`, the reference image `image_url`, and the reference video link `video_url` to obtain the processed result. We also need to input the mode `mode`, which currently mainly includes standard mode `std` and fast mode `pro`. The specific content is as follows:

<p><img src="https://cdn.acedata.cloud/5qlpjt.png" width="500" class="m-auto"></p>

Here we can see that we have set the Request Headers, including:

- `accept`: the format of the response result you want to receive, filled in as `application/json`, which means JSON format.
- `authorization`: the key to call the API, which can be directly selected after application.

Additionally, we set the Request Body, including:

- `image_url`: the reference image. The characters, background, and other elements in the generated video are based on this reference image.
- `video_url`: the link to obtain the reference video. The character movements in the generated video will match the reference video.
- `mode`: the mode for generating the video, mainly standard mode `std` and fast mode `pro`.
- `keep_original_sound`: optional, whether to keep the original sound of the video, enumeration values: `yes`, `no`.
- `character_orientation`: the orientation of the character in the generated video, can be aligned with the image or the video, enumeration values: `image`, `video`.
- `prompt`: prompt words.
- `callback_url`: the URL to which the results need to be returned.

After selection, you can see that the corresponding code is also generated on the right side, as shown in the image:

<p><img src="https://cdn.acedata.cloud/buwczd.png" width="500" class="m-auto"></p>

Click the "Try" button to test, as shown in the image above, and we obtained the following result:

```json
{
  "success": true,
  "video_id": "842578800134742051",
  "video_url": "https://v4-fdl.kechuangai.com/ksc2/yGPGHvUVDQEzDCs6tC0rYIbd_JwWNFaF8BEYAlw_xVcWX72xFuIUVqB_Hp5Sa7YEijI-yXqfKI92WW7bmyeCtpMjSOImlOFpQCmMUa-9iojt_ifXJnex_tvNkA0ZlJmuJLpeOfvX3j8d9oeeWgLeU3ftzBjQq1g9OC9FU92OfjRQLUTSzfWRzkhzirV32BT-BwfxgqJKsUD-WHxjqCJmOw.mp4",
  "duration": "5.066",
  "state": "succeed",
  "task_id": "363c7a84-e880-472e-a4d4-098e50cfc292"
}
```

The returned result contains multiple fields, described as follows:

- `success`: the status of the video generation task at this time.
- `task_id`: the ID of the video generation task at this time.
- `video_id`: the video ID of the video generation task.
- `video_url`: the video link of the video generation task.
- `duration`: the video duration of the video generation task.
- `state`: the state of the video generation task.

We can see that we have obtained satisfactory video information, and we only need to obtain the generated Kling video based on the video link address in `video_url`.

Additionally, if you want to generate the corresponding integration code, you can directly copy it, for example, the CURL code is as follows:

```shell
curl -X POST 'https://api.acedata.cloud/kling/motion' \
-H 'accept: application/json' \
-H 'authorization: Bearer {token}' \
-H 'content-type: application/json' \
-d '{
  "image_url": "https://sourceyoya.wenge.com/2025/06/03/683e9f76e4b0684509ab1aca.jpg",
  "video_url": "https://cdn.acedata.cloud/odwfm5.mp4",
  "prompt": "Make the scene come alive",
  "mode": "std",
  "character_orientation": "image"
}'
```

## Asynchronous Callback

Since the time taken by the Kling Motion Generation API is relatively long, approximately 1-2 minutes, if the API does not respond for a long time, the HTTP request will keep the connection open, leading to additional system resource consumption. Therefore, this API also provides support for asynchronous callbacks.

The overall process is: when the client initiates a request, an additional `callback_url` field is specified. After the client initiates the API request, the API will immediately return a result containing a `task_id` field information, representing the current task ID. When the task is completed, the generated video result will be sent to the client-specified `callback_url` in the form of a POST JSON, which also includes the `task_id` field, allowing the task result to be associated by ID.

Let's understand how to operate specifically through an example.

First, the Webhook callback is a service that can receive HTTP requests, and developers should replace it with the URL of their own built HTTP server. For demonstration purposes, a public Webhook sample site https://webhook.site/ is used, and opening this site will provide a Webhook URL, as shown in the image:

![](https://cdn.acedata.cloud/tbcnai.png)

Copy this URL, and it can be used as a Webhook. The sample here is `https://webhook.site/624b2c78-6dbd-4618-9d2b-b32eade6d8c3`.

Next, we can set the `callback_url` field to the above Webhook URL, while filling in the corresponding parameters, as shown in the image:

<p><img src="https://cdn.acedata.cloud/vdx12s.png" width="500" class="m-auto"></p>

Clicking run, you can find that an immediate result is obtained, as follows:

```
{
  "task_id": "20068983-0cc9-4c6a-aeb6-9c6a3c668be0"
}
```

After a moment, we can observe the generated video result at `https://webhook.site/624b2c78-6dbd-4618-9d2b-b32eade6d8c3`, as shown in the image:

![](https://cdn.acedata.cloud/zv5u2q.png)

The content is as follows:

```json
{
    "success": true,
    "video_id": "030bb06d-98d4-4044-9042-0aa0822e8c8c",
    "video_url": "https://cdn.klingai.com/bs2/upload-kling-api/7822108635/text2video/CjJzzGfBfqcAAAAAAKdVMQ-0_raw_video_1.mp4",
    "duration": "5.1",
    "state": "succeed",
    "task_id": "20068983-0cc9-4c6a-aeb6-9c6a3c668be0"
}
```

It can be seen that the result contains a `task_id` field, and the other fields are similar to the above text, allowing the task to be associated through this field.

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

Through this document, you have learned how to use the Kling Motion Generation API to generate videos with motion transfer from Kling AI. We hope this document can help you better integrate and use this API. If you have any questions, please feel free to contact our technical support team.
