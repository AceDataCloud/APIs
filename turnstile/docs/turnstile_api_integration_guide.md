# Turnstile API Integration Guide

This article introduces the Turnstile API integration instructions, which automatically solves Cloudflare Turnstile CAPTCHA challenges without any manual interaction.

## Application Process

To use the Turnstile API, apply for the corresponding service on the [Turnstile API](https://platform.acedata.cloud/documents/turnstile) page. After entering the page, click the "Acquire" button.

If you are not logged in or registered, you will be automatically redirected to the login page inviting you to register and log in. After logging in or registering, you will be automatically returned to the current page.

There is a free quota available for first-time applicants, allowing you to use this API for free. **One API key can call every service on the platform — you do not need to apply separately for each service.**

## Basic Usage

Submit the `website_key` and `website_url` of the page protected by Cloudflare Turnstile. The API solves the challenge in the background and returns a `token` you can submit to the target site.

The required request body fields are:

- `website_key` (required): the Turnstile site key of the target page (e.g. `0x4AAAAAAADnPIDROrmt1Wwj`).
- `website_url` (required): the full URL of the page embedding the Turnstile widget (e.g. `https://react-turnstile.vercel.app`).

Optional fields:

- `action`: the Turnstile `action` string configured on the target site (e.g. `login`).
- `cdata`: the Turnstile `cData` string configured on the target site.
- `async`: when `true`, the API returns immediately with a `task_id` instead of blocking until the token is solved. Poll `POST /captcha/tasks` with that `task_id` to retrieve the token. Billing occurs once, only on a solved token. Default: `false`.

### Request Example

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

### Response Example

```json
{
  "token": "0.zScW-EiocHwwpwqtk1QXlJnGnU......",
  "started_at": "2026-07-24T09:34:13+00:00",
  "finished_at": "2026-07-24T09:34:50+00:00",
  "elapsed": 12.4
}
```

The response fields are:

- `token`: the solved Turnstile token to submit to the target site.
- `started_at`: ISO 8601 timestamp when the challenge solving started.
- `finished_at`: ISO 8601 timestamp when the challenge solving finished.
- `elapsed`: total elapsed time in seconds for solving the challenge.

## Async Mode

For non-blocking workflows set `async` to `true`. The API returns immediately with a `task_id`:

### Request Example

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

Poll `POST /captcha/tasks` with the returned `task_id` until the token is ready. Billing occurs once, only on a successfully solved token.

## Error Handling

The API returns standard HTTP status codes with a JSON error body:

```json
{
  "error": {
    "code": "bad_request",
    "message": "model is invalid."
  },
  "trace_id": "2efa9340-b21b-4e26-9e14-4aac95f343ab"
}
```

Common error codes:

| HTTP Status | Code | Description |
|---|---|---|
| 400 | `token_mismatched` | The specified token is not matched with the API. |
| 400 | `api_not_implemented` | The API is not implemented. |
| 400 | `disabled` | Your application has been disabled due to abnormal usage. |
| 400 | `bad_request` | Invalid request parameters. |
| 400 | `no_token` | No token specified for the request. |
| 401 | `invalid_token` | The specified token is invalid or wrong. |
| 401 | `token_expired` | The token has expired. |
| 401 | `token_mismatched` | The token and API do not match. |
| 403 | `used_up` | Insufficient balance — please top up on Ace Data Cloud. |
| 404 | `no_api` | API does not exist — check the URL. |
| 429 | `too_many_requests` | Rate limit exceeded. |
| 500 | `api_error` | Internal server error. |

## Support

If you meet any issue, please check [support info](https://platform.acedata.cloud/support) or browse the latest documentation on [docs.acedata.cloud](https://docs.acedata.cloud)
