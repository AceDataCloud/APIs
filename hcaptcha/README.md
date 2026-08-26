# hCaptcha API

Solve hCaptcha challenges through the Ace Data Cloud API.

- Base URL: `https://api.acedata.cloud`
- Authentication: send your API token in the `Authorization` header.
- Content type: `application/json`

## Endpoints

| Endpoint | Description |
| --- | --- |
| `POST /captcha/token/hcaptcha` | Get an hCaptcha token. |
| `POST /captcha/recognition/hcaptcha` | Recognize an hCaptcha image challenge. |
| `POST /captcha/tasks` | Read the state or result of an asynchronous CAPTCHA task. |

## hCaptcha Token

`POST /captcha/token/hcaptcha` requires `website_url` and `website_key`. For an
Enterprise challenge, provide its optional `rqdata`; `proxy` is an optional
BYO proxy in `http`, `https`, `socks4`, or `socks5` form.

```bash
curl -X POST 'https://api.acedata.cloud/captcha/token/hcaptcha' \
  -H 'accept: application/json' \
  -H 'authorization: YOUR_API_TOKEN' \
  -H 'content-type: application/json' \
  -d '{
    "website_url": "https://accounts.hcaptcha.com/demo",
    "website_key": "10000000-ffff-ffff-ffff-000000000001"
  }'
```

A successful synchronous request returns a token:

```json
{
  "token": "P1_eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9",
  "started_at": 1784885653.0,
  "finished_at": 1784885655.4,
  "elapsed": 2.4
}
```

## hCaptcha Image Recognition

`POST /captcha/recognition/hcaptcha` accepts `queries`, an array of Base64
challenge-image screenshots, and `question`, the challenge instruction.

```bash
curl -X POST 'https://api.acedata.cloud/captcha/recognition/hcaptcha' \
  -H 'accept: application/json' \
  -H 'authorization: YOUR_API_TOKEN' \
  -H 'content-type: application/json' \
  -d '{
    "queries": ["data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAAB"],
    "question": "Please click on the UNIQUE object among the others."
  }'
```

The synchronous response contains `solution`. Each recognized item can contain
its click coordinate in `box`, its `label`, and `confidences`.

```json
{
  "solution": [
    {
      "box": [180, 138],
      "label": "unique object",
      "confidences": 0.6354503631591797
    }
  ],
  "started_at": 1784885653.0,
  "finished_at": 1784885655.4,
  "elapsed": 2.4
}
```

## Asynchronous Tasks

All hCaptcha endpoints support `"async": true`. Creation returns HTTP 201 with
`task_id` and `trace_id`; the server then continues processing independently of
the client. Use `POST /captcha/tasks` to read persisted task state (for example,
every 3–5 seconds). Reading a task never starts or advances processing.

```bash
curl -X POST 'https://api.acedata.cloud/captcha/tasks' \
  -H 'accept: application/json' \
  -H 'authorization: YOUR_API_TOKEN' \
  -H 'content-type: application/json' \
  -d '{"task_id":"61138bb6-19aa-11ec-a9c8-0242ac110002"}'
```

While it is running, the response is:

```json
{
  "success": true,
  "task_id": "61138bb6-19aa-11ec-a9c8-0242ac110002",
  "status": "processing"
}
```

When it is ready, `status` is `ready` and the result contains `token` for token
requests or `solution` for image-recognition requests. Ready responses also
include `started_at`, `finished_at`, and `elapsed`.

The server has a 120-second deadline. A task that does not complete returns the
following terminal HTTP 504 response on every subsequent read:

```json
{
  "detail": "The captcha task timed out.",
  "code": "timeout",
  "success": false,
  "task_id": "61138bb6-19aa-11ec-a9c8-0242ac110002",
  "status": "failed",
  "started_at": 1784885653.0,
  "finished_at": 1784885765.4,
  "elapsed": 112.4
}
```

Creating a task, reading `processing`, and timed-out tasks are not charged. A
successful result is charged once when the client first reads it. Task lookup
can also return `400 invalid_request`, `401 invalid_token`, or `404 not_found`.
