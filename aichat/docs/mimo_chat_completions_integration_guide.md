# MiMo Chat API Integration Guide

MiMo 2.6 Pro and MiMo 2.6 Flash are Xiaomi MiMo models. This API follows the OpenAI Chat Completions format and bills input, output and cached input tokens separately.

> This is a preparation guide. The service is not yet available. Check service acquisition status and the model list in the console before integrating.

## Models and endpoint

| Model | Intended use |
| --- | --- |
| `mimo-v2.6-pro` | Complex analysis, reasoning and tool calling |
| `mimo-v2.6-flash` | Everyday chat and lightweight tasks |

Once available, acquire MiMo and create an API credential for the service. Send requests to `https://api.acedata.cloud/mimo/chat/completions`, or set the OpenAI SDK base URL to `https://api.acedata.cloud/mimo`. The unified `/v1/chat/completions` endpoint also requires the corresponding service permission.

The initial scope is text Chat Completions. Image, audio, video, built-in web search, Responses, Messages, Batch and UltraSpeed are outside this release.

## Python example

```python
import os
from openai import OpenAI

client = OpenAI(
    api_key=os.environ["ACEDATACLOUD_API_KEY"],
    base_url="https://api.acedata.cloud/mimo",
)
response = client.chat.completions.create(
    model="mimo-v2.6-pro",
    messages=[{"role": "user", "content": "Explain how a rainbow forms."}],
    max_completion_tokens=256,
    extra_body={"thinking": {"type": "disabled"}},
)
print(response.choices[0].message.content)
print(response.usage)
```

This example demonstrates the request shape. A real response example will be added after service validation.

## Streaming, reasoning and tools

Set `stream=true` for SSE and `stream_options={"include_usage": true}` for final usage. Handle content, reasoning and tool-call deltas as well as the final usage event.

Use `thinking.type=enabled` for reasoning or `disabled` to turn it off. Reasoning is returned in `reasoning_content`, separately from final `content`. Preserve assistant reasoning, complete `tool_calls` and matching `tool_call_id` values when continuing a tool interaction.

Only `type=function` tools and `tool_choice=auto` are in scope. Your application executes tools and returns their results; a tool call emitted by the model does not mean the tool ran. Built-in web search is not enabled.

## Billing

`prompt_tokens` includes cache hits. `prompt_tokens_details.cached_tokens` is charged at the cached-input rate; remaining input uses the standard input rate. `completion_tokens` includes reasoning output: do not add reasoning tokens again. Streaming requests also settle against final usage.

Consult the console for current prices. The USD value of a Credit depends on the purchased package. A failed request is not a successful completion; provide the response trace identifier when investigating a charge.

## Errors

Check request parameters for validation errors and credentials or service access for authentication and permission errors. Back off on 429. A lack of healthy model capacity may return 503. If a stream is interrupted, inspect received results and usage before retrying to avoid duplicate work.
