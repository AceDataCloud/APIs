# reCAPTCHA API

reCAPTCHA is Ace Data Cloud's captcha solving service for Google reCAPTCHA v2 and v3 challenges. It supports both image recognition (click-based, for reCAPTCHA v2) and protocol-level token generation (for both v2 and v3), so you can bypass reCAPTCHA verification automatically.

![Platform](https://img.shields.io/badge/platform-Ace%20Data%20Cloud-0f766e?style=flat-square)
![API](https://img.shields.io/badge/type-AI%20API-2563eb?style=flat-square)
![Docs](https://img.shields.io/badge/docs-online-16a34a?style=flat-square)

API home page: [Ace Data Cloud — reCAPTCHA](https://platform.acedata.cloud/service/recaptcha)

Keywords: recaptcha api, recaptcha solver, recaptcha v2, recaptcha v3, captcha bypass, captcha recognition, ai api, rest api, developer tools, Ace Data Cloud

---

## Why reCAPTCHA on Ace Data Cloud

- **Image recognition (v2)** — submit the challenge image and question ID, get back the grid cells to click.
- **Protocol-level token (v2 & v3)** — submit the site key and URL, get back a ready-to-use `g-recaptcha-response` token.
- **Async mode** — fire-and-forget with `async: true`, then poll `/captcha/tasks` for the result.
- **One API key for everything** — a single `Authorization: Bearer` token covers all platform services.
- **Free quota for new users** — try the service before you commit.

---

## Endpoints

| Path | Purpose | Guide |
|---|---|---|
| `POST /captcha/recognition/recaptcha2` | Image recognition (v2) — returns grid cells to click | [reCAPTCHA2 Recognition guide](docs/captcha_recognition_recaptcha2.md) |
| `POST /captcha/token/recaptcha2` | Protocol token (v2) — returns bypass token | [reCAPTCHA2 Token guide](docs/captcha_token_recaptcha2.md) |
| `POST /captcha/token/recaptcha3` | Protocol token (v3) — returns bypass token | [reCAPTCHA3 Token guide](docs/captcha_token_recaptcha3.md) |
| `POST /captcha/tasks` | Query async task results | Shared with other captcha services |

---

## Quick Start

### reCAPTCHA2 protocol token

```bash
curl -X POST https://api.acedata.cloud/captcha/token/recaptcha2 \
  -H "Authorization: ******" \
  -H "Content-Type: application/json" \
  -d '{
    "website_key": "6Le-wvkSAAAAAPBMRTvw0Q4Muexq9bi0DJwx_mJ-",
    "website_url": "https://www.google.com/recaptcha/api2/demo"
  }'
```

### reCAPTCHA3 protocol token

```bash
curl -X POST https://api.acedata.cloud/captcha/token/recaptcha3 \
  -H "Authorization: ******" \
  -H "Content-Type: application/json" \
  -d '{
    "website_url": "https://recaptcha-demo.appspot.com/recaptcha-v3-request-scores.php",
    "website_key": "6LdKlZEpAAAAAAOQjzC2v_d36tWxCl6dWsozdSy9",
    "page_action": "examples/v3scores"
  }'
```

---

## Application Process

To use the reCAPTCHA API, go to the [Ace Data Cloud Console](https://platform.acedata.cloud/console/applications) to obtain your API Token. One token covers all platform services. A free quota is provided to first-time applicants.

---

## API Reference

| API | Path | Integration guide |
|---|---|---|
| reCAPTCHA2 Image Recognition API | `POST /captcha/recognition/recaptcha2` | [reCAPTCHA2 Recognition integration guide](docs/captcha_recognition_recaptcha2.md) |
| reCAPTCHA2 Token API | `POST /captcha/token/recaptcha2` | [reCAPTCHA2 Token integration guide](docs/captcha_token_recaptcha2.md) |
| reCAPTCHA3 Token API | `POST /captcha/token/recaptcha3` | [reCAPTCHA3 Token integration guide](docs/captcha_token_recaptcha3.md) |
