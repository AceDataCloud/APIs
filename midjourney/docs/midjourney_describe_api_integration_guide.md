# Midjourney Describe API Integration Guide

The Midjourney Describe API analyses an uploaded image and returns a set of descriptive text prompts that can be used to recreate or inspire similar images with Midjourney.

This document provides detailed integration instructions for the Midjourney Describe API.

## Application Process

To use the Midjourney Describe API, you first need to apply for the corresponding service on the [Midjourney Describe API](https://platform.acedata.cloud/documents/midjourney-describe) page. After entering the page, click the "Acquire" button, as shown in the image:

![Application Page](https://cdn.acedata.cloud/q6ytrc.png)

If you have not logged in or registered, you will be automatically redirected to the [login page](https://platform.acedata.cloud) inviting you to register and log in. After logging in or registering, you will be automatically returned to the current page.

There is a free quota available for first-time applicants, allowing you to use this API for free.

## Basic Usage

The basic usage involves passing an `image_url` with the URL of the image you want to describe.

**Request Headers** include:

- `accept`: Specifies that the response should be in JSON format, set to `application/json`.
- `authorization`: The key to call the API, which can be selected directly from the dropdown after application.

**Request Body** includes:

- `image_url`: The URL of the image to describe (required).

### Code Example

#### CURL

```bash
curl -X POST 'https://api.acedata.cloud/midjourney/describe' \
-H 'accept: application/json' \
-H 'authorization: ******' \
-H 'content-type: application/json' \
-d '{
  "image_url": "https://example.com/image.png"
}'
```

#### Python

```python
import requests

url = "https://api.acedata.cloud/midjourney/describe"

headers = {
    "accept": "application/json",
    "authorization": "******",
    "content-type": "application/json"
}

payload = {
    "image_url": "https://example.com/image.png"
}

response = requests.post(url, json=payload, headers=headers)
print(response.text)
```

### Response Example

Upon successful request, the API will return a list of descriptive prompts for the image. For example:

```json
{
  "descriptions": [
    "a white fluffy cat sitting on a wooden table, bright natural lighting, photorealistic, 4k",
    "white cat resting on a table indoors, cozy atmosphere, soft bokeh background",
    "close-up of a white domestic cat on a table, sharp eyes, natural daylight",
    "white cat portrait on a wooden surface, high detail photography, studio lighting"
  ]
}
```

The returned result contains the following fields:

- `descriptions`: An array of text prompt strings that describe the content and style of the uploaded image. Each description can be used directly as a prompt for the Midjourney Imagine API to generate similar images.

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

Through this document, you have learned how to use the Midjourney Describe API to obtain descriptive prompts for an image. These prompts can be used to recreate or inspire similar Midjourney generations. We hope this document helps you integrate and use the API more effectively. If you have any questions, please feel free to contact our technical support team.
