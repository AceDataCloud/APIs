# Kling Videos Generation API Integration Guide

This article introduces the Kling Videos Generation API integration instructions. By inputting custom parameters, you can generate official Kling AI videos.

## Application Process

To use the API, you need to first apply for the corresponding service on the [Kling Videos Generation API](https://platform.acedata.cloud/documents/3b921a16-a411-4557-8335-53f21d3f9e46) page. After entering the page, click the "Acquire" button, as shown in the image:

![](https://cdn.acedata.cloud/q6ytrc.png)

If you are not logged in or registered, you will be automatically redirected to the login page inviting you to register and log in. After logging in or registering, you will be automatically returned to the current page.

There will be a free quota offered for the first application, allowing you to use the API for free.

## Basic Usage

First, understand the basic usage method: input the prompt `prompt`, the generation action `action`, an optional first-frame reference image `start_image_url`, and the model `model` to obtain the processed result. You first need to pass the `action` field, whose value is `text2video`. The API supports three main actions: text-to-video (`text2video`), image-to-video (`image2video`), and video extension (`extend`). You also need to specify the model `model`. The currently supported models are `kling-v1`, `kling-v1-6`, `kling-v2-master`, `kling-v2-1-master`, `kling-v2-5-turbo`, `kling-v2-6`, `kling-v3`, `kling-v3-omni`, and `kling-video-o1`. The specific content is as follows:

<p><img src="https://cdn.acedata.cloud/ke1bok.png" width="500" class="m-auto"></p>

Here we have set the Request Headers, including:

- `accept`: the format of the response result you want to receive, filled in as `application/json`, which means JSON format.
- `authorization`: the key to call the API, which can be directly selected from the dropdown after application.

Additionally, we set the Request Body, including:

- `model`: the model used to generate the video. Supported models: `kling-v1`, `kling-v1-6`, `kling-v2-master`, `kling-v2-1-master`, `kling-v2-5-turbo`, `kling-v2-6`, `kling-v3`, `kling-v3-omni`, `kling-video-o1`.
- `mode`: the mode for generating the video. Options: standard mode `std`, high-quality mode `pro`, and native 4K mode `4k`. The `4k` mode is only supported by `kling-v3` and `kling-v3-omni`, and is not compatible with `camera_control` (motion control).
- `action`: the action for this video generation task. Options: text-to-video (`text2video`), image-to-video (`image2video`), and video extension (`extend`).
- `start_image_url`: when the `image2video` action is selected, you must provide a first-frame reference image URL.
- `end_image_url`: optional for image-to-video, specifies the last frame. Only valid with `action=image2video` and a non-empty `start_image_url`.
- `duration`: video duration in seconds. For `kling-v3` and `kling-v3-omni` models, supports flexible duration of 3–15 seconds (integer). For other models, supports 5 or 10 seconds.
- `generate_audio`: whether to generate audio along with the video, optional boolean. Supported only by `kling-v3`, `kling-v3-omni`, and `kling-v2-6` (pro mode only). Default is `false`.
- `aspect_ratio`: the aspect ratio of the video, optional. Options: `16:9`, `9:16`, `1:1`. Default is `16:9`.
- `cfg_scale`: degree of correlation strength, range [0, 1]. A higher value means the output follows the prompt more closely.
- `camera_control`: optional object for controlling camera movement. Supports type/simple presets and configuration fields: `horizontal`, `vertical`, `pan`, `tilt`, `roll`, `zoom`.
- `negative_prompt`: optional, content you do not want to appear in the video. Maximum 200 characters.
- `element_list`: list of reference subjects. Only applicable to the `kling-video-o1` model. For usage details, refer to the [official documentation](https://docs.qingque.cn/d/home/eZQAyImcbaS0fz-8ANjXvU5ed?identityId=1oEG9JKKMFv#section=h.5t7wme23nn6z).
- `video_list`: reference video, obtained via URL. Only applicable to the `kling-video-o1` model. For usage details, refer to the [official documentation](https://docs.qingque.cn/d/home/eZQAyImcbaS0fz-8ANjXvU5ed?identityId=1oEG9JKKMFv#section=h.5t7wme23nn6z).
- `prompt`: the text prompt for video generation.
- `callback_url`: the URL to which the result will be sent upon completion.

After setting the parameters, you can see that the corresponding code has been generated on the right side, as shown in the image:

<p><img src="https://cdn.acedata.cloud/3yjql0.png" width="500" class="m-auto"></p>

Click the "Try" button to test. Here we obtained the following result:

```json
{
  "success": true,
  "video_id": "af9a1af0-9aa0-4638-81c1-d41d6143c508",
  "video_url": "https://cdn.klingai.com/bs2/upload-kling-api/7485378259/text2video/Cjil4mfBfs0AAAAAAKbMQQ-0_raw_video_1.mp4",
  "duration": "5.1",
  "state": "succeed",
  "task_id": "e3a575aa-a4bd-49c8-9b12-cde38d5462e0"
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
curl -X POST 'https://api.acedata.cloud/kling/videos' \
-H 'accept: application/json' \
-H 'authorization: Bearer {token}' \
-H 'content-type: application/json' \
-d '{
  "action": "text2video",
  "model": "kling-v1",
  "prompt": "White ceramic coffee mug on glossy marble countertop with morning window light. Camera slowly rotates 360 degrees around the mug, pausing briefly at the handle."
}'
```

## Model Capability Matrix

Different models support different parameters. The following matrix is compiled from the [Kling official video models documentation](https://app.klingai.com/global/dev/document-api/apiReference/model/videoModels). Before making a request, verify that your chosen `model` / `mode` / `duration` combination supports the features you need — otherwise the upstream service will return errors such as `model/mode/duration(...) is not supported with image_tail`.

| Model | Mode | `end_image_url` (start/end frame) | `generate_audio` (audio) | `camera_control` (camera movement) | Notes |
|---|---|---|---|---|---|
| `kling-v1` | std / pro | ✅ `duration=5` only | ❌ | ✅ `duration=5` only | `extend` does not support `negative_prompt` or `cfg_scale` |
| `kling-v1-6` | std | ❌ | ❌ | ❌ | Multi-image-to-video; `extend` available in all modes |
| `kling-v1-6` | pro | ✅ | ❌ | ❌ | |
| `kling-v2-master` | — | ❌ | ❌ | ❌ | Single mode; `duration=5/10` only |
| `kling-v2-1-master` | — | ❌ | ❌ | ❌ | Single mode; `duration=5/10` only |
| `kling-v2-5-turbo` | std | ❌ | ❌ | ❌ | |
| `kling-v2-5-turbo` | pro | ✅ | ❌ | ❌ | |
| `kling-v2-6` | std | ❌ | ❌ | ❌ | |
| `kling-v2-6` | pro | ✅ | ✅ | ❌ | Only non-v3 model supporting audio generation |
| `kling-v3` | std / pro | ✅ | ✅ | ✅ | `duration` range: 3–15 seconds |
| `kling-v3` | 4k | ✅ | ✅ | ❌ | 4K mode is incompatible with motion control |
| `kling-v3-omni` | std / pro / 4k | ✅ | ✅ | ❌ | |
| `kling-video-o1` | std / pro | ✅ | ❌ | ❌ | `duration=5/10` only |

Notes:

- `mode=4k` is only supported by `kling-v3` and `kling-v3-omni`, and is mutually exclusive with `camera_control` (motion control).
- `end_image_url` can only be used with `action=image2video` together with `start_image_url`. Providing only `end_image_url` (without `start_image_url`) will be rejected.
- `kling-v3` / `kling-v3-omni` accept any integer `duration` between 3–15 seconds; all other models only accept 5 or 10.
- `generate_audio` defaults to `false`. Only `kling-v3`, `kling-v3-omni`, and `kling-v2-6` (pro mode) support it.

## Video Extension

To extend an already generated Kling video, set the `action` parameter to `extend` and provide the `video_id` of the video you want to continue. The video ID is obtained from the basic usage response, as shown below:

<p><img src="https://cdn.acedata.cloud/om6p6g.png" width="500" class="m-auto"></p>

The video ID is:

```
"video_id": "030bb06d-98d4-4044-9042-0aa0822e8c8c"
```

> Note: The `video_id` here is the ID of a previously generated video. If you are unsure how to generate a video, refer to the Basic Usage section above.

Next, provide the required parameters for the extension:

- `model`: the model for generating the video. Supported models: `kling-v1`, `kling-v1-5`, and `kling-v1-6`.
- `mode`: the mode for video generation. Options: standard mode `std`, high-quality mode `pro`, and native 4K mode `4k` (`kling-v3` and `kling-v3-omni` only; incompatible with motion control).
- `duration`: the duration of this video generation task, supports 5s and 10s.
- `start_image_url`: when the `image2video` action is selected, the first-frame reference image URL is required.
- `prompt`: the text prompt.

An example is shown below:

<p><img src="https://cdn.acedata.cloud/ejimqy.png" width="500" class="m-auto"></p>

The corresponding Python code:

```python
import requests

url = "https://api.acedata.cloud/kling/videos"

headers = {
    "accept": "application/json",
    "authorization": "Bearer {token}",
    "content-type": "application/json"
}

payload = {
    "action": "extend",
    "model": "kling-v1",
    "video_id": "030bb06d-98d4-4044-9042-0aa0822e8c8c",
    "prompt": "White ceramic coffee mug on glossy marble countertop with morning window light. Camera slowly rotates 360 degrees around the mug, pausing briefly at the handle.",
    "duration": 10
}

response = requests.post(url, json=payload, headers=headers)
print(response.text)
```

After running, you will get the following result:

```json
{
  "success": true,
  "video_id": "bbc3b105-ac72-4de2-8390-0cb37dc7d41e",
  "video_url": "https://cdn.klingai.com/bs2/upload-kling-api/7822108635/extendVideo/Cjil4mfBfs0AAAAAAKhr6A-0_raw_video_1.mp4",
  "duration": "9.6",
  "state": "succeed",
  "task_id": "3ece87e6-3ee3-4f5e-bd70-5ae5eca89a23"
}
```

The result is consistent with what is described in the Basic Usage section, achieving the video extension functionality.

## Asynchronous Callback

Since the Kling Videos Generation API takes a relatively long time (approximately 1–2 minutes), keeping the HTTP connection open for the full duration may cause unnecessary resource consumption. Therefore, the API also supports asynchronous callbacks.

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

Through this document, you have learned how to use the Kling Videos Generation API to generate videos by inputting a text prompt and optional reference images. We hope this document helps you integrate and use the API more effectively. If you have any questions, please feel free to contact our technical support team.
