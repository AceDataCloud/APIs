# Midjourney Shorten API Integration and Usage

The Midjourney Shorten API integrates Midjourney's official `/shorten` prompt-analysis command. It analyzes a prompt, keeps the highest-weighted keywords, and returns up to 5 concise prompt candidates.

This API is useful when you want to:

- shorten long prompts before calling `imagine` to improve generation relevance;
- understand how Midjourney weighs tokens for prompt engineering;
- normalize and simplify user prompts in automated pipelines.

## Application Process

To use the Midjourney Shorten API, first apply for the service on the [Midjourney Shorten API](https://platform.acedata.cloud/documents/f0c6be1d-c084-43ac-bde6-44ef9cf824a2) page, then click the "Acquire" button.

If you are not logged in or registered, you will be automatically redirected to the [login page](https://platform.acedata.cloud). After login/registration, you will be returned to the current page.

First-time applicants receive a free quota, so you can try the API at no cost.

## Request Example

Let's use a long prompt as an example to demonstrate how to analyze and shorten it.

### Setting Request Headers and Request Body

**Request Headers** include:

- `accept`: Specifies JSON response format, set to `application/json`.
- `authorization`: The API token used for authentication.

**Request Body** includes:

- `prompt`: The prompt text to analyze and shorten (English prompt text is recommended).

### Code Example

#### CURL

```bash
curl -X POST 'https://api.acedata.cloud/midjourney/shorten' \
-H 'accept: application/json' \
-H 'authorization: Bearer {token}' \
-H 'content-type: application/json' \
-d '{
  "prompt": "a serene mountain lake at sunrise, mist rising from the water, towering pine trees on the shore, golden hour lighting, ultra detailed, cinematic, 35mm film photography style, masterpiece --ar 16:9 --v 6"
}'
```

#### Python

```python
import requests

url = "https://api.acedata.cloud/midjourney/shorten"

headers = {
    "accept": "application/json",
    "authorization": "Bearer {token}",
    "content-type": "application/json"
}

payload = {
    "prompt": (
        "a serene mountain lake at sunrise, mist rising from the water, "
        "towering pine trees on the shore, golden hour lighting, ultra "
        "detailed, cinematic, 35mm film photography style, masterpiece "
        "--ar 16:9 --v 6"
    )
}

response = requests.post(url, json=payload, headers=headers)
print(response.json())
```

### Response Example

After a successful request, the API returns up to 5 shortened candidate prompts:

```json
{
  "prompts": [
    "a serene mountain lake at sunrise, mist rising from the water, golden hour lighting --ar 16:9",
    "mountain lake sunrise with mist, golden light --ar 16:9 --v 6",
    "tranquil alpine lake, dawn mist, warm golden tones, cinematic --ar 16:9",
    "sunrise over a misty mountain lake, rich golden hour photography --ar 16:9 --style raw",
    "misty lake at dawn, mountains in background, golden sunrise --ar 16:9"
  ]
}
```

The response contains a `prompts` field with shortened prompt candidates. Each candidate keeps the most important weighted tokens while removing redundant wording.

## Error Handling

If an error occurs, the API returns a corresponding error code and message, for example:

- `400 token_mismatched`: The specified token does not match this API.
- `400 api_not_implemented`: The API is not implemented for the current context.
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

You can use Midjourney Shorten API to analyze long prompts and produce concise candidate prompts before generation. For better results, combine it with the Midjourney Imagine API workflow.
