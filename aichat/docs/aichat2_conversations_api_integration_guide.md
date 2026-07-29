# AI Chat v2 API Integration Guide

The AI Chat v2 API (`/aichat2/conversations`) is the next-generation dialogue interface on Ace Data Cloud. It keeps the simple request pattern from v1 while adding multimodal input, structured streaming events, tool invocation, pause/resume support, and lightweight conversation CRUD actions.

For existing clients, v2 is backward compatible with the classic AI Chat API: you can still send `model` + `question` (+ optional `stateful`, `id`, `references`, `preset`) and receive the same `{ "answer": "...", "id": "..." }` JSON shape.

## Authentication

Get your API Token from the [Ace Data Cloud Console](https://platform.acedata.cloud/console/applications).

- Base URL: `https://api.acedata.cloud`
- Endpoint: `POST /aichat2/conversations`
- Header: `authorization: ******`
- `accept`: `application/json`, `application/x-ndjson`, or `text/event-stream`

One API Token works across Ace Data Cloud services, so you do not need to subscribe separately for AI Chat. New accounts receive free starter credit, and you can top up your shared balance in the [console](https://platform.acedata.cloud/console/coin).

> Full documentation: [AI Chat v2 API](https://platform.acedata.cloud/documents/aichat2-conversations)

## Basic Usage

The simplest request only needs `model`. In normal chat usage, you typically send `model` together with `question`.

```shell
curl -X POST 'https://api.acedata.cloud/aichat2/conversations' \
-H 'accept: application/json' \
-H 'authorization: ******' \
-H 'content-type: application/json' \
-d '{
  "model": "gpt-4o",
  "question": "Introduce AceDataCloud in one sentence."
}'
```

Response:

```json
{
  "answer": "AceDataCloud is a unified API platform that aggregates mainstream AI models and multimodal services, allowing developers to access services like GPT, Claude, Gemini, Midjourney, Suno, Veo, and more with a single key.",
  "id": "f2f4b3e8-0c0a-4d3a-aaa2-7ff80c0a1c44"
}
```

Python example:

```python
import requests

url = "https://api.acedata.cloud/aichat2/conversations"

headers = {
    "accept": "application/json",
    "authorization": "******",
    "content-type": "application/json",
}

payload = {
    "model": "gpt-4o",
    "question": "Introduce AceDataCloud in one sentence.",
}

response = requests.post(url, json=payload, headers=headers)
print(response.json())
```

## Request Body

Common request fields:

| Field | Type | Required | Description |
| --- | --- | --- | --- |
| `model` | string | ✅ | Model identifier to run |
| `question` | string | ❌ | Plain-text user prompt |
| `message` | array | ❌ | Structured multimodal input blocks |
| `stateful` | boolean | ❌ | Save conversation state for follow-up turns |
| `id` | string | ❌ | Existing conversation ID |
| `references` | array of strings | ❌ | Backward-compatible file or image URLs |
| `preset` | string | ❌ | System-level preset/instruction |
| `action` | string | ❌ | `chat`, `retrieve`, `retrieve_batch`, `update`, or `delete` |
| `max_turns` | integer | ❌ | Limit model/tool self-invocation rounds |
| `async` | boolean | ❌ | Queue a background task and return immediately |
| `callback_url` | string | ❌ | Webhook URL for async completion |
| `allowed_skills` | array | ❌ | Pre-authorized connected Skills for unattended mode |
| `allowed_mcp_servers` | array | ❌ | Pre-authorized connected MCP servers for unattended mode |
| `unattended_policy` | object | ❌ | Equivalent structured pre-authorization object |
| `tool_results` | array | ❌ | Resume a paused conversation by returning tool answers |
| `messages` | array | ❌ | Conversation history used with `action: update` |
| `title` | string | ❌ | Conversation title, mainly for `action: update` |
| `user_id` | string | ❌ | Optional filter for batch retrieval |
| `application_id` | string | ❌ | Optional filter for batch retrieval |
| `model_group` | string | ❌ | Optional filter: `chatgpt`, `claude`, `gemini`, `grok`, `kimi`, `glm`, or `deepseek` |
| `offset` | integer | ❌ | Batch pagination offset |
| `limit` | integer | ❌ | Batch pagination limit |

## Multi-Turn Conversations

Like v1, pass `stateful: true` to enable conversation storage. The API returns an `id` that you can pass in subsequent requests.

```shell
curl -X POST 'https://api.acedata.cloud/aichat2/conversations' \
-H 'accept: application/json' \
-H 'authorization: ******' \
-H 'content-type: application/json' \
-d '{
  "model": "gpt-4o",
  "stateful": true,
  "question": "Remember a number: 42."
}'
```

Response:

```json
{
  "answer": "Okay, I have remembered 42. What would you like me to do with it?",
  "id": "f2f4b3e8-0c0a-4d3a-aaa2-7ff80c0a1c44"
}
```

Follow-up request:

```shell
curl -X POST 'https://api.acedata.cloud/aichat2/conversations' \
-H 'accept: application/json' \
-H 'authorization: ******' \
-H 'content-type: application/json' \
-d '{
  "model": "gpt-4o",
  "stateful": true,
  "id": "f2f4b3e8-0c0a-4d3a-aaa2-7ff80c0a1c44",
  "question": "What number did I just ask you to remember?"
}'
```

`stateful` defaults to `true`. Set `stateful: false` if you do not want the round to be saved.

## Streaming Responses

AI Chat v2 supports three response formats:

| Scenario | `accept` | Data format |
| --- | --- | --- |
| Standard response | `application/json` | One `{answer, id}` object |
| NDJSON streaming | `application/x-ndjson` | One JSON event per line |
| SSE streaming | `text/event-stream` | `data: {json}\n\n` blocks ending with `data: [DONE]` |

```python
import json
import requests

url = "https://api.acedata.cloud/aichat2/conversations"

headers = {
    "accept": "application/x-ndjson",
    "authorization": "******",
    "content-type": "application/json",
}

payload = {
    "model": "gpt-4o",
    "stateful": True,
    "question": "Introduce Hangzhou in three sentences.",
}

with requests.post(url, json=payload, headers=headers, stream=True) as resp:
    answer = ""
    for line in resp.iter_lines():
        if not line:
            continue
        event = json.loads(line)
        if event.get("type") == "text_delta":
            answer += event["content"]
            print(event["delta_answer"], end="", flush=True)
        elif event.get("type") == "done":
            print()
            print("usage =", event.get("usage"))
```

Example event stream:

```json
{"type":"text_delta","content":"Hang","delta_answer":"Hang","id":"f2f4b3e8-..."}
{"type":"text_delta","content":"zhou","delta_answer":"zhou","id":"f2f4b3e8-..."}
{"type":"done","conversation_id":"f2f4b3e8-...","usage":{"prompt_tokens":21,"completion_tokens":58,"total_tokens":79},"terminal_reason":"natural_stop"}
```

Common streaming event types:

| `type` | Meaning |
| --- | --- |
| `text_delta` | Incremental assistant text. `delta_answer` mirrors `content` for v1 compatibility. |
| `thinking` | Reasoning output from models that expose it |
| `tool_use` | Tool invocation request |
| `tool_result` | Result of a previous tool invocation |
| `card` | Structured renderable card output |
| `citation` | Citation metadata for the response |
| `ask_user_question` | The conversation is paused waiting for user input |
| `artifact` | Generated artifact such as code or document output |
| `system_message` | System-level UI message |
| `compact` | Internal context compaction event |
| `error` | Streaming error event |
| `done` | Final event with usage and terminal reason |

## Multimodal Input

For image or file input, use `message` blocks instead of `question`:

```json
{
  "model": "gpt-4o",
  "stateful": true,
  "message": [
    { "type": "text", "text": "How many cats are in this picture?" },
    { "type": "image_url", "image_url": { "url": "https://cdn.acedata.cloud/cats.jpg" } }
  ]
}
```

Supported block types:

- `text`
- `image_url`
- `file_url`

For backward compatibility, v2 still accepts `references: ["https://..."]`. Image URLs are converted to `image_url` blocks, other files are converted to `file_url` blocks, and `question` becomes a leading `text` block.

## Tool Invocation and MCP

Tool invocation is enabled by default in v2. The model can autonomously use built-in tools such as web search or file reading, and it can also use connected MCP servers that the user has authorized.

```json
{"type":"tool_use","tool_id":"toolu_01ABCDEF","tool_name":"web_search","input":{"query":"Shanghai 2026 spring exhibitions"},"id":"f2f4b3e8-..."}
{"type":"tool_result","tool_id":"toolu_01ABCDEF","output":"...","is_error":false,"id":"f2f4b3e8-..."}
```

Set `max_turns` to limit how many times the model can self-invoke tools in a single request.

## Async Execution and Unattended Authorization

Set `async: true` when you want the request to continue in the background:

```json
{
  "model": "gpt-4o",
  "async": true,
  "question": "My service is alarming, notify the on-call team."
}
```

Example async response:

```json
{
  "task_id": "f2f4b3e8-0c0a-4d3a-aaa2-7ff80c0a1c44",
  "conversation_id": "f2f4b3e8-0c0a-4d3a-aaa2-7ff80c0a1c44",
  "id": "f2f4b3e8-0c0a-4d3a-aaa2-7ff80c0a1c44",
  "status": "queued"
}
```

If unattended execution needs write-capable tools, explicitly pre-authorize them with `allowed_skills`, `allowed_mcp_servers`, or `unattended_policy`.

## Resume Paused Conversations

When the model emits an `ask_user_question` event, continue the same conversation by sending `tool_results` with the matching `tool_use_id`:

```shell
curl -X POST 'https://api.acedata.cloud/aichat2/conversations' \
  -H 'accept: text/event-stream' \
  -H 'authorization: ******' \
  -H 'content-type: application/json' \
  -d '{
    "model": "gpt-4o",
    "stateful": true,
    "id": "f2f4b3e8-0c0a-4d3a-aaa2-7ff80c0a1c44",
    "tool_results": [
      {
        "tool_use_id": "toolu_01XYZW",
        "output": "English"
      }
    ]
  }'
```

When `tool_results` are present, `question`, `message`, and `references` are ignored.

## Conversation Management

Use the `action` field on the same endpoint for lightweight CRUD.

### Retrieve one conversation

```json
{
  "action": "retrieve",
  "id": "f2f4b3e8-0c0a-4d3a-aaa2-7ff80c0a1c44"
}
```

### Retrieve conversation summaries

```json
{
  "action": "retrieve_batch",
  "model_group": "chatgpt",
  "limit": 20,
  "offset": 0
}
```

### Update a conversation title

```json
{
  "action": "update",
  "id": "f2f4b3e8-0c0a-4d3a-aaa2-7ff80c0a1c44",
  "title": "Hangzhou Travel Plan"
}
```

### Delete a conversation

```json
{
  "action": "delete",
  "id": "f2f4b3e8-0c0a-4d3a-aaa2-7ff80c0a1c44"
}
```

`retrieve` returns the full conversation record. `retrieve_batch` returns `{ items, total }` summary data. `delete` returns `{ id, success: true }`.

## Response Schemas

### Success response

For standard chat requests with `accept: application/json`, the API returns:

```json
{
  "answer": "string",
  "id": "string"
}
```

### Error response

Errors use this structure:

```json
{
  "error": {
    "code": "chat_error",
    "message": "upstream LLM returned an error"
  },
  "trace_id": "2cf86e86-22a4-46e1-ac2f-032c0f2a4e89"
}
```

Common HTTP status codes:

- `400`: invalid request body, missing required fields, or mismatched `tool_use_id`
- `401`: invalid API token
- `404`: conversation not found for `retrieve`, `update`, or `delete`
- `429`: rate limit triggered
- `500`: upstream model or platform processing error

## Migrating from v1

To migrate from `/aichat/conversations` to `/aichat2/conversations`:

1. Change the request URL.
2. Upgrade older model names to current model identifiers where possible.
3. Keep your existing line-by-line NDJSON parsing if you already rely on `delta_answer`.

After migrating, you can adopt `message`, SSE streaming, tool invocation, and CRUD actions incrementally.
