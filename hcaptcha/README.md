# hCaptcha API

Captcha-solving APIs for hCaptcha image recognition and token acquisition.

![Platform](https://img.shields.io/badge/platform-Ace%20Data%20Cloud-0f766e?style=flat-square) ![API](https://img.shields.io/badge/type-Automation%20API-2563eb?style=flat-square) ![Docs](https://img.shields.io/badge/docs-online-16a34a?style=flat-square)

API home page: [Ace Data Cloud - hCaptcha](https://platform.acedata.cloud/service/hcaptcha)

Keywords: hcaptcha-api, captcha-recognition, captcha-token, browser-automation, verification-code, rest-api, automation-api, Ace Data Cloud

## Why Use hCaptcha on Ace Data Cloud

- Unified developer platform with one API token, billing system, and usage tracking.
- Production-ready API endpoints served from https://api.acedata.cloud.
- English integration guides, API references, and service documentation.
- Shared trial quota and consistent authentication across Ace Data Cloud services.

## Overview

The hCaptcha package provides two complementary flows: solve click-based challenges with `/captcha/recognition/hcaptcha`, or request a ready-to-submit token with `/captcha/token/hcaptcha`.

## Application Process

Open the hCaptcha service page, copy your Ace Data Cloud API token, and choose either the image-recognition or token-based workflow below. The same token also works with other Ace Data Cloud services.

## Quick Start

- Base URL: [https://api.acedata.cloud](https://api.acedata.cloud)
- Service page: [hCaptcha on Ace Data Cloud](https://platform.acedata.cloud/service/hcaptcha)
- Docs: [Developer documentation](https://docs.acedata.cloud)

```bash
curl --request POST "https://api.acedata.cloud/captcha/token/hcaptcha" \
  --header "accept: application/json" \
  --header "authorization: ******" \
  --header "content-type: application/json" \
  --data '{
    "website_key": "a5f74b19-9e45-40e0-b45d-47ff91b7a6c2",
    "website_url": "https://accounts.hcaptcha.com/demo"
  }'
```

## APIs and Guides

Explore the supported endpoints and local integration guides for hCaptcha.

| API | Path | Integration Guidance |
| ---- | ---- | -------------------- |
| hCaptcha Image Recognition API | `/captcha/recognition/hcaptcha` | [hcaptcha_recognition_api_integration_guide.md](docs/hcaptcha_recognition_api_integration_guide.md) |
| hCaptcha Token API | `/captcha/token/hcaptcha` | [hcaptcha_token_api_integration_guide.md](docs/hcaptcha_token_api_integration_guide.md) |

## Related Resources

- [Ace Data Cloud Developer Platform](https://platform.acedata.cloud)
- [Ace Data Cloud Docs](https://docs.acedata.cloud)
- [Status Page](https://status.acedata.cloud)
- [Ace Data Cloud GitHub Organization](https://github.com/AceDataCloud)

## Support

If you run into issues, check [support info](https://platform.acedata.cloud/support) or browse the latest documentation on [docs.acedata.cloud](https://docs.acedata.cloud).
