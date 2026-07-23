# hCaptcha Image Recognition API Integration Instructions

This guide explains how to call the hCaptcha image recognition API. Submit the challenge image plus the prompt text, and the API returns the coordinates that should be clicked.

## Application Process

To use the hCaptcha Image Recognition API, open the [Ace Data Cloud Console](https://platform.acedata.cloud/console/applications) and copy your API token.

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
| `queries` | array of strings | Recommended | Base64-encoded challenge images. |
| `question` | string | Recommended | The hCaptcha instruction text, such as `Please click on the UNIQUE object among the others.` |
| `async` | boolean | Optional | When `true`, return immediately with a `task_id` instead of blocking. Poll `POST /captcha/tasks` to retrieve the result later. |

## Request Example

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

## Response Example

```json
{
  "solution": {
    "box": ["565", "140"],
    "label": "Please click the center of the seahorses head",
    "confidences": 0.7175476551055908
  }
}
```

Use the returned `box` coordinates to simulate the click in the challenge image.

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
