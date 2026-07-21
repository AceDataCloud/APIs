# Midjourney Translate API Integration Guide

The Midjourney Translate API translates non-English text into an English prompt suitable for use with Midjourney image generation.

This document provides detailed integration instructions for the Midjourney Translate API.

## Application Process

To use the Midjourney Translate API, you first need to apply for the corresponding service on the [Midjourney Translate API](https://platform.acedata.cloud/documents/midjourney-translate) page. After entering the page, click the "Acquire" button, as shown in the image:

![Application Page](https://cdn.acedata.cloud/q6ytrc.png)

If you have not logged in or registered, you will be automatically redirected to the [login page](https://platform.acedata.cloud) inviting you to register and log in. After logging in or registering, you will be automatically returned to the current page.

There is a free quota available for first-time applicants, allowing you to use this API for free.

## Basic Usage

The basic usage involves passing a `content` field with the non-English text you want to translate into a Midjourney-compatible English prompt.

**Request Headers** include:

- `accept`: Specifies that the response should be in JSON format, set to `application/json`.
- `authorization`: The key to call the API, which can be selected directly from the dropdown after application.

**Request Body** includes:

- `content`: The non-English text to translate (required). Example: `精致，无暇，洁白的天使`.

### Code Example

#### CURL

```bash
curl -X POST 'https://api.acedata.cloud/midjourney/translate' \
-H 'accept: application/json' \
-H 'authorization: ******' \
-H 'content-type: application/json' \
-d '{
  "content": "精致，无暇，洁白的天使"
}'
```

#### Python

```python
import requests

url = "https://api.acedata.cloud/midjourney/translate"

headers = {
    "accept": "application/json",
    "authorization": "******",
    "content-type": "application/json"
}

payload = {
    "content": "精致，无暇，洁白的天使"
}

response = requests.post(url, json=payload, headers=headers)
print(response.text)
```

### Response Example

Upon successful request, the API will return the translated English prompt. For example:

```json
{
  "content": "delicate, flawless, pure white angel"
}
```

The returned result contains the following field:

- `content`: The translated English prompt, ready to be used directly with the Midjourney Imagine API.

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

Through this document, you have learned how to use the Midjourney Translate API to convert non-English text into Midjourney-compatible English prompts. We hope this document helps you integrate and use the API more effectively. If you have any questions, please feel free to contact our technical support team.
