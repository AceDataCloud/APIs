# AI Chat v2 API Integration Guide

The AI Chat v2 API (`/aichat2/conversations`) is the next-generation conversational interface, a comprehensive upgrade of the [AI Chat API](https://platform.acedata.cloud/documents/aichat-conversations). Building on the simplicity and multi-turn conversation hosting of v1, it extends with:

- **Multimodal User Input**: Directly pass text + images + file blocks via a structured `message` field without needing to attach them indirectly via `references`.
- **Agent-style Tool Invocation**: Built-in tools for web search, web scraping, file reading, etc., with the ability to mount user-authorized MCP servers (Google Drive, Notion, Slack, GitHub, etc.). The model can autonomously invoke tools multiple times within a single request to complete complex tasks.
- **Structured Streaming Events**: By setting `accept: text/event-stream` or `application/x-ndjson`, you can receive token-by-token events such as `text_delta`, `tool_use`, `tool_result`, `thinking`, `citation`, `card`, `artifact`, etc., facilitating frontend rendering by event type.
- **Interruptible / Resumable**: When the model needs additional user input, it emits an `ask_user_question` event and pauses; the next call can resume by feeding back answers via `tool_results`.
- **New CRUD Actions**: Supports `retrieve` / `retrieve_batch` / `update` / `delete` via the same endpoint using the `action` field, eliminating the need for separate session management APIs.
- **Continuously Updated Model List**: Default access to contemporary models such as GPT-5.4, Claude Opus 4.7, Claude Sonnet 4.6, Gemini 3.1 Pro, GLM 5.1, DeepSeek V4, Kimi K2.5, and more.

It is also **fully backward compatible with v1 at the request body level**: simply pass `model` + `question` (+ optional `stateful` / `id` / `references` / `preset`) to get a `{answer, id}` JSON response equivalent to v1. Thus, migrating from `/aichat/conversations` only requires changing the path to `/aichat2/conversations` without rewriting the client.

> If you are currently using `/aichat/conversations`, the old interface will remain available, so you can migrate at your own pace.

## Application Process

To use AI Chat v2 API, first open the [Ace Data Cloud Console](https://platform.acedata.cloud/console/applications) and copy your API Token.

![](https://cdn.acedata.cloud/5hmkdg.jpg)

If you are not logged in, you will be redirected to sign in and brought back to this page automatically.

**A single API Token works across every service on the platform — no need to subscribe per service.** New accounts receive free starter credit; when it runs low you can top up your shared balance in the [console](https://platform.acedata.cloud/console/coin).

## Basic Usage

The simplest usage is identical to v1: pass `model` + `question` and receive `{answer, id}`.

CURL example:

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
  "answer": "AceDataCloud is a unified API platform aggregating mainstream AI models and multimodal services, allowing developers to access GPT, Claude, Gemini, Midjourney, Suno, Veo, and others with a single key.",
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
    "model": "gpt-5.4",
    "question": "Introduce AceDataCloud in one sentence.",
}

response = requests.post(url, json=payload, headers=headers)
print(response.json())
```

### Request Headers

| Header | Description |
| --- | --- |
| `accept` | Response format: `application/json` (default), `application/x-ndjson` for NDJSON streaming, or `text/event-stream` for SSE streaming |
| `authorization` | ****** obtained from your Ace Data Cloud account |

### Request Body

| Field | Type | Required | Description |
| --- | --- | --- | --- |
| `model` | string | ✅ | The model to use (see supported models below) |
| `question` | string | ❌ | The prompt or question to answer (use `question` or `message`) |
| `message` | string or array | ❌ | Multimodal message content (text, image_url, file_url blocks) |
| `id` | string | ❌ | Conversation ID for multi-turn conversations |
| `stateful` | boolean | ❌ | Enable stateful (multi-turn) conversation mode (default: `true`) |
| `preset` | string | ❌ | System-level preset (equivalent to `system_prompt`) |
| `references` | array of strings | ❌ | Image/file URLs for vision or file requests (v1 compatibility) |
| `max_turns` | integer | ❌ | Maximum tool invocation turns per request |
| `async` | boolean | ❌ | Enable async mode (default: `false`) |
| `callback_url` | string | ❌ | Callback URL for async responses |
| `allowed_skills` | array of strings | ❌ | Restrict which built-in skills are enabled |
| `allowed_mcp_servers` | array of strings | ❌ | Restrict which MCP servers the model can access |
| `unattended_policy` | object | ❌ | Policy for unattended / automated tool invocation |
| `tool_results` | array | ❌ | Tool results to resume a paused conversation |
| `messages` | array | ❌ | Full message history (advanced use) |
| `title` | string | ❌ | Conversation title (used with `action: update`) |
| `user_id` | string | ❌ | User identifier for multi-tenant scenarios |
| `application_id` | string | ❌ | Application identifier |
| `model_group` | string | ❌ | Filter by model group: `chatgpt`, `claude`, `gemini`, `grok`, `kimi`, `glm`, `deepseek` |
| `action` | string | ❌ | CRUD action: `chat` (default), `retrieve`, `retrieve_batch`, `update`, `delete` |
| `offset` | integer | ❌ | Pagination offset for `retrieve_batch` (default: `0`) |
| `limit` | integer | ❌ | Pagination limit for `retrieve_batch` (default: `100`, max: `100`) |

### Supported Models

Available `model` values include:

- **OpenAI**: `gpt-5.4-mini`, `gpt-5.4-nano`, `gpt-5.2-pro`, `gpt-5.1-all`, `gpt-5-all`, `gpt-4.1`, `gpt-4o`, `gpt-4o-image`, `gpt-4o-all`, `o3`, `o4-mini`, `o1`, `o1-mini`, `o1-pro`, `gpt-image-1`, etc.
- **Anthropic**: `claude-opus-4-8`, `claude-opus-4-7`, `claude-opus-4-6`, `claude-opus-4-5-20251101`, `claude-opus-4-1-20250805`, `claude-opus-4-20250514`, `claude-sonnet-5`, `claude-sonnet-4-6`, `claude-sonnet-4-5-20250929`, `claude-haiku-4-5-20251001`, `claude-fable-5`, etc.
- **Google**: `gemini-3.1-pro`, `gemini-3.1-pro-preview`, `gemini-3.1-flash-image-preview`, `gemini-3.1-flash-lite-preview`, `gemini-3-pro-preview`, `gemini-2.5-flash-lite`, `gemini-2.0-flash-lite`, etc.
- **xAI**: `grok-4`, `grok-4.5`, `grok-4-0709`, `grok-3`, `grok-3-fast`, etc.
- **DeepSeek**: `deepseek-v4-flash`, `deepseek-v3.2-exp`, `deepseek-v3-250324`, `deepseek-r1-0528`, `deepseek-r1`, `deepseek-chat`, `deepseek-reasoner`, etc.
- **Moonshot**: `kimi-k3`, `kimi-k2.5`, `kimi-k2-thinking`, `kimi-k2-thinking-turbo`, `kimi-k2-instruct-0905`, `kimi-k2-turbo-preview`, etc.
- **Zhipu**: `glm-5.2`, `glm-5.1`, `glm-5`, `glm-5-turbo`, `glm-4.7`, `glm-4.6`, `glm-4.5`, `glm-4.5v`, `glm-3-turbo`, etc.

## Multi-Turn Conversations

As with v1, pass `stateful: true` to enable session saving. The API returns an `id`; subsequent requests include this `id` to continue the conversation without maintaining the message history yourself.

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

Second request, with the same `id`:

```shell
curl -X POST 'https://api.acedata.cloud/aichat2/conversations' \
  -H 'accept: application/json' \
  -H 'authorization: ******' \
  -H 'content-type: application/json' \
  -d '{
    "model": "gpt-5.4",
    "stateful": true,
    "id": "f2f4b3e8-0c0a-4d3a-aaa2-7ff80c0a1c44",
    "question": "What number did I ask you to remember?"
  }'
```

Response:

```json
{
  "answer": "The number you asked me to remember is 42.",
  "id": "f2f4b3e8-0c0a-4d3a-aaa2-7ff80c0a1c44"
}
```

> The default for `stateful` is `true`. Omitting it is equivalent to explicitly passing `true`. If you do not want the server to save this conversation, explicitly set `stateful: false`.

## Streaming Responses

v2 supports two streaming formats, selectable via the `accept` header:

| Scenario | `accept` | Data Format |
| --- | --- | --- |
| Web frontend / EventSource | `text/event-stream` | `data: {json}\n\n`, ends with `data: [DONE]\n\n` |
| Server / CLI / Node streaming | `application/x-ndjson` | One JSON object per line |
| No streaming needed | `application/json` (default) | Single `{answer, id}` response |

### NDJSON Example

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

with requests.post(url, json=payload, headers=headers, stream=True) as resp:
    for line in resp.iter_lines():
        if not line:
            continue
        event = json.loads(line)
        if event.get("type") == "text_delta":
            print(event["delta_answer"], end="", flush=True)
        elif event.get("type") == "done":
            print()
            print("usage =", event.get("usage"))
```

Each NDJSON line is a structured event, most commonly `text_delta`:

```json
{"type":"text_delta","content":"Hang","delta_answer":"Hang","id":"f2f4b3e8-..."}
{"type":"text_delta","content":"zhou","delta_answer":"zhou","id":"f2f4b3e8-..."}
...
{"type":"done","conversation_id":"f2f4b3e8-...","usage":{"prompt_tokens":21,"completion_tokens":58,"total_tokens":79},"terminal_reason":"natural_stop"}
```

### SSE Example

```javascript
const resp = await fetch("https://api.acedata.cloud/aichat2/conversations", {
  method: "POST",
  headers: {
    accept: "text/event-stream",
    authorization: "******",
    "content-type": "application/json",
  },
  body: JSON.stringify({
    model: "gpt-5.4",
    stateful: true,
    question: "Introduce Hangzhou in three sentences.",
  }),
});

const reader = resp.body.getReader();
const decoder = new TextDecoder();
let buffer = "";
while (true) {
  const { value, done } = await reader.read();
  if (done) break;
  buffer += decoder.decode(value, { stream: true });
  const blocks = buffer.split("\n\n");
  buffer = blocks.pop() ?? "";
  for (const block of blocks) {
    const dataLine = block.split("\n").find((l) => l.startsWith("data: "));
    if (!dataLine) continue;
    const payload = dataLine.slice(6);
    if (payload === "[DONE]") return;
    const event = JSON.parse(payload);
    if (event.type === "text_delta") process.stdout.write(event.content);
  }
}
```

### Streaming Event Types

| `type` | Description |
| --- | --- |
| `text_delta` | Incremental text fragment of the assistant's answer. `content` is the new content; `delta_answer` equals `content` for v1 compatibility. |
| `thinking` | Model's reasoning process (only appears if the selected model exposes reasoning). |
| `tool_use` | Model decides to invoke a tool; event carries `tool_id`, `tool_name`, and `input`. |
| `tool_result` | Result of tool execution, paired with the previous `tool_use` via `tool_id`; `is_error` indicates failure. |
| `card` | Structured card output from tools (e.g., images, link previews), suitable for direct rendering. |
| `citation` | Source URLs supplementing referenced text fragments. |
| `ask_user_question` | Model requests additional user input; conversation enters `awaiting_user_input` state. |
| `artifact` | Independent artifacts generated by the model (e.g., code blocks, documents). |
| `system_message` | System prompt messages, for UI hints only. |
| `compact` | Internal context compression event, no special handling needed. |
| `error` | Error occurred in this turn; `message` describes the error. |
| `done` | Streaming response ended; includes `usage` (`prompt_tokens` / `completion_tokens` / `total_tokens`) and `terminal_reason`. |

## Multimodal Input

If user input includes images or files, pass `message` (an array) instead of `question`. Each array element is a content block:

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

- `text` — plain text, requires `text` field.
- `image_url` — image, requires `image_url.url`.
- `file_url` — file (PDF, CSV, TXT, etc.), requires `file_url.url`.

### Relation to v1 `references`

For backward compatibility, v2 still recognizes the `references: ["https://...", ...]` field:

- URLs with suffixes `jpg / jpeg / png / gif / bmp / webp / svg / heic / heif` are automatically converted to `image_url` blocks.
- Other extensions are converted to `file_url` blocks.
- If `question` is also provided, it is prepended as a `text` block.

## Tool Invocation and MCP

A core enhancement in v2 is that the model can autonomously invoke tools to complete multi-step tasks. **This is enabled by default** and requires no extra client configuration.

Common scenarios:

- User asks, "Help me search for recent exhibitions in Shanghai" → model invokes built-in web search → organizes results into an answer.
- User asks, "Read this PDF and write a summary" → model invokes file_read → writes summary.
- User has authorized Google Drive / GitHub / Notion, etc. in [Connections](https://platform.acedata.cloud/connections) → model can invoke corresponding MCP tools to read/write data.

In NDJSON / SSE streams, tool invocation is represented by `tool_use` and `tool_result` events:

```json
{"type":"tool_use","tool_id":"toolu_01ABCDEF","tool_name":"web_search","input":{"query":"Shanghai 2026 spring exhibitions"},"id":"f2f4b3e8-..."}
{"type":"tool_result","tool_id":"toolu_01ABCDEF","output":"...","is_error":false,"id":"f2f4b3e8-..."}
```

The `max_turns` parameter limits how many times the model can self-invoke tools in this request. Setting it to `1` forces a single answer without any tool invocation.

## Resuming Paused Conversations

Some tools cause the model to "ask the user" for clarification. The model emits an `ask_user_question` event and pauses:

```json
{
  "type": "ask_user_question",
  "tool_id": "toolu_01XYZW",
  "tool_name": "ask_user_question",
  "question": "Do you want the report in Chinese or English?",
  "options": ["Chinese", "English"],
  "id": "f2f4b3e8-..."
}
```

Resume the conversation by passing `tool_results` with the same `id`:

```shell
curl -X POST 'https://api.acedata.cloud/aichat2/conversations' \
  -H 'accept: text/event-stream' \
  -H 'authorization: ******' \
  -H 'content-type: application/json' \
  -d '{
    "model": "gpt-5.4",
    "stateful": true,
    "id": "f2f4b3e8-0c0a-4d3a-aaa2-7ff80c0a1c44",
    "tool_results": [
      {
        "tool_use_id": "toolu_01XYZW",
        "output": "Chinese"
      }
    ]
  }'
```

The `tool_use_id` **must** exactly match the paused `tool_id`; mismatches return 400.

## Conversation Management (CRUD)

v2 provides conversation management via the same endpoint using the `action` field.

### `action: retrieve` — Fetch a conversation

```shell
curl -X POST 'https://api.acedata.cloud/aichat2/conversations' \
  -H 'accept: application/json' \
  -H 'authorization: ******' \
  -H 'content-type: application/json' \
  -d '{
    "action": "retrieve",
    "id": "f2f4b3e8-0c0a-4d3a-aaa2-7ff80c0a1c44"
  }'
```

Returns the full conversation document (including `messages` history, `model`, `title`, `tools_used`, etc.).

### `action: retrieve_batch` — List conversation summaries

```json
{
  "action": "retrieve_batch",
  "model_group": "chatgpt",
  "limit": 20,
  "offset": 0
}
```

Returns `{ items: [...], total }`. Summaries do not include `messages`; use `action: retrieve` to fetch full messages. Optional filters: `user_id`, `application_id`, `model_group`, `model`.

### `action: update` — Change title

```json
{
  "action": "update",
  "id": "f2f4b3e8-0c0a-4d3a-aaa2-7ff80c0a1c44",
  "title": "Hangzhou Travel Plan"
}
```

### `action: delete` — Delete a conversation

```json
{
  "action": "delete",
  "id": "f2f4b3e8-0c0a-4d3a-aaa2-7ff80c0a1c44"
}
```

Returns `{ id, success: true }`. Deletion is irreversible.

## Migration from v1

If you are already using `/aichat/conversations`, migrating to v2 requires almost no code changes:

1. Change the URL from `https://api.acedata.cloud/aichat/conversations` to `https://api.acedata.cloud/aichat2/conversations`.
2. Upgrade to contemporary models (e.g., `gpt-5.4`, `claude-opus-4-7`, `gemini-3.1-pro`) when switching to v2.
3. NDJSON stream fields remain backward compatible: each `text_delta` event still carries `delta_answer` and `id`.

## Response Schema

### Success (200)

| Field | Type | Description |
| --- | --- | --- |
| `answer` | string | The model's reply to the question |
| `id` | string | Conversation ID |

### Error (400 / 401 / 404 / 429 / 500)

| Field | Type | Description |
| --- | --- | --- |
| `error.code` | string | Error code (e.g. `bad_request`, `token_mismatched`, `invalid_token`, `not_found`, `too_many_requests`, `chat_error`) |
| `error.message` | string | Human-readable error description |
| `trace_id` | string | Trace ID for debugging |

Common errors:

- `400 bad_request`: missing required fields, `tool_use_id` mismatch, invalid schema, etc.
- `401 invalid_token`: incorrect `authorization` header.
- `404 not_found`: conversation with specified `id` does not exist.
- `429 too_many_requests`: rate limit exceeded.
- `500 chat_error`: upstream LLM error.
