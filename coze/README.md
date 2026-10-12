# Coze service plugins

This launch review covers 32 API plugins and seven developer/deployment guides.
Names use the service brand, spaces instead of underscores, and `Resolver` for
CAPTCHA services. Fish uses its short brand name. Datasets, Digital Human,
Dreamina, AI Chat and the earlier cross-service Agent concepts are excluded by
`catalog/launch-scope.json`. Historical source snapshots retain provenance and
are not the active launch list.

## Get your Ace Data Cloud API key

1. Open [Ace Data Cloud → Applications](https://platform.acedata.cloud/console/applications?utm_source=github&utm_medium=referral&utm_campaign=evergreen&utm_content=coze_api_readme_api_key). Sign in, or register an account first.
2. Find **General application**. If it has not been created, choose **Initialize General Application**. A general key can use the services available to your account; a dedicated application's key is limited to its service. Check the required service/model access and [current pricing](https://platform.acedata.cloud/models?utm_source=github&utm_medium=referral&utm_campaign=evergreen&utm_content=coze_api_readme_pricing).
3. Copy the **API Key** from the application card, or open **Keys / Manage Keys → Create** to create a separate key for this integration. Give it a recognizable name so you can revoke or rotate it independently.
4. When creating a key, review **Expiration Time**, **Set Usage Limitation**, and **Allowed APIs**. Enable only the restrictions you need, allow the operations you will call, then click **Create** and copy the token from the key list. Task lookup does not grant permission to submit a generation. Confirm the application's balance can cover your first request; any trial allowance is whatever your account currently displays.
5. Copy only the token value, without quotation marks, spaces, or `Bearer `. An API Key / API Token field expects this raw value; only a manually configured HTTP `Authorization` header needs the `Bearer ` prefix. A `platform-...` account-management token cannot replace a generation API key.

![Copy an application API key or open Manage Keys](https://raw.githubusercontent.com/AceDataCloud/NanoBananaDify/2522b2f57210597af2db866445319334a1677a23/_assets/tutorial/get-api-key-en.png)

![Create a separately named key with optional restrictions](https://raw.githubusercontent.com/AceDataCloud/NanoBananaDify/2522b2f57210597af2db866445319334a1677a23/_assets/tutorial/create-api-key-en.png)

Save the key in Coze's private credential configuration described below. Never put it in a prompt, shared workflow, screenshot, or Git commit. If authentication fails, check the full copied value, application/service access, expiration, usage limit, and balance before creating another key.

## Configure a private user credential

After installing a store plugin, bind its `Authorization` parameter using
**Reference** to your private `adc_auth` variable. Its value is
`Bearer <your application API key>`. Exclude the variable from prompts, keep its
shared default empty, and set the value for the current debug session before
testing. Read back the saved binding; a fixed Input default can be replaced by
a model-generated placeholder. Each user supplies their own key and pays from
their own account. A private Service token is not a public multi-user default.

## Icons

Official brand assets are recorded in `catalog/official-icons.json` and retained
in `icons/official/`. The builder scales originals to a 512px canvas; the review
UI adds no inner padding. Fish uses the clearer matching mark from our Fish MCP,
and Qwen Image uses the official Qwen favicon rather than the generic Alibaba
logo. Gemini, Veo and GLM receive an optical crop of excess white margins
without cutting the brand mark. These three revised draft icons were also
uploaded and checked in Coze on 2026-10-06.

`catalog/icon-overrides.json` selects custom GPT Image 2 utility icons for Identity
Verification, Web Extractor and Localization. Originals are in `icons/custom/`;
the exact prompt set and model are in `catalog/generated-icon-prompts.json`.
These three images were generated through the AceDataCloud GPT Image API and
visually checked before use. They are custom utility artwork, not official
third-party brand logos. No publisher badge or added service-name caption is used.

## MCP capability baseline

Use the full corresponding MCP's business capabilities as the acceptance
baseline, not the number of HTTP routes. The inventory has 25 dedicated MCP
matches, with live tools/list evidence for 21 hosted services. For example,
Suno exposes 42 live tools, while its 18 prepared HTTP operations are a separate
inventory. Generation, editing, batch retrieval, management, model discovery
and usage guidance all count.

| Service plugin | MCP target tools | Prepared HTTP operations | Contract |
|---|---:|---:|---|
| DeepSeek | No dedicated MCP | 1 | [Contract](plugins/deepseek.yaml) |
| Claude | No dedicated MCP | 3 | [Contract](plugins/claude.yaml) |
| Maestro | 3 | 2 | [Contract](plugins/maestro.yaml) |
| Turnstile Resolver | 4 | 2 | [Contract](plugins/turnstile.yaml) |
| CAPTCHA OCR Resolver | 4 | 2 | [Contract](plugins/image2text.yaml) |
| Kimi | No dedicated MCP | 1 | [Contract](plugins/kimi.yaml) |
| Hailuo | 6 | 2 | [Contract](plugins/hailuo.yaml) |
| OpenAI | 15 | 6 | [Contract](plugins/openai.yaml) |
| Gemini | No dedicated MCP | 4 | [Contract](plugins/gemini.yaml) |
| Grok | 8 | 3 | [Contract](plugins/grok.yaml) |
| Veo | 8 | 2 | [Contract](plugins/veo.yaml) |
| Google Search | 11 | 1 | [Contract](plugins/serp.yaml) |
| Luma | 8 | 2 | [Contract](plugins/luma.yaml) |
| Identity Verification | No dedicated MCP | 10 | [Contract](plugins/identity.yaml) |
| Seedance | 7 | 2 | [Contract](plugins/seedance.yaml) |
| reCAPTCHA Resolver | 5 | 4 | [Contract](plugins/recaptcha.yaml) |
| hCaptcha Resolver | 5 | 3 | [Contract](plugins/hcaptcha.yaml) |
| Qwen Image | No dedicated MCP | 2 | [Contract](plugins/qwen-image.yaml) |
| Short URL | 4 | 1 | [Contract](plugins/shorturl.yaml) |
| Web Extractor | 5 | 3 | [Contract](plugins/webextrator.yaml) |
| Producer | 18 | 6 | [Contract](plugins/producer.yaml) |
| Nano Banana | 4 | 2 | [Contract](plugins/nano-banana.yaml) |
| Wan | 8 | 2 | [Contract](plugins/wan.yaml) |
| Suno | 42 | 18 | [Contract](plugins/suno.yaml) |
| HappyHorse | 7 | 2 | [Contract](plugins/happyhorse.yaml) |
| Kling | 15 | 7 | [Contract](plugins/kling.yaml) |
| Localization | No dedicated MCP | 1 | [Contract](plugins/localization.yaml) |
| Fish | 6 | 5 | [Contract](plugins/fish.yaml) |
| MiniMax | 10 | 2 | [Contract](plugins/minimax.yaml) |
| GLM | 3 | 1 | [Contract](plugins/glm.yaml) |
| Seedream | 7 | 2 | [Contract](plugins/seedream.yaml) |
| FLUX | 7 | 3 | [Contract](plugins/flux.yaml) |

`catalog/mcp-parity.json` preserves source and live metadata provenance.
`mcp-plugins/` holds native MCP configuration targets; these are not native Coze
exports. `examples/catalog/mcp-validation-cases.json` references every benchmark
tool without authorizing its execution. Some MCPs have no verified hosted
transport; seven API services have no dedicated corresponding MCP.

The public invalid marker `COZE_METADATA_ONLY_INVALID_TOKEN` may be used only for
metadata discovery on service MCPs that deliberately defer API validation to the
actual service call. It is not a credential and grants no service access. Remove
it and configure caller-owned authorization before release. No paid tools/call
was executed for metadata discovery.

## Current release gate (checked 2026-10-11)

Fourteen HTTP plugins have confirmed store submission receipts, covering 32
currently enabled tools. The authenticated store and installed-Agent check on
2026-10-11 recorded:

- **Approved, found in the store and verified after installation:** Localization,
  Short URL, Google Search, DeepSeek, Nano Banana and Qwen Image. The private
  verification Agent exercised eight distinct tools with real results and
  matching billing records.
- **Under Review:** Kimi, GLM, Grok, Claude, Web Extractor, Gemini, Fish and OpenAI.
  No rejection was shown. Store installation and Agent verification await approval.

Workspace publication, store submission, approval, public discoverability and
installed-Agent execution are separate gates. These are dated results, not a
2026-10-12 store readback. Approved store versions still need to be reconciled
with this source catalog. See [the continuation PR](https://github.com/AceDataCloud/APIs/pull/956)
for the operational record; private evidence and credentials remain outside Git.

Localization returned translated Markdown; Short URL returned a verified 302
redirect; Google Search returned real links; DeepSeek returned the requested
text. Nano Banana and Qwen Image returned completed, viewable images. Qwen reached
Coze's 10-operation limit while polling; a subsequent Agent turn retrieved the
same completed task rather than submitting another generation.

The installed-Agent verification exposed the private variable binding issue
covered above. Temporary test credentials were expired, and both shared/default
and runtime variable values were cleared after verification.

Gemini's four tools passed fresh calls. OpenAI's five enabled tools returned text
and completed image results; embeddings returned HTTP 500 and is disabled for
this version. Fish's four enabled tools returned an MP3, voice-list entries and
voice details; custom voice creation returned a reference-audio download error
and is disabled. Both reduced scopes were published as workspace v0.0.2 and
submitted with explicit store-copy limitations. No failed tool was given a
fabricated successful example. Localization remains Markdown/plain-text only;
its store copy explicitly excludes JSON-object translation.

Grok, Gemini and OpenAI task outputs now explicitly retain media URLs, completion
details, costs and errors for single and batch retrieval. The OpenAI import
preserves pagination metadata. Fish voice-list output declares IDs, titles,
license metadata and pagination bounds, so Coze does not return empty entries.
The same completed tasks were read again through Coze after output fixes,
without repeating generation. These changes do not alter provider routing,
authentication or billing rules.

### Earlier validation and scope

The local `e2e-v4/launch-gate.json` evidence file is the
per-service evidence index; the generated review accepts it with
`--e2e-evidence`. Fifteen services have verified real Coze tool calls:
Suno (native MCP generation, task retrieval, two reachable MP3 results),
DeepSeek, Short URL, Google Search, Web Extractor, Kimi, OpenAI, Claude,
Gemini, Grok, GLM, Nano Banana, Qwen Image, Fish and Localization.
Localization is limited to Markdown text translation; JSON-object translation
remains unverified. `build_batch_review.py` creates a separate first-batch
review page with names, icons, copy, draft links and proof for these 15.
The 21 hosted MCP inventories and 19 free information calls were direct MCP
checks, separate from Coze execution. The earlier 23-service API batch was
direct API testing, separate from both.

Short URL and Google Search also returned usable results from real Coze draft calls.
Web Extractor originally submitted and completed an owned task, but Coze stripped
its dynamic response object. Its output contract now declares explicit content
fields for single and batch retrieval. The Coze draft was updated and the same
task returned a title, text and Markdown through Coze.

OpenAI, Claude and Kimi exposed a Coze editor problem: it validates required
children of optional nested inputs even when unused. Their text-chat import
projections omit inactive optional objects and message tool-call children while
the canonical public contracts retain them. The three projections were reimported,
their chat tools enabled and real assistant text returned through Coze. This
verifies text chat only; it does not establish their full multimodal/tool parity.
Gemini, Grok and GLM use chat-only reimports that leave other tools in their
existing drafts. Nano Banana and Qwen Image task results now return image URLs
after Coze output parsing. Fish returns an async task ID, then an audio URL;
both image and audio assets returned HTTP 200.

Localization's union input imported into Coze as an untyped field, so the editor
omitted the required input. A Markdown-only import projection was tested through
Coze and returned Chinese text; JSON-object translation and the earlier direct
API failure remain open.

The documented Coze standard OAuth flow omits a PKCE challenge and sends JSON to
the token endpoint; the hosted MCP OAuth endpoint currently requires PKCE and
form fields. User connection therefore remains blocked. The existing temporary
Suno header was restored to a public invalid metadata marker after the test.
The Suno native MCP draft remains unpublished so it does not expose a connection
that cannot make authenticated calls.

After the user's first-batch publish authorization, 14 HTTP plugins were published
as Coze workspace version v0.0.1: DeepSeek, Short URL, Google Search, Web
Extractor, Claude, OpenAI, Kimi, Gemini, Grok, GLM, Nano Banana, Qwen Image,
Fish and Localization. The latter exposes only the verified Markdown form. This
workspace publication is separate from Plugin Store submission: the store flow
asks for a running example for each tool. The subsequent confirmed submissions
are listed above. The later installed-Agent check covers the six approved plugins
listed above; the other eight still await store approval. The pre-handoff test
credentials were expired and read back. The pre-handoff
ledger was 29.372048470 Credits of the approved 200-Credit cap; continuation
usage is tracked separately in the local credential readbacks.

## Contracts, trials and publication

`plugins/` contains full public HTTP contracts. `imports/` records Coze-compatible
projections for Claude, OpenAI, Kimi, Gemini chat, Grok chat, GLM chat,
Fish TTS and voice listing, Localization Markdown, Nano Banana/Qwen Image tasks,
Grok/Gemini video tasks, OpenAI image tasks, Kling and
Google Search, with explicit limitations.
They are supplementary preparation and do not establish complete MCP parity.
Suno persona deletion is included in the definition, but all destructive and
sensitive fixtures require their own explicit execution scope.

Keep credentials out of prompts, examples, exports and version control. Coze
Request previews can retain a token even after an input field is edited. Build
the saved request with a redacted Authorization value, retain the real response,
then read the persisted example back before publication. Never publish a
real-token example or treat a request template as a successful runtime result.
Imported `Failed` labels before testing are not provider-failure evidence.
Previous API tests do not prove revised native MCP or Coze runtime success.

The user authorized publication of the reviewed first batch on 2026-10-06.
The other 17 catalog plugins are outside that batch; Suno remains a separate
unpublished native MCP draft because caller OAuth is blocked. Across the 32 HTTP
catalog entries, 18 have not been submitted (those 17 plus Suno). Installation
and Agent E2E are verified only for the six approved items above, not every
prepared schema or MCP capability.
Removed services are excluded from the launch materials; historical private Coze
drafts are not automatically or permanently deleted by these builders.

## Store copy and acquisition links

The generated `listings.json` is review material. Its setup links retain the
legacy `from=coze` marker and add `utm_source=coze`, `utm_medium=referral`,
`utm_campaign=evergreen` and a service-specific `utm_content`. Updating source
copy does not update an already approved listing. Before a store update, carry
over the API-key setup steps, read back the saved private binding instructions
and URL parameters, then verify the approved listing after review. Tagged links
alone do not prove registrations, first calls or revenue attribution.

## Current host documentation

On 2026-10-12, the [current Coze China plugin documentation](https://docs.coze.cn/create-plugin)
describes Skill/MCP/optional Panel bundles imported as Agent Plugins 1.0.0 ZIPs,
and separates publication from enterprise-team-store listing. These HTTP
OpenAPI assets and native MCP targets are not that bundle format. Verify the
actual host, region and distribution contract before reusing or uploading them;
historical HTTP Plugin Store evidence does not establish listing in the newer
China extension center. Each user must configure their own authorization.

## Rebuild

```bash
pip install 'PyYAML>=6,<7' 'openapi-spec-validator>=0.7,<0.8' 'Pillow>=11,<12' 'CairoSVG>=2.7,<3'
python coze/build_catalog.py
python coze/build_imports.py
python coze/build_icons.py
python coze/build_mcp_inventory.py --mcp-root /absolute/path/MCPs --check-live
python coze/build_review.py --output /absolute/path/review.html
python coze/build_batch_review.py --evidence-root /absolute/path/evidence --output /absolute/path/evidence/review-batch-1.html
python -m unittest discover -s tests -v
```

The review builder accepts `--drafts`, `--trials` and `--native-evidence` paths.
Review notes are stored only in the browser and can be exported as JSON; the page
never publishes. Keep private workspace IDs and operational logs outside the repo.
