# hCaptcha Verification API

hCaptcha token solving, image recognition, and asynchronous task polling through Ace Data Cloud.

Service page: [hCaptcha Verification](https://platform.acedata.cloud/service/hcaptcha)

## Quick start

```bash
curl -X POST 'https://api.acedata.cloud/captcha/token/hcaptcha' \
  -H 'Authorization: ******' \
  -H 'Content-Type: application/json' \
  -d '{
    "website_key": "a5f74b19-9e45-40e0-b45d-47ff91b7a6c2",
    "website_url": "https://accounts.hcaptcha.com/demo"
  }'
```

## APIs

| API | Path | Guide |
|---|---|---|
| hCaptcha Token API | `/captcha/token/hcaptcha` | [Token guide](docs/captcha_token_hcaptcha_api_integration_guide.md) |
| hCaptcha Image Recognition API | `/captcha/recognition/hcaptcha` | [Recognition guide](docs/captcha_recognition_hcaptcha_api_integration_guide.md) |
| CAPTCHA Tasks API | `/captcha/tasks` | [Task guide](docs/captcha_tasks_api_integration_guide.md) |

## Authentication

All endpoints use the shared Ace Data Cloud API token in the `Authorization` header.
