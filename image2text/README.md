# Image2Text API

Image2Text is Ace Data Cloud's digital English captcha recognition service. It uses deep learning to recognize variable-length English numeric captchas from images, returning the captcha text.

![Platform](https://img.shields.io/badge/platform-Ace%20Data%20Cloud-0f766e?style=flat-square)
![API](https://img.shields.io/badge/type-AI%20API-2563eb?style=flat-square)
![Docs](https://img.shields.io/badge/docs-online-16a34a?style=flat-square)

API home page: [Ace Data Cloud — Image2Text](https://platform.acedata.cloud/service/image2text)

Keywords: image2text api, captcha recognition, ocr captcha, digital captcha solver, english numeric captcha, ai api, rest api, developer tools, Ace Data Cloud

---

## Why Image2Text on Ace Data Cloud

- **Deep learning OCR** — recognizes variable-length English numeric captchas with high accuracy.
- **Simple integration** — submit a Base64-encoded image, get back the text.
- **Async mode** — fire-and-forget with `async: true`, then poll `/captcha/tasks` for the result.
- **One API key for everything** — a single `Authorization: Bearer` token covers all platform services.
- **Free quota for new users** — try the service before you commit.

---

## Endpoints

| Path | Purpose | Guide |
|---|---|---|
| `POST /captcha/recognition/image2text` | Recognize text from captcha image | [Image Recognition guide](docs/captcha_recognition_image2text.md) |
| `POST /captcha/tasks` | Query async task results | Shared with other captcha services |

---

## Quick Start

```bash
curl -X POST https://api.acedata.cloud/captcha/recognition/image2text \
  -H "Authorization: ******" \
  -H "Content-Type: application/json" \
  -d '{
    "image": "<base64-encoded-captcha-image>"
  }'
```

Response:

```json
{
  "text": "7364",
  "elapsed": 1.2
}
```

---

## Application Process

To use the Image2Text API, go to the [Ace Data Cloud Console](https://platform.acedata.cloud/console/applications) to obtain your API Token. One token covers all platform services. A free quota is provided to first-time applicants.

---

## API Reference

| API | Path | Integration guide |
|---|---|---|
| Image2Text Recognition API | `POST /captcha/recognition/image2text` | [Image Recognition integration guide](docs/captcha_recognition_image2text.md) |
