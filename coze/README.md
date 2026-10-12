# AceData Cloud — Coze / 扣子 Plugins

Import AceData Cloud's AI APIs into [Coze](https://www.coze.com) / [扣子](https://www.coze.cn)
as plugins, so your Coze bots and workflows can generate music, images and video —
and later search the web — through a single Bearer token.

Coze imports **standard OpenAPI 3.0** schemas, so every file here can be imported
directly with no code. This directory currently contains eight legacy schema examples, one `<service>.yaml` per plugin. Schema availability does not establish store approval or current service availability. The newer store catalog and its authorization flow are being maintained in [the Coze store update](https://github.com/AceDataCloud/APIs/pull/956).

## Get your Ace Data Cloud API key

1. Open [Ace Data Cloud → Applications](https://platform.acedata.cloud/console/applications?utm_source=github&utm_medium=referral&utm_campaign=evergreen&utm_content=coze_api_readme_api_key). Sign in, or register an account first.
2. Find **General application**. If it has not been created, choose **Initialize General Application**. A general key can use the services available to your account; a dedicated application's key is limited to its service. Check the required service/model access and [current pricing](https://platform.acedata.cloud/models?utm_source=github&utm_medium=referral&utm_campaign=evergreen&utm_content=coze_api_readme_pricing).
3. Copy the **API Key** from the application card, or open **Keys / Manage Keys → Create** to create a separate key for this integration. Give it a recognizable name so you can revoke or rotate it independently.
4. When creating a key, review **Expiration Time**, **Set Usage Limitation**, and **Allowed APIs**. Enable only the restrictions you need, allow the operations you will call, then click **Create** and copy the token from the key list. Task lookup does not grant permission to submit a generation. Confirm the application's balance can cover your first request; any trial allowance is whatever your account currently displays.
5. Copy only the token value, without quotation marks, spaces, or `Bearer `. An API Key / API Token field expects this raw value; only a manually configured HTTP `Authorization` header needs the `Bearer ` prefix. A `platform-...` account-management token cannot replace a generation API key.

![Copy an application API key or open Manage Keys](https://raw.githubusercontent.com/AceDataCloud/NanoBananaDify/2522b2f57210597af2db866445319334a1677a23/_assets/tutorial/get-api-key-en.png)

![Create a separately named key with optional restrictions](https://raw.githubusercontent.com/AceDataCloud/NanoBananaDify/2522b2f57210597af2db866445319334a1677a23/_assets/tutorial/create-api-key-en.png)

Save the key in the client's credential store or the environment variable shown below. Never put it in a prompt, shared workflow, screenshot, or Git commit. If authentication fails, check the full copied value, application/service access, expiration, usage limit, and balance before creating another key.

## Plugins

| File | Tool (`operationId`) | AceData API | What it does |
|---|---|---|---|
| [`suno.yaml`](./suno.yaml) | `generateMusic` | `POST /suno/audios` | Generate a full song from a prompt or custom lyrics |
| [`image.yaml`](./image.yaml) | `generateImage` | `POST /openai/images/generations` | Generate images — GPT Image, Nano Banana or DALL·E (pick the model) |
| [`seedream.yaml`](./seedream.yaml) | `generateImage` | `POST /seedream/images` | Generate images with ByteDance Seedream (Doubao) |
| [`flux.yaml`](./flux.yaml) | `generateImage` | `POST /flux/images` | Generate or edit images with Flux |
| [`sora.yaml`](./sora.yaml) | `generateVideo` | `POST /sora/videos` | Historical schema; Sora is retired, do not use for new integrations |
| [`kling.yaml`](./kling.yaml) | `generateVideo` | `POST /kling/videos` | Generate videos with Kuaishou Kling |
| [`veo.yaml`](./veo.yaml) | `generateVideo` | `POST /veo/videos` | Generate videos with Google Veo |
| [`seedance.yaml`](./seedance.yaml) | `generateVideo` | `POST /seedance/videos` | Generate videos with ByteDance Seedance |

## Import into Coze (扣子)

1. **Get an API token.** Follow the [API key steps above](#get-your-ace-data-cloud-api-key). Choose a general key for multiple services, or a dedicated key for the service you are importing.
2. **Create the plugin from the schema.**
   - Coze.com: **Development → Plugins → Create plugin → Import**, then upload the
     `.yaml` (or paste its contents).
   - 扣子 (coze.cn):「**资源库 → 插件 → 创建插件 → 导入**」，上传或粘贴 `.yaml`。
3. **Configure authorization.** Choose **Service** auth with:
   - Location: **Header**
   - Parameter name: **`Authorization`**
   - Service token / value: **`Bearer <your api.acedata.cloud token>`**
     (include the literal `Bearer ` prefix).
4. **Test.** Coze turns each `operationId` into a callable tool. Run **Test** with
   a minimal payload, e.g. `{ "prompt": "a lofi track for studying" }`, and confirm
   the response contains an `audio_url`.
5. **Choose the sharing scope.** The fixed Service token above is for your own private plugin/workflow and uses your balance. Do not publish your personal key as a shared default. A public store submission needs its own reviewed user-authorization configuration; source import, workspace publication and store approval are separate steps.

## Notes

- **Synchronous by design.** These endpoints return the result inline (the `200`
  body already contains the `audio_url` / image `url`), which is what Coze tools
  expect. Do **not** add `callback_url` / `async` to the schema — that switches the
  API into webhook mode and Coze would only receive a task id.
- **One general key, permitted services.** The base URL is `https://api.acedata.cloud` and the
  general application key can access the services your account is entitled to use. A service-specific key cannot access another service.
- **Real descriptions.** These schemas hand-write human-readable descriptions on
  purpose — the platform's internal OpenAPI specs use `$t(...)` i18n placeholders
  that would otherwise show up literally as tool/parameter names inside Coze.

## Store status and next steps

The [Coze store continuation PR](https://github.com/AceDataCloud/APIs/pull/956) records the 2026-10-11 authenticated store checks. It separates source preparation, workspace publication, store review, and installation into an Agent:

- **Approved and verified after installation:** Localization, Short URL, Google Search, DeepSeek, Nano Banana, and Qwen Image.
- **Submitted; under review at that check:** Kimi, GLM, Grok, Claude, Web Extractor, Gemini, Fish, and OpenAI.
- **Suno native MCP:** not published; its caller OAuth flow is not compatible with the current Coze flow.

These are dated review results, not a claim that every schema in this directory is live. Follow the continuation PR for current status and the pending catalog rather than reusing old install/call counts. Installed Agents must bind the user's private credential as a variable reference, keep it out of prompts and shared defaults, and follow the authorization mode documented for that plugin. The private fixed-Service-token import example above is not a multi-user store authorization design.

Before updating a public listing, carry over the detailed API-key steps and tagged setup link, verify that Coze preserves the URL parameters, and read back the approved listing after review. Store metadata and screenshots are updated separately from this GitHub README. Sora's historical schema should not be submitted as an active service.
