# Recaptcha Verification Code Recognition API

Recaptcha captcha solving service: recognize Recaptcha2 image challenges (click-coordinate recognition), and obtain bypass tokens for Recaptcha2 and Recaptcha3 via protocol recognition.

![Platform](https://img.shields.io/badge/platform-Ace%20Data%20Cloud-0f766e?style=flat-square) ![API](https://img.shields.io/badge/type-AI%20API-2563eb?style=flat-square) ![Docs](https://img.shields.io/badge/docs-online-16a34a?style=flat-square)

API home page: [Ace Data Cloud - Recaptcha](https://platform.acedata.cloud/documents/captcha-token-recaptcha2)

Keywords: recaptcha-api, captcha-solver, recaptcha2, recaptcha3, captcha-bypass, captcha-token, image-recognition, ai-api, REST API, Developer API, Ace Data Cloud

## Why Use Recaptcha API on Ace Data Cloud

- Unified developer platform with one API key, billing system, and usage tracking
- Production-ready AI API endpoints served from [https://api.acedata.cloud](https://api.acedata.cloud)
- English integration guides, API references, and service documentation
- Global-ready workflow for developers building automation, scraping, and verification bypass products

## Overview

The Recaptcha service provides three endpoints: an image recognition endpoint that returns the grid areas to click in a Recaptcha2 challenge, a Recaptcha2 protocol recognition (token) endpoint, and a Recaptcha3 protocol recognition (token) endpoint. Both token endpoints automatically solve the captcha in the background by accepting the website URL and site key.

## Application Process

To use the Recaptcha APIs, go to the [Ace Data Cloud Console](https://platform.acedata.cloud/console/applications) to obtain your API Token.

There is a free quota available for first-time applicants, allowing you to use this API for free.

## Quick Start

- Base URL: [https://api.acedata.cloud](https://api.acedata.cloud)
- Docs: [Developer documentation](https://docs.acedata.cloud)

```bash
curl -X POST 'https://api.acedata.cloud/captcha/token/recaptcha2' \
  -H 'accept: application/json' \
  -H 'authorization: ******' \
  -H 'content-type: application/json' \
  -d '{
    "website_key": "6Le-wvkSAAAAAPBMRTvw0Q4Muexq9bi0DJwx_mJ-",
    "website_url": "https://www.google.com/recaptcha/api2/demo"
  }'
```

## APIs and Guides

| API | Path | Integration Guidance |
| ---- | ---- | ------------ |
| [Recaptcha2 Image Recognition API](https://platform.acedata.cloud/documents/captcha-recognition-recaptcha2) | `/captcha/recognition/recaptcha2` | [Recaptcha2 Image Recognition API Integration Guide](docs/captcha_recognition_recaptcha2_integration_guide.md) |
| [Recaptcha2 Protocol Recognition API](https://platform.acedata.cloud/documents/captcha-token-recaptcha2) | `/captcha/token/recaptcha2` | [Recaptcha2 Protocol Recognition API Integration Guide](docs/captcha_token_recaptcha2_integration_guide.md) |
| [Recaptcha3 Protocol Recognition API](https://platform.acedata.cloud/documents/captcha-token-recaptcha3) | `/captcha/token/recaptcha3` | [Recaptcha3 Protocol Recognition API Integration Guide](docs/captcha_token_recaptcha3_integration_guide.md) |

## Related Resources

- [Ace Data Cloud Developer Platform](https://platform.acedata.cloud)
- [Ace Data Cloud Docs](https://docs.acedata.cloud)
- [Status Page](https://status.acedata.cloud)
- [Ace Data Cloud GitHub Organization](https://github.com/AceDataCloud)

## Support

If you meet any issue, please check [support info](https://platform.acedata.cloud/support) or browse the latest documentation on [docs.acedata.cloud](https://docs.acedata.cloud)
