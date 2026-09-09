# Claude Messages Count Tokens API Application and Usage

The Claude Messages Count Tokens API can calculate the input token count of a message without actually creating the message, including the token count of tools, images, and documents. This is very useful when estimating costs or checking if the input exceeds the model's context limits.

This document mainly describes the usage process of the Claude Messages Count Tokens API.

## Application Process

Open the [Ace Data Cloud application list](https://platform.acedata.cloud/console/applications), access an application, and copy its API key. The same key works across Ace Data Cloud services, and usage is deducted from the application's shared balance.

## Basic Usage

The request path for the Claude Messages Count Tokens API is `/v1/messages/count_tokens`, consistent with the official Anthropic API. We need to provide at least two required parameters:

- `model`: Use the latest flagship `claude-fable-5-1`; the earlier `claude-fable-5` remains compatible.
- `messages`: An array of input messages, each containing `role` and `content`.

Common optional parameters:

- `system`: System prompt, which will be included in the token count.
- `tools`: Tool definitions, which will be included in the token count.
- `tool_choice`: Tool selection configuration.
- `thinking`: Extended thinking configuration.
- `cache_control`: Prompt cache configuration.

Multimodal content and tool structures follow the Claude Messages API request format.

### cURL Example

```bash
curl -X POST 'https://api.acedata.cloud/v1/messages/count_tokens' \
  -H 'accept: application/json' \
  -H 'authorization: Bearer {token}' \
  -H 'content-type: application/json' \
  -d '{
    "model": "claude-fable-5-1",
    "messages": [
      {
        "role": "user",
        "content": "Hello, Claude"
      }
    ]
  }'
```

### Python Example

```python
import httpx

url = "https://api.acedata.cloud/v1/messages/count_tokens"
headers = {
    "accept": "application/json",
    "authorization": "Bearer {token}",
    "content-type": "application/json",
}
payload = {
    "model": "claude-fable-5-1",
    "messages": [
        {
            "role": "user",
            "content": "Hello, Claude"
        }
    ],
}
response = httpx.post(url, headers=headers, json=payload)
print(response.json())
```

Example of return result:

```json
{
  "input_tokens": 11
}
```

### Using Anthropic SDK

The endpoint can be called with the official Anthropic SDK, but Ace Data Cloud currently returns a local token estimate rather than an official tokenizer result.

```python
from anthropic import Anthropic

client = Anthropic(
    api_key="{token}",
    base_url="https://api.acedata.cloud",
)

result = client.messages.count_tokens(
    model="claude-opus-4-8",
    messages=[
        {
            "role": "user",
            "content": "Hello, Claude"
        }
    ],
)
print(result.input_tokens)
```

## Token Count Including Tools

If your request includes tool definitions, these tools will also be included in the token count:

```python
result = client.messages.count_tokens(
    model="claude-opus-4-8",
    messages=[
        {
            "role": "user",
            "content": "What is the weather in San Francisco?"
        }
    ],
    tools=[
        {
            "name": "get_weather",
            "description": "Get the current weather in a given location",
            "input_schema": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "The city and state, e.g. San Francisco, CA"
                    }
                },
                "required": ["location"]
            }
        }
    ],
)
print(result.input_tokens)
```

## Token Count Including System Prompts

System prompts will also be included in the token count:

```python
result = client.messages.count_tokens(
    model="claude-opus-4-8",
    system="You are a helpful assistant that speaks Chinese.",
    messages=[
        {
            "role": "user",
            "content": "Hello"
        }
    ],
)
print(result.input_tokens)
```

## Notes

- This API only calculates the input token count and does not produce any model output.
- The result is a rough local estimate and is not suitable for billing, context-limit enforcement, or tokenizer comparisons.
- Visual and PDF token estimates may differ substantially from actual model usage.
