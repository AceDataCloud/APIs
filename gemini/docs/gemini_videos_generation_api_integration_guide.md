# Gemini Videos Generation API Integration Instructions

The Gemini Videos API generates videos from text prompts and optional reference media. Ace Data Cloud exposes this endpoint at `POST /gemini/videos`.

## Application Process

Create an API Token in the [Ace Data Cloud Console](https://platform.acedata.cloud/console/applications), then send it in the `Authorization` header.

One API Token works across Ace Data Cloud services. New accounts receive starter credit, and you can top up shared balance in the [console](https://platform.acedata.cloud/console/coin).

Full documentation: [Gemini Videos Generation API](https://platform.acedata.cloud/documents/gemini-videos)

## Basic Usage

Send a POST request to `/gemini/videos`.

### Request Headers

- `Authorization`: your Ace Data Cloud API Token
- `Content-Type: application/json`
- `Accept: application/json`

### Request Body

- `prompt` (string, required): text prompt describing the video to generate.
- `model` (string, optional): currently `omni-flash`.
- `aspect_ratio` (string, optional): `16:9` or `9:16`.
- `resolution` (string, optional): `720p` or `1080p`.
- `image_urls` (array, optional): reference image URLs.
- `video_urls` (array, optional): reference video URLs.
- `callback_url` (string, optional): callback URL for asynchronous completion.
- `async` (boolean, optional): preserve the returned `task_id` and fetch task status later from the Gemini Tasks API.

### CURL Example

```bash
curl -X POST 'https://api.acedata.cloud/gemini/videos' \
  -H 'accept: application/json' \
  -H 'authorization: ******' \
  -H 'content-type: application/json' \
  -d '{
    "prompt": "A cinematic shot of a kitten chasing a butterfly in a sunlit garden",
    "model": "omni-flash",
    "aspect_ratio": "16:9"
  }'
```

### Response Example

```json
{
  "success": true,
  "task_id": "b8976e18-32dc-4718-9ed8-1ea090fcb6ea",
  "trace_id": "fb751e1e-4705-49ea-9fd4-5024b7865ea2",
  "data": [
    {
      "id": "omni-flash:job_01k777hjrbfrgs2060q5zvf2a5",
      "video_url": "https://cdn.acedata.cloud/43a57990c0.mp4",
      "state": "succeeded"
    }
  ]
}
```

The success response includes:

- `success`: whether the request succeeded.
- `task_id`: the task identifier for later lookup.
- `trace_id`: request trace identifier for support and debugging.
- `data`: an array of generated video results.
  - `id`: generated video identifier.
  - `video_url`: output video URL.
  - `state`: task state, such as `pending`, `succeeded`, or `failed`.

## Image to Video

You can guide generation with reference images by passing `image_urls`:

```json
{
  "prompt": "The woman slowly turns around and smiles at the camera, gentle breeze",
  "model": "omni-flash",
  "aspect_ratio": "9:16",
  "image_urls": [
    "https://platform2.cdn.acedata.cloud/nanobanana/e44bfceb-1458-4b4b-9d10-21024678f1a3.png"
  ]
}
```

## Video Editing / Reference Video

You can also guide generation with reference video input by passing `video_urls`. Current Ace Data Cloud documentation pairs this workflow with at least one reference image in `image_urls`.

```json
{
  "prompt": "Convert this tropical beach scene into a snowy winter scene while keeping the same camera layout.",
  "model": "omni-flash",
  "aspect_ratio": "9:16",
  "resolution": "720p",
  "image_urls": [
    "https://cdn.acedata.cloud/99289603bd.png"
  ],
  "video_urls": [
    "https://platform2.cdn.acedata.cloud/seedance/dd3dc063-3383-4f29-bedc-e771a096758c.mp4"
  ],
  "async": true
}
```

## Asynchronous Processing

If you provide `callback_url` or submit work with `async: true`, keep the returned `task_id`. You can later query `POST /gemini/tasks` to inspect the stored request, latest response, and timing fields for the job.

Example task lookup request:

```bash
curl -X POST 'https://api.acedata.cloud/gemini/tasks' \
  -H 'accept: application/json' \
  -H 'authorization: ******' \
  -H 'content-type: application/json' \
  -d '{
    "id": "b8976e18-32dc-4718-9ed8-1ea090fcb6ea",
    "action": "retrieve"
  }'
```

## Error Handling

The current Gemini Videos OpenAPI documents the following error responses:

| HTTP Status Code | Meaning |
| --- | --- |
| 400 | Invalid request parameters |
| 401 | Authentication failed |
| 403 | Request forbidden or blocked by upstream |
| 500 | Internal server error |
