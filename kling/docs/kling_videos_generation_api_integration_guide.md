# Kling Videos Generation API Integration Instructions

This article will introduce the Kling Videos Generation API integration instructions, which can generate official Kling AI videos by inputting custom parameters.

## Application Process

To use the API, you need to first apply for the corresponding service on the [Kling Videos Generation API](https://platform.acedata.cloud/documents/3b921a16-a411-4557-8335-53f21d3f9e46) page. After entering the page, click the "Acquire" button, as shown in the image:

![](https://cdn.acedata.cloud/q6ytrc.png)

If you are not logged in or registered, you will be automatically redirected to the login page inviting you to register and log in. After logging in or registering, you will be automatically returned to the current page.

There will be a free quota offered for the first application, allowing you to use the API for free.

## Basic Usage

First, understand the basic usage method, which involves inputting the prompt `prompt`, the action `action`, the first frame reference image `start_image_url`, and the model `model` to obtain the processed result. You first need to simply pass a field `action`. It mainly includes three types of actions: text-to-video (`text2video`), image-to-video (`image2video`), and video extension (`extend`). Then, we also need to input the model `model`, which currently mainly includes `kling-v1`, `kling-v1-6`, `kling-v2-master`, `kling-v2-1-master`, `kling-v2-5-turbo`, `kling-v2-6`, `kling-v3`, `kling-v3-omni`, and `kling-video-o1`. The specific content is as follows:

<p><img src="https://cdn.acedata.cloud/ke1bok.png" width="500" class="m-auto"></p>

Here we can see that we have set the Request Headers, including:

- `accept`: the format of the response result you want to receive, filled in as `application/json`, which means JSON format.
- `authorization`: the key to call the API, which can be directly selected after application.

Additionally, we set the Request Body, including:

- `model`: the model for generating the video, mainly including `kling-v1`, `kling-v1-6`, `kling-v2-master`, `kling-v2-1-master`, `kling-v2-5-turbo`, `kling-v2-6`, `kling-v3`, `kling-v3-omni`, and `kling-video-o1`.
- `mode`: the mode for generating the video, optional values are standard mode `std`, fast mode `pro`, and native 4K mode `4k`. The `4k` mode is only supported by `kling-v3` and `kling-v3-omni`, and is incompatible with `camera_control`.
- `action`: the action for this video generation task, mainly including three actions: text-to-video (`text2video`), image-to-video (`image2video`), and video extension (`extend`).
- `start_image_url`: when selecting the image-to-video action `image2video`, it is required to upload the first frame reference image link.
- `end_image_url`: optional for image-to-video, specifies the last frame reference image.
- `duration`: video duration in seconds. For `kling-v3` and `kling-v3-omni` models, flexible duration of 3–15 seconds (integers) is supported; other models support 5 or 10 seconds.
- `generate_audio`: whether to generate audio simultaneously, optional boolean. Supported by `kling-v3`, `kling-v3-omni`, and `kling-v2-6` (pro mode only). Defaults to `false`.
- `aspect_ratio`: video aspect ratio, optional, supports `16:9`, `9:16`, `1:1`, defaults to `16:9`.
- `cfg_scale`: relevance strength, range [0,1]; higher values follow the prompt more closely.
- `camera_control`: optional, an object controlling camera movement, supports type/simple presets as well as horizontal, vertical, pan, tilt, roll, and zoom configurations.
- `negative_prompt`: optional, reverse prompt describing content you do not want to appear, up to 200 characters.
- `element_list`: subject reference list, only applicable to the `kling-video-o1` model. For detailed usage, refer to the [official documentation](https://docs.qingque.cn/d/home/eZQAyImcbaS0fz-8ANjXvU5ed?identityId=1oEG9JKKMFv#section=h.5t7wme23nn6z).
- `video_list`: reference videos retrieved by URL, only applicable to the `kling-video-o1` model. For detailed usage, refer to the [official documentation](https://docs.qingque.cn/d/home/eZQAyImcbaS0fz-8ANjXvU5ed?identityId=1oEG9JKKMFv#section=h.5t7wme23nn6z).
- `prompt`: prompt words.
- `callback_url`: the URL to which the results need to be returned.

After selection, you can see that the corresponding code is also generated on the right side, as shown in the image:

<p><img src="https://cdn.acedata.cloud/3yjql0.png" width="500" class="m-auto"></p>

Click the "Try" button to test, as shown in the image above, and we obtained the following result:

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

- `success`: the status of the video generation task at this time.
- `task_id`: the ID of the video generation task at this time.
- `video_id`: the video ID of the video generation task.
- `video_url`: the video link of the video generation task.
- `duration`: the video duration of the video generation task.
- `state`: the state of the video generation task.

We can see that we have obtained satisfactory video information, and we only need to obtain the generated Kling video based on the video link address in `video_url`.

Additionally, if you want to generate the corresponding integration code, you can directly copy it, for example, the CURL code is as follows:

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

Different models have significant differences in parameter support. The following matrix is compiled from the [Kling official video models documentation](https://app.klingai.com/global/dev/document-api/apiReference/model/videoModels). Before calling, please verify that the current `model` / `mode` / `duration` combination supports the features you need, otherwise the upstream will return errors such as `model/mode/duration(...) is not supported with image_tail`.

| Model | Mode | `end_image_url` (last frame) | `generate_audio` | `camera_control` | Notes |
|---|---|---|---|---|---|
| `kling-v1` | std / pro | ✅ `duration=5` only | ❌ | ✅ `duration=5` only | `extend` does not support `negative_prompt` or `cfg_scale` |
| `kling-v1-6` | std | ❌ | ❌ | ❌ | Multi-image-to-video and `extend` available in all modes |
| `kling-v1-6` | pro | ✅ | ❌ | ❌ | |
| `kling-v2-master` | — | ❌ | ❌ | ❌ | Single mode, `duration=5/10` only |
| `kling-v2-1-master` | — | ❌ | ❌ | ❌ | Single mode, `duration=5/10` only |
| `kling-v2-5-turbo` | std | ❌ | ❌ | ❌ | |
| `kling-v2-5-turbo` | pro | ✅ | ❌ | ❌ | |
| `kling-v2-6` | std | ❌ | ❌ | ❌ | |
| `kling-v2-6` | pro | ✅ | ✅ | ❌ | Only non-v3 model that also supports audio generation |
| `kling-v3` | std / pro | ✅ | ✅ | ✅ | `duration` range 3–15 seconds |
| `kling-v3` | 4k | ✅ | ✅ | ❌ | 4K mode is incompatible with camera control |
| `kling-v3-omni` | std / pro / 4k | ✅ | ✅ | ❌ | |
| `kling-video-o1` | std / pro | ✅ | ❌ | ❌ | `duration=5/10` only |

Notes:

- `mode=4k` is only supported by `kling-v3` and `kling-v3-omni`, and is mutually exclusive with `camera_control`.
- `end_image_url` can only be used with `action=image2video` together with `start_image_url`. Passing only `end_image_url` without `start_image_url` will be rejected.
- `kling-v3` / `kling-v3-omni` accept any integer `duration` from 3–15 seconds; all other models only accept 5 or 10.
- `generate_audio` defaults to `false`. Only `kling-v3`, `kling-v3-omni`, and `kling-v2-6` (pro mode) support it.

## Video Extension Functionality

If you want to continue generating an existing Kling video, you can set the parameter `action` to `extend` and input the ID of the video to continue from. The video ID is obtained from the basic usage response, as shown below:

<p><img src="https://cdn.acedata.cloud/om6p6g.png" width="500" class="m-auto"></p>

At this point, you can see that the video ID is:

```
"video_id": "030bb06d-98d4-4044-9042-0aa0822e8c8c"
```

> Note: The `video_id` here is the ID of the generated video. If you do not know how to generate a video, please refer to the Basic Usage section above.

Next, you must fill in the prompt words for the next step to customize the generated video. You can specify the following content:

- `model`: the model for generating the video, mainly including `kling-v1`, `kling-v1-5`, and `kling-v1-6`.
- `mode`: the mode for generating the video, optional values are standard mode `std`, fast mode `pro`, and native 4K mode `4k` (only supported by `kling-v3` and `kling-v3-omni`, incompatible with camera control).
- `duration`: the video duration for this video generation task, mainly supporting 5s and 10s.
- `start_image_url`: when selecting the image-to-video action `image2video`, it is required to upload the first frame reference image link.
- `prompt`: prompt words.

An example of filling out is as follows:

<p><img src="https://cdn.acedata.cloud/ejimqy.png" width="500" class="m-auto"></p>

After filling it out, the code is automatically generated as follows:

<p><img src="https://cdn.acedata.cloud/52x4u5.png" width="500" class="m-auto"></p>

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

Clicking run, you can find that a result is obtained, as follows:

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

It can be seen that the result content is consistent with the above text, thus achieving the video extension functionality.

## Asynchronous Callback

Since the time taken by the Kling Videos Generation API is relatively long, approximately 1-2 minutes, if the API does not respond for a long time, the HTTP request will keep the connection open, leading to additional system resource consumption. Therefore, this API also provides support for asynchronous callbacks.

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

Through this document, you have learned how to use the Kling Videos Generation API to generate videos by inputting prompt words and optional reference images. We hope this document can help you better integrate and use this API. If you have any questions, please feel free to contact our technical support team.
