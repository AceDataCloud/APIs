# WebExtrator Tasks API Integration Guide

`POST https://api.acedata.cloud/webextrator/tasks`

The WebExtrator Tasks API lets you look up historical `render` / `extract`
job envelopes. Useful for:

- Retrieving the result of an **async** job after the platform `POST`s it to
  your `callback_url` (or instead of polling).
- Auditing what you submitted — task records keep both the **request** body
  and the **response** envelope side by side.
- Batch back-fill — pull many tasks in one call by `id` or `trace_id`.

Task records are retained for **7 days** in Redis.

The Tasks API is **free** (no Credit consumption per call).

---

## Authentication

```
Authorization: Bearer YOUR_API_KEY
Content-Type:  application/json
```

You can only look up tasks owned by your own AceDataCloud account.

---

## Request Body

The body is a discriminated union on `action`. Two actions are supported:

### `action: "retrieve"` — single task

| Field | Type | Required | Description |
|---|---|:---:|---|
| `action` | const | ✅ | Must be `"retrieve"`. |
| `id` | string | one of | Task id (returned in `task_id` of every render/extract envelope). |
| `trace_id` | string | one of | Trace id (returned in `trace_id` of every envelope). |

Exactly one of `id` or `trace_id` must be supplied.

### `action: "retrieve_batch"` — many tasks

| Field | Type | Required | Description |
|---|---|:---:|---|
| `action` | const | ✅ | Must be `"retrieve_batch"`. |
| `ids` | string[] | one of | List of task ids. |
| `trace_ids` | string[] | one of | List of trace ids. |
| `offset` | number | ❌ | Pagination offset (default 0). |
| `limit` | number | ❌ | Page size, 1–100 (default 50). |

Exactly one of `ids` or `trace_ids` must be supplied.

---

## Response — single task

```json
{
  "task": {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "trace_id": "550e8400-e29b-41d4-a716-446655440001",
    "type": "extract",
    "created_at": 1730000000000,
    "started_at": "2026-05-02T10:30:00.123Z",
    "finished_at": "2026-05-02T10:30:02.535Z",
    "elapsed": 2.412,
    "request": {
      "url": "https://en.wikipedia.org/wiki/Diffbot",
      "expected_type": "article"
    },
    "response": {
      "success": true,
      "data": { /* the full extract envelope */ }
    }
  }
}
```

If no task is found with the given id / trace id, returns
`{ "task": null }` (HTTP 200).

---

## Response — batch

```json
{
  "items": [
    { /* same shape as single-task `.task` */ },
    { /* ... */ }
  ],
  "count": 2
}
```

Missing ids return no error — they are simply absent from `items`.

---

## Examples

### Retrieve a single task by id

```bash
curl -X POST https://api.acedata.cloud/webextrator/tasks \
  -H "Authorization: Bearer $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "action": "retrieve",
    "id": "550e8400-e29b-41d4-a716-446655440000"
  }'
```

### Retrieve a single task by trace id

```bash
curl -X POST https://api.acedata.cloud/webextrator/tasks \
  -H "Authorization: Bearer $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "action": "retrieve",
    "trace_id": "550e8400-e29b-41d4-a716-446655440001"
  }'
```

### Batch retrieve

```bash
curl -X POST https://api.acedata.cloud/webextrator/tasks \
  -H "Authorization: Bearer $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "action": "retrieve_batch",
    "ids": [
      "550e8400-e29b-41d4-a716-446655440000",
      "550e8400-e29b-41d4-a716-446655440002"
    ],
    "limit": 50
  }'
```

### Python (requests) — poll until done

```python
import os, time, requests

API_KEY = os.environ["ACEDATA_API_KEY"]
BASE = "https://api.acedata.cloud"

# 1) Fire an async extract.
queue = requests.post(
    f"{BASE}/webextrator/extract",
    headers={"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"},
    json={"url": "https://example.com", "mode": "async"},
).json()

job_id = queue["jobId"]

# 2) Poll the Tasks API until the task finishes.
while True:
    r = requests.post(
        f"{BASE}/webextrator/tasks",
        headers={"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"},
        json={"action": "retrieve", "id": job_id},
    ).json()
    task = r.get("task")
    if task and task.get("finished_at"):
        print("done in", task["elapsed"], "s")
        print(task["response"]["data"]["title"])
        break
    time.sleep(2)
```

### Node.js (fetch) — process a callback then re-fetch the full envelope

```js
// Inside your callback_url handler:
app.post('/hooks/webextrator', async (req, res) => {
  res.status(200).end();              // ack fast

  const taskId = req.body?.task_id;
  if (!taskId) return;

  const fetchRes = await fetch('https://api.acedata.cloud/webextrator/tasks', {
    method: 'POST',
    headers: {
      Authorization: `Bearer ${process.env.ACEDATA_API_KEY}`,
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ action: 'retrieve', id: taskId }),
  });
  const { task } = await fetchRes.json();
  console.log('full envelope:', task.response.data);
});
```

---

## Error Responses

| HTTP | `error.code` | Meaning |
|---|---|---|
| 400 | `bad_request` | Validation failure (missing `action`, both `id` and `trace_id` present, …). |
| 401 | `unauthorized` | Missing or invalid `Authorization: Bearer …`. |

```json
{ "error": { "code": "bad_request", "message": "..." } }
```

---

## Tips and Gotchas

- **Use trace_id when the caller chose it.** Pass `?trace_id=…` on the
  original render/extract request to make tasks searchable by your own ids
  (e.g. workflow run id). Otherwise the server generates a uuid for you.
- **Retention is 7 days.** Older tasks return `task: null` — store anything
  you need long-term on your side.
- **Tasks API is free.** Look up as often as you want; the cost was already
  paid when the original render/extract job ran.
- **Async > polling.** When practical, set `callback_url` on the original
  request so the platform delivers the envelope to you instead of you
  polling every 2 s.
