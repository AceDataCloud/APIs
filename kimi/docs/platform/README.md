<!-- Generated from PlatformBackend; edit the backend source. -->
# API reference

These are the public HTTP API contracts. Native MCP tools and CLI commands are described in the package README.

## Kimi

| Method | Endpoint | Request fields |
| --- | --- | --- |
| POST | `/kimi/chat/completions` | `n`, `model`, `stream`, `messages`, `max_tokens`, `temperature`, `response_format`, `top_p`, `frequency_penalty`, `presence_penalty`, `seed`, `stop`, `max_completion_tokens`, `logprobs`, `top_logprobs`, `stream_options`, `parallel_tool_calls`, `user`, `reasoning_effort`, `service_tier`, `store`, `metadata`, `logit_bias`, `modalities`, `audio`, `prediction`, `web_search_options`, `tools`, `tool_choice`, `thinking` |

Full schema: [kimi.json](openapi/kimi.json).

### Guides

- [development_kimi_chat_completions.md](guides/development_kimi_chat_completions.md)

Source: [PlatformBackend@bdae773e02f3](https://github.com/AceDataCloud/PlatformBackend/tree/bdae773e02f3f51d2896eef497b569748577b753).
