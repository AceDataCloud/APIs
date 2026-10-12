# Short Link Generation API

Turn long URLs into compact, shareable short links served from `suro.id`.

![Platform](https://img.shields.io/badge/platform-Ace%20Data%20Cloud-0f766e?style=flat-square) ![API](https://img.shields.io/badge/type-AI%20API-2563eb?style=flat-square) ![Docs](https://img.shields.io/badge/docs-online-16a34a?style=flat-square)

API home page: [Ace Data Cloud - Short Link Generation](https://platform.acedata.cloud/services/349bfa75-d270-44e9-8188-9894e3b9512c?utm_source=github&utm_medium=referral&utm_campaign=evergreen&utm_content=shorturl_api_readme_services_349bfa75_d270_44e9_8188_9894e3b9512c)

Keywords: shorturl-api, short-link, url-shortener, suro.id, link-generation, rest-api, ai-api, AI API, REST API, Developer API, Ace Data Cloud

## Get your Ace Data Cloud API key

1. Open [Ace Data Cloud → Applications](https://platform.acedata.cloud/console/applications?utm_source=github&utm_medium=referral&utm_campaign=evergreen&utm_content=shorturl_api_readme_api_key). Sign in, or register an account first.
2. Find **General application**. If it has not been created, choose **Initialize General Application**. A general key can use the services available to your account; a dedicated application's key is limited to its service. Check the required service/model access and [current pricing](https://platform.acedata.cloud/models?utm_source=github&utm_medium=referral&utm_campaign=evergreen&utm_content=shorturl_api_readme_pricing).
3. Copy the **API Key** from the application card, or open **Keys / Manage Keys → Create** to create a separate key for this integration. Give it a recognizable name so you can revoke or rotate it independently.
4. When creating a key, review **Expiration Time**, **Set Usage Limitation**, and **Allowed APIs**. Enable only the restrictions you need, allow the operations you will call, then click **Create** and copy the token from the key list. Task lookup does not grant permission to submit a generation. Confirm the application's balance can cover your first request; any trial allowance is whatever your account currently displays.
5. Copy only the token value, without quotation marks, spaces, or `Bearer `. An API Key / API Token field expects this raw value; only a manually configured HTTP `Authorization` header needs the `Bearer ` prefix. A `platform-...` account-management token cannot replace a generation API key.

![Copy an application API key or open Manage Keys](https://raw.githubusercontent.com/AceDataCloud/NanoBananaDify/2522b2f57210597af2db866445319334a1677a23/_assets/tutorial/get-api-key-en.png)

![Create a separately named key with optional restrictions](https://raw.githubusercontent.com/AceDataCloud/NanoBananaDify/2522b2f57210597af2db866445319334a1677a23/_assets/tutorial/create-api-key-en.png)

Save the key in the client's credential store or the environment variable shown below. Never put it in a prompt, shared workflow, screenshot, or Git commit. If authentication fails, check the full copied value, application/service access, expiration, usage limit, and balance before creating another key.

## Why Use Short Link Generation on Ace Data Cloud

- Unified developer platform with one API key, billing system, and usage tracking
- Production-ready API endpoints served from [https://api.acedata.cloud](https://api.acedata.cloud)
- English integration guides, API references, and service documentation
- Global-ready workflow for developers building chat, image, video, music, and search products

## Overview

The Short URL API generates a short link for a given long URL. Send the original URL in `content` and receive a shortened `url` in the response.

## Application Process

To use the Short URL API, apply for the corresponding service on the [Short URL API](https://platform.acedata.cloud/documents/d57df7ea-e1ba-4873-905c-d4c072e40450?utm_source=github&utm_medium=referral&utm_campaign=evergreen&utm_content=shorturl_api_readme_documents_d57df7ea_e1ba_4873_905c_d4c072e40450) page. After entering the page, click the "Acquire" button.

There is a free quota available for first-time applicants, allowing you to use this API for free.

## Quick Start

- Base URL: [https://api.acedata.cloud](https://api.acedata.cloud)
- Service page: [Short Link Generation on Ace Data Cloud](https://platform.acedata.cloud/services/349bfa75-d270-44e9-8188-9894e3b9512c?utm_source=github&utm_medium=referral&utm_campaign=evergreen&utm_content=shorturl_api_readme_services_349bfa75_d270_44e9_8188_9894e3b9512c)
- Docs: [Developer documentation](https://platform.acedata.cloud/documents?utm_source=github&utm_medium=referral&utm_campaign=evergreen&utm_content=shorturl_api_readme_documents)

```bash
curl --request POST "https://api.acedata.cloud/shorturl" \
  --header "Authorization: Bearer YOUR_API_KEY" \
  --header "Content-Type: application/json" \
  --data '{
    "content": "https://platform.acedata.cloud/service/shorturl"
  }'
```

## APIs and Guides

| API | Path | Integration Guidance |
| ---- | ---- | ------------ |
| [Short URL API](https://platform.acedata.cloud/documents/d57df7ea-e1ba-4873-905c-d4c072e40450?utm_source=github&utm_medium=referral&utm_campaign=evergreen&utm_content=shorturl_api_readme_documents_d57df7ea_e1ba_4873_905c_d4c072e40450) | `/shorturl` | [Short URL API Integration Guide](docs/short_url_api_integration_guide.md) |

## Related Resources

- [Ace Data Cloud Developer Platform](https://platform.acedata.cloud?utm_source=github&utm_medium=referral&utm_campaign=evergreen&utm_content=shorturl_api_readme_platform)
- [Ace Data Cloud Docs](https://platform.acedata.cloud/documents?utm_source=github&utm_medium=referral&utm_campaign=evergreen&utm_content=shorturl_api_readme_documents)
- [Status Page](https://status.acedata.cloud)
- [Ace Data Cloud GitHub Organization](https://github.com/AceDataCloud)

## Support

If you meet any issue, please check [support info](https://platform.acedata.cloud/support?utm_source=github&utm_medium=referral&utm_campaign=evergreen&utm_content=shorturl_api_readme_support) or browse the latest documentation on [docs.acedata.cloud](https://platform.acedata.cloud/documents?utm_source=github&utm_medium=referral&utm_campaign=evergreen&utm_content=shorturl_api_readme_documents)
