# Image-to-Text Captcha Recognition API

English numeric captcha recognition API that converts a Base64 captcha image into text.

![Platform](https://img.shields.io/badge/platform-Ace%20Data%20Cloud-0f766e?style=flat-square) ![API](https://img.shields.io/badge/type-AI%20API-2563eb?style=flat-square) ![Docs](https://img.shields.io/badge/docs-online-16a34a?style=flat-square)

API home page: [Ace Data Cloud - Digital English Captcha Recognition API](https://platform.acedata.cloud/documents/captcha-recognition-image2text)

Keywords: image2text-api, captcha-recognition, ocr-api, english-captcha, numeric-captcha, rest-api, ai-api, AI API, REST API, Developer API, Ace Data Cloud

## Why Use Image-to-Text on Ace Data Cloud

- Unified developer platform with one API token, billing system, and usage tracking
- Production-ready API endpoints served from [https://api.acedata.cloud](https://api.acedata.cloud)
- Simple request body with a single Base64 captcha image
- English integration guide with ready-to-run request examples

## Overview

The Image-to-Text API recognizes variable-length English numeric captchas. Submit the captcha image as Base64 and the API returns the decoded text.

## Application Process

To use the Image-to-Text API, open the [Ace Data Cloud Console](https://platform.acedata.cloud/console/applications) and copy your API token. One API token works across every service on the platform.

## Quick Start

- Base URL: [https://api.acedata.cloud](https://api.acedata.cloud)
- Docs: [Developer documentation](https://docs.acedata.cloud)

```bash
curl --request POST "https://api.acedata.cloud/captcha/recognition/image2text" \
  --header "Authorization: ******" \
  --header "Content-Type: application/json" \
  --data '{
    "image": "iVBORw0KGgoAAAANSUhEUgAAAgUAAAE3CAYAAAA6xjI2AAAAAX..."
  }'
```

## APIs and Guides

| API | Path | Integration Guidance |
| ---- | ---- | ------------ |
| [Digital English Captcha Recognition API](https://platform.acedata.cloud/documents/captcha-recognition-image2text) | `/captcha/recognition/image2text` | [Digital English Captcha Recognition API Integration Guide](docs/image2text_captcha_recognition_api_integration_guide.md) |

## Related Resources

- [Ace Data Cloud Developer Platform](https://platform.acedata.cloud)
- [Ace Data Cloud Docs](https://docs.acedata.cloud)
- [Status Page](https://status.acedata.cloud)
- [Ace Data Cloud GitHub Organization](https://github.com/AceDataCloud)

## Support

If you meet any issue, please check [support info](https://platform.acedata.cloud/support) or browse the latest documentation on [docs.acedata.cloud](https://docs.acedata.cloud)
