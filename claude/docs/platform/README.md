<!-- Generated from PlatformBackend; edit the backend source. -->
# API reference

These are the public HTTP API contracts. Native MCP tools and CLI commands are described in the package README.

## Claude AI

| Method | Endpoint | Request fields |
| --- | --- | --- |
| POST | `/v1/chat/completions` | `n`, `model`, `stream`, `messages`, `max_tokens`, `temperature`, `response_format`, `top_p`, `frequency_penalty`, `presence_penalty`, `seed`, `stop`, `max_completion_tokens`, `logprobs`, `top_logprobs`, `stream_options`, `parallel_tool_calls`, `user`, `reasoning_effort`, `service_tier`, `store`, `metadata`, `logit_bias`, `modalities`, `audio`, `prediction`, `web_search_options`, `tools`, `tool_choice` |
| POST | `/v1/messages` | `model`, `messages`, `max_tokens`, `metadata`, `stop_sequences`, `stream`, `system`, `temperature`, `tool_choice`, `tools`, `top_k`, `top_p`, `thinking`, `output_config`, `cache_control` |
| POST | `/v1/messages/count_tokens` | `model`, `messages`, `system`, `thinking`, `tool_choice`, `tools`, `cache_control` |

Full schema: [claude.json](openapi/claude.json).

### Guides

- [development_claude_messages.md](guides/development_claude_messages.md)
- [development_claude_messages_count_tokens.md](guides/development_claude_messages_count_tokens.md)

Source: [PlatformBackend@945664eca88d](https://github.com/AceDataCloud/PlatformBackend/tree/945664eca88d16d21159d3739f874c830c046005).
