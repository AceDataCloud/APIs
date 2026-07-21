# Midjourney Shorten API Integration Guide

The Midjourney Shorten API analyses a long prompt and returns a set of concise alternative prompts, helping you identify the most impactful words and shorten your prompts for better results.

This document provides detailed integration instructions for the Midjourney Shorten API.

## Application Process

To use the Midjourney Shorten API, you first need to apply for the corresponding service on the [Midjourney Shorten API](https://platform.acedata.cloud/documents/midjourney-shorten) page. After entering the page, click the "Acquire" button, as shown in the image:

![Application Page](https://cdn.acedata.cloud/q6ytrc.png)

If you have not logged in or registered, you will be automatically redirected to the [login page](https://platform.acedata.cloud) inviting you to register and log in. After logging in or registering, you will be automatically returned to the current page.

There is a free quota available for first-time applicants, allowing you to use this API for free.

## Basic Usage

The basic usage involves passing a `prompt` field with the long prompt you want to shorten.

**Request Headers** include:

- `accept`: Specifies that the response should be in JSON format, set to `application/json`.
- `authorization`: The key to call the API, which can be selected directly from the dropdown after application.

**Request Body** includes:

- `prompt`: The long text prompt to shorten (required).

### Code Example

#### CURL

```bash
curl -X POST 'https://api.acedata.cloud/midjourney/shorten' \
-H 'accept: application/json' \
-H 'authorization: ******' \
-H 'content-type: application/json' \
-d '{
  "prompt": "a beautiful and majestic white fluffy cat with bright blue eyes sitting gracefully on an old rustic wooden table in a warmly lit cozy kitchen with morning sunlight streaming through the window"
}'
```

#### Python

```python
import requests

url = "https://api.acedata.cloud/midjourney/shorten"

headers = {
    "accept": "application/json",
    "authorization": "******",
    "content-type": "application/json"
}

payload = {
    "prompt": "a beautiful and majestic white fluffy cat with bright blue eyes sitting gracefully on an old rustic wooden table in a warmly lit cozy kitchen with morning sunlight streaming through the window"
}

response = requests.post(url, json=payload, headers=headers)
print(response.text)
```

### Response Example

Upon successful request, the API will return a list of shortened prompt alternatives. For example:

```json
{
  "prompts": [
    "white fluffy cat, blue eyes, rustic wooden table, morning sunlight, cozy kitchen",
    "majestic white cat sitting on wooden table, warm morning light",
    "white cat, old table, kitchen, sunlight streaming through window",
    "fluffy white cat, blue eyes, cozy kitchen, morning light",
    "white cat on rustic table, morning sunlight, warm atmosphere"
  ]
}
```

The returned result contains the following fields:

- `prompts`: An array of shortened prompt strings derived from the original long prompt. Each shortened prompt retains the key descriptive elements and can be used directly with the Midjourney Imagine API.

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

Through this document, you have learned how to use the Midjourney Shorten API to condense long prompts into concise alternatives. We hope this document helps you integrate and use the API more effectively. If you have any questions, please feel free to contact our technical support team.
