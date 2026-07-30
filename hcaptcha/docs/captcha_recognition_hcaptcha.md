# hCaptcha Image Recognition API Integration Guide

`POST https://api.acedata.cloud/captcha/recognition/hcaptcha`

This guide introduces how to integrate the hCaptcha image recognition API, which can identify the content of an hCaptcha verification image and return the coordinates of the small image that needs to be clicked to complete the verification.

---

## Application Process

To use the hCaptcha image recognition API, first go to the [Ace Data Cloud Console](https://platform.acedata.cloud/console/applications) to obtain your API Token.

If you are not logged in or registered, you will be automatically redirected to the login page. After completing registration and login, you will be returned to the current page.

**One API Token can call all services on the platform without needing to apply separately for each service.** The first application grants a free quota for trial use; when the quota is insufficient, you can recharge the general balance in the [console](https://platform.acedata.cloud/console/coin).

> Complete Documentation: [hCaptcha Image Recognition API →](https://platform.acedata.cloud/documents/recognition-hcaptcha-integration)

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
| `queries` | string[] | ✅ | List of Base64-encoded verification images (without `data:image/...;base64,` prefix). Recommended image size ≤ 100 KB. |
| `question` | string | ✅ | The recognition question text related to the verification image, e.g. `Please click on the UNIQUE object among the others.` |
| `async` | boolean | ❌ | Pass `true` to enable async mode — returns `task_id` immediately without blocking. Default: `false`. |

---

## Response (Sync)

```json
{
  "solution": {
    "label": "Please click on the UNIQUE object among the others",
    "box": [
      "360",
      "276"
    ],
    "confidences": 0.6354503631591797
  }
}
```

| Field | Description |
|---|---|
| `solution.label` | The content recognized from the verification image. |
| `solution.box` | Coordinate `[x, y]` of the click target in the verification image. The origin is the lower-left corner of the image; x is horizontal, y is vertical. |
| `solution.confidences` | Confidence score of the recognition result. |
| `started_at` / `finished_at` | ISO-8601 UTC timestamps for when processing started and finished. |
| `elapsed` | Total processing time in seconds. |

Simulate a click at the `box` coordinates on the uploaded verification image to pass the challenge.

---

## Async Mode

By default, the API is synchronous. Pass `async: true` in the request body to enable async mode. The API immediately returns a `task_id`:

```bash
curl -X POST 'https://api.acedata.cloud/captcha/recognition/hcaptcha' \
-H 'accept: application/json' \
-H 'authorization: ******' \
-H 'content-type: application/json' \
-d '{
  "question": "Please click on the UNIQUE object among the others.",
  "queries": ["iVBORw0KGgoAAAANSU....."],
  "async": true
}'
```

```json
{
  "task_id": "61138bb6-19aa-11ec-a9c8-0242ac110002",
  "trace_id": "2efa9340-b21b-4e26-9e14-4aac95f343ab"
}
```

Poll `POST /captcha/tasks` with the `task_id` every 3–5 seconds. See the [Tasks guide](captcha_tasks.md) for details.

**Billing:** Creating a task and polling while `processing` are free. A charge is incurred only when the result is successfully returned (same price as sync mode).

---

## Examples

### cURL

```bash
curl -X POST 'https://api.acedata.cloud/captcha/recognition/hcaptcha' \
-H 'accept: application/json' \
-H 'authorization: ******' \
-H 'content-type: application/json' \
-d '{
  "question": "Please click on the UNIQUE object among the others.",
  "queries": ["iVBORw0KGgoAAAANSU.....eY+85KVlzKHav28uq/WLVhL2kHUlFMKUcZbL31S8bpd0pEPKxNllXAE2wgu3uEfj+BfAzOGelsQNFAAAAAElFTkSuQmCC"]
}'
```

### Python

```python
import requests

url = "https://api.acedata.cloud/captcha/recognition/hcaptcha"

headers = {
    "accept": "application/json",
    "authorization": "******",
    "content-type": "application/json"
}

payload = {
    "question": "Please click on the UNIQUE object among the others.",
    "queries": ["iVBORw0KGgoAAAANSU.....eY+85KVlzKHav28uq/WLVhL2kHUlFMKUcZbL31S8bpd0pEPKxNllXAE2wgu3uEfj+BfAzOGelsQNFAAAAAElFTkSuQmCC"]
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
