# Happy Horse Video API

Generate and edit AI videos with Happy Horse through one Ace Data Cloud API.

![Platform](https://img.shields.io/badge/platform-Ace%20Data%20Cloud-0f766e?style=flat-square) ![API](https://img.shields.io/badge/type-AI%20Video%20API-2563eb?style=flat-square) ![Docs](https://img.shields.io/badge/docs-online-16a34a?style=flat-square)

API home page: [Ace Data Cloud - Happy Horse Video](https://platform.acedata.cloud/services/9cd79226-f638-4979-9573-212328a65a31?utm_source=github&utm_medium=referral&utm_campaign=evergreen&utm_content=happyhorse_api_readme_service_happyhorse)

Keywords: happy-horse-api, happyhorse-api, ai-video, video-generation, video-editing,
text-to-video, image-to-video, reference-to-video, rest-api, ai-api, Ace Data Cloud

## Get your Ace Data Cloud API key

1. Open [Ace Data Cloud → Applications](https://platform.acedata.cloud/console/applications?utm_source=github&utm_medium=referral&utm_campaign=evergreen&utm_content=happyhorse_api_readme_api_key). Sign in, or register an account first.
2. Find **General application**. If it has not been created, choose **Initialize General Application**. A general key can use the services available to your account; a dedicated application's key is limited to its service. Check the required service/model access and [current pricing](https://platform.acedata.cloud/models?utm_source=github&utm_medium=referral&utm_campaign=evergreen&utm_content=happyhorse_api_readme_pricing).
3. Copy the **API Key** from the application card, or open **Keys / Manage Keys → Create** to create a separate key for this integration. Give it a recognizable name so you can revoke or rotate it independently.
4. When creating a key, review **Expiration Time**, **Set Usage Limitation**, and **Allowed APIs**. Enable only the restrictions you need, allow the operations you will call, then click **Create** and copy the token from the key list. Task lookup does not grant permission to submit a generation. Confirm the application's balance can cover your first request; any trial allowance is whatever your account currently displays.
5. Copy only the token value, without quotation marks, spaces, or `Bearer `. An API Key / API Token field expects this raw value; only a manually configured HTTP `Authorization` header needs the `Bearer ` prefix. A `platform-...` account-management token cannot replace a generation API key.

![Copy an application API key or open Manage Keys](https://raw.githubusercontent.com/AceDataCloud/NanoBananaDify/2522b2f57210597af2db866445319334a1677a23/_assets/tutorial/get-api-key-en.png)

![Create a separately named key with optional restrictions](https://raw.githubusercontent.com/AceDataCloud/NanoBananaDify/2522b2f57210597af2db866445319334a1677a23/_assets/tutorial/create-api-key-en.png)

Save the key in the client's credential store or the environment variable shown below. Never put it in a prompt, shared workflow, screenshot, or Git commit. If authentication fails, check the full copied value, application/service access, expiration, usage limit, and balance before creating another key.

## Why Use Happy Horse on Ace Data Cloud

- One endpoint for text, first-frame image, reference-image, and video-edit workflows
- Unified API key, billing, usage records, and task tracking
- 720P and 1080P output with 3-15 second generation
- Asynchronous polling and webhook callbacks for long-running jobs
- CDN-backed final video URLs

## Overview

`POST /happyhorse/videos` dispatches four workflows through the `action` field:

| Action | Models | Required input |
|---|---|---|
| `generate` | `happyhorse-1.0-t2v`, `happyhorse-1.1-t2v` | `prompt` |
| `image_to_video` | `happyhorse-1.0-i2v`, `happyhorse-1.1-i2v` | `image_url` |
| `reference_to_video` | `happyhorse-1.0-r2v`, `happyhorse-1.1-r2v` | `prompt`, 1-9 `image_urls` |
| `video_edit` | `happyhorse-1.0-video-edit` | `prompt`, `video_url` |

`POST /happyhorse/tasks` retrieves one or several asynchronous tasks.

## Quick Start

- Base URL: [https://api.acedata.cloud](https://api.acedata.cloud)
- Service page: [Happy Horse Video on Ace Data Cloud](https://platform.acedata.cloud/services/9cd79226-f638-4979-9573-212328a65a31?utm_source=github&utm_medium=referral&utm_campaign=evergreen&utm_content=happyhorse_api_readme_service_happyhorse)
- Developer docs: [docs.acedata.cloud](https://docs.acedata.cloud)

```bash
curl --request POST "https://api.acedata.cloud/happyhorse/videos" \
  --header "Authorization: Bearer YOUR_API_KEY" \
  --header "Content-Type: application/json" \
  --data '{
    "action": "generate",
    "model": "happyhorse-1.1-t2v",
    "prompt": "A cinematic white horse crossing a snowy ridge at sunrise, slow camera push",
    "resolution": "720P",
    "ratio": "16:9",
    "duration": 5,
    "async": true
  }'
```

Poll the returned task ID:

```bash
curl --request POST "https://api.acedata.cloud/happyhorse/tasks" \
  --header "Authorization: Bearer YOUR_API_KEY" \
  --header "Content-Type: application/json" \
  --data '{"id": "TASK_ID", "action": "retrieve"}'
```

## APIs and Guides

| API | Path | Integration guide |
|---|---|---|
| [Happy Horse Videos API](https://platform.acedata.cloud/documents/happyhorse-videos?utm_source=github&utm_medium=referral&utm_campaign=evergreen&utm_content=happyhorse_api_readme_documents_happyhorse_videos) | `/happyhorse/videos` | [Videos API Integration Guide](docs/happyhorse_videos_api_integration_guide.md) |
| [Happy Horse Tasks API](https://platform.acedata.cloud/documents/happyhorse-tasks?utm_source=github&utm_medium=referral&utm_campaign=evergreen&utm_content=happyhorse_api_readme_documents_happyhorse_tasks) | `/happyhorse/tasks` | [Tasks API Integration Guide](docs/happyhorse_tasks_api_integration_guide.md) |

## Agent Integrations

- MCP package: [`mcp-happyhorse`](https://pypi.org/project/mcp-happyhorse/)
- Hosted MCP: `https://happyhorse.mcp.acedata.cloud/mcp`
- Agent Skill: [`happyhorse-video`](https://github.com/AceDataCloud/Skills/tree/main/skills/happyhorse-video)

## Related Resources

- [Ace Data Cloud Developer Platform](https://platform.acedata.cloud?utm_source=github&utm_medium=referral&utm_campaign=evergreen&utm_content=happyhorse_api_readme_platform)
- [API Documentation](https://docs.acedata.cloud)
- [Status Page](https://status.acedata.cloud)
- [Ace Data Cloud GitHub Organization](https://github.com/AceDataCloud)

## Support

For support, visit [platform.acedata.cloud/support](https://platform.acedata.cloud/support?utm_source=github&utm_medium=referral&utm_campaign=evergreen&utm_content=happyhorse_api_readme_support).