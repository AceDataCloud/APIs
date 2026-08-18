# AI Chat v2 Conversations API Integration Guide

The AI Chat v2 Conversations API (`/aichat2/conversations`) is the current AI Dialogue endpoint on Ace Data Cloud. It supports unified access to GPT, Claude, Gemini, Grok, Kimi, GLM, and DeepSeek model families, stateful conversations, streaming responses, multimodal message content, tool workflows, and conversation management actions.

## Application Process

To use the API, visit the [AI Chat API](https://platform.acedata.cloud/documents/59fb1199-6694-4afb-a222-3554d7f7d05a) page and click the "Acquire" button.

First-time applicants receive a free usage quota. Use the API token from [https://platform.acedata.cloud](https://platform.acedata.cloud) as the `Authorization` header.

## Basic Usage

Send a chat request by providing at least the `model` field. For normal chat requests, include `question` or `message`.

```shell
curl -X POST 'https://api.acedata.cloud/aichat2/conversations' \
-H 'accept: application/json' \
-H 'authorization: ******' \
-H 'content-type: application/json' \
-d '{
  "model": "gpt-4o",
  "question": "What is the capital of France?"
}'
```

Python equivalent:

```python
import requests

url = "https://api.acedata.cloud/aichat2/conversations"
headers = {
    "accept": "application/json",
    "authorization": "******",
    "content-type": "application/json"
}
payload = {
    "model": "gpt-4o",
    "question": "What is the capital of France?"
}

response = requests.post(url, json=payload, headers=headers)
print(response.text)
```

Success response:

```json
{
  "id": "f2f4b3e8-0c0a-4d3a-aaa2-7ff80c0a1c44",
  "answer": "Hi! I'm an AI assistant. How can I help you today?"
}
```

## Request Headers

| Header | Description |
| --- | --- |
| `accept` | Response format: `application/json`, `application/x-ndjson`, or `text/event-stream` |
| `authorization` | API token from your Ace Data Cloud account |
| `content-type` | `application/json` |

## Request Body

| Field | Type | Required | Description |
| --- | --- | --- | --- |
| `model` | string | ✅ | Model to use |
| `action` | string | ❌ | Operation: `chat`, `retrieve`, `retrieve_batch`, `update`, or `delete` |
| `question` | string | ❌ | Prompt or question for chat requests |
| `message` | string or array | ❌ | Text or multimodal message parts (`text`, `image_url`, `file_url`) |
| `messages` | array | ❌ | Message objects for OpenAI-style chat history |
| `id` | string | ❌ | Conversation ID for retrieval, update, delete, or continuing a stateful chat |
| `stateful` | boolean | ❌ | Enable stateful conversation mode; defaults to `true` |
| `references` | array of strings | ❌ | Reference URLs for image or file inputs |
| `preset` | string | ❌ | System-level preset prompt |
| `max_turns` | integer | ❌ | Maximum stateful conversation turns; minimum `1` |
| `async` | boolean | ❌ | Run asynchronously; defaults to `false` |
| `callback_url` | string | ❌ | Callback URL for asynchronous results |
| `allowed_skills` | array of strings | ❌ | Skills the model may use |
| `allowed_mcp_servers` | array of strings | ❌ | MCP servers the model may use |
| `unattended_policy` | object | ❌ | Policy with allowed skills, allowed MCP servers, and `expires_at` |
| `tool_results` | array | ❌ | Tool outputs with `tool_use_id`, `output`, and optional `is_error` |
| `title` | string | ❌ | Conversation title, typically for update actions |
| `user_id` | string | ❌ | End-user identifier |
| `application_id` | string | ❌ | Application identifier |
| `model_group` | string | ❌ | Model family filter: `chatgpt`, `claude`, `gemini`, `grok`, `kimi`, `glm`, or `deepseek` |
| `offset` | integer | ❌ | Pagination offset for batch retrieval; defaults to `0` |
| `limit` | integer | ❌ | Pagination limit for batch retrieval; `1` to `100`, defaults to `100` |

## Supported Models

Supported `model` values include:

`gpt-4`, `gpt-4.1`, `gpt-4.1-mini`, `gpt-4.1-nano`, `gpt-4o`, `gpt-4o-2024-05-13`, `gpt-4o-all`, `gpt-4o-image`, `gpt-4o-mini`, `gpt-5-all`, `gpt-5.1-all`, `gpt-5.2-pro`, `gpt-5.4-mini`, `gpt-5.4-nano`, `gpt-image-1`, `claude-3-5-haiku-20241022`, `claude-3-5-sonnet-20240620`, `claude-3-5-sonnet-20241022`, `claude-3-7-sonnet-20250219`, `claude-3-haiku-20240307`, `claude-3-sonnet-20240229`, `claude-haiku-4-5-20251001`, `claude-opus-4-1-20250805`, `claude-opus-4-20250514`, `claude-opus-4-5-20251101`, `claude-opus-4-6`, `claude-fable-5`, `claude-opus-5`, `claude-opus-4-8`, `claude-opus-4-7`, `claude-sonnet-4-20250514`, `claude-sonnet-4-5-20250929`, `claude-sonnet-4-6`, `claude-sonnet-5`, `gemini-2.0-flash-lite`, `gemini-2.5-flash-lite`, `gemini-3-pro-preview`, `gemini-3.1-flash-image-preview`, `gemini-3.1-flash-lite-preview`, `gemini-3.1-pro`, `gemini-3.1-pro-preview`, `grok-3`, `grok-3-fast`, `grok-4`, `grok-4.5`, `grok-4-0709`, `deepseek-chat`, `deepseek-r1`, `deepseek-r1-0528`, `deepseek-reasoner`, `deepseek-v3`, `deepseek-v3-250324`, `deepseek-v3.2-exp`, `deepseek-v4-flash`, `deepseek-v4-pro`, `kimi-k2-thinking`, `kimi-k2-thinking-turbo`, `kimi-k3`, `kimi-k2.6`, `kimi-k2.5`, `glm-3-turbo`, `glm-4.5`, `glm-4.5v`, `glm-4.6`, `glm-4.7`, `glm-5`, `glm-5-turbo`, `glm-5.2`, `glm-5.1`, `o1`, `o1-mini`, `o1-pro`, `o3`, `o3-mini`, `o3-pro`, `o4-mini`

## Streaming Responses

To receive newline-delimited streaming chunks, set the `accept` header to `application/x-ndjson`.

```shell
curl -X POST 'https://api.acedata.cloud/aichat2/conversations' \
-H 'accept: application/x-ndjson' \
-H 'authorization: ******' \
-H 'content-type: application/json' \
-d '{
  "model": "gpt-4o",
  "question": "Hello"
}'
```

Example stream item:

```json
{"type":"text_delta","content":" today","delta_answer":" today","answer":"Hello! How can I assist you today","id":"f2f4b3e8-0c0a-4d3a-aaa2-7ff80c0a1c44"}
```

The endpoint also supports `text/event-stream` for server-sent event clients.

## Conversation Management

Use the `action` field to manage conversations:

- `chat`: create or continue a conversation.
- `retrieve`: retrieve one conversation by `id`.
- `retrieve_batch`: list conversations, optionally using `model_group`, `offset`, and `limit`.
- `update`: update fields such as `title` for a conversation identified by `id`.
- `delete`: delete the conversation identified by `id`.

## Response Schema

### Success (200)

| Field | Type | Description |
| --- | --- | --- |
| `id` | string | Conversation ID |
| `answer` | string | Model reply or accumulated answer |

Streaming chunks may additionally include `type`, `content`, and `delta_answer`.

### Error (400 / 401 / 404 / 429 / 500)

| Field | Type | Description |
| --- | --- | --- |
| `error.code` | string | Error code, such as `bad_request`, `invalid_token`, `not_found`, `too_many_requests`, or `chat_error` |
| `error.message` | string | Human-readable error description |
| `trace_id` | string | Trace ID for debugging |
