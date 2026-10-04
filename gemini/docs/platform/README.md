<!-- Generated from PlatformBackend; edit the backend source. -->
# API reference

These are the public HTTP API contracts. Native MCP tools and CLI commands are described in the package README.

## Gemini AI

| Method | Endpoint | Request fields |
| --- | --- | --- |
| POST | `/gemini/chat/completions` | `n`, `model`, `stream`, `messages`, `max_tokens`, `temperature`, `response_format`, `top_p`, `frequency_penalty`, `presence_penalty`, `seed`, `stop`, `max_completion_tokens`, `logprobs`, `top_logprobs`, `stream_options`, `parallel_tool_calls`, `user`, `reasoning_effort`, `service_tier`, `store`, `metadata`, `logit_bias`, `modalities`, `audio`, `prediction`, `web_search_options`, `tools`, `tool_choice` |
| POST | `/v1beta/models/{model}:generateContent` | `contents`, `systemInstruction`, `generationConfig`, `tools`, `toolConfig`, `safetySettings` |
| POST | `/v1beta/models/{model}:streamGenerateContent` | `contents`, `systemInstruction`, `generationConfig`, `tools`, `toolConfig`, `safetySettings` |
| POST | `/gemini/videos` | `prompt`, `model`, `aspect_ratio`, `resolution`, `image_urls`, `video_urls`, `callback_url`, `async` |
| POST | `/gemini/tasks` | `id`, `ids`, `action` |

Full schema: [gemini.json](openapi/gemini.json).

### Guides

- [development_gemini_chat_completions.md](guides/development_gemini_chat_completions.md)
- [development_gemini_generate_content.md](guides/development_gemini_generate_content.md)
- [development_gemini_tasks.md](guides/development_gemini_tasks.md)
- [development_gemini_videos.md](guides/development_gemini_videos.md)

Source: [PlatformBackend@bdae773e02f3](https://github.com/AceDataCloud/PlatformBackend/tree/bdae773e02f3f51d2896eef497b569748577b753).
