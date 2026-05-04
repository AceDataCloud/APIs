# Midjourney Seed API Integration and Usage

The main function of the Midjourney Seed API is to retrieve the seed value of a generated image by providing its image ID. The seed is a number that controls the randomness of the image generation process — knowing the seed of an image allows you to reproduce similar results in future generations.

This document will provide a detailed introduction to the integration instructions for the Midjourney Seed API, helping you easily integrate and fully utilize the powerful features of this API. With the Midjourney Seed API, you can retrieve seed values from previously generated images and use them to produce reproducible or similar images.

## Application Process

To use the Midjourney Seed API, you need to first apply for the corresponding service on the application page [Midjourney Imagine API](https://platform.acedata.cloud/documents/e52c028d-897a-4d51-b110-60fccbe6118d). After entering the page, click the "Acquire" button, as shown in the image below:

![Application Page](https://cdn.acedata.cloud/nyq0xz.png)

If you are not logged in or registered, you will be automatically redirected to the [login page](https://platform.acedata.cloud) inviting you to register and log in. After logging in or registering, you will be automatically returned to the current page.

There is a free quota available for first-time applicants, allowing you to use the API for free.

## Request Example

To use this API, you need to have the image ID of a previously generated image. You can obtain the `image_id` from the response of the [Midjourney Imagine API](https://platform.acedata.cloud/documents/e52c028d-897a-4d51-b110-60fccbe6118d).

### Setting Request Headers and Request Body

**Request Headers** include:

- `accept`: Specifies that the response should be in JSON format, set to `application/json`.
- `authorization`: The key to call the API, which can be selected directly after application.

**Request Body** includes:

- `image_id`: The ID of the image whose seed you want to retrieve.

### Code Example

Some code examples are as follows:

#### CURL

```bash
curl -X POST 'https://api.acedata.cloud/midjourney/seed' \
-H 'accept: application/json' \
-H 'authorization: Bearer {token}' \
-H 'content-type: application/json' \
-d '{
  "image_id": "1234197197067915365"
}'
```

#### Python

```python
import requests

url = "https://api.acedata.cloud/midjourney/seed"

headers = {
    "accept": "application/json",
    "authorization": "Bearer {token}",
    "content-type": "application/json"
}

payload = {
    "image_id": "1234197197067915365"
}

response = requests.post(url, json=payload, headers=headers)
print(response.json())
```

### Response Example

After a successful request, the API will return the seed information for the image. For example:

```json
{
  "seed": "3849571023"
}
```

As you can see, the result contains a `seed` field, which includes the seed value associated with the image. This seed value can be used in future generation requests with the `--seed` parameter in the prompt to reproduce similar images.

- `seed`: The seed value of the specified image, which can be referenced in future prompts using the `--seed` flag.

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

Through this document, you have learned how to use the Midjourney Seed API to retrieve the seed value of a generated image. We hope this document helps you better integrate and use this API. If you have any questions, please feel free to contact our technical support team.
