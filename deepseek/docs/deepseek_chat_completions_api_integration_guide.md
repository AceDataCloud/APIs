# DeepSeek Chat Completions API Integration Guide

The DeepSeek Chat Completions API provides OpenAI-compatible chat completions for DeepSeek models on Ace Data Cloud.

## Application Process

To use the DeepSeek Chat Completions API, visit the [DeepSeek API](https://platform.acedata.cloud/service/deepseek) page and click the "Acquire" button.

First-time applicants receive a free usage quota. Use the API token from [https://platform.acedata.cloud](https://platform.acedata.cloud) as the `Authorization` header.

## Basic Usage

Send a request with the required `model` and `messages` fields.

```shell
curl -X POST 'https://api.acedata.cloud/deepseek/chat/completions' \
-H 'accept: application/json' \
-H 'authorization: ******' \
-H 'content-type: application/json' \
-d '{
  "model": "deepseek-v3",
  "messages": [{"role": "user", "content": "Hello"}]
}'
```

Python equivalent:

```python
import requests

url = "https://api.acedata.cloud/deepseek/chat/completions"
headers = {
    "accept": "application/json",
    "authorization": "******",
    "content-type": "application/json"
}
payload = {
    "model": "deepseek-v3",
    "messages": [{"role": "user", "content": "Hello"}]
}

response = requests.post(url, json=payload, headers=headers)
print(response.text)
```

A successful response follows the chat-completion schema:

```json
{
  "id": "chatcmpl-example",
  "model": "deepseek-v3",
  "object": "chat.completion",
  "created": 1765706120,
  "choices": [
    {
      "index": 0,
      "message": {
        "role": "assistant",
        "content": "Hello! How can I help you today?"
      },
      "finish_reason": "stop"
    }
  ],
  "usage": {
    "prompt_tokens": 8,
    "completion_tokens": 10,
    "total_tokens": 18
  }
}
```

## Request Headers

| Header | Description |
| --- | --- |
| `accept` | `application/json` |
| `authorization` | API token from your Ace Data Cloud account |
| `content-type` | `application/json` |

## Request Body

| Field | Type | Required | Description |
| --- | --- | --- | --- |
| `model` | string | ✅ | DeepSeek model to use |
| `messages` | array | ✅ | Chat messages. Each message requires a `role`; `content` can be text or multimodal parts |
| `n` | number | ❌ | Number of candidate responses, from `1` to `128`; defaults to `1` |
| `stream` | boolean | ❌ | Stream response chunks; defaults to `false` |
| `max_tokens` | number | ❌ | Maximum tokens in the response |
| `temperature` | number | ❌ | Sampling temperature from `0` to `2`; defaults to `1` |
| `response_format` | object | ❌ | Response format: `text`, `json_object`, or `json_schema` |
| `top_p` | number | ❌ | Nucleus sampling value from `0` to `1`; defaults to `1` |
| `frequency_penalty` | number | ❌ | Frequency penalty from `-2` to `2`; defaults to `0` |
| `presence_penalty` | number | ❌ | Presence penalty from `-2` to `2`; defaults to `0` |
| `seed` | integer | ❌ | Seed for deterministic sampling where supported |
| `stop` | string or array | ❌ | Stop sequence, or up to four stop sequences |
| `max_completion_tokens` | integer | ❌ | Maximum completion tokens |
| `logprobs` | boolean | ❌ | Whether to return log probabilities; defaults to `false` |
| `top_logprobs` | integer | ❌ | Number of top log probabilities to return, from `0` to `20` |
| `stream_options` | object | ❌ | Streaming options such as `include_usage` |
| `parallel_tool_calls` | boolean | ❌ | Enable parallel tool calls; defaults to `true` |
| `user` | string | ❌ | End-user identifier |
| `reasoning_effort` | string | ❌ | Reasoning effort: `minimal`, `low`, `medium`, or `high`; defaults to `medium` |
| `service_tier` | string | ❌ | Service tier: `auto`, `default`, `flex`, `scale`, or `priority`; defaults to `auto` |
| `store` | boolean | ❌ | Whether to store the output; defaults to `false` |
| `metadata` | object | ❌ | String metadata key-value pairs |
| `logit_bias` | object | ❌ | Token bias map |
| `modalities` | array | ❌ | Output modalities: `text` or `audio` |
| `audio` | object | ❌ | Audio output settings with `voice` and `format` |
| `prediction` | object | ❌ | Static predicted output content |
| `web_search_options` | object | ❌ | Search context and approximate user location options |
| `tools` | array | ❌ | Function tools available to the model |
| `tool_choice` | string or object | ❌ | Tool choice: `none`, `auto`, `required`, or a specific function |

### Supported Models

`deepseek-r1`, `deepseek-r1-0528`, `deepseek-v3`, `deepseek-v3-250324`, `deepseek-v3.2-exp`, `deepseek-v4-flash`, `deepseek-v4-pro`

### Messages

Each message requires a `role` with one of `user`, `assistant`, `system`, `developer`, or `tool`. The `content` field can be a string or an array of parts. Supported parts include text and image URL objects:

```json
{
  "role": "user",
  "content": [
    {"type": "text", "text": "Describe this image"},
    {"type": "image_url", "image_url": {"url": "https://cdn.acedata.cloud/ht05g0.png", "detail": "auto"}}
  ]
}
```

## Streaming Response

Set `stream` to `true` to receive streaming chat-completion chunks.

```shell
curl -X POST 'https://api.acedata.cloud/deepseek/chat/completions' \
-H 'accept: application/json' \
-H 'authorization: ******' \
-H 'content-type: application/json' \
-d '{
  "model": "deepseek-v3",
  "messages": [{"role": "user", "content": "Hello"}],
  "stream": true
}'
```

## Tool Calls

Provide function tools with the `tools` field and control selection with `tool_choice`.

```json
{
  "model": "deepseek-v3",
  "messages": [{"role": "user", "content": "What is the weather?"}],
  "tools": [
    {
      "type": "function",
      "function": {
        "name": "get_weather",
        "description": "Get weather for a city",
        "parameters": {
          "type": "object",
          "properties": {
            "city": {"type": "string"}
          },
          "required": ["city"]
        }
      }
    }
  ],
  "tool_choice": "auto"
}
```

## Response Schema

### Success (200)

| Field | Type | Description |
| --- | --- | --- |
| `id` | string | Chat completion ID |
| `model` | string | Model used for the response |
| `object` | string | `chat.completion` |
| `choices` | array | Candidate responses with `index`, `message`, and `finish_reason` |
| `created` | number | Creation timestamp |
| `system_fingerprint` | string | System fingerprint, when available |
| `usage` | object | Token usage details |

### Error (400 / 401 / 429 / 500)

The API returns a JSON error object for invalid requests, authentication failures, rate limits, or server errors. Use the response status and any returned error details for troubleshooting.
