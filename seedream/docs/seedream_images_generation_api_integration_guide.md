# Seedream Images Generation API Integration Instructions

This article will introduce the integration instructions for the SeeDream Images Generation API, which can generate official SeeDream images by inputting custom parameters.

## Application Process

To use the SeeDream Images Generation API, apply for the corresponding service on the [Seedream Images Generation API](https://platform.acedata.cloud/documents/86ad30f3-0bc8-4b9b-b019-b9fa5b05672e) page. After entering the page, click the "Acquire" button.

If you are not logged in or registered, you will be automatically redirected to the login page. Upon the first application, there will be a free quota provided. **One API token calls every platform service.**

## Basic Usage

Request body fields:

- `prompt`: the prompt (required).
- `model`: the generation model, default is `doubao-seedream-5-0-260128` (SeeDream 5.0 Lite, latest). Supports:
  - `doubao-seedream-5-0-pro-260628`: SeeDream 5.0 Pro, flagship single image model; **does not support group images (`sequential_image_generation`), streaming (`stream`), or online search (`tools`)**
  - `doubao-seedream-5-0-260128`: SeeDream 5.0 Lite (default)
  - `doubao-seedream-4-5-251128`: SeeDream 4.5
  - `doubao-seedream-4-0-250828`: SeeDream 4.0
  - `doubao-seedream-3-0-t2i-250415`: SeeDream 3.0 text-to-image
  - `doubao-seededit-3-0-i2i-250628`: SeedEdit 3.0 image-to-image editing
  - **The `model` must use the complete model string (e.g., `doubao-seedream-5-0-260128`); passing abbreviations will return 400.**
- `image`: the input image information (URL or Base64 encoding) for image-to-image generation or editing. `doubao-seedream-5-0-pro-260628` supports single or multiple image inputs (2-10 images); `doubao-seedream-5-0-260128`, `doubao-seedream-4-5-251128`, `doubao-seedream-4-0-250828` support single or multiple image inputs; `doubao-seededit-3-0-i2i-250628` supports only single image input; `doubao-seedream-3-0-t2i-250415` does not support this parameter.
- `size`: output resolution. Two methods:
  - Method 1: Preset resolution keyword — `doubao-seedream-5-0-pro-260628` supports `1K`/`2K`; `doubao-seedream-5-0-260128` supports `2K`/`3K`/`4K`; `doubao-seedream-4-5-251128` supports `2K`/`4K`; `doubao-seedream-4-0-250828` supports `1K`/`2K`/`4K`; `doubao-seedream-3-0-t2i-250415` and `doubao-seededit-3-0-i2i-250628` **do not support presets**, only Method 2.
  - Method 2: Specify exact pixel values like `2048x2048`. Default is `2048x2048`.
- `seed`: random seed, range [-1, 2147483647]. **Only `doubao-seedream-3-0-t2i-250415` supports this parameter**.
- `sequential_image_generation`: group images (a set of related images). Supported by `doubao-seedream-5-0-260128`, `doubao-seedream-4-5-251128`, `doubao-seedream-4-0-250828`. Default `disabled`.
- `stream`: streaming output mode. Supported by `doubao-seedream-5-0-260128`, `doubao-seedream-4-5-251128`, `doubao-seedream-4-0-250828`. Default `false`.
- `guidance_scale`: consistency between model output and prompt, range [1, 10]. `doubao-seedream-3-0-t2i-250415` default 2.5, `doubao-seededit-3-0-i2i-250628` default 5.5; other models do not support.
- `response_format`: return format of the generated image. Default `url`, also supports `b64_json`.
- `watermark`: whether to add a watermark. Default `true`.
- `output_format`: file format of the generated image, `jpeg` (default) or `png`. Only `doubao-seedream-5-0-pro-260628` and `doubao-seedream-5-0-260128` support.
- `tools`: tools the model will call, currently supporting `web_search` (online search). Only `doubao-seedream-5-0-260128` supports.
- `callback_url`: the URL to which the results will be sent upon task completion.
- `async`: when set to `true`, the interface immediately returns `task_id`; poll results through the Seedream Tasks API.

### Request Example

```bash
curl -X POST 'https://api.acedata.cloud/seedream/images' -H 'authorization: ******' -H 'accept: application/json' -H 'content-type: application/json' -d '{
  "model": "doubao-seedream-5-0-260128",
  "prompt": "A photorealistic studio product shot of a frosted-glass perfume bottle on wet black slate, single softbox key light, water droplets, dark moody background, 85mm macro."
}'
```

### Response Example

```json
{
  "success": true,
  "task_id": "81246f86-05ff-4d7d-9553-1013e0c1cd32",
  "trace_id": "ab50a78d-ab1f-457f-a46b-c2259cd5d35b",
  "data": [
    {
      "prompt": "A photorealistic studio product shot of a frosted-glass perfume bottle on wet black slate, single softbox key light, water droplets, dark moody background, 85mm macro.",
      "size": "2048x2048",
      "image_url": "https://platform2.cdn.acedata.cloud/seedream/901c6af6-e83a-4849-b233-295f6c20bacb.jpg"
    }
  ]
}
```

Response fields:

- `success`: the status of the image generation task.
- `task_id`: the ID of the image generation task.
- `trace_id`: the tracking ID of this request.
- `data`: the result list.
  - `image_url`: the link to the generated image.
  - `prompt`: the prompt used.
  - `size`: the pixel size of the generated image.

## Image Editing

To edit an image, pass the source image in the `image` parameter:

```python
import requests

url = "https://api.acedata.cloud/seedream/images"

headers = {
    "accept": "application/json",
    "authorization": "******",
    "content-type": "application/json"
}

payload = {
    "model": "doubao-seedream-4-0-250828",
    "prompt": "Keep the model pose and the liquid garment flowing shape unchanged. Change the clothing material from silver metal to completely transparent water (or glass). Through the liquid flow, the details of the model skin are visible. The light and shadow effect shifts from reflection to refraction.",
    "image": ["https://ark-project.tos-cn-beijing.volces.com/doc_image/seedream4_5_imageToimage.png"],
    "size": "2K",
    "watermark": False
}

response = requests.post(url, json=payload, headers=headers)
print(response.text)
```

Result:

```json
{
  "success": true,
  "task_id": "c9aaffa2-b8ac-40ff-8468-43e77cb9ddde",
  "trace_id": "131a40c3-2eaf-44c9-af28-c9b408577286",
  "data": [
    {
      "prompt": "Keep the model pose and the liquid garment flowing shape unchanged...",
      "size": "2048x2048",
      "image_url": "https://platform.cdn.acedata.cloud/seedream/3e88db7e-4771-4f6a-adbd-5ae4590c5d59.jpg"
    }
  ]
}
```

## Asynchronous Callback

For long-running requests, use `callback_url` or `async: true`:

- Set `callback_url` to receive the result via POST JSON when the task completes.
- Set `async: true` to get an immediate `task_id` and poll results via the Seedream Tasks API.

## Error Handling

| HTTP | Code | Meaning |
| ---- | ---- | ---- |
| 400 | `token_mismatched` | Bad request, missing or invalid parameters |
| 400 | `api_not_implemented` | Interface not implemented |
| 401 | `invalid_token` | Authentication failed or token missing |
| 429 | `too_many_requests` | Request frequency limit exceeded |
| 500 | `api_error` | Server exception |

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
