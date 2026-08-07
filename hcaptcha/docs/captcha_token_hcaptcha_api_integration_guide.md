# hCaptcha Token API Integration Guide

`POST /captcha/token/hcaptcha` solves an hCaptcha challenge and returns a
verification token.

## Authentication

Include your API token in every request:

```http
Authorization: ******
```

## Request

| Field | Required | Description |
| --- | --- | --- |
| `website_key` | Yes | The hCaptcha site key. |
| `website_url` | Yes | URL of the page containing the hCaptcha challenge. |
| `rqdata` | No | The raw `data-rqdata` value from an hCaptcha Enterprise challenge. Omit it for standard hCaptcha challenges. |
| `proxy` | No | A bring-your-own proxy in `scheme://[user:pass@]host:port` form. Supported schemes are `http`, `https`, `socks4`, and `socks5`. |
| `async` | No | Set to `true` to return a task ID immediately and poll `POST /captcha/tasks` for the result. Defaults to `false`. |

```bash
curl --request POST "https://api.acedata.cloud/captcha/token/hcaptcha" \
  --header "accept: application/json" \
  --header "Authorization: ******" \
  --header "content-type: application/json" \
  --data '{
    "website_key": "a5f74b19-9e45-40e0-b45d-47ff91b7a6c2",
    "website_url": "https://accounts.hcaptcha.com/demo",
    "rqdata": "<enterprise-rqdata>"
  }'
```

### Response

```json
{
  "token": "P1_eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1Ni......",
  "elapsed": 31.6
}
```

When `async` is `true`, the response contains a `task_id`. Poll
[`POST /captcha/tasks`](captcha_tasks_api_integration_guide.md) until its
`status` is `ready`; the response then includes `token`.

## Errors

The endpoint can return `400` for invalid requests, `401` for an invalid or
missing API token, `403` when access is denied, `404` when the API is
unavailable, `429` when rate limited, and `500` for server errors. Error
responses include an `error` object and `trace_id`.
