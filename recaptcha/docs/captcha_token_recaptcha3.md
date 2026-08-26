# reCAPTCHA3 Token API Integration Guide

`POST https://api.acedata.cloud/captcha/token/recaptcha3`

This guide introduces the reCAPTCHA3 protocol recognition API. Users can complete verification without recognizing or clicking challenge images — simply submit the Website Key and URL for automatic background decoding.

---

## Application Process

To use the reCAPTCHA3 Token API, first go to the [Ace Data Cloud Console](https://platform.acedata.cloud/console/applications) to obtain your API Token.

**One API Token can call all services on the platform without needing to apply separately for each service.** The first application grants a free quota for trial use; when the quota is insufficient, you can recharge the general balance in the [console](https://platform.acedata.cloud/console/coin).

> Complete Documentation: [reCAPTCHA3 Protocol Recognition API →](https://platform.acedata.cloud/documents/captcha-token-recaptcha3)

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
| `website_url` | string | ✅ | The URL of the website that contains the reCAPTCHA3 verification. |
| `website_key` | string | ✅ | The reCAPTCHA3 site key. Found as the string passed to `.execute()` in the page source. |
| `page_action` | string | ✅ | The `action` parameter from `.execute(sitekey, {action: '...'})` in the page source. |
| `async` | boolean | ❌ | Pass `true` to enable async mode — returns `task_id` immediately. Default: `false`. |

### Finding website_key and page_action

Open F12, search for `.execute(` in the Elements tab. You will find `grecaptcha.execute(sitekey, {action: 'actionName'})` — the first argument is `website_key` and the `action` value is `page_action`.

---

## Response (Sync)

```json
{
  "token": "03AFcWeA5mfdNlQD0RGX9PTWPs0l65......",
  "elapsed": 31.6
}
```

| Field | Description |
|---|---|
| `token` | The reCAPTCHA3 bypass token. Submit as a query parameter or in the form body. Valid for 120 seconds; use within 60 seconds for best results. |
| `started_at` / `finished_at` | Unix timestamps in seconds (float) for when processing started and finished. |
| `elapsed` | Total processing time in seconds. |

### Submitting the token

```python
import requests

url = "https://recaptcha-demo.appspot.com/recaptcha-v3-verify.php?action=examples/v3scores&token={token}"

r = requests.get(url)
print(r.text)
```

Response example:

```json
{
  "success": true,
  "hostname": "recaptcha-demo.appspot.com",
  "score": 0.9,
  "action": "examples/v3scores"
}
```

---

## Async Mode

Pass `async: true` to enable async mode:

```bash
curl -X POST 'https://api.acedata.cloud/captcha/token/recaptcha3' \
-H 'accept: application/json' \
-H 'authorization: ******' \
-H 'content-type: application/json' \
-d '{
  "website_url": "https://recaptcha-demo.appspot.com/recaptcha-v3-request-scores.php",
  "website_key": "6LdKlZEpAAAAAAOQjzC2v_d36tWxCl6dWsozdSy9",
  "page_action": "examples/v3scores",
  "async": true
}'
```

```json
{
  "task_id": "61138bb6-19aa-11ec-a9c8-0242ac110002",
  "trace_id": "2efa9340-b21b-4e26-9e14-4aac95f343ab"
}
```

Querying `POST /captcha/tasks` with the `task_id` every 3–5 seconds is optional: reads do not trigger or advance processing, and server-side processing continues even if the client disconnects or exits. When complete:

```json
{
  "success": true,
  "task_id": "61138bb6-19aa-11ec-a9c8-0242ac110002",
  "status": "ready",
  "token": "03AFcWeA5mfdNlQD0RGX9PTWPs0l65QukjwbYObCue5hygRuA6......"
}
```

**Billing:** Creating a task and `processing` status reads are free. Successful completion is charged once, on the client's first successful result read; background completion alone is not charged. Tasks that are unsuccessful within the server-managed 120-second deadline terminate with an uncharged HTTP 504 timeout.

---

## Examples

### cURL

```bash
curl -X POST 'https://api.acedata.cloud/captcha/token/recaptcha3' \
-H 'accept: application/json' \
-H 'authorization: ******' \
-H 'content-type: application/json' \
-d '{
  "website_url": "https://recaptcha-demo.appspot.com/recaptcha-v3-request-scores.php",
  "website_key": "6LdKlZEpAAAAAAOQjzC2v_d36tWxCl6dWsozdSy9",
  "page_action": "examples/v3scores"
}'
```

### Python

```python
import requests

url = "https://api.acedata.cloud/captcha/token/recaptcha3"

headers = {
    "accept": "application/json",
    "authorization": "******",
    "content-type": "application/json"
}

payload = {
    "website_url": "https://recaptcha-demo.appspot.com/recaptcha-v3-request-scores.php",
    "website_key": "6LdKlZEpAAAAAAOQjzC2v_d36tWxCl6dWsozdSy9",
    "page_action": "examples/v3scores"
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
