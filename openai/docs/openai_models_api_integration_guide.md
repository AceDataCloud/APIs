# OpenAI Models API (`/openai/models`)

List the OpenAI-compatible models available to the current Ace Data Cloud application.

## Request

```bash
curl 'https://api.acedata.cloud/openai/models' \
  -H 'accept: application/json' \
  -H 'authorization: ******'
```

## Response

```json
{
  "object": "list",
  "data": [
    {
      "id": "gpt-6-astra",
      "object": "model",
      "created": 1700000000,
      "owned_by": "acedatacloud"
    }
  ]
}
```

`data` is the OpenAI-compatible model list. Responses may also include a `models` array with platform capabilities such as display names, reasoning levels, input modalities, tool support, and truncation policy. Use only entries whose `supported_in_api` value is `true`.

The endpoint returns `401` for an invalid token, `429` when rate-limited, and `500` for a service error.
