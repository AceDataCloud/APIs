# hCaptcha verification code recognition service API

This article will introduce a method for integrating the hCaptcha image recognition API, which can identify the content input by the user and the hCaptcha verification image, and finally return the coordinates of the small image that needs to be clicked to complete the verification.

![Platform](https://img.shields.io/badge/platform-Ace%20Data%20Cloud-0f766e?style=flat-square) ![API](https://img.shields.io/badge/type-AI%20API-2563eb?style=flat-square) ![Docs](https://img.shields.io/badge/docs-online-16a34a?style=flat-square)

API home page: [Ace Data Cloud - hCaptcha verification code recognition service](https://platform.acedata.cloud/documents/recognition-hcaptcha-integration)

Keywords: hcaptcha-api, hcaptcha, rest-api, ai-api, AI API, REST API, Developer API, Ace Data Cloud

## Why Use hCaptcha verification code recognition service on Ace Data Cloud

- Unified developer platform with one API key, billing system, and usage tracking
- Production-ready AI API endpoints served from [https://api.acedata.cloud](https://api.acedata.cloud)
- English integration guides, API references, and service documentation
- Global-ready workflow for developers building chat, image, video, music, and search products

## Overview

This article will introduce a method for integrating the hCaptcha image recognition API, which can identify the content input by the user and the hCaptcha verification image, and finally return the coordinates of the small image that needs to be clicked to complete the verification.

## Application Process

To use the APIs in this service, first open the [Ace Data Cloud Console](https://platform.acedata.cloud/console/applications) and copy your API Token.

![](https://cdn.acedata.cloud/5hmkdg.jpg)

If you are not logged in, you will be redirected to sign in and brought back to this page automatically.

**A single API Token works across every service on the platform — no need to subscribe per service.** New accounts receive free starter credit; when it runs low you can top up your shared balance in the [console](https://platform.acedata.cloud/console/coin).

## Quick Start

- Base URL: [https://api.acedata.cloud](https://api.acedata.cloud)
- Main docs page: [Service documentation](https://platform.acedata.cloud/documents/recognition-hcaptcha-integration)
- Docs: [Developer documentation](https://docs.acedata.cloud)

```bash
curl -X POST 'https://api.acedata.cloud/captcha/recognition/hcaptcha' \
-H 'accept: application/json' \
-H 'authorization: Bearer {token}' \
-H 'content-type: application/json' \
-d '{
  "question": "Please click on the UNIQUE object among the others.",
  "queries": ["iVBORw0KGgoAAAANSU.....eY+85KVlzKHav28uq/WLVhL2kHUlFMKUcZbL31S8bpd0pEPKxNllXAE2wgu3uEfj+BfAzOGelsQNFAAAAAElFTkSuQmCC"]
}'
```

## APIs and Guides

Explore the supported endpoints and integration guides for hCaptcha verification code recognition service.

| API | Path | Integration Guidance |
| ---- | ---- | ------------ |
| [hCaptcha Image Recognition API Integration Instructions](https://platform.acedata.cloud/documents/recognition-hcaptcha-integration) | `/captcha/recognition/hcaptcha` | [hCaptcha Image Recognition API Integration Instructions](docs/captcha_recognition_hcaptcha_api_integration_guide.md) |
| [hCaptcha Protocol Recognition API Integration Instructions](https://platform.acedata.cloud/documents/captcha-token-hcaptcha) | `/captcha/token/hcaptcha` | [hCaptcha Protocol Recognition API Integration Instructions](docs/captcha_token_hcaptcha_api_integration_guide.md) |
| [CAPTCHA Task Query API (Asynchronous Polling) Integration Instructions](https://platform.acedata.cloud/documents/captcha-tasks) | `/captcha/token/recaptcha2` | [CAPTCHA Task Query API (Asynchronous Polling) Integration Instructions](docs/captcha_tasks_api_integration_guide.md) |

## Related Resources

- [Ace Data Cloud Developer Platform](https://platform.acedata.cloud)
- [Ace Data Cloud Docs](https://docs.acedata.cloud)
- [Status Page](https://status.acedata.cloud)
- [Ace Data Cloud GitHub Organization](https://github.com/AceDataCloud)

## Support

If you meet any issue, please check [support info](https://platform.acedata.cloud/support) or browse the latest documentation on [docs.acedata.cloud](https://docs.acedata.cloud)
