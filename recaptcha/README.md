# reCAPTCHA API

Solve reCAPTCHA token and image-recognition challenges through the Ace Data
Cloud API.

- Base URL: `https://api.acedata.cloud`
- Authentication: send your API token in the `Authorization` header.
- Content type: `application/json`

## Endpoints

| Endpoint | Description |
| --- | --- |
| `POST /captcha/token/recaptcha2` | Get a reCAPTCHA v2 token. |
| `POST /captcha/token/recaptcha3` | Get a reCAPTCHA v3 token. |
| `POST /captcha/recognition/recaptcha2` | Recognize a reCAPTCHA v2 image challenge. |
| `POST /captcha/tasks` | Read the state or result of an asynchronous CAPTCHA task. |

## reCAPTCHA v2 Token

`POST /captcha/token/recaptcha2` requires `website_url` and `website_key`. An
optional `proxy` accepts a BYO proxy in `http`, `https`, `socks4`, or `socks5`
form.

```bash
curl -X POST 'https://api.acedata.cloud/captcha/token/recaptcha2' \
  -H 'accept: application/json' \
  -H 'authorization: YOUR_API_TOKEN' \
  -H 'content-type: application/json' \
  -d '{
    "website_url": "https://www.google.com/recaptcha/api2/demo",
    "website_key": "6LeIxAcTAAAAAJcZVRqyHh71UMIEGNQ_MXjiZKhI"
  }'
```

## reCAPTCHA v3 Token

`POST /captcha/token/recaptcha3` requires `website_url`, `website_key`, and
`page_action`, the action value expected by the target page.

```bash
curl -X POST 'https://api.acedata.cloud/captcha/token/recaptcha3' \
  -H 'accept: application/json' \
  -H 'authorization: YOUR_API_TOKEN' \
  -H 'content-type: application/json' \
  -d '{
    "website_url": "https://example.com/login",
    "website_key": "6LeIxAcTAAAAAJcZVRqyHh71UMIEGNQ_MXjiZKhI",
    "page_action": "login"
  }'
```

Both token endpoints return `token` with `started_at`, `finished_at`, and
`elapsed` for synchronous requests.

## reCAPTCHA v2 Image Recognition

`POST /captcha/recognition/recaptcha2` requires a Base64 `image` and the
challenge `question`.

```bash
curl -X POST 'https://api.acedata.cloud/captcha/recognition/recaptcha2' \
  -H 'accept: application/json' \
  -H 'authorization: YOUR_API_TOKEN' \
  -H 'content-type: application/json' \
  -d '{
    "image": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAAB",
    "question": "Select all images with traffic lights"
  }'
```

The response's `solution` can include `size`, `label`, `confidences`, `objects`,
and `type`, together with `started_at`, `finished_at`, and `elapsed`.

## Asynchronous Tasks

All reCAPTCHA endpoints accept `"async": true`. An HTTP 201 creation response
contains `task_id` and `trace_id`; the server manages the task after creation,
including when the client disconnects. Poll the shared `POST /captcha/tasks`
endpoint with that `task_id` only when progress needs to be checked
(recommended every 3–5 seconds). Polling reads persisted state and never
triggers or advances task processing.

```bash
curl -X POST 'https://api.acedata.cloud/captcha/tasks' \
  -H 'accept: application/json' \
  -H 'authorization: YOUR_API_TOKEN' \
  -H 'content-type: application/json' \
  -d '{"task_id":"61138bb6-19aa-11ec-a9c8-0242ac110002"}'
```

It returns `status: "processing"` while running. On completion, it returns
`status: "ready"` with `token` for token requests or `solution` for image
recognition, plus timing fields.

The 120-second deadline produces a terminal HTTP 504 response with
`detail: "The captcha task timed out."`, `code: "timeout"`, `success: false`,
`status: "failed"`, the `task_id`, and timing fields. Repeated reads return the
same result. Creating tasks, reading `processing`, and timed-out tasks are not
charged; a successful result is charged once on its first client read. Task
lookup can return `400 invalid_request`, `401 invalid_token`, or `404 not_found`.
