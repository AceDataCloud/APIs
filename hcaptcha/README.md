# hCaptcha Recognition API

Solve hCaptcha challenges with either a verification token or image-recognition
coordinates.

![Platform](https://img.shields.io/badge/platform-Ace%20Data%20Cloud-0f766e?style=flat-square) ![API](https://img.shields.io/badge/type-AI%20API-2563eb?style=flat-square) ![Docs](https://img.shields.io/badge/docs-online-16a34a?style=flat-square)

## Quick Start

- Base URL: [https://api.acedata.cloud](https://api.acedata.cloud)
- Authentication: `Authorization: ******`

```bash
curl --request POST "https://api.acedata.cloud/captcha/token/hcaptcha" \
  --header "Authorization: ******" \
  --header "Content-Type: application/json" \
  --data '{
    "website_key": "a5f74b19-9e45-40e0-b45d-47ff91b7a6c2",
    "website_url": "https://accounts.hcaptcha.com/demo"
  }'
```

## APIs and Guides

| API | Path | Integration guide |
| --- | --- | --- |
| hCaptcha Token API | `POST /captcha/token/hcaptcha` | [Token API guide](docs/captcha_token_hcaptcha_api_integration_guide.md) |
| hCaptcha Image Recognition API | `POST /captcha/recognition/hcaptcha` | [Image Recognition API guide](docs/captcha_recognition_hcaptcha_api_integration_guide.md) |
| Captcha Tasks API | `POST /captcha/tasks` | [Tasks API guide](docs/captcha_tasks_api_integration_guide.md) |

## Support

For help, visit [Ace Data Cloud support](https://platform.acedata.cloud/support)
or [the latest documentation](https://docs.acedata.cloud).
