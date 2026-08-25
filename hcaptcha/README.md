# hCaptcha Verification Code Recognition API

Solve hCaptcha challenges using token-based protocol recognition, image recognition, and asynchronous task polling on Ace Data Cloud.

![Platform](https://img.shields.io/badge/platform-Ace%20Data%20Cloud-0f766e?style=flat-square) ![API](https://img.shields.io/badge/type-AI%20API-2563eb?style=flat-square) ![Docs](https://img.shields.io/badge/docs-online-16a34a?style=flat-square)

API home page: [Ace Data Cloud - hCaptcha Verification Code Recognition](https://platform.acedata.cloud/service/hcaptcha)

Keywords: hcaptcha-api, captcha-recognition, captcha-solver, token-recognition, image-recognition, rest-api, ai-api, AI API, REST API, Developer API, Ace Data Cloud

## Why Use hCaptcha Verification Code Recognition on Ace Data Cloud

- Unified developer platform with one API token, billing system, and usage tracking
- Production-ready API endpoints served from [https://api.acedata.cloud](https://api.acedata.cloud)
- English integration guides, API references, and service documentation
- Supports synchronous requests and asynchronous polling for multi-solver workflows

## Overview

The hCaptcha verification code recognition service provides APIs for hCaptcha token solving, hCaptcha image-coordinate recognition, and asynchronous CAPTCHA task result polling.

## Application Process

To use the hCaptcha APIs, go to the [Ace Data Cloud Console](https://platform.acedata.cloud/console/applications) to obtain your API Token. One API Token can call all services on the platform without needing to apply separately for each service.

## Quick Start

- Base URL: [https://api.acedata.cloud](https://api.acedata.cloud)
- Service page: [hCaptcha Verification Code Recognition on Ace Data Cloud](https://platform.acedata.cloud/service/hcaptcha)
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
| [hCaptcha Protocol Recognition API](https://platform.acedata.cloud/documents/captcha-token-hcaptcha) | `/captcha/token/hcaptcha` | [hCaptcha Protocol Recognition API Integration Guide](docs/hcaptcha_protocol_recognition_api_integration_guide.md) |
| [hCaptcha Image Recognition API](https://platform.acedata.cloud/documents/recognition-hcaptcha-integration) | `/captcha/recognition/hcaptcha` | [hCaptcha Image Recognition API Integration Guide](docs/hcaptcha_image_recognition_api_integration_guide.md) |
| [CAPTCHA Task Query API](https://platform.acedata.cloud/documents/captcha-tasks) | `/captcha/tasks` | [CAPTCHA Task Query API Integration Guide](docs/captcha_task_query_api_asynchronous_polling_integration_guide.md) |

## Authentication

All endpoints require an Ace Data Cloud API token in the `authorization` request header.

## Related Resources

- [Ace Data Cloud Developer Platform](https://platform.acedata.cloud)
- [Ace Data Cloud Docs](https://docs.acedata.cloud)
- [Status Page](https://status.acedata.cloud)
- [Ace Data Cloud GitHub Organization](https://github.com/AceDataCloud)

## Support

If you meet any issue, please check [support info](https://platform.acedata.cloud/support) or browse the latest documentation on [docs.acedata.cloud](https://docs.acedata.cloud)
