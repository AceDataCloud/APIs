# hCaptcha API

hCaptcha is Ace Data Cloud's captcha solving service for hCaptcha challenges. It supports both image recognition (click-based) and protocol-level token generation, so you can bypass hCaptcha verification automatically.

![Platform](https://img.shields.io/badge/platform-Ace%20Data%20Cloud-0f766e?style=flat-square)
![API](https://img.shields.io/badge/type-AI%20API-2563eb?style=flat-square)
![Docs](https://img.shields.io/badge/docs-online-16a34a?style=flat-square)

API home page: [Ace Data Cloud — hCaptcha](https://platform.acedata.cloud/service/hcaptcha)

Keywords: hcaptcha api, captcha solver, captcha recognition, hcaptcha token, captcha bypass, ai api, rest api, developer tools, Ace Data Cloud

---

## Why hCaptcha on Ace Data Cloud

- **Image recognition** — submit the challenge image and question, get back the coordinates to click.
- **Protocol-level token** — submit the site key and URL, get back a ready-to-use token without any image interaction.
- **Async mode** — fire-and-forget with `async: true`, then poll `/captcha/tasks` for the result.
- **One API key for everything** — a single `Authorization: Bearer` token covers all platform services.
- **Free quota for new users** — try the service before you commit.

---

## Endpoints

| Path | Purpose | Guide |
|---|---|---|
| `POST /captcha/recognition/hcaptcha` | Image recognition — returns click coordinates | [Image Recognition guide](docs/captcha_recognition_hcaptcha.md) |
| `POST /captcha/token/hcaptcha` | Protocol token — returns bypass token | [Token guide](docs/captcha_token_hcaptcha.md) |
| `POST /captcha/tasks` | Query async task results | [Tasks guide](docs/captcha_tasks.md) |

---

## Quick Start

### Image recognition

```bash
curl -X POST https://api.acedata.cloud/captcha/recognition/hcaptcha \
  -H "Authorization: ******" \
  -H "Content-Type: application/json" \
  -d '{
    "question": "Please click on the UNIQUE object among the others.",
    "queries": ["<base64-image>"]
  }'
```

### Protocol token

```bash
curl -X POST https://api.acedata.cloud/captcha/token/hcaptcha \
  -H "Authorization: ******" \
  -H "Content-Type: application/json" \
  -d '{
    "website_key": "a5f74b19-9e45-40e0-b45d-47ff91b7a6c2",
    "website_url": "https://accounts.hcaptcha.com/demo"
  }'
```

---

## Application Process

To use the hCaptcha API, go to the [Ace Data Cloud Console](https://platform.acedata.cloud/console/applications) to obtain your API Token. One token covers all platform services. A free quota is provided to first-time applicants.

---

## API Reference

| API | Path | Integration guide |
|---|---|---|
| hCaptcha Image Recognition API | `POST /captcha/recognition/hcaptcha` | [Image Recognition integration guide](docs/captcha_recognition_hcaptcha.md) |
| hCaptcha Token API | `POST /captcha/token/hcaptcha` | [Token integration guide](docs/captcha_token_hcaptcha.md) |
| CAPTCHA Tasks API | `POST /captcha/tasks` | [Tasks integration guide](docs/captcha_tasks.md) |
