# Short Link Generation API

Turn long URLs into compact, shareable short links served from `suro.id`.

![Platform](https://img.shields.io/badge/platform-Ace%20Data%20Cloud-0f766e?style=flat-square) ![API](https://img.shields.io/badge/type-AI%20API-2563eb?style=flat-square) ![Docs](https://img.shields.io/badge/docs-online-16a34a?style=flat-square)

API home page: [Ace Data Cloud - Short Link Generation](https://platform.acedata.cloud/service/shorturl)

Keywords: shorturl-api, short-link, url-shortener, suro.id, link-generation, rest-api, ai-api, AI API, REST API, Developer API, Ace Data Cloud

## Why Use Short Link Generation on Ace Data Cloud

- Unified developer platform with one API key, billing system, and usage tracking
- Production-ready API endpoints served from [https://api.acedata.cloud](https://api.acedata.cloud)
- English integration guides, API references, and service documentation
- Global-ready workflow for developers building chat, image, video, music, and search products

## Overview

The Short URL API generates a short link for a given long URL. Send the original URL in `content` and receive a shortened `url` in the response.

## Application Process

To use the Short URL API, apply for the corresponding service on the [Short URL API](https://platform.acedata.cloud/documents/d57df7ea-e1ba-4873-905c-d4c072e40450) page. After entering the page, click the "Acquire" button.

There is a free quota available for first-time applicants, allowing you to use this API for free.

## Quick Start

- Base URL: [https://api.acedata.cloud](https://api.acedata.cloud)
- Service page: [Short Link Generation on Ace Data Cloud](https://platform.acedata.cloud/service/shorturl)
- Docs: [Developer documentation](https://docs.acedata.cloud)

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
| [Short URL API](https://platform.acedata.cloud/documents/d57df7ea-e1ba-4873-905c-d4c072e40450) | `/shorturl` | [Short URL API Integration Guide](docs/short_url_api_integration_guide.md) |

## Related Resources

- [Ace Data Cloud Developer Platform](https://platform.acedata.cloud)
- [Ace Data Cloud Docs](https://docs.acedata.cloud)
- [Status Page](https://status.acedata.cloud)
- [Ace Data Cloud GitHub Organization](https://github.com/AceDataCloud)

## Support

If you meet any issue, please check [support info](https://platform.acedata.cloud/support) or browse the latest documentation on [docs.acedata.cloud](https://docs.acedata.cloud)
