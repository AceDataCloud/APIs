# hCaptcha API

hCaptcha verification code recognition service: identify and solve hCaptcha challenges automatically, supporting both image recognition and protocol-based token generation.

![Platform](https://img.shields.io/badge/platform-Ace%20Data%20Cloud-0f766e?style=flat-square) ![API](https://img.shields.io/badge/type-AI%20API-2563eb?style=flat-square) ![Docs](https://img.shields.io/badge/docs-online-16a34a?style=flat-square)

API home page: [Ace Data Cloud - hCaptcha](https://platform.acedata.cloud/service/hcaptcha)

Keywords: hcaptcha-api, captcha-recognition, captcha-solver, hcaptcha-bypass, captcha-token, rest-api, ai-api, AI API, REST API, Developer API, Ace Data Cloud

## Why Use hCaptcha API on Ace Data Cloud

- Unified developer platform with one API key, billing system, and usage tracking
- Production-ready AI API endpoints served from [https://api.acedata.cloud](https://api.acedata.cloud)
- English integration guides, API references, and service documentation
- Global-ready workflow for developers building automation, scraping, and testing products

## Overview

The hCaptcha API provides two approaches to solving hCaptcha challenges:

1. **Image Recognition API** (`/captcha/recognition/hcaptcha`): Accepts a screenshot of the hCaptcha verification image and a question string, and returns the coordinates of the image that needs to be clicked to complete the verification.
2. **Protocol Recognition API** (`/captcha/token/hcaptcha`): Accepts a website URL and website key, and returns a valid hCaptcha token that can be submitted directly to the target website, bypassing the need to interact with the visual challenge.

## Application Process

To use the hCaptcha APIs, first open the [Ace Data Cloud Console](https://platform.acedata.cloud/console/applications) and copy your API Token.

There is a free quota available for first-time applicants, allowing you to use this API for free.

## Quick Start

- Base URL: [https://api.acedata.cloud](https://api.acedata.cloud)
- Service page: [hCaptcha on Ace Data Cloud](https://platform.acedata.cloud/service/hcaptcha)
- Docs: [Developer documentation](https://docs.acedata.cloud)

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

| API | Path | Integration Guidance |
| ---- | ---- | ------------ |
| [hCaptcha Image Recognition API](https://platform.acedata.cloud/documents/recognition-hcaptcha-integration) | `/captcha/recognition/hcaptcha` | [hCaptcha Image Recognition API Integration Guide](docs/captcha_recognition_hcaptcha_api_integration_guide.md) |
| [hCaptcha Protocol Recognition API](https://platform.acedata.cloud/documents/captcha-token-hcaptcha) | `/captcha/token/hcaptcha` | [hCaptcha Protocol Recognition API Integration Guide](docs/captcha_token_hcaptcha_api_integration_guide.md) |

## Related Resources

- [Ace Data Cloud Developer Platform](https://platform.acedata.cloud)
- [Ace Data Cloud Docs](https://docs.acedata.cloud)
- [Status Page](https://status.acedata.cloud)
- [Ace Data Cloud GitHub Organization](https://github.com/AceDataCloud)

## Support

If you meet any issue, please check [support info](https://platform.acedata.cloud/support) or browse the latest documentation on [docs.acedata.cloud](https://docs.acedata.cloud)
