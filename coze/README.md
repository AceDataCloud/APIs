# AceData Cloud — Coze / 扣子 Plugins

Import AceData Cloud's AI APIs into [Coze](https://www.coze.com) / [扣子](https://www.coze.cn)
as plugins, so your Coze bots and workflows can generate music, images and video —
and later search the web — through a single Bearer token.

Coze imports **standard OpenAPI 3.0** schemas, so every file here can be imported
directly with no code. We start with **Suno (AI music)**; more services follow the
exact same pattern (one `<service>.yaml` per plugin).

## Plugins

| File | Tool (`operationId`) | AceData API | What it does |
|---|---|---|---|
| [`suno.yaml`](./suno.yaml) | `generateMusic` | `POST /suno/audios` | Generate a full song from a prompt or custom lyrics |

## Import into Coze (扣子)

1. **Get an API token.** Create one at
   <https://platform.acedata.cloud/console/credentials> — a per-service
   `api.acedata.cloud` token. Keep it secret.
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
5. **Publish.** Publish the plugin to the Coze plugin store (扣子插件商店) so other
   users can install it into their own bots and workflows.

## Notes

- **Synchronous by design.** These endpoints return the result inline (the `200`
  body already contains `audio_url`), which is what Coze tools expect. Do **not**
  add `callback_url` / `async` to the schema — that switches the API into webhook
  mode and Coze would only receive a task id.
- **One token, all services.** The base URL is `https://api.acedata.cloud` and the
  same token style works across services, so additional plugins here reuse the same
  auth setup.
- **Real descriptions.** These schemas hand-write human-readable descriptions on
  purpose — the platform's internal OpenAPI specs use `$t(...)` i18n placeholders
  that would otherwise show up literally as tool/parameter names inside Coze.

## Roadmap

Same pattern, one file each: `flux.yaml` (image), `luma.yaml` / `veo.yaml` (video),
`serp.yaml` (web search). Contributions welcome — copy `suno.yaml`, swap the path,
parameters and descriptions, and add a row to the table above.
