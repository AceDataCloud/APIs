# GLM API

GLM (General Language Model) generative services by Zhipu AI, including chat completions.

![Platform](https://img.shields.io/badge/platform-Ace%20Data%20Cloud-0f766e?style=flat-square) ![API](https://img.shields.io/badge/type-AI%20API-2563eb?style=flat-square) ![Docs](https://img.shields.io/badge/docs-online-16a34a?style=flat-square)

API home page: [Ace Data Cloud - GLM](https://platform.acedata.cloud/services/0c5b6cb3-79a7-473f-844f-7821553f2ca7?utm_source=github&utm_medium=referral&utm_campaign=evergreen&utm_content=glm_api_readme_services_0c5b6cb3_79a7_473f_844f_7821553f2ca7)

Keywords: glm-api, glm-5.2, glm-5.1, glm-4.7, chat-completions, zhipu-ai, rest-api, ai-api, developer-tools, AI API, REST API, Developer API, Ace Data Cloud

## Get your Ace Data Cloud API key

1. Open [Ace Data Cloud → Applications](https://platform.acedata.cloud/console/applications?utm_source=github&utm_medium=referral&utm_campaign=evergreen&utm_content=glm_api_readme_api_key). Sign in, or register an account first.
2. Find **General application**. If it has not been created, choose **Initialize General Application**. A general key can use the services available to your account; a dedicated application's key is limited to its service. Check the required service/model access and [current pricing](https://platform.acedata.cloud/models?utm_source=github&utm_medium=referral&utm_campaign=evergreen&utm_content=glm_api_readme_pricing).
3. Copy the **API Key** from the application card, or open **Keys / Manage Keys → Create** to create a separate key for this integration. Give it a recognizable name so you can revoke or rotate it independently.
4. When creating a key, review **Expiration Time**, **Set Usage Limitation**, and **Allowed APIs**. Enable only the restrictions you need, allow the operations you will call, then click **Create** and copy the token from the key list. Task lookup does not grant permission to submit a generation. Confirm the application's balance can cover your first request; any trial allowance is whatever your account currently displays.
5. Copy only the token value, without quotation marks, spaces, or `Bearer `. An API Key / API Token field expects this raw value; only a manually configured HTTP `Authorization` header needs the `Bearer ` prefix. A `platform-...` account-management token cannot replace a generation API key.

![Copy an application API key or open Manage Keys](https://raw.githubusercontent.com/AceDataCloud/NanoBananaDify/2522b2f57210597af2db866445319334a1677a23/_assets/tutorial/get-api-key-en.png)

![Create a separately named key with optional restrictions](https://raw.githubusercontent.com/AceDataCloud/NanoBananaDify/2522b2f57210597af2db866445319334a1677a23/_assets/tutorial/create-api-key-en.png)

Save the key in the client's credential store or the environment variable shown below. Never put it in a prompt, shared workflow, screenshot, or Git commit. If authentication fails, check the full copied value, application/service access, expiration, usage limit, and balance before creating another key.

## Why Use GLM on Ace Data Cloud

- Unified developer platform with one API key, billing system, and usage tracking
- Production-ready AI API endpoints served from [https://api.acedata.cloud](https://api.acedata.cloud)
- English integration guides, API references, and service documentation
- Global-ready workflow for developers building chat, image, video, music, and search products

## Overview

GLM (General Language Model) is the next-generation large language model series by Zhipu AI (Z.ai), featuring powerful Chinese and English understanding and generation capabilities. The current flagship `glm-5.2`, along with `glm-5.1`, `glm-5`, `glm-4.7`, `glm-4.6` and other new-generation models, has been extensively optimized for long-context, tool calling, and code tasks. They are widely applicable to intelligent Q&A, content creation, code assistance, customer service bots, and more.

## Application Process

To use the GLM API, apply for the corresponding service on the [GLM Chat Completion API](https://platform.acedata.cloud/documents/ccfbc8fa-0dce-424b-85a4-99c280ddb5cf?utm_source=github&utm_medium=referral&utm_campaign=evergreen&utm_content=glm_api_readme_documents_ccfbc8fa_0dce_424b_85a4_99c280ddb5cf) page. After entering the page, click the "Acquire" button.

There is a free quota available for first-time applicants, allowing you to use this API for free.

## Quick Start

- Base URL: [https://api.acedata.cloud](https://api.acedata.cloud)
- Service page: [GLM on Ace Data Cloud](https://platform.acedata.cloud/services/0c5b6cb3-79a7-473f-844f-7821553f2ca7?utm_source=github&utm_medium=referral&utm_campaign=evergreen&utm_content=glm_api_readme_services_0c5b6cb3_79a7_473f_844f_7821553f2ca7)
- Docs: [Developer documentation](https://platform.acedata.cloud/documents?utm_source=github&utm_medium=referral&utm_campaign=evergreen&utm_content=glm_api_readme_documents)

```bash
curl --request POST "https://api.acedata.cloud/glm/chat/completions" \
  --header "Authorization: Bearer YOUR_API_KEY" \
  --header "Content-Type: application/json" \
  --data '{
    "model": "glm-5.2",
    "messages": [{"role": "user", "content": "Hello!"}]
  }'
```

## APIs and Guides

Explore the supported endpoints and integration guides for GLM.

| API | Path | Integration Guidance |
| ---- | ---- | ------------ |
| [GLM Chat Completion API](https://platform.acedata.cloud/documents/ccfbc8fa-0dce-424b-85a4-99c280ddb5cf?utm_source=github&utm_medium=referral&utm_campaign=evergreen&utm_content=glm_api_readme_documents_ccfbc8fa_0dce_424b_85a4_99c280ddb5cf) | `/glm/chat/completions` | [GLM Chat Completion API Integration Guide](docs/glm_chat_completions_api_integration_guide.md) |
