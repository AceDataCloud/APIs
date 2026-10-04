# Ace Data Cloud plugins for Coze

This collection prepares the complete public service catalog for Coze review. The
2026-10-05 snapshot contains 83 services: 35 API services, 41 datasets, 3 developer
agent products and 4 deployment products. It produces 35 import definitions with
113 tools, 35 API listing drafts, a consistent icon family, and 9 application
configuration blueprints. These files do not mean a plugin or app is published.

## Canonical plugin definitions

| Plugin | Tools | Definition |
|---|---:|---|
| AceData_DeepSeek_Chat | 1 | [deepseek.yaml](./plugins/deepseek.yaml) |
| AceData_Claude_Assistant | 3 | [claude.yaml](./plugins/claude.yaml) |
| AceData_Maestro_Video_Studio | 2 | [maestro.yaml](./plugins/maestro.yaml) |
| AceData_Turnstile_Tools | 2 | [turnstile.yaml](./plugins/turnstile.yaml) |
| AceData_Captcha_OCR | 2 | [image2text.yaml](./plugins/image2text.yaml) |
| AceData_Kimi_Assistant | 1 | [kimi.yaml](./plugins/kimi.yaml) |
| AceData_Hailuo_Video | 2 | [hailuo.yaml](./plugins/hailuo.yaml) |
| AceData_OpenAI_Studio | 6 | [openai.yaml](./plugins/openai.yaml) |
| AceData_Gemini_Studio | 4 | [gemini.yaml](./plugins/gemini.yaml) |
| AceData_Grok_Studio | 3 | [grok.yaml](./plugins/grok.yaml) |
| AceData_Veo_Video | 2 | [veo.yaml](./plugins/veo.yaml) |
| AceData_AI_Dialogue | 2 | [aichat.yaml](./plugins/aichat.yaml) |
| AceData_Google_Web_Search | 1 | [serp.yaml](./plugins/serp.yaml) |
| AceData_Luma_Video | 2 | [luma.yaml](./plugins/luma.yaml) |
| AceData_Identity_Checks | 10 | [identity.yaml](./plugins/identity.yaml) |
| AceData_Seedance_Video | 2 | [seedance.yaml](./plugins/seedance.yaml) |
| AceData_reCAPTCHA_Tools | 4 | [recaptcha.yaml](./plugins/recaptcha.yaml) |
| AceData_hCaptcha_Tools | 3 | [hcaptcha.yaml](./plugins/hcaptcha.yaml) |
| AceData_Qwen_Image_Studio | 2 | [qwen-image.yaml](./plugins/qwen-image.yaml) |
| AceData_Short_Links | 1 | [shorturl.yaml](./plugins/shorturl.yaml) |
| AceData_Web_Extractor | 3 | [webextrator.yaml](./plugins/webextrator.yaml) |
| AceData_Producer_Music_Studio | 6 | [producer.yaml](./plugins/producer.yaml) |
| AceData_Nano_Banana_Images | 2 | [nano-banana.yaml](./plugins/nano-banana.yaml) |
| AceData_Wan_Video | 2 | [wan.yaml](./plugins/wan.yaml) |
| AceData_Dreamina_Avatar | 2 | [dreamina.yaml](./plugins/dreamina.yaml) |
| AceData_Suno_Music_Studio | 17 | [suno.yaml](./plugins/suno.yaml) |
| AceData_Digital_Human_Studio | 3 | [digitalhuman.yaml](./plugins/digitalhuman.yaml) |
| AceData_HappyHorse_Video | 2 | [happyhorse.yaml](./plugins/happyhorse.yaml) |
| AceData_Kling_Video_Studio | 7 | [kling.yaml](./plugins/kling.yaml) |
| AceData_Localization_Tools | 1 | [localization.yaml](./plugins/localization.yaml) |
| AceData_Fish_Voice_Studio | 5 | [fish.yaml](./plugins/fish.yaml) |
| AceData_MiniMax_Video | 2 | [minimax.yaml](./plugins/minimax.yaml) |
| AceData_GLM_Assistant | 1 | [glm.yaml](./plugins/glm.yaml) |
| AceData_Seedream_Images | 2 | [seedream.yaml](./plugins/seedream.yaml) |
| AceData_Flux_Creative_Studio | 3 | [flux.yaml](./plugins/flux.yaml) |

The complete canonical definitions are in [`plugins/`](./plugins/). Both JSON and YAML are
provided. Coze-import-tested projections for Claude, OpenAI, Kling and Google Search are in
[`imports/`](./imports/); their representation limits are recorded in
`imports/compatibility-notes.json`. They preserve routes and caller-owned auth
but do not provide complete multimodal/opaque-object input parity. Response
shapes come from published examples or sanitized real response shapes, with
example values omitted. Canonical constraints remain authoritative. The historical root filenames remain synchronized for existing links;
`image.yaml` now contains the full OpenAI JSON-compatible tool set. The retired
Sora definition is kept in [`legacy/`](./legacy/) for migration reference only.
It is not in the public catalog or launch batch.

## Review assets

- [`listings.json`](./listings.json): names (30 characters or fewer), briefs
  (50 or fewer), full copy, scenarios, proposed categories and privacy questions.
- [`icons/`](./icons/): 512 × 512 PNG and JPEG icons, with the Ace Data Cloud mark.
  Use JPEG if the Coze file chooser rejects PNG for that import flow.
- [`catalog/coverage.json`](./catalog/coverage.json): every service and every
  declared API has a disposition; incompatible or unpublished operations are
  explicitly accounted for.
- [`apps/`](./apps/): eight task-specific app blueprints and a service guide.
  These JSON files are configuration/review material, not a claimed native Coze
  app export. Bind the final published plugin IDs during app assembly.
- [`catalog/service-guide.txt`](./catalog/service-guide.txt): all 83 service
  entries for a catalog knowledge source. Datasets link to acquisition guidance;
  developer clients link to setup; deployments require a user-owned instance.
- [`examples/catalog/starter-flows.json`](./examples/catalog/starter-flows.json):
  minimal request cases validated against the schemas. Unexecuted cases have no
  fabricated successful response. Identity/CAPTCHA/avatar fixtures are gated.
- [`examples/catalog/validation-cases.json`](./examples/catalog/validation-cases.json):
  per-operation test plans. Replace owned-resource placeholders only after a
  preceding authorized generation has produced those resources.
- Existing top-level files in [`examples/`](./examples/) contain sanitized
  results from the initial four real Coze trials. Their evidence does not cover
  the newly added tools or prove store publication.

## Coze setup

1. Import one service definition through **Library → Resources → Plugin →
   Import → URL & Raw data** or the file chooser. Check that all expected tools
   and conditional inputs survived the import.
2. Upload the matching icon. Set the name, brief and full description from
   `listings.json`. The importer can truncate descriptions and copy the long
   text into the brief; correct both fields in **Edit Plugin Configuration**.
3. At plugin level select **No authorization required**, then bind the required
   **Authorization header input** privately to `Bearer YOUR_API_TOKEN`. This
   describes Coze's transport configuration: the Ace Data Cloud API still
   requires a valid caller-owned credential with the relevant API permissions.
   Usage is billed to that caller's account. Do not put credentials in prompts,
   shared examples, default values or exported workflows.
4. Enable a tool before testing it. Imports may display **Failed** by default
   before any trial is run; that label is not provider failure evidence.
5. Run an authorized minimal test. For asynchronous tools, submit once, retain
   `task_id`, then retrieve its matching task until completion. Inspect the
   actual media or content and the usage record. Do not retry a submission just
   because a request timed out; first determine whether it created a task.
6. Keep real-token debug results unsaved as examples. Coze's Request preview
   retains the token captured at run time even after an input is replaced.
7. Prepare the privacy declaration, running examples, category, About and
   Scenarios for review. **Workspace Publish** and **store Submit** are separate
   actions. Neither should be performed during a review hold.

## Compatibility and limits

Streaming is disabled for JSON tools. Async-capable creation tools default to
submission plus polling. Callback URLs are optional. Conditional request fields
and union constraints are retained, with top-level fields exposed for Coze's
importer. API defaults and supported models come from the dated public contract;
there is no fallback model substitution.

Binary speech, multipart transcription, live sessions and streaming-only routes
need a tested adapter. Internal routes and APIs whose documents are not publicly
listed are excluded. DeepSeek uses the explicitly published DeepSeek model subset on the AI Dialogue
conversation API; its hidden brand-specific API remains excluded. Some Suno management operations require owned
resources and separate authorization; their presence in a schema does not mean
those actions were executed or validated.

Coze OAuth and MCP support must be verified separately. This batch does not claim
one-click OAuth account connection. A publisher-funded shared token is not used.
Users still need to bind a private credential before a functional API call.

## Rebuild and verify

The public snapshot is a review input, not a replacement for the live platform
catalog. Refresh it from anonymous public service and document APIs when service
visibility changes, keeping private/internal contracts out of the import set.

```bash
pip install 'PyYAML>=6,<7' 'openapi-spec-validator>=0.7,<0.8' 'Pillow>=11,<12'
python coze/build_catalog.py
python coze/build_imports.py
python coze/build_icons.py
python coze/build_review.py --output /absolute/path/review.html
python -m unittest discover -s tests -v
```

Pass `--drafts /absolute/path/coze-drafts.json` to the review builder to overlay
verified workspace evidence. Keep live workspace IDs, credentials and operational
logs outside the public source snapshot. Review artifacts can link to those
private workspace drafts without publishing them in this repository.

Official Coze guides: [plugin import](https://www.coze.com/open/docs/guides/plugin_import)
and [OAuth plugins](https://www.coze.com/open/docs/guides/oauth_plugin).

Use `--apps-evidence /absolute/path/coze-app-drafts.json` with the review builder
to overlay saved Agent drafts. Review choices and notes are browser-local and
can be exported as JSON; they never publish anything.
