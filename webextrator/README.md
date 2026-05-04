# WebExtrator API

WebExtrator web rendering and intelligent content extraction services.

![Platform](https://img.shields.io/badge/platform-Ace%20Data%20Cloud-0f766e?style=flat-square) ![API](https://img.shields.io/badge/type-AI%20API-2563eb?style=flat-square) ![Docs](https://img.shields.io/badge/docs-online-16a34a?style=flat-square)

API home page: [Ace Data Cloud - WebExtrator](https://platform.acedata.cloud/service/webextrator)

Keywords: webextrator-api, web-render, web-extract, content-extraction, rest-api, ai-api, developer-tools, AI API, REST API, Developer API, Ace Data Cloud

## Why Use WebExtrator on Ace Data Cloud

- Unified developer platform with one API key, billing system, and usage tracking
- Production-ready AI API endpoints served from [https://api.acedata.cloud](https://api.acedata.cloud)
- English integration guides, API references, and service documentation
- Global-ready workflow for developers building chat, image, video, music, and search products

## Overview

WebExtrator provides a two-layer API for working with web pages:

1. **Render** (`/webextrator/render`): Headless browser rendering — returns the full rendered HTML, markdown, plain text, screenshot (base64), and extracted links for any URL.
2. **Extract** (`/webextrator/extract`): Builds on top of Render to provide structured content extraction — supports article extraction, markdown, raw text, link lists, or fully custom structured output powered by an optional LLM post-processing step.
3. **Tasks** (`/webextrator/tasks`): Free query interface to look up historical `render` / `extract` tasks (retained for 7 days).

## Application Process

To use the WebExtrator API, apply for the corresponding service on the [WebExtrator Render API](https://platform.acedata.cloud/documents/) page. After entering the page, click the "Acquire" button.

There is a free quota available for first-time applicants, allowing you to use this API for free.

## Quick Start

```bash
curl -X POST https://api.acedata.cloud/webextrator/render \
  -H "Authorization: Bearer $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://example.com",
    "wait_until": "networkidle",
    "block_resources": ["image", "media", "font"]
  }'
```

## APIs and Guides

| API | Path | Integration Guidance |
| ---- | ---- | ------------ |
| WebExtrator Render API | `/webextrator/render` | [WebExtrator Render API Integration Guide](docs/webextrator_render_api_integration_guide.md) |
| WebExtrator Extract API | `/webextrator/extract` | [WebExtrator Extract API Integration Guide](docs/webextrator_extract_api_integration_guide.md) |
| WebExtrator Tasks API | `/webextrator/tasks` | [WebExtrator Tasks API Integration Guide](docs/webextrator_tasks_api_integration_guide.md) |
