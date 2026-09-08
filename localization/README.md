# Localization Translate API

Translate markdown text or JSON localization content into a target locale.

![Platform](https://img.shields.io/badge/platform-Ace%20Data%20Cloud-0f766e?style=flat-square) ![API](https://img.shields.io/badge/type-AI%20API-2563eb?style=flat-square) ![Docs](https://img.shields.io/badge/docs-online-16a34a?style=flat-square)

API home page: [Ace Data Cloud - Localization Translate](https://platform.acedata.cloud/documents/localization-translate)

Keywords: localization-api, translate-api, i18n, markdown-translation, json-translation, rest-api, ai-api, AI API, REST API, Developer API, Ace Data Cloud

## Why Use Localization Translate on Ace Data Cloud

- Unified developer platform with one API key, billing system, and usage tracking
- Production-ready API endpoints served from [https://api.acedata.cloud](https://api.acedata.cloud)
- English integration guides, API references, and service documentation
- Global-ready workflow for developers localizing apps, websites, and content

## Overview

The Localization Translate API translates input content into a target language and returns the result in either markdown or JSON format. Send markdown text with `extension` set to `md`, or send a JSON object with `extension` set to `json`.

## Application Process

To use the Localization Translate API, obtain an API token from the [Ace Data Cloud Console](https://platform.acedata.cloud/console/applications).

One API token can call all services on the platform without needing to apply separately for each service. The first application grants a free quota for trial use; when the quota is insufficient, recharge your balance in the [console](https://platform.acedata.cloud/console/coin).

## Quick Start

- Base URL: [https://api.acedata.cloud](https://api.acedata.cloud)
- API reference: [Localization Translate API](https://platform.acedata.cloud/documents/localization-translate)
- Docs: [Developer documentation](https://docs.acedata.cloud)

```bash
curl -X POST 'https://api.acedata.cloud/localization/translate' \
  -H 'accept: application/json' \
  -H 'authorization: ******' \
  -H 'content-type: application/json' \
  -d '{
    "input": "# Title 1\n\nThis is a paragraph.\n\n## Title 2\n\nThis is another paragraph.",
    "locale": "zh-CN",
    "extension": "md"
  }'
```

## APIs and Guides

| API | Path | Integration Guidance |
| ---- | ---- | ------------ |
| [Localization Translate API](https://platform.acedata.cloud/documents/localization-translate) | `/localization/translate` | [Localization Translate API Integration Guide](docs/localization_translate_api_integration_guide.md) |

## Related Resources

- [Ace Data Cloud Developer Platform](https://platform.acedata.cloud)
- [Ace Data Cloud Docs](https://docs.acedata.cloud)
- [Status Page](https://status.acedata.cloud)
- [Ace Data Cloud GitHub Organization](https://github.com/AceDataCloud)

## Support

If you meet any issue, please check [support info](https://platform.acedata.cloud/support) or browse the latest documentation on [docs.acedata.cloud](https://docs.acedata.cloud)
