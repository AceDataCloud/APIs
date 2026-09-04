# AI Chat v2 API Integration Guide

AI Chat v2 (`/aichat2/conversations`) is a backward-compatible upgrade of the AI Chat Conversations API. In addition to single- and multi-turn dialogue, it supports multimodal messages, structured streaming events, tool invocation, resumable conversations, and conversation CRUD actions.

## Authentication

Use an API Token from the [Ace Data Cloud Console](https://platform.acedata.cloud/console/applications):

```http
Authorization: ******
Content-Type: application/json
```

## Basic Usage

The `model` field is required. Send `question` for the v1-compatible request format:

```bash
curl -X POST 'https://api.acedata.cloud/aichat2/conversations' \
  -H 'accept: application/json' \
  -H 'authorization: ******' \
  -H 'content-type: application/json' \
  -d '{
    "model": "gpt-5.4",
    "question": "Introduce AceDataCloud in one sentence."
  }'
```

```json
{
  "answer": "AceDataCloud is a unified API platform for mainstream AI models and multimodal services.",
  "id": "f2f4b3e8-0c0a-4d3a-aaa2-7ff80c0a1c44"
}
```

Common request fields:

| Field | Type | Description |
| --- | --- | --- |
| `model` | string | Required model identifier. |
| `question` | string | v1-compatible user prompt. |
| `message` | string or array | User content; an array supports `text`, `image_url`, and `file_url` blocks. |
| `stateful` | boolean | Saves conversation state; defaults to `true`. |
| `id` | string | Conversation ID for a subsequent request or CRUD action. |
| `references` | array of strings | Reference URLs for v1-compatible multimodal requests. |
| `preset` | string | System-level prompt preset. |
| `action` | string | `chat`, `retrieve`, `retrieve_batch`, `update`, or `delete`. |
| `async` | boolean | Requests asynchronous processing. |
| `callback_url` | string | Callback URL for asynchronous processing. |

## Multi-Turn Conversations

Set `stateful` to `true` and include the returned `id` in the next request:

```json
{
  "model": "gpt-5.4",
  "stateful": true,
  "id": "f2f4b3e8-0c0a-4d3a-aaa2-7ff80c0a1c44",
  "question": "What did I just ask?"
}
```

## Streaming Responses

Set `accept` to `application/x-ndjson` for one JSON event per line, or `text/event-stream` for server-sent events. A text event includes `type: "text_delta"`, `content`, `delta_answer`, and `id`; the terminal event has `type: "done"`.

```python
import json
import requests

response = requests.post(
    "https://api.acedata.cloud/aichat2/conversations",
    headers={
        "accept": "application/x-ndjson",
        "authorization": "******",
        "content-type": "application/json",
    },
    json={"model": "gpt-5.4", "question": "Hello"},
    stream=True,
)

for line in response.iter_lines():
    if line:
        event = json.loads(line)
        if event.get("type") == "text_delta":
            print(event["delta_answer"], end="", flush=True)
```

## Conversation Actions

Use `action` to manage saved conversations:

```json
{ "action": "retrieve", "id": "f2f4b3e8-0c0a-4d3a-aaa2-7ff80c0a1c44" }
```

```json
{ "action": "retrieve_batch", "model_group": "chatgpt", "limit": 20, "offset": 0 }
```

```json
{ "action": "update", "id": "f2f4b3e8-0c0a-4d3a-aaa2-7ff80c0a1c44", "title": "Travel Plan" }
```

```json
{ "action": "delete", "id": "f2f4b3e8-0c0a-4d3a-aaa2-7ff80c0a1c44" }
```

`retrieve` returns the complete conversation, `retrieve_batch` returns `{ "items": [...], "total": 0 }`, and `delete` returns `{ "id": "...", "success": true }`.
