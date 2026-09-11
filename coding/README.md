# Coding Plan API

Ace Data Cloud Coding Plan provides OpenAI-compatible endpoints for coding assistants.

## Authentication

Obtain an API Key from the [Ace Data Cloud application console](https://platform.acedata.cloud/console/applications). Send it with each request:

```http
Authorization: ******
```

## Endpoints

| API | Path |
| --- | --- |
| Claude Messages Count Tokens | `POST /v1/messages/count_tokens` |
| Claude Messages | `POST /v1/messages` |
| OpenAI Chat Completions | `POST /openai/chat/completions` |
| Claude Chat Completions | `POST /v1/chat/completions` |
| DeepSeek Chat Completions | `POST /deepseek/chat/completions` |
| GLM Chat Completions | `POST /glm/chat/completions` |
| Gemini Chat Completions | `POST /gemini/chat/completions` |
| Grok Chat Completions | `POST /grok/chat/completions` |
| Kimi Chat Completions | `POST /kimi/chat/completions` |
| OpenAI Responses | `POST /openai/responses` |

## Configure coding assistants

For Cline, Kilo Code, Roo Code, and WorkBuddy, select the OpenAI-compatible or custom provider and use:

| Setting | Value |
| --- | --- |
| Base URL | `https://api.acedata.cloud/v1` |
| API Key | Your Ace Data Cloud API Key |
| Model ID | A model ID available in Coding Plan |

Keep optional capability switches at their defaults unless the selected model supports them. Enable tools only for models with native tool/function-calling support. After saving, send `Reply only OK` and run a read-only file task to verify the configuration.

## Related Resources

- [Ace Data Cloud Developer Platform](https://platform.acedata.cloud)
- [Usage history](https://platform.acedata.cloud/console/usages)
