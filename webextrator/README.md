# WebExtrator API

WebExtrator web rendering and content extraction services.

![Platform](https://img.shields.io/badge/platform-Ace%20Data%20Cloud-0f766e?style=flat-square) ![API](https://img.shields.io/badge/type-AI%20API-2563eb?style=flat-square) ![Docs](https://img.shields.io/badge/docs-online-16a34a?style=flat-square)

API home page: [Ace Data Cloud - WebExtrator](https://platform.acedata.cloud/service/webextrator)

Keywords: webextrator-api, web-scraping, web-rendering, content-extraction, rest-api, developer-tools, AI API, REST API, Developer API, Ace Data Cloud

## Why Use WebExtrator on Ace Data Cloud

- Unified developer platform with one API key, billing system, and usage tracking
- Production-ready AI API endpoints served from [https://api.acedata.cloud](https://api.acedata.cloud)
- English integration guides, API references, and service documentation
- Global-ready workflow for developers building chat, image, video, music, and search products

## Overview

WebExtrator is a web rendering and intelligent content extraction service. It can fully render JavaScript-heavy pages using a headless browser and return the HTML, text, Markdown, screenshot, and links. On top of rendering, the extract endpoint supports AI-powered content extraction — you can extract article body text, structured data, links, and more with a single API call.

## Application Process

To use the WebExtrator API, apply for the corresponding service on the platform. After entering the page, click the "Acquire" button.

There is a free quota available for first-time applicants, allowing you to use this API for free.

## Quick Start

- Base URL: [https://api.acedata.cloud](https://api.acedata.cloud)
- Service page: [WebExtrator on Ace Data Cloud](https://platform.acedata.cloud/service/webextrator)
- Docs: [Developer documentation](https://docs.acedata.cloud)

```bash
curl -X POST https://api.acedata.cloud/webextrator/render \
  --header "Authorization: Bearer YOUR_API_KEY" \
  --header "Content-Type: application/json" \
  --data '{
    "url": "https://example.com"
  }'
```

## APIs and Guides

Explore the supported endpoints and integration guides for WebExtrator.

| API | Path | Integration Guidance |
| ---- | ---- | ------------ |
| WebExtrator Render API | `/webextrator/render` | [WebExtrator Render API Integration Guide](docs/webextrator_render_api_integration_guide.md) |
| WebExtrator Extract API | `/webextrator/extract` | [WebExtrator Extract API Integration Guide](docs/webextrator_extract_api_integration_guide.md) |
| WebExtrator Tasks API | `/webextrator/tasks` | [WebExtrator Tasks API Integration Guide](docs/webextrator_tasks_api_integration_guide.md) |
