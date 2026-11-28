# Seedream Images API integration guide

Use `POST https://api.acedata.cloud/seedream/images` with an AceDataCloud bearer token. [Seedream API reference](https://platform.acedata.cloud/documents/86ad30f3-0bc8-4b9b-b019-b9fa5b05672e).

Sign in to [Applications](https://platform.acedata.cloud/console/applications) and open **General Application**. Initialize it on your first visit if prompted, then copy the key shown in **API KEY**. Keep the copied key on your server and use it in place of `YOUR_API_TOKEN` below.

![General Application API KEY field and copy button](https://cdn.acedata.cloud/dvc3cg.jpg)

## Model selection

| Model | Presets | Capabilities |
|---|---|---|
| `doubao-seedream-5-5-261028` | 1K, 1.5K, 2K | Up to 10 references, native transparent PNG, up to 99 editable layers and optional styled OCR |
| `doubao-seedream-5-0-flash-260915` | 1K, 1.5K, 2K | Fast single-image generation and editing, up to 10 references and 16 editable layers |
| `doubao-seedream-5-0-pro-260628` | 1K, 1.5K, 2K | Up to 10 references and 16 editable layers, standard or fast prompt optimization |
| `doubao-seedream-5-0-lite-260128` | 2K, 3K, 4K | Up to 14 references, sequential images, streaming and web search |

Explicit `WIDTHxHEIGHT` values are accepted within each model's pixel and aspect-ratio limits. Seedream 4.5 and 4.0 remain supported for compatibility.

## Generate or edit images

```bash
curl https://api.acedata.cloud/seedream/images \
  -H 'Authorization: Bearer YOUR_API_TOKEN' \
  -H 'Content-Type: application/json' \
  -d '{
    "model": "doubao-seedream-5-0-lite-260128",
    "prompt": "a four-panel storyboard of a courier crossing a rainy neon city",
    "size": "2K",
    "sequential_image_generation": "auto",
    "sequential_image_generation_options": {"max_images": 4},
    "watermark": false
  }'
```

Add `image` as one image URL, a Base64 string, or an array for editing. Lite requires the sum of input images and requested outputs to be at most 15 and can use `tools: [{"type":"web_search"}]`. Use `output_format` to choose JPEG or PNG and `response_format` to choose a URL or Base64. For 5.5 or Flash layer decomposition, use URL output.

## Generate a transparent image

```json
{
  "model": "doubao-seedream-5-5-261028",
  "prompt": "A matte blue cube isolated on a transparent background",
  "background": "transparent",
  "output_format": "png",
  "size": "1.5K"
}
```

Seedream 5.5 accepts a text prompt alone, or a prompt with reference images. For transparent editing with 5.0 Pro or Flash, supply exactly one reference image with an alpha channel. Use PNG for transparent output and omit `background` in layer decomposition.

## Decompose one image into editable layers

```json
{
  "model": "doubao-seedream-5-5-261028",
  "image": "https://example.com/poster.png",
  "layer_decomposition": true,
  "layer_decomposition_options": {"max_images": 12, "text_recognition": true},
  "size": "auto",
  "watermark": false
}
```

Omit `prompt` for automatic decomposition, describe desired elements, or use normalized `<bbox>` coordinates. The result contains one base image (`z_index: 0`) and transparent PNG layers. Seedream 5.5 allows up to 100 images including the base and can return text and styles in `data[].text_recognition` for recognized text layers. Seedream 5.0 Pro and Flash support up to 16 layers. Draw layers in ascending `z_index` at their bounding-box positions to reconstruct the image.

## Async and streaming

Use `"async": true` to return a `task_id`, then poll `POST /seedream/tasks` with `{"action":"retrieve","id":"..."}`. A real public `callback_url` can receive the result instead.

Lite/4.x streaming uses `"stream": true` and `Accept: application/x-ndjson`. Read one JSON event per line until `image_generation.completed`. Do not combine streaming with `async` or `callback_url`.

## Response fields

A normal response includes `success`, `task_id`, `trace_id`, `data`, optional `tools`, and `usage`. Each data item can contain `image_url` or `b64_json`, `size`, and `output_format`. Lite image sets can include per-item `error` objects without discarding successful items. Layer responses additionally include `z_index`, `name`, `description`, and bounding boxes.

Save results you want to keep before their URLs expire. Seedream 5.5 charges for each reference image and each successful output by pixel tier. Seedream 5.0 Flash charges a flat rate for each successful output and includes reference images. The base image and layers are individual outputs. [Current pricing](https://platform.acedata.cloud/services/seedream?tab=pricing)

## Error codes

| HTTP | Code | Meaning |
|---|---|---|
| 400 | `bad_request` | Unsupported model/parameter combination or invalid input |
| 401 | `invalid_token`, `token_expired` | Invalid authentication |
| 403 | `used_up`, `forbidden` | Insufficient balance or blocked content |
| 429 | `too_many_requests` | Rate limited |
| 500 | `api_error` | Service error |
