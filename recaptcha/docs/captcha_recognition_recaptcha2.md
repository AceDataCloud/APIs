# reCAPTCHA2 Image Recognition API Integration Guide

`POST https://api.acedata.cloud/captcha/recognition/recaptcha2`

This guide introduces the reCAPTCHA2 image recognition API. It can identify the content of a reCAPTCHA2 verification image and return the grid cell indices that need to be clicked to complete the verification.

---

## Application Process

To use the reCAPTCHA2 image recognition API, first go to the [Ace Data Cloud Console](https://platform.acedata.cloud/console/applications) to obtain your API Token.

**One API Token can call all services on the platform without needing to apply separately for each service.** The first application grants a free quota for trial use; when the quota is insufficient, you can recharge the general balance in the [console](https://platform.acedata.cloud/console/coin).

> Complete Documentation: [reCAPTCHA2 Image Recognition API →](https://platform.acedata.cloud/documents/captcha-recognition-recaptcha2)

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
| `image` | string | ✅ | Base64-encoded reCAPTCHA2 verification image. Must be scaled to standard sizes: 100×100, 300×300, or 450×450. |
| `question` | string | ✅ | The reCAPTCHA question ID (starts with `/m/`). See the content table below. |
| `async` | boolean | ❌ | Pass `true` to enable async mode — returns `task_id` immediately without blocking. Default: `false`. |

### Question ID Content Table

| ID | English | Chinese |
|---|---|---|
| `/m/0pg52` | taxis | 出租车 |
| `/m/01bjv` | bus | 巴士 |
| `/m/02yvhj` | school bus | 校车 |
| `/m/04_sv` | motorcycles | 摩托车 |
| `/m/013xlm` | tractors | 拖拉机 |
| `/m/01jk_4` | chimneys | 烟囱 |
| `/m/014xcs` | crosswalks | 人行横道 |
| `/m/015qff` | traffic lights | 红绿灯 |
| `/m/0199g` | bicycles | 自行车 |
| `/m/015qbp` | parking meters | 停车计价表 |
| `/m/0k4j` | cars | 汽车 |
| `/m/015kr` | bridges | 桥 |
| `/m/019jd` | boats | 船 |
| `/m/0cdl1` | palm trees | 棕榈树 |
| `/m/09d_r` | mountains or hills | 山 |
| `/m/01pns0` | fire hydrant | 消防栓 |
| `/m/01lynh` | stairs | 楼梯 |

---

## Response (Sync)

```json
{
  "solution": {
    "size": 300,
    "label": "/m/01pns0",
    "confidences": [0, 0.0007, 1, 0.0003, 0.0046, 1, 0, 1, 0],
    "objects": [2, 5, 7],
    "type": "multi"
  }
}
```

| Field | Description |
|---|---|
| `solution.size` | The size of the reCAPTCHA2 verification image (e.g., 300 means 300×300). |
| `solution.label` | The question ID recognized. |
| `solution.confidences` | Confidence scores for each grid cell (0-indexed). |
| `solution.objects` | 0-indexed grid cells that match the question. Click these cells to pass verification. |
| `solution.type` | `multi` when multiple cells are selected. |
| `started_at` / `finished_at` | ISO-8601 UTC timestamps. |
| `elapsed` | Total processing time in seconds. |

The grid cells are numbered starting from 0 (top-left). Click the cells listed in `objects` to pass the challenge.

---

## Async Mode

By default, the API is synchronous. Pass `async: true` to enable async mode:

```bash
curl -X POST 'https://api.acedata.cloud/captcha/recognition/recaptcha2' \
-H 'accept: application/json' \
-H 'authorization: ******' \
-H 'content-type: application/json' \
-d '{
  "question": "/m/01pns0",
  "image": "iVBORw0KGgoAAAANSUhEUgAAASoAAAEsCAIAAAD7AWllAAAAAX...",
  "async": true
}'
```

```json
{
  "task_id": "61138bb6-19aa-11ec-a9c8-0242ac110002",
  "trace_id": "2efa9340-b21b-4e26-9e14-4aac95f343ab"
}
```

Poll `POST /captcha/tasks` every 3–5 seconds. When complete:

```json
{
  "success": true,
  "task_id": "61138bb6-19aa-11ec-a9c8-0242ac110002",
  "status": "ready",
  "solution": {
    "size": 300,
    "label": "/m/01pns0",
    "objects": [2, 5, 7],
    "type": "multi"
  }
}
```

**Billing:** Creating a task and polling while `processing` are free. A charge is incurred only when the result is successfully returned.

---

## Examples

### cURL

```bash
curl -X POST 'https://api.acedata.cloud/captcha/recognition/recaptcha2' \
-H 'accept: application/json' \
-H 'authorization: ******' \
-H 'content-type: application/json' \
-d '{
  "question": "/m/01pns0",
  "image": "iVBORw0KGgoAAAANSUhEUgAAASoAAAEsCAIAAAD7AWllAAAAAX..."
}'
```

### Python

```python
import requests

url = "https://api.acedata.cloud/captcha/recognition/recaptcha2"

headers = {
    "accept": "application/json",
    "authorization": "******",
    "content-type": "application/json"
}

payload = {
    "question": "/m/01pns0",
    "image": "iVBORw0KGgoAAAANSUhEUgAAASoAAAEsCAIAAAD7AWllAAAAAX..."
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
