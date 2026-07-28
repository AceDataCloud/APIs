# AI Chat v2 API Integration Guide

The AI Chat v2 API (`/aichat2/conversations`) is the next-generation AI dialogue interface on Ace Data Cloud. It is backward compatible with the classic `/aichat/conversations` request body while adding multimodal `message` input, structured streaming events, tool invocation, asynchronous execution, and lightweight conversation CRUD actions.

## Application Process

To use the AI Chat v2 API, open the [Ace Data Cloud Console](https://platform.acedata.cloud/console/applications) and copy your API token.

If you are not yet logged in or registered, you will be redirected to the login page and then returned to the console automatically.

**A single API token works across every service on the platform, so you do not need to apply separately for AI Chat.** New accounts receive free starter credit, and you can top up your shared balance in the [console](https://platform.acedata.cloud/console/coin).

> Full documentation: [AI Chat v2 API →](https://platform.acedata.cloud/documents/aichat2-conversations)

## Basic Usage

The simplest usage is to pass a `model` and a `question` and receive a JSON response containing the answer and conversation ID.

```shell
curl -X POST 'https://api.acedata.cloud/aichat2/conversations' \
-H 'accept: application/json' \
-H 'authorization: ******' \
-H 'content-type: application/json' \
-d '{
  "model": "gpt-5.4",
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

Python equivalent:

```python
import requests

url = "https://api.acedata.cloud/aichat2/conversations"

headers = {
    "accept": "application/json",
    "authorization": "******",
    "content-type": "application/json",
}

payload = {
    "model": "gpt-5.4",
    "question": "Introduce AceDataCloud in one sentence.",
}

response = requests.post(url, json=payload, headers=headers)
print(response.json())
```

## Request Headers

| Header | Description |
| --- | --- |
| `accept` | Response format: `application/json` (default), `application/x-ndjson`, or `text/event-stream` |
| `authorization` | Your API token from the Ace Data Cloud console |
| `content-type` | Set to `application/json` |

## Request Body

The v2 endpoint uses the same path for both chat completion and conversation-management actions.

| Field | Type | Required | Description |
| --- | --- | --- | --- |
| `model` | string | ✅ for chat requests | Model to use for generation |
| `question` | string | Conditional | Plain-text user prompt for chat requests |
| `message` | array | Conditional | Structured multimodal input blocks, such as text, images, and files |
| `stateful` | boolean | ❌ | Enable stored multi-turn conversations; defaults to `true` |
| `id` | string | ❌ | Conversation ID used for continuing, retrieving, updating, or deleting a conversation |
| `action` | string | ❌ | Conversation action: `retrieve`, `retrieve_batch`, `update`, or `delete` |
| `references` | array of strings | ❌ | Backward-compatible list of attachment URLs; image URLs become image blocks automatically |
| `preset` | string | ❌ | System-level instruction similar to `system_prompt` |
| `max_turns` | integer | ❌ | Maximum number of autonomous tool-use turns in a request |
| `async` | boolean | ❌ | Run the request asynchronously and return a queued task immediately |
| `callback_url` | string | ❌ | HTTP/HTTPS webhook to receive async completion results |
| `allowed_skills` | array of strings | ❌ | Skills that may execute without manual confirmation in unattended mode |
| `allowed_mcp_servers` | array of strings | ❌ | MCP servers that may execute without manual confirmation in unattended mode |
| `unattended_policy` | object | ❌ | Fine-grained unattended authorization policy |
| `tool_results` | array | ❌ | User-provided answers for resuming paused tool flows |
| `messages` | array | ❌ | Full conversation messages, mainly for `action: update` |
| `title` | string | ❌ | Conversation title used by `action: update` |
| `user_id` | string | ❌ | Filter field for batch retrieval |
| `application_id` | string | ❌ | Filter field for batch retrieval |
| `model_group` | string | ❌ | Filter field for batch retrieval |
| `offset` | integer | ❌ | Pagination offset for `retrieve_batch` |
| `limit` | integer | ❌ | Pagination limit for `retrieve_batch` |

## Multi-Turn Conversations

Like the classic endpoint, v2 can maintain server-side context for you. Pass `stateful: true`, then reuse the returned `id` in later requests.

First request:

```shell
curl -X POST 'https://api.acedata.cloud/aichat2/conversations' \
-H 'accept: application/json' \
-H 'authorization: ******' \
-H 'content-type: application/json' \
-d '{
  "model": "gpt-5.4",
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

Second request:

```shell
curl -X POST 'https://api.acedata.cloud/aichat2/conversations' \
-H 'accept: application/json' \
-H 'authorization: ******' \
-H 'content-type: application/json' \
-d '{
  "model": "gpt-5.4",
  "stateful": true,
  "id": "f2f4b3e8-0c0a-4d3a-aaa2-7ff80c0a1c44",
  "question": "What number did I just ask you to remember?"
}'
```

```json
{
  "answer": "The number you asked me to remember is 42.",
  "id": "f2f4b3e8-0c0a-4d3a-aaa2-7ff80c0a1c44"
}
```

## Streaming Responses

v2 supports both NDJSON and Server-Sent Events:

| Scenario | `accept` | Data format |
| --- | --- | --- |
| Standard request/response | `application/json` | Returns `{answer, id}` |
| CLI or server streaming | `application/x-ndjson` | One JSON object per line |
| Browser/frontend streaming | `text/event-stream` | SSE `data: ...` events ending with `data: [DONE]` |

NDJSON example:

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
    "model": "gpt-5.4",
    "stateful": True,
    "question": "Introduce Hangzhou in three sentences.",
}

with requests.post(url, json=payload, headers=headers, stream=True) as response:
    for line in response.iter_lines():
        if not line:
            continue
        event = json.loads(line)
        print(event)
```

Typical NDJSON response events:

```json
{"type":"text_delta","content":"Hang","delta_answer":"Hang","id":"f2f4b3e8-..."}
{"type":"text_delta","content":"zhou","delta_answer":"zhou","id":"f2f4b3e8-..."}
{"type":"done","conversation_id":"f2f4b3e8-...","usage":{"prompt_tokens":21,"completion_tokens":58,"total_tokens":79},"terminal_reason":"natural_stop"}
```

Common event types include `text_delta`, `thinking`, `tool_use`, `tool_result`, `citation`, `card`, `artifact`, `ask_user_question`, `error`, and `done`.

## Multimodal Input

If the user input contains images or files, use `message` instead of `question`:

```json
{
  "model": "gpt-5.4",
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

The legacy `references` field is still supported for backward compatibility. Image URLs are converted automatically into image blocks, and other URLs are converted into file blocks.

## Tool Invocation and MCP

AI Chat v2 can autonomously call built-in tools and connected MCP servers to complete multi-step tasks. Tool activity appears in streaming responses as `tool_use` and `tool_result` events.

Example streaming events:

```json
{"type":"tool_use","tool_id":"toolu_01ABCDEF","tool_name":"web_search","input":{"query":"Shanghai 2026 spring exhibitions"},"id":"f2f4b3e8-..."}
{"type":"tool_result","tool_id":"toolu_01ABCDEF","output":"...","is_error":false,"id":"f2f4b3e8-..."}
{"type":"text_delta","content":"Here","delta_answer":"Here","id":"f2f4b3e8-..."}
```

If your client only cares about the final answer, concatenate all `text_delta` content and ignore the tool-related event types.

## Asynchronous Execution

For webhook or background workflows, set `async: true` to queue the job and return immediately:

```json
{
  "model": "gpt-5.5",
  "async": true,
  "question": "Summarize the latest deployment incident and draft a status update."
}
```

Response:

```json
{
  "task_id": "f2f4b3e8-0c0a-4d3a-aaa2-7ff80c0a1c44",
  "conversation_id": "f2f4b3e8-0c0a-4d3a-aaa2-7ff80c0a1c44",
  "id": "f2f4b3e8-0c0a-4d3a-aaa2-7ff80c0a1c44",
  "status": "queued"
}
```

You can later retrieve the result with `action: retrieve` and the same `id`, or provide a `callback_url` to receive the result automatically.

If unattended execution needs permission to use connected tools, pass `allowed_skills`, `allowed_mcp_servers`, or an `unattended_policy` object in the request body.

## Resuming Paused Conversations

Some tool flows pause and ask the user for more information. In streaming mode, the API emits an `ask_user_question` event:

```json
{
  "type": "ask_user_question",
  "tool_id": "toolu_01XYZW",
  "tool_name": "ask_user_question",
  "question": "Do you want the report in English or Chinese?",
  "options": ["English", "Chinese"],
  "id": "f2f4b3e8-..."
}
```

Resume the conversation by sending the same conversation `id` together with `tool_results`:

```json
{
  "model": "gpt-5.4",
  "stateful": true,
  "id": "f2f4b3e8-0c0a-4d3a-aaa2-7ff80c0a1c44",
  "tool_results": [
    {
      "tool_use_id": "toolu_01XYZW",
      "output": "English"
    }
  ]
}
```

When `tool_results` is present, `question`, `message`, and `references` are ignored.

## Conversation Management

The same endpoint also supports lightweight CRUD actions.

### Retrieve one conversation

```json
{
  "action": "retrieve",
  "id": "f2f4b3e8-0c0a-4d3a-aaa2-7ff80c0a1c44"
}
```

### Retrieve a batch of conversation summaries

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

Deleting returns:

```json
{
  "id": "f2f4b3e8-0c0a-4d3a-aaa2-7ff80c0a1c44",
  "success": true
}
```

## Migration from `/aichat/conversations`

The v2 API is designed for smooth migration:

1. Change the request URL from `https://api.acedata.cloud/aichat/conversations` to `https://api.acedata.cloud/aichat2/conversations`.
2. Keep using the classic `question`, `stateful`, `id`, `references`, and `preset` fields if you want a minimal client change.
3. Upgrade to newer models and features like structured streaming, multimodal `message`, tool invocation, and CRUD actions when you are ready.

## Response Schema

### Success (200)

Depending on the `accept` header and request mode, the API can return:

- Standard JSON chat result: `{ "answer": "...", "id": "..." }`
- NDJSON stream events such as `text_delta`, `tool_use`, `tool_result`, and `done`
- SSE stream events ending with `data: [DONE]`
- Async queue result such as `{ "task_id": "...", "conversation_id": "...", "status": "queued" }`
- CRUD results such as a full conversation object, `{ items, total }`, or `{ id, success: true }`

### Error Responses

| Status | Example error code | Description |
| --- | --- | --- |
| `400` | `bad_request` | Missing or invalid request fields, mismatched `tool_use_id`, or invalid `messages` schema |
| `401` | `invalid_token` | Invalid `authorization` header |
| `404` | `not_found` | Conversation ID not found for retrieve, update, or delete actions |
| `429` | `too_many_requests` | Rate limit exceeded |
| `500` | `chat_error` | Upstream model or internal processing error |

Error body example:

```json
{
  "error": {
    "code": "chat_error",
    "message": "upstream LLM returned an error"
  },
  "trace_id": "2cf86e86-22a4-46e1-ac2f-032c0f2a4e89"
}
```
