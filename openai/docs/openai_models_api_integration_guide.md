# OpenAI Models API Application and Usage

The OpenAI Models API lists the OpenAI-compatible models available through Ace Data Cloud.

## Application Process

Use an Ace Data Cloud API token from the [console](https://platform.acedata.cloud/console/applications). Send the token in the `Authorization` header.

## Endpoint

```text
GET https://api.acedata.cloud/openai/models
```

## Request Headers

| Header | Required | Description |
| --- | --- | --- |
| `Authorization` | Yes | Ace Data Cloud API token. |
| `accept` | No | Use `application/json`. |

## Basic Usage

```shell
curl -X GET "https://api.acedata.cloud/openai/models" \
  -H "Authorization: ******" \
  -H "accept: application/json"
```

```python
import requests

url = "https://api.acedata.cloud/openai/models"
headers = {
    "accept": "application/json",
    "authorization": "******",
}

response = requests.get(url, headers=headers)
print(response.text)
```

## Response

A successful request returns a JSON list of available models. Authentication failures return `401`, rate limits return `429`, and server errors return `500`.

## Conclusion

Use this endpoint to discover the current model IDs before calling chat, responses, image, audio, or realtime APIs.
