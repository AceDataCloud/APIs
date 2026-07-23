# hCaptcha Verification Code Recognition API

hCaptcha captcha solving service: recognize hCaptcha image challenges (click-coordinate recognition) and obtain bypass tokens via protocol recognition.

![Platform](https://img.shields.io/badge/platform-Ace%20Data%20Cloud-0f766e?style=flat-square) ![API](https://img.shields.io/badge/type-AI%20API-2563eb?style=flat-square) ![Docs](https://img.shields.io/badge/docs-online-16a34a?style=flat-square)

API home page: [Ace Data Cloud - hCaptcha](https://platform.acedata.cloud/documents/captcha-token-hcaptcha)

Keywords: hcaptcha-api, captcha-solver, captcha-recognition, captcha-bypass, hcaptcha-token, image-recognition, ai-api, REST API, Developer API, Ace Data Cloud

## Why Use hCaptcha API on Ace Data Cloud

- Unified developer platform with one API key, billing system, and usage tracking
- Production-ready AI API endpoints served from [https://api.acedata.cloud](https://api.acedata.cloud)
- English integration guides, API references, and service documentation
- Global-ready workflow for developers building automation, scraping, and verification bypass products

## Overview

The hCaptcha service provides two endpoints: an image recognition endpoint that returns the coordinates of the target area to click in a hCaptcha challenge, and a protocol recognition (token) endpoint that automatically solves the hCaptcha challenge in the background by accepting the website URL and site key.

## Application Process

To use the hCaptcha APIs, go to the [Ace Data Cloud Console](https://platform.acedata.cloud/console/applications) to obtain your API Token.

There is a free quota available for first-time applicants, allowing you to use this API for free.

## Quick Start

- Base URL: [https://api.acedata.cloud](https://api.acedata.cloud)
- Docs: [Developer documentation](https://docs.acedata.cloud)

```bash
curl -X POST 'https://api.acedata.cloud/captcha/token/hcaptcha' \
  -H 'accept: application/json' \
  -H 'authorization: ******' \
  -H 'content-type: application/json' \
  -d '{
    "website_key": "a5f74b19-9e45-40e0-b45d-47ff91b7a6c2",
    "website_url": "https://accounts.hcaptcha.com/demo"
  }'
```

## APIs and Guides

| API | Path | Integration Guidance |
| ---- | ---- | ------------ |
| [hCaptcha Image Recognition API](https://platform.acedata.cloud/documents/recognition-hcaptcha-integration) | `/captcha/recognition/hcaptcha` | [hCaptcha Image Recognition API Integration Guide](docs/captcha_recognition_hcaptcha_integration_guide.md) |
| [hCaptcha Protocol Recognition API](https://platform.acedata.cloud/documents/captcha-token-hcaptcha) | `/captcha/token/hcaptcha` | [hCaptcha Protocol Recognition API Integration Guide](docs/captcha_token_hcaptcha_integration_guide.md) |

## Related Resources

- [Ace Data Cloud Developer Platform](https://platform.acedata.cloud)
- [Ace Data Cloud Docs](https://docs.acedata.cloud)
- [Status Page](https://status.acedata.cloud)
- [Ace Data Cloud GitHub Organization](https://github.com/AceDataCloud)

## Support

If you meet any issue, please check [support info](https://platform.acedata.cloud/support) or browse the latest documentation on [docs.acedata.cloud](https://docs.acedata.cloud)
