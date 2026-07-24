# Cloudflare Turnstile Captcha Service

Automatically solve Cloudflare Turnstile CAPTCHA challenges by submitting the site key — no manual interaction required.

![Platform](https://img.shields.io/badge/platform-Ace%20Data%20Cloud-0f766e?style=flat-square) ![API](https://img.shields.io/badge/type-AI%20API-2563eb?style=flat-square) ![Docs](https://img.shields.io/badge/docs-online-16a34a?style=flat-square)

API home page: [Ace Data Cloud - Cloudflare Turnstile Captcha Service](https://platform.acedata.cloud/service/turnstile)

Keywords: turnstile-api, captcha, cloudflare-turnstile, captcha-solver, bypass-turnstile, rest-api, ai-api, AI API, REST API, Developer API, Ace Data Cloud

## Why Use Cloudflare Turnstile Captcha Service on Ace Data Cloud

- Unified developer platform with one API key, billing system, and usage tracking
- Production-ready API endpoints served from [https://api.acedata.cloud](https://api.acedata.cloud)
- English integration guides, API references, and service documentation
- Global-ready workflow for developers building chat, image, video, music, and search products

## Overview

The Turnstile API solves Cloudflare Turnstile CAPTCHA challenges in the background. Submit the `website_key` and `website_url` and receive a solved `token` ready to submit to the target site. An async mode is also available for non-blocking workflows.

## Application Process

To use the Turnstile API, apply for the corresponding service on the [Turnstile API](https://platform.acedata.cloud/documents/turnstile) page. After entering the page, click the "Acquire" button.

There is a free quota available for first-time applicants, allowing you to use this API for free.

## Quick Start

- Base URL: [https://api.acedata.cloud](https://api.acedata.cloud)
- Service page: [Cloudflare Turnstile Captcha Service on Ace Data Cloud](https://platform.acedata.cloud/service/turnstile)
- Docs: [Developer documentation](https://docs.acedata.cloud)

```bash
curl --request POST "https://api.acedata.cloud/captcha/token/turnstile" \
  --header "Authorization: ******" \
  --header "Content-Type: application/json" \
  --data '{
    "website_key": "0x4AAAAAAADnPIDROrmt1Wwj",
    "website_url": "https://react-turnstile.vercel.app"
  }'
```

## APIs and Guides

| API | Path | Integration Guidance |
| ---- | ---- | ------------ |
| [Turnstile API](https://platform.acedata.cloud/documents/turnstile) | `/captcha/token/turnstile` | [Turnstile API Integration Guide](docs/turnstile_api_integration_guide.md) |

## Related Resources

- [Ace Data Cloud Developer Platform](https://platform.acedata.cloud)
- [Ace Data Cloud Docs](https://docs.acedata.cloud)
- [Status Page](https://status.acedata.cloud)
- [Ace Data Cloud GitHub Organization](https://github.com/AceDataCloud)

## Support

If you meet any issue, please check [support info](https://platform.acedata.cloud/support) or browse the latest documentation on [docs.acedata.cloud](https://docs.acedata.cloud)
