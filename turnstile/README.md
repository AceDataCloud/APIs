# Turnstile API

Turnstile is Ace Data Cloud's captcha solving service for Cloudflare Turnstile challenges. Users can bypass Turnstile verification automatically without any image interaction — simply submit the Website Key and URL for background decoding.

![Platform](https://img.shields.io/badge/platform-Ace%20Data%20Cloud-0f766e?style=flat-square)
![API](https://img.shields.io/badge/type-AI%20API-2563eb?style=flat-square)
![Docs](https://img.shields.io/badge/docs-online-16a34a?style=flat-square)

API home page: [Ace Data Cloud — Turnstile](https://platform.acedata.cloud/service/turnstile)

Keywords: cloudflare turnstile api, turnstile solver, turnstile bypass, captcha token, ai api, rest api, developer tools, Ace Data Cloud

---

## Why Turnstile on Ace Data Cloud

- **Protocol-level token** — submit the site key and URL, get back a ready-to-use Turnstile token without any challenge interaction.
- **Async mode** — fire-and-forget with `async: true`, then poll `/captcha/tasks` for the result.
- **One API key for everything** — a single `Authorization: Bearer` token covers all platform services.
- **Free quota for new users** — try the service before you commit.

---

## Endpoints

| Path | Purpose | Guide |
|---|---|---|
| `POST /captcha/token/turnstile` | Protocol token — returns Turnstile bypass token | [Token guide](docs/captcha_token_turnstile.md) |
| `POST /captcha/tasks` | Query async task results | Shared with other captcha services |

---

## Quick Start

```bash
curl -X POST https://api.acedata.cloud/captcha/token/turnstile \
  -H "Authorization: ******" \
  -H "Content-Type: application/json" \
  -d '{
    "website_key": "0x4AAAAAAADnPIDROrmt1Wwj",
    "website_url": "https://react-turnstile.vercel.app"
  }'
```

Response:

```json
{
  "token": "0.zScW-EiocHwwpwqtk1QXlJnGnU......",
  "elapsed": 12.4
}
```

---

## Application Process

To use the Turnstile API, go to the [Ace Data Cloud Console](https://platform.acedata.cloud/console/applications) to obtain your API Token. One token covers all platform services. A free quota is provided to first-time applicants.

---

## API Reference

| API | Path | Integration guide |
|---|---|---|
| Turnstile Token API | `POST /captcha/token/turnstile` | [Token integration guide](docs/captcha_token_turnstile.md) |
