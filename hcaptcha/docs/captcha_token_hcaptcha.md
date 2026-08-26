# hCaptcha Token API Integration Guide

`POST https://api.acedata.cloud/captcha/token/hcaptcha`

This guide introduces the hCaptcha Protocol Recognition API. Users can bypass recognizing and clicking on hCaptcha verification images — simply submit the Website Key and URL to achieve automatic background decoding.

---

## Application Process

To use the hCaptcha Token API, first go to the [Ace Data Cloud Console](https://platform.acedata.cloud/console/applications) to obtain your API Token.

If you are not logged in or registered, you will be automatically redirected to the login page. After completing registration and login, you will be returned to the current page.

**One API Token can call all services on the platform without needing to apply separately for each service.** The first application grants a free quota for trial use; when the quota is insufficient, you can recharge the general balance in the [console](https://platform.acedata.cloud/console/coin).

> Complete Documentation: [hCaptcha Protocol Recognition API →](https://platform.acedata.cloud/documents/captcha-token-hcaptcha)

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
| `website_url` | string | ✅ | The URL of the website that contains the hCaptcha verification. |
| `website_key` | string | ✅ | The hCaptcha site key (`data-sitekey`) found on the target page. |
| `rqdata` | string | ❌ | Optional hCaptcha Enterprise `data-rqdata` value. Use the original value from the page when the challenge provides it. |
| `proxy` | string | ❌ | Optional proxy to use for solving. Format: `scheme://[user:pass@]host:port`. Supports `http`/`https`/`socks4`/`socks5`. If omitted, the platform's default proxy is used. |
| `async` | boolean | ❌ | Pass `true` to enable async mode — returns `task_id` immediately without blocking. Default: `false`. |

### Finding the website_key

Open the target page, press F12, and search for `data-sitekey` in the Elements tab. The string value is your `website_key`.

---

## Response (Sync)

```json
{
  "token": "P1_eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9......",
  "elapsed": 31.6
}
```

| Field | Description |
|---|---|
| `token` | The hCaptcha bypass token. Submit this to the target site's form field. Valid for 120 seconds; use within 60 seconds for best results. |
| `started_at` / `finished_at` | Unix timestamps in seconds (float) for when processing started and finished. |
| `elapsed` | Total processing time in seconds. |

### Submitting the token

After obtaining the token, submit it to the target website's captcha form fields. For `https://accounts.hcaptcha.com/demo`, submit to `g-recaptcha-response` and `h-captcha-response`:

```bash
curl 'https://accounts.hcaptcha.com/demo' \
  --data-raw 'email=&g-recaptcha-response={token}&h-captcha-response={token}'
```

```python
import requests

token = '{token}'

data = {
    'email': '',
    'g-recaptcha-response': token,
    'h-captcha-response': token
}

response = requests.post('https://accounts.hcaptcha.com/demo', data=data)
print(response.text)
```

---

## Async Mode

By default, the API is synchronous. Pass `async: true` in the request body to enable async mode. The API immediately returns a `task_id`:

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
  "token": "P1_eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1Ni......"
}
```

See the [Tasks guide](captcha_tasks.md) for full polling details.

**Billing:** Creating a task and `processing` status reads are free. Successful completion is charged once, on the client's first successful result read (same price as sync mode); background completion alone is not charged. Tasks that are unsuccessful within the server-managed 120-second deadline terminate with an uncharged HTTP 504 timeout.

---

## Examples

### cURL

```bash
curl -X POST 'https://api.acedata.cloud/captcha/token/hcaptcha' \
-H 'accept: application/json' \
-H 'authorization: ******' \
-H 'content-type: application/json' \
-d '{
  "website_key": "a5f74b19-9e45-40e0-b45d-47ff91b7a6c2",
  "website_url": "https://accounts.hcaptcha.com/demo"
}'
```

### Python

```python
import requests

url = "https://api.acedata.cloud/captcha/token/hcaptcha"

headers = {
    "accept": "application/json",
    "authorization": "******",
    "content-type": "application/json"
}

payload = {
    "website_key": "a5f74b19-9e45-40e0-b45d-47ff91b7a6c2",
    "website_url": "https://accounts.hcaptcha.com/demo"
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
