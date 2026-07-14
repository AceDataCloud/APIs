# Kling Motion Generation API Integration Guide

This article introduces the Kling Motion Generation API integration instructions. By inputting custom parameters, you can generate official Kling AI videos with character motion driven by a reference image and reference video.

## Application Process

To use Kling Motion Generation API, first open the [Ace Data Cloud Console](https://platform.acedata.cloud/console/applications) and copy your API Token.

![](https://cdn.acedata.cloud/5hmkdg.jpg)

If you are not logged in, you will be redirected to sign in and brought back to this page automatically.

**A single API Token works across every service on the platform — no need to subscribe per service.** New accounts receive free starter credit; when it runs low you can top up your shared balance in the [console](https://platform.acedata.cloud/console/coin).

> 📘 Full documentation: [Kling Motion Generation API →](https://platform.acedata.cloud/documents/kling-motion)

## Basic Usage

First, understand the basic usage method: input the prompt `prompt`, a reference image `image_url`, and a reference video `video_url` to obtain the processed result. You also need to specify the mode `mode`, which currently supports `std` (standard) and `pro` (high quality). The specific content is as follows:

<p><img src="https://cdn.acedata.cloud/5qlpjt.png" width="500" class="m-auto"></p>

Here we have set the Request Headers, including:

- `accept`: the format of the response result you want to receive, filled in as `application/json`, which means JSON format.
- `authorization`: the key to call the API, which can be directly selected from the dropdown after application.

Additionally, we set the Request Body, including:

- `image_url`: reference image. The characters, backgrounds, and other elements in the generated video are based on this reference image.
- `video_url`: reference video URL. The character movements in the generated video are consistent with those in the reference video.
- `mode`: the mode for generating the video. Options: standard mode `std` and high-quality mode `pro`.
- `keep_original_sound`: optional, whether to keep the original sound of the video. Options: `yes` (keep) or `no` (remove).
- `character_orientation`: the orientation of the characters in the generated video. Options: consistent with the image (`image`) or consistent with the video (`video`).
- `prompt`: the text prompt for video generation.
- `callback_url`: the URL to which the result will be sent upon completion.

After setting the parameters, you can see that the corresponding code has been generated on the right side, as shown in the image:

<p><img src="https://cdn.acedata.cloud/buwczd.png" width="500" class="m-auto"></p>

Click the "Try" button to test. Here we obtained the following result:

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

- `success`: the status of the video generation task.
- `task_id`: the ID of the video generation task.
- `video_id`: the video ID of the video generation task.
- `video_url`: the video link of the generated video.
- `duration`: the duration of the generated video.
- `state`: the current state of the video generation task.

We can see that we have obtained the satisfactory video information. You only need to retrieve the generated Kling video using the `video_url` in the result.

Additionally, to generate the corresponding integration code, you can directly copy it. For example, the CURL code is as follows:

```shell
curl -X POST 'https://api.acedata.cloud/kling/motion' \
-H 'accept: application/json' \
-H 'authorization: Bearer {token}' \
-H 'content-type: application/json' \
-d '{
  "image_url": "https://sourceyoya.wenge.com/2025/06/03/683e9f76e4b0684509ab1aca.jpg",
  "video_url": "https://cdn.acedata.cloud/odwfm5.mp4",
  "prompt": "Make the picture come alive",
  "mode": "std",
  "character_orientation": "image"
}'
```

## Asynchronous Callback

Since the Kling Motion Generation API takes a relatively long time (approximately 1–2 minutes), keeping the HTTP connection open for the full duration may cause unnecessary resource consumption. Therefore, the API also supports asynchronous callbacks.

The overall flow is: the client specifies an additional `callback_url` field when making the request. The API immediately returns a result containing a `task_id` field representing the current task ID. When the task completes, the generated video result is sent via POST JSON to the specified `callback_url`, also including the `task_id` field, so the task result can be associated by ID.

Below is an example of how to use this feature.

First, a Webhook callback is an HTTP service that can receive requests. Developers should replace it with the URL of their own HTTP server. For demonstration purposes, we use the public Webhook sample site https://webhook.site/. Opening this site gives you a Webhook URL, as shown:

![](https://cdn.acedata.cloud/tbcnai.png)

Copy this URL to use as the Webhook. The sample URL here is `https://webhook.site/624b2c78-6dbd-4618-9d2b-b32eade6d8c3`.

Next, set the `callback_url` field to the above Webhook URL and fill in the corresponding parameters, as shown:

<p><img src="https://cdn.acedata.cloud/vdx12s.png" width="500" class="m-auto"></p>

After running, you will immediately get a result like:

```json
{
  "task_id": "20068983-0cc9-4c6a-aeb6-9c6a3c668be0"
}
```

After a short wait, you can observe the generated video result at `https://webhook.site/624b2c78-6dbd-4618-9d2b-b32eade6d8c3`, as shown:

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

The result includes a `task_id` field. All other fields are similar to those described above, and through this field, task results can be correlated by ID.

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

Through this document, you have learned how to use the Kling Motion Generation API to implement Kling AI's motion control functionality. We hope this document helps you integrate and use the API more effectively. If you have any questions, please feel free to contact our technical support team.
