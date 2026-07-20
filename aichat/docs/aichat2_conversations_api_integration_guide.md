# AI Chat v2 API Integration Guide

The AI Chat v2 API (`/aichat2/conversations`) is the next generation dialogue interface, a comprehensive upgrade of the [AI Chat API](https://platform.acedata.cloud/documents/aichat-conversations). It expands on the simplicity and multi-turn dialogue hosting of v1 by adding:

- **Multimodal User Input**: Directly transmit text + images + file blocks through the structured `message` field, without needing to first attach via `references`.
- **Agent-like Tool Invocation**: Built-in tools for web search, web scraping, file reading, etc., and can mount user-authorized MCP servers (Google Drive, Notion, Slack, GitHub, etc.), allowing the model to autonomously call tools multiple times in a single request to complete complex tasks.
- **Structured Streaming Events**: By using `accept: text/event-stream` or `application/x-ndjson`, you can receive token-by-token events such as `text_delta`, `tool_use`, `tool_result`, `thinking`, `citation`, `card`, `artifact`, etc., making it easier to render them separately in the frontend by type.
- **Interruptible / Resumable**: The model will emit an `ask_user_question` event and pause when it needs additional information from the user; the next call can continue by filling in the answer through `tool_results`.
- **New CRUD Actions**: Complete `retrieve` / `retrieve_batch` / `update` / `delete` actions on the same endpoint using the `action` field, eliminating the need for additional session management APIs.
- **Continuously Updated Model List**: By default, it connects to contemporary models such as GPT-5.4, Claude Opus 4.8, Claude Sonnet 4.6, Gemini 3.1 Pro, GLM 5.1, DeepSeek V4, Kimi K3, etc.

At the same time, it is **fully backward compatible with v1** at the request body level: simply pass `model` + `question` (+ optional `stateful` / `id` / `references` / `preset`) to receive an equivalent `{answer, id}` JSON response as in v1, so migrating from `/aichat/conversations` does not require rewriting the client; just change the path to `/aichat2/conversations`.

> If you are currently using `/aichat/conversations`, the old interface will still be available for service, allowing you to migrate at your own pace.

## Application Process

To use the AI Chat v2 API, first obtain your API Token from the [Ace Data Cloud Console](https://platform.acedata.cloud/console/applications).

![](https://cdn.acedata.cloud/5hmkdg.jpg)

If you are not logged in or registered, you will be automatically redirected to the login page to invite you to register and log in, and will return to the current page automatically after completion.

**One API Token can call all services on the platform, no need to apply separately for each service.** The first application will grant free credits for a trial experience; when credits are insufficient, you can recharge the general balance in the [console](https://platform.acedata.cloud/console/coin).

## Basic Usage

The simplest usage is identical to v1: pass `model` + `question` to get `{answer, id}`.

CURL Example:

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
  "answer": "AceDataCloud is a unified API platform that aggregates mainstream AI models and multimodal services, allowing developers to access services like GPT, Claude, Gemini, Midjourney, Suno, Veo, etc., with a single key.",
  "id": "f2f4b3e8-0c0a-4d3a-aaa2-7ff80c0a1c44"
}
```

Python Example:

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

Available `model` values include:

- OpenAI: `gpt-5.4-mini`, `gpt-5.4-nano`, `gpt-5.2-pro`, `gpt-5.1-all`, `gpt-5-all`, `gpt-4.1`, `gpt-4o`, `gpt-4o-image`, `o3`, `o4-mini`, etc.
- Anthropic: `claude-opus-4-8`, `claude-opus-4-7`, `claude-opus-4-6`, `claude-opus-4-5-20251101`, `claude-sonnet-4-6`, `claude-sonnet-4-5-20250929`, `claude-haiku-4-5-20251001`, etc.
- Google: `gemini-3.1-pro`, `gemini-3.1-pro-preview`, `gemini-3.1-flash-image-preview`, `gemini-3-pro-preview`, `gemini-2.5-flash-lite`, etc.
- xAI: `grok-4`, etc.
- DeepSeek: `deepseek-v4-flash`, `deepseek-v3.2-exp`, `deepseek-r1-0528`, etc.
- Moonshot: `kimi-k3`, `kimi-k2.6`, `kimi-k2.5`, etc.
- Zhipu: `glm-5.1`, `glm-5`, `glm-5-turbo`, `glm-4.7`, `glm-4.5v`, etc.

## Multi-Turn Dialogue

Like v1, pass `stateful: true` to enable session saving, and the API will return an `id`; subsequent requests can continue the conversation by bringing back the `id`, without needing to maintain message history yourself.

First Request:

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

Second Request, bring the same `id`:

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

> `stateful` defaults to `true`, omitting it is equivalent to explicitly passing `true`. If you do not want the server to save this round of conversation, you can explicitly set `stateful: false`.

## Streaming Response

v2 supports two streaming formats, selected by the `accept` header:

| Scenario | `accept` | Data Format |
| --- | --- | --- |
| Web Frontend / EventSource | `text/event-stream` | `data: {json}\n\n`, last line `data: [DONE]\n\n` |
| Server / CLI / Node Streaming Parsing | `application/x-ndjson` | One JSON object per line |
| No Streaming | `application/json` (default) | Returns `{answer, id}` in one go |

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

Each line of NDJSON is a structured event, the most common being `text_delta`:

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

| `type` | Meaning |
| --- | --- |
| `text_delta` | Incremental text fragments of the assistant's response. `content` is the new content; for compatibility with v1, the same event also carries `delta_answer` (equal to `content`) and `id`. |
| `thinking` | The model's thinking process (only appears when the selected model exposes reasoning). |
| `tool_use` | The model decides to call a tool, the event carries `tool_id`, `tool_name`, and `input`. |
| `tool_result` | The result of the tool execution, paired with the previous `tool_use` by `tool_id`, `is_error` indicates whether it failed. |
| `card` | Structured cards produced by the tool (such as images, link previews), suitable for direct rendering. |
| `citation` | Used to supplement the source URL of the corresponding text fragment. |
| `ask_user_question` | The model issues a request for additional information from the user, entering the `awaiting_user_input` state. |
| `artifact` | Independent products generated by the model (such as code blocks, documents), which can be saved or downloaded. |
| `system_message` | System prompt information (not user and assistant content), used only for UI prompts. |
| `compact` | Events where the internal context is compressed, no special handling required. |
| `error` | An error occurred in this round, `message` describes the error content. |
| `done` | The streaming response ends, carrying `usage` (including `prompt_tokens` / `completion_tokens` / `total_tokens`) and `terminal_reason`. |

For clients that only care about the final answer, concatenating all `text_delta` `content` is equivalent to the `answer` in `application/json` mode.

## Multimodal Input

If the user input contains images or files, pass `message` (array) instead of `question`. Each array element is a content block:

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

- `text` — Plain text, the `text` field is required.
- `image_url` — Image, the `image_url.url` is required.
- `file_url` — File (PDF, CSV, TXT, etc.), the `file_url.url` is required.

### Relationship with v1 `references`

To maintain compatibility with old clients, v2 still recognizes the `references: ["https://...", ...]` field:
- URLs ending in `jpg / jpeg / png / gif / bmp / webp / svg / heic / heif` are automatically converted to `image_url` blocks.
- Other extensions are converted to `file_url` blocks.
- If a `question` is also provided, it will be placed as a `text` block in front.

Therefore, if you only want to migrate from v1 without changing the request body, just change the path to `/aichat2/conversations`, and the original `references` usage will work as usual.

## Tool Invocation and MCP

The core enhancement of v2 is that the model can autonomously call tools to complete multi-step tasks — **this is enabled by default**, and the client does not need any additional configuration. Common scenarios:

- The user asks "Help me find out what new exhibitions are in Shanghai recently" → the model calls the built-in web search → organizes the results into a response.
- The user asks "Read this PDF and then write a summary" → the model calls file_read → writes a summary.
- The user has authorized Google Drive / GitHub / Notion, etc., in [Connections](https://platform.acedata.cloud/connections) → the model can call the corresponding MCP tools to read and write their data.

In NDJSON / SSE streams, tool invocation is presented through `tool_use` and `tool_result` event types:

```json
{"type":"tool_use","tool_id":"toolu_01ABCDEF","tool_name":"web_search","input":{"query":"Shanghai 2026 spring exhibitions"},"id":"f2f4b3e8-..."}
{"type":"tool_result","tool_id":"toolu_01ABCDEF","output":"...","is_error":false,"id":"f2f4b3e8-..."}
{"type":"text_delta","content":"Currently","delta_answer":"Currently","id":"f2f4b3e8-..."}
...
```

`max_turns` can limit how many rounds the model can self-invoke tools in this request. Setting it low (for example, `max_turns: 1`) can enforce a single response without allowing any tool invocation.

## Asynchronous Execution

If your invocation comes from an alert webhook, CI/CD, or other background tasks, set `async: true` to let the interface immediately return the task ID while the background continues to execute:

```json
{
  "model": "gpt-5.5",
  "async": true,
  "question": "Summarize the latest changes in repository X..."
}
```

Return example:

```json
{
  "task_id": "f2f4b3e8-0c0a-4d3a-aaa2-7ff80c0a1c44",
  "conversation_id": "f2f4b3e8-0c0a-4d3a-aaa2-7ff80c0a1c44",
  "id": "f2f4b3e8-0c0a-4d3a-aaa2-7ff80c0a1c44",
  "status": "queued"
}
```

Use `action: retrieve` + `id` to query the session result, or provide a `callback_url` to receive a POST callback when the task completes.

For background tasks that need to call Skills or MCP Servers in unattended mode, pass the pre-authorization list:

```json
{
  "model": "gpt-5.5",
  "async": true,
  "allowed_skills": ["acedatacloud/personal-wechat"],
  "allowed_mcp_servers": [],
  "question": "..."
}
```

## Resuming Paused Conversations

When the model needs additional information from the user, it emits an `ask_user_question` event and the conversation enters the `awaiting_user_input` state:

```json
{
  "type": "ask_user_question",
  "tool_id": "toolu_01XYZW",
  "tool_name": "ask_user_question",
  "question": "Should the generated report be in English or Chinese?",
  "options": ["English", "Chinese"],
  "id": "f2f4b3e8-..."
}
```

Render this event as a card for the user to answer, then initiate the next request with the same `id`, filling in the answer through `tool_results`:

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
        "output": "English"
      }
    ]
  }'
```

The `tool_use_id` in the request body **must** exactly match the `tool_id` at the time of pause; otherwise it will return 400.

## Session Management (CRUD)

v2 provides lightweight session management through the `action` field on the same endpoint.

### `action: retrieve` — Pull a session

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

Returns the complete conversation document (including `messages` history, `model`, `title`, `tools_used`, etc.).

### `action: retrieve_batch` — List conversation summaries

```json
{
  "action": "retrieve_batch",
  "model_group": "chatgpt",
  "limit": 20,
  "offset": 0
}
```

Returns `{ items: [...], total }`. Summaries do not include `messages`; use `action: retrieve` to fetch complete messages for a specific conversation.

### `action: update` — Change title or rewrite history

```json
{
  "action": "update",
  "id": "f2f4b3e8-0c0a-4d3a-aaa2-7ff80c0a1c44",
  "title": "New Conversation Title"
}
```

### `action: delete` — Delete a conversation

```json
{
  "action": "delete",
  "id": "f2f4b3e8-0c0a-4d3a-aaa2-7ff80c0a1c44"
}
```

Returns `{ id, success: true }`. Deletion is permanent and cannot be recovered.

## Migrating from v1

If you are already using `/aichat/conversations`, migrating to v2 requires almost no code changes:

1. Change the URL from `https://api.acedata.cloud/aichat/conversations` to `https://api.acedata.cloud/aichat2/conversations`.
2. Upgrade model names to contemporary models (e.g. `gpt-5.4`, `claude-opus-4-8`, `gemini-3.1-pro`) when switching to v2.
3. The NDJSON stream remains backward compatible: each `text_delta` event still carries `delta_answer` and `id`.

After migration, you can enable new v2 capabilities (multimodal `message`, SSE, tool calls, `action` CRUD) at your own pace.

## Error Handling

Error responses are unified as:

```json
{
  "error": {
    "code": "chat_error",
    "message": "upstream LLM returned an error"
  },
  "trace_id": "2cf86e86-22a4-46e1-ac2f-032c0f2a4e89"
}
```

Common errors:

- `400 bad_request`: Missing required fields, `tool_use_id` mismatch, illegal `messages` schema, etc.
- `401 invalid_token`: Incorrect `authorization` header.
- `404 not_found`: The session corresponding to `id` does not exist during `action: retrieve / update / delete`.
- `429 too_many_requests`: Rate limit triggered.
- `500 chat_error`: Upstream LLM error.

In streaming responses, errors are sent as `{"type":"error","message":"..."}` events followed immediately by end of stream.

## Conclusion

The AI Chat v2 API maintains backward compatibility with v1 while upgrading conversations from "single-turn/multi-turn Q&A" to "agent-based observable dialogues": multimodal input, tool calls, pause/resume, streaming structured events, and built-in CRUD. New integrations are recommended to use v2 directly; existing v1 integrations can migrate smoothly in phases.
