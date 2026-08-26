# OpenAI Models API Application and Usage

The OpenAI Models API lists the model identifiers currently available through Ace Data Cloud's OpenAI-compatible service. Use this endpoint before building model selectors or validating whether a model is enabled for API use.

## Application Process

Open the [Ace Data Cloud Console](https://platform.acedata.cloud/console/applications) and copy your API Token. A single API Token works across every service on the platform.

## Endpoint

```http
GET https://api.acedata.cloud/openai/models
```

## Request Headers

- `accept: application/json`
- `authorization: ******`

## Code Example

```bash
curl -X GET 'https://api.acedata.cloud/openai/models' \
  -H 'accept: application/json' \
  -H 'authorization: ******'
```

```python
import requests

url = "https://api.acedata.cloud/openai/models"
headers = {
    "accept": "application/json",
    "authorization": "******",
}

response = requests.get(url, headers=headers)
print(response.json())
```

## Response Example

```json
{
  "object": "list",
  "data": [
    {
      "id": "gpt-5.6-sol",
      "object": "model",
      "created": 1700000000,
      "owned_by": "acedatacloud"
    }
  ],
  "models": [
    {
      "slug": "gpt-5.6-sol",
      "display_name": "gpt-5.6-sol",
      "description": "Model description",
      "default_reasoning_level": "medium",
      "supported_reasoning_levels": [
        { "effort": "low", "description": "Low reasoning effort" },
        { "effort": "medium", "description": "Medium reasoning effort" },
        { "effort": "high", "description": "High reasoning effort" }
      ],
      "shell_type": "chat",
      "visibility": "list",
      "supported_in_api": true,
      "priority": 0,
      "availability_nux": null,
      "upgrade": null,
      "base_instructions": "",
      "support_verbosity": true,
      "default_verbosity": null,
      "apply_patch_tool_type": null,
      "truncation_policy": { "mode": "auto", "limit": 0 },
      "supports_parallel_tool_calls": true,
      "experimental_supported_tools": [],
      "input_modalities": ["text", "image"]
    }
  ]
}
```

## Field Descriptions

- `object`: Always `list` for the model list response.
- `data`: OpenAI-compatible model list. Each item includes `id`, `object`, `created`, and `owned_by`.
- `models`: Ace Data Cloud model metadata, including display name, reasoning levels, visibility, API availability, verbosity support, truncation policy, parallel tool-call support, experimental tools, and supported input modalities.

## Error Handling

If the token is invalid or the request fails, the API returns an error object with an `error.code`, `error.message`, and `trace_id`.
