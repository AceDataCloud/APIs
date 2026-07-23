# Recaptcha2 Image Recognition API Integration Instructions

This guide explains how to recognize a Recaptcha2 image challenge. Submit the challenge image plus the question identifier, and the API returns the matching tiles.

## Application Process

To use the Recaptcha2 Image Recognition API, open the [Ace Data Cloud Console](https://platform.acedata.cloud/console/applications) and copy your API token.

If you are not logged in, you will be redirected to sign in and brought back to this page automatically.

A single API token works across every service on the platform — no need to subscribe per service. New accounts receive free starter credit; when it runs low you can top up your shared balance in the [console](https://platform.acedata.cloud/console/coin).

## Request Headers

| Header | Description |
| --- | --- |
| `accept` | Response format. Use `application/json`. |
| `authorization` | Your Ace Data Cloud API token. |
| `content-type` | Use `application/json`. |

## Request Body

| Field | Type | Required | Description |
| --- | --- | --- | --- |
| `image` | string | ✅ | Base64-encoded Recaptcha2 challenge image. |
| `question` | string | ✅ | Challenge label ID such as `/m/01pns0`. |
| `async` | boolean | Optional | When `true`, return immediately with a `task_id` instead of blocking. Poll `POST /captcha/tasks` to retrieve the result later. |

## Request Example

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

## Response Example

```json
{
  "solution": {
    "size": 300,
    "type": "multi",
    "label": "/m/0k4j",
    "objects": [1, 2, 7],
    "confidences": [0.998, 0.9997, 0.9988, 0, 0.1885, 0.0002, 0.9898, 0.9993, 0.0535]
  }
}
```

Use the `objects` indexes to determine which tiles should be clicked.

## Async Mode

If you set `"async": true`, the API returns immediately with a task ID. Poll `POST /captcha/tasks` until the task is ready.

## Error Handling

Common error responses include:

- `400 token_mismatched`: missing or invalid parameters.
- `400 api_not_implemented`: unsupported request format.
- `401 invalid_token`: invalid or missing authorization token.
- `429 too_many_requests`: rate limit exceeded.
- `500 api_error`: internal server error.

### Error Response Example

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

## Support

If you meet any issue, please check [support info](https://platform.acedata.cloud/support) or browse the latest documentation on [docs.acedata.cloud](https://docs.acedata.cloud)
