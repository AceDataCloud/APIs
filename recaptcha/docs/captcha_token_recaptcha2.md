# reCAPTCHA2 Token API Integration Guide

`POST https://api.acedata.cloud/captcha/token/recaptcha2`

This guide introduces the reCAPTCHA2 protocol recognition API. Users can bypass recognizing and clicking on reCAPTCHA2 verification images — simply submit the Website Key and URL to achieve automatic background decoding.

---

## Application Process

To use the reCAPTCHA2 Token API, first go to the [Ace Data Cloud Console](https://platform.acedata.cloud/console/applications) to obtain your API Token.

**One API Token can call all services on the platform without needing to apply separately for each service.** The first application grants a free quota for trial use; when the quota is insufficient, you can recharge the general balance in the [console](https://platform.acedata.cloud/console/coin).

> Complete Documentation: [reCAPTCHA2 Protocol Recognition API →](https://platform.acedata.cloud/documents/captcha-token-recaptcha2)

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
| `website_url` | string | ✅ | The URL of the website that contains the reCAPTCHA2 verification. |
| `website_key` | string | ✅ | The reCAPTCHA2 site key (`data-sitekey`) found on the target page. |
| `proxy` | string | ❌ | Optional proxy. Format: `scheme://[user:pass@]host:port`. Supports `http`/`https`/`socks4`/`socks5`. If omitted, the platform's default proxy is used. |
| `async` | boolean | ❌ | Pass `true` to enable async mode — returns `task_id` immediately. Default: `false`. |

### Finding the website_key

Open the target page, press F12, and search for `data-sitekey` in the Elements tab. The string value is your `website_key`.

---

## Response (Sync)

```json
{
  "token": "03AFcWeA5kjJyDQ9S1a9UYimR6nuxnp......",
  "elapsed": 31.6
}
```

| Field | Description |
|---|---|
| `token` | The reCAPTCHA2 bypass token. Submit this as `g-recaptcha-response` to the target site. Valid for 120 seconds; use within 60 seconds for best results. |
| `started_at` / `finished_at` | Unix timestamps in seconds (float) for when processing started and finished. |
| `elapsed` | Total processing time in seconds. |

### Submitting the token

```bash
curl 'https://www.google.com/recaptcha/api2/demo' \
  --data-raw 'g-recaptcha-response={token}'
```

```python
import requests

token = '{token}'

data = {
    'g-recaptcha-response': token,
}

response = requests.post('https://www.google.com/recaptcha/api2/demo', data=data)
print(response.text)
```

---

## Async Mode

Pass `async: true` to enable async mode. The API immediately returns a `task_id`:

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

Querying `POST /captcha/tasks` with the `task_id` every 3–5 seconds is optional: reads do not trigger or advance processing, and server-side processing continues even if the client disconnects or exits. When complete:

```json
{
  "success": true,
  "task_id": "61138bb6-19aa-11ec-a9c8-0242ac110002",
  "status": "ready",
  "token": "03AFcWeA5kjJyDQ9S1a9UYimR6nuxnpEnAs5x2Pixao0dXZhMB......"
}
```

**Billing:** Creating a task and `processing` status reads are free. Successful completion is charged once, on the client's first successful result read; background completion alone is not charged. Tasks that are unsuccessful within the server-managed 120-second deadline terminate with an uncharged HTTP 504 timeout.

---

## Examples

### cURL

```bash
curl -X POST 'https://api.acedata.cloud/captcha/token/recaptcha2' \
-H 'accept: application/json' \
-H 'authorization: ******' \
-H 'content-type: application/json' \
-d '{
  "website_key": "6Le-wvkSAAAAAPBMRTvw0Q4Muexq9bi0DJwx_mJ-",
  "website_url": "https://www.google.com/recaptcha/api2/demo"
}'
```

### Python

```python
import requests

url = "https://api.acedata.cloud/captcha/token/recaptcha2"

headers = {
    "accept": "application/json",
    "authorization": "******",
    "content-type": "application/json"
}

payload = {
    "website_key": "6Le-wvkSAAAAAPBMRTvw0Q4Muexq9bi0DJwx_mJ-",
    "website_url": "https://www.google.com/recaptcha/api2/demo"
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
