# Qwen Image Images API Integration Instructions

This guide explains how to call the Qwen Image Images API to generate or edit images with Qwen Image 3 models.

## Application Process

To use Qwen Image APIs, first open the [Ace Data Cloud Console](https://platform.acedata.cloud/console/applications) and copy your API Token.

If you are not logged in, you will be redirected to sign in and brought back automatically.

**A single API Token works across every service on the platform — no need to subscribe per service.** New accounts receive free starter credit; when it runs low you can top up your shared balance in the [console](https://platform.acedata.cloud/console/coin).

> 📘 Full documentation: [Qwen Image Images API →](https://platform.acedata.cloud/documents/qwen-image-images)

## Basic Usage

Send a POST request to `/qwen-image/images` with your API token in the `Authorization` header and a JSON request body.

**Request Headers** include:

- `accept`: the format of the response result you want to receive, filled in as `application/json`.
- `authorization`: your Ace Data Cloud API Token.
- `content-type`: `application/json`.

**Request Body** includes:

- `model`: required, one of `qwen-image-3.0` or `qwen-image-3.0-pro`. The default is `qwen-image-3.0`.
- `prompt`: required image description, 1 to 18000 characters.
- `image_urls`: optional source image URL array for image editing, 1 to 3 URLs.
- `n`: optional number of images to generate, from 1 to 6. The default is 1.
- `size`: optional image size in `width*height` format, for example `1024*1024`.
- `prompt_extend`: optional, whether to enable prompt extension. The default is true.
- `prompt_extend_mode`: optional prompt extension mode, `direct` or `agent`. The default is `direct`.
- `enable_thinking`: optional, whether to enable thinking mode. The default is true.
- `negative_prompt`: optional description of content to avoid.
- `seed`: optional random seed from 0 to 2147483647 for reproducible results.
- `watermark`: optional, whether to add a watermark. The default is false.
- `callback_url`: optional URL to receive asynchronous results.
- `async`: optional, whether to return immediately with a task ID. The default is false.

### Text-to-Image Request Example

```bash
curl -X POST 'https://api.acedata.cloud/qwen-image/images' \
-H 'accept: application/json' \
-H 'authorization: YOUR_API_TOKEN' \
-H 'content-type: application/json' \
-d '{
  "model": "qwen-image-3.0",
  "prompt": "a serene mountain lake at sunrise, photorealistic",
  "size": "1024*1024",
  "n": 1
}'
```

### Python Example

```python
import requests

url = "https://api.acedata.cloud/qwen-image/images"

headers = {
    "accept": "application/json",
    "authorization": "YOUR_API_TOKEN",
    "content-type": "application/json"
}

payload = {
    "model": "qwen-image-3.0",
    "prompt": "a serene mountain lake at sunrise, photorealistic",
    "size": "1024*1024",
    "n": 1
}

response = requests.post(url, json=payload, headers=headers)
print(response.text)
```

### Response Example

```json
{
  "success": true,
  "task_id": "ec22ae22-0140-4033-8c86-a48b536da595",
  "trace_id": "1cc87db0-8ee5-4436-969b-35cc571a9fd5",
  "data": [
    {
      "image_url": "https://cdn.acedata.cloud/qwen-image/example.png"
    }
  ],
  "usage": {
    "model": "qwen-image-3.0"
  }
}
```

The returned result contains multiple fields, described as follows:

- `success`: whether the request succeeded.
- `task_id`: the image generation task ID. Use it with the Qwen Image Tasks API when polling asynchronous work.
- `trace_id`: request trace identifier.
- `data`: generated image results. Each item contains an `image_url`.
- `usage`: usage information returned by the service.

## Image Editing

Pass one to three source image URLs in `image_urls` to edit images based on the prompt.

```json
{
  "model": "qwen-image-3.0-pro",
  "prompt": "make the sky golden hour and keep the original composition",
  "image_urls": ["https://example.com/photo.png"],
  "size": "1024*1024"
}
```

## Asynchronous Processing

Set `async` to true or provide `callback_url` when you want the API to return immediately with a task ID. You can poll `/qwen-image/tasks` with that task ID, or receive the completed result at your callback URL.

```json
{
  "model": "qwen-image-3.0",
  "prompt": "a futuristic city at sunset",
  "async": true
}
```

## Error Handling

When calling the API, if an error occurs, the API will return the corresponding error code and message. For example:

- `400 token_mismatched`: Bad request, the token is not matched with this API.
- `400 api_not_implemented`: Bad request, the API is not implemented.
- `401 invalid_token`: Unauthorized, invalid or missing authorization token.
- `401 token_expired`: Unauthorized, the token has expired.
- `403 used_up`: Insufficient balance for the current request.
- `404 no_api`: API does not exist; check the URL.
- `413 request_too_large`: Request body is too large.
- `429 too_many_requests`: Too many requests, you have exceeded the rate limit.
- `500 api_error`: Internal server error, something went wrong on the server.

### Error Response Example

```json
{
  "error": {
    "code": "api_error",
    "message": "Internal server error."
  },
  "trace_id": "2efa9340-b21b-4e26-9e14-4aac95f343ab"
}
```

## Conclusion

Through this document, you have learned how to use the Qwen Image Images API to generate and edit images. If you have any questions, please contact our technical support team.
