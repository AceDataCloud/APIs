# OpenAI Models API Integration and Usage

The OpenAI Models API lists the OpenAI-compatible model IDs currently available through Ace Data Cloud.

## Endpoint

```text
GET https://api.acedata.cloud/openai/models
```

Use your Ace Data Cloud API token in the `Authorization` header.

## CURL Code Example

```bash
curl --request GET "https://api.acedata.cloud/openai/models" \
  --header "Authorization: ******" \
  --header "Accept: application/json"
```

## Response Example

```json
{
  "object": "list",
  "data": [
    {
      "id": "gpt-4o",
      "object": "model",
      "created": 1714500000,
      "owned_by": "system"
    },
    {
      "id": "gpt-4o-mini",
      "object": "model",
      "created": 1714500000,
      "owned_by": "system"
    },
    {
      "id": "claude-sonnet-4-5",
      "object": "model",
      "created": 1714500000,
      "owned_by": "system"
    }
  ]
}
```

Each item includes the model `id`, object type, creation timestamp, and owner. Use the returned `id` in compatible chat, responses, image, embedding, audio, or realtime requests as appropriate.
