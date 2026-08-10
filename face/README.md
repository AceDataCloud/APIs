# Face Transformation API

Face analysis and transformation service: detect keypoints, beautify portraits, change age/gender, swap faces, cartoonify, and detect liveness.

![Platform](https://img.shields.io/badge/platform-Ace%20Data%20Cloud-0f766e?style=flat-square) ![API](https://img.shields.io/badge/type-AI%20API-2563eb?style=flat-square) ![Docs](https://img.shields.io/badge/docs-online-16a34a?style=flat-square)

API home page: [Ace Data Cloud - Face Transformation](https://platform.acedata.cloud/service/face-change)

Keywords: face-api, face-swap, face-detection, beautify, face-cartoon, age-change, gender-change, liveness, image-api, ai-api, AI API, REST API, Developer API, Ace Data Cloud

## Why Use Face Transformation on Ace Data Cloud

- Unified developer platform with one API key, billing system, and usage tracking
- Production-ready AI API endpoints served from [https://api.acedata.cloud](https://api.acedata.cloud)
- English integration guides, API references, and service documentation
- Global-ready workflow for developers building chat, image, video, music, and search products

## Overview

The Face Transformation service provides seven endpoints for analyzing and editing faces in photos: keypoint analysis, beautification, age/gender transformation, face swap, cartoon avatars, and liveness detection.

## Application Process

To use the Face Transformation APIs, apply for the corresponding service on the [Face Swap API](https://platform.acedata.cloud/documents/6be9e2dd-e3ca-4e8f-b38c-d5057e92354e) page. After entering the page, click the "Acquire" button.

There is a free quota available for first-time applicants, allowing you to use this API for free.

## Quick Start

- Base URL: [https://api.acedata.cloud](https://api.acedata.cloud)
- Service page: [Face Transformation on Ace Data Cloud](https://platform.acedata.cloud/service/face-change)
- Docs: [Developer documentation](https://docs.acedata.cloud)

```bash
curl --request POST "https://api.acedata.cloud/face/swap" \
  --header "Authorization: Bearer YOUR_API_KEY" \
  --header "Content-Type: application/json" \
  --data '{
    "source_image_url": "https://example.com/source.jpg",
    "target_image_url": "https://example.com/target.jpg"
  }'
```

## APIs and Guides

| API | Path | Integration Guidance |
| ---- | ---- | ------------ |
| [Face Swap API](https://platform.acedata.cloud/documents/6be9e2dd-e3ca-4e8f-b38c-d5057e92354e) | `/face/swap` | [Face Swap API Integration Guide](docs/face_swap_api_integration_guide.md) |
| [Face Beautify API](https://platform.acedata.cloud/documents/7d536eb6-8fea-48d5-a050-43aa57a23f7e) | `/face/beautify` | [Face Beautify API Integration Guide](docs/face_beautify_api_integration_guide.md) |
| [Face Analyze API](https://platform.acedata.cloud/documents/e4fbc3b6-4f44-48fb-a049-40f5c27c7cd3) | `/face/analyze` | [Face Analyze API Integration Guide](docs/face_analyze_api_integration_guide.md) |
| [Face ChangeAge API](https://platform.acedata.cloud/documents/2c7f6468-58d9-4611-885b-1e34664d49e9) | `/face/change-age` | [Face Change Age API Integration Guide](docs/face_change_age_api_integration_guide.md) |
| [Face ChangeGender API](https://platform.acedata.cloud/documents/2f64e798-d272-460d-92c5-9c1ff99f223b) | `/face/change-gender` | [Face Change Gender API Integration Guide](docs/face_change_gender_api_integration_guide.md) |
| [Face Cartoon API](https://platform.acedata.cloud/documents/1bbce3f9-beec-46bd-8423-5642f0c9e3b8) | `/face/cartoon` | [Face Cartoon API Integration Guide](docs/face_cartoon_api_integration_guide.md) |
| [Face DetectLive API](https://platform.acedata.cloud/documents/96006810-b5b7-4585-90eb-90c2ca127b67) | `/face/detect-live` | [Face Detect Live API Integration Guide](docs/face_detect_live_api_integration_guide.md) |

## Related Resources

- [Ace Data Cloud Developer Platform](https://platform.acedata.cloud)
- [Ace Data Cloud Docs](https://docs.acedata.cloud)
- [Status Page](https://status.acedata.cloud)
- [Ace Data Cloud GitHub Organization](https://github.com/AceDataCloud)

## Support

If you meet any issue, please check [support info](https://platform.acedata.cloud/support) or browse the latest documentation on [docs.acedata.cloud](https://docs.acedata.cloud)
