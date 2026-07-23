# Recaptcha Verification Code Recognition API

Recaptcha-solving APIs for image recognition plus background token generation for Recaptcha2 and Recaptcha3.

![Platform](https://img.shields.io/badge/platform-Ace%20Data%20Cloud-0f766e?style=flat-square) ![API](https://img.shields.io/badge/type-AI%20API-2563eb?style=flat-square) ![Docs](https://img.shields.io/badge/docs-online-16a34a?style=flat-square)

API home page: [Ace Data Cloud - Recaptcha2 Protocol Recognition API](https://platform.acedata.cloud/documents/captcha-token-recaptcha2)

Keywords: recaptcha-api, recaptcha2, recaptcha3, captcha-solving, token-generation, image-recognition, rest-api, ai-api, AI API, REST API, Developer API, Ace Data Cloud

## Why Use Recaptcha on Ace Data Cloud

- Unified developer platform with one API token, billing system, and usage tracking
- Production-ready API endpoints served from [https://api.acedata.cloud](https://api.acedata.cloud)
- Support for both image-click challenges and direct token workflows
- Separate guides for Recaptcha2 image recognition, Recaptcha2 token solving, and Recaptcha3 token solving

## Overview

The Recaptcha package documents three endpoints: a Recaptcha2 image recognition API for click challenges, a Recaptcha2 token API, and a Recaptcha3 token API that also requires `page_action`.

## Application Process

To use the Recaptcha APIs, open the [Ace Data Cloud Console](https://platform.acedata.cloud/console/applications) and copy your API token. One API token works across every service on the platform.

## Quick Start

- Base URL: [https://api.acedata.cloud](https://api.acedata.cloud)
- Docs: [Developer documentation](https://docs.acedata.cloud)

```bash
curl --request POST "https://api.acedata.cloud/captcha/token/recaptcha2" \
  --header "Authorization: ******" \
  --header "Content-Type: application/json" \
  --data '{
    "website_key": "6Le-wvkSAAAAAPBMRTvw0Q4Muexq9bi0DJwx_mJ-",
    "website_url": "https://www.google.com/recaptcha/api2/demo"
  }'
```

## APIs and Guides

| API | Path | Integration Guidance |
| ---- | ---- | ------------ |
| [Recaptcha2 Image Recognition API](https://platform.acedata.cloud/documents/captcha-recognition-recaptcha2) | `/captcha/recognition/recaptcha2` | [Recaptcha2 Image Recognition API Integration Guide](docs/recaptcha2_image_recognition_api_integration_guide.md) |
| [Recaptcha2 Protocol Recognition API](https://platform.acedata.cloud/documents/captcha-token-recaptcha2) | `/captcha/token/recaptcha2` | [Recaptcha2 Protocol Recognition API Integration Guide](docs/recaptcha2_protocol_recognition_api_integration_guide.md) |
| [Recaptcha3 Protocol Recognition API](https://platform.acedata.cloud/documents/captcha-token-recaptcha3) | `/captcha/token/recaptcha3` | [Recaptcha3 Protocol Recognition API Integration Guide](docs/recaptcha3_protocol_recognition_api_integration_guide.md) |

## Related Resources

- [Ace Data Cloud Developer Platform](https://platform.acedata.cloud)
- [Ace Data Cloud Docs](https://docs.acedata.cloud)
- [Status Page](https://status.acedata.cloud)
- [Ace Data Cloud GitHub Organization](https://github.com/AceDataCloud)

## Support

If you meet any issue, please check [support info](https://platform.acedata.cloud/support) or browse the latest documentation on [docs.acedata.cloud](https://docs.acedata.cloud)
