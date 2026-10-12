# Face Transformation API

Face analysis and transformation service: detect keypoints, beautify portraits, change age/gender, swap faces, cartoonify, and detect liveness.

![Platform](https://img.shields.io/badge/platform-Ace%20Data%20Cloud-0f766e?style=flat-square) ![API](https://img.shields.io/badge/type-AI%20API-2563eb?style=flat-square) ![Docs](https://img.shields.io/badge/docs-online-16a34a?style=flat-square)

API home page: [Ace Data Cloud - Face Transformation](https://platform.acedata.cloud/services/8efa1d83-9b75-4562-b44a-af95ce563d05?utm_source=github&utm_medium=referral&utm_campaign=evergreen&utm_content=face_api_readme_services_8efa1d83_9b75_4562_b44a_af95ce563d05)

Keywords: face-api, face-swap, face-detection, beautify, face-cartoon, age-change, gender-change, liveness, image-api, ai-api, AI API, REST API, Developer API, Ace Data Cloud

## Get your Ace Data Cloud API key

1. Open [Ace Data Cloud → Applications](https://platform.acedata.cloud/console/applications?utm_source=github&utm_medium=referral&utm_campaign=evergreen&utm_content=face_api_readme_api_key). Sign in, or register an account first.
2. Find **General application**. If it has not been created, choose **Initialize General Application**. A general key can use the services available to your account; a dedicated application's key is limited to its service. Check the required service/model access and [current pricing](https://platform.acedata.cloud/models?utm_source=github&utm_medium=referral&utm_campaign=evergreen&utm_content=face_api_readme_pricing).
3. Copy the **API Key** from the application card, or open **Keys / Manage Keys → Create** to create a separate key for this integration. Give it a recognizable name so you can revoke or rotate it independently.
4. When creating a key, review **Expiration Time**, **Set Usage Limitation**, and **Allowed APIs**. Enable only the restrictions you need, allow the operations you will call, then click **Create** and copy the token from the key list. Task lookup does not grant permission to submit a generation. Confirm the application's balance can cover your first request; any trial allowance is whatever your account currently displays.
5. Copy only the token value, without quotation marks, spaces, or `Bearer `. An API Key / API Token field expects this raw value; only a manually configured HTTP `Authorization` header needs the `Bearer ` prefix. A `platform-...` account-management token cannot replace a generation API key.

![Copy an application API key or open Manage Keys](https://raw.githubusercontent.com/AceDataCloud/NanoBananaDify/2522b2f57210597af2db866445319334a1677a23/_assets/tutorial/get-api-key-en.png)

![Create a separately named key with optional restrictions](https://raw.githubusercontent.com/AceDataCloud/NanoBananaDify/2522b2f57210597af2db866445319334a1677a23/_assets/tutorial/create-api-key-en.png)

Save the key in the client's credential store or the environment variable shown below. Never put it in a prompt, shared workflow, screenshot, or Git commit. If authentication fails, check the full copied value, application/service access, expiration, usage limit, and balance before creating another key.

## Why Use Face Transformation on Ace Data Cloud

- Unified developer platform with one API key, billing system, and usage tracking
- Production-ready AI API endpoints served from [https://api.acedata.cloud](https://api.acedata.cloud)
- English integration guides, API references, and service documentation
- Global-ready workflow for developers building chat, image, video, music, and search products

## Overview

The Face Transformation service provides seven endpoints for analyzing and editing faces in photos: keypoint analysis, beautification, age/gender transformation, face swap, cartoon avatars, and liveness detection.

## Application Process

To use the Face Transformation APIs, apply for the corresponding service on the [Face Swap API](https://platform.acedata.cloud/documents/6be9e2dd-e3ca-4e8f-b38c-d5057e92354e?utm_source=github&utm_medium=referral&utm_campaign=evergreen&utm_content=face_api_readme_documents_6be9e2dd_e3ca_4e8f_b38c_d5057e92354e) page. After entering the page, click the "Acquire" button.

There is a free quota available for first-time applicants, allowing you to use this API for free.

## Quick Start

- Base URL: [https://api.acedata.cloud](https://api.acedata.cloud)
- Service page: [Face Transformation on Ace Data Cloud](https://platform.acedata.cloud/services/8efa1d83-9b75-4562-b44a-af95ce563d05?utm_source=github&utm_medium=referral&utm_campaign=evergreen&utm_content=face_api_readme_services_8efa1d83_9b75_4562_b44a_af95ce563d05)
- Docs: [Developer documentation](https://platform.acedata.cloud/documents?utm_source=github&utm_medium=referral&utm_campaign=evergreen&utm_content=face_api_readme_documents)

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
| [Face Swap API](https://platform.acedata.cloud/documents/6be9e2dd-e3ca-4e8f-b38c-d5057e92354e?utm_source=github&utm_medium=referral&utm_campaign=evergreen&utm_content=face_api_readme_documents_6be9e2dd_e3ca_4e8f_b38c_d5057e92354e) | `/face/swap` | [Face Swap API Integration Guide](docs/face_swap_api_integration_guide.md) |
| [Face Beautify API](https://platform.acedata.cloud/documents/7d536eb6-8fea-48d5-a050-43aa57a23f7e?utm_source=github&utm_medium=referral&utm_campaign=evergreen&utm_content=face_api_readme_documents_7d536eb6_8fea_48d5_a050_43aa57a23f7e) | `/face/beautify` | [Face Beautify API Integration Guide](docs/face_beautify_api_integration_guide.md) |
| [Face Analyze API](https://platform.acedata.cloud/documents/e4fbc3b6-4f44-48fb-a049-40f5c27c7cd3?utm_source=github&utm_medium=referral&utm_campaign=evergreen&utm_content=face_api_readme_documents_e4fbc3b6_4f44_48fb_a049_40f5c27c7cd3) | `/face/analyze` | Detect face keypoints and shape |
| [Face ChangeAge API](https://platform.acedata.cloud/documents/2c7f6468-58d9-4611-885b-1e34664d49e9?utm_source=github&utm_medium=referral&utm_campaign=evergreen&utm_content=face_api_readme_documents_2c7f6468_58d9_4611_885b_1e34664d49e9) | `/face/change-age` | Age a face up or down |
| [Face ChangeGender API](https://platform.acedata.cloud/documents/2f64e798-d272-460d-92c5-9c1ff99f223b?utm_source=github&utm_medium=referral&utm_campaign=evergreen&utm_content=face_api_readme_documents_2f64e798_d272_460d_92c5_9c1ff99f223b) | `/face/change-gender` | Swap perceived gender |
| [Face Cartoon API](https://platform.acedata.cloud/documents/1bbce3f9-beec-46bd-8423-5642f0c9e3b8?utm_source=github&utm_medium=referral&utm_campaign=evergreen&utm_content=face_api_readme_documents_1bbce3f9_beec_46bd_8423_5642f0c9e3b8) | `/face/cartoon` | Cartoonify a portrait |
| [Face DetectLive API](https://platform.acedata.cloud/documents/96006810-b5b7-4585-90eb-90c2ca127b67?utm_source=github&utm_medium=referral&utm_campaign=evergreen&utm_content=face_api_readme_documents_96006810_b5b7_4585_90eb_90c2ca127b67) | `/face/detect-live` | Liveness detection |

## Related Resources

- [Ace Data Cloud Developer Platform](https://platform.acedata.cloud?utm_source=github&utm_medium=referral&utm_campaign=evergreen&utm_content=face_api_readme_platform)
- [Ace Data Cloud Docs](https://platform.acedata.cloud/documents?utm_source=github&utm_medium=referral&utm_campaign=evergreen&utm_content=face_api_readme_documents)
- [Status Page](https://status.acedata.cloud)
- [Ace Data Cloud GitHub Organization](https://github.com/AceDataCloud)

## Support

If you meet any issue, please check [support info](https://platform.acedata.cloud/support?utm_source=github&utm_medium=referral&utm_campaign=evergreen&utm_content=face_api_readme_support) or browse the latest documentation on [docs.acedata.cloud](https://platform.acedata.cloud/documents?utm_source=github&utm_medium=referral&utm_campaign=evergreen&utm_content=face_api_readme_documents)
