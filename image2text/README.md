# Image2Text CAPTCHA Recognition API

Recognize text in CAPTCHA images through the Ace Data Cloud API.

- Base URL: `https://api.acedata.cloud`
- Authentication: send your API token in the `Authorization` header.
- Endpoint: `POST /captcha/recognition/image2text`

## Recognize a CAPTCHA

Send the CAPTCHA image as a Base64 string in the required `image` field.

```bash
curl -X POST 'https://api.acedata.cloud/captcha/recognition/image2text' \
  -H 'accept: application/json' \
  -H 'authorization: YOUR_API_TOKEN' \
  -H 'content-type: application/json' \
  -d '{
    "image": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAAB"
  }'
```

The synchronous response returns the recognized text:

```json
{
  "text": "7364",
  "started_at": 1784885653.0,
  "finished_at": 1784885655.4,
  "elapsed": 2.4
}
```

## Asynchronous Tasks

Add `"async": true` to create an asynchronous task. The HTTP 201 response
contains `task_id` and `trace_id`. The server continues processing even if the
client disconnects or never polls.

Read the result with the shared `POST /captcha/tasks` endpoint:

```bash
curl -X POST 'https://api.acedata.cloud/captcha/tasks' \
  -H 'accept: application/json' \
  -H 'authorization: YOUR_API_TOKEN' \
  -H 'content-type: application/json' \
  -d '{"task_id":"61138bb6-19aa-11ec-a9c8-0242ac110002"}'
```

Task lookup is observational: it does not trigger or advance processing. It
returns `status: "processing"` while running, then `status: "ready"` with
`text`, `started_at`, `finished_at`, and `elapsed`. Polling every 3–5 seconds is
recommended when progress must be checked.

Tasks have a 120-second deadline. If a task cannot complete, task lookup returns
terminal HTTP 504 with `code: "timeout"`, `success: false`, `status: "failed"`,
the `task_id`, and timing fields. Repeated reads return the same failure.

Creating a task, reading `processing`, and timeouts are not charged. The first
client read of a successful result is charged once. Task lookup can return
`400 invalid_request`, `401 invalid_token`, or `404 not_found`.
