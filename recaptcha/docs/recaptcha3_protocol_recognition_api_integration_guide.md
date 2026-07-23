# Recaptcha3 Protocol Recognition API Integration Instructions

This guide explains how to solve Recaptcha3 by submitting a `website_key`, `website_url`, and `page_action`. The API returns a token that can be sent to the target page.

## Application Process

To use the Recaptcha3 Protocol Recognition API, open the [Ace Data Cloud Console](https://platform.acedata.cloud/console/applications) and copy your API token.

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
| `page_action` | string | ✅ | The Recaptcha3 `action` value used by the target page. |
| `website_key` | string | ✅ | The Recaptcha3 site key from the target page. |
| `website_url` | string | ✅ | The page URL where the challenge is displayed. |
| `async` | boolean | Optional | When `true`, return immediately with a `task_id` instead of blocking. Poll `POST /captcha/tasks` to retrieve the token later. |

## Request Example

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

## Response Example

```json
{
  "token": "03AGdBq25SxXT-pmSeBXjzScW-EiocHwwpwqtk1QXlJnGnU......"
}
```

Submit the returned token to the target page as the Recaptcha3 response.

## Async Mode

If you set `"async": true`, the API returns a `task_id` immediately. Poll `POST /captcha/tasks` until the task returns `status: ready` and includes the solved token.

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
