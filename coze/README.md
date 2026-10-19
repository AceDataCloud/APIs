# Coze service plugins

Use a service-specific plugin to add music, image or video tools to a Coze Agent
or Workflow. Ace Data Cloud provides these integrations and bills API usage to
the caller's Ace account. They are not endorsements by the model brands or
entries in Coze's default model-provider selector.

## Find your service and get started

Search by the service name and confirm the publisher is **AceDataCloud**. The
prepared titles below identify the integration provider; approved store titles
and versions still require a separate readback. A source file is not a store
installation.

| Independent service entry | Official international listing | English / 简体中文 | Latest dated evidence |
|---|---|---|---|
| Suno by Ace Data Cloud | [Suno](https://www.coze.com/store/plugin/7695633467463286837) | [Guide](guides/suno/README.md) / [教程](guides/suno/README_zh-CN.md) | Submitted 2026-10-12; 12 enabled tools; current approval unknown |
| Seedance by Ace Data Cloud | No verified listing yet | [Guide](guides/seedance/README.md) / [教程](guides/seedance/README_zh-CN.md) | Prepared text-only two-tool import; not submitted or host-verified |
| HappyHorse by Ace Data Cloud | No verified listing yet | [Guide](guides/happyhorse/README.md) / [教程](guides/happyhorse/README_zh-CN.md) | Prepared two-tool import; not submitted or host-verified |
| GPT Image by Ace Data Cloud | [GPT Image](https://www.coze.com/store/plugin/7695652131059187765) | [Guide](guides/gpt-image/README.md) / [教程](guides/gpt-image/README_zh-CN.md) | Submitted 2026-10-12; three enabled tools; current approval unknown |
| Nano Banana by Ace Data Cloud | [Nano Banana](https://www.coze.com/store/plugin/7693585509326815285) | [Guide](guides/nano-banana/README.md) / [教程](guides/nano-banana/README_zh-CN.md) | Older version installed/tested 2026-10-11; description update under review 2026-10-12 |

The 2026-10-12 documentation-update receipts put all 14 initial listing updates
back under review, including the six approved older versions. Suno and GPT Image
bring the recorded submissions to 16. No authenticated 2026-10-18 review or
version readback is available in this source update. Use existing plugin IDs
when updating an entry; do not create duplicate submissions.

Each guide covers the official entry, registration, General application,
API-token copying/creation, private Coze `Reference → adc_auth` binding, first
use and same-task retrieval. Existing redacted Ace screenshots and unmodified
Coze China documentation screenshots have dated [source records](_assets/tutorial/sources.json).
The China images illustrate another plugin and do not establish an Ace install
or the international editor's current layout.

## Native model-provider status

The [current Coze China model guide](https://docs.coze.cn/guides_model) separates
its adapted provider selector from custom Chat/Responses/Messages connections.
Ace Data Cloud is not in that documented provider list. A custom connection can
be useful but does not constitute default-provider inclusion. The low-code
[enterprise custom-model route](https://docs.coze.cn/guides_deploy_custom_model)
has its own plan/administrator requirements.

The open-source [Coze Studio provider registry](https://github.com/coze-dev/coze-studio/blob/fefb05ff27be1da939612fbf9faf5db62583b8ae/backend/bizpkg/config/modelmgr/mode_provider.go)
and [contribution guide](https://github.com/coze-dev/coze-studio/blob/fefb05ff27be1da939612fbf9faf5db62583b8ae/CONTRIBUTING.md)
are a separate upstream route. A template using OpenAI protocol still belongs
to that protocol's provider group; it is not a new Ace provider and does not
change either commercial Coze region. Default inclusion and public plugin-store
discovery remain separate release goals.

## Developer catalog

This launch review covers 33 API plugin entries across 32 services, including a
separate GPT Image entry, and seven developer/deployment guides.
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
| GPT Image | OpenAI image subset | 3 | [Contract](plugins/gpt-image.yaml) |
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

## Suno and standalone GPT Image (checked 2026-10-12)

[GPT Image](https://www.coze.com/store/plugin/7695652131059187765) is a separate
three-tool plugin: image generation, editing and completed task retrieval.
It uses the existing OpenAI image routes and GPT Image model family. The
existing OpenAI plugin retains its current tools. Generation and editing both
returned completed images through Coze; the edited image changed the requested
teapot color. Its store submission is **Under Review**.

[Suno](https://www.coze.com/store/plugin/7695633467463286837) now has a submitted
HTTP plugin with caller-owned Authorization, independent of the unpublished
native MCP draft. Its **12 enabled tools** passed real Coze calls and have saved,
redacted examples: music generation, default-model lyrics, style refinement,
voice-reference creation from authorized audio, persona listing, audio upload,
lyric timing, vocal-segment extraction, MP3/WAV export, MIDI note data and task
retrieval. Two generated songs and completed MP3/WAV assets returned HTTP 200.
The store submission is **Under Review**; public installation and installed-Agent
verification for these two new entries await approval.

The Coze projections declare actual lyrics/style/upload objects, aligned words,
export `file_url` values and MIDI instruments/notes, which Coze otherwise drops
or rejects. MIDI is structured note data, not a downloadable MIDI file.
Vocal extraction uses synchronous output in this form, and its result URL may
expire. Timing, MIDI and vocal extraction passed using an uploaded, owned audio
ID after the generated ID was rejected. The timing example is an excerpt of the
real response. Use only authorized audio and obtain consent for voice references.

Five advanced Suno tools remain disabled: direct persona creation from a song ID
rejected both tested source kinds; MP4 export returned a service error; lyric
blending returned 404; custom-model listing timed out in Coze; studio project
management was not validated. Persona deletion is not exposed or tested. These
limits are explicit in the store description; full native-MCP parity is not
claimed. Provider routing, prices and billing rules are unchanged.

`imports/suno.json` and `imports/suno.yaml` contain only these 12 verified tools.
The five disabled tools and unexercised persona deletion remain solely in the
full `plugins/suno.*` contracts. Re-import the reduced projection to preserve
the submitted scope; do not import the full contract as a tested store release.

## Initial batch checks (2026-10-11)

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
The October 12 continuation adds the Suno HTTP plugin and the separate GPT Image
entry, bringing confirmed submissions to 16 of 33 entries. The other 17 remain
outside these submitted batches. Suno's native MCP draft remains unpublished
because caller OAuth is blocked. Installation and Agent E2E are verified only
for the six initial approved items above, not every prepared schema or MCP
capability.
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

For keyless checks against pinned official Coze Studio import/parameter-mapping
code, see [the reproducible component verification](validation/studio_import/README.md).
It covers JSON/YAML import, request/response fields and blank/reference credential
mapping without sending a service request. It is separate from authenticated
commercial-host installation, permissions, live errors, media and billing.

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
