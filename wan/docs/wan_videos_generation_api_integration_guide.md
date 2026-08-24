# Wan Videos Generation API Integration Instructions

This article will introduce the Wan Videos Generation API integration instructions, which can generate official videos of Tongyi Wanxiang by inputting custom parameters.

## Application Process

To use Wan Videos Generation API, first open the [Ace Data Cloud Console](https://platform.acedata.cloud/console/applications) and copy your API Token.

![](https://cdn.acedata.cloud/dvc3cg.jpg)

If you are not logged in, you will be redirected to sign in and brought back to this page automatically.

**A single API Token works across every service on the platform — no need to subscribe per service.** New accounts receive free starter credit; when it runs low you can top up your shared balance in the [console](https://platform.acedata.cloud/console/coin).

> 📘 Full documentation: [Wan Videos Generation API →](https://platform.acedata.cloud/documents/wan-videos)

## Basic Usage

First, understand the basic usage method, which involves inputting the prompt `prompt`, the action `action`, the first frame reference image `image_url`, and the model `model` to obtain the processed result. You first need to simply pass a field `action`, with the value set to `text2video`. It includes two types of actions: text-to-video (`text2video`) and image-to-video (`image2video`). Then, we also need to input the model `model`, which currently mainly includes `wan2.6-i2v`, `wan2.6-r2v`, `wan2.6-i2v-flash`, `wan2.6-t2v`, and `wan3.0-video`. The specific content is as follows:

<p><img src="https://cdn.acedata.cloud/03gqdz.png" width="500" class="m-auto"></p>

Here we can see that we have set the Request Headers, including:

- `accept`: the format of the response result you want to receive, filled in as `application/json`, which means JSON format.
- `authorization`: the key to call the API, which can be directly selected after application.

Additionally, we set the Request Body, including:

- `model`: the model for generating the video, mainly including `wan2.6-i2v`, `wan2.6-r2v`, `wan2.6-i2v-flash`, `wan2.6-t2v`, and `wan3.0-video`.
- `action`: the action for this video generation task, either text-to-video (`text2video`) or image-to-video (`image2video`). When it is text-to-video, use a text-to-video model such as `wan2.6-t2v`. When it is image-to-video, use an image/video reference model such as `wan2.6-i2v`, `wan2.6-r2v`, `wan2.6-i2v-flash`, or `wan3.0-video`.
- `image_url`: when selecting the image-to-video action `image2video`, upload the first frame reference image link. Currently, only the models `wan2.6-i2v` and `wan2.6-i2v-flash` are supported.
- `reference_video_urls`: optional for image-to-video, specifies the reference video links for generation. Currently, only the model `wan2.6-r2v` is supported.
- `size`: specifies the resolution of the generated video, in the format of width*height. The default value and available enumerated values for this parameter depend on the model parameter. For specific rules, please refer to the [official documentation](https://modelstudio.console.alibabacloud.com/ap-southeast-1/?tab=api#/api/?type=model&url=2865250).
- `duration`: the duration of the video generation. The API accepts integer durations from 2 to 30 seconds, or `-1` for model default behavior.
- `shot_type`: optional, specifies the type of shot for the generated video, i.e., whether the video consists of a continuous shot or multiple switching shots. Effective condition: only effective when "prompt_extend": true. Parameter priority: shot_type > prompt. For example, if shot_type is set to "single", even if the prompt contains "generate multi-shot video", the model will still output a single-shot video. For specific rules, please refer to the [official documentation](https://modelstudio.console.alibabacloud.com/ap-southeast-1/?tab=api#/api/?type=model&url=2865250).
- `negative_prompt`: optional, reverse prompt words used to describe content that you do not want to see in the video frame, which can limit the video frame. Supports both Chinese and English, with a length not exceeding 500 characters; excess parts will be automatically truncated. Example values: low resolution, errors, worst quality, low quality, incomplete, extra fingers, poor proportions, etc.
- `resolution`: specifies the resolution level of the generated video, used to adjust the clarity of the video (total pixels). The model will automatically scale to a similar total pixel count based on the selected resolution level, and the video aspect ratio will try to maintain consistency with the aspect ratio of the input image img_url. For more details, please refer to the [official documentation](https://modelstudio.console.alibabacloud.com/ap-southeast-1/?tab=api#/api/?type=model&url=2867393).
- `audio_url`: the URL of the audio file, which the model will use to generate the video. For usage, refer to the [official documentation](https://modelstudio.console.alibabacloud.com/ap-southeast-1/?tab=api#/api/?type=model&url=2867393).
- `audio`: whether to generate a video with sound. Parameter priority: audio > audio_url. When audio=false, even if audio_url is passed in, the output will still be a silent video, and billing will be calculated as a silent video. The default value is false.
- `prompt_extend`: whether to enable intelligent rewriting of the prompt. When enabled, a large model will intelligently rewrite the input prompt. The effect of generation is significantly improved for shorter prompts, but it will increase processing time. The default value is false.
- `prompt`: prompt words.
- `media`: optional media URL array for `wan3.0-video`, up to 10 items.
- `ratio`: output aspect ratio, one of `adaptive`, `16:9`, `4:3`, `1:1`, `3:4`, or `9:16`.
- `seed`: optional random seed from 0 to 2147483647 for reproducible results.
- `watermark`: whether to add a watermark. The default value is false.
- `async`: whether to return immediately with a task ID for asynchronous polling.
- `callback_url`: the URL to which the results need to be returned.

After selection, you can see that the corresponding code is also generated on the right side, as shown in the image:

<p><img src="https://cdn.acedata.cloud/03gqdz.png" width="500" class="m-auto"></p>

Click the "Try" button to test, as shown in the image above, and we obtained the following result:

```json
{
  "success": true,
  "video_url": "https://cdn.acedata.cloud/43a57990c0.mp4",
  "state": "completed",
  "task_id": "a4bca552-d964-46a1-8ff7-fd922f916582",
  "video_id": "b4ef4c5e-9680-41c8-a678-0ce2ce6194de",
  "video_width": 1552,
  "video_height": 656,
  "thumbnail_url": "https://cdn.acedata.cloud/4hfydw.jpg",
  "thumbnail_width": 1552,
  "thumbnail_height": 656
}
```

The returned result contains multiple fields, described as follows:

- `success`: the status of the video generation task at this time.
- `task_id`: the ID of the video generation task at this time.
- `video_url`: the video link of the video generation task at this time.
- `state`: the status of the video generation task at this time.
- `video_id`: the generated video identifier.
- `video_width` / `video_height`: generated video dimensions.
- `thumbnail_url`: generated video thumbnail URL.
- `thumbnail_width` / `thumbnail_height`: thumbnail dimensions.

We can see that we have obtained satisfactory video information, and we only need to obtain the generated Tongyi Wanxiang video based on the video link address in `video_url`.

Additionally, if you want to generate the corresponding integration code, you can directly copy it, for example, the CURL code is as follows:

```shell
curl -X POST 'https://api.acedata.cloud/wan/videos' \
-H 'accept: application/json' \
-H 'authorization: YOUR_API_TOKEN' \
-H 'content-type: application/json' \
-d '{
  "action": "text2video",
  "model": "wan2.6-t2v",
  "prompt": "Astronauts shuttle from space to volcano",
  "duration": 5
}'
```

## Image-to-Video Functionality

If you want to generate a video based on a reference image or reference video, you can set the parameter `action` to `image2video`, and input the required reference image link or reference video link. Next, you must fill in the prompt words needed for the next step to customize the generated video, specifying the following content:

- `model`: The model for generating the video, mainly including `wan2.6-i2v`, `wan2.6-r2v`, `wan2.6-i2v-flash`, `wan2.6-t2v`, and `wan3.0-video` models.
- `image_url`: When selecting the image-to-video action `image2video`, you must upload the link to the first frame reference image, currently only supporting models `wan2.6-i2v`, `wan2.6-i2v-flash`. For `wan3.0-video`, use the `media` array when passing media references.
- `reference_video_urls`: Optional when generating video from images, specify the reference video link for generation, currently only supporting model `wan2.6-r2v`.
- `prompt`: Prompt words.

An example of filling out is as follows:

<p><img src="https://cdn.acedata.cloud/94l0kk.png" width="500" class="m-auto"></p>

After filling it out, the code is automatically generated as follows:

<p><img src="https://cdn.acedata.cloud/b5q8tt.png" width="500" class="m-auto"></p>

The corresponding Python code:

```python
import requests

url = "https://api.acedata.cloud/wan/videos"

headers = {
    "accept": "application/json",
    "authorization": "YOUR_API_TOKEN",
    "content-type": "application/json"
}

payload = {
    "action": "image2video",
    "model": "wan2.6-i2v",
    "prompt": "Astronauts shuttle from space to volcano",
    "duration": 5,
    "image_url": "https://cdn.acedata.cloud/r9vsv9.png",
    "callback_url": "https://www.baidu.com/"
}

response = requests.post(url, json=payload, headers=headers)
print(response.text)
```

Clicking run, you can find that a result is obtained, as follows:

```json
{
  "success": true,
  "video_url": "https://cdn.acedata.cloud/43a57990c0.mp4",
  "state": "completed",
  "task_id": "a4bca552-d964-46a1-8ff7-fd922f916582",
  "video_id": "b4ef4c5e-9680-41c8-a678-0ce2ce6194de",
  "video_width": 1552,
  "video_height": 656,
  "thumbnail_url": "https://cdn.acedata.cloud/4hfydw.jpg",
  "thumbnail_width": 1552,
  "thumbnail_height": 656
}
```

It can be seen that the result content is consistent with the above text, thus achieving the video extension function.

## Asynchronous Callback

Since the time taken by the Wan Videos Generation API is relatively long, approximately 1-2 minutes, if the API does not respond for a long time, the HTTP request will keep the connection open, leading to additional system resource consumption. Therefore, this API also provides support for asynchronous callbacks.

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
  "video_url": "https://cdn.acedata.cloud/43a57990c0.mp4",
  "state": "completed",
  "task_id": "a4bca552-d964-46a1-8ff7-fd922f916582",
  "video_id": "b4ef4c5e-9680-41c8-a678-0ce2ce6194de",
  "video_width": 1552,
  "video_height": 656,
  "thumbnail_url": "https://cdn.acedata.cloud/4hfydw.jpg",
  "thumbnail_width": 1552,
  "thumbnail_height": 656
}
```

It can be seen that the result contains a `task_id` field, and the other fields are similar to the above text, allowing the task to be associated through this field.

## Error Handling

When calling the API, if an error occurs, the API will return the corresponding error code and message. For example:

- `400 bad_request`: Bad request, possibly due to missing or invalid parameters.
- `400 token_mismatched`: Bad request, the token is not matched with this API.
- `400 api_not_implemented`: Bad request, the API is not implemented.
- `401 invalid_token`: Unauthorized, invalid or missing authorization token.
- `403 forbidden`: The prompt or media violates moderation rules.
- `429 too_many_requests`: Too many requests, you have exceeded the rate limit.
- `500 api_error`: Internal server error, something went wrong on the server.
- `504 timeout`: The request timed out while generating the video.

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

Through this document, you have learned how to use the Wan Videos Generation API to generate videos by inputting prompt words and the first frame reference image. We hope this document can help you better integrate and use this API. If you have any questions, please feel free to contact our technical support team.
