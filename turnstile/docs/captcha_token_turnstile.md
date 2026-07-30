# Cloudflare Turnstile Token API Integration Guide

`POST https://api.acedata.cloud/captcha/token/turnstile`

This guide introduces the Cloudflare Turnstile captcha service API. Users do not need to identify or interact with the Turnstile challenge — simply submit the Website Key and URL for automatic background decoding.

---

## Application Process

To use the Turnstile Token API, first go to the [Ace Data Cloud Console](https://platform.acedata.cloud/console/applications) to obtain your API Token.

If you are not logged in or registered, you will be automatically redirected to the login page. After completing registration and login, you will be returned to the current page.

**One API Token can call all services on the platform without needing to apply separately for each service.** The first application grants a free quota for trial use; when the quota is insufficient, you can recharge the general balance in the [console](https://platform.acedata.cloud/console/coin).

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
| `website_url` | string | ✅ | The URL of the website that contains the Turnstile challenge. |
| `website_key` | string | ✅ | The Turnstile site key. Found as the `data-sitekey` attribute or in the JavaScript call to `turnstile.render()`. Example: `0x4AAAAAAADnPIDROrmt1Wwj`. |
| `action` | string | ❌ | The optional `action` string passed to the Turnstile widget. |
| `cdata` | string | ❌ | The optional `cData` string for customer data. |
| `async` | boolean | ❌ | Pass `true` to enable async mode — returns `task_id` immediately without blocking. Default: `false`. |

---

## Response (Sync)

```json
{
  "token": "0.zScW-EiocHwwpwqtk1QXlJnGnU......",
  "elapsed": 12.4
}
```

| Field | Description |
|---|---|
| `token` | The Turnstile bypass token. Submit this as `cf-turnstile-response` to the target site. For one-time use; validity depends on the site configuration. |
| `started_at` / `finished_at` | ISO-8601 UTC timestamps for when processing started and finished. |
| `elapsed` | Total processing time in seconds. |

---

## Async Mode

By default, the API is synchronous. Pass `async: true` in the request body to enable async mode. The API immediately returns a `task_id`:

```bash
curl -X POST 'https://api.acedata.cloud/captcha/token/turnstile' \
-H 'accept: application/json' \
-H 'authorization: ******' \
-H 'content-type: application/json' \
-d '{
  "website_key": "0x4AAAAAAADnPIDROrmt1Wwj",
  "website_url": "https://react-turnstile.vercel.app",
  "async": true
}'
```

```json
{
  "task_id": "61138bb6-19aa-11ec-a9c8-0242ac110002",
  "trace_id": "2efa9340-b21b-4e26-9e14-4aac95f343ab"
}
```

Poll `POST /captcha/tasks` with the `task_id` every 3–5 seconds. When complete, it returns:

```json
{
  "success": true,
  "task_id": "61138bb6-19aa-11ec-a9c8-0242ac110002",
  "status": "ready",
  "token": "0.zScW-EiocHwwpwqtk1QXlJnGnU......"
}
```

**Billing:** Creating a task and polling while `processing` are free. A charge is incurred only when the token is successfully returned (same price as sync mode).

---

## Examples

### cURL

```bash
curl -X POST 'https://api.acedata.cloud/captcha/token/turnstile' \
-H 'accept: application/json' \
-H 'authorization: ******' \
-H 'content-type: application/json' \
-d '{
  "website_key": "0x4AAAAAAADnPIDROrmt1Wwj",
  "website_url": "https://react-turnstile.vercel.app"
}'
```

### Python

```python
import requests

url = "https://api.acedata.cloud/captcha/token/turnstile"

headers = {
    "accept": "application/json",
    "authorization": "******",
    "content-type": "application/json"
}

payload = {
    "website_key": "0x4AAAAAAADnPIDROrmt1Wwj",
    "website_url": "https://react-turnstile.vercel.app"
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
| `400 disabled` | Your application has been disabled due to abnormal usage. Contact support. |
| `400 bad_request` | Invalid request body. |
| `401 invalid_token` | Unauthorized — invalid or missing authorization token. |
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
