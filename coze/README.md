# AceData Cloud — Coze / 扣子 Plugins

Import AceData Cloud's AI APIs into [Coze](https://www.coze.com) / [扣子](https://www.coze.cn)
as plugins, so your Coze agents and workflows can generate music, images and video,
search the web, and create short links with an Ace Data Cloud API credential.

Coze imports **standard OpenAPI 3.0** schemas, so every file here can be imported
directly with no code. We ship **music (Suno)**, **image** (GPT Image / Nano Banana /
DALL·E / Seedream / Flux) and **video** (Sora / Kling / Veo / Seedance) — one
`<service>.yaml` per plugin. A schema in this repository is an importable definition,
not evidence that a plugin is published or approved in either regional store.

## Plugins

| File | Tool (`operationId`) | AceData API | What it does |
|---|---|---|---|
| [`suno.yaml`](./suno.yaml) | `generateMusic` | `POST /suno/audios` | Generate a full song from a prompt or custom lyrics |
| [`image.yaml`](./image.yaml) | `generateImage` | `POST /openai/images/generations` | Generate images — GPT Image, Nano Banana or DALL·E (pick the model) |
| [`seedream.yaml`](./seedream.yaml) | `generateImage` | `POST /seedream/images` | Generate images with ByteDance Seedream (Doubao) |
| [`flux.yaml`](./flux.yaml) | `generateImage` | `POST /flux/images` | Generate or edit images with Flux |
| [`serp.yaml`](./serp.yaml) | `searchGoogle` | `POST /serp/google` | Search web pages with source links, language, country, recency and pagination filters |
| [`shorturl.yaml`](./shorturl.yaml) | `createShortLink` | `POST /shorturl` | Turn a long URL into a shareable short link |
| [`sora.yaml`](./sora.yaml) | `generateVideo` | `POST /sora/videos` | Generate videos with OpenAI Sora |
| [`kling.yaml`](./kling.yaml) | `generateVideo` | `POST /kling/videos` | Generate videos with Kuaishou Kling |
| [`veo.yaml`](./veo.yaml) | `generateVideo` | `POST /veo/videos` | Generate videos with Google Veo |
| [`seedance.yaml`](./seedance.yaml) | `generateVideo` | `POST /seedance/videos` | Generate videos with ByteDance Seedance |

## Import into Coze (扣子)

1. **Get an API token.** Create one at
   <https://platform.acedata.cloud/console/credentials>. Ensure that its API
   permissions cover the selected tool. Keep it secret.
2. **Create the plugin from the schema.**
   - Coze.com: **Library → Resources → Plugin → Import**, then upload the
     `.yaml` (or paste its contents).
   - 扣子 (coze.cn):「**资源库 → 插件 → 创建插件 → 导入**」，上传或粘贴 `.yaml`。
3. **Configure authorization.** The Seedream, Flux, SERP and Short URL schemas
   declare a required `Authorization` **Header input** on each tool. Select
   **No authorization required** at the plugin level, and supply
   `Bearer <your api.acedata.cloud token>` through that input. The underlying
   Ace Data Cloud API still requires a valid credential. Bind the input privately
   in the workflow; do not put API keys in agent prompts, conversations, schema
   defaults or shared workflow exports.

   The other schemas use an OpenAPI security scheme. Coze may not import that
   scheme into its authorization settings. For a private plugin, configure
   **Service → Service token / API key**, **Header**, parameter **Authorization**,
   value **Bearer TOKEN**. A fixed service token belongs to the publisher: do not
   publish it for general use unless you intentionally fund those calls and have
   established limits. The four Header-input plugins instead use each caller's
   own credential and balance.
4. **Test.** Run **Test Run** with the real API. Verify a successful response and
   usable output (`data[].image_url`, `organic[].link`, or `data.url`, as applicable).
   HTTP 200, a task ID, or a mock response alone is not a successful generation.
   Do not save a debugging example containing credentials.
5. **Publish to the workspace.** Every enabled tool must pass its trial run.
   Complete the privacy collection statement accurately, then publish a version.
6. **Submit to the store.** Use the separate **Publish plugin** entry in
   **Plugin Store**, complete its listing and review requirements, and record the
   resulting public listing URL and status. Workspace publication is not store
   approval. Verify Coze.com and Coze.cn independently.

## Notes

- **Long-running tasks.** These generation schemas request synchronous results.
  Verify that real generation fits Coze's tool timeout before publishing. For a
  longer video or music workflow, add both asynchronous submission and task
  retrieval tools; a submission-only plugin cannot deliver the finished media.
- **Token permissions.** All tools use `https://api.acedata.cloud`, but a
  credential's API allowlist, expiry and quota still apply.
- **OAuth.** Coze also offers standard OAuth with a client ID and secret. This
  requires a registered application, the plugin-specific callback URL, a
  compatible token exchange and end-to-end authorization testing. Do not claim
  one-click account connection merely because an MCP server supports OAuth.
- **Real descriptions.** These schemas hand-write human-readable descriptions on
  purpose — the platform's internal OpenAPI specs use `$t(...)` i18n placeholders
  that would otherwise show up literally as tool/parameter names inside Coze.

## Extending the collection

Add one schema per service, using the actual published API contract for paths,
parameters, model IDs and result fields. Keep descriptions readable instead of
copying untranslated `$t(...)` placeholders. Validate a real user flow before
claiming the plugin is available in the store.

Official Coze guides: [import a plugin](https://www.coze.com/open/docs/guides/plugin_import),
[OAuth plugins](https://www.coze.com/open/docs/guides/oauth_plugin).
