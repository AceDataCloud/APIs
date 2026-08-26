# CAPTCHA Tasks API Integration Guide

`POST https://api.acedata.cloud/captcha/tasks`

The CAPTCHA Task Query API allows you to poll for the results of asynchronous CAPTCHA jobs. When you call any CAPTCHA interface (token series or recognition series) with `async: true`, the API immediately returns a `task_id`. Querying this endpoint is optional: reads do not trigger or advance processing, and server-side processing continues even if the client disconnects or exits.

This API is **free** (no credit consumption per call).

---

## Application Process

To use this API, first go to the [Ace Data Cloud Console](https://platform.acedata.cloud/console/applications) to obtain your API Token. **One API Token can call all services on the platform, no need to apply separately.**

> Complete interactive documentation: [CAPTCHA Task Query API →](https://platform.acedata.cloud/documents/captcha-tasks)

---

## Authentication

```
Authorization: ******
Content-Type:  application/json
```

---

## Usage

### Step 1: Create a task asynchronously

Pass `async: true` in any CAPTCHA API request body. The API returns a `task_id` immediately (HTTP 201):

```bash
curl -X POST 'https://api.acedata.cloud/captcha/token/recaptcha2' \
-H 'accept: application/json' \
-H 'authorization: ******' \
-H 'content-type: application/json' \
-d '{
  "website_key": "6Le-wvkSAAAAAPBMRTvw0Q4Muexq9bi0DJwx_mJ-",
  "website_url": "https://www.google.com/recaptcha/api2/demo",
  "async": true
}'
```

```json
{
  "task_id": "61138bb6-19aa-11ec-a9c8-0242ac110002",
  "trace_id": "2efa9340-b21b-4e26-9e14-4aac95f343ab"
}
```

### Step 2: Poll results using task_id

Optionally query `POST /captcha/tasks` every 3–5 seconds:

```bash
curl -X POST 'https://api.acedata.cloud/captcha/tasks' \
-H 'accept: application/json' \
-H 'authorization: ******' \
-H 'content-type: application/json' \
-d '{
  "task_id": "61138bb6-19aa-11ec-a9c8-0242ac110002"
}'
```

**While processing:**

```json
{ "success": true, "task_id": "61138bb6-19aa-11ec-a9c8-0242ac110002", "status": "processing" }
```

**When complete** — returns `status: ready` with the result:

- **Token series** (hcaptcha, recaptcha2, recaptcha3, turnstile) returns `token`:

```json
{
  "success": true,
  "task_id": "61138bb6-19aa-11ec-a9c8-0242ac110002",
  "status": "ready",
  "started_at": 1784885653.0,
  "finished_at": 1784885665.4,
  "elapsed": 12.4,
  "token": "03AFcWeA5kjJyDQ9S1a9UYimR6nuxnpEnAs5x2Pixao0dXZhMB......"
}
```

- **Recognition series** (`recognition/recaptcha2`, `recognition/hcaptcha`) returns `solution`.
- **`recognition/image2text`** returns `text`.

`/captcha/tasks` is universal to all CAPTCHA interfaces — poll with the same `task_id` regardless of which API created it.

If the task is unsuccessful within the server-managed 120-second deadline, the API returns HTTP 504 without charge. This is a terminal state: stop polling this `task_id`. Repeated queries for the same `task_id` return the same stable failure response:

```json
{
  "detail": "The captcha task timed out.",
  "code": "timeout",
  "success": false,
  "task_id": "61138bb6-19aa-11ec-a9c8-0242ac110002",
  "status": "failed",
  "started_at": 1784885653.0,
  "finished_at": 1784885765.4,
  "elapsed": 112.4
}
```

Both `status: ready` and HTTP 504 terminal responses include timing fields:

- `started_at`: when processing started, as a Unix timestamp in seconds (float).
- `finished_at`: when the task produced a result or terminal failure, as a Unix timestamp in seconds (float). This is not returned while still `processing`.
- `elapsed`: processing duration in seconds (float, rounded to 3 decimal places). This is not returned while still `processing`.

---

## Billing

In async mode, creating tasks and reads that return `status: processing` are free. Successful completion is charged once, on the client's first successful result read (same price as sync mode); background completion alone is not charged. Canceling unfinished tasks during rotation or tasks that terminate with HTTP 504 timeout incur no cost.

---

## Error Handling

| Code | Meaning |
|---|---|
| `400 invalid_request` | The request is missing the `task_id` parameter. |
| `401 invalid_token` | Unauthorized — the authorization token is invalid or missing. |
| `404 not_found` | The `task_id` does not exist or does not belong to the current account. |
| `504 timeout` | The task reached its deadline without a result. Stop polling this `task_id`; the failure is stable and not billed. |

```json
{
  "success": false,
  "error": {
    "code": "not_found",
    "message": "task not found"
  }
}
```
