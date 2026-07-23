# hCaptcha Verification Code Recognition API

hCaptcha captcha-solving APIs for image recognition and background token generation.

![Platform](https://img.shields.io/badge/platform-Ace%20Data%20Cloud-0f766e?style=flat-square) ![API](https://img.shields.io/badge/type-AI%20API-2563eb?style=flat-square) ![Docs](https://img.shields.io/badge/docs-online-16a34a?style=flat-square)

API home page: [Ace Data Cloud - hCaptcha Protocol Recognition API](https://platform.acedata.cloud/documents/captcha-token-hcaptcha)

Keywords: hcaptcha-api, captcha-solving, captcha-recognition, token-generation, image-recognition, rest-api, ai-api, AI API, REST API, Developer API, Ace Data Cloud

## Why Use hCaptcha on Ace Data Cloud

- Unified developer platform with one API token, billing system, and usage tracking
- Production-ready API endpoints served from [https://api.acedata.cloud](https://api.acedata.cloud)
- English integration guides, request examples, and response references
- Support for both image-click workflows and direct token-generation workflows

## Overview

The hCaptcha package documents two endpoints: one API recognizes which tile should be clicked in an hCaptcha image challenge, and the other solves hCaptcha by returning a ready-to-submit token from a `website_key` and `website_url`.

## Application Process

To use the hCaptcha APIs, open the [Ace Data Cloud Console](https://platform.acedata.cloud/console/applications) and copy your API token. One API token works across every service on the platform.

## Quick Start

- Base URL: [https://api.acedata.cloud](https://api.acedata.cloud)
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
| [hCaptcha Image Recognition API](https://platform.acedata.cloud/documents/recognition-hcaptcha-integration) | `/captcha/recognition/hcaptcha` | [hCaptcha Image Recognition API Integration Guide](docs/hcaptcha_image_recognition_api_integration_guide.md) |
| [hCaptcha Protocol Recognition API](https://platform.acedata.cloud/documents/captcha-token-hcaptcha) | `/captcha/token/hcaptcha` | [hCaptcha Protocol Recognition API Integration Guide](docs/hcaptcha_protocol_recognition_api_integration_guide.md) |

## Related Resources

- [Ace Data Cloud Developer Platform](https://platform.acedata.cloud)
- [Ace Data Cloud Docs](https://docs.acedata.cloud)
- [Status Page](https://status.acedata.cloud)
- [Ace Data Cloud GitHub Organization](https://github.com/AceDataCloud)

## Support

If you meet any issue, please check [support info](https://platform.acedata.cloud/support) or browse the latest documentation on [docs.acedata.cloud](https://docs.acedata.cloud)
