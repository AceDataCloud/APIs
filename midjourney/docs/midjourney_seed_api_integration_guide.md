# Midjourney Seed API Integration Guide

The Midjourney Seed API retrieves the seed value associated with a previously generated Midjourney image. The seed value can be used to reproduce or slightly vary the same image in future generation requests.

This document provides detailed integration instructions for the Midjourney Seed API.

## Application Process

To use the Midjourney Seed API, you first need to apply for the corresponding service on the [Midjourney Seed API](https://platform.acedata.cloud/documents/midjourney-seed) page. After entering the page, click the "Acquire" button, as shown in the image:

![Application Page](https://cdn.acedata.cloud/q6ytrc.png)

If you have not logged in or registered, you will be automatically redirected to the [login page](https://platform.acedata.cloud) inviting you to register and log in. After logging in or registering, you will be automatically returned to the current page.

There is a free quota available for first-time applicants, allowing you to use this API for free.

## Basic Usage

The basic usage involves passing an `image_id` field with the ID of the generated image whose seed you want to retrieve.

**Request Headers** include:

- `accept`: Specifies that the response should be in JSON format, set to `application/json`.
- `authorization`: The key to call the API, which can be selected directly from the dropdown after application.

**Request Body** includes:

- `image_id`: The ID of the previously generated Midjourney image (required). This ID is returned in the `image_id` field of the Midjourney Imagine API response.

### Code Example

#### CURL

```bash
curl -X POST 'https://api.acedata.cloud/midjourney/seed' \
-H 'accept: application/json' \
-H 'authorization: ******' \
-H 'content-type: application/json' \
-d '{
  "image_id": "1234567890abcdef"
}'
```

#### Python

```python
import requests

url = "https://api.acedata.cloud/midjourney/seed"

headers = {
    "accept": "application/json",
    "authorization": "******",
    "content-type": "application/json"
}

payload = {
    "image_id": "1234567890abcdef"
}

response = requests.post(url, json=payload, headers=headers)
print(response.text)
```

### Response Example

Upon successful request, the API will return the seed value for the specified image. For example:

```json
{
  "seed": "3748291650"
}
```

The returned result contains the following field:

- `seed`: The seed value of the generated image. This value can be used in the Midjourney Imagine API with the `--seed` parameter to reproduce or create variations of the same image.

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

Through this document, you have learned how to use the Midjourney Seed API to retrieve the seed value of a generated image. We hope this document helps you integrate and use the API more effectively. If you have any questions, please feel free to contact our technical support team.
