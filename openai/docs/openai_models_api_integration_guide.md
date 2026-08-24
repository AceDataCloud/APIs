The OpenAI Models API returns the models currently available through the Ace Data Cloud OpenAI-compatible service.

## Authentication

Send your Ace Data Cloud API Token with HTTP bearer authentication.

```http
Authorization: ******
Accept: application/json
```

## List Models

```bash
curl --request GET 'https://api.acedata.cloud/openai/models' \
  --header 'Authorization: ******' \
  --header 'Accept: application/json'
```

The response is an OpenAI-compatible model list:

```json
{
  "object": "list",
  "data": [
    {
      "id": "gpt-5.5",
      "object": "model",
      "created": 0,
      "owned_by": "acedata"
    }
  ]
}
```

Use a returned `data[].id` as the `model` value for a compatible API.

## Errors

- `401`: Missing or invalid API Token.
- `429`: Rate limit exceeded.
- `500`: Internal service error.
