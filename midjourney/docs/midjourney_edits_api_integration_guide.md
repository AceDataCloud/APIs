# Midjourney Edits API Integration Guide

The Midjourney Edits API allows editing existing images using Midjourney's in-painting and re-drawing capabilities by providing an image URL and a prompt.

This document provides detailed integration instructions for the Midjourney Edits API, helping you easily integrate and fully utilize its powerful image editing features.

## Application Process

To use the Midjourney Edits API, you first need to apply for the corresponding service on the [Midjourney Edits API](https://platform.acedata.cloud/documents/midjourney-edits) page. After entering the page, click the "Acquire" button, as shown in the image:

![Application Page](https://cdn.acedata.cloud/q6ytrc.png)

If you have not logged in or registered, you will be automatically redirected to the [login page](https://platform.acedata.cloud) inviting you to register and log in. After logging in or registering, you will be automatically returned to the current page.

There is a free quota available for first-time applicants, allowing you to use this API for free.

## Basic Usage

The basic usage involves passing an `image_url` with the link to the image you want to edit and a `prompt` describing the desired modification.

**Request Headers** include:

- `accept`: Specifies that the response should be in JSON format, set to `application/json`.
- `authorization`: The key to call the API, which can be selected directly from the dropdown after application.

**Request Body** includes:

- `prompt`: The text prompt describing the desired editing result (required). Example: `A cat sitting on a table`.
- `image_url`: The URL of the image to edit (required).
- `action`: The editing action. Default is `generate`.
- `mode`: The generation mode. Options: `fast`, `relax`, `turbo`.
- `mask`: An optional mask image URL specifying which area of the image to edit.
- `callback_url`: The URL to which the result will be sent upon completion (for async mode).
- `async`: Whether to use asynchronous mode. When `true`, the API returns a `task_id` immediately.
- `split_images`: Whether to split the generated 2×2 image grid into four individual images. Default is `false`.

### Code Example

#### CURL

```bash
curl -X POST 'https://api.acedata.cloud/midjourney/edits' \
-H 'accept: application/json' \
-H 'authorization: ******' \
-H 'content-type: application/json' \
-d '{
  "prompt": "A cat sitting on a table",
  "image_url": "https://example.com/source-image.png"
}'
```

#### Python

```python
import requests

url = "https://api.acedata.cloud/midjourney/edits"

headers = {
    "accept": "application/json",
    "authorization": "******",
    "content-type": "application/json"
}

payload = {
    "prompt": "A cat sitting on a table",
    "image_url": "https://example.com/source-image.png"
}

response = requests.post(url, json=payload, headers=headers)
print(response.text)
```

### Response Example

Upon successful request, the API will return the edited image information. For example:

```json
{
  "success": true,
  "task_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
  "image_id": "1234567890abcdef",
  "progress": 100,
  "image_url": "https://cdn.acedata.cloud/midjourney/result.png",
  "image_width": "2048",
  "image_height": "2048",
  "raw_image_url": "https://cdn.acedata.cloud/midjourney/result_raw.png",
  "raw_image_width": "2048",
  "raw_image_height": "2048",
  "actions": ["upsample1", "upsample2", "upsample3", "upsample4", "variation1", "variation2", "variation3", "variation4"]
}
```

The returned result contains multiple fields. The field descriptions are as follows:

- `success`: Whether the image editing task succeeded.
- `task_id`: The ID of the task, used to query the task status via the Tasks API.
- `image_id`: The ID of the generated image, used when performing follow-up actions.
- `progress`: The progress of the task (0–100).
- `image_url`: The URL of the edited image.
- `image_width`: The width of the edited image.
- `image_height`: The height of the edited image.
- `raw_image_url`: The URL of the original full-resolution edited image.
- `raw_image_width`: The width of the original image.
- `raw_image_height`: The height of the original image.
- `actions`: A list of follow-up actions available for the edited image.

## Asynchronous Callback

Since the Midjourney Edits API may take a relatively long time, the API supports asynchronous callbacks to avoid holding the HTTP connection open.

The overall flow is: the client specifies an additional `callback_url` field and sets `async` to `true` when making the request. The API immediately returns a result containing a `task_id` field. When the task completes, the edited image result is sent via POST JSON to the specified `callback_url`.

### Code Example

```bash
curl -X POST 'https://api.acedata.cloud/midjourney/edits' \
-H 'accept: application/json' \
-H 'authorization: ******' \
-H 'content-type: application/json' \
-d '{
  "prompt": "A cat sitting on a table",
  "image_url": "https://example.com/source-image.png",
  "async": true,
  "callback_url": "https://webhook.site/your-webhook-id"
}'
```

The API immediately returns:

```json
{
  "task_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890"
}
```

When the task completes, the full result is posted to your `callback_url`.

## Error Handling

When calling the API, if an error occurs, the API will return the corresponding error code and message. For example:

- `400 token_mismatched`: Bad request, possibly due to missing or invalid parameters.
- `400 api_not_implemented`: Bad request, possibly due to missing or invalid parameters.
- `401 invalid_token`: Unauthorized, invalid or missing authorization token.
- `403 forbidden`: Forbidden, you do not have permission to access this resource.
- `429 too_many_requests`: Too many requests, you have exceeded the rate limit.
- `500 api_error`: Internal server error, something went wrong on the server.
- `504 gateway_timeout`: Gateway timeout, the upstream service did not respond in time.

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

Through this document, you have learned how to use the Midjourney Edits API to edit images using a prompt and optional mask. We hope this document helps you integrate and use the API more effectively. If you have any questions, please feel free to contact our technical support team.
