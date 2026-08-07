# hCaptcha Image Recognition API Integration Guide

`POST /captcha/recognition/hcaptcha` identifies the click coordinates for an
hCaptcha image challenge.

## Authentication

```http
Authorization: ******
```

## Request

| Field | Required | Description |
| --- | --- | --- |
| `queries` | No | List of Base64-encoded hCaptcha challenge images. |
| `question` | No | The hCaptcha challenge prompt, in English or Chinese. |
| `async` | No | Set to `true` to return a task ID immediately and poll `POST /captcha/tasks` for the result. Defaults to `false`. |

```bash
curl --request POST "https://api.acedata.cloud/captcha/recognition/hcaptcha" \
  --header "accept: application/json" \
  --header "Authorization: ******" \
  --header "content-type: application/json" \
  --data '{
    "question": "Please click on the UNIQUE object among the others.",
    "queries": ["<BASE64_ENCODED_IMAGE>"]
  }'
```

### Response

```json
{
  "solution": {
    "box": ["565", "140"],
    "label": "Please click the center of the seahorses head",
    "confidences": 0.7175476551055908
  },
  "elapsed": 31.6
}
```

`solution.box` contains the coordinate to click. For asynchronous requests,
poll [`POST /captcha/tasks`](captcha_tasks_api_integration_guide.md) until
`status` is `ready`; the result is returned in `solution`.

## Errors

The endpoint can return `400` for invalid requests, `401` for an invalid or
missing API token, `403` when access is denied, `404` when the API is
unavailable, `429` when rate limited, and `500` for server errors. Error
responses include an `error` object and `trace_id`.
