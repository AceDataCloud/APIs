# Digital English Captcha Recognition API Integration Guide

`POST https://api.acedata.cloud/captcha/recognition/image2text`

This guide introduces the Digital English Captcha Recognition API integration. Based on deep learning technology, this API can recognize variable-length English numeric captchas — it takes the captcha image as input and outputs the captcha text result.

---

## Application Process

To use the Digital English Captcha Recognition API, first go to the [Ace Data Cloud Console](https://platform.acedata.cloud/console/applications) to obtain your API Token.

If you are not logged in or registered, you will be automatically redirected to the login page. After completing registration and login, you will be returned to the current page.

**One API Token can call all services on the platform without needing to apply separately for each service.** The first application grants a free quota for trial use; when the quota is insufficient, you can recharge the general balance in the [console](https://platform.acedata.cloud/console/coin).

> Complete documentation: [Digital English Captcha Recognition API →](https://platform.acedata.cloud/documents/captcha-recognition-image2text)

---

## Authentication

```
Authorization: ******
Content-Type:  application/json
```

---

## Request Body

| Field | Type | Required | Description |
|---|---|:---:|---|
| `image` | string | ✅ | Base64-encoded captcha image, without the `data:image/...;base64,` prefix. |
| `async` | boolean | ❌ | Pass `true` to enable async mode — returns `task_id` immediately without blocking. Default: `false`. |

---

## Response (Sync)

```json
{
  "text": "7364",
  "elapsed": 1.2
}
```

| Field | Description |
|---|---|
| `text` | The recognized text from the captcha image. |
| `started_at` / `finished_at` | Unix timestamps in seconds (float) for when processing started and finished. |
| `elapsed` | Total processing time in seconds. |

---

## Async Mode

By default, the API is synchronous. Pass `async: true` in the request body to enable async mode. The API immediately returns a `task_id`:

```bash
curl -X POST 'https://api.acedata.cloud/captcha/recognition/image2text' \
-H 'accept: application/json' \
-H 'authorization: ******' \
-H 'content-type: application/json' \
-d '{
  "image": "iVBORw0KGgoAAAANSUhEUgAAAgUAAAE3CAYAAAA6xjI2AAAAAX...",
  "async": true
}'
```

```json
{
  "task_id": "61138bb6-19aa-11ec-a9c8-0242ac110002",
  "trace_id": "2efa9340-b21b-4e26-9e14-4aac95f343ab"
}
```

Querying `POST /captcha/tasks` with the `task_id` every 3–5 seconds is optional: reads do not trigger or advance processing, and server-side processing continues even if the client disconnects or exits. When complete, it returns:

```json
{
  "success": true,
  "task_id": "61138bb6-19aa-11ec-a9c8-0242ac110002",
  "status": "ready",
  "text": "7364"
}
```

**Billing:** Creating a task and `processing` status reads are free. Successful completion is charged once, on the client's first successful result read (same price as sync mode); background completion alone is not charged. Tasks that are unsuccessful within the server-managed 120-second deadline terminate with an uncharged HTTP 504 timeout.

---

## Examples

### cURL

```bash
curl -X POST 'https://api.acedata.cloud/captcha/recognition/image2text' \
-H 'accept: application/json' \
-H 'authorization: ******' \
-H 'content-type: application/json' \
-d '{
  "image": "iVBORw0KGgoAAAANSUhEUgAAAgUAAAE3CAYAAAA6xjI2AAAAAX..."
}'
```

### Python

```python
import requests

url = "https://api.acedata.cloud/captcha/recognition/image2text"

headers = {
    "accept": "application/json",
    "authorization": "******",
    "content-type": "application/json"
}

payload = {
    "image": "iVBORw0KGgoAAAANSUhEUgAAAgUAAAE3CAYAAAA6xjI2AAAAAX..."
}

response = requests.post(url, json=payload, headers=headers)
print(response.text)
```

---

## Error Handling

| Code | Meaning |
|---|---|
| `400 token_mismatched` | Bad request — missing or invalid parameters. |
| `400 api_not_implemented` | Bad request — missing or invalid parameters. |
| `401 invalid_token` | Unauthorized — invalid or missing authorization token. |
| `403 forbidden` | Forbidden — the application is disabled or does not have access. |
| `404 not_found` | The requested API or resource was not found. |
| `429 too_many_requests` | Rate limit exceeded. |
| `500 api_error` | Internal server error. |

```json
{
  "success": false,
  "error": {
    "code": "api_error",
    "message": "fetch failed"
  },
  "trace_id": "2cf86e86-22a4-46e1-ac2f-032c0f2a4e89"
}
```
