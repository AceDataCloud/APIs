# Claude Messages API Application and Usage

Anthropic Claude is a very powerful AI dialogue system that can generate smooth and natural replies in just a few seconds by inputting prompts. The Claude Messages API is the official native API format from Anthropic, which differs from the OpenAI compatible format (Chat Completion) by adopting Anthropic's own request and response structure, allowing better utilization of Claude's unique capabilities, such as multimodal content input, tool invocation, and advanced features like Extended Thinking.

This document mainly introduces the usage process of the Claude Messages API, allowing us to use the native interface consistent with Anthropic's official standards to invoke Claude's dialogue capabilities.

## Application Process

Open the [Ace Data Cloud application list](https://platform.acedata.cloud/console/applications), access an application, and copy its API key:

![](https://cdn.acedata.cloud/5hmkdg.jpg)

The same API key works across Ace Data Cloud services, and usage is deducted from the application's shared balance.

## Basic Usage

The request path for the Claude Messages API is `/v1/messages`, consistent with the Anthropic official API. We need to provide at least three required parameters:

- `model`: Choose the Claude model to use. The current lineup leads with `claude-fable-5-1` (1M-token context and up to 128K output tokens), while `claude-fable-5`, `claude-opus-5`, `claude-opus-4-8` and `claude-sonnet-5` remain available; older releases such as `claude-opus-4-20250514` and `claude-sonnet-4-20250514` remain available.
- `messages`: An array of input messages, each containing `role` (role) and `content` (content), where `role` supports `user` and `assistant`.
- `max_tokens`: The maximum number of output tokens, used to limit the length of a single reply.

Common optional parameters:

- `system`: System prompt used to set the model's behavior and role.
- `temperature`: Generation randomness, between 0-1, with higher values resulting in more diverse replies.
- `stream`: Whether to use streaming responses; set to `true` for a word-by-word return effect.
- `stop_sequences`: Custom stop sequences; the model will stop generating when encountering these texts.
- `top_p`: Nucleus sampling parameter, used in conjunction with temperature to control generation randomness.
- `top_k`: Sample only from the top K options with the highest probabilities.
- `tools`: Tool definitions for allowing the model to invoke external functions.
- `tool_choice`: Controls how the model uses the provided tools.
- `cache_control`: Configures prompt caching at the last cacheable block.

### cURL Example

```bash
curl -X POST 'https://api.acedata.cloud/v1/messages' \
  -H 'accept: application/json' \
  -H 'authorization: Bearer {token}' \
  -H 'content-type: application/json' \
  -d '{
    "model": "claude-fable-5-1",
    "max_tokens": 1024,
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
import requests

url = "https://api.acedata.cloud/v1/messages"

headers = {
    "accept": "application/json",
    "authorization": "Bearer {token}",
    "content-type": "application/json"
}

payload = {
    "model": "claude-fable-5-1",
    "max_tokens": 1024,
    "messages": [
        {"role": "user", "content": "Hello, Claude"}
    ]
}

response = requests.post(url, json=payload, headers=headers)
print(response.json())
```

After the call, the returned result is as follows:

```json
{
  "id": "msg_013Zva2CMHLNnXjNJJKqJ2EF",
  "type": "message",
  "role": "assistant",
  "content": [
    {
      "type": "text",
      "text": "Hi! My name is Claude. How can I help you today?"
    }
  ],
  "model": "claude-opus-4-8",
  "stop_reason": "end_turn",
  "stop_sequence": null,
  "usage": {
    "input_tokens": 12,
    "output_tokens": 15
  }
}
```

Returned result field descriptions:

- `id`: The unique identifier for this message.
- `type`: Always `message`.
- `role`: Always `assistant`.
- `content`: An array of reply content, with each element containing `type` (e.g., `text`) and corresponding content.
- `model`: The name of the model processing the request.
- `stop_reason`: The reason for stopping. Values include `end_turn`, `max_tokens`, `stop_sequence`, `tool_use`, `pause_turn`, `refusal`, and `model_context_window_exceeded`.
- `stop_details`: Additional structured details about why generation stopped, when available.
- `stop_sequence`: If stopped due to a custom stop sequence, displays the matching stop sequence text.
- `usage`: Token and cost statistics, including `input_tokens`, `output_tokens`, `cache_creation_input_tokens`, `cache_read_input_tokens`, and `cost`.

## System Prompt

The Claude Messages API supports setting a system prompt through the `system` field, used to define the model's behavior, role, and context.

### Python Example

```python
import requests

url = "https://api.acedata.cloud/v1/messages"

headers = {
    "accept": "application/json",
    "authorization": "Bearer {token}",
    "content-type": "application/json"
}

payload = {
    "model": "claude-sonnet-4-20250514",
    "max_tokens": 1024,
    "system": "You are a professional Chinese translation assistant. Please translate the user's input from English to Chinese.",
    "messages": [
        {"role": "user", "content": "The quick brown fox jumps over the lazy dog."}
    ]
}

response = requests.post(url, json=payload, headers=headers)
print(response.json())
```

By setting the `system` prompt, you can precisely control Claude's role and behavior.

## Streaming Response

This interface also supports streaming responses; setting the `stream` parameter to `true` will provide a step-by-step return effect, which is very suitable for implementing word-by-word display on a webpage.

### Python Example

```python
import requests

url = "https://api.acedata.cloud/v1/messages"

headers = {
    "accept": "application/json",
    "authorization": "Bearer {token}",
    "content-type": "application/json"
}

payload = {
    "model": "claude-sonnet-4-20250514",
    "max_tokens": 1024,
    "stream": True,
    "messages": [
        {"role": "user", "content": "Hello, Claude"}
    ]
}

response = requests.post(url, json=payload, headers=headers, stream=True)
for line in response.iter_lines():
    if line:
        print(line.decode("utf-8"))
```

Streaming responses are returned in Server-Sent Events (SSE) format, with each line prefixed by `event:` and `data:`. Streaming event types include:

- `message_start`: Message start, containing basic information about the message and model name.
- `content_block_start`: Content block start.
- `content_block_delta`: Content block incremental update, containing newly generated text segments.
- `content_block_stop`: Content block end.
- `message_delta`: Message-level incremental update, containing `stop_reason` and final `usage` information.
- `message_stop`: Message end.

The output effect is as follows:
```
event: message_start
data: {"type":"message_start","message":{"id":"msg_01XFDUDYJgAACzvnptvVoYEL","type":"message","role":"assistant","content":[],"model":"claude-sonnet-4-20250514","stop_reason":null,"stop_sequence":null,"usage":{"input_tokens":12,"output_tokens":0}}}

event: content_block_start
data: {"type":"content_block_start","index":0,"content_block":{"type":"text","text":""}}

event: content_block_delta
data: {"type":"content_block_delta","index":0,"delta":{"type":"text_delta","text":"Hi"}}

event: content_block_delta
data: {"type":"content_block_delta","index":0,"delta":{"type":"text_delta","text":"! My name is"}}

event: content_block_delta
data: {"type":"content_block_delta","index":0,"delta":{"type":"text_delta","text":" Claude. How can I help you today?"}}

event: content_block_stop
data: {"type":"content_block_stop","index":0}

event: message_delta
data: {"type":"message_delta","delta":{"stop_reason":"end_turn","stop_sequence":null},"usage":{"output_tokens":15}}

event: message_stop
data: {"type":"message_stop"}
```

You can see that the `content_block_delta` events in the streaming response contain the progressively generated text content, and by concatenating all `text_delta`, you can obtain the complete reply.

### JavaScript Example

```javascript
const options = {
  method: "POST",
  headers: {
    accept: "application/json",
    authorization: "Bearer {token}",
    "content-type": "application/json",
  },
  body: JSON.stringify({
    model: "claude-sonnet-4-20250514",
    max_tokens: 1024,
    stream: true,
    messages: [{ role: "user", content: "Hello, Claude" }],
  }),
};

const response = await fetch("https://api.acedata.cloud/v1/messages", options);
const reader = response.body.getReader();
const decoder = new TextDecoder();

while (true) {
  const { done, value } = await reader.read();
  if (done) break;
  console.log(decoder.decode(value));
}
```

## Multi-turn Conversation

If you want to integrate multi-turn conversation functionality, you need to alternate the messages of the `user` and `assistant` roles in the `messages` array, including the previous conversation history.

### Python Example

```python
import requests

url = "https://api.acedata.cloud/v1/messages"

headers = {
    "accept": "application/json",
    "authorization": "Bearer {token}",
    "content-type": "application/json"
}

payload = {
    "model": "claude-sonnet-4-20250514",
    "max_tokens": 1024,
    "messages": [
        {"role": "user", "content": "Hello, my name is Alice."},
        {"role": "assistant", "content": "Hello Alice! Nice to meet you. How can I help you today?"},
        {"role": "user", "content": "What is my name?"}
    ]
}

response = requests.post(url, json=payload, headers=headers)
print(response.json())
```

The response is as follows:

```json
{
  "id": "msg_01Y1wfQmd89g968TVbFu57Yc",
  "type": "message",
  "role": "assistant",
  "content": [
    {
      "type": "text",
      "text": "Your name is Alice, as you just told me!"
    }
  ],
  "model": "claude-sonnet-4-20250514",
  "stop_reason": "end_turn",
  "stop_sequence": null,
  "usage": {
    "input_tokens": 40,
    "output_tokens": 14
  }
}
```

By passing the complete conversation history in `messages`, Claude can provide accurate answers based on the context.

## Deep Thinking Model

Claude's thinking and thinking summary are different concepts: the model can reason internally, but the API does not return raw chain-of-thought. When reasoning is displayed, the API returns a processed summary. Current models recommend adaptive thinking controlled by `output_config.effort`.

### Python Example

```python
import requests

url = "https://api.acedata.cloud/v1/messages"

headers = {
    "accept": "application/json",
    "authorization": "Bearer {token}",
    "content-type": "application/json"
}

payload = {
    "model": "claude-opus-5",
    "max_tokens": 16000,
    "thinking": {"type": "adaptive", "display": "summarized"},
    "output_config": {"effort": "high"},
    "messages": [
        {"role": "user", "content": "What is the sine of 30 degrees? Show your reasoning."}
    ]
}

response = requests.post(url, json=payload, headers=headers)
print(response.json())
```

The response is as follows:

```json
{
  "type": "thinking",
  "thinking": "The problem asks for a standard trigonometric value...",
  "signature": "opaque-signature"
}
```

Notes:

- `display: "summarized"` returns a readable summary, not raw chain-of-thought; `display: "omitted"` returns an empty `thinking` value while retaining the opaque signature.
- Display affects returned content and streaming latency, not whether reasoning occurs or how thinking tokens are billed.
- New models should use `thinking.type=adaptive` and `output_config.effort`; `budget_tokens` is for older fixed-budget models. Fable 5.1 thinking cannot be disabled.
- Replay complete thinking blocks and signatures unchanged in multi-turn conversations and tool calls. Never modify or generate a signature.
- In streams, summarized thinking produces `thinking_delta`; omitted thinking retains only the block lifecycle and `signature_delta`.

## Visual Model

Claude supports multimodal input, allowing it to process both text and images simultaneously. In the Messages API, you can use visual capabilities by setting `content` to an array format and passing in image content blocks.

### Using Base64 Encoded Images

```python
import base64
import requests

url = "https://api.acedata.cloud/v1/messages"

headers = {
    "accept": "application/json",
    "authorization": "Bearer {token}",
    "content-type": "application/json"
}

# Read and encode the image
with open("image.png", "rb") as f:
    image_data = base64.standard_b64encode(f.read()).decode("utf-8")

payload = {
    "model": "claude-sonnet-4-20250514",
    "max_tokens": 1024,
    "messages": [
        {
            "role": "user",
            "content": [
                {
                    "type": "image",
                    "source": {
                        "type": "base64",
                        "media_type": "image/png",
                        "data": image_data
                    }
                },
                {
                    "type": "text",
                    "text": "What's in this image?"
                }
            ]
        }
    ]
}

response = requests.post(url, json=payload, headers=headers)
print(response.json())
```

### Using URL Images
```python
import requests

url = "https://api.acedata.cloud/v1/messages"

headers = {
    "accept": "application/json",
    "authorization": "Bearer {token}",
    "content-type": "application/json"
}

payload = {
    "model": "claude-sonnet-4-20250514",
    "max_tokens": 1024,
    "messages": [
        {
            "role": "user",
            "content": [
                {
                    "type": "image",
                    "source": {
                        "type": "url",
                        "url": "https://cdn.acedata.cloud/ueugot.png"
                    }
                },
                {
                    "type": "text",
                    "text": "What's in this image?"
                }
            ]
        }
    ]
}

response = requests.post(url, json=payload, headers=headers)
print(response.json())
```

### cURL Example

```bash
curl -X POST 'https://api.acedata.cloud/v1/messages' \
  -H 'accept: application/json' \
  -H 'authorization: Bearer {token}' \
  -H 'content-type: application/json' \
  -d '{
    "model": "claude-sonnet-4-20250514",
    "max_tokens": 1024,
    "messages": [
      {
        "role": "user",
        "content": [
          {
            "type": "image",
            "source": {
              "type": "url",
              "url": "https://cdn.acedata.cloud/ueugot.png"
            }
          },
          {
            "type": "text",
            "text": "What'\''s in this image?"
          }
        ]
      }
    ]
  }'
```

Supported image formats include: `image/jpeg`, `image/png`, `image/gif`, `image/webp`.

## Documents and PDFs

PDFs use a `document` content block and support Base64 or URL sources. Base64 sources must use `application/pdf`:

```python
import base64

with open("report.pdf", "rb") as f:
    pdf_data = base64.standard_b64encode(f.read()).decode("utf-8")

payload = {
    "model": "claude-fable-5-1",
    "max_tokens": 1024,
    "messages": [{
        "role": "user",
        "content": [
            {
                "type": "document",
                "source": {
                    "type": "base64",
                    "media_type": "application/pdf",
                    "data": pdf_data
                },
                "title": "Quarterly report"
            },
            {"type": "text", "text": "Summarize this PDF."}
        ]
    }]
}
```

URL sources use `{"type":"url","url":"https://example.com/report.pdf"}`. Documents also support `text/plain` and `content` sources composed of text or image blocks, with optional `title`, `context`, and `citations`.

## Cache Control

Top-level `cache_control` places a cache breakpoint at the last cacheable block:

```python
payload = {
    "model": "claude-fable-5-1",
    "max_tokens": 1024,
    "cache_control": {"type": "ephemeral", "ttl": "5m"},
    "system": "You are an expert on this reference material.",
    "messages": [{"role": "user", "content": "Summarize the key points."}]
}
```

For precise placement, add `cache_control` to text, image, document, tool-use, tool-result blocks, or tool definitions. `ttl` supports `5m` (default) and `1h`. Check `usage.cache_creation_input_tokens` and `usage.cache_read_input_tokens` for cache writes and hits.

Example of return result:

```json
{
  "id": "msg_01NCrxpZmV17bhQJJRQEFEb9",
  "type": "message",
  "role": "assistant",
  "content": [
    {
      "type": "text",
      "text": "This image shows an API request configuration interface for what appears to be an AI chat completion service. The interface includes parameters for model selection, messages, stream mode, and max tokens settings."
    }
  ],
  "model": "claude-sonnet-4-20250514",
  "stop_reason": "end_turn",
  "stop_sequence": null,
  "usage": {
    "input_tokens": 1570,
    "output_tokens": 52
  }
}
```

## Tool Use

The Claude Messages API natively supports tool invocation functionality, allowing the model to call your predefined tools/functions when needed.

### Python Example

```python
import requests

url = "https://api.acedata.cloud/v1/messages"

headers = {
    "accept": "application/json",
    "authorization": "Bearer {token}",
    "content-type": "application/json"
}

payload = {
    "model": "claude-sonnet-4-20250514",
    "max_tokens": 1024,
    "tools": [
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
    "messages": [
        {"role": "user", "content": "What's the weather like in San Francisco?"}
    ]
}

response = requests.post(url, json=payload, headers=headers)
print(response.json())
```

When the model decides to call a tool, the `content` in the return result will contain a `tool_use` type content block:

```json
{
  "id": "msg_01Aq9w938a90dw8q",
  "type": "message",
  "role": "assistant",
  "content": [
    {
      "type": "text",
      "text": "Let me check the weather in San Francisco for you."
    },
    {
      "type": "tool_use",
      "id": "toolu_01A09q90qw90lq917835lgs",
      "name": "get_weather",
      "input": {
        "location": "San Francisco, CA"
      }
    }
  ],
  "model": "claude-sonnet-4-20250514",
  "stop_reason": "tool_use",
  "stop_sequence": null,
  "usage": {
    "input_tokens": 120,
    "output_tokens": 68
  }
}
```

Note that `stop_reason` is `tool_use`, indicating that the model needs to call a tool. Upon receiving this result, you need to execute the tool function and return the result in the form of `tool_result` to the model:

```python
payload = {
    "model": "claude-sonnet-4-20250514",
    "max_tokens": 1024,
    "tools": [
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
    "messages": [
        {"role": "user", "content": "What's the weather like in San Francisco?"},
        {
            "role": "assistant",
            "content": [
                {"type": "text", "text": "Let me check the weather in San Francisco for you."},
                {"type": "tool_use", "id": "toolu_01A09q90qw90lq917835lgs", "name": "get_weather", "input": {"location": "San Francisco, CA"}}
            ]
        },
        {
            "role": "user",
            "content": [
                {
                    "type": "tool_result",
                    "tool_use_id": "toolu_01A09q90qw90lq917835lgs",
                    "content": "Sunny, 72°F"
                }
            ]
        }
    ]
}

response = requests.post(url, json=payload, headers=headers)
print(response.json())
```

The model will generate the final natural language reply based on the result returned from the tool.

## Differences with Chat Completion API

Ace Data Cloud provides two formats of the Claude API, with the main differences as follows:

The Messages API's `usage.input_tokens` counts uncached input only. Cache reads and cache creation are reported and billed independently.

| Feature       | Messages API (`/v1/messages`)    | Chat Completion API (`/v1/chat/completions`) |
| -------- | -------------------------------- | -------------------------------------------- |
| Format       | Anthropic native format                   | OpenAI compatible format                                  |
| System Prompt    | Independent `system` field                  | Passed through `role: "system"` in `messages`          |
| Response Structure     | `content` array (supports multiple types)             | `choices` array (contains `message`)                   |
| Streaming Format     | SSE events (multiple event types)                   | SSE `data` lines                                 |
| Deep Thinking     | Native `thinking` parameter                 | Triggered by special model names (e.g., `-thinking` suffix)                  |
| Tool Invocation     | Native `tools` + `input_schema`      | OpenAI compatible `functions` format                    |
| Token Statistics | `input_tokens` / `output_tokens` | `prompt_tokens` / `completion_tokens`        |

If your system is already integrated with the OpenAI format API, you can use the Chat Completion API for a seamless switch. If you need to utilize all native capabilities of Claude, it is recommended to use the Messages API.

## Error Handling

Errors use the Ace Data Cloud envelope: `error.code` is a stable code, `error.message` explains the failure, and `trace_id` supports troubleshooting. Common HTTP statuses include:

- `400`: Invalid request parameters or protocol content.
- `401`: Invalid, missing, or expired authorization token.
- `403`: Forbidden access, insufficient balance, or quota limits.
- `404`: API or model does not exist.
- `413`: Request body too large.
- `429`: Too many requests.
- `500` / `503` / `504`: Service error, temporary unavailability, or timeout.

### Error Response Example
```json
{
  "error": {
    "code": "api_error",
    "message": "fetch failed"
  },
  "trace_id": "2cf86e86-22a4-46e1-ac2f-032c0f2a4e89"
}
```

This runtime contract is not the official Anthropic error envelope; handle errors according to HTTP status and `error.code`.

## Conclusion

Through this document, you have learned how to use the Claude Messages API to call Claude's conversational features in Anthropic's native format. The Messages API supports basic conversations, system prompts, streaming responses, multi-turn dialogues, adaptive thinking, visual and PDF input, prompt caching, and tool calls.
