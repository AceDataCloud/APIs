# Recaptcha API

Captcha-solving APIs for Recaptcha2 image recognition plus Recaptcha2 and Recaptcha3 token solving.

![Platform](https://img.shields.io/badge/platform-Ace%20Data%20Cloud-0f766e?style=flat-square) ![API](https://img.shields.io/badge/type-Automation%20API-2563eb?style=flat-square) ![Docs](https://img.shields.io/badge/docs-online-16a34a?style=flat-square)

API home page: [Ace Data Cloud - Recaptcha](https://platform.acedata.cloud/service/recaptcha)

Keywords: recaptcha-api, recaptcha2, recaptcha3, captcha-recognition, captcha-token, browser-automation, rest-api, automation-api, Ace Data Cloud

## Why Use Recaptcha on Ace Data Cloud

- Unified developer platform with one API token, billing system, and usage tracking.
- Production-ready API endpoints served from https://api.acedata.cloud.
- English integration guides, API references, and service documentation.
- Shared trial quota and consistent authentication across Ace Data Cloud services.

## Overview

The Recaptcha package supports image-based Recaptcha2 solving with `/captcha/recognition/recaptcha2`, token solving for Recaptcha2 with `/captcha/token/recaptcha2`, and score-based token solving for Recaptcha3 with `/captcha/token/recaptcha3`.

## Application Process

Open the Recaptcha service page, create or reuse your Ace Data Cloud token, and choose the guide that matches the verification flow you need. New users receive trial quota and can reuse the same token across other services.

## Quick Start

- Base URL: [https://api.acedata.cloud](https://api.acedata.cloud)
- Service page: [Recaptcha on Ace Data Cloud](https://platform.acedata.cloud/service/recaptcha)
- Docs: [Developer documentation](https://docs.acedata.cloud)

```bash
curl --request POST "https://api.acedata.cloud/captcha/token/recaptcha2" \
  --header "accept: application/json" \
  --header "authorization: ******" \
  --header "content-type: application/json" \
  --data '{
    "website_key": "6Le-wvkSAAAAAPBMRTvw0Q4Muexq9bi0DJwx_mJ-",
    "website_url": "https://www.google.com/recaptcha/api2/demo"
  }'
```

## APIs and Guides

Explore the supported endpoints and local integration guides for Recaptcha.

| API | Path | Integration Guidance |
| ---- | ---- | -------------------- |
| Recaptcha2 Image Recognition API | `/captcha/recognition/recaptcha2` | [recaptcha_recaptcha2_recognition_api_integration_guide.md](docs/recaptcha_recaptcha2_recognition_api_integration_guide.md) |
| Recaptcha2 Token API | `/captcha/token/recaptcha2` | [recaptcha_recaptcha2_token_api_integration_guide.md](docs/recaptcha_recaptcha2_token_api_integration_guide.md) |
| Recaptcha3 Token API | `/captcha/token/recaptcha3` | [recaptcha_recaptcha3_token_api_integration_guide.md](docs/recaptcha_recaptcha3_token_api_integration_guide.md) |

## Related Resources

- [Ace Data Cloud Developer Platform](https://platform.acedata.cloud)
- [Ace Data Cloud Docs](https://docs.acedata.cloud)
- [Status Page](https://status.acedata.cloud)
- [Ace Data Cloud GitHub Organization](https://github.com/AceDataCloud)

## Support

If you run into issues, check [support info](https://platform.acedata.cloud/support) or browse the latest documentation on [docs.acedata.cloud](https://docs.acedata.cloud).
